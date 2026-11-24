# Illustrate the two parts of Q2 with synthetic numbers (not results)
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT: Path = Path(__file__).resolve().parents[1] / "figures" / "Q2_illustration_synthetic.png"
plt.rcParams.update({"axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
                     "axes.titlesize": 10, "legend.fontsize": 9, "font.size": 9})


def spread(n: np.ndarray, s1: float, rho: float) -> np.ndarray:
    """Relative spread of an estimate from n years: s1 / sqrt(n_eff), n_eff = n (1 − ρ) / (1 + ρ)."""
    n_eff = n * (1 - rho) / (1 + rho)
    return s1 / np.sqrt(n_eff)


def years_needed(n: np.ndarray, s: np.ndarray, eps: float) -> int:
    """Smallest record length n with spread s(n) ≤ eps."""
    ok = n[s <= eps]
    return int(ok[0]) if ok.size else -1


n = np.arange(5, 101)
eps = 5.0                                   # target precision (% of value), illustrative
s_mean = spread(n, 10.0, 0.2)               # e.g. mean capacity factor
s_ext = spread(n, 30.0, 0.2)                # e.g. 1-in-20-year drought duration
n_mean, n_ext = years_needed(n, s_mean, eps), years_needed(n, s_ext, eps)

years = np.arange(2025, 2081)
sig_demand = -0.25 * (years - 2025)          # e.g. heating-driven demand peak, % change
sig_wind = -0.03 * (years - 2025)            # e.g. wind-plus-solar variability, % change
noise = 2 * spread(np.array([30]), 10.0, 0.2)[0]   # ±2 × spread of a 30-year window
toe = int(years[np.argmax(np.abs(sig_demand) > noise)])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(190 / 25.4, 78 / 25.4), constrained_layout=True)
a1.plot(n, s_mean, color="#0b6a93", lw=2, label=f"Mean: {n_mean} years needed")
a1.plot(n, s_ext, color="#b06d00", lw=2, label=f"1-in-20-year drought: {n_ext} years needed")
a1.axhline(eps, color="0.4", ls="--", lw=1, label=f"Target precision ({eps:.0f} %)")
a1.set(xlabel="Record length (years)", ylabel="Uncertainty of the estimate (% of value)",
       title="(a) How many years make a statistic stable?", xlim=(5, 100), ylim=(0, 40))
leg1 = a1.legend(loc="upper right", frameon=False, borderaxespad=0.6)

a2.fill_between(years, -noise, noise, color="0.85", label=f"Noise of a 30-year record (±{noise:.1f} %)")
a2.plot(years, sig_demand, color="#b06d00", lw=2, label=f"Demand-like statistic: emerges in {toe}")
a2.plot(years, sig_wind, color="#0b6a93", lw=2, label="Wind/solar-like statistic: stays in noise")
a2.vlines(toe, -16, noise, color="#b06d00", ls=":", lw=1, label="Time of emergence")
a2.set(xlabel="Year", ylabel="Change in statistic (% of today's value)",
       title="(b) When does climate change exceed the noise?", xlim=(2025, 2080), ylim=(-16, 22))
leg2 = a2.legend(loc="upper right", frameon=False, borderaxespad=0.6)
fig.canvas.draw()
for ax, leg in ((a1, leg1), (a2, leg2)):
    box = leg.get_window_extent()
    for line in ax.get_lines():
        pts = ax.transData.transform(np.column_stack(line.get_data()))
        inside = (pts[:, 0] > box.x0) & (pts[:, 0] < box.x1) & (pts[:, 1] > box.y0) & (pts[:, 1] < box.y1)
        assert not inside.any(), f"legend overlaps {line.get_label()}"
fig.savefig(OUT, dpi=220, bbox_inches="tight")
print(OUT, "n_mean", n_mean, "n_ext", n_ext, "noise", round(noise, 2), "toe", toe)
