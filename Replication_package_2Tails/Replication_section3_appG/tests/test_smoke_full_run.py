import json
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("sequence_jacobian")

from hank_replication.config import load_replication_config
from hank_replication.pipeline import run_full_replication


@pytest.mark.slow
def test_smoke_full_run_generates_expected_outputs(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_replication_config(root / "config").for_smoke_test(n_a=24, n_e=7, T=24)

    output_dir = tmp_path / "Output"
    result = run_full_replication(config=config, output_dir=output_dir)

    manifest_path = output_dir / "run_manifest.json"
    assert manifest_path.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert set(manifest.keys()) == {"generated_at_utc", "figures", "tables", "metrics"}

    expected_static = [
        "labor_supply_vs_assets.png",
        "labor_supply_vs_assets_zoomed.png",
        "consumption_vs_assets.png",
        "baseline_IRFs_with_L_and_C.png",
        "labor_supply_models_across_income.png",
        "HANK_HetL_decomp_bins_H_comb.png",
        "HANK_HetL_decomp_C_comb.png",
        "HANK_HetL_decomp_bins_C_comb.png",
        "impact_labor_supply_hom_vs_het.png",
        "HANK_direct_vs_indirect_C_simple.png",
        "HANK_irfs_core_vars.png",
        "HANK_irfs_H_bins.png",
        "HANK_irfs_C_bins.png",
        "HANK_HetL_bins_L_contribution.png",
        "HANK_HetL_bins_C_contribution.png",
    ]

    het_names = [spec.name for spec in config.get_family_scenarios("het")]
    expected_scenario = []
    for name in het_names:
        expected_scenario.extend(
            [
                f"labor_supply_vs_assets_{name}.png",
                f"labor_supply_vs_assets_zoomed_{name}.png",
                f"consumption_vs_assets_{name}.png",
                f"IRFs_with_L_and_C_{name}.png",
            ]
        )

    for filename in expected_static + expected_scenario:
        assert (output_dir / filename).exists(), filename

    for table_file in [
        "steady_state_summary.md",
        "table2.md",
        "table3.md",
        "table3.tex",
        "matchAggL_implied_eis.md",
        "table3_matchAggL.md",
        "table3_matchAggL.tex",
    ]:
        assert (output_dir / table_file).exists(), table_file

    metrics = manifest["metrics"]
    for key in ["MPC", "HTM", "Y", "L", "C"]:
        assert np.isfinite(metrics["baseline_ss"][key]), key

    for key in ["Y", "C", "pi"]:
        assert np.isfinite(metrics["impact_irf"][key]), key

    assert "robustness_matchAggL" in metrics

    table2_text = (output_dir / "table2.md").read_text(encoding="utf-8")
    table3_text = (output_dir / "table3.md").read_text(encoding="utf-8")
    table3_match_text = (output_dir / "table3_matchAggL.md").read_text(encoding="utf-8")
    assert "low σ HANK-HomL" in table2_text
    assert "Baseline" in table3_text
    assert "match agg" in table3_match_text

    assert Path(result["manifest_path"]) == manifest_path
