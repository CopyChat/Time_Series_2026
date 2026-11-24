# ai_workspace index

Claude's processing files and illustrations for this project.

| Path | Role | Task and date | Status |
|---|---|---|---|
| `concepts/scripts/path_vs_distribution.py` | script | Explain "path" vs value distribution with synthetic data, 2026-11-10 | active |
| `concepts/figures/path_vs_distribution_synthetic.png` | figure | Output of the script above (synthetic data, not observations), 2026-11-10 | active |
| `meeting_page/scripts/q2_illustration.py` | script | Synthetic illustration of Q2 (record length; time of emergence) for the meeting page, 2026-11-10 | active |
| `meeting_page/figures/Q2_illustration_synthetic.png` | figure | Output of the script above, embedded in `presentation/2026-11-10_Matti_meeting.html` (synthetic, not results), 2026-11-10 | active |
| `nayak_reading/scripts/marginal_distribution_quantile_mapping.py` | script | Synthetic illustration of marginal distribution and quantile mapping (Nayak et al. 2026, Eq. 2), 2026-11-12 | active |
| `nayak_reading/figures/marginal_distribution_quantile_mapping_synthetic.png` | figure | Output of the script above (synthetic data, not observations), 2026-11-12 | active |
| `nayak_reading/tmp/nayak.txt` | tmp | Text extracted from the Nayak et al. PDF (pdftotext) for reading, 2026-11-12 | active |
| `shubham_meeting/scripts/year_ranking_wind_indicators.py` | script | Rank weather years 1982–2020 by onshore-wind statistics from the Mopo data (question B1 for Shubham), 2026-11-13 | active |
| `shubham_meeting/figures/year_rank_wind_onshore_indicators_1h_Mopo-regions_1982-2020_CorRES-Mopo_EUR.png` | figure | Output of the script above (real Mopo data, preliminary), 2026-11-13 | active |
| `shubham_meeting/figures/year_rank_wind_onshore_indicators_1h_Mopo-regions_1982-2020_CorRES-Mopo_EUR.csv` | table | Yearly indicators and ranks behind the figure, 2026-11-13 | active |
| `event_definition/scripts/shadow_price_toy_lp.py` | script | Toy one-node capacity-expansion LP (wind, solar, H2 chain) on a synthetic year: shadow prices, Σ d·λ = total cost, 14-day window as in Grochowicz 2024/2026; for explaining the SDE definition, 2026-11-16 | active |
| `event_definition/figures/shadow_price_toy_lp_synthetic.png` | figure | Output of the script above (synthetic data, not observations), 2026-11-16 | active |
| `event_definition/scripts/sde_dependence_experiments.py` | script | Toy experiments: system-defined event vs cost assumption, existing backup, rest of the year; residual-load deficit with fixed capacities, 2026-11-16 | active |
| `event_definition/figures/sde_dependence_toy_synthetic.csv` | table | Output of the script above (synthetic data), 2026-11-16 | active |
| `data_hub/scripts/organize_balmorel_dtu.py` | script | Move the public DTU Data files (doi:10.11583/DTU.c.7964141) out of Shubham's working copy into `~/local_data/Balmorel_DTU/raw/`, MD5-checked, and leave relative symlinks, 2026-11-20 | active (run once) |
| `pecd_download/scripts/cds_retrieve.py` | script | Standard-library CDS client (submit, poll, size, download) for PECD 4.2 (`sis-energy-pecd`); copy on the tt server at `/gpfs/labos/le2p/ctang/local_data/PECD/scripts/`, 2026-11-20 | active |
| `data_understanding/scripts/compute_stats.py` | script | Statistics and figures of the Balmorel_DTU data (demand, wind, PV, hydro), window 1982–2020; writes `01_data_understanding/tables/` and `figures/`, 2026-11-23 | active |
| `data_understanding/scripts/build_html.py` | script | Builds `01_data_understanding/data_understanding.html` from the tables, 2026-11-23 | active |
| `date_format/backups/` | backups | Copies of `01_research_plan.md`, `todo.md` and the 2026-11-23 note before the date-format change (月日 instead of MM-DD), 2026-11-23 | active |
| `data_understanding/scripts/supply_demand_heat.py` | script | Supply-demand overview (2025 capacities x CF) and heat/COP figures for the data page, 2026-11-23 | active |
