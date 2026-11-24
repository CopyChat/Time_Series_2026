# Toy experiments: why a system-defined event (shadow-price definition) depends on model assumptions
# and on the rest of its weather year, while a residual-load measure with fixed capacities does not.
# Synthetic data only; uses the toy LP in shadow_price_toy_lp.py.

from pathlib import Path

import numpy as np
import pandas as pd

from shadow_price_toy_lp import CAPEX, T, WINDOW_H, make_synthetic_year, solve_lp

OUT: Path = Path(__file__).resolve().parents[1] / "figures" / "sde_dependence_toy_synthetic.csv"
FEB: slice = slice(24 * 225, 24 * 245)   # 11 Feb - 3 Mar (days since 1 July): extra 20-day weak-wind period


def window_stats(d: np.ndarray, lam: np.ndarray, spell: slice) -> tuple[float, float, float]:
    """Best 14-day window overlapping the spell: (amount in bn EUR, share of annual sum, max over year bn EUR)."""
    hc = d * lam
    cs = np.concatenate([[0.0], np.cumsum(hc)])
    roll = cs[WINDOW_H:] - cs[:-WINDOW_H]
    starts = np.arange(max(spell.start - WINDOW_H + 1, 0), spell.stop)
    best = roll[starts].max()
    return best / 1e9, best / hc.sum(), roll.max() / 1e9


def deficit_fixed(d: np.ndarray, cf_w: np.ndarray, cf_s: np.ndarray, cap_w: float, cap_s: float,
                  period: slice) -> tuple[float, float]:
    """Residual load with fixed wind/solar capacities over a period: (energy deficit TWh, peak GW)."""
    rl = d[period] - cf_w[period] * cap_w - cf_s[period] * cap_s
    return np.clip(rl, 0, None).sum() / 1e6, rl.max() / 1e3


def main() -> None:
    d1, w1, s1, spell = make_synthetic_year()
    d2, w2, s2 = d1.copy(), w1.copy(), s1.copy()
    w2[FEB] *= 0.5
    d2[FEB] *= 1.05

    cases = {
        "A base": dict(d=d1, w=w1, s=s1, kw={}),
        "B H2 store cost x4": dict(d=d1, w=w1, s=s1, kw={"capex": {**CAPEX, "h2_store": 4 * CAPEX["h2_store"]}}),
        "C existing backup 60 GW": dict(d=d1, w=w1, s=s1, kw={"backup_mw": 60_000.0, "backup_mc": 150.0}),
        "D same January, weak February": dict(d=d2, w=w2, s=s2, kw={}),
    }
    rows = []
    base_threshold = None
    base_caps = None
    for name, cfg in cases.items():
        sol = solve_lp(cfg["d"], cfg["w"], cfg["s"], **cfg["kw"])
        amount, share, year_max = window_stats(cfg["d"], sol["lam"], spell)
        annual = (cfg["d"] * sol["lam"]).sum() / 1e9
        if base_threshold is None:
            base_threshold = 0.35 * annual            # fixed absolute threshold, as Grochowicz uses fixed EUR
            base_caps = sol["caps"]
        e_jan, p_jan = deficit_fixed(cfg["d"], cfg["w"], cfg["s"], base_caps[0], base_caps[1], spell)
        rows.append({
            "case": name, "total_cost_bnEUR": sol["obj"] / 1e9, "annual_sum_d_lambda_bnEUR": annual,
            "peak_shadow_price_EUR_MWh": sol["lam"].max(),
            "fuel_cell_GW": sol["caps"][3] / 1e3, "h2_store_TWh": sol["caps"][4] / 1e6,
            "jan_window_bnEUR": amount, "jan_window_share": share,
            "jan_is_event_fixed_threshold": amount >= base_threshold,
            "year_max_window_bnEUR": year_max,
            "jan_deficit_fixed_caps_TWh": e_jan, "jan_peak_deficit_fixed_caps_GW": p_jan,
        })
    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False, float_format="%.3f")
    pd.set_option("display.width", 250)
    print(f"fixed threshold = {base_threshold:.2f} bn EUR (35% of base annual sum)")
    print(df.T.to_string())
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()
