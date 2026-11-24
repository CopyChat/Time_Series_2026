"""Single source of all statistical formulas of the Time_Series_2026 project.

Every notebook and script imports its metric functions from this file.
"""
import pandas as pd


def weighted_mean_series(cf: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """Capacity-weighted mean capacity factor over regions.

    x_t = sum_r (w_r * CF_r,t) / sum_r w_r

    cf: hourly capacity factor, one column per region (–). weights: capacity per region (GW).
    """
    w: pd.Series = weights.reindex(cf.columns).fillna(0.0)
    return (cf * w).sum(axis=1) / w.sum()


def min_running_mean(x: pd.Series, window_h: int) -> float:
    """Lowest running mean over a window of window_h hours.

    m = min_t [ (1 / W) * sum_{k=0..W-1} x_{t-k} ],  W = window_h
    """
    return float(x.rolling(window_h).mean().min())


def hours_below(x: pd.Series, threshold: float) -> int:
    """Number of hours with the value below a threshold.

    N = sum_t 1[x_t < c],  c = threshold
    """
    return int((x < threshold).sum())


def rank_most_stressful(values: pd.Series, low_is_stress: bool) -> pd.Series:
    """Rank of each year, 1 = most stressful.

    low_is_stress=True: rank 1 is the lowest value; False: rank 1 is the highest value.
    """
    return values.rank(ascending=low_is_stress, method="min").astype(int)
