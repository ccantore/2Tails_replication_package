"""Table builders and text exports for replication outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def steady_state_summary_table(ss0: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for key, result in ss0.items():
        row = {
            "Model": key,
            "beta": result["beta"],
            "vphi": result["vphi"],
            "eis": result["eis"],
            "frish": result["frisch"],
            "min_a": result["min_a"],
            "rho_e": result["rho_e"],
            "sd_e": result["sd_e"],
            "mu": result["mu"],
            "kappa": result["kappa"],
            "B": result["B"],
            "phi": result["phi"],
            "n_e": result["n_e"],
            "n_a": result["n_a"],
            "max_a": result["max_a"],
            "rstar": result["rstar"],
            "HTM": result["HTM"],
            "MPC": result["MPC"],
            "L": result["L"],
            "goods_mkt": result["goods_mkt"],
            "labor_mkt": result["labor_mkt"],
            "asset_mkt": result["asset_mkt"],
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.sort_values("MPC", ascending=False)
    cols_to_round = df.columns.drop("Model")
    df[cols_to_round] = df[cols_to_round].map(lambda x: round(x, 3))
    return df


def table2(ss0: dict[str, Any]) -> pd.DataFrame:
    keys_low = ("HANK-HomL EIS025", "HANK-HetL EIS025")
    keys_baseline = ("HANK-HomL", "HANK-HetL")
    keys_high = ("HANK-HomL EIS1", "HANK-HetL EIS1")

    def get(record: dict[str, Any], key: str):
        return record[key] if key in record else np.nan

    tab = pd.DataFrame(
        {
            "Parameter": [r"$\beta$", r"$\varphi$", "$B$", "MPC"],
            "low σ HANK-HomL": [
                round(get(ss0[keys_low[0]], "beta"), 2),
                round(get(ss0[keys_low[0]], "vphi"), 2),
                round(get(ss0[keys_low[0]], "B"), 2),
                f"{round(100 * get(ss0[keys_low[0]], 'MPC'), 1)}%",
            ],
            "low σ HANK": [
                round(get(ss0[keys_low[1]], "beta"), 2),
                round(get(ss0[keys_low[1]], "vphi"), 2),
                round(get(ss0[keys_low[1]], "B"), 2),
                f"{round(100 * get(ss0[keys_low[1]], 'MPC'), 1)}%",
            ],
            "baseline σ HANK-HomL": [
                round(get(ss0[keys_baseline[0]], "beta"), 2),
                round(get(ss0[keys_baseline[0]], "vphi"), 2),
                round(get(ss0[keys_baseline[0]], "B"), 2),
                f"{round(100 * get(ss0[keys_baseline[0]], 'MPC'), 1)}%",
            ],
            "baseline σ HANK": [
                round(get(ss0[keys_baseline[1]], "beta"), 2),
                round(get(ss0[keys_baseline[1]], "vphi"), 2),
                round(get(ss0[keys_baseline[1]], "B"), 2),
                f"{round(100 * get(ss0[keys_baseline[1]], 'MPC'), 1)}%",
            ],
            "high σ HANK-HomL": [
                round(get(ss0[keys_high[0]], "beta"), 2),
                round(get(ss0[keys_high[0]], "vphi"), 2),
                round(get(ss0[keys_high[0]], "B"), 2),
                f"{round(100 * get(ss0[keys_high[0]], 'MPC'), 1)}%",
            ],
            "high σ HANK": [
                round(get(ss0[keys_high[1]], "beta"), 2),
                round(get(ss0[keys_high[1]], "vphi"), 2),
                round(get(ss0[keys_high[1]], "B"), 2),
                f"{round(100 * get(ss0[keys_high[1]], 'MPC'), 1)}%",
            ],
        }
    )
    return tab


def compute_sacrifice_ratios(irfs_lin: dict[str, Any], ss_map: dict[str, Any]) -> tuple[dict[str, np.ndarray], dict[str, float]]:
    sac_ratios: dict[str, np.ndarray] = {}
    for m in [
        "HANK-HomL EIS025",
        "HANK-HetL EIS025",
        "HANK-HomL",
        "HANK-HetL",
        "HANK-HomL EIS1",
        "HANK-HetL EIS1",
    ]:
        irfsY = 100 * irfs_lin[m]["Y"] / ss_map[m]["Y"]
        irfPi = 100 * irfs_lin[m]["pi"]
        sac_ratios[m] = np.cumsum(irfsY[:4]) / np.cumsum(irfPi[:4])

    last_values = {m: float(sac_ratios[m][-1]) for m in sac_ratios}
    return sac_ratios, last_values


def table3_dataframe(last_values: dict[str, float]) -> pd.DataFrame:
    rows = [
        ("Low $\\sigma$", "HANK-HomL EIS025", "HANK-HetL EIS025"),
        ("Baseline $\\sigma$", "HANK-HomL", "HANK-HetL"),
        ("High $\\sigma$", "HANK-HomL EIS1", "HANK-HetL EIS1"),
    ]
    table_data = [(label, last_values[hom], last_values[het]) for label, hom, het in rows]
    df = pd.DataFrame(table_data, columns=["", "HANK-HomL", "HANK"]).set_index("")
    return df


def table3_latex(last_values: dict[str, float]) -> str:
    latex_rows = [
        (r"Low $\\sigma$", last_values["HANK-HomL EIS025"], last_values["HANK-HetL EIS025"]),
        (r"Baseline $\\sigma$", last_values["HANK-HomL"], last_values["HANK-HetL"]),
        (r"High $\\sigma$", last_values["HANK-HomL EIS1"], last_values["HANK-HetL EIS1"]),
    ]
    latex_lines = [
        r"\\begin{tabular}{lcc}",
        r"\\toprule",
        r" & HANK-HomL & HANK \\",
        r"\\midrule",
    ] + [f"{label} & {v1:.2f} & {v2:.2f} \\\\" for label, v1, v2 in latex_rows] + [
        r"\\bottomrule",
        r"\\end{tabular}",
    ]
    return "\n".join(latex_lines)


def save_table_artifacts(
    output_dir: Path,
    steady_state_df: pd.DataFrame,
    table2_df: pd.DataFrame,
    table3_df: pd.DataFrame,
    table3_latex_str: str,
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    steady_md = output_dir / "steady_state_summary.md"
    table2_md = output_dir / "table2.md"
    table3_md = output_dir / "table3.md"
    table3_tex = output_dir / "table3.tex"

    steady_md.write_text(steady_state_df.to_markdown(index=False) + "\n", encoding="utf-8")
    table2_md.write_text(table2_df.to_markdown(index=False) + "\n", encoding="utf-8")
    table3_md.write_text(table3_df.round(2).to_markdown() + "\n", encoding="utf-8")
    table3_tex.write_text(table3_latex_str + "\n", encoding="utf-8")

    return {
        "steady_state_summary": steady_md.name,
        "table2": table2_md.name,
        "table3": table3_md.name,
        "table3_latex": table3_tex.name,
    }
