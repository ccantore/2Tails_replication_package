from pathlib import Path

from hank_replication.config import load_replication_config


def test_scenario_expansion_order_and_overrides() -> None:
    config_dir = Path(__file__).resolve().parents[1] / "config"
    config = load_replication_config(config_dir)

    expected_names = [
        "HANK-HetL EIS1",
        "HANK-HetL",
        "HANK-HetL EIS025",
        "HANK-HetL EIS1 a0",
        "HANK-HetL a0",
        "HANK-HetL EIS025 a0",
        "HANK-HomL EIS1",
        "HANK-HomL",
        "HANK-HomL EIS025",
        "HANK-HomL EIS1 a0",
        "HANK-HomL a0",
        "HANK-HomL EIS025 a0",
    ]

    assert config.scenario_names() == expected_names

    expanded = config.expanded_calibration()
    assert set(expanded.keys()) == set(expected_names)

    assert expanded["HANK-HetL EIS1"]["eis"] == 1.0
    assert expanded["HANK-HetL EIS025"]["eis"] == 0.25
    assert expanded["HANK-HetL a0"]["min_a"] == 0.0

    assert expanded["HANK-HomL EIS1"]["eis"] == 1.1
    assert expanded["HANK-HomL EIS025"]["eis"] == 0.445
    assert expanded["HANK-HomL EIS025 a0"]["min_a"] == 0.0
