#!/usr/bin/env python3
"""Python replication entrypoint for the theoretical package."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hank_replication.config import load_replication_config
from hank_replication.pipeline import run_full_replication


# ## Replication code for Cantore et al. (2026) "A Tail of Labor Supply and a Tale of Monetary Policy"
# ### Heterogenous agents block for the Homogeneous labor model
# ### Heterogenous agents block for the Heterogenous labor model
# ### Define heterogenous inputs for both models
# ### Combine HA and inputs blocks
# ### Define heterogeneous outputs for both models
# ### Cobine HA, inputs and outputs blocks
# ### Define GE blocks for the Steady State DAG
# ### Combine HA blocks and GE blocks to define the models in steady state
# ### Baseline Calibration
# ### Solve for the steady state in the Het-L model
# ### Produce a table summarising the steady state of Het-L
# ### Mapping discrete income states into percentiles of income
# ### Plot policy functions - Appendix Figures G1 and G2
# ### Define the Phillips curve and set up the dynamic DAG
# ### Compute the GE Jacobian
# ### Produce figure 6
# ### We now solve the model under different values of EIS and Borrowing constraint
# ### Produce policy functions figures in Appendix - G3, G4, G6, G7, G9, G10, G12, G13, G15 and G16
# ### Produce IRFs figures in Appendix - G5, G8, G11, G14 and G17
# ### Reproduce Figure 7
# ### IRFs decomposition
# ### Decomposition of individual labor supplies (Figure 8)
# ### Decomposition of C - Figure G18 in Appendix
# ### Figure G19
# ### We now solve the HANK-HomL model for different calibrations of the EIS
# ### Display a table with the steady state values of all models
# ### Table 2
# ### Replicate impact figure G20 in Appendix
# ### Compute decomposition for HOM-L model
# ### Figure G21 in Appendix
# ### Figure G22 in Appendix
# ### Figure G23 in Appendix
# ### Figure G24 in Appendix
# ### Figure G25a in Appendix
# ### Figure G25b in Appendix
# ### We now compute the sacrifice ratios
# ### Table 3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run full Python replication for the HANK package")
    parser.add_argument(
        "--config-dir",
        default="config",
        help="Directory with base_calibration.json, scenario_overrides.json, solver_settings.json",
    )
    parser.add_argument(
        "--output-dir",
        default="Output",
        help="Directory where figures/tables/manifest are written",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_dir = (ROOT / args.config_dir).resolve()
    output_dir = (ROOT / args.output_dir).resolve()

    config = load_replication_config(config_dir)
    result = run_full_replication(config=config, output_dir=output_dir)

    print(f"Replication completed. Figures: {len(result['figures'])}")
    print(f"Manifest: {result['manifest_path']}")


if __name__ == "__main__":
    main()
