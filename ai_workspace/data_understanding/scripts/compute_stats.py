"""Compute statistics and figures for 01_data_understanding (Balmorel_DTU data).

Reads ~/local_data/Balmorel_DTU/raw (read-only). Writes tables to 01_data_understanding/tables,
figures to 01_data_understanding/figures and results.json (numbers used by build_html.py).
Study window: 1982-01-01 00:00 to 2020-12-31 23:00 GMT (weather years 1982-2020, plan D16).
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAW: Path = Path.home() / "local_data" / "Balmorel_DTU" / "raw"
OUT: Path = Path(__file__).resolve().parents[3] / "01_data_understanding"
FIG: Path = OUT / "figures"
TAB: Path = OUT / "tables"
FIG.mkdir(exist_ok=True)
TAB.mkdir(exist_ok=True)
START, END = pd.Timestamp("1982-01-01 00:00", tz="UTC"), pd.Timestamp("2020-12-31 23:00", tz="UTC")
FORCE: bool = True

mpl.rcParams.update({"figure.dpi": 150, "savefig.dpi": 220, "font.size": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5,
                     "axes.titlesize": 8, "axes.spines.top": False, "axes.spines.right": False})
R: dict = {}


def read_ts(path: Path, first_col_time: bool = True) -> pd.DataFrame:
    """Read a CSV with a time column as first column; return UTC-aware, float32, window-sliced frame."""
    df = pd.read_csv(path)
    df = df.set_index(pd.to_datetime(df.iloc[:, 0])).drop(columns=df.columns[0]).astype("float32")
    df.index = df.index.tz_localize("UTC")
    df.index.name = "DateTime"
    return df


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG / f"{name}.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def note(ax: plt.Axes, text: str, loc: str = "ul") -> None:
    x, y, ha, va = {"ul": (0.02, 0.97, "left", "top"), "ur": (0.98, 0.97, "right", "top"),
                    "ll": (0.02, 0.03, "left", "bottom"), "lr": (0.98, 0.03, "right", "bottom")}[loc]
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=7)


# demand
dem_full = read_ts(RAW / "electricity_demand" / "classic_demand.csv")
R["demand_file_span"] = [str(dem_full.index[0]), str(dem_full.index[-1]), len(dem_full)]
dem = dem_full.loc[START:END]
REG = list(dem.columns)
DUP = ["DE4-N", "DE4-S", "DE4-W"]
UNIQ = [c for c in REG if c not in DUP]
R["n_regions_demand"], R["n_unique_demand"] = len(REG), len(UNIQ)
R["demand_nan"] = int(dem_full.isna().sum().sum())
R["demand_nonpositive"] = int((dem_full <= 0).sum().sum())
R["demand_hourly_continuous"] = bool((dem_full.index.to_series().diff().dropna() == pd.Timedelta("1h")).all())
R["de4_identical"] = bool(all(np.allclose(dem["DE4-E"], dem[c]) for c in DUP))
tot = dem[UNIQ].sum(axis=1)
hrs_per_year = 8766.0
rows = []
for c in UNIQ:
    s = dem[c]
    ann = s.groupby(s.index.year).mean() * hrs_per_year / 1e6
    rows.append(dict(region=c if c != "DE4-E" else "DE4 (one of four identical columns)",
                     mean_GW=s.mean() / 1e3, P1_GW=s.quantile(.01) / 1e3, P99_GW=s.quantile(.99) / 1e3,
                     max_GW=s.max() / 1e3, max_time=str(s.idxmax())[:13], min_GW=s.min() / 1e3,
                     min_time=str(s.idxmin())[:13],
                     annual_TWh=ann.mean(), annual_CV_pct=100 * ann.std() / ann.mean(),
                     annual_min_year=int(ann.idxmin()), annual_max_year=int(ann.idxmax()),
                     DJF_over_JJA=s[s.index.month.isin([12, 1, 2])].mean() / s[s.index.month.isin([6, 7, 8])].mean(),
                     peak_over_mean=s.max() / s.mean()))
dtab = pd.DataFrame(rows)
dtab.to_csv(TAB / "demand_by_region_1982-2020.csv", index=False, float_format="%.4g")
ann_tot = tot.groupby(tot.index.year).mean() * hrs_per_year / 1e6
R["dem_tot_mean_GW"] = tot.mean() / 1e3
R["dem_tot_annual_TWh"] = ann_tot.mean()
R["dem_tot_annual_CV_pct"] = 100 * ann_tot.std() / ann_tot.mean()
R["dem_tot_annual_range_TWh"] = [ann_tot.min(), ann_tot.max(), int(ann_tot.idxmin()), int(ann_tot.idxmax())]
R["dem_tot_max_GW"] = [tot.max() / 1e3, str(tot.idxmax())]
R["dem_tot_min_GW"] = [tot.min() / 1e3, str(tot.idxmin())]
R["dem_tot_P1_P99_GW"] = [tot.quantile(.01) / 1e3, tot.quantile(.99) / 1e3]
cv_regions = dtab["annual_CV_pct"]
R["dem_region_annual_CV_range_pct"] = [cv_regions.min(), cv_regions.max(), float(cv_regions.median())]
de_ann = dem["DE4-E"].groupby(dem.index.year).mean() * hrs_per_year / 1e6
R["de_annual_TWh"] = [de_ann.mean(), de_ann.min(), de_ann.max()]
# linear trend of annual total (TWh per year) and share of mean
x = ann_tot.index.values.astype(float)
sl = np.polyfit(x, ann_tot.values, 1)[0]
R["dem_tot_trend_TWh_per_year"], R["dem_tot_trend_pct_per_decade"] = sl, 100 * sl * 10 / ann_tot.mean()
# top demand hours / days
top_hours = tot.nlargest(200)
topdays = tot.resample("D").mean().nlargest(5)
R["dem_top_days"] = [(str(i.date()), v / 1e3) for i, v in topdays.items()]
R["dem_peak_month_counts"] = {int(k): int(v) for k, v in tot.resample("D").mean().nlargest(100).index.month.value_counts().sort_index().items()}

# demand figures
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.6))
mon = tot.groupby([tot.index.year, tot.index.month]).mean().unstack() / 1e3
ax = axs[0]
ax.fill_between(range(1, 13), mon.min(), mon.max(), color="0.85", label="min–max over 39 years")
ax.plot(range(1, 13), mon.mean(), color="C0", label="mean")
ax.set_xlabel("Month"); ax.set_ylabel("Total demand (GW)"); ax.set_xticks([1, 3, 5, 7, 9, 11])
ax.legend(frameon=False, loc="lower center", borderaxespad=0.6)
note(ax, f"annual mean {R['dem_tot_mean_GW']:.0f} GW\nDJF/JJA {tot[tot.index.month.isin([12,1,2])].mean()/tot[tot.index.month.isin([6,7,8])].mean():.2f}", "ur")
ax = axs[1]
yrs = ann_tot.index
ax.plot(yrs, ann_tot / ann_tot.mean(), color="k", label="26 regions total")
for c, col in [("DE4-E", "C1"), ("FR", "C2"), ("NO2", "C3"), ("UK", "C4")]:
    a = dem[c].groupby(dem.index.year).mean()
    ax.plot(yrs, a / a.mean(), color=col, lw=0.8, label=("DE4" if c == "DE4-E" else c))
ax.set_xlabel("Year"); ax.set_ylabel("Annual demand / 1982–2020 mean (–)")
ax.legend(frameon=False, ncol=2, loc="lower left", borderaxespad=0.6, columnspacing=0.8, handlelength=1.2)
note(ax, f"total: CV {R['dem_tot_annual_CV_pct']:.2f} %\nregions: CV {cv_regions.min():.2f}–{cv_regions.max():.2f} %", "ur")
ax.set_ylim(0.97, 1.05)
ax = axs[2]
for months, col, lab in [([12, 1, 2], "C0", "DJF"), ([6, 7, 8], "C3", "JJA")]:
    s = tot[tot.index.month.isin(months)]
    h = s.groupby(s.index.hour).mean() / 1e3
    ax.plot(h.index, h, color=col, label=lab)
ax.set_xlabel("Hour of day (GMT)"); ax.set_ylabel("Total demand (GW)")
ax.legend(frameon=False, loc="lower right", borderaxespad=0.6)
fig.tight_layout()
save(fig, "demand_overview")

# ECDF + extremes demand
fig, axs = plt.subplots(1, 2, figsize=(7.4, 2.6))
ax = axs[0]
for months, col, lab in [([12, 1, 2], "C0", "DJF"), ([6, 7, 8], "C3", "JJA"), (list(range(1, 13)), "k", "all months")]:
    s = np.sort((tot[tot.index.month.isin(months)] / tot.mean()).values)[::50]
    ax.plot(s, np.linspace(0, 1, len(s)), color=col, label=lab)
ax.set_xlabel("Total demand / annual mean (–)"); ax.set_ylabel("Cumulative probability (–)")
ax.legend(frameon=False, loc="lower right", borderaxespad=0.6)
note(ax, f"max/mean {tot.max()/tot.mean():.2f}\nmin/mean {tot.min()/tot.mean():.2f}", "ul")
ax = axs[1]
winter = tot.copy()
season = np.where(winter.index.month >= 7, winter.index.year, winter.index.year - 1)
peak = (winter.groupby(season).max() / 1e3).loc[1982:2019]
pk_time = winter.groupby(season).idxmax().loc[1982:2019]
ax.plot(peak.index, peak.values, "o", ms=3, color="C0", label="highest hourly total demand per season (1 Jul – 30 Jun)")
ax.set_xlabel("Season start year"); ax.set_ylabel("Peak total demand (GW)")
ax.set_ylim(peak.min() - 0.15, peak.max() + 0.75)
ax.legend(frameon=False, loc="upper center", borderaxespad=0.6, fontsize=6.5)
note(ax, f"range {peak.min():.2f}–{peak.max():.2f} GW (spread {100*(peak.max()-peak.min())/peak.mean():.2f} %)\nall peaks on {pk_time.dt.day.min()}–{pk_time.dt.day.max()} Dec at {int(pk_time.dt.hour.min())}:00–{int(pk_time.dt.hour.max())}:00 GMT", "lr")
R["dem_peak_dates"] = dict(day_min=int(pk_time.dt.day.min()), day_max=int(pk_time.dt.day.max()), month_set=sorted(set(int(m) for m in pk_time.dt.month)), hour_set=sorted(set(int(h) for h in pk_time.dt.hour)), weekday_set=sorted(set(int(w) for w in pk_time.dt.weekday)))
top3 = peak.nlargest(3)
fig.tight_layout()
save(fig, "demand_distribution_extremes")
R["dem_peak_by_season_top3"] = [(int(k), float(v)) for k, v in top3.items()]
R["dem_peak_season_range_GW"] = [float(peak.min()), float(peak.max())]
R["dem_peak_season_n"] = int(len(peak))
R["dem_high7_distinct_values"] = sorted(set(round(float(v), 1) for v in (tot.resample("D").mean().rolling(7).mean()[tot.resample("D").mean().rolling(7).mean().index.month.isin([11,12,1,2,3])].groupby(np.where(tot.resample("D").mean().rolling(7).mean()[tot.resample("D").mean().rolling(7).mean().index.month.isin([11,12,1,2,3])].index.month >= 7, tot.resample("D").mean().rolling(7).mean()[tot.resample("D").mean().rolling(7).mean().index.month.isin([11,12,1,2,3])].index.year, tot.resample("D").mean().rolling(7).mean()[tot.resample("D").mean().rolling(7).mean().index.month.isin([11,12,1,2,3])].index.year - 1)).max().loc[1982:2019] / 1e3)))

# VRE files
VRE_FILES = {
    "onshore SP277_HH150 RGA": "wind_onshore/SP277_HH150_RGA.csv",
    "onshore SP277_HH150 RGB": "wind_onshore/SP277_HH150_RGB.csv",
    "onshore SP277_HH150 RGC": "wind_onshore/SP277_HH150_RGC.csv",
    "onshore existing 2020 fleet": "wind_onshore/Existing.csv",
    "offshore SP316_HH155 RGB (bottom-fixed)": "wind_offshore/Future_bottom_fixed/SP316_HH155_RGB.csv",
    "offshore existing 2020 fleet": "wind_offshore/Existing.csv",
    "PV utility no tracking RGA": "solar_PV/PV_Utility_scale_no_tracking_RGA.csv",
    "PV utility no tracking RGB": "solar_PV/PV_Utility_scale_no_tracking_RGB.csv",
    "PV utility no tracking RGC": "solar_PV/PV_Utility_scale_no_tracking_RGC.csv",
    "PV utility tracking RGB": "solar_PV/PV_Utility_scale_tracking_RGB.csv",
    "PV rooftop RGB": "solar_PV/PV_Rooftop_RGB.csv",
}
V: dict[str, pd.DataFrame] = {}
inv = []
for name, rel in VRE_FILES.items():
    full = read_ts(RAW / rel)
    sub = full.loc[START:END]
    V[name] = sub
    inv.append(dict(series=name, file=rel, n_regions=full.shape[1], first=str(full.index[0])[:16], last=str(full.index[-1])[:16],
                    rows=len(full), nan=int(full.isna().sum().sum()), below0=int((full < 0).sum().sum()),
                    min=float(full.min().min()), above1=int((full > 1).sum().sum()), max=float(full.max().max()),
                    mean_CF_window=float(sub.mean().mean()),
                    mean_CF_common29=float(sub[[c for c in REG if c in sub.columns]].mean().mean()) if not name.startswith("offshore") else np.nan))
itab = pd.DataFrame(inv)
itab.to_csv(TAB / "vre_files_inventory.csv", index=False, float_format="%.4g")
R["vre_inventory"] = itab.round(4).to_dict(orient="records")
R["vre_neg_max"] = float(itab["min"].min())

MAIN = {"wind": "onshore SP277_HH150 RGB", "offshore": "offshore SP316_HH155 RGB (bottom-fixed)", "pv": "PV utility no tracking RGB"}
cov_regions = {k: list(V[v].columns) for k, v in MAIN.items()}
R["cov"] = {k: len(v) for k, v in cov_regions.items()}
COMMON = [c for c in REG if c in V[MAIN["wind"]].columns and c in V[MAIN["pv"]].columns]
R["common_regions"] = len(COMMON)


def cf_stats(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    rows = []
    for c in cols:
        s = df[c].astype("float64")
        ann = s.groupby(s.index.year).mean()
        rows.append(dict(region=c, mean=s.mean(), std=s.std(), P5=s.quantile(.05), P50=s.median(), P95=s.quantile(.95), max=s.max(),
                         share_below_0p01=(s < 0.01).mean(), DJF=s[s.index.month.isin([12, 1, 2])].mean(),
                         JJA=s[s.index.month.isin([6, 7, 8])].mean(), annual_mean_min=ann.min(), annual_mean_max=ann.max(),
                         annual_CV_pct=100 * ann.std() / ann.mean()))
    return pd.DataFrame(rows)


for k, cols in [("wind", COMMON), ("pv", COMMON), ("offshore", cov_regions["offshore"])]:
    t = cf_stats(V[MAIN[k]], cols)
    t.to_csv(TAB / f"cf_{k}_by_region_1982-2020.csv", index=False, float_format="%.4g")
    R[f"cf_{k}_summary"] = dict(mean_of_region_means=float(t["mean"].mean()), min_region=[t.loc[t["mean"].idxmin(), "region"], float(t["mean"].min())],
                                max_region=[t.loc[t["mean"].idxmax(), "region"], float(t["mean"].max())],
                                CV_annual_median=float(t["annual_CV_pct"].median()), CV_annual_range=[float(t["annual_CV_pct"].min()), float(t["annual_CV_pct"].max())],
                                DJF_over_JJA=float(t["DJF"].mean() / t["JJA"].mean()), zero_share_mean=float(t["share_below_0p01"].mean()))

# Europe mean series (unweighted mean over the common 29 regions; onshore and PV) and offshore (all)
E = {"onshore wind": V[MAIN["wind"]][COMMON].mean(axis=1), "PV": V[MAIN["pv"]][COMMON].mean(axis=1), "offshore wind": V[MAIN["offshore"]].mean(axis=1)}
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.6))
ax = axs[0]
for (lab, s), col in zip(E.items(), ["C0", "C1", "C2"]):
    m = s.groupby([s.index.year, s.index.month]).mean().unstack()
    ax.plot(range(1, 13), m.mean(), color=col, label=lab)
    if lab == "onshore wind":
        ax.fill_between(range(1, 13), m.min(), m.max(), color=col, alpha=0.15, label="onshore wind, min–max over 39 years")
ax.set_xlabel("Month"); ax.set_ylabel("Capacity factor, region mean (–)"); ax.set_xticks([1, 3, 5, 7, 9, 11])
ax.legend(frameon=False, loc="upper center", borderaxespad=0.6, ncol=1, fontsize=6.5)
ax.set_ylim(0, 1.05)
ax = axs[1]
for (lab, s), col in zip(E.items(), ["C0", "C1", "C2"]):
    a = s.groupby(s.index.year).mean()
    ax.plot(a.index, 100 * (a / a.mean() - 1), color=col, label=lab)
    R[f"E_annual_CV_{lab}"] = float(100 * a.std() / a.mean())
    R[f"E_annual_range_{lab}"] = [float(100 * (a.min() / a.mean() - 1)), float(100 * (a.max() / a.mean() - 1)), int(a.idxmin()), int(a.idxmax())]
ax.axhline(0, color="0.5", lw=0.6)
ax.set_xlabel("Year"); ax.set_ylabel("Annual mean CF anomaly (%)")
ax.legend(frameon=False, loc="upper left", borderaxespad=0.6, fontsize=6.5)
note(ax, "CV: " + ", ".join(f"{R['E_annual_CV_'+l]:.1f}%" for l in E), "lr")
ax.set_ylim(-14, 24)
ax = axs[2]
for lab, s, col in [("onshore wind", E["onshore wind"], "C0"), ("PV", E["PV"], "C1")]:
    v = np.sort(s.values)[::40]
    ax.plot(v, np.linspace(0, 1, len(v)), color=col, label=lab)
ax.set_xlabel("Hourly CF, region mean (–)"); ax.set_ylabel("Cumulative probability (–)")
ax.legend(frameon=False, loc="lower right", borderaxespad=0.6)
fig.tight_layout()
save(fig, "vre_overview")

# VRE regional distributions
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.6))
ax = axs[0]
for c, col in [("DK1", "C0"), ("ES", "C1"), ("FR", "C2"), ("DE4-N", "C3"), ("NO2", "C4")]:
    s = V[MAIN["wind"]][c]
    h, b = np.histogram(s, bins=40, range=(0, 1), density=True)
    ax.plot(0.5 * (b[1:] + b[:-1]), h, color=col, label=c)
ax.set_xlabel("Onshore wind CF, hourly (–)"); ax.set_ylabel("Probability density (–)")
ax.legend(frameon=False, loc="upper center", borderaxespad=0.6, ncol=1)
ax = axs[1]
for c, col in [("DK1", "C0"), ("ES", "C1"), ("FR", "C2"), ("DE4-N", "C3"), ("NO2", "C4")]:
    s = V[MAIN["pv"]][c]
    v = np.sort(s.values)[::40]
    ax.plot(v, np.linspace(0, 1, len(v)), color=col, label=c)
ax.set_xlabel("PV CF, hourly (–)"); ax.set_ylabel("Cumulative probability (–)")
ax.legend(frameon=False, loc="lower right", borderaxespad=0.6)
ax.text(0.12, 0.42, "hours with CF < 0.01:\n" + "\n".join(f"{c}: {100*(V[MAIN['pv']][c]<0.01).mean():.0f} %" for c in ["DK1", "ES"]), fontsize=7, va="top")
ax = axs[2]
labs = ["RGA", "RGB", "RGC"]
w = [V[f"onshore SP277_HH150 {g}"][COMMON].mean().mean() for g in labs]
p = [V[f"PV utility no tracking {g}"][COMMON].mean().mean() for g in labs]
xx = np.arange(3)
ax.bar(xx - 0.2, w, 0.4, color="C0", label="onshore wind SP277_HH150")
ax.bar(xx + 0.2, p, 0.4, color="C1", label="PV utility, no tracking")
for xi, a, b in zip(xx, w, p):
    ax.text(xi - 0.2, a, f"{a:.3f}", ha="center", va="bottom", fontsize=6.5); ax.text(xi + 0.2, b, f"{b:.3f}", ha="center", va="bottom", fontsize=6.5)
ax.set_xticks(xx); ax.set_xticklabels(labs); ax.set_xlabel("Resource grade"); ax.set_ylabel("Mean CF, 29 regions (–)")
ax.set_ylim(0, 0.62); ax.legend(frameon=False, loc="upper right", borderaxespad=0.6, fontsize=6.5)
fig.tight_layout()
save(fig, "vre_distribution_resource_grade")
R["rg_means_wind"], R["rg_means_pv"] = [float(x) for x in w], [float(x) for x in p]

# spatial correlation of daily-mean wind CF
dwind = V[MAIN["wind"]][COMMON].resample("D").mean()
cm = dwind.corr()
fig, ax = plt.subplots(figsize=(4.6, 4.0))
im = ax.imshow(cm.values, vmin=-0.2, vmax=1, cmap="viridis")
ax.set_xticks(range(len(COMMON))); ax.set_xticklabels(COMMON, rotation=90, fontsize=6)
ax.set_yticks(range(len(COMMON))); ax.set_yticklabels(COMMON, fontsize=6)
cb = fig.colorbar(im, ax=ax, shrink=0.8); cb.set_label("Correlation of daily-mean onshore wind CF (–)", fontsize=7)
ax.set_xlabel("Region"); ax.set_ylabel("Region")
off = cm.values[np.triu_indices(len(COMMON), 1)]
note(ax, "", "ul")
fig.tight_layout()
save(fig, "wind_spatial_correlation")
R["wind_corr_pairs"] = dict(mean=float(off.mean()), P10=float(np.quantile(off, .1)), P90=float(np.quantile(off, .9)), min=float(off.min()))
dwint = dwind[dwind.index.month.isin([12, 1, 2])]
cw = dwint.corr().values[np.triu_indices(len(COMMON), 1)]
R["wind_corr_pairs_DJF_mean"] = float(cw.mean())
# demand-wind-PV correlation in winter (daily, Europe aggregates)
dd = tot.resample("D").mean()
dw = E["onshore wind"].resample("D").mean(); dp = E["PV"].resample("D").mean()
for lab, months in [("DJF", [12, 1, 2]), ("all", list(range(1, 13)))]:
    m = dd.index.month.isin(months)
    R[f"corr_dem_wind_{lab}"] = float(np.corrcoef(dd[m], dw[m])[0, 1])
    R[f"corr_dem_pv_{lab}"] = float(np.corrcoef(dd[m], dp[m])[0, 1])
# anomalies (deseasonalized) correlation DJF
def anom(s):
    doy = s.index.dayofyear
    return s - s.groupby(doy).transform("mean")
m = dd.index.month.isin([12, 1, 2])
R["corr_dem_wind_DJF_anom"] = float(np.corrcoef(anom(dd)[m], anom(dw)[m])[0, 1])

# low-wind extremes, Europe mean onshore wind
dws = E["onshore wind"].resample("D").mean()
r7 = dws.rolling(7).mean()
wmask = r7.index.month.isin([11, 12, 1, 2, 3])
low7 = r7[wmask]
lowest = low7.nsmallest(1)
R["wind_lowest_day"] = [float(dws.min()), str(dws.idxmin().date())]
R["wind_lowest_7d_winter"] = [float(lowest.iloc[0]), str(lowest.index[0].date())]
p10 = dws.quantile(.10)
below = (dws < p10).astype(int)
runs = below.groupby((below != below.shift()).cumsum()).agg(["sum", lambda x: x.index[0]])
runs.columns = ["len", "start"]
lr = runs[below.groupby((below != below.shift()).cumsum()).first() == 1].sort_values("len", ascending=False).head(5)
R["wind_longest_below_P10_days"] = [(int(r.len), str(r.start.date())) for r in lr.itertuples()]
R["wind_P10_daily_CF"] = float(p10)
season_s = np.where(r7.index.month >= 7, r7.index.year, r7.index.year - 1)
low_by_season = r7[wmask].groupby(season_s[wmask]).min().loc[1982:2019]
dem7 = dd.rolling(7).mean()
high_by_season = (dem7[wmask].groupby(season_s[wmask]).max() / 1e3).loc[1982:2019]
# winter compound: lowest 7-day wind and 7-day demand in same week
fig, axs = plt.subplots(1, 2, figsize=(7.4, 2.7))
ax = axs[0]
ax.bar(low_by_season.index, low_by_season.values, color="C0", label="lowest 7-day mean per winter")
top = low_by_season.nsmallest(3)
ax.bar(top.index, top.values, color="C3", label="three lowest winters")
ax.set_xlabel("Winter start year (Nov–Mar)"); ax.set_ylabel("Onshore wind CF, region mean (–)")
ax.legend(frameon=False, loc="upper left", borderaxespad=0.6, fontsize=6.5)
ax.set_ylim(0, low_by_season.max() * 1.8)
note(ax, f"mean {low_by_season.mean():.3f}\nlowest {low_by_season.min():.3f}\n({int(low_by_season.idxmin())}/{str(int(low_by_season.idxmin())+1)[2:]})", "ur")
ax = axs[1]
ax.scatter(high_by_season.values, low_by_season.reindex(high_by_season.index).values, s=10, color="C0", label="winter (one point per winter)")
for yv in set(top.index) | set(high_by_season.nlargest(3).index):
    ax.annotate(f"{yv}/{str(yv+1)[2:]}", (high_by_season[yv], low_by_season[yv]), xytext=(4, -3), textcoords="offset points", fontsize=6.5)
ax.set_xlabel("Highest 7-day mean total demand (GW)"); ax.set_ylabel("Lowest 7-day mean wind CF (–)")
r_season = float(np.corrcoef(high_by_season.values, low_by_season.reindex(high_by_season.index).values)[0, 1])
note(ax, f"r = {r_season:.2f}  (n = {len(high_by_season)})", "lr")
ax.legend(frameon=False, loc="upper right", borderaxespad=0.6, fontsize=6.5)
ax.set_xlim(high_by_season.min() - 0.8, high_by_season.max() + 1.6)
fig.tight_layout()
save(fig, "winter_extremes_wind_demand")
R["season_corr_lowwind_highdemand"] = r_season
R["wind_low7_top3"] = [(int(k), float(v)) for k, v in top.items()]
R["dem_high7_top3"] = [(int(k), float(v)) for k, v in high_by_season.nlargest(3).items()]
R["season_sample"] = int(len(high_by_season))


# demand: calendar versus weather structure (daily mean of 26 regions)
dayd = tot.resample("D").mean() / 1e3
dfd = pd.DataFrame({"y": dayd, "doy": dayd.index.dayofyear, "wd": dayd.index.weekday})
res1 = dfd["y"] - dfd.groupby("doy")["y"].transform("mean")
Xd = pd.get_dummies(dfd["wd"]).astype(float)
bet = np.linalg.lstsq(Xd.values, res1.values, rcond=None)[0]
res2 = res1 - Xd.values @ bet
R["dem_daily_std_GW"], R["dem_daily_mean_GW"] = float(dayd.std()), float(dayd.mean())
R["dem_resid_doy_std_GW"], R["dem_resid_doy_wd_std_GW"] = float(res1.std()), float(res2.std())
R["dem_weekday_effect_GW"] = [float(b) for b in bet]
R["dem_explained_by_calendar_pct"] = float(100 * (1 - res2.var() / dayd.var()))
rr = []
for c in UNIQ:
    sd = dem[c].resample("D").mean(); r1 = sd - sd.groupby(sd.index.dayofyear).transform("mean")
    Xc = pd.get_dummies(sd.index.weekday).astype(float).values
    b2 = np.linalg.lstsq(Xc, r1.values, rcond=None)[0]
    rr.append(100 * (r1 - Xc @ b2).std() / sd.mean())
R["dem_resid_region_pct_range"] = [float(min(rr)), float(max(rr)), float(np.median(rr))]
rw = []
for lab, ser in E.items():
    sd = ser.resample("D").mean(); r1 = sd - sd.groupby(sd.index.dayofyear).transform("mean")
    rw.append((lab, float(100 * r1.std() / sd.mean())))
R["vre_daily_anom_std_pct"] = rw

# winter low-wind runs
dws_w = dws[dws.index.month.isin([11, 12, 1, 2, 3])]
p10w = dws_w.quantile(.10)
bw = (dws < p10w).astype(int)
grp = (bw != bw.shift()).cumsum()
runs_w = bw.groupby(grp).agg(["sum"]).rename(columns={"sum": "len"})
runs_w["start"] = [bw[grp == g].index[0] for g in runs_w.index]
runs_w["val"] = bw.groupby(grp).first().values
runs_w = runs_w[(runs_w["val"] == 1) & runs_w["start"].map(lambda t: t.month in [11, 12, 1, 2, 3])].sort_values("len", ascending=False).head(6)
R["wind_winter_P10_daily_CF"] = float(p10w)
R["wind_winter_longest_runs"] = [(int(r.len), str(r.start.date())) for r in runs_w.itertuples()]

# hydro
H = {k: read_ts(RAW / "hydro_inflow" / f"{k}_inflow.csv") for k in ["res", "ror"]}
H = {k: v.loc[START:END] for k, v in H.items()}
DUPH = ["DE4-N_A", "DE4-S_A", "DE4-W_A"]
HU = {k: [c for c in H[k].columns if c not in DUPH] for k in H}
R["hydro_areas"] = {k: H[k].shape[1] for k in H}
R["hydro_unique"] = {k: len(HU[k]) for k in H}
R["hydro_cols_only_res"] = sorted(set(H["res"].columns) - set(H["ror"].columns))
R["hydro_cols_only_ror"] = sorted(set(H["ror"].columns) - set(H["res"].columns))
hrows = []
for k in ["res", "ror"]:
    for c in HU[k]:
        s = H[k][c].astype("float64")
        ann = s.groupby(s.index.year).mean() * hrs_per_year / 1e6
        mm = s.groupby(s.index.month).mean()
        hrows.append(dict(area=c, type=k, mean_per_hour=s.mean(), annual_sum_1e6=ann.mean(), annual_CV_pct=100 * ann.std() / ann.mean() if ann.mean() > 0 else np.nan,
                          annual_min_year=int(ann.idxmin()), annual_max_year=int(ann.idxmax()), peak_month=int(mm.idxmax()), trough_month=int(mm.idxmin()),
                          max_hourly=s.max(), zero_share=(s == 0).mean()))
htab = pd.DataFrame(hrows)
htab.to_csv(TAB / "hydro_inflow_by_area_1982-2020.csv", index=False, float_format="%.4g")
R["hydro_table_head"] = htab.round(3).to_dict(orient="records")
tot_h = {k: H[k][HU[k]].sum(axis=1) for k in H}
R["hydro_total_annual_1e6"] = {k: float((tot_h[k].groupby(tot_h[k].index.year).mean() * hrs_per_year / 1e6).mean()) for k in tot_h}
R["hydro_total_annual_CV"] = {k: float(100 * (tot_h[k].groupby(tot_h[k].index.year).mean()).std() / (tot_h[k].groupby(tot_h[k].index.year).mean()).mean()) for k in tot_h}
for k in tot_h:
    a = tot_h[k].groupby(tot_h[k].index.year).mean() * hrs_per_year / 1e6
    R[f"hydro_total_range_{k}"] = [float(a.min()), float(a.max()), int(a.idxmin()), int(a.idxmax())]
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.6))
for ax, k in zip(axs[:2], ["res", "ror"]):
    for c, col in [("NO2_A1", "C0"), ("SE2A", "C1"), ("FinA", "C4"), ("AT_A", "C2"), ("ES_A", "C3"), ("FR_A", "C5")]:
        if c not in H[k].columns:
            continue
        s = H[k][c]
        m = s.groupby(s.index.month).mean()
        ax.plot(range(1, 13), m / m.mean(), color=col, label=c)
    ax.set_xlabel("Month"); ax.set_ylabel(f"{'Reservoir' if k=='res' else 'Run-of-river'} inflow / annual mean (–)"); ax.set_xticks([1, 3, 5, 7, 9, 11])
axs[0].legend(frameon=False, loc="upper left", borderaxespad=0.6, ncol=2, fontsize=6.5)
ax = axs[2]
for k, col, lab in [("res", "C0", "reservoir"), ("ror", "C1", "run-of-river")]:
    a = tot_h[k].groupby(tot_h[k].index.year).mean() * hrs_per_year / 1e6
    ax.plot(a.index, a / a.mean(), color=col, label=lab)
ax.set_xlabel("Year"); ax.set_ylabel("Annual inflow / 1982–2020 mean (–)")
ax.legend(frameon=False, loc="upper left", borderaxespad=0.6, fontsize=6.5)
note(ax, f"CV: res {R['hydro_total_annual_CV']['res']:.1f}%, ror {R['hydro_total_annual_CV']['ror']:.1f}%", "lr")
ax.set_ylim(0.78, 1.17)
fig.tight_layout()
save(fig, "hydro_overview")
# hydro time structure
R["hydro_res_weekly_const"] = True  # verified separately below
x = H["res"]["AT_A"]
R["hydro_res_distinct_per_isoweek_median"] = float(x.groupby([x.index.isocalendar().year, x.index.isocalendar().week]).nunique().median())
x = H["ror"]["AT_A"]
R["hydro_ror_distinct_per_isoweek_median"] = float(x.groupby([x.index.isocalendar().year, x.index.isocalendar().week]).nunique().median())
R["hydro_nan"] = int(sum(int(H[k].isna().sum().sum()) for k in H))
R["hydro_de4_identical"] = bool(all(np.allclose(H["res"]["DE4-E_A"], H["res"][c]) for c in ["DE4-N_A", "DE4-S_A", "DE4-W_A"]))

# gap weeks (Shubham 52-week windows)
def first_monday(y: int) -> pd.Timestamp:
    s = pd.Timestamp(year=y, month=1, day=1)
    return s + pd.Timedelta(days=(7 - s.weekday()) % 7)


gaps = []
tot_utc = tot
clim_w = E["onshore wind"]
for y in range(1982, 2020):
    end = first_monday(y) + pd.Timedelta(hours=52 * 168)
    nxt = first_monday(y + 1)
    if nxt > end:
        a = pd.Timestamp(end, tz="UTC"); b = pd.Timestamp(nxt, tz="UTC") - pd.Timedelta(hours=1)
        d_gap, w_gap = tot_utc.loc[a:b].mean() / 1e3, clim_w.loc[a:b].mean()
        dw_gap = clim_w.loc[a:b].resample("D").mean()
        # same calendar days (Dec 31 - Jan 6) in all years for reference
        gaps.append(dict(year_end=y, gap_start=str(a.date()), gap_end=str(b.date()), mean_demand_GW=d_gap, mean_wind_CF=w_gap, min_daily_wind_CF=float(dw_gap.min())))
# 1982 start
a, b = pd.Timestamp("1982-01-01", tz="UTC"), pd.Timestamp(first_monday(1982), tz="UTC") - pd.Timedelta(hours=1)
gaps.insert(0, dict(year_end="start 1982", gap_start=str(a.date()), gap_end=str(b.date()), mean_demand_GW=tot.loc[a:b].mean() / 1e3,
                    mean_wind_CF=clim_w.loc[a:b].mean(), min_daily_wind_CF=float(clim_w.loc[a:b].resample("D").mean().min())))
gtab = pd.DataFrame(gaps)
gtab.to_csv(TAB / "shubham_52week_gap_weeks.csv", index=False, float_format="%.4g")
R["gap_table"] = gtab.round(3).to_dict(orient="records")
dec_jan = tot[(tot.index.month == 12) & (tot.index.day >= 28) | (tot.index.month == 1) & (tot.index.day <= 6)]
R["clim_dem_late_dec_early_jan_GW"] = float(dec_jan.mean() / 1e3)
dj_w = clim_w[(clim_w.index.month == 12) & (clim_w.index.day >= 28) | (clim_w.index.month == 1) & (clim_w.index.day <= 6)]
R["clim_wind_late_dec_early_jan_CF"] = float(dj_w.mean())
R["dem_winter_DJF_mean_GW"] = float(tot[tot.index.month.isin([12, 1, 2])].mean() / 1e3)
R["gap_days_total"] = int(7 * (len(gtab) - 1))

# presence matrix
allr = sorted(set(REG) | set(cov_regions["wind"]) | set(cov_regions["pv"]) | set(cov_regions["offshore"]) | {c.replace("_A1", "").replace("_A", "").replace("A", "") for c in H["res"].columns if False})
pres = []
hyd_map = {c: c for c in REG}
def hyd_name(h: str) -> str:
    return (h.replace("_A1", "").replace("_Other_DH", "").replace("_A", "")
            .replace("FinA", "FIN").replace("SE1A", "SE1").replace("SE2A", "SE2").replace("SE3A", "SE3").replace("SE4A", "SE4"))
hyd_regions = {hyd_name(c) for k in H for c in H[k].columns}
for r in sorted(set(REG) | set(cov_regions["wind"]) | hyd_regions | {c.replace("_OFF", "").replace("_OFF1", "").replace("_OFF2", "") for c in cov_regions["offshore"]}):
    pres.append(dict(region=r, demand=r in REG, onshore_wind=r in cov_regions["wind"], PV=r in cov_regions["pv"],
                     offshore_wind=any(c.startswith(r + "_OFF") for c in cov_regions["offshore"]), hydro=r in hyd_regions))
ptab = pd.DataFrame(pres)
ptab.to_csv(TAB / "coverage_by_region.csv", index=False)
R["coverage_table"] = ptab.to_dict(orient="records")
R["offshore_regions"] = cov_regions["offshore"]
R["demand_regions"] = REG
R["hydro_columns"] = {k: list(H[k].columns) for k in H}
R["wind_regions"] = cov_regions["wind"]
R["pv_regions"] = cov_regions["pv"]
R["window"] = [str(START), str(END), len(dem)]
R["dem_table"] = dtab.round(3).to_dict(orient="records")
R["wind_table"] = pd.read_csv(TAB / "cf_wind_by_region_1982-2020.csv").round(3).to_dict(orient="records")
R["pv_table"] = pd.read_csv(TAB / "cf_pv_by_region_1982-2020.csv").round(3).to_dict(orient="records")
R["offshore_table"] = pd.read_csv(TAB / "cf_offshore_by_region_1982-2020.csv").round(3).to_dict(orient="records")
(OUT / "tables" / "results.json").write_text(json.dumps(R, indent=1, default=str))
print("done", len(R), "keys")
