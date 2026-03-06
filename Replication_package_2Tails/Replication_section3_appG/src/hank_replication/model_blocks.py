"""Model blocks used by the replication package."""

from __future__ import annotations

import numpy as np
import sequence_jacobian as sj
from numba import njit, vectorize


# Heterogenous agents block for the Homogeneous labor model


def hh_init_hom(a_grid, we, r, eis, T):
    fininc = (1 + r) * a_grid + T[:, np.newaxis] - a_grid[0]
    coh = (1 + r) * a_grid[np.newaxis, :] + we[:, np.newaxis] + T[:, np.newaxis]
    Va = (1 + r) * coh ** (-1 / eis)
    return Va, fininc


@sj.het(exogenous="Pi", policy="a", backward="Va", backward_init=hh_init_hom)
def hh_hom(Va_p, a_grid, we, r, beta, eis, T):
    uc_nextgrid = beta * Va_p
    c_nextgrid = uc_nextgrid ** (-eis)
    coh = (1 + r) * a_grid[np.newaxis, :] + we[:, np.newaxis] + T[:, np.newaxis]
    a = sj.interpolate.interpolate_y(c_nextgrid + a_grid, coh, a_grid)
    sj.misc.setmin(a, a_grid[0])
    c = coh - a
    Va = (1 + r) * c ** (-1 / eis)
    return Va, a, c


# Heterogenous agents block for the Heterogenous labor model


def hh_init_het(a_grid, we, r, eis, T):
    fininc = (1 + r) * a_grid + T[:, np.newaxis] - a_grid[0]
    coh = (1 + r) * a_grid[np.newaxis, :] + we[:, np.newaxis] + T[:, np.newaxis]
    Va = (1 + r) * (0.1 * coh) ** (-1 / eis)
    return fininc, Va


@sj.het(exogenous="Pi", policy="a", backward="Va", backward_init=hh_init_het)
def hh_het(Va_p, a_grid, we, T, r, beta, eis, frisch, vphi):
    uc_nextgrid = beta * Va_p
    c_nextgrid, n_nextgrid = cn(uc_nextgrid, we[:, np.newaxis], eis, frisch, vphi)

    lhs = c_nextgrid - we[:, np.newaxis] * n_nextgrid + a_grid[np.newaxis, :] - T[:, np.newaxis]
    rhs = (1 + r) * a_grid
    c = sj.interpolate.interpolate_y(lhs, rhs, c_nextgrid)
    n = sj.interpolate.interpolate_y(lhs, rhs, n_nextgrid)

    a = rhs + we[:, np.newaxis] * n + T[:, np.newaxis] - c
    iconst = np.nonzero(a < a_grid[0])
    a[iconst] = a_grid[0]

    if iconst[0].size != 0 and iconst[1].size != 0:
        c[iconst], n[iconst] = solve_cn(
            we[iconst[0]],
            rhs[iconst[1]] + T[iconst[0]] - a_grid[0],
            eis,
            frisch,
            vphi,
            Va_p[iconst],
        )

    Va = (1 + r) * c ** (-1 / eis)
    return Va, a, c, n


@njit
def cn(uc, w, eis, frisch, vphi):
    return uc ** (-eis), (w * uc / vphi) ** frisch


def solve_cn(w, T, eis, frisch, vphi, uc_seed):
    uc = solve_uc(w, T, eis, frisch, vphi, uc_seed)
    return cn(uc, w, eis, frisch, vphi)


@vectorize
def solve_uc(w, T, eis, frisch, vphi, uc_seed):
    log_uc = np.log(uc_seed)
    for _ in range(30):
        ne, ne_p = netexp(log_uc, w, T, eis, frisch, vphi)
        if abs(ne) < 1e-11:
            break
        log_uc -= ne / ne_p
    else:
        raise ValueError("Cannot solve constrained household's problem: No convergence after 30 iterations!")

    return np.exp(log_uc)


@njit
def netexp(log_uc, w, T, eis, frisch, vphi):
    c, n = cn(np.exp(log_uc), w, eis, frisch, vphi)
    ne = c - w * n - T

    c_loguc = -eis * c
    n_loguc = frisch * n
    netexp_loguc = c_loguc - w * n_loguc
    return ne, netexp_loguc


# Define heterogenous inputs for both models


def make_grids(rho_e, sd_e, n_e, min_a, max_a, n_a):
    e_grid, pi_e, Pi = sj.grids.markov_rouwenhorst(rho_e, sd_e, n_e)
    a_grid = sj.grids.asset_grid(min_a, max_a, n_a)
    return e_grid, pi_e, Pi, a_grid


def transfers(pi_e, Div, Tax, e_grid):
    tax_rule, div_rule = e_grid, e_grid
    div = Div / np.sum(pi_e * div_rule) * div_rule
    tax = Tax / np.sum(pi_e * tax_rule) * tax_rule
    T = div - tax
    return T


def wages_hom(w, e_grid, N):
    we = w * e_grid * N
    return we


def wages_het(w, e_grid):
    we = w * e_grid
    return we


# Define heterogeneous outputs for both models


def labor_supply(n, e_grid):
    ne = e_grid[:, np.newaxis] * n
    return ne


def compute_weighted_mpc(c, a, a_grid, r, e_grid):
    mpc = np.empty_like(c)
    post_return = (1 + r) * a_grid
    mpc[:, 1:-1] = (c[:, 2:] - c[:, 0:-2]) / (post_return[2:] - post_return[:-2])
    mpc[:, 0] = (c[:, 1] - c[:, 0]) / (post_return[1] - post_return[0])
    mpc[:, -1] = (c[:, -1] - c[:, -2]) / (post_return[-1] - post_return[-2])
    mpc[a == a_grid[0]] = 1
    mpc = mpc * e_grid[:, np.newaxis]
    return mpc


def compute_htm(a, a_grid):
    htm = np.zeros_like(a)
    htm[a == a_grid[0]] = 1
    return htm


def compute_consumption(c):
    c0_2 = np.zeros_like(c)
    c2_11 = np.zeros_like(c)
    c11_34 = np.zeros_like(c)
    c34_66 = np.zeros_like(c)
    c66_89 = np.zeros_like(c)
    c89_98 = np.zeros_like(c)
    c98_100 = np.zeros_like(c)
    c0_2[0, :] = c[0, :]
    c2_11[1, :] = c[1, :]
    c11_34[2, :] = c[2, :]
    c34_66[3, :] = c[3, :]
    c66_89[4, :] = c[4, :]
    c89_98[5, :] = c[5, :]
    c98_100[6, :] = c[6, :]
    return c0_2, c2_11, c11_34, c34_66, c66_89, c89_98, c98_100


def compute_assets(a):
    a0_2 = np.zeros_like(a)
    a2_11 = np.zeros_like(a)
    a11_34 = np.zeros_like(a)
    a34_66 = np.zeros_like(a)
    a66_89 = np.zeros_like(a)
    a89_98 = np.zeros_like(a)
    a98_100 = np.zeros_like(a)
    a0_2[0, :] = a[0, :]
    a2_11[1, :] = a[1, :]
    a11_34[2, :] = a[2, :]
    a34_66[3, :] = a[3, :]
    a66_89[4, :] = a[4, :]
    a89_98[5, :] = a[5, :]
    a98_100[6, :] = a[6, :]
    return a0_2, a2_11, a11_34, a34_66, a66_89, a89_98, a98_100


def compute_labor(ne):
    l0_2 = np.zeros_like(ne)
    l2_11 = np.zeros_like(ne)
    l11_34 = np.zeros_like(ne)
    l34_66 = np.zeros_like(ne)
    l66_89 = np.zeros_like(ne)
    l89_98 = np.zeros_like(ne)
    l98_100 = np.zeros_like(ne)
    l0_2[0, :] = ne[0, :]
    l2_11[1, :] = ne[1, :]
    l11_34[2, :] = ne[2, :]
    l34_66[3, :] = ne[3, :]
    l66_89[4, :] = ne[4, :]
    l89_98[5, :] = ne[5, :]
    l98_100[6, :] = ne[6, :]
    return l0_2, l2_11, l11_34, l34_66, l66_89, l89_98, l98_100


def compute_labor_1(n):
    n0_2 = np.zeros_like(n)
    n2_11 = np.zeros_like(n)
    n11_34 = np.zeros_like(n)
    n34_66 = np.zeros_like(n)
    n66_89 = np.zeros_like(n)
    n89_98 = np.zeros_like(n)
    n98_100 = np.zeros_like(n)
    n0_2[0, :] = n[0, :]
    n2_11[1, :] = n[1, :]
    n11_34[2, :] = n[2, :]
    n34_66[3, :] = n[3, :]
    n66_89[4, :] = n[4, :]
    n89_98[5, :] = n[5, :]
    n98_100[6, :] = n[6, :]
    return n0_2, n2_11, n11_34, n34_66, n66_89, n89_98, n98_100


# Define GE blocks for the Steady State DAG


@sj.simple
def firm_hom(Y, w, Z, pi, mu, kappa):
    L = Y / Z
    Div = Y - w * L - mu / (mu - 1) / (2 * kappa) * (1 + pi).apply(np.log) ** 2 * Y
    return L, Div


@sj.simple
def LSss_hom(w, frisch, N, eis, Y):
    vphi = w / ((N) ** (1 / frisch) * (Y) ** (1 / eis))
    return vphi


@sj.simple
def LS_hom(frisch, vphi, N, eis, Y):
    w = vphi * (Y) ** (1 / eis) * N ** (1 / frisch)
    return w


@sj.simple
def firm_het(Y, w, Z, pi, mu, kappa):
    L = Y / Z
    Div = Y - w * L - mu / (mu - 1) / (2 * kappa) * (1 + pi).apply(np.log) ** 2 * Y
    return L, Div


@sj.simple
def monetary(pi, rstar, phi):
    r = (1 + rstar(-1) + phi * pi(-1)) / (1 + pi) - 1
    return r


@sj.simple
def mkt_clearing_hom(A, Y, C, mu, kappa, pi, B, N, L):
    asset_mkt = A - B
    labor_mkt = N - L
    goods_mkt = C - Y + mu / (mu - 1) / (2 * kappa) * (1 + pi).apply(np.log) ** 2 * Y
    return asset_mkt, goods_mkt, labor_mkt


@sj.simple
def mkt_clearing_het(A, NE, C, L, Y, B, pi, mu, kappa):
    asset_mkt = A - B
    labor_mkt = NE - L
    goods_mkt = Y - C - mu / (mu - 1) / (2 * kappa) * (1 + pi).apply(np.log) ** 2 * Y
    return asset_mkt, labor_mkt, goods_mkt


@sj.simple
def nkpc_ss(mu):
    w = 1 / mu
    return w


@sj.simple
def fiscal(B, r):
    Tax = r * B
    return Tax


# Linearized dynamics using Jacobians


@sj.simple
def nkpc(pi, w, Z, Y, r, mu, kappa):
    nkpc_res = (
        kappa * (w / Z - 1 / mu)
        + Y(+1) / Y * (1 + pi(+1)).apply(np.log) / (1 + r(+1))
        - (1 + pi).apply(np.log)
    )
    return nkpc_res
