"""Plotting utilities for full replication output parity."""

from __future__ import annotations

from pathlib import Path
import shutil
from typing import Any

import matplotlib

matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


def _save_figure(fig, output_dir: Path, filename: str, dpi: int | None = None) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    if dpi is None:
        fig.savefig(path)
    else:
        fig.savefig(path, dpi=dpi)
    plt.close(fig)
    return filename


def plot_baseline_policy_functions(ss0_het: dict[str, Any], state_labels: list[str], output_dir: Path) -> list[str]:
    files: list[str] = []
    hh_het_internals = ss0_het.internals["hh_het"]

    fig, ax = plt.subplots()
    for i, label in enumerate(state_labels):
        ax.plot(hh_het_internals["a_grid"], hh_het_internals["n"][i], label=label)
    ax.legend()
    ax.set_xlabel("Assets")
    ax.set_ylabel("Labor supply")
    files.append(_save_figure(fig, output_dir, "labor_supply_vs_assets.png"))

    fig, ax = plt.subplots()
    for i, label in enumerate(state_labels):
        ax.plot(hh_het_internals["a_grid"], hh_het_internals["n"][i], label=label)
    ax.legend()
    ax.set_xlabel("Assets")
    ax.set_ylabel("Labor supply")
    ax.set_xlim(ss0_het["min_a"], 5)
    files.append(_save_figure(fig, output_dir, "labor_supply_vs_assets_zoomed.png"))

    fig, ax = plt.subplots()
    for i, label in enumerate(state_labels):
        ax.plot(hh_het_internals["a_grid"], hh_het_internals["c"][i], label=label)
    ax.legend()
    ax.set_xlabel("Assets")
    ax.set_ylabel("Consumption")
    files.append(_save_figure(fig, output_dir, "consumption_vs_assets.png"))

    return files


def plot_baseline_irfs(irf: dict[str, np.ndarray], ss_het: dict[str, Any], output_dir: Path) -> str:
    dY_lin = 100 * irf["Y"] / ss_het["Y"]
    dL0_2_lin = 100 * irf["L0_2"] / ss_het["L0_2"]
    dL2_11_lin = 100 * irf["L2_11"] / ss_het["L2_11"]
    dL11_34_lin = 100 * irf["L11_34"] / ss_het["L11_34"]
    dL34_66_lin = 100 * irf["L34_66"] / ss_het["L34_66"]
    dL66_89_lin = 100 * irf["L66_89"] / ss_het["L66_89"]
    dL89_98_lin = 100 * irf["L89_98"] / ss_het["L89_98"]
    dL98_100_lin = 100 * irf["L98_100"] / ss_het["L98_100"]
    dC0_2_lin = 100 * irf["C0_2"] / ss_het["C0_2"]
    dC2_11_lin = 100 * irf["C2_11"] / ss_het["C2_11"]
    dC11_34_lin = 100 * irf["C11_34"] / ss_het["C11_34"]
    dC34_66_lin = 100 * irf["C34_66"] / ss_het["C34_66"]
    dC66_89_lin = 100 * irf["C66_89"] / ss_het["C66_89"]
    dC89_98_lin = 100 * irf["C89_98"] / ss_het["C89_98"]
    dC98_100_lin = 100 * irf["C98_100"] / ss_het["C98_100"]
    dL_lin = 100 * irf["L"] / ss_het["L"]
    dC_lin = 100 * irf["C"] / ss_het["C"]
    dpi_lin = 10000 * irf["pi"]
    drtstar = 10000 * irf["rstar"]

    fig, axs = plt.subplots(2, 3, figsize=(12, 12))

    axs[0, 0].plot(drtstar[:16], linestyle="-", linewidth=2.5, color="blue")
    axs[0, 0].set_title(r"Interest Rate Shock ($r^*$)")
    axs[0, 0].set_xlabel("quarters")
    axs[0, 0].set_ylabel("Bp deviation from ss")
    axs[0, 0].grid(False)

    axs[0, 1].plot(dpi_lin[:16], linestyle="-", linewidth=2.5, color="orange")
    axs[0, 1].set_title(r"Inflation ($\pi$)")
    axs[0, 1].set_xlabel("quarters")
    axs[0, 1].set_ylabel("Bp deviation from ss")
    axs[0, 1].grid(False)

    axs[0, 2].plot(dY_lin[:16], linestyle="-", linewidth=2.5, color="green")
    axs[0, 2].set_title(r"Output ($Y$)")
    axs[0, 2].set_xlabel("quarters")
    axs[0, 2].set_ylabel("% deviation from ss")
    axs[0, 2].grid(False)

    axs[1, 0].plot(dL0_2_lin[:16], label="P0_2", linestyle=":", linewidth=2.5)
    axs[1, 0].plot(dL2_11_lin[:16], label="P2_11", linestyle="-.", linewidth=2.5)
    axs[1, 0].plot(dL11_34_lin[:16], label="P11_34", linestyle="--", linewidth=2.5)
    axs[1, 0].plot(dL34_66_lin[:16], label="P34_66", linestyle="-", linewidth=2.5, color="gray")
    axs[1, 0].plot(dL66_89_lin[:16], label="P66_89", linestyle="-", linewidth=2.5, color="darkgray")
    axs[1, 0].plot(dL89_98_lin[:16], label="P89_98", linestyle="-", linewidth=2.5, color="dimgray")
    axs[1, 0].plot(dL98_100_lin[:16], label="P98_100", linestyle="-", linewidth=2.5, color="lightgray")
    axs[1, 0].plot(dL_lin[:16], label="Aggregate", linestyle="-", linewidth=2.5, color="black")
    axs[1, 0].set_title("Labor Supply (H)")
    axs[1, 0].set_xlabel("quarters")
    axs[1, 0].set_ylabel("% deviation from ss")
    axs[1, 0].grid(False)

    axs[1, 1].plot(dC0_2_lin[:16], label="P0_2", linestyle=":", linewidth=2.5)
    axs[1, 1].plot(dC2_11_lin[:16], label="P2_11", linestyle="-.", linewidth=2.5)
    axs[1, 1].plot(dC11_34_lin[:16], label="P11_34", linestyle="--", linewidth=2.5)
    axs[1, 1].plot(dC34_66_lin[:16], label="P34_66", linestyle="-", linewidth=2.5, color="gray")
    axs[1, 1].plot(dC66_89_lin[:16], label="P66_89", linestyle="-", linewidth=2.5, color="darkgray")
    axs[1, 1].plot(dC89_98_lin[:16], label="P89_98", linestyle="-", linewidth=2.5, color="dimgray")
    axs[1, 1].plot(dC98_100_lin[:16], label="P98_100", linestyle="-", linewidth=2.5, color="lightgray")
    axs[1, 1].plot(dC_lin[:16], label="Aggregate", linestyle="-", linewidth=2.5, color="black")
    axs[1, 1].set_title("Consumption (C)")
    axs[1, 1].set_xlabel("quarters")
    axs[1, 1].set_ylabel("% deviation from ss")
    axs[1, 1].legend()
    axs[1, 1].grid(False)

    axs[1, 2].axis("off")
    fig.tight_layout()
    return _save_figure(fig, output_dir, "baseline_IRFs_with_L_and_C.png")


def plot_policy_functions_for_models(
    ss0_map: dict[str, Any],
    model_names: list[str],
    state_labels: list[str],
    output_dir: Path,
) -> list[str]:
    files: list[str] = []
    for name in model_names:
        hh_het_internals = ss0_map[name].internals["hh_het"]
        fig, ax = plt.subplots()
        for i, label in enumerate(state_labels):
            ax.plot(hh_het_internals["a_grid"], hh_het_internals["n"][i], label=label)
        ax.legend()
        ax.set_xlabel("Assets")
        ax.set_ylabel("Labor supply")
        files.append(_save_figure(fig, output_dir, f"labor_supply_vs_assets_{name}.png"))

        fig, ax = plt.subplots()
        for i, label in enumerate(state_labels):
            ax.plot(hh_het_internals["a_grid"], hh_het_internals["n"][i], label=label)
        ax.legend()
        ax.set_xlabel("Assets")
        ax.set_ylabel("Labor supply")
        ax.set_xlim(-1, 5)
        files.append(_save_figure(fig, output_dir, f"labor_supply_vs_assets_zoomed_{name}.png"))

        fig, ax = plt.subplots()
        for i, label in enumerate(state_labels):
            ax.plot(hh_het_internals["a_grid"], hh_het_internals["c"][i], label=label)
        ax.legend()
        ax.set_xlabel("Assets")
        ax.set_ylabel("Consumption")
        files.append(_save_figure(fig, output_dir, f"consumption_vs_assets_{name}.png"))

    return files


def plot_irfs_for_models(
    irfs_lin: dict[str, Any],
    ss_map: dict[str, Any],
    model_names: list[str],
    output_dir: Path,
) -> list[str]:
    files: list[str] = []

    for name in model_names:
        dY_lin = 100 * irfs_lin[name]["Y"] / ss_map[name]["Y"]
        dL_lin = 100 * irfs_lin[name]["L"] / ss_map[name]["L"]
        dC_lin = 100 * irfs_lin[name]["C"] / ss_map[name]["C"]
        dpi_lin = 10000 * irfs_lin[name]["pi"]
        drtstar = 10000 * irfs_lin[name]["rstar"]

        dL0_2_lin = 100 * irfs_lin[name]["L0_2"] / ss_map[name]["L0_2"]
        dL2_11_lin = 100 * irfs_lin[name]["L2_11"] / ss_map[name]["L2_11"]
        dL11_34_lin = 100 * irfs_lin[name]["L11_34"] / ss_map[name]["L11_34"]
        dL34_66_lin = 100 * irfs_lin[name]["L34_66"] / ss_map[name]["L34_66"]
        dL66_89_lin = 100 * irfs_lin[name]["L66_89"] / ss_map[name]["L66_89"]
        dL89_98_lin = 100 * irfs_lin[name]["L89_98"] / ss_map[name]["L89_98"]
        dL98_100_lin = 100 * irfs_lin[name]["L98_100"] / ss_map[name]["L98_100"]

        dC0_2_lin = 100 * irfs_lin[name]["C0_2"] / ss_map[name]["C0_2"]
        dC2_11_lin = 100 * irfs_lin[name]["C2_11"] / ss_map[name]["C2_11"]
        dC11_34_lin = 100 * irfs_lin[name]["C11_34"] / ss_map[name]["C11_34"]
        dC34_66_lin = 100 * irfs_lin[name]["C34_66"] / ss_map[name]["C34_66"]
        dC66_89_lin = 100 * irfs_lin[name]["C66_89"] / ss_map[name]["C66_89"]
        dC89_98_lin = 100 * irfs_lin[name]["C89_98"] / ss_map[name]["C89_98"]
        dC98_100_lin = 100 * irfs_lin[name]["C98_100"] / ss_map[name]["C98_100"]

        fig, axs = plt.subplots(2, 3, figsize=(12, 12))

        axs[0, 0].plot(drtstar[:16], linestyle="-", linewidth=2.5, color="blue")
        axs[0, 0].set_title(r"Interest Rate Shock ($r^*$)")
        axs[0, 0].set_xlabel("quarters")
        axs[0, 0].set_ylabel("Bp deviation from ss")

        axs[0, 1].plot(dpi_lin[:16], linestyle="-", linewidth=2.5, color="orange")
        axs[0, 1].set_title(r"Inflation ($\pi$)")
        axs[0, 1].set_xlabel("quarters")
        axs[0, 1].set_ylabel("Bp deviation from ss")

        axs[0, 2].plot(dY_lin[:16], linestyle="-", linewidth=2.5, color="green")
        axs[0, 2].set_title(r"Output ($Y$)")
        axs[0, 2].set_xlabel("quarters")
        axs[0, 2].set_ylabel("% deviation from ss")

        axs[1, 0].plot(dL0_2_lin[:16], label="P0_2", linestyle=":", linewidth=2.5)
        axs[1, 0].plot(dL2_11_lin[:16], label="P2_11", linestyle="-.", linewidth=2.5)
        axs[1, 0].plot(dL11_34_lin[:16], label="P11_34", linestyle="--", linewidth=2.5)
        axs[1, 0].plot(dL34_66_lin[:16], label="P34_66", color="gray", linewidth=2.5)
        axs[1, 0].plot(dL66_89_lin[:16], label="P66_89", color="darkgray", linewidth=2.5)
        axs[1, 0].plot(dL89_98_lin[:16], label="P89_98", color="dimgray", linewidth=2.5)
        axs[1, 0].plot(dL98_100_lin[:16], label="P98_100", color="lightgray", linewidth=2.5)
        axs[1, 0].plot(dL_lin[:16], label="Aggregate", color="black", linewidth=2.5)
        axs[1, 0].set_title("Labor Supply (H)")
        axs[1, 0].set_xlabel("quarters")
        axs[1, 0].set_ylabel("% deviation from ss")

        axs[1, 1].plot(dC0_2_lin[:16], label="P0_2", linestyle=":", linewidth=2.5)
        axs[1, 1].plot(dC2_11_lin[:16], label="P2_11", linestyle="-.", linewidth=2.5)
        axs[1, 1].plot(dC11_34_lin[:16], label="P11_34", linestyle="--", linewidth=2.5)
        axs[1, 1].plot(dC34_66_lin[:16], label="P34_66", color="gray", linewidth=2.5)
        axs[1, 1].plot(dC66_89_lin[:16], label="P66_89", color="darkgray", linewidth=2.5)
        axs[1, 1].plot(dC89_98_lin[:16], label="P89_98", color="dimgray", linewidth=2.5)
        axs[1, 1].plot(dC98_100_lin[:16], label="P98_100", color="lightgray", linewidth=2.5)
        axs[1, 1].plot(dC_lin[:16], label="Aggregate", color="black", linewidth=2.5)
        axs[1, 1].set_title("Consumption (C)")
        axs[1, 1].set_xlabel("quarters")
        axs[1, 1].set_ylabel("% deviation from ss")
        axs[1, 1].legend()

        axs[1, 2].axis("off")
        fig.tight_layout()
        files.append(_save_figure(fig, output_dir, f"IRFs_with_L_and_C_{name}.png"))

    return files


def plot_labor_supply_models_across_income(
    irfs_lin: dict[str, Any],
    ss_map: dict[str, Any],
    model_names: list[str],
    output_dir: Path,
    use_tex: bool,
) -> str:
    has_latex = bool(shutil.which("latex"))
    old_usetex = plt.rcParams.get("text.usetex", False)
    plt.rcParams["text.usetex"] = bool(use_tex and has_latex)

    variables = ["L0_2", "L2_11", "L11_34", "L34_66", "L66_89", "L89_98", "L98_100"]
    income_labels = ["P0_2", "P2_11", "P11_34", "P34_66", "P66_89", "P89_98", "P98_100"]

    model_styles = {
        "HANK-HetL EIS025 a0": {"color": "blue", "linestyle": "--"},
        "HANK-HetL a0": {"color": "red", "linestyle": "--"},
        "HANK-HetL EIS1 a0": {"color": "green", "linestyle": "--"},
        "HANK-HetL EIS025": {"color": "blue", "linestyle": "-"},
        "HANK-HetL": {"color": "red", "linestyle": "-"},
        "HANK-HetL EIS1": {"color": "green", "linestyle": "-"},
    }

    irfs_percent_dev: dict[str, list[float]] = {}
    for model in model_names:
        values: list[float] = []
        for var in variables:
            ss_value = ss_map[model][var]
            irf_value = irfs_lin[model][var][0]
            percent_dev = (irf_value / ss_value) * 100 if ss_value != 0 else np.nan
            values.append(float(percent_dev))
        irfs_percent_dev[model] = values

    fig, ax = plt.subplots(figsize=(10, 6))
    for model in model_names:
        style = model_styles.get(model, {})
        ax.plot(income_labels, irfs_percent_dev[model], marker="o", label=model, **style)

    ax.axhline(0, color="black", linewidth=1, linestyle="-")
    ax.set_ylim(-0.425, 0.55)
    ax.set_xlabel("Income Distribution")
    ax.set_ylabel(r"IRFs in Period 1 (\% Deviation from SS)")
    if plt.rcParams["text.usetex"]:
        legend_labels = [
            r"$\underline{a}=-0.5, \sigma=1$",
            r"$\underline{a}=-0.5, \sigma=0.5$",
            r"$\underline{a}=-0.5, \sigma=0.25$",
            r"$\underline{a}=0, \sigma=1$",
            r"$\underline{a}=0, \sigma=0.5$",
            r"$\underline{a}=0, \sigma=0.25$",
        ]
    else:
        legend_labels = [
            "a=-0.5, sigma=1",
            "a=-0.5, sigma=0.5",
            "a=-0.5, sigma=0.25",
            "a=0, sigma=1",
            "a=0, sigma=0.5",
            "a=0, sigma=0.25",
        ]
    ax.legend(legend_labels, loc="best")
    ax.grid(False)

    out = _save_figure(fig, output_dir, "labor_supply_models_across_income.png")
    plt.rcParams["text.usetex"] = old_usetex
    return out


def plot_het_labor_decomposition_bins(
    ge_jac_het: dict[str, Any],
    J_het: dict[str, Any],
    G_ha_het: dict[str, Any],
    shock_path: dict[str, np.ndarray],
    ss_het: dict[str, Any],
    income_labels: list[str],
    output_dir: Path,
) -> str:
    bin_keys = ["NE", "L0_2", "L2_11", "L11_34", "L34_66", "L66_89", "L89_98", "L98_100"]
    horizon = 10
    tt = np.arange(horizon)
    bcolor = ["darkblue", "red", "gold", "orange"]
    channels = ["r", "Div+Tax", "w"]

    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 10), sharex=True, sharey=False)
    axes = axes.flatten()
    index = 0

    for idx, key in enumerate(bin_keys):
        ax = axes[idx]
        yyoldminus = np.zeros(horizon)
        yyoldplus = np.zeros(horizon)
        dl_bin_lin_het = 100 * ge_jac_het[key]["rstar"] @ shock_path["rstar"] / ss_het[key]

        for iter_i, ch in enumerate(channels):
            if ch == "Div+Tax":
                yy_div = J_het[key].get("Div", 0) @ G_ha_het.get("Div", {}).get("rstar", 0) @ shock_path["rstar"]
                yy_tax = J_het[key].get("Tax", 0) @ G_ha_het.get("Tax", {}).get("rstar", 0) @ shock_path["rstar"]
                yy = (yy_div + yy_tax) / ss_het[key] * 100
            else:
                if ch not in J_het[key] or ch not in G_ha_het:
                    continue
                yy = J_het[key][ch] @ G_ha_het[ch]["rstar"] @ shock_path["rstar"] / ss_het[key] * 100

            ax.bar(tt, yy[:horizon].clip(min=0), bottom=yyoldplus, label=ch, color=bcolor[iter_i])
            ax.bar(tt, yy[:horizon].clip(max=0), bottom=yyoldminus, color=bcolor[iter_i])
            yyoldplus += yy[:horizon].clip(min=0)
            yyoldminus += yy[:horizon].clip(max=0)

        ax.plot(tt, dl_bin_lin_het[:horizon], label="Total", linestyle="-", linewidth=2.5)
        if key == "NE":
            ax.set_title("Aggregate Labor Supply")
        else:
            ax.set_title(f"{income_labels[idx - 1]}")
        ax.grid(False)

        index += 1
        if 1 < index < 4:
            ax.set_ylim(-0.1, 0.6)
        else:
            ax.set_ylim(-0.35, 0.2)

    for j in range(len(bin_keys), len(axes)):
        fig.delaxes(axes[j])

    axes[0].legend(loc="upper right", fontsize="small")
    fig.text(0.5, 0.04, "Time", ha="center")
    fig.text(0.04, 0.5, "Percent deviation", va="center", rotation="vertical")

    return _save_figure(fig, output_dir, "HANK_HetL_decomp_bins_H_comb.png", dpi=300)


def plot_het_consumption_decomposition_total(
    J_het: dict[str, Any],
    G_ha_het: dict[str, Any],
    shock_path: dict[str, np.ndarray],
    ss_het: dict[str, Any],
    irf_het: dict[str, np.ndarray],
    output_dir: Path,
) -> str:
    T = len(shock_path["rstar"])
    tt = np.arange(0, T)
    horizon = 10
    yyoldminus = np.zeros(horizon)
    yyoldplus = np.zeros(horizon)
    bcolor = ["darkblue", "red", "gold"]
    channel_labels = ["r", "Div+Tax", "w"]

    fig, ax = plt.subplots()

    for iter_i, ch in enumerate(channel_labels):
        if ch == "Div+Tax":
            yy_div = J_het["C"].get("Div", 0) @ G_ha_het.get("Div", {}).get("rstar", 0) @ shock_path["rstar"]
            yy_tax = J_het["C"].get("Tax", 0) @ G_ha_het.get("Tax", {}).get("rstar", 0) @ shock_path["rstar"]
            yy = (yy_div + yy_tax) / ss_het["C"] * 100
        else:
            yy = J_het["C"][ch] @ G_ha_het[ch]["rstar"] @ shock_path["rstar"] / ss_het["C"] * 100

        ax.bar(tt[:horizon], yy[:horizon].clip(min=0), bottom=yyoldplus, label=ch, color=bcolor[iter_i])
        ax.bar(tt[:horizon], yy[:horizon].clip(max=0), bottom=yyoldminus, color=bcolor[iter_i])
        yyoldplus += yy[:horizon].clip(min=0)
        yyoldminus += yy[:horizon].clip(max=0)

    dC_lin = 100 * irf_het["C"] / ss_het["C"]
    ax.plot(dC_lin[:horizon], label="Total", linestyle="-", linewidth=2.5)
    ax.set_xlabel("Time")
    ax.set_ylabel("Percent deviation")
    ax.legend(loc="lower right")
    fig.tight_layout()
    return _save_figure(fig, output_dir, "HANK_HetL_decomp_C_comb.png", dpi=300)


def plot_het_consumption_decomposition_bins(
    ge_jac_het: dict[str, Any],
    J_het: dict[str, Any],
    G_ha_het: dict[str, Any],
    shock_path: dict[str, np.ndarray],
    ss_het: dict[str, Any],
    income_labels: list[str],
    output_dir: Path,
) -> str:
    bin_keys = ["C0_2", "C2_11", "C11_34", "C34_66", "C66_89", "C89_98", "C98_100"]
    horizon = 10
    tt = np.arange(horizon)
    bcolor = ["darkblue", "red", "gold", "orange"]
    channels = ["r", "Div+Tax", "w"]

    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 10), sharex=True, sharey=False)
    axes = axes.flatten()
    index = 0

    for idx, key in enumerate(bin_keys):
        ax = axes[idx]
        yyoldminus = np.zeros(horizon)
        yyoldplus = np.zeros(horizon)
        dl_bin_lin_het = 100 * ge_jac_het[key]["rstar"] @ shock_path["rstar"] / ss_het[key]

        for iter_i, ch in enumerate(channels):
            if ch == "Div+Tax":
                yy_div = J_het[key].get("Div", 0) @ G_ha_het.get("Div", {}).get("rstar", 0) @ shock_path["rstar"]
                yy_tax = J_het[key].get("Tax", 0) @ G_ha_het.get("Tax", {}).get("rstar", 0) @ shock_path["rstar"]
                yy = (yy_div + yy_tax) / ss_het[key] * 100
            else:
                if ch not in J_het[key] or ch not in G_ha_het:
                    continue
                yy = J_het[key][ch] @ G_ha_het[ch]["rstar"] @ shock_path["rstar"] / ss_het[key] * 100

            ax.bar(tt, yy[:horizon].clip(min=0), bottom=yyoldplus, label=ch, color=bcolor[iter_i])
            ax.bar(tt, yy[:horizon].clip(max=0), bottom=yyoldminus, color=bcolor[iter_i])
            yyoldplus += yy[:horizon].clip(min=0)
            yyoldminus += yy[:horizon].clip(max=0)

        ax.plot(tt, dl_bin_lin_het[:horizon], label="Total", linestyle="-", linewidth=2.5)
        ax.set_title(f"{income_labels[iter_i]}")
        ax.grid(False)

        index += 1
        if index < 4:
            ax.set_ylim(-0.6, 0.1)
        else:
            ax.set_ylim(-0.2, 0.1)

    for j in range(len(bin_keys), len(axes)):
        fig.delaxes(axes[j])

    axes[0].legend(loc="lower right", fontsize="small")
    fig.text(0.5, 0.04, "Time", ha="center")
    fig.text(0.04, 0.5, "Percent deviation", va="center", rotation="vertical")
    return _save_figure(fig, output_dir, "HANK_HetL_decomp_bins_C_comb.png", dpi=300)


def plot_impact_labor_supply_hom_vs_het(
    irfs_lin: dict[str, Any],
    ss_map: dict[str, Any],
    income_labels: list[str],
    output_dir: Path,
) -> str:
    bins = ["L0_2", "L2_11", "L11_34", "L34_66", "L66_89", "L89_98", "L98_100"]
    percent_devs = [irfs_lin["HANK-HetL"][b][0] / ss_map["HANK-HetL"][b] * 100 for b in bins]
    percent_devs = np.array(percent_devs)

    percent_devs_h = irfs_lin["HANK-HomL"]["L"][0] / ss_map["HANK-HomL"]["L"] * 100 * np.ones(7)

    fig, ax = plt.subplots()
    ax.plot(bins, percent_devs, linestyle="--")
    ax.plot(bins, percent_devs_h, linestyle="-")
    ax.set_xlabel("Income Bin")
    ax.set_xticks(bins, income_labels)
    ax.set_ylabel(r"Impact Response (\% deviation)")
    ax.legend(["HANK", "HANK-HomL"])
    return _save_figure(fig, output_dir, "impact_labor_supply_hom_vs_het.png")


def plot_direct_vs_indirect_consumption(
    irfs_lin: dict[str, Any],
    ss_map: dict[str, Any],
    het_channels: dict[str, np.ndarray],
    hom_channels: dict[str, np.ndarray],
    output_dir: Path,
) -> str:
    horizon = 10
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(100 * irfs_lin["HANK-HomL"]["C"][:horizon] / ss_map["HANK-HomL"]["C"], color="black", linestyle="-")
    ax.plot(hom_channels["J_r_hom_C"][:horizon], color="blue", linestyle="-")
    ax.plot(
        hom_channels["J_w_hom_C"][:horizon]
        + hom_channels["J_N_hom_C"][:horizon]
        + hom_channels["J_Div_hom_C"][:horizon]
        + hom_channels["J_Tax_hom_C"][:horizon],
        color="red",
        linestyle="-",
    )

    ax.plot(100 * irfs_lin["HANK-HetL"]["C"][:horizon] / ss_map["HANK-HetL"]["C"], color="black", linestyle="--")
    ax.plot(het_channels["J_r_het_C"][:horizon], color="blue", linestyle="--")
    ax.plot(
        het_channels["J_w_het_C"][:horizon]
        + het_channels["J_Div_het_C"][:horizon]
        + het_channels["J_Tax_het_C"][:horizon],
        color="red",
        linestyle="--",
    )

    legend_elements = [
        Line2D([0], [0], color="blue", lw=2, label="direct effects ($r$)"),
        Line2D([0], [0], color="red", lw=2, label="indirict effects ($w+Div+Tax$)"),
        Line2D([0], [0], color="black", lw=2, linestyle="-", label="Consumption HomL"),
        Line2D([0], [0], color="black", lw=2, linestyle="--", label="Consumption HetL"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize="small")
    ax.set_xlabel("Time")
    ax.set_ylabel("Percent deviation")
    ax.grid(False)
    fig.tight_layout()
    return _save_figure(fig, output_dir, "HANK_direct_vs_indirect_C_simple.png", dpi=300)


def plot_core_irfs(irfs_lin: dict[str, Any], ss_map: dict[str, Any], output_dir: Path) -> str:
    variables = [
        ("rstar", "Interest Rate shock ($r^*$)", "absolute"),
        ("pi", "Inflation ($\\pi$)", "absolute"),
        ("C", "Consumption ($C$)", "percent"),
        ("HTM", "Hand-to-Mouth", "percent"),
        ("Div", "Dividends ($Div$)", "percent"),
        ("w", "Wage ($w$)", "percent"),
    ]

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 6), sharex=True)
    axes = axes.flatten()
    T_plot = 10

    for idx, (var, title, dev_type) in enumerate(variables):
        ax = axes[idx]

        for key in ["HANK-HetL", "HANK-HomL"]:
            if var not in irfs_lin[key]:
                continue

            ss_val = ss_map[key][var]
            irf_val = irfs_lin[key][var][:T_plot]
            if dev_type == "absolute":
                y = 10000 * irf_val
                ax.set_ylabel("BP Deviation")
            else:
                y = 100 * irf_val / ss_val
                ax.set_ylabel(r"\% Deviation")

            linestyle = "--" if "Het" in key else "-"
            color = "blue" if "Het" in key else "orange"

            if key == "HANK-HetL":
                ax.plot(y, label="HANK", linestyle=linestyle, color=color)
            else:
                ax.plot(y, label="HANK-HomL", linestyle=linestyle, color=color)

        ax.set_title(title)
        ax.axhline(0, color="gray", linestyle="--", linewidth=0.5)
        ax.grid(False)

    for ax in axes[2:]:
        ax.set_xlabel("Periods")

    axes[0].legend(loc="best", fontsize="small")
    fig.tight_layout()
    return _save_figure(fig, output_dir, "HANK_irfs_core_vars.png", dpi=300)


def plot_hours_bins(irfs_lin: dict[str, Any], ss_map: dict[str, Any], output_dir: Path) -> str:
    variables = [
        ("L", "Hours ($L$)", "percent"),
        ("L0_2", r"Hours (0-2%)", "percent"),
        ("L2_11", r"Hours (2-11%)", "percent"),
        ("L11_34", r"Hours (11-34%)", "percent"),
        ("L34_66", r"Hours (34-66%)", "percent"),
        ("L66_89", r"Hours (66-89%)", "percent"),
        ("L89_98", r"Hours (89-98%)", "percent"),
        ("L98_100", r"Hours (98-100%)", "percent"),
    ]

    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12, 8), sharex=True)
    axes = axes.flatten()
    T_plot = 10

    for idx, (var, title, dev_type) in enumerate(variables):
        ax = axes[idx]
        for key in ["HANK-HetL", "HANK-HomL"]:
            target_var = var if "Het" in key else "L"
            if target_var not in irfs_lin[key]:
                continue

            ss_val = ss_map[key][target_var]
            irf_val = irfs_lin[key][target_var][:T_plot]
            if dev_type == "absolute":
                y = 10000 * irf_val
                ax.set_ylabel("BP Deviation")
            else:
                y = 100 * irf_val / ss_val
                ax.set_ylabel(r"\% Deviation")

            linestyle = "--" if "Het" in key else "-"
            color = "blue" if "Het" in key else "orange"
            if key == "HANK-HetL":
                ax.plot(y, label="HANK", linestyle=linestyle, color=color)
            else:
                ax.plot(y, label="HANK-HomL", linestyle=linestyle, color=color)

        ax.set_title(title)
        ax.axhline(0, color="gray", linestyle="--", linewidth=0.5)
        ax.grid(False)

    for ax in axes[2:]:
        ax.set_xlabel("Periods")

    axes[0].legend(loc="best", fontsize="small")
    fig.tight_layout()
    return _save_figure(fig, output_dir, "HANK_irfs_H_bins.png", dpi=300)


def plot_consumption_bins(irfs_lin: dict[str, Any], ss_map: dict[str, Any], output_dir: Path) -> str:
    variables = [
        ("C", "Consumption ($C$)", "percent"),
        ("C0_2", r"Consumption (0-2%)", "percent"),
        ("C2_11", r"Consumption (2-11%)", "percent"),
        ("C11_34", r"Consumption (11-34%)", "percent"),
        ("C34_66", r"Consumption (34-66%)", "percent"),
        ("C66_89", r"Consumption (66-89%)", "percent"),
        ("C89_98", r"Consumption (89-98%)", "percent"),
        ("C98_100", r"Consumption (98-100%)", "percent"),
    ]

    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12, 8), sharex=True)
    axes = axes.flatten()
    T_plot = 10

    for idx, (var, title, dev_type) in enumerate(variables):
        ax = axes[idx]
        for key in ["HANK-HetL", "HANK-HomL"]:
            if var not in irfs_lin[key]:
                continue

            ss_val = ss_map[key][var]
            irf_val = irfs_lin[key][var][:T_plot]
            if dev_type == "absolute":
                y = 10000 * irf_val
                ax.set_ylabel("BP Deviation")
            else:
                y = 100 * irf_val / ss_val
                ax.set_ylabel(r"\% Deviation")

            linestyle = "--" if "Het" in key else "-"
            color = "blue" if "Het" in key else "orange"
            if key == "HANK-HetL":
                ax.plot(y, label="HANK", linestyle=linestyle, color=color)
            else:
                ax.plot(y, label="HANK-HomL", linestyle=linestyle, color=color)

        ax.set_title(title)
        ax.axhline(0, color="gray", linestyle="--", linewidth=0.5)
        ax.grid(False)

    for ax in axes[2:]:
        ax.set_xlabel("Periods")

    axes[0].legend(loc="best", fontsize="small")
    fig.tight_layout()
    return _save_figure(fig, output_dir, "HANK_irfs_C_bins.png", dpi=300)


def _resolve_key_for_model(irfs_lin: dict[str, Any], ss_map: dict[str, Any], model_key: str, var: str) -> str | None:
    candidates = [var]
    if var:
        candidates.append(var[0].lower() + var[1:])
        candidates.append(var[0].upper() + var[1:])

    for cand in dict.fromkeys(candidates):
        if cand in irfs_lin.get(model_key, {}) and cand in ss_map.get(model_key, {}):
            return cand
    return None


def _plot_two_model_grid(
    irfs_lin: dict[str, Any],
    ss_map: dict[str, Any],
    variables: list[tuple[str, str, str]],
    output_dir: Path,
    filename: str,
    nrows: int,
    ncols: int,
    het_key: str,
    hom_key: str,
    hom_var_rule: str,
    hom_label: str,
    T_plot: int = 10,
) -> str:
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 6 if nrows == 3 else 8), sharex=True)
    axes = axes.flatten()

    for idx, (var, title, dev_type) in enumerate(variables):
        ax = axes[idx]
        model_specs = [
            (het_key, "HANK", "--", "blue", var),
            (hom_key, hom_label, "-", "orange", "L" if hom_var_rule == "L" else var),
        ]

        for model_key, label, linestyle, color, raw_var in model_specs:
            key = _resolve_key_for_model(irfs_lin=irfs_lin, ss_map=ss_map, model_key=model_key, var=raw_var)
            if key is None:
                continue

            ss_val = ss_map[model_key][key]
            irf_val = irfs_lin[model_key][key][:T_plot]

            if dev_type == "absolute":
                y = 10000 * irf_val
                ax.set_ylabel("BP Deviation")
            else:
                y = 100 * irf_val / ss_val
                ax.set_ylabel("% Deviation")

            ax.plot(y, label=label, linestyle=linestyle, color=color)

        ax.set_title(title)
        ax.axhline(0, color="gray", linestyle="--", linewidth=0.5)
        ax.grid(False)

    for ax in axes[2:]:
        ax.set_xlabel("Periods")

    axes[0].legend(loc="best", fontsize="small")
    fig.tight_layout()
    return _save_figure(fig, output_dir, filename, dpi=300)


def plot_core_irfs_match_aggl(
    irfs_lin: dict[str, Any],
    ss_map: dict[str, Any],
    output_dir: Path,
    het_key: str = "HANK-HetL",
    hom_key: str = "HANK-HomL matchAggL",
) -> str:
    variables = [
        ("rstar", "Interest Rate shock ($r^*$)", "absolute"),
        ("pi", "Inflation ($\\pi$)", "absolute"),
        ("C", "Consumption ($C$)", "percent"),
        ("HTM", "Hand-to-Mouth", "percent"),
        ("Div", "Dividends ($Div$)", "percent"),
        ("w", "Wage ($w$)", "percent"),
    ]
    return _plot_two_model_grid(
        irfs_lin=irfs_lin,
        ss_map=ss_map,
        variables=variables,
        output_dir=output_dir,
        filename="HANK_irfs_core_vars_matchAggL.png",
        nrows=3,
        ncols=2,
        het_key=het_key,
        hom_key=hom_key,
        hom_var_rule="same",
        hom_label="HANK-HomL (match agg $L$)",
    )


def plot_hours_bins_match_aggl(
    irfs_lin: dict[str, Any],
    ss_map: dict[str, Any],
    output_dir: Path,
    het_key: str = "HANK-HetL",
    hom_key: str = "HANK-HomL matchAggL",
) -> str:
    variables = [
        ("L", "Hours ($L$)", "percent"),
        ("L0_2", r"Hours (0-2%)", "percent"),
        ("L2_11", r"Hours (2-11%)", "percent"),
        ("L11_34", r"Hours (11-34%)", "percent"),
        ("L34_66", r"Hours (34-66%)", "percent"),
        ("L66_89", r"Hours (66-89%)", "percent"),
        ("L89_98", r"Hours (89-98%)", "percent"),
        ("L98_100", r"Hours (98-100%)", "percent"),
    ]
    return _plot_two_model_grid(
        irfs_lin=irfs_lin,
        ss_map=ss_map,
        variables=variables,
        output_dir=output_dir,
        filename="HANK_irfs_H_bins_matchAggL.png",
        nrows=4,
        ncols=2,
        het_key=het_key,
        hom_key=hom_key,
        hom_var_rule="L",
        hom_label="HANK-HomL (match agg $L$)",
    )


def plot_consumption_bins_match_aggl(
    irfs_lin: dict[str, Any],
    ss_map: dict[str, Any],
    output_dir: Path,
    het_key: str = "HANK-HetL",
    hom_key: str = "HANK-HomL matchAggL",
) -> str:
    variables = [
        ("C", "Consumption ($C$)", "percent"),
        ("C0_2", r"Consumption (0-2%)", "percent"),
        ("C2_11", r"Consumption (2-11%)", "percent"),
        ("C11_34", r"Consumption (11-34%)", "percent"),
        ("C34_66", r"Consumption (34-66%)", "percent"),
        ("C66_89", r"Consumption (66-89%)", "percent"),
        ("C89_98", r"Consumption (89-98%)", "percent"),
        ("C98_100", r"Consumption (98-100%)", "percent"),
    ]
    return _plot_two_model_grid(
        irfs_lin=irfs_lin,
        ss_map=ss_map,
        variables=variables,
        output_dir=output_dir,
        filename="HANK_irfs_C_bins_matchAggL.png",
        nrows=4,
        ncols=2,
        het_key=het_key,
        hom_key=hom_key,
        hom_var_rule="same",
        hom_label="HANK-HomL (match agg $L$)",
    )


def plot_hank_hetl_bins_l_contribution(irfs_lin: dict[str, Any], output_dir: Path) -> str:
    model_key = "HANK-HetL"
    bins = ["L0_2", "L2_11", "L11_34", "L34_66", "L66_89", "L89_98", "L98_100"]
    colors = ["darkblue", "darkgreen", "grey", "gold", "orange", "indianred", "purple"]
    labels = [r"0-2%", r"2-11%", r"11-34%", r"34-66%", r"66-89%", r"89-98%", r"98-100%"]
    horizon = 10
    tt = np.arange(horizon)

    fig, ax = plt.subplots(figsize=(10, 6))
    yyoldminus = np.zeros(horizon)
    yyoldplus = np.zeros(horizon)

    for i, bin_key in enumerate(bins):
        yy = irfs_lin[model_key][bin_key][:horizon] * 10000
        ax.bar(tt, yy.clip(min=0), bottom=yyoldplus, label=labels[i], color=colors[i])
        ax.bar(tt, yy.clip(max=0), bottom=yyoldminus, color=colors[i])
        yyoldplus += yy.clip(min=0)
        yyoldminus += yy.clip(max=0)

    ax.plot(tt, irfs_lin[model_key]["L"][:horizon] * 10000, label="Total (L)", color="black", linestyle="--", linewidth=2.5)
    ax.set_xlabel("Time")
    ax.set_ylabel("BP")
    ax.legend(loc="lower right", fontsize="small")
    fig.tight_layout()
    return _save_figure(fig, output_dir, "HANK_HetL_bins_L_contribution.png", dpi=300)


def plot_hank_hetl_bins_c_contribution(irfs_lin: dict[str, Any], output_dir: Path) -> str:
    model_key = "HANK-HetL"
    bins = ["C0_2", "C2_11", "C11_34", "C34_66", "C66_89", "C89_98", "C98_100"]
    colors = ["darkblue", "darkgreen", "grey", "gold", "orange", "indianred", "purple"]
    labels = [r"0-2%", r"2-11%", r"11-34%", r"34-66%", r"66-89%", r"89-98%", r"98-100%"]
    horizon = 10
    tt = np.arange(horizon)

    fig, ax = plt.subplots(figsize=(10, 6))
    yyoldminus = np.zeros(horizon)
    yyoldplus = np.zeros(horizon)

    for i, bin_key in enumerate(bins):
        yy = irfs_lin[model_key][bin_key][:horizon] * 10000
        ax.bar(tt, yy.clip(min=0), bottom=yyoldplus, label=labels[i], color=colors[i])
        ax.bar(tt, yy.clip(max=0), bottom=yyoldminus, color=colors[i])
        yyoldplus += yy.clip(min=0)
        yyoldminus += yy.clip(max=0)

    ax.plot(tt, irfs_lin[model_key]["C"][:horizon] * 10000, label="Total (C)", color="black", linestyle="--", linewidth=2.5)
    ax.set_xlabel("Time")
    ax.set_ylabel("Absolute deviation")
    ax.legend(loc="lower right", fontsize="small")
    fig.tight_layout()
    return _save_figure(fig, output_dir, "HANK_HetL_bins_C_contribution.png", dpi=300)
