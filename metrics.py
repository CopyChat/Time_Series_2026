"""Single source of all statistical formulas of the Time_Series_2026 project.

Every notebook and script imports its metric functions from this file.
"""
import numpy as np
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


def pearson_r(x: pd.Series, y: pd.Series) -> float:
    """Pearson correlation coefficient.

    r = sum_t (x_t - mean x)(y_t - mean y) / sqrt( sum_t (x_t - mean x)^2 * sum_t (y_t - mean y)^2 )
    """
    return float(np.corrcoef(x.values, y.values)[0, 1])


def cumulative_deficit(residual: pd.Series, reference: float) -> pd.Series:
    """Cumulative deficit of residual load above a reference supply level (research plan, event definition).

    cumulative deficit(t) = max( 0 , cumulative deficit(t-1) + residual load(t) - reference supply level )

    residual: hourly residual load (GW); reference: reference supply level (GW). Result in GWh.
    """
    x: np.ndarray = residual.values - reference
    c: np.ndarray = np.zeros_like(x)
    acc: float = 0.0
    for i, v in enumerate(x):
        acc = max(0.0, acc + v)
        c[i] = acc
    return pd.Series(c, index=residual.index)


def deficit_events(cum: pd.Series, residual: pd.Series, reference: float) -> pd.DataFrame:
    """Events = runs of consecutive hours with cumulative deficit > 0.

    For each event: start, end, duration (h), maximum cumulative deficit (GWh, storage energy that the event needs),
    peak gap = max_t (residual load - reference) (GW), mean residual load (GW).
    """
    on: np.ndarray = cum.values > 0
    rows: list[dict] = []
    i, n = 0, len(on)
    while i < n:
        if on[i]:
            j = i
            while j + 1 < n and on[j + 1]:
                j += 1
            seg = slice(i, j + 1)
            rows.append(dict(start=cum.index[i], end=cum.index[j], duration_h=j - i + 1,
                             max_cum_deficit_GWh=float(cum.values[seg].max()),
                             peak_gap_GW=float((residual.values[seg] - reference).max()),
                             mean_residual_GW=float(residual.values[seg].mean())))
            i = j + 1
        else:
            i += 1
    return pd.DataFrame(rows)


def storage_unserved(residual: pd.Series, firm: float, p_sto: float, e_sto: float, eta: float = 1.0) -> pd.Series:
    """Unserved energy after firm capacity and one aggregated storage (greedy dispatch, no foresight).

    gap(t)      = residual load(t) - firm capacity
    gap > 0 :  discharge d = min(gap, storage power, state of charge);   unserved(t) = gap - d
    gap < 0 :  charge    c = min(-gap, storage power, (storage energy - state of charge) / efficiency)
    state of charge starts full. Units: GW, GWh per hour step.
    """
    x: np.ndarray = residual.values - firm
    u: np.ndarray = np.zeros_like(x)
    soc: float = e_sto
    for i, g in enumerate(x):
        if g > 0:
            d = min(g, p_sto, soc)
            soc -= d
            u[i] = g - d
        else:
            c = min(-g, p_sto, (e_sto - soc) / eta)
            soc += c * eta
    return pd.Series(u, index=residual.index)


def calendar_decomposition(daily: pd.Series) -> dict:
    """Split the variance of a daily series into season, day of week and remainder.

    season(d)     = mean over all years of the series on the same day of the year
    anomaly(d)    = series(d) - season(d)
    weekday(d)    = least-squares mean of the anomaly on the same weekday (Monday ... Sunday)
    remainder(d)  = anomaly(d) - weekday(d)          (weather response, holidays, trend)

    share_season    = 1 - var(anomaly) / var(series)
    share_weekday   = (var(anomaly) - var(remainder)) / var(series)
    share_remainder = var(remainder) / var(series)
    """
    doy = daily.index.dayofyear
    season = daily.groupby(doy).transform("mean")
    anom = daily - season
    X = pd.get_dummies(daily.index.weekday).astype(float).values
    beta = np.linalg.lstsq(X, anom.values, rcond=None)[0]
    remainder = anom - X @ beta
    v = daily.var()
    return dict(season=season, weekday_effect=beta, fit=season + X @ beta, anomaly=anom, remainder=remainder,
                std=float(daily.std()), std_anom=float(anom.std()), std_remainder=float(remainder.std()),
                share_season=float(1 - anom.var() / v), share_weekday=float((anom.var() - remainder.var()) / v),
                share_remainder=float(remainder.var() / v))


def return_period_weibull(values: pd.Series) -> pd.Series:
    """Empirical return period of annual (or per-winter) maxima, Weibull plotting position.

    T_k = (n + 1) / k,   k = rank in descending order (1 = largest),  n = number of years
    """
    k: pd.Series = values.rank(ascending=False, method="first")
    return (len(values) + 1) / k
