"""Supply-demand overview (2025 capacities x capacity factors vs classic demand) and heat/COP figures.

Reads ~/local_data/Balmorel_DTU/raw and ~/local_data/Mopo/raw (read-only).
Writes 01_data_understanding/figures/{supply_demand,heat_cop}.png and tables/supply_demand_heat.json.
Assumptions (stated on the page): wind = 2020 existing-fleet capacity factors, capacities = Mopo 2025
country totals split equally over the country's Balmorel regions that have a series; PV = utility-scale
no-tracking RGB capacity factor (no existing-fleet PV series exists); run-of-river generation = inflow
(unit assumed MWh per hour); reservoir inflow is shown separately and is not generation.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAW: Path = Path.home() / "local_data" / "Balmorel_DTU" / "raw"
CAP: Path = Path.home() / "local_data" / "Mopo" / "raw" / "VRE_installed_capacities_2020_and_2025"
OUT: Path = Path(__file__).resolve().parents[3] / "01_data_understanding"
S, E = "1982-01-01", "2020-12-31 23:00"
mpl.rcParams.update({"figure.dpi": 150, "savefig.dpi": 220, "font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 7, "axes.spines.top": False, "axes.spines.right": False})
R: dict = {}


def rd(p: Path) -> pd.DataFrame:
    d = pd.read_csv(p)
    d = d.set_index(pd.to_datetime(d.iloc[:, 0])).drop(columns=d.columns[0])
    return d.loc[S:E].astype("float64")


dem = rd(RAW / "electricity_demand" / "classic_demand.csv") / 1e3  # GW (MW assumed)
REG = list(dem.columns)
country = {r: r for r in REG}
for r in REG:
    if r.startswith("DE4"):
        country[r] = "DE"
    elif r in ("DK1", "DK2"):
        country[r] = "DK"
    elif r[:2] in ("NO", "SE") and r[2:].isdigit():
        country[r] = r[:2]
    elif r == "FIN":
        country[r] = "FI"
UNIQ = [r for r in REG if r not in ("DE4-N", "DE4-S", "DE4-W")]
dem_tot = dem[UNIQ].sum(axis=1)


def capacity(f: str) -> pd.Series:
    x = pd.read_excel(CAP / f"capacity_{f}-existing.xlsx", sheet_name="Country_level")
    return x.set_index("Code")[2025].astype(float)


cap_on, cap_off, cap_pv = capacity("wind-on"), capacity("wind-off"), capacity("solar-PV")
won = rd(RAW / "wind_onshore" / "Existing.csv")
woff = rd(RAW / "wind_offshore" / "Existing.csv")
pv = rd(RAW / "solar_PV" / "PV_Utility_scale_no_tracking_RGB.csv")
res = rd(RAW / "hydro_inflow" / "res_inflow.csv") / 1e3
ror = rd(RAW / "hydro_inflow" / "ror_inflow.csv") / 1e3


def split(cap: pd.Series, cols_by_region: dict[str, list[str]]) -> dict[str, float]:
    """Split the 2025 country capacity (GW) equally over the available regions of the country."""
    out: dict[str, float] = {}
    by_c: dict[str, list[str]] = {}
    for r, c in cols_by_region.items():
        by_c.setdefault(c, []).append(r)
    for c, rs in by_c.items():
        for r in rs:
            out[r] = float(cap.get(c, 0.0)) / len(rs)
    return out


reg_on = {r: country[r] for r in REG if r in won.columns}
reg_pv = {r: country[r] for r in REG if r in pv.columns}
off_cols = [c for c in woff.columns if c.replace("_OFF2", "").replace("_OFF1", "").replace("_OFF", "") in REG]
off_c = {c: country[c.replace("_OFF2", "").replace("_OFF1", "").replace("_OFF", "")] for c in off_cols}
c_on, c_pv, c_off = split(cap_on, reg_on), split(cap_pv, reg_pv), split(cap_off, off_c)
R["cap_used_GW"] = dict(onshore=sum(c_on.values()), offshore=sum(c_off.values()), pv=sum(c_pv.values()))
R["cap_country_total_GW"] = {k: float(cap_on[[c for c in set(country.values()) if c in cap_on.index]].sum()) if k == "on" else 0 for k in ["on"]}
countries = set(country.values())
R["cap_offshore_countries_without_series_GW"] = {c: float(cap_off.get(c, 0)) for c in countries if cap_off.get(c, 0) > 0 and c not in set(off_c.values())}
R["onshore_no_series_regions"] = [r for r in REG if r not in won.columns]
gon = sum(won[r] * g for r, g in c_on.items())
goff = sum(woff[c] * g for c, g in c_off.items())
gpv = sum(pv[r].clip(lower=0) * g for r, g in c_pv.items())


def hname(h: str) -> str:
    for a, b in [("_A1", ""), ("_Other_DH", ""), ("_A", ""), ("FinA", "FIN"), ("SE1A", "SE1"), ("SE2A", "SE2"), ("SE3A", "SE3"), ("SE4A", "SE4")]:
        h = h.replace(a, b)
    return h


hcols = [c for c in ror.columns if hname(c) in REG and c not in ("DE4-N_A", "DE4-S_A", "DE4-W_A")]
g_ror = ror[hcols].sum(axis=1)
g_res_inflow = res[[c for c in res.columns if hname(c) in REG and c not in ("DE4-N_A", "DE4-S_A", "DE4-W_A")]].sum(axis=1)
vre = gon + goff + gpv
resid = dem_tot - vre - g_ror
ann = lambda s: s.mean() * 8766 / 1e3  # TWh
R["annual_TWh"] = dict(demand=ann(dem_tot), onshore=ann(gon), offshore=ann(goff), pv=ann(gpv), ror=ann(g_ror), res_inflow=ann(g_res_inflow), residual=ann(resid))
R["mean_CF_fleet"] = dict(onshore=float(gon.mean() / sum(c_on.values())), offshore=float(goff.mean() / sum(c_off.values())), pv=float(gpv.mean() / sum(c_pv.values())))
R["vre_share_of_demand_pct"] = 100 * ann(vre) / ann(dem_tot)
R["resid_stats_GW"] = dict(mean=float(resid.mean()), min=float(resid.min()), max=float(resid.max()), P99=float(resid.quantile(.99)),
                           max_time=str(resid.idxmax()), neg_hours_pct=float(100 * (resid < 0).mean()))
r7 = resid.rolling(24 * 7).mean()
R["resid_max_7d_GW"] = [float(r7.max()), str(r7.idxmax())]

# figure 1
fig = plt.figure(figsize=(7.4, 5.4))
ax = fig.add_subplot(2, 2, 1)
mon = lambda s: s.groupby(s.index.month).mean()
bot = np.zeros(12)
for s, lab, col in [(g_ror, "run-of-river (inflow)", "#5aa9c9"), (gon, "onshore wind", "#2c7fb8"), (goff, "offshore wind", "#08306b"), (gpv, "PV", "#f2b134")]:
    m = mon(s).values
    ax.bar(range(1, 13), m, bottom=bot, color=col, label=lab, width=0.8)
    bot += m
ax.plot(range(1, 13), mon(dem_tot).values, "k-o", ms=3, label="classic demand")
ax.plot(range(1, 13), mon(resid).values, color="C3", ls="--", label="residual load")
ax.set_xlabel("Month"); ax.set_ylabel("Mean power (GW)"); ax.set_xticks(range(1, 13)); ax.set_ylim(0, 540)
ax.legend(frameon=False, ncol=2, loc="upper center", borderaxespad=0.6, fontsize=6.5)
ax.text(0.98, 0.66, f"wind+PV = {R['vre_share_of_demand_pct']:.0f} % of demand\n(1982–2020 mean)", transform=ax.transAxes, ha="right", fontsize=6.5)
# panel b: two winter weeks around lowest 7-day wind
t0 = pd.Timestamp("1989-12-27")
sl = slice(t0, t0 + pd.Timedelta(days=14))
ax = fig.add_subplot(2, 2, 2)
x = dem_tot.loc[sl].index
ax.stackplot(x, g_ror.loc[sl], gon.loc[sl], goff.loc[sl], gpv.loc[sl], colors=["#5aa9c9", "#2c7fb8", "#08306b", "#f2b134"],
             labels=["run-of-river", "onshore wind", "offshore wind", "PV"])
ax.plot(x, dem_tot.loc[sl], "k-", lw=1, label="classic demand")
ax.set_ylabel("Power (GW)"); ax.set_xlabel("Date (GMT), 1989/90")
ax.xaxis.set_major_locator(mpl.dates.DayLocator(interval=4)); ax.xaxis.set_major_formatter(mpl.dates.DateFormatter("%d %b")); ax.set_ylim(0, 700)
ax.legend(frameon=False, ncol=3, loc="upper center", borderaxespad=0.6, fontsize=6.5)
ax.text(0.98, 0.68, f"mean wind+PV {vre.loc[sl].mean():.0f} GW\nmean demand {dem_tot.loc[sl].mean():.0f} GW", transform=ax.transAxes, ha="right", fontsize=6.5)
# panel c: residual load duration
ax = fig.add_subplot(2, 2, 3)
v = np.sort(resid.values)[::-1][::40]
ax.plot(np.linspace(0, 100, len(v)), v, color="C3", label="residual load, 39 years")
ax.plot(np.linspace(0, 100, len(v)), np.sort(dem_tot.values)[::-1][::40], color="k", label="classic demand")
ax.axhline(0, color="0.5", lw=0.6)
ax.set_xlabel("Share of hours exceeded (%)"); ax.set_ylabel("Power (GW)")
ax.legend(frameon=False, loc="upper right", borderaxespad=0.6)
ax.text(0.03, 0.05, f"residual: max {resid.max():.0f} GW, min {resid.min():.0f} GW\nnegative in {R['resid_stats_GW']['neg_hours_pct']:.1f} % of hours", transform=ax.transAxes, fontsize=6.5)
# panel d: annual energy balance
ax = fig.add_subplot(2, 2, 4)
names = ["demand", "onshore\nwind", "offshore\nwind", "PV", "run-of-\nriver", "reservoir\ninflow*"]
vals = [ann(dem_tot), ann(gon), ann(goff), ann(gpv), ann(g_ror), ann(g_res_inflow)]
ax.bar(range(6), vals, color=["k", "#2c7fb8", "#08306b", "#f2b134", "#5aa9c9", "#cfe3ee"])
for i, vv in enumerate(vals):
    ax.text(i, vv + 20, f"{vv:.0f}", ha="center", fontsize=6.5)
ax.set_xticks(range(6)); ax.set_xticklabels(names, fontsize=6.5); ax.set_ylabel("Annual energy (TWh)"); ax.set_ylim(0, 3000)
ax.text(0.98, 0.95, "* inflow, not generation", transform=ax.transAxes, ha="right", fontsize=6.5)
fig.tight_layout()
fig.savefig(OUT / "figures" / "supply_demand.png", dpi=220, bbox_inches="tight"); plt.close(fig)

# heat and COP
hs = rd(RAW / "heat_demand" / "heat_profile_indiv_user_residential.csv")
cw = rd(RAW / "heat_pump_COP" / "cop_air_water_profile.csv")
ca = rd(RAW / "heat_pump_COP" / "cop_air_air_profile.csv")
R["heat_cols"], R["cop_cols"] = hs.shape[1], cw.shape[1]
share = (hs.groupby(hs.index.month).sum() / hs.sum()).T * 100  # % of annual per month per region
R["heat_month_share_median_pct"] = [float(x) for x in share.median()]
R["heat_DJF_over_JJA_median"] = float((hs[hs.index.month.isin([12, 1, 2])].mean() / hs[hs.index.month.isin([6, 7, 8])].mean()).median())
R["heat_zero_hours_pct_median"] = float((100 * (hs <= 0).mean()).median())
R["heat_JJA_share_pct_median"] = float(share[[6, 7, 8]].sum(axis=1).median())
dd = hs.resample("D").mean()
R["heat_daily_zero_share_pct_median"] = float((100 * (dd <= 1e-9).mean()).median())
cw_m = cw.groupby(cw.index.month).mean(); ca_m = ca.groupby(ca.index.month).mean()
R["cop_airwater_month_median"] = [float(x) for x in cw_m.median(axis=1)]
R["cop_airair_month_median"] = [float(x) for x in ca_m.median(axis=1)]
R["cop_airwater_range"] = [float(cw.min().min()), float(cw.max().max())]
R["cop_airair_range"] = [float(ca.min().min()), float(ca.max().max())]
common = [c for c in hs.columns if c.split("_")[0] in cw.columns.str.split("_").str[0].tolist()]
# heat-pump electricity shape: heat / COP (air-water, matched by country prefix where available)
cw_c = {c.split("_")[0]: c for c in cw.columns}
elec_share, heat_share_m = [], []
for c in hs.columns:
    k = c.split("_")[0]
    if k in cw_c:
        h = hs[c]; e = h / cw[cw_c[k]]
        elec_share.append((e.groupby(e.index.month).sum() / e.sum()).values * 100)
        heat_share_m.append((h.groupby(h.index.month).sum() / h.sum()).values * 100)
elec_share, heat_share_m = np.array(elec_share), np.array(heat_share_m)
R["n_matched_heat_cop"] = int(len(elec_share))
R["heat_share_month_matched_pct"] = [float(x) for x in np.median(heat_share_m, axis=0)]
R["hp_elec_share_month_pct"] = [float(x) for x in np.median(elec_share, axis=0)]
R["hp_elec_peak_over_heat_peak"] = float(np.median(elec_share.max(axis=1) / heat_share_m.max(axis=1)))

fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.7))
ax = axs[0]
ax.fill_between(range(1, 13), share.quantile(.1), share.quantile(.9), color="0.85", label="10–90 % of regions")
ax.plot(range(1, 13), share.median(), "C0-o", ms=3, label="median region")
ax.axhline(100 / 12, color="0.4", lw=0.6, ls=":", label="uniform (8.3 %)")
ax.set_xlabel("Month"); ax.set_ylabel("Share of annual space heat (%)"); ax.set_xticks([1, 3, 5, 7, 9, 11]); ax.set_ylim(0, 20)
ax.legend(frameon=False, loc="upper center", borderaxespad=0.6, fontsize=6.5)
ax = axs[1]
ax.fill_between(range(1, 13), cw_m.quantile(.1, axis=1), cw_m.quantile(.9, axis=1), color="0.85", label="10–90 % of areas (air-water)")
ax.plot(range(1, 13), cw_m.median(axis=1), "C0-o", ms=3, label="air-to-water, median")
ax.plot(range(1, 13), ca_m.median(axis=1), "C1-o", ms=3, label="air-to-air, median")
ax.set_xlabel("Month"); ax.set_ylabel("COP, monthly mean (–)"); ax.set_xticks([1, 3, 5, 7, 9, 11]); ax.set_ylim(0, 6.5)
ax.legend(frameon=False, loc="upper center", borderaxespad=0.6, fontsize=6.5)
ax = axs[2]
ax.plot(range(1, 13), np.median(heat_share_m, axis=0), "C0-o", ms=3, label="heat demand")
ax.plot(range(1, 13), np.median(elec_share, axis=0), "C3-o", ms=3, label="heat-pump electricity = heat ÷ COP")
ax.set_xlabel("Month"); ax.set_ylabel("Share of annual total (%)"); ax.set_xticks([1, 3, 5, 7, 9, 11]); ax.set_ylim(0, 20)
ax.legend(frameon=False, loc="upper center", borderaxespad=0.6, fontsize=6.5)
ax.text(0.98, 0.30, f"Jan share {np.median(heat_share_m,0)[0]:.1f} → {np.median(elec_share,0)[0]:.1f} %\nn = {len(elec_share)} areas", transform=ax.transAxes, ha="right", fontsize=6.5)
fig.tight_layout()
fig.savefig(OUT / "figures" / "heat_cop.png", dpi=220, bbox_inches="tight"); plt.close(fig)
(OUT / "tables" / "supply_demand_heat.json").write_text(json.dumps(R, indent=1, default=str))
print(json.dumps({k: R[k] for k in R if k not in ("cap_country_total_GW",)}, indent=0, default=str)[:3500])
