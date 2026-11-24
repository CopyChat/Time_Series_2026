"""Illustrate marginal distribution and quantile mapping (Nayak et al. 2026, Eq. 2).

All data are synthetic (AR(1) process mapped to a Beta distribution); not observations.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Settings
RNG: np.random.Generator = np.random.default_rng(7)
N_YEARS: int = 39
STEPS_PER_DAY: int = 8  # 3-hourly
DAYS_PER_YEAR: int = 364
N_YEAR: int = DAYS_PER_YEAR * STEPS_PER_DAY
PHI: float = 0.97  # lag-1 autocorrelation of the latent Gaussian process
WEEKS: tuple[int, ...] = (2, 8, 15, 21, 28, 34, 41, 47)  # weeks used in the manuscript
OUT: Path = Path(__file__).resolve().parents[1] / "figures" / "marginal_distribution_quantile_mapping_synthetic.png"

plt.rcParams.update({
    "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.titlesize": 9, "legend.fontsize": 8, "font.size": 8,
    "figure.dpi": 150, "savefig.dpi": 220,
})


def ar1(n: int, phi: float, rng: np.random.Generator) -> np.ndarray:
    """Standard Gaussian AR(1) series of length n."""
    eps: np.ndarray = rng.standard_normal(n) * np.sqrt(1.0 - phi**2)
    z: np.ndarray = np.empty(n)
    z[0] = rng.standard_normal()
    for i in range(1, n):
        z[i] = phi * z[i - 1] + eps[i]
    return z


def lag1(x: np.ndarray) -> float:
    """Lag-1 autocorrelation r1 = corr(x_t, x_{t+1})."""
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])


def quantile_map(short: np.ndarray, full: np.ndarray) -> np.ndarray:
    """p* = F_full^-1( F_short(p) ), both CDFs empirical (Nayak et al. 2026, Eq. 2)."""
    u: np.ndarray = (stats.rankdata(short) - 0.5) / short.size  # F_short(p)
    return np.quantile(full, u)  # F_full^-1(u)


def ecdf(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Empirical CDF: sorted values and cumulative probability."""
    xs: np.ndarray = np.sort(x)
    return xs, (np.arange(1, xs.size + 1) - 0.5) / xs.size


# Synthetic 39-year capacity factor: latent AR(1) + year offset -> Beta(1.6, 3.2)
year_offset: np.ndarray = RNG.normal(0.0, 0.18, N_YEARS)
latent: np.ndarray = ar1(N_YEARS * N_YEAR, PHI, RNG) + np.repeat(year_offset, N_YEAR)
full: np.ndarray = stats.beta.ppf(stats.norm.cdf(latent / latent.std()), 1.6, 3.2)
years: np.ndarray = full.reshape(N_YEARS, N_YEAR)

# Short selection: Thursday-Saturday of 8 weeks from the lowest-mean year
low_year: int = int(np.argmin(years.mean(axis=1)))
idx: np.ndarray = np.concatenate([
    np.arange(((w - 1) * 7 + 3) * STEPS_PER_DAY, ((w - 1) * 7 + 6) * STEPS_PER_DAY) for w in WEEKS
])
short: np.ndarray = years[low_year, idx]
scaled: np.ndarray = quantile_map(short, full)

# Panel a/b data: one 30-day excerpt and the same values in random order
seg: np.ndarray = years[low_year, : 30 * STEPS_PER_DAY]
shuf: np.ndarray = RNG.permutation(seg)
t_seg: np.ndarray = np.arange(seg.size) / STEPS_PER_DAY

fig = plt.figure(figsize=(190 / 25.4, 150 / 25.4), constrained_layout=True)
gs = fig.add_gridspec(2, 1)
gs_top = gs[0].subgridspec(1, 2, width_ratios=[1.45, 1.0])
gs_bot = gs[1].subgridspec(1, 2, width_ratios=[1.0, 1.45])
gs_a = gs_top[0].subgridspec(2, 1, hspace=0.08)

# (a) same values, two different orders
ax_a1 = fig.add_subplot(gs_a[0])
ax_a2 = fig.add_subplot(gs_a[1], sharex=ax_a1, sharey=ax_a1)
ax_a1.plot(t_seg, seg, color="C0", lw=0.9, label=f"Series A (original order), r1 = {lag1(seg):.2f}")
ax_a2.plot(t_seg, shuf, color="C1", lw=0.9, label=f"Series B (same values, shuffled), r1 = {lag1(shuf):.2f}")
ax_a1.set_title("(a) Two series with the same values in a different order")
ax_a1.tick_params(labelbottom=False)
ax_a2.set_xlabel("Time (days)")
for ax in (ax_a1, ax_a2):
    ax.set_ylim(0, 1.25)
    ax.set_ylabel("Capacity factor (–)")
    ax.legend(loc="upper left", frameon=False, borderaxespad=0.6)

# (b) their marginal distribution is identical
ax_b = fig.add_subplot(gs_top[1])
bins: np.ndarray = np.linspace(0, 1, 21)
ax_b.hist(seg, bins=bins, color="C0", alpha=0.55, label=f"A: mean = {seg.mean():.3f},\nsd = {seg.std():.3f}")
ax_b.hist(shuf, bins=bins, histtype="step", color="C1", lw=1.4,
          label=f"B: mean = {shuf.mean():.3f},\nsd = {shuf.std():.3f}")
ax_b.set_title("(b) Marginal distribution of A and B")
ax_b.set_xlabel("Capacity factor (–)")
ax_b.set_ylabel(f"Number of time steps (n = {seg.size})")
ax_b.set_ylim(0, ax_b.get_ylim()[1] * 1.6)
ax_b.legend(loc="upper right", frameon=False, borderaxespad=0.6)

# (c) quantile mapping on the two empirical CDFs
ax_c = fig.add_subplot(gs_bot[0])
xs_s, ps_s = ecdf(short)
xs_f, ps_f = ecdf(full)
ax_c.plot(xs_s, ps_s, color="C3", lw=1.2, label=f"F_short (n = {short.size}),\nmean = {short.mean():.3f}")
ax_c.plot(xs_f, ps_f, color="k", lw=1.2, label=f"F_full ({N_YEARS} years),\nmean = {full.mean():.3f}")
p_ex: float = float(np.quantile(short, 0.7))
u_ex: float = 0.7
p_star: float = float(np.quantile(full, u_ex))
ax_c.annotate("", xy=(p_ex, u_ex), xytext=(p_ex, 0), arrowprops=dict(arrowstyle="->", color="C3", lw=0.9))
ax_c.annotate("", xy=(p_star, u_ex), xytext=(p_ex, u_ex), arrowprops=dict(arrowstyle="->", color="0.4", lw=0.9))
ax_c.annotate("", xy=(p_star, 0), xytext=(p_star, u_ex), arrowprops=dict(arrowstyle="->", color="k", lw=0.9))
ax_c.plot([], [], color="0.4", lw=0.9,
          label=f"Example: p = {p_ex:.2f} →\nu = {u_ex:.2f} → p* = {p_star:.2f}")
ax_c.set_title("(c) p* = F_full⁻¹(F_short(p))")
ax_c.set_xlabel("Capacity factor (–)")
ax_c.set_ylabel("Cumulative probability (–)")
ax_c.set_xlim(0, 1)
ax_c.set_ylim(0, 1.9)
ax_c.set_yticks(np.arange(0, 1.01, 0.25))
ax_c.legend(loc="upper left", frameon=False, borderaxespad=0.6)

# (d) the short series before and after scaling
ax_d = fig.add_subplot(gs_bot[1])
t_short: np.ndarray = np.arange(short.size)
rho: float = float(stats.spearmanr(short, scaled)[0])
ax_d.plot(t_short, short, color="C3", lw=0.9,
          label=f"Before scaling: mean = {short.mean():.3f}, r1 = {lag1(short):.2f}")
ax_d.plot(t_short, scaled, color="k", lw=0.9,
          label=f"After scaling: mean = {scaled.mean():.3f}, r1 = {lag1(scaled):.2f}")
ax_d.plot([], [], " ", label=f"Rank correlation before/after = {rho:.2f};\n39-year mean = {full.mean():.3f}")
ax_d.set_title("(d) Selected steps before and after scaling")
ax_d.set_xlabel("Selected time step (index; 8 blocks of 3 days, 3-hourly)")
ax_d.set_ylabel("Capacity factor (–)")
ax_d.set_ylim(0, 1.75)
ax_d.set_yticks(np.arange(0, 1.01, 0.25))
ax_d.legend(loc="upper left", frameon=False, borderaxespad=0.6)

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=220, bbox_inches="tight")
print(OUT)
print(f"short mean {short.mean():.3f} scaled mean {scaled.mean():.3f} full mean {full.mean():.3f}")
print(f"lag1 seg {lag1(seg):.2f} shuf {lag1(shuf):.2f}; short {lag1(short):.2f} scaled {lag1(scaled):.2f}; rho {rho:.3f}")
