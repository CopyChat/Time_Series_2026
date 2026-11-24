# Time Series 2026 — data inventory

Every dataset the project reads or writes: where it comes from, where it lives, where the backup is,
which code makes it, and when it was made.

- Written: **2026-10-15**, at the start of the project (idea stage, DTU Wind visit 10 Nov 2026 – 5 Feb 2027).
- First dataset obtained on 2026-11-13 (Mopo VRE data, section 2). Nothing on the server yet.
- Hardlinked as `~/ctang.CODE/CT_DATA_HUB/PROJECT_DATA_USE/Time_Series_2026_DATA.md`; editing either
  path edits both. If an editor breaks the link, `check_local_data.py` restores it.
- Registry of record for shared-source locations: `~/ctang.CODE/CT_DATA_HUB/registry.toml`. Nothing of
  this project is registered there yet.

## 1. Candidate inputs (not yet chosen)

Named in `working/2026-10-15_topic_keywords_references.md` section 4 as options to settle with Matti Koivisto (DTU).
None has been obtained; this list is a plan, not an inventory.

| Candidate | Content | Status |
|---|---|---|
| CorRES European runs (DTU) | simulated wind/solar generation time series | to ask DTU |
| EURO-CORDEX | regional climate model wind fields | to ask DTU / reuse from Wind_CORDEX_2025 |
| CorRES_2026 outputs (Réunion) | CorRES wind/solar series from the CorRES_2026 project | possible, not decided |
| CorRES Mopo pan-European VRE data (Zenodo, doi:10.5281/zenodo.17950648, CC-BY-4.0) | hourly simulated wind (9 onshore, 4 offshore technologies + existing) and PV (3 technologies), ERA5 + GWA; 1.6 GB zip | public; years and zones not stated on the record (added 2026-11-09) |
| Mopo climate projections (Zenodo, doi:10.5281/zenodo.18549865) | same, MPI-ESM1-2-HR and EC-Earth3 × SSP2-4.5/SSP5-8.5, 2015–2100 hourly; 12.6 GB zip | public (added 2026-11-09) |
| PECD 4.2 (C3S/ENTSO-E, doi:10.24381/cds.f323c5ec) | wind/solar capacity factors (wind by CorRES), hydro, temperature; ERA5 from 1950 + 6 CMIP6 × 4 SSP; NUTS0/NUTS2/PEON/P2ON zones | public on CDS (added 2026-11-09) |

## 2. Datasets used

| Registry key | Path | Copies | Content | Used by | Obtained |
|---|---|---|---|---|---|
| `Mopo/raw/VRE_pan_european` | `~/local_data/Mopo/raw/` | Mac only (no server or external copy yet) | Zenodo zip (1.6 GB), doi:10.5281/zenodo.17950648. Hourly capacity factors 1980–2021, UTC; 126 onshore regions (PECD-based), 77 offshore regions. Extracted so far: `wind-on-SP277-HH100.csv`, `wind-off-FB-SP370-HH155.csv`, `solar-PV-no-tracking.csv`, installed capacities, info PDFs | `ai_workspace/shubham_meeting/scripts/year_ranking_wind_indicators.py` (reads the onshore wind file and the 2025 regional capacities) | 2026-11-13 |
| `Balmorel_DTU/raw/pan_european` | `~/local_data/Balmorel_DTU/raw/<item>/` (40 CSVs, 4.8 GB; read-only) | Mac + server `/gpfs/scratch/le2p/local_data/Balmorel_DTU` (MD5 verified 2026-11-21) | Public DTU Data collection doi:10.11583/DTU.c.7964141. Items: `electricity_demand/`, `heat_demand/`, `heat_pump_COP/`, `hydro_inflow/`, `wind_onshore/` (Existing + 12 future techs), `wind_offshore/` (Existing + `Future_bottom_fixed/SP316_HH155_RGB.csv`), `solar_PV/` (9 techs); provider `readme.txt` in each; provenance and MD5 list in `~/local_data/Balmorel_DTU/README.md`. Content notes: see the next row | not used yet | 2026-11-20, moved from Shubham's working copy (MD5-identical to the online files) |
| `Shubham/raw/minimum_working_copy_p3` | `~/local_data/Shubham_minimum_working_copy_p3/` (745 MB + 47 relative symlinks into `Balmorel_DTU/raw`) | Mac + server `/gpfs/scratch/le2p/local_data/Shubham_minimum_working_copy_p3` (MD5 verified 2026-11-21) | Shubham Nayak's working copy of the Balmorel inputs ("Paper 3", representative-weather experiments). `non_vre_time_series_data_1982_2020/cop_and_demand_csv/Bal_ready_csvs/classic_demand.csv` (link → `Balmorel_DTU/raw/electricity_demand/classic_demand.csv`): hourly electricity demand 1982–2021, 29 Balmorel regions (Nordic, Baltic, Western and Central Europe; no CH, Balkans, GR), no NaN; the four German regions DE4-E/N/S/W each hold the full German series (identical columns, do not sum); annual totals vary by < 0.7 % between years (checked 2026-11-20). Same folder: heat profiles and heat-pump COP (1982–2021). `hydro_csv/.../res_inflow.csv`, `ror_inflow.csv`: hourly 1980–2021, 25 areas. `clustering weather time series/{wind,wind_off,solar}/P.csv`: CorRES capacity factors per Balmorel region, hourly 1980–2021 | not used yet | received from Shubham (date not recorded). Public source: DTU Data collection doi:10.11583/DTU.c.7964141 ("Pan-European weather dependent generation and demand time series for Balmorel"); MD5 identical (2026-11-20) for `classic_demand.csv` (DTU.32881565), `res_inflow.csv` and `ror_inflow.csv` (DTU.32881376), wind `P.csv` = onshore `SP277_HH150_RGB.csv` (DTU.29618153), wind_off `P.csv` = `SP316_HH155_RGB.csv` (DTU.29617955), solar `P.csv` = `PV_Utility_scale_no_tracking_RGB.csv` (DTU.29617220); all 16 CSVs under `non_vre_time_series_data_1982_2020/` match the online MD5 except `cop_ground_water_profile.csv` (not online, Shubham's addition). Readmes of the 7 data items: now in `~/local_data/Balmorel_DTU/raw/<item>/readme.txt` (no units stated; generating code: github.com/nyk95/weather_to_balmorel) |

When a dataset is added, give it a row here (registry key, path, copies, producing code) and
register shared sources in `registry.toml`.
