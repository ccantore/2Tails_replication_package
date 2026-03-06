"""Numerical solve helpers, including optional disk caching."""

from __future__ import annotations

import hashlib
import json
import pickle
from pathlib import Path
from typing import Any, Callable

import numpy as np


def build_rstar_shock_path(T: int, rho_r: float, sig_r: float) -> dict[str, np.ndarray]:
    return {"rstar": sig_r * rho_r ** (np.arange(T))}


def _stable_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _cache_file(cache_dir: Path, namespace: str, payload: dict[str, Any]) -> Path:
    return cache_dir / namespace / f"{_stable_hash(payload)}.pkl"


def _load_or_compute(
    compute: Callable[[], Any],
    cache_enabled: bool,
    cache_dir: Path,
    namespace: str,
    payload: dict[str, Any],
) -> Any:
    if not cache_enabled:
        return compute()

    path = _cache_file(cache_dir=cache_dir, namespace=namespace, payload=payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            with path.open("rb") as fh:
                return pickle.load(fh)
        except Exception:
            pass

    result = compute()
    try:
        with path.open("wb") as fh:
            pickle.dump(result, fh)
    except Exception:
        pass
    return result


def solve_steady_states(
    model,
    scenario_names: list[str],
    calibration_map: dict[str, dict[str, Any]],
    unknowns_ss: dict[str, Any],
    targets_ss: dict[str, Any],
    solver_name: str,
    cache_enabled: bool,
    cache_dir: Path,
    model_tag: str,
) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for name in scenario_names:
        calibration = calibration_map[name]
        payload = {
            "task": "steady_state",
            "model": model_tag,
            "name": name,
            "calibration": calibration,
            "unknowns": unknowns_ss,
            "targets": targets_ss,
            "solver": solver_name,
        }

        def _compute():
            return model.solve_steady_state(calibration, unknowns_ss, targets_ss, solver=solver_name)

        results[name] = _load_or_compute(
            compute=_compute,
            cache_enabled=cache_enabled,
            cache_dir=cache_dir,
            namespace="steady_state",
            payload=payload,
        )

    return results


def validate_dynamic_steady_states(dynamic_model, ss0_map: dict[str, Any]) -> dict[str, Any]:
    ss_map: dict[str, Any] = {}
    for name, ss0 in ss0_map.items():
        ss = dynamic_model.steady_state(ss0)
        for key in ss0.keys():
            lhs = ss[key]
            rhs = ss0[key]
            if not np.all(np.isclose(lhs, rhs)):
                raise AssertionError(f"Steady-state consistency check failed for {name}:{key}")
        ss_map[name] = ss
    return ss_map


def solve_ge_jacobians(
    dynamic_model,
    scenario_names: list[str],
    ss_map: dict[str, Any],
    unknowns: list[str],
    targets: list[str],
    exogenous: list[str],
    T: int,
    cache_enabled: bool,
    cache_dir: Path,
    model_tag: str,
) -> dict[str, Any]:
    jacobians: dict[str, Any] = {}
    for name in scenario_names:
        payload = {
            "task": "jacobian",
            "model": model_tag,
            "name": name,
            "unknowns": unknowns,
            "targets": targets,
            "exogenous": exogenous,
            "T": T,
        }

        def _compute():
            return dynamic_model.solve_jacobian(ss_map[name], unknowns, targets, exogenous, T=T)

        jacobians[name] = _load_or_compute(
            compute=_compute,
            cache_enabled=cache_enabled,
            cache_dir=cache_dir,
            namespace="jacobian",
            payload=payload,
        )
    return jacobians


def solve_linear_impulses(
    dynamic_model,
    scenario_names: list[str],
    ss_map: dict[str, Any],
    unknowns: list[str],
    targets: list[str],
    shock_path: dict[str, np.ndarray],
    cache_enabled: bool,
    cache_dir: Path,
    model_tag: str,
) -> dict[str, Any]:
    irfs: dict[str, Any] = {}
    for name in scenario_names:
        payload = {
            "task": "irf",
            "model": model_tag,
            "name": name,
            "unknowns": unknowns,
            "targets": targets,
            "shock": {k: v.tolist() for k, v in shock_path.items()},
        }

        def _compute():
            return dynamic_model.solve_impulse_linear(ss_map[name], unknowns, targets, shock_path)

        irfs[name] = _load_or_compute(
            compute=_compute,
            cache_enabled=cache_enabled,
            cache_dir=cache_dir,
            namespace="irf",
            payload=payload,
        )

    return irfs


def solve_partial_ha_jacobian(hh_block, ss: dict[str, Any], inputs: list[str], T: int) -> dict[str, Any]:
    return hh_block.jacobian(ss, inputs=inputs, T=T)


def solve_general_ha_jacobian(
    dynamic_model,
    ss: dict[str, Any],
    unknowns: list[str],
    targets: list[str],
    exogenous: list[str],
    T: int,
    hh_jacobian: dict[str, Any],
) -> dict[str, Any]:
    return dynamic_model.solve_jacobian(ss, unknowns, targets, exogenous, T=T, Js={"hh": hh_jacobian})


def compute_het_consumption_channel_decomposition(
    J_het: dict[str, Any],
    G_ha_het: dict[str, Any],
    shock_path: dict[str, np.ndarray],
    ss_het: dict[str, Any],
) -> dict[str, np.ndarray]:
    rstar = shock_path["rstar"]
    return {
        "J_r_het_C": J_het["C"]["r"] @ G_ha_het["r"]["rstar"] @ rstar / ss_het["C"] * 100,
        "J_w_het_C": J_het["C"]["w"] @ G_ha_het["w"]["rstar"] @ rstar / ss_het["C"] * 100,
        "J_Tax_het_C": J_het["C"]["Tax"] @ G_ha_het["Tax"]["rstar"] @ rstar / ss_het["C"] * 100,
        "J_Div_het_C": J_het["C"]["Div"] @ G_ha_het["Div"]["rstar"] @ rstar / ss_het["C"] * 100,
    }


def compute_hom_consumption_channel_decomposition(
    J_hom: dict[str, Any],
    G_ha_hom: dict[str, Any],
    shock_path: dict[str, np.ndarray],
    ss_hom: dict[str, Any],
) -> dict[str, np.ndarray]:
    rstar = shock_path["rstar"]
    return {
        "J_r_hom_C": J_hom["C"]["r"] @ G_ha_hom["r"]["rstar"] @ rstar / ss_hom["C"] * 100,
        "J_w_hom_C": J_hom["C"]["w"] @ G_ha_hom["w"]["rstar"] @ rstar / ss_hom["C"] * 100,
        "J_N_hom_C": J_hom["C"]["N"] @ G_ha_hom["N"]["rstar"] @ rstar / ss_hom["C"] * 100,
        "J_Tax_hom_C": J_hom["C"]["Tax"] @ G_ha_hom["Tax"]["rstar"] @ rstar / ss_hom["C"] * 100,
        "J_Div_hom_C": J_hom["C"]["Div"] @ G_ha_hom["Div"]["rstar"] @ rstar / ss_hom["C"] * 100,
    }
