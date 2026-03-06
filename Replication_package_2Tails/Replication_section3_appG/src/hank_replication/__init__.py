"""HANK replication package."""

from .config import ReplicationConfig, ScenarioSpec, load_replication_config


def run_full_replication(*args, **kwargs):
    from .pipeline import run_full_replication as _run_full_replication

    return _run_full_replication(*args, **kwargs)

__all__ = [
    "ReplicationConfig",
    "ScenarioSpec",
    "load_replication_config",
    "run_full_replication",
]
