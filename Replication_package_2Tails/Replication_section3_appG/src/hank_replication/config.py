"""Configuration loading and scenario expansion for HANK replication."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import copy
import json
from typing import Any


@dataclass(frozen=True)
class ScenarioSpec:
    """A fully specified calibration scenario."""

    name: str
    family: str
    base_key: str
    overrides: dict[str, Any]


@dataclass(frozen=True)
class ReplicationConfig:
    """Top-level configuration loaded from JSON files."""

    base_calibration: dict[str, dict[str, Any]]
    scenario_specs: list[ScenarioSpec]
    solver_settings: dict[str, Any]

    @property
    def state_labels(self) -> list[str]:
        return list(self.solver_settings["plotting"]["state_labels"])

    @property
    def income_labels(self) -> list[str]:
        return list(self.solver_settings["plotting"]["income_labels"])

    @property
    def cache_enabled(self) -> bool:
        return bool(self.solver_settings.get("cache", {}).get("enabled", False))

    @property
    def cache_dir(self) -> str:
        return str(self.solver_settings.get("cache", {}).get("dir", ".cache"))

    def scenario_names(self) -> list[str]:
        return [spec.name for spec in self.scenario_specs]

    def get_family_scenarios(self, family: str) -> list[ScenarioSpec]:
        return [spec for spec in self.scenario_specs if spec.family == family]

    def expanded_calibration(self) -> dict[str, dict[str, Any]]:
        """Expand base calibrations with deterministic scenario overrides."""
        expanded: dict[str, dict[str, Any]] = {}
        for spec in self.scenario_specs:
            if spec.base_key not in self.base_calibration:
                raise KeyError(f"Unknown base calibration key: {spec.base_key}")
            params = copy.deepcopy(self.base_calibration[spec.base_key])
            params.update(spec.overrides)
            expanded[spec.name] = params
        return expanded

    def for_smoke_test(self, n_a: int = 40, n_e: int = 7, T: int = 40) -> "ReplicationConfig":
        """Return a reduced-size config for faster smoke tests."""
        base = copy.deepcopy(self.base_calibration)
        for key in base:
            base[key]["n_a"] = n_a
            base[key]["n_e"] = n_e
            base[key]["max_a"] = min(base[key].get("max_a", 150), 20)

        settings = copy.deepcopy(self.solver_settings)
        settings["irf"]["T"] = T
        settings["plotting"]["usetex"] = False
        settings["cache"]["enabled"] = False

        return ReplicationConfig(
            base_calibration=base,
            scenario_specs=list(self.scenario_specs),
            solver_settings=settings,
        )


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_replication_config(config_dir: Path | str) -> ReplicationConfig:
    """Load full replication config from JSON files in config_dir."""
    config_path = Path(config_dir)
    base_calibration = _load_json(config_path / "base_calibration.json")
    scenario_overrides = _load_json(config_path / "scenario_overrides.json")
    solver_settings = _load_json(config_path / "solver_settings.json")

    scenario_specs: list[ScenarioSpec] = []
    for family in ("het", "hom"):
        raw_specs = scenario_overrides.get(family, [])
        for raw in raw_specs:
            scenario_specs.append(
                ScenarioSpec(
                    name=raw["name"],
                    family=family,
                    base_key=raw["base_key"],
                    overrides=dict(raw.get("overrides", {})),
                )
            )

    return ReplicationConfig(
        base_calibration=base_calibration,
        scenario_specs=scenario_specs,
        solver_settings=solver_settings,
    )
