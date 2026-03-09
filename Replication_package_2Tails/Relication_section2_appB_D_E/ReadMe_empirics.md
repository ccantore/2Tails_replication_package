# Stata and Matlab Replication Package (`Replication_section2_appB_D_E`)

## Replication code for Cantore et al. (2026) "A Tail of Labor Supply and a Tale of Monetary Policy" for Section 2 and Appendix B, D, E

This package provides replication material for the estimation presented in section 2 and Online Appendix B, D, E of the paper.
It computes all datasets used in the estimation from CPS microdata and macro data.
It then uses these datasets for the estimation and prints all figures in PDFs to Replication_files_section2_appB_D_E/Output/.

## Requirements

- Operating System: 
    - Windows only for data construction (due to the use of seasonal adjustment X-13-ARIMA-SEATS software).
    - Linux and MacOS are supported for the estimation and plotting.
  
- Software:
  - Matlab R2023b
  - Stata/MP 18.5 (MP2)

### External Data Sources (Including vintage information)

1. CEPR CPS ORG extracts (1979-2019): uniform CPS outgoing rotation group (ORG) data extracts from CEPR.
   - Included in this package under: `data/Raw_data/CPS/CEPR_ORG/`
   - Website (optional re-download): <https://ceprdata.org/>
   - Vintage used in this package: `CEPR CPS ORG Feb 2026`
2. Kansas City Fed harmonized and longitudinally matched CPS extract:
   - Included in this package under: `data/Raw_data/CPS/kansas/` (`CPS_harmonized_variable_longitudinally_matched_age16plus.dta`)
   - Website (optional re-download): <https://cps.kansascityfed.org/>
   - Vintage used in this package: `Kansas City Fed harmonized and longitudinally matched CPS extract May 2024`
3. FRED-MD monthly macro database:
   - File used in this package: `data/Raw_data/raw/fred_md_new.xls`
   - Vintage used in this package: `FRED-MD 2021 M5`
   - Download source: <https://www.stlouisfed.org/research/economists/mccracken/fred-databases>
4. Excess bond premium (EBP) series:
   - File used in this package: `data/Raw_data/raw/ebp2.xls`
   - Source page: <https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html>
   - Direct download CSV: <https://www.federalreserve.gov/econres/notes/feds-notes/ebp_csv.csv>
5. Additional BLS labor-market and price series:
   - Files used in this package: `data/Raw_data/raw/AWHNONAG.xls`, `AWHMAN.xls`, `CES0500000030.xls`, `CPIAUCSL.xls`, `HOHWMN02USM065S.xls`, and the detailed unemployment spreadsheets in `data/Raw_data/raw/un/`
   - These bundled BLS-origin series are used by the MATLAB preprocessing scripts for aggregate hours, wage, price, and unemployment comparisons, including `data/Raw_data/CPS/MatlabCode/extract_data_1_quantiles.m`, `data/Raw_data/CPS/MatlabCode/construct_aggregate_counterfactual.m`, and the `data/Raw_data/arrange_data_*.m` scripts.
   - Public source institution: U.S. Bureau of Labor Statistics
   - Website (optional reference): <https://www.bls.gov/data/>
6. Conventional Fed monetary policy shock instrument:
   - File used in this package: `data/Raw_data/raw/ff4_instruments_shared.xlsx`
   - Used by `data/Raw_data/arrange_data_allworkers_MPI.m` to construct `data_QUANT1_MPI.mat` for the MPI robustness exercise.
   - Miranda-Agrippino and Ricco (2021), "The Transmission of Monetary Policy Shocks"
7. FRBSF monetary policy surprises workbook:
   - File used in this package: `data/Raw_data/raw/FOMC_Bauer_Swanson.xlsx`
   - Also read by `data/Raw_data/arrange_data_allworkers_MPI.m`
   - Source page: <https://www.frbsf.org/research-and-insights/data-and-indicators/monetary-policy-surprises/>

## Run

### Step A: CPS data construction

Open `data/Raw_data/CPS/RUN_ALL.do` and set `global dir` once to the absolute path of your local `CPS/` folder.
In Stata, run `RUN_ALL.do` (from any working directory).
`RUN_ALL.do` automatically detects Windows vs macOS and sets the appropriate path separator (`\` or `/`). You do not need to edit path separators elsewhere in the code.
`RUN_ALL.do` automatically runs the CEPR and Kansas extraction scripts and writes:
- CSV outputs in `data/Raw_data/CPS/ELABORATED DATA/` (e.g., `data_YYYY.csv`, `dataun_YYYY.csv`, `YYYY_zz.csv`)
- Approximate running times of each called do-file are reported inside `RUN_ALL.do`.
Once the CEPR CSVs are present in `data/Raw_data/CPS/ELABORATED DATA/`, you can regenerate selected appendix figures:

### Step B: Data preparation for estimation

Run `data/arrange_all_data.m` to prepare the data for estimation.
- .mat outputs in `data/Raw_data/DataEstimation/` (e.g., `data_QUANT1.mat`)
- Figure outputs in `Replication_files_section2_appB_D_E/Output/` 

### Step C: Estimation

Run `run_empirical_replication.m` in `full` mode to run the estimation and plotting workflow.
  - Figure outputs are written to `Replication_files_section2_appB_D_E/Output/`
  - Figure-specific cache files such as `results.mat` and `priors_1.mat` are generated during the run when needed, but they are not bundled in the submission archive.

For the clean archival workflow, use:

```matlab
mode = 'full';
run('run_empirical_replication.m')
```



## Structure

- `data/`: contains the data construction and preparation code.
- `data/functions/`: contains the functions used in the estimation and plotting.
- `data/Raw_data/`: contains the raw data and the scripts used to construct the datasets used in the estimation and plotting.
- `data/Raw_data/CPS/CEPR_ORG/`: contains the CEPR CPS ORG data.
- `data/Raw_data/CPS/kansas/`: contains the Kansas City Fed harmonized and longitudinally matched CPS data.
- `data/Raw_data/raw/`: contains the raw macro data.
- `data/Raw_data/raw/fred_md_new.xls`: contains the FRED-MD monthly macro database.
- `data/Raw_data/raw/ebp2.xls`: contains the Excess bond premium (EBP) series.
- `data/Raw_data/raw/AWHNONAG.xls`, `AWHMAN.xls`, `CES0500000030.xls`, `CPIAUCSL.xls`, `HOHWMN02USM065S.xls`, and `data/Raw_data/raw/un/`: contain bundled BLS-origin hours, wage, price, and unemployment series used by the aggregate comparison and preprocessing scripts.
- `data/Raw_data/raw/ff4_instruments_shared.xlsx`: contains the conventional Fed monetary policy shock instrument used in the MPI robustness exercise.
- `data/Raw_data/raw/FOMC_Bauer_Swanson.xlsx`: contains the FRBSF monthly monetary policy surprises workbook also read by the MPI preprocessing code.
- `data/arrange_all_data.m`: prepares the data for estimation.
- `run_empirical_replication.m`: runs the empirical replication in full or plotting only mode and writes the final PDFs to `Output/`.
- `functions_new/`: contains the scripts used for the estimation and plotting.
- `Output/`: contains the figures and tables generated by the estimation and plotting.

## Running times
Desktop Specs:
Processor	Intel(R) Core(TM) i7-14700 (2.10 GHz)
RAM 	32,0 GB (31,8 GB utilizzabile)
Sistem	SO 64 bit, processor x64

Windows Specs:
Edition	Windows 11 Enterprise
Version	25H2

arrange_all_data.
[2026-03-06 09:12] Start time
[2026-03-06 09:47] Replication runner

run_empirics_replication.m 
[2026-03-05 17:52:01] Start time
[2026-03-05 18:23:35] Replication runner summary
Mode: full
Total jobs: 11
Succeeded: 11
Failed: 0
[2026-03-05 18:23:35] All jobs completed successfully.
