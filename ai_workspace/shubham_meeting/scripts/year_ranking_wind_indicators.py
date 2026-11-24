"""Rank the weather years 1982-2020 with statistics of the input data only (question B1).

Input: Mopo pan-European VRE data (Koivisto et al., Zenodo, doi:10.5281/zenodo.17950648),
onshore wind SP277-HH100, hourly, UTC. No demand, hydro or solar is used.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT: Path = Path(__file__).resolve().parents[3]
sys.dont_write_bytecode = True  # keep the project root free of __pycache__
sys.path.insert(0, str(ROOT))
from metrics import hours_below, min_running_mean, rank_most_stressful, weighted_mean_series  # noqa: E402

# Settings
RAW: Path = Path.home() / "local_data" / "Mopo" / "raw"
TECH: str = "wind-on-SP277-HH100"
YEARS: tuple[int, int] = (1982, 2020)  # period of Nayak et al. 2026
WINTER_MONTHS: tuple[int, ...] = (1, 2, 11, 12)
WINDOW_H: int = 14 * 24
LOW_QUANTILE: float = 0.10
EXTREME_YEARS: dict[int, str] = {1985: "#D55E00", 2010: "#0072B2", 1987: "#009E73", 1996: "#CC79A7"}
BASELINE_YEAR: int = 1995
FORCE_REPRODUCE_DATA: bool = False
OUT_DIR: Path = Path(__file__).resolve().parents[1] / "figures"
VAR, TRES, SRES, SOURCE, DOMAIN = "year_rank_wind_onshore_indicators", "1h", "Mopo-regions", "CorRES-Mopo", "EUR"
OUT_CSV: Path = OUT_DIR / f"{VAR}_{TRES}_{SRES}_{YEARS[0]}-{YEARS[1]}_{SOURCE}_{DOMAIN}.csv"
OUT_PNG: Path = OUT_CSV.with_suffix(".png")

plt.rcParams.update({
    "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.titlesize": 9, "legend.fontsize": 8, "font.size": 8,
    "figure.dpi": 150, "savefig.dpi": 220,
})

# (column, panel title, y label, low value = stress)
INDICATORS: list[tuple[str, str, str, bool]] = [
    ("annual_mean_cf", "(a) Annual mean", "Capacity factor (–)", True),
    ("winter_mean_cf", "(b) Winter mean (Jan, Feb, Nov, Dec)", "Capacity factor (–)", True),
    ("min_14d_mean_cf", "(c) Lowest 14-day running mean", "Capacity factor (–)", True),
    ("winter_low_hours", "(d) Winter hours below the 39-year 10th percentile",
     "Number of hours (h)", False),
]


def compute_indicators() -> pd.DataFrame:
    """Yearly indicators of the capacity-weighted European onshore wind capacity factor."""
    cf: pd.DataFrame = pd.read_csv(RAW / "VRE_time_series" / f"{TECH}.csv", index_col=0, parse_dates=True)
    cf.index = cf.index.tz_localize("UTC")
    cf = cf.dropna(axis=1, how="all").loc[str(YEARS[0]):str(YEARS[1])]
    cap: pd.DataFrame = pd.read_excel(
        RAW / "VRE_installed_capacities_2020_and_2025" / "capacity_wind-on-existing.xlsx", sheet_name="Regional")
    weights: pd.Series = cap.set_index("Child")[2025]
    x: pd.Series = weighted_mean_series(cf, weights)
    p_low: float = float(x.quantile(LOW_QUANTILE))
    winter: pd.Series = x[x.index.month.isin(WINTER_MONTHS)]
    by_year = x.groupby(x.index.year)
    out: pd.DataFrame = pd.DataFrame({
        "annual_mean_cf": by_year.mean(),
        "winter_mean_cf": winter.groupby(winter.index.year).mean(),
        "min_14d_mean_cf": by_year.apply(lambda s: min_running_mean(s, WINDOW_H)),
        "winter_low_hours": winter.groupby(winter.index.year).apply(lambda s: hours_below(s, p_low)),
    })
    for col, _, _, low in INDICATORS:
        out[f"rank_{col}"] = rank_most_stressful(out[col], low)
    out.index.name = "Year"
    print(f"regions used: {cf.shape[1]}, hours: {cf.shape[0]}, NaN: {int(x.isna().sum())}, mean CF: {x.mean():.4f}, P10: {p_low:.4f}")
    return out


def plot_ranking(ind: pd.DataFrame) -> plt.Figure:
    """Four panels, one indicator each; the years named by Nayak et al. 2026 are marked."""
    fig, axes = plt.subplots(2, 2, figsize=(190 / 25.4, 170 / 25.4), constrained_layout=True)
    n: int = len(ind)
    for ax, (col, title, ylabel, low) in zip(axes.ravel(), INDICATORS):
        v: pd.Series = ind[col]
        rk: pd.Series = ind[f"rank_{col}"]
        ax.plot(v.index, v.values, color="0.6", lw=0.8, marker="o", ms=2.5,
                label=f"n = {n}: mean = {v.mean():.3g}, sd = {v.std():.2g}")
        for yr, colour in EXTREME_YEARS.items():
            ax.plot(yr, v[yr], "o", ms=5.5, color=colour, label=f"{yr}: {v[yr]:.3g}, rank {rk[yr]}")
        ax.plot(BASELINE_YEAR, v[BASELINE_YEAR], "s", ms=5, mfc="none", mec="k",
                label=f"{BASELINE_YEAR} (baseline): {v[BASELINE_YEAR]:.3g}, rank {rk[BASELINE_YEAR]}")
        span: float = float(v.max() - v.min())
        ax.set_ylim(v.min() - 0.08 * span, v.max() + 1.1 * span)
        ax.set_title(title)
        ax.set_xlabel("Weather year")
        ax.set_ylabel(ylabel)
        ax.legend(loc="upper left", ncol=1, frameon=False, borderaxespad=0.6,
                  columnspacing=1.0, handletextpad=0.4,
                  title="Rank 1 = most stressful (" + ("lowest" if low else "highest") + " value)")
    return fig


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if OUT_CSV.exists() and not FORCE_REPRODUCE_DATA:
        indicators: pd.DataFrame = pd.read_csv(OUT_CSV, index_col="Year")
    else:
        indicators = compute_indicators()
        indicators.to_csv(OUT_CSV)
    figure: plt.Figure = plot_ranking(indicators)
    figure.savefig(OUT_PNG, dpi=220, bbox_inches="tight")
    rank_cols: list[str] = [c for c in indicators.columns if c.startswith("rank_")]
    print(indicators.loc[list(EXTREME_YEARS) + [BASELINE_YEAR]].round(4).to_string())
    for c in rank_cols:
        print(c, "five most stressful:", indicators[c].sort_values().index[:5].tolist())
    print(indicators.describe().loc[["min", "max"]].round(4).to_string())
    print(OUT_PNG)
