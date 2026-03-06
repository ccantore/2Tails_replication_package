"""Model assembly helpers for steady-state and dynamic DAGs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sequence_jacobian as sj

from .model_blocks import (
    LS_hom,
    LSss_hom,
    compute_assets,
    compute_consumption,
    compute_htm,
    compute_labor,
    compute_labor_1,
    compute_weighted_mpc,
    firm_hom,
    firm_het,
    fiscal,
    hh_hom,
    hh_het,
    labor_supply,
    make_grids,
    mkt_clearing_hom,
    mkt_clearing_het,
    monetary,
    nkpc,
    nkpc_ss,
    transfers,
    wages_hom,
    wages_het,
)


@dataclass(frozen=True)
class ModelBundle:
    hh_ext_hom: Any
    hh_ext_het: Any
    hank_ss_hom: Any
    hank_ss_het: Any
    hank_hom: Any
    hank_het: Any


def build_models() -> ModelBundle:
    """Build all model objects used by the replication pipeline."""
    household_simple_hom = hh_hom.add_hetinputs([make_grids, wages_hom, transfers])
    household_simple_het = hh_het.add_hetinputs([make_grids, wages_het, transfers])

    hh_ext_hom = household_simple_hom.add_hetoutputs(
        [compute_weighted_mpc, compute_htm, compute_consumption, compute_assets]
    )
    hh_ext_het = household_simple_het.add_hetoutputs(
        [
            labor_supply,
            compute_weighted_mpc,
            compute_htm,
            compute_consumption,
            compute_assets,
            compute_labor,
            compute_labor_1,
        ]
    )

    hank_ss_hom = sj.create_model(
        [hh_ext_hom, firm_hom, monetary, mkt_clearing_hom, fiscal, nkpc_ss, LSss_hom],
        name="HANK Model SS - hom",
    )
    hank_ss_het = sj.create_model(
        [hh_ext_het, firm_het, monetary, mkt_clearing_het, fiscal, nkpc_ss],
        name="HANK Model SS - Het",
    )

    hank_hom = sj.create_model(
        [hh_ext_hom, firm_hom, monetary, mkt_clearing_hom, nkpc, fiscal, LS_hom],
        name="HANK Model - Hom",
    )
    hank_het = sj.create_model(
        [hh_ext_het, firm_het, monetary, mkt_clearing_het, fiscal, nkpc],
        name="HANK Model - Het",
    )

    return ModelBundle(
        hh_ext_hom=hh_ext_hom,
        hh_ext_het=hh_ext_het,
        hank_ss_hom=hank_ss_hom,
        hank_ss_het=hank_ss_het,
        hank_hom=hank_hom,
        hank_het=hank_het,
    )
