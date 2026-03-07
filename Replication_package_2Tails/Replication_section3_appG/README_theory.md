# Python Replication Package (`Replication_section3_appG`)

## Replication code for Cantore et al. (2026) "A Tail of Labor Supply and a Tale of Monetary Policy"

This package provides replication material for the simulations presented in section 3 and Online Appendix G of the paper.
It solves two different versions of the one-asset HANK model: with and without heterogeneous labor supply.
It uses the toolbox and replication material of Auclert, Bardoczy, Rognlie, Straub (2021): "Using the Sequence-Space Jacobian to Solve and Estimate Heterogeneous-Agent Models" ([link to paper](https://www.bencebardoczy.com/publication/sequence-jacobian/sequence-jacobian.pdf)).

## Requirements

- Python 3.13
- Python packages listed in `requirements.txt`

## Run

From the repository root:

```bash
cd Replication_section3_appG
pip install --upgrade pip
pip install -r requirements.txt
python run_replication.py --config-dir config --output-dir Output
```

- Last run environment: Python 3.13
- Caching: if enabled in `config/solver_settings.json`, the code will create a local `.cache/` directory (which can be large). This submission archive does **not** include `.cache/`.

## Structure

- `run_replication.py`: full replication orchestrator.
- `config/*.json`: all calibration and solver settings.
- `src/hank_replication/model_blocks.py`: HH, GE, NKPC blocks.
- `src/hank_replication/model_factory.py`: SSJ model assembly.
- `src/hank_replication/solve.py`: SS/Jacobian/IRF solvers + optional disk cache.
- `src/hank_replication/plots.py`: all replication figures with paper/appendix filename conventions.
- `src/hank_replication/tables.py`: Table 2, Table 3, and steady-state summaries.
- `src/hank_replication/pipeline.py`: full replication pipeline and manifest export.


## Outputs

The script writes figures and tables to `Output/` with replication filenames and also writes:

- `steady_state_summary.md`
- `table2.md`
- `table3.md`
- `table3.tex`
- `matchAggL_implied_eis.md`
- `table3_matchAggL.md`
- `table3_matchAggL.tex`
- `run_manifest.json`

## Running times

5 minutes to run the full replications on a standard desktop machine.