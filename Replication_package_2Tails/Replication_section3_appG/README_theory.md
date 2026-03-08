# Python Replication Package (`Replication_section3_appG`)

## Replication code for Cantore et al. (2026) "A Tail of Labor Supply and a Tale of Monetary Policy"

This package provides replication material for the simulations in Section 3 and Online Appendix G of the paper.
It solves one-asset HANK models with and without heterogeneous labor supply, using the Sequence-Jacobian toolkit of Auclert, Bardoczy, Rognlie, and Straub (2021) ([paper link](https://www.bencebardoczy.com/publication/sequence-jacobian/sequence-jacobian.pdf)).

## Supported Environment

- Python 3.12 (official public target)
- Runtime dependencies pinned in `requirements.txt`
- Optional development/test dependencies in `requirements-dev.txt`

Last verified environment: Python 3.12.

## Install

From the repository root:

```bash
cd Replication_package_2Tails/Replication_section3_appG
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run

```bash
python run_replication.py --config-dir config --output-dir Output
```

## Success Check

A successful run creates `Output/run_manifest.json` plus tables and figures in `Output/`.
At minimum, verify these files exist:

- `Output/run_manifest.json`
- `Output/table2.md`
- `Output/table3.md`

## Notes

- Caching: if enabled in `config/solver_settings.json`, the code creates `.cache/` (can be large). This archive does not ship `.cache/`.
- LaTeX is optional. If a system `latex` executable is not available, the plotting code falls back to standard Matplotlib text rendering.

## Structure

- `run_replication.py`: full replication orchestrator.
- `config/*.json`: calibration and solver settings.
- `src/hank_replication/model_blocks.py`: HH, GE, NKPC blocks.
- `src/hank_replication/model_factory.py`: SSJ model assembly.
- `src/hank_replication/solve.py`: SS/Jacobian/IRF solvers + optional disk cache.
- `src/hank_replication/plots.py`: replication figures with paper/appendix filename conventions.
- `src/hank_replication/tables.py`: Table 2, Table 3, and steady-state summaries.
- `src/hank_replication/pipeline.py`: full replication pipeline and manifest export.

## Outputs

The script writes figures/tables to `Output/`, including:

- `steady_state_summary.md`
- `table2.md`
- `table3.md`
- `table3.tex`
- `matchAggL_implied_eis.md`
- `table3_matchAggL.md`
- `table3_matchAggL.tex`
- `run_manifest.json`

## Running Time

Around 5 minutes on a standard desktop machine (first run can be slightly longer due to JIT compilation and cache warm-up).
