"""End-to-end replication pipeline."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
import warnings

import numpy as np
import pandas as pd

from .config import ReplicationConfig
from .model_factory import build_models
from .plots import (
    plot_baseline_irfs,
    plot_baseline_policy_functions,
    plot_consumption_bins,
    plot_core_irfs,
    plot_direct_vs_indirect_consumption,
    plot_hank_hetl_bins_c_contribution,
    plot_hank_hetl_bins_l_contribution,
    plot_hours_bins,
    plot_het_consumption_decomposition_bins,
    plot_het_consumption_decomposition_total,
    plot_het_labor_decomposition_bins,
    plot_impact_labor_supply_hom_vs_het,
    plot_irfs_for_models,
    plot_labor_supply_models_across_income,
    plot_policy_functions_for_models,
)
from .solve import (
    build_rstar_shock_path,
    compute_het_consumption_channel_decomposition,
    compute_hom_consumption_channel_decomposition,
    solve_general_ha_jacobian,
    solve_ge_jacobians,
    solve_linear_impulses,
    solve_partial_ha_jacobian,
    solve_steady_states,
    validate_dynamic_steady_states,
)
from .tables import (
    compute_sacrifice_ratios,
    save_table_artifacts,
    steady_state_summary_table,
    table2,
    table3_dataframe,
    table3_latex,
)


def _print_income_state_mapping(ss0_het: dict[str, Any]) -> None:
    hh_het_internals = ss0_het.internals["hh_het"]
    cdf = np.cumsum(hh_het_internals["pi_e"])
    for i in range(len(hh_het_internals["e_grid"])):
        percentile = cdf[i] * 100
        income = hh_het_internals["e_grid"][i]
        c_array = hh_het_internals["c"][i]
        n_array = hh_het_internals["n"][i]
        consumption = np.median(c_array)
        hours = np.median(n_array)
        print(
            f"State {i + 1}: {percentile:.1f}th percentile, "
            f"Income: {income:.2f}, Consumption: {consumption:.2f}, Hours: {hours:.2f}"
        )


def _unique_keep_order(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def _sr4_from_model(ss_map: dict[str, Any], irfs_map: dict[str, Any], model_key: str) -> float:
    irfsY = 100.0 * irfs_map[model_key]["Y"] / ss_map[model_key]["Y"]
    irfPi = 100.0 * irfs_map[model_key]["pi"]
    return float((np.cumsum(irfsY[:4]) / np.cumsum(irfPi[:4]))[-1])


def _ss0_scalar(ss0_obj: Any, name: str, default: float) -> float:
    try:
        return float(ss0_obj[name])
    except Exception:
        return float(default)


def _solve_hom_for_eis_match_aggl(
    models: Any,
    calibration_hom: dict[str, Any],
    eis: float,
    anchor_keys: list[str],
    ss0_map: dict[str, Any],
    unknowns_hom: list[str],
    targets_hom: list[str],
    shock_path: dict[str, np.ndarray],
) -> tuple[Any, Any, Any]:
    calib = calibration_hom.copy()
    calib["eis"] = float(eis)

    guess_key = min(anchor_keys, key=lambda k: abs(float(ss0_map[k]["eis"]) - float(eis)))
    unknowns_local = {
        "beta": _ss0_scalar(ss0_map[guess_key], "beta", 0.99),
        "B": _ss0_scalar(ss0_map[guess_key], "B", 4.0),
    }
    targets_local = {"asset_mkt": 0, "HTM": 0.2}

    try:
        ss0_tmp = models.hank_ss_hom.solve_steady_state(calib, unknowns_local, targets_local, solver="hybr")
    except Exception:
        ss0_tmp = models.hank_ss_hom.solve_steady_state(calib, unknowns_local, targets_local, solver="lm")

    ss_tmp = models.hank_hom.steady_state(ss0_tmp)
    irfs_tmp = models.hank_hom.solve_impulse_linear(ss_tmp, unknowns_hom, targets_hom, shock_path)
    return ss0_tmp, ss_tmp, irfs_tmp


def _run_match_aggl_robustness(
    models: Any,
    calibration: dict[str, dict[str, Any]],
    ss0: dict[str, Any],
    ss: dict[str, Any],
    irfs_lin: dict[str, Any],
    unknowns_hom: list[str],
    targets_hom: list[str],
    output_path: Path,
    shock_path: dict[str, np.ndarray],
) -> dict[str, Any]:
    rows = [
        ("Low $\\sigma$", "HANK-HomL EIS025", "HANK-HetL EIS025"),
        ("Baseline $\\sigma$", "HANK-HomL", "HANK-HetL"),
        ("High $\\sigma$", "HANK-HomL EIS1", "HANK-HetL EIS1"),
    ]
    hom_anchor_keys = [r[1] for r in rows]

    anchor_rows: list[dict[str, float | str]] = []
    for key in hom_anchor_keys:
        if key not in ss0 or key not in ss or key not in irfs_lin:
            raise RuntimeError(f"Missing {key} in ss0/ss/irfs_lin. Run HomL solve first.")
        anchor_rows.append(
            {
                "model": key,
                "eis": float(ss0[key]["eis"]),
                "dL0_pct": float(100.0 * irfs_lin[key]["L"][0] / ss[key]["L"]),
            }
        )

    df_anchors = pd.DataFrame(anchor_rows).sort_values("eis")
    print("HomL anchors (already solved):")
    print(df_anchors.to_markdown(index=False))

    pts = sorted([(float(row["dL0_pct"]), float(row["eis"])) for row in anchor_rows], key=lambda t: t[0])
    d_vals = np.array([d for d, _ in pts], dtype=float)
    e_vals = np.array([e for _, e in pts], dtype=float)

    match_rows: list[dict[str, float | str]] = []
    for scen_label, hom_key, het_key in rows:
        target_L_pct = float(100.0 * irfs_lin[het_key]["L"][0] / ss[het_key]["L"])
        eis_star = float(np.interp(target_L_pct, d_vals, e_vals))
        hom_match_key = hom_key.replace("HANK-HomL", "HANK-HomL matchAggL")

        ss0_star, ss_star, irfs_star = _solve_hom_for_eis_match_aggl(
            models=models,
            calibration_hom=calibration["HANK-HomL"],
            eis=eis_star,
            anchor_keys=hom_anchor_keys,
            ss0_map=ss0,
            unknowns_hom=unknowns_hom,
            targets_hom=targets_hom,
            shock_path=shock_path,
        )

        calibration[hom_match_key] = calibration["HANK-HomL"].copy()
        calibration[hom_match_key]["eis"] = eis_star
        ss0[hom_match_key] = ss0_star
        ss[hom_match_key] = ss_star
        irfs_lin[hom_match_key] = irfs_star

        hom_L_pct = float(100.0 * irfs_lin[hom_match_key]["L"][0] / ss[hom_match_key]["L"])
        match_rows.append(
            {
                "Scenario": scen_label,
                "Target dL0 HetL (%)": target_L_pct,
                "Implied EIS HomL": eis_star,
                "Achieved dL0 HomL (%)": hom_L_pct,
                "Match error (pp)": hom_L_pct - target_L_pct,
            }
        )

    df_match = pd.DataFrame(match_rows)
    print("HomL EIS implied by aggregate-L matching (period 0):")
    print(df_match.to_markdown(index=False))

    sr_rows = []
    for scen_label, hom_key, het_key in rows:
        hom_match_key = hom_key.replace("HANK-HomL", "HANK-HomL matchAggL")
        sr_rows.append((scen_label, _sr4_from_model(ss, irfs_lin, hom_match_key), _sr4_from_model(ss, irfs_lin, het_key)))

    df_sr = pd.DataFrame(sr_rows, columns=["", "HANK-HomL (match agg $L$)", "HANK"]).set_index("")
    print("Sacrifice ratios (4q): new aggregate-L-matched HomL vs HetL")
    print(df_sr.round(2).to_markdown())

    latex_lines = [
        r"\\begin{tabular}{lcc}",
        r"\\toprule",
        r" & HANK-HomL (match agg $L$) & HANK \\",
        r"\\midrule",
    ] + [f"{label} & {v1:.2f} & {v2:.2f} \\\\" for label, v1, v2 in sr_rows] + [
        r"\\bottomrule",
        r"\\end{tabular}",
    ]
    latex_str = "\n".join(latex_lines)
    print(latex_str)

    robust_match_md = output_path / "matchAggL_implied_eis.md"
    robust_sr_md = output_path / "table3_matchAggL.md"
    robust_sr_tex = output_path / "table3_matchAggL.tex"
    robust_match_md.write_text(df_match.to_markdown(index=False) + "\n", encoding="utf-8")
    robust_sr_md.write_text(df_sr.round(2).to_markdown() + "\n", encoding="utf-8")
    robust_sr_tex.write_text(latex_str + "\n", encoding="utf-8")

    return {
        "df_anchors": df_anchors,
        "df_match": df_match,
        "df_sr": df_sr,
        "table_files": {
            "matchAggL_implied_eis": robust_match_md.name,
            "table3_matchAggL": robust_sr_md.name,
            "table3_matchAggL_latex": robust_sr_tex.name,
        },
        "implied_eis": {row["Scenario"]: float(row["Implied EIS HomL"]) for row in match_rows},
        "sacrifice_ratios": {label: {"hom_matchAggL": float(v1), "het": float(v2)} for label, v1, v2 in sr_rows},
    }


def run_full_replication(config: ReplicationConfig, output_dir: Path | str) -> dict[str, Any]:
    """Run the full replication workflow and return artifact metadata."""
    warnings.filterwarnings(
        "ignore",
        category=RuntimeWarning,
        message=r".*(divide by zero|overflow|invalid value).*matmul",
    )
    warnings.filterwarnings(
        "ignore",
        category=RuntimeWarning,
        message=r".*invalid value encountered in power",
    )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    cache_dir = Path(config.cache_dir)
    if not cache_dir.is_absolute():
        cache_dir = output_path.parent / cache_dir

    models = build_models()
    calibration = config.expanded_calibration()

    settings = config.solver_settings
    irf_settings = settings["irf"]
    ss_settings = settings["steady_state"]

    T = int(irf_settings["T"])
    rho_r = float(irf_settings["rho_r"])
    sig_r = float(irf_settings["sig_r"])
    exogenous = list(irf_settings["exogenous"])
    shock_path = build_rstar_shock_path(T=T, rho_r=rho_r, sig_r=sig_r)

    het_names = [spec.name for spec in config.get_family_scenarios("het")]
    hom_names = [spec.name for spec in config.get_family_scenarios("hom")]

    if "HANK-HetL" not in het_names:
        raise ValueError("Expected baseline HANK-HetL scenario in het scenario list")

    ss0: dict[str, Any] = {}
    ss: dict[str, Any] = {}
    ge_jacobians: dict[str, Any] = {}
    irfs_lin: dict[str, Any] = {}
    generated_files: list[str] = []

    # Baseline calibration
    baseline_het_name = "HANK-HetL"
    baseline_ss0 = solve_steady_states(
        model=models.hank_ss_het,
        scenario_names=[baseline_het_name],
        calibration_map=calibration,
        unknowns_ss=ss_settings["het"]["unknowns"],
        targets_ss=ss_settings["het"]["targets"],
        solver_name=ss_settings["solver"],
        cache_enabled=config.cache_enabled,
        cache_dir=cache_dir,
        model_tag="hank_ss_het",
    )
    ss0.update(baseline_ss0)

    baseline_table_df = steady_state_summary_table(baseline_ss0)
    print(baseline_table_df.to_markdown(index=False))
    _print_income_state_mapping(ss0[baseline_het_name])

    generated_files.extend(
        plot_baseline_policy_functions(
            ss0_het=ss0[baseline_het_name],
            state_labels=config.state_labels,
            output_dir=output_path,
        )
    )

    ss_baseline = validate_dynamic_steady_states(models.hank_het, baseline_ss0)
    ss.update(ss_baseline)

    ge_baseline = solve_ge_jacobians(
        dynamic_model=models.hank_het,
        scenario_names=[baseline_het_name],
        ss_map=ss,
        unknowns=list(irf_settings["het"]["unknowns"]),
        targets=list(irf_settings["het"]["targets"]),
        exogenous=exogenous,
        T=T,
        cache_enabled=config.cache_enabled,
        cache_dir=cache_dir,
        model_tag="hank_het",
    )
    ge_jacobians.update(ge_baseline)

    irf_baseline = solve_linear_impulses(
        dynamic_model=models.hank_het,
        scenario_names=[baseline_het_name],
        ss_map=ss,
        unknowns=list(irf_settings["het"]["unknowns"]),
        targets=list(irf_settings["het"]["targets"]),
        shock_path=shock_path,
        cache_enabled=config.cache_enabled,
        cache_dir=cache_dir,
        model_tag="hank_het",
    )
    irfs_lin.update(irf_baseline)

    generated_files.append(plot_baseline_irfs(irf=irfs_lin[baseline_het_name], ss_het=ss[baseline_het_name], output_dir=output_path))

    # Solve all Het-L scenarios
    ss0_het_all = solve_steady_states(
        model=models.hank_ss_het,
        scenario_names=het_names,
        calibration_map=calibration,
        unknowns_ss=ss_settings["het"]["unknowns"],
        targets_ss=ss_settings["het"]["targets"],
        solver_name=ss_settings["solver"],
        cache_enabled=config.cache_enabled,
        cache_dir=cache_dir,
        model_tag="hank_ss_het",
    )
    ss0.update(ss0_het_all)

    ss_het_all = validate_dynamic_steady_states(models.hank_het, {name: ss0[name] for name in het_names})
    ss.update(ss_het_all)

    generated_files.extend(
        plot_policy_functions_for_models(
            ss0_map=ss0,
            model_names=het_names,
            state_labels=config.state_labels,
            output_dir=output_path,
        )
    )

    ge_het_all = solve_ge_jacobians(
        dynamic_model=models.hank_het,
        scenario_names=het_names,
        ss_map=ss,
        unknowns=list(irf_settings["het"]["unknowns"]),
        targets=list(irf_settings["het"]["targets"]),
        exogenous=exogenous,
        T=T,
        cache_enabled=config.cache_enabled,
        cache_dir=cache_dir,
        model_tag="hank_het",
    )
    ge_jacobians.update(ge_het_all)

    irf_het_all = solve_linear_impulses(
        dynamic_model=models.hank_het,
        scenario_names=het_names,
        ss_map=ss,
        unknowns=list(irf_settings["het"]["unknowns"]),
        targets=list(irf_settings["het"]["targets"]),
        shock_path=shock_path,
        cache_enabled=config.cache_enabled,
        cache_dir=cache_dir,
        model_tag="hank_het",
    )
    irfs_lin.update(irf_het_all)

    generated_files.extend(plot_irfs_for_models(irfs_lin=irfs_lin, ss_map=ss, model_names=het_names, output_dir=output_path))

    generated_files.append(
        plot_labor_supply_models_across_income(
            irfs_lin=irfs_lin,
            ss_map=ss,
            model_names=het_names,
            output_dir=output_path,
            use_tex=bool(settings["plotting"].get("usetex", False)),
        )
    )

    # IRFs decomposition for Het-L
    J_het = solve_partial_ha_jacobian(
        hh_block=models.hh_ext_het,
        ss=ss[baseline_het_name],
        inputs=list(irf_settings["het"]["hh_inputs"]),
        T=T,
    )
    G_ha_het = solve_general_ha_jacobian(
        dynamic_model=models.hank_het,
        ss=ss[baseline_het_name],
        unknowns=list(irf_settings["het"]["unknowns"]),
        targets=list(irf_settings["het"]["targets"]),
        exogenous=exogenous,
        T=T,
        hh_jacobian=J_het,
    )

    generated_files.append(
        plot_het_labor_decomposition_bins(
            ge_jac_het=ge_jacobians[baseline_het_name],
            J_het=J_het,
            G_ha_het=G_ha_het,
            shock_path=shock_path,
            ss_het=ss[baseline_het_name],
            income_labels=config.income_labels,
            output_dir=output_path,
        )
    )

    generated_files.append(
        plot_het_consumption_decomposition_total(
            J_het=J_het,
            G_ha_het=G_ha_het,
            shock_path=shock_path,
            ss_het=ss[baseline_het_name],
            irf_het=irfs_lin[baseline_het_name],
            output_dir=output_path,
        )
    )

    generated_files.append(
        plot_het_consumption_decomposition_bins(
            ge_jac_het=ge_jacobians[baseline_het_name],
            J_het=J_het,
            G_ha_het=G_ha_het,
            shock_path=shock_path,
            ss_het=ss[baseline_het_name],
            income_labels=config.income_labels,
            output_dir=output_path,
        )
    )

    het_channels = compute_het_consumption_channel_decomposition(
        J_het=J_het,
        G_ha_het=G_ha_het,
        shock_path=shock_path,
        ss_het=ss[baseline_het_name],
    )

    # Solve all Hom-L scenarios
    ss0_hom_all = solve_steady_states(
        model=models.hank_ss_hom,
        scenario_names=hom_names,
        calibration_map=calibration,
        unknowns_ss=ss_settings["hom"]["unknowns"],
        targets_ss=ss_settings["hom"]["targets"],
        solver_name=ss_settings["solver"],
        cache_enabled=config.cache_enabled,
        cache_dir=cache_dir,
        model_tag="hank_ss_hom",
    )
    ss0.update(ss0_hom_all)

    ss_hom_all = validate_dynamic_steady_states(models.hank_hom, {name: ss0[name] for name in hom_names})
    ss.update(ss_hom_all)

    full_steady_table_df = steady_state_summary_table(ss0)
    print(full_steady_table_df.to_markdown(index=False))

    table2_df = table2(ss0)
    print(table2_df.to_markdown(index=False))

    ge_hom_all = solve_ge_jacobians(
        dynamic_model=models.hank_hom,
        scenario_names=hom_names,
        ss_map=ss,
        unknowns=list(irf_settings["hom"]["unknowns"]),
        targets=list(irf_settings["hom"]["targets"]),
        exogenous=exogenous,
        T=T,
        cache_enabled=config.cache_enabled,
        cache_dir=cache_dir,
        model_tag="hank_hom",
    )
    ge_jacobians.update(ge_hom_all)

    irf_hom_all = solve_linear_impulses(
        dynamic_model=models.hank_hom,
        scenario_names=hom_names,
        ss_map=ss,
        unknowns=list(irf_settings["hom"]["unknowns"]),
        targets=list(irf_settings["hom"]["targets"]),
        shock_path=shock_path,
        cache_enabled=config.cache_enabled,
        cache_dir=cache_dir,
        model_tag="hank_hom",
    )
    irfs_lin.update(irf_hom_all)

    generated_files.append(
        plot_impact_labor_supply_hom_vs_het(
            irfs_lin=irfs_lin,
            ss_map=ss,
            income_labels=config.income_labels,
            output_dir=output_path,
        )
    )

    J_hom = solve_partial_ha_jacobian(
        hh_block=models.hh_ext_hom,
        ss=ss["HANK-HomL"],
        inputs=list(irf_settings["hom"]["hh_inputs"]),
        T=T,
    )

    G_ha_hom = solve_general_ha_jacobian(
        dynamic_model=models.hank_hom,
        ss=ss["HANK-HomL"],
        unknowns=list(irf_settings["hom"]["unknowns"]),
        targets=list(irf_settings["hom"]["targets"]),
        exogenous=exogenous,
        T=T,
        hh_jacobian=J_hom,
    )

    hom_channels = compute_hom_consumption_channel_decomposition(
        J_hom=J_hom,
        G_ha_hom=G_ha_hom,
        shock_path=shock_path,
        ss_hom=ss["HANK-HomL"],
    )

    generated_files.append(
        plot_direct_vs_indirect_consumption(
            irfs_lin=irfs_lin,
            ss_map=ss,
            het_channels=het_channels,
            hom_channels=hom_channels,
            output_dir=output_path,
        )
    )

    generated_files.append(plot_core_irfs(irfs_lin=irfs_lin, ss_map=ss, output_dir=output_path))
    generated_files.append(plot_hours_bins(irfs_lin=irfs_lin, ss_map=ss, output_dir=output_path))
    generated_files.append(plot_consumption_bins(irfs_lin=irfs_lin, ss_map=ss, output_dir=output_path))
    generated_files.append(plot_hank_hetl_bins_l_contribution(irfs_lin=irfs_lin, output_dir=output_path))
    generated_files.append(plot_hank_hetl_bins_c_contribution(irfs_lin=irfs_lin, output_dir=output_path))

    # Sacrifice ratios and table 3
    _, last_values = compute_sacrifice_ratios(irfs_lin=irfs_lin, ss_map=ss)
    print("Sacrifice Ratios:")
    print(last_values)

    table3_df = table3_dataframe(last_values)
    print(table3_df.round(2))

    table3_latex_str = table3_latex(last_values)
    print(table3_latex_str)

    table_files = save_table_artifacts(
        output_dir=output_path,
        steady_state_df=full_steady_table_df,
        table2_df=table2_df,
        table3_df=table3_df,
        table3_latex_str=table3_latex_str,
    )

    robustness = _run_match_aggl_robustness(
        models=models,
        calibration=calibration,
        ss0=ss0,
        ss=ss,
        irfs_lin=irfs_lin,
        unknowns_hom=list(irf_settings["hom"]["unknowns"]),
        targets_hom=list(irf_settings["hom"]["targets"]),
        output_path=output_path,
        shock_path=shock_path,
    )
    table_files.update(robustness["table_files"])

    generated_files = _unique_keep_order(generated_files)

    metrics = {
        "baseline_ss": {
            "MPC": float(ss["HANK-HetL"]["MPC"]),
            "HTM": float(ss["HANK-HetL"]["HTM"]),
            "Y": float(ss["HANK-HetL"]["Y"]),
            "L": float(ss["HANK-HetL"]["L"]),
            "C": float(ss["HANK-HetL"]["C"]),
        },
        "impact_irf": {
            "Y": float(irfs_lin["HANK-HetL"]["Y"][0]),
            "C": float(irfs_lin["HANK-HetL"]["C"][0]),
            "pi": float(irfs_lin["HANK-HetL"]["pi"][0]),
        },
        "sacrifice_ratios": last_values,
        "robustness_matchAggL": {
            "implied_eis": robustness["implied_eis"],
            "sacrifice_ratios": robustness["sacrifice_ratios"],
        },
    }

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "figures": generated_files,
        "tables": table_files,
        "metrics": metrics,
    }

    manifest_path = output_path / "run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {
        "figures": generated_files,
        "table_files": table_files,
        "table_objects": {
            "steady_state_summary": full_steady_table_df,
            "table2": table2_df,
            "table3": table3_df,
            "matchAggL_implied_eis": robustness["df_match"],
            "table3_matchAggL": robustness["df_sr"],
        },
        "metrics": metrics,
        "manifest": manifest,
        "manifest_path": manifest_path,
    }
