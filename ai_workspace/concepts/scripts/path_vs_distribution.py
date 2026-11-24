# Illustrate "path" vs "distribution of values" with synthetic data (not observations)
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

OUT: Path = Path(__file__).resolve().parents[1] / "figures" / "path_vs_distribution_synthetic.png"
plt.rcParams.update({"axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
                     "axes.titlesize": 10, "legend.fontsize": 9, "font.size": 9})


def lag1_autocorr(x: np.ndarray) -> float:
    """r1 = corr(x_t, x_{t+1})."""
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])


def max_ramp(x: np.ndarray) -> float:
    """max_t |x_{t+1} − x_t| (MW per hour)."""
    return float(np.max(np.abs(np.diff(x))))


rng = np.random.default_rng(3)
h = np.arange(24)
# Path A: a smooth synthetic day of wind power for a 100 MW fleet (wind dropping in the evening)
path_a = 60 + 30 * np.cos(2 * np.pi * (h - 3) / 24) + rng.normal(0, 2, 24)
path_a = np.clip(path_a, 0, 100)
# Path B: the same 24 hourly values in a random order
path_b = rng.permutation(path_a)

ks = ks_2samp(path_a, path_b).statistic
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(190 / 25.4, 75 / 25.4), constrained_layout=True)
ax1.plot(h, path_a, "-o", ms=3, color="#0b6a93",
         label=f"Path A: r1 = {lag1_autocorr(path_a):.2f}, max ramp = {max_ramp(path_a):.0f} MW/h")
ax1.plot(h, path_b, "-s", ms=3, color="#b06d00",
         label=f"Path B: r1 = {lag1_autocorr(path_b):.2f}, max ramp = {max_ramp(path_b):.0f} MW/h")
ax1.set(xlabel="Hour of day (h)", ylabel="Wind power (MW)", xlim=(-0.5, 23.5), ylim=(0, 140),
        title="(a) Two paths: same values, different order")
ax1.legend(loc="upper center", frameon=False, borderaxespad=0.6)

for x, c, lab in [(path_a, "#0b6a93", "Path A"), (path_b, "#b06d00", "Path B")]:
    ax2.plot(np.arange(1, 25), np.sort(x)[::-1], color=c, lw=2 if lab == "Path A" else 1, ls="-" if lab == "Path A" else "--",
             label=f"{lab} duration curve")
ax2.set(xlabel="Rank of hour (h)", ylabel="Wind power (MW)", xlim=(0.5, 24.5), ylim=(0, 140),
        title="(b) Identical value distributions")
ax2.legend(loc="upper right", frameon=False, borderaxespad=0.6, title=f"KS distance A vs B = {ks:.2f}")
fig.savefig(OUT, dpi=220, bbox_inches="tight")
print(OUT, "KS", ks, "r1", lag1_autocorr(path_a), lag1_autocorr(path_b), "ramps", max_ramp(path_a), max_ramp(path_b))
