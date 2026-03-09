# README for "A tail of labor supply and a tale of monetary policy"

**Authors:** Cristiano Cantore, Filippo Ferroni, Haroon Mumtaz, Angeliki Theophilopoulou  
**Archive:** master replication package for the empirical and theoretical results  
**Last updated:** 2026-03-08

## Overview

This archive is the master replication package for the paper "A tail of labor supply and a tale of monetary policy." It covers both the empirical analysis and the theoretical HANK simulations.

The package is organized around two replication workflows:

1. Empirical workflow
   Folder: `Relication_section2_appB_D_E/`
   Main entrypoint: `run_empirical_replication.m`
   Main outputs: `Output/*.pdf`
   Optional: 
   - `data/Raw_data/CPS/RUN_ALL.do` to build the raw micro-data from sources.
   - `data/arrange_all_data.m` to build the datasets used in the estimation.

2. Theoretical workflow
   Folder: `Replication_section3_appG/`
   Main entrypoint: `run_replication.py`
   Main outputs: `Output/` figures, tables, and `run_manifest.json`

Workflow-specific documentation is provided in:

- `Relication_section2_appB_D_E/ReadMe_empirics.md`
- `Replication_section3_appG/README_theory.md`

Path conventions used below:

- Unless otherwise stated, paths are relative to `Replication_package_2Tails/`.
- In empirical subsections, the prefix `Relication_section2_appB_D_E/` is omitted when the context is already empirical.
- In theory subsections, the prefix `Replication_section3_appG/` is omitted when the context is already theoretical.

The folder name `Relication_section2_appB_D_E` is intentionally written exactly as shipped in the archive. Do not rename it, since the code uses that path.

The simplest route for a replicator is:

1. From `Relication_section2_appB_D_E/`, run `run_empirical_replication.m` using the bundled `data/Raw_data/DataEstimation/*.mat` inputs. The first run should use `full` mode.
2. From `Replication_section3_appG/`, run `run_replication.py`.
3. Optionally rebuild the empirical CPS-based intermediate data from the bundled raw data. The rebuild order is:
   empirical root `Relication_section2_appB_D_E/`
   then `data/Raw_data/CPS/RUN_ALL.do`
   then `data/arrange_all_data.m`

Some scripts called by `data/arrange_all_data.m` require the Windows-only [`x13tbx` MATLAB toolbox](https://www.mathworks.com/matlabcentral/fileexchange/49120-x-13-toolbox-for-seasonal-filtering).
No confidential data are used in the replication workflows.

## Coverage and Package Organization

### Coverage summary

- `Relication_section2_appB_D_E/` reproduces the empirical main-text figures (section 2) and the empirical online appendix figures (appendix B, D, E) backed by CPS, macro, and external-instrument data.
- `Replication_section3_appG/` reproduces the main HANK figures and tables (section 3), the Appendix G figures, and the Appendix G robustness tables.
- Generated outputs are printed in the `Output/` directories in both workflows.


### Package map

- `jeea-checklist.docx`: JEEA checklist included with the replication package.
- `Relication_section2_appB_D_E/data/Raw_data/`: raw empirical inputs, bundled intermediate data, and preprocessing scripts.
- `Relication_section2_appB_D_E/functions_new/`: MATLAB helper routines used by the empirical estimation and plotting scripts.
- `Relication_section2_appB_D_E/Output/`: empirical PDF outputs.
- `Replication_section3_appG/config/`: theory calibration and solver settings.
- `Replication_section3_appG/src/hank_replication/`: Python source code for the HANK replication pipeline.
- `Replication_section3_appG/Output/`: theory figures, tables, and run manifest.

## Data Availability and Provenance Statements

### Summary statements

- [x] The empirical workflow uses external data.
- [x] The theoretical workflow does not require external data downloads; it uses only the bundled configuration files and model code.
- [x] All data needed to run the public replication workflows described in this README are available in the archive.
- [x] No confidential data are required for the packaged workflows.
- [x] The archive includes `LICENSE.txt` with a package-level rights notice and references to bundled third-party software licenses.
- [x] The archive includes `LICENSE-third-party-data.txt` with source-specific redistribution notes for bundled third-party data.

The archive includes a package-level rights notice in `LICENSE.txt` and source-specific third-party data notes in `LICENSE-third-party-data.txt`. Those files are documentation aids. They do not override the original source terms.

### Current redistribution assessment for bundled third-party data

In this subsection, file paths are relative to the empirical raw-data folder.
Empirical raw-data folder: `Relication_section2_appB_D_E/` + `data/Raw_data/`

1. `CPS/CEPR_ORG/cepr_org_*.dta`
   Rights note: publicly downloadable source with attribution expectations documented by CEPR.
   Evidence from source: CEPRdata publicly distributes these extracts for download and asks users to cite them; the CEPR site terms state that the website is under CC BY 4.0.

2. Kansas longitudinal CPS file
   Folder: `CPS/kansas/`
   File: `CPS_harmonized_variable_longitudinally_matched_age16plus.dta`
   Rights note: source note documents a non-private-gain reproduction condition.
   Evidence from source: the Federal Reserve Bank of Kansas City disclaimer states that reproduction of information on its website may be made without limitation as to number, provided it is not for private gain.

3. `raw/un/*.xls`, `raw/AWHNONAG.xls`, `raw/AWHMAN.xls`, `raw/CES0500000030.xls`
   Rights note: public-domain source note.
   Evidence from source: BLS states that everything it publishes is in the public domain, except separately copyrighted photos and illustrations.

4. `raw/ebp2.xls`
   Rights note: public-domain source note unless otherwise indicated by the Board.
   Evidence from source: the Board states that, unless otherwise indicated, information on its website is in the public domain and may be copied and distributed with citation.

5. `raw/ff4_instruments_shared.xlsx`
   Rights note: source attribution note for the bundled instrument used in the MPI robustness exercise.
   Evidence from source: the archive documents this workbook as the conventional Fed monetary policy shock instrument in Miranda-Agrippino and Ricco (2021), "The Transmission of Monetary Policy Shocks".

6. `raw/FOMC_Bauer_Swanson.xlsx`
   Rights note: source note documents reproduction with credit and non-private-gain conditions unless otherwise specified.
   Evidence from source: FRBSF site policies permit reproduction of FRBSF information if it is not distributed for private gain and is appropriately credited, unless otherwise specified or third-party rights apply.

7. `raw/fred_md_new.xls`
   Rights note: bundled source with source-specific note documented in `LICENSE-third-party-data.txt`.
   Evidence from source: St. Louis Fed legal notices and FRED terms warn that some information or series may be owned by third parties, and permission may be required for uses beyond personal use.


### Summary of data availability

For empirical items below, paths are relative to `Relication_section2_appB_D_E/`.
For theory items below, paths are relative to `Replication_section3_appG/`.

1. CEPR CPS ORG extracts, 1979-2019
   Workflow: Empirics
   Path: `data/Raw_data/CPS/CEPR_ORG/cepr_org_*.dta`
   Notes: bundled copies of the CEPR CPS Outgoing Rotation Group extracts used to build the wage-distribution and hours measures. Source portal: [CEPR CPS data portal](https://ceprdata.org/).

2. Kansas City Fed harmonized and longitudinally matched CPS extract, vintage May 2024
   Workflow: Empirics
   Folder: `data/Raw_data/CPS/kansas/`
   File: `CPS_harmonized_variable_longitudinally_matched_age16plus.dta`
   Notes: bundled copy of the longitudinally matched CPS extract used for the full-time and three-month-employed exercises. Source portal: [Kansas City Fed CPS portal](https://cps.kansascityfed.org/). Vintage used in this package: `May 2024`.

3. FRED-MD monthly macro database, vintage 2021 M5
   Workflow: Empirics
   Path: `data/Raw_data/raw/fred_md_new.xls`
   Notes: bundled copy of the FRED-MD macro dataset used in the empirical preprocessing scripts. Download source: [FRED-MD page](https://www.stlouisfed.org/research/economists/mccracken/fred-databases). Vintage used in this package: `FRED-MD 2021 M5`. See `LICENSE-third-party-data.txt` for the source-specific note retained with the archive.

4. Excess bond premium series
   Workflow: Empirics
   Path: `data/Raw_data/raw/ebp2.xls`
   Notes: bundled copy of the EBP series used in the FAVAR preprocessing scripts. Source page: [Federal Reserve Board EBP page](https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html).

5. Additional public macro and labor-market time series
   Workflow: Empirics
   Folder: `data/Raw_data/raw/`
   Files: `AWHNONAG.xls`, `AWHMAN.xls`, `CES0500000030.xls`, `CPIAUCSL.xls`, `HOHWMN02USM065S.xls`, and `un/*.xls`
   Notes: bundled public macro, hours, CPI, wage, and unemployment spreadsheets used by the aggregate comparison and preprocessing scripts. These files are used directly by the MATLAB preprocessing code in `data/Raw_data/`.

6. Conventional Fed monetary policy shock instrument for the MPI robustness exercise
   Workflow: Empirics
   Path: `data/Raw_data/raw/ff4_instruments_shared.xlsx`
   Notes: used by `arrange_data_allworkers_MPI.m` in `data/Raw_data/` to build `data_QUANT1_MPI.mat` for `FigureD1`. Source: Miranda-Agrippino and Ricco (2021), "The Transmission of Monetary Policy Shocks".

7. FRBSF monthly monetary policy surprises workbook
   Workflow: Empirics
   Path: `data/Raw_data/raw/FOMC_Bauer_Swanson.xlsx`
   Notes: bundled copy of the FRBSF workbook also read by `arrange_data_allworkers_MPI.m` in `data/Raw_data/`. Source page: [FRBSF monetary policy surprises page](https://www.frbsf.org/research-and-insights/data-and-indicators/monetary-policy-surprises/).

8. Author-generated calibration and configuration files
   Workflow: Theory
   Path: `config/base_calibration.json`, `config/scenario_overrides.json`, `config/solver_settings.json`
   Notes: no external theory data download is needed. The theoretical package uses only the bundled calibration and solver settings.

### Dataset list

For empirical dataset items below, locations are relative to `Relication_section2_appB_D_E/`.
For theory dataset items below, locations are relative to `Replication_section3_appG/`.

1. Raw CPS and macro inputs for empirics
   Type: raw input data
   Format: `.dta`, `.xls`, `.xlsx`
   Location: `data/Raw_data/`
   Notes: bundled external data used by the empirical preprocessing scripts.

2. CPS-derived intermediate files
   Type: intermediate empirical data
   Format: `.csv`, `.mat`
   Location: `data/Raw_data/CPS/ELABORATED DATA/`
   Notes: created by the Stata and MATLAB preprocessing steps; already bundled.

3. Empirical estimation inputs
   Type: analysis data
   Format: `.mat`
   Location: `data/Raw_data/DataEstimation/`
   Notes: direct inputs for the empirical figure-replication scripts.

4. Empirical output figures
   Type: generated output
   Format: `.pdf`
   Location: `Output/`
   Notes: final empirical figures bundled in the archive.

5. Theory calibration inputs
   Type: analysis inputs
   Format: `.json`
   Location: `config/`
   Notes: bundled configuration files only; no external data.

6. Theory outputs
   Type: generated output
   Format: `.png`, `.md`, `.tex`, `.json`
   Location: `Output/`
   Notes: final figures, tables, and manifest bundled in the archive.

## Computational Requirements

### Software requirements

#### Empirical workflow

- Full raw-data reconstruction should be treated as a `Stata` plus `MATLAB` workflow.
- Software versions used in the empirical workflow:
  - `Stata/MP 18.5 (MP2)`
  - `MATLAB R2023b`
- Notes:
  - full data construction should be treated as Windows-oriented because of the seasonal-adjustment dependency used in the raw-data construction step;
  - estimation and plotting can be run once the intermediate data are present.

#### Theoretical workflow

- `Python 3.12`
- Runtime dependencies are pinned in `Replication_section3_appG/requirements.txt`:
  - `numpy==1.26.4`
  - `scipy==1.17.1`
  - `numba==0.62.1`
  - `matplotlib==3.10.8`
  - `pandas==3.0.1`
  - `tabulate==0.10.0`
  - `sequence-jacobian==1.0.0`
- Optional development dependency:
  - `pytest>=8.0` in `Replication_section3_appG/requirements-dev.txt`
- LaTeX is optional for plotting. If a system `latex` executable is not available, the plotting code falls back to standard Matplotlib text rendering.
- Solver caching is enabled by default in `Replication_section3_appG/config/solver_settings.json`, which writes cache files to `Replication_section3_appG/.cache/`.

### Controlled randomness

In the empirical list below, paths are relative to `Relication_section2_appB_D_E/`.

- The empirical estimation scripts set a deterministic MATLAB random seed via `rng(1,'twister')` at line 12 of the estimation scripts in:
  - `Figure1/estimate_new_f4_quant.m`
  - `Figure3/estimate_new_f4_quant.m`
  - `Figure4/estimate_new_f4_quant_FT.m`
  - `Figure5/estimate_new_f4GR.m`
  - `FigureD1/estimate_new_f4_quant.m`
  - `FigureD2/estimate_new_f4_quant_sign.m`
  - `FigureD4/estimate_new_f4_quant.m`
  - `FigureD7/estimate_new_f4_quant.m`
  - `FigureE1/estimate_new_f4_quant.m`
- The public theory runner `Replication_section3_appG/run_replication.py` does not rely on a pseudo-random simulation step in the exposed replication pipeline.

### Memory, runtime, and storage requirements

#### Approximate runtime

- Running the empirical MATLAB estimation from the bundled `DataEstimation/*.mat` files:
  - `data/arrange_all_data.m`: about 35 minutes.
  - `run_empirical_replication.m` in `full` mode: about 31 minutes.
- Building the CPS-derived empirical inputs from raw bundled data:
  - `RUN_ALL.do` reports approximate component times of about 90 seconds, 90 seconds, and 9 minutes for the main Stata substeps
  - after that raw rebuild, `data/arrange_all_data.m` must still be run in MATLAB
- Running the theory package: about 5 minutes on a standard desktop machine, with the first run slightly slower if the cache is empty.
  
#### Approximate storage

- Current size:
  - `Replication_package_2Tails/`: about 22 GB
  - `Relication_section2_appB_D_E/`: about 22 GB
  - `Replication_section3_appG/`: about 4.2 MB



#### Reported verification hardware

- The most recent run was on a Windows 11 Enterprise machine with:
  - Intel Core i7-14700
  - 32 GB RAM

## Description of Programs and Code

Empirical paths in this section are relative to `Relication_section2_appB_D_E/`.
Theory paths in this section are relative to `Replication_section3_appG/`.

1. `data/Raw_data/CPS/RUN_ALL.do`
   Purpose: Stata master script that rebuilds the CPS-derived empirical CSV inputs from the bundled CEPR and Kansas CPS files.

2. `data/arrange_all_data.m`
   Purpose: MATLAB master preprocessing script that builds the empirical `.mat` datasets in `data/Raw_data/DataEstimation/` and related cached intermediate files.

3. `run_empirical_replication.m`
   Purpose: main empirical replication runner; the archival workflow uses `full` mode to regenerate the empirical figures in `Output/`.

4. `functions_new/`
   Purpose: MATLAB helper functions for FAVAR estimation, plotting, and export.

5. `run_replication.py`
   Purpose: main Python entrypoint for the HANK replication pipeline.

6. `src/hank_replication/pipeline.py`
   Purpose: end-to-end orchestration of steady states, IRFs, decomposition figures, table exports, and manifest writing.

7. `src/hank_replication/plots.py`
   Purpose: theory figure writers.

8. `src/hank_replication/tables.py`
   Purpose: theory table builders and Markdown/LaTeX exports.

9. `config/*.json`
   Purpose: theory calibration, scenario overrides, plotting, cache, and solver settings.

## Detailed instructions to Replicators

Follow the steps below from the root of this archive, i.e. from `Replication_package_2Tails/`.

### 1. Run the empirical MATLAB figures from the bundled intermediate inputs

In this empirical subsection, paths are relative to `Relication_section2_appB_D_E/`.

This is the recommended empirical rerun path for a public replicator. The necessary `.mat` analysis inputs are already bundled in `data/Raw_data/DataEstimation/`, so a full raw-data rebuild is not required.

In MATLAB:

```matlab
cd('Relication_section2_appB_D_E')
addpath(genpath(pwd))
mode = 'full';
run('run_empirical_replication.m')
```

Notes:

- `mode = 'full'` reruns estimation and plotting.
- Figure-specific cache files such as `results.mat` and `priors_1.mat` are generated during a full run when needed, but they are not present in the submission archive.
- Outputs are written to `Output/`.

### 2. Optional: fully rebuild the empirical intermediate data from the bundled raw inputs

Use this route only if you want to reconstruct the CPS-derived intermediate files instead of relying on the bundled `DataEstimation/*.mat` files.

#### 2a. Run the Stata CPS master script

Open `data/Raw_data/CPS/RUN_ALL.do` and edit the `global dir` line so that it points to the absolute path of your local `data/Raw_data/CPS` folder.

Then run `RUN_ALL.do` in Stata. This step writes CPS-derived CSV and cached `.mat` files to:

- `data/Raw_data/CPS/ELABORATED DATA/`

#### 2b. Run the MATLAB empirical preprocessing script

In MATLAB:

```matlab
cd('Relication_section2_appB_D_E/data')
addpath(genpath(pwd))
run('arrange_all_data.m')
```

This step rebuilds the empirical analysis inputs in:

- `data/Raw_data/DataEstimation/`

#### 2c. Run the empirical figure replication

After the preprocessing steps finish, return to:

```matlab
cd('Relication_section2_appB_D_E')
addpath(genpath(pwd))
mode = 'full';
run('run_empirical_replication.m')
```

## List of Tables, Figures, and Output Files

### Empirical outputs

In this empirical output subsection, file names are relative to `Relication_section2_appB_D_E/Output/`.

All empirical outputs are produced by `run_empirical_replication.m` and written to `Output/`.

| Manuscript object | Output file | Runner job or source |
| --- | --- | --- |
| Main text empirical figure: "Impulse responses to a monetary policy shock" | `figure1.pdf` | `Figure1` |
| Main text empirical figure: "Distribution of responses to a monetary policy shock" | `figure2_6.pdf` | `Figure2` |
| Main text empirical figure: "Impulse responses to a monetary policy shock" (counterfactual hours comparison) | `figure3.pdf` | `Figure3` |
| Main text empirical figure: "Responses of hours for full-time employees" | `figure_ft_2.pdf` | `Figure4` |
| Main text empirical figure: "Distribution of responses of the growth rate of hours worked and of employment after monetary policy tightening" | `figure4_6.pdf` | `Figure5` |
| Online appendix figure `CPS:char_us` | `char.pdf` | `FigureA1_A2` |
| Online appendix figure `CPS:char_us1` | `industry_by_wage_quintile_cepr_av_app.pdf` | `FigureA1_A2` |
| Online appendix figure `Agg_h_us` | `ag_hours.pdf` | `FigureA3` |
| Online appendix figure `fig:CPS_robustness1` | `figure_mpi.pdf` | `FigureD1` |
| Online appendix figure `fig:CPS_robustness2` | `figure_sign.pdf` | `FigureD2` |
| Online appendix figure `ind` | `industry_by_wage_quintile_cepr_av.pdf` | `FigureD3` |
| Online appendix figure `irf_ind` | `hours_ind.pdf` | `FigureD4` |
| Online appendix figure `college2` | `college_by_wage2.pdf` | `FigureD5` |
| Online appendix figure `college3` | `college_by_wage3.pdf` | `FigureD6` |
| Online appendix figure `irf_educ1` | `hours_educ1.pdf` | `FigureD7` |
| Online appendix figure `FF:wages:IRF` | `figure_wages.pdf` | `FigureD8` |
| Online appendix figure `fig:hours_3M` | `figure_panel3M.pdf` | `FigureE1` |


### 3. Run the theory package

```bash
cd Replication_section3_appG
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run_replication.py --config-dir config --output-dir Output
```

Successful completion should refresh `Output/run_manifest.json` and the bundled figure and table files in `Output/`.



### Theoretical outputs

In this theory output subsection, file names are relative to `Replication_section3_appG/Output/`.

All theory outputs are produced by `run_replication.py` and written to `Output/`.

| Manuscript object | Output file(s) | Notes |
| --- | --- | --- |
| Main text table `tab:HANK_calib` | `config/base_calibration.json`; `Output/steady_state_summary.md` | |
| Main text figure `fig:baseline_irfs` | `baseline_IRFs_with_L_and_C.png` | Bundled and regenerated by the main theory runner |
| Main text figure `fig:labor_supply_models_across_income` | `labor_supply_models_across_income.png` | Bundled and regenerated by the main theory runner |
| Main text figure `fig:hetl_labor_decomp_combined` | `HANK_HetL_decomp_bins_H_comb.png` | Bundled and regenerated by the main theory runner |
| Main text table `tab:HANK_calib_comp` | `table2.md` | Exported by `tables.py` |
| Main text table `tab:sacrifice_ratios` | `table3.md`, `table3.tex` | Exported by `tables.py` |
| Appendix G table `tab:income_states` | printed to console during the run | The pipeline prints the income-state mapping via `_print_income_state_mapping(...)`. |
| Appendix G figure `fig:LS_PC` | `labor_supply_vs_assets.png`, `labor_supply_vs_assets_zoomed.png` | Baseline policy-function figure |
| Appendix G figure `fig:C_policy` | `consumption_vs_assets.png` | Baseline consumption policy function |
| Appendix G figure `fig:LS_PC_a1_s1` | `labor_supply_vs_assets_HANK-HetL EIS1.png`, `labor_supply_vs_assets_zoomed_HANK-HetL EIS1.png` | Alternative calibration |
| Appendix G figure `fig:C_policy_a1_s1` | `consumption_vs_assets_HANK-HetL EIS1.png` | Alternative calibration |
| Appendix G figure `fig:irfs_a1_s1` | `IRFs_with_L_and_C_HANK-HetL EIS1.png` | Alternative calibration |
| Appendix G figure `fig:LS_PC_a1_s025` | `labor_supply_vs_assets_HANK-HetL EIS025.png`, `labor_supply_vs_assets_zoomed_HANK-HetL EIS025.png` | Alternative calibration |
| Appendix G figure `fig:C_policy_a1_s025` | `consumption_vs_assets_HANK-HetL EIS025.png` | Alternative calibration |
| Appendix G figure `fig:irfs_a1_s025` | `IRFs_with_L_and_C_HANK-HetL EIS025.png` | Alternative calibration |
| Appendix G figure `fig:LS_PC_a0_s1` | `labor_supply_vs_assets_HANK-HetL EIS1 a0.png`, `labor_supply_vs_assets_zoomed_HANK-HetL EIS1 a0.png` | Alternative calibration |
| Appendix G figure `fig:C_policy_a0_s1` | `consumption_vs_assets_HANK-HetL EIS1 a0.png` | Alternative calibration |
| Appendix G figure `fig:irfs_a0_s1` | `IRFs_with_L_and_C_HANK-HetL EIS1 a0.png` | Alternative calibration |
| Appendix G figure `fig:LS_PC_a0_s05` | `labor_supply_vs_assets_HANK-HetL a0.png`, `labor_supply_vs_assets_zoomed_HANK-HetL a0.png` | Alternative calibration |
| Appendix G figure `fig:C_policy_a0_s05` | `consumption_vs_assets_HANK-HetL a0.png` | Alternative calibration |
| Appendix G figure `fig:irfs_a0_s05` | `IRFs_with_L_and_C_HANK-HetL a0.png` | Alternative calibration |
| Appendix G figure `fig:LS_PC_a0_s025` | `labor_supply_vs_assets_HANK-HetL EIS025 a0.png`, `labor_supply_vs_assets_zoomed_HANK-HetL EIS025 a0.png` | Alternative calibration |
| Appendix G figure `fig:C_policy_a0_s025` | `consumption_vs_assets_HANK-HetL EIS025 a0.png` | Alternative calibration |
| Appendix G figure `fig:irfs_a0_s025` | `IRFs_with_L_and_C_HANK-HetL EIS025 a0.png` | Alternative calibration |
| Appendix G figure `fig:hetl_cons_decomp` | `HANK_HetL_decomp_C_comb.png` | Consumption decomposition |
| Appendix G figure `fig:hetl_cons_bins` | `HANK_HetL_decomp_bins_C_comb.png` | Consumption decomposition by income bin |
| Appendix G figure `fig:impact_H_eis` | `impact_labor_supply_hom_vs_het.png` | HANK vs HANK-HomL comparison |
| Appendix G figure `fig:dir_vs_indir` | `HANK_direct_vs_indirect_C_simple.png` | Direct vs indirect consumption effects |
| Appendix G table `tab:sacrifice_ratios_aggL` | `table3_matchAggL.md`, `table3_matchAggL.tex` | Robustness table; implied EIS file is `matchAggL_implied_eis.md` |
| Appendix G figure `fig:core_irfs` | `HANK_irfs_core_vars.png` | Core macro responses |
| Appendix G figure `fig:L_bins_irfs` | `HANK_irfs_H_bins.png` | Labor responses by income bin |
| Appendix G figure `fig:C_bins_irfs` | `HANK_irfs_C_bins.png` | Consumption responses by income bin |
| Appendix G figure `fig:contribution` | `HANK_HetL_bins_L_contribution.png`, `HANK_HetL_bins_C_contribution.png` | Two-panel contribution figure |

## References and Data Citations

- CEPR. CPS ORG Uniform Extracts. [CEPR data portal](https://ceprdata.org/).
- Federal Reserve Bank of Kansas City. Harmonized and longitudinally matched CPS extract. [Kansas City Fed CPS portal](https://cps.kansascityfed.org/).
- McCracken, Michael W., and Serena Ng. FRED-MD monthly database. [Federal Reserve Bank of St. Louis FRED-MD page](https://www.stlouisfed.org/research/economists/mccracken/fred-databases).
- Federal Reserve Board. Excess bond premium series update page. [Federal Reserve Board EBP page](https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html).
- Miranda-Agrippino, Silvia, and Giovanni Ricco. 2021. "The Transmission of Monetary Policy Shocks." 
- Federal Reserve Bank of San Francisco. Monetary policy surprises data page. [FRBSF monetary policy surprises page](https://www.frbsf.org/research-and-insights/data-and-indicators/monetary-policy-surprises/).
- U.S. Bureau of Labor Statistics public time-series data, as bundled in the empirical raw-data folders `data/Raw_data/raw/` and `data/Raw_data/raw/un/`
