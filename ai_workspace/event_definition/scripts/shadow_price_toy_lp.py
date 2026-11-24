# Toy capacity-expansion LP: what an electricity shadow price is and why
# sum_t d_t * lambda_t over a window measures how much investment the window drives.
# Synthetic data only (one node, one year July-June); not observations, not a European model.

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

mpl.rcParams["figure.dpi"] = 150
mpl.rcParams["savefig.dpi"] = 220
plt.rcParams.update({
    "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.titlesize": 10, "legend.fontsize": 9, "font.size": 9,
})

OUT_DIR: Path = Path(__file__).resolve().parents[1] / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)
T: int = 8760
WINDOW_H: int = 336            # 14 days, as in Grochowicz et al. 2024/2026
THRESHOLD_SHARE: float = 0.35  # Grochowicz 2026: C = 100 bn EUR is ~35% of annual electricity cost

# Annualised capital costs (EUR per MW or MWh per year), illustrative values
CAPEX: dict[str, float] = {
    "wind": 110_000.0, "solar": 45_000.0,
    "electrolyser": 60_000.0, "fuel_cell": 90_000.0, "h2_store": 250.0,
}
ETA_CH: float = 0.70   # electrolyser efficiency
ETA_DIS: float = 0.50  # fuel cell efficiency
MC_DIS: float = 0.01   # tiny operating cost (EUR/MWh) to avoid degenerate cycling


def make_synthetic_year(seed: int = 3) -> tuple[np.ndarray, np.ndarray, np.ndarray, slice]:
    """Hourly demand (MW), wind and solar capacity factors for one July-June year,
    with one inserted cold, calm spell in January. Returns (d, cf_wind, cf_solar, spell)."""
    rng = np.random.default_rng(seed)
    h = np.arange(T)
    doy = h / 24.0                                   # days since 1 July
    winter = np.cos(2 * np.pi * (doy - 198) / 365)   # +1 in mid-January
    hod = h % 24
    daily = np.sin(2 * np.pi * (hod - 7) / 24)
    d = 350_000 * (1 + 0.18 * winter + 0.07 * daily) + rng.normal(0, 6_000, T)

    sun = np.clip(np.sin(np.pi * (hod - 6) / 12), 0, None) * (hod >= 6) * (hod <= 18)
    clouds = np.repeat(rng.uniform(0.35, 1.0, T // 24), 24)
    cf_solar = np.clip(sun * (0.55 - 0.30 * winter) * clouds, 0, 1)

    z = np.zeros(T)
    for t in range(1, T):
        z[t] = 0.985 * z[t - 1] + rng.normal(0, 0.17)
    spell = slice(24 * 192, 24 * 204)                # 9-21 January: 12 days
    z[spell] -= 2.2
    d[spell] *= 1.10
    cf_wind = 1 / (1 + np.exp(-(z + 0.35 * winter - 0.85)))
    return d, cf_wind, cf_solar, spell


def solve_lp(d: np.ndarray, cf_w: np.ndarray, cf_s: np.ndarray, capex: dict[str, float] | None = None,
             backup_mw: float = 0.0, backup_mc: float = 0.0) -> dict:
    """Minimise annualised capex + opex subject to hourly balance; return capacities,
    dispatch, objective and the dual of the balance constraint (shadow price, EUR/MWh).
    Optional existing backup plant: fixed capacity backup_mw (no capex), running cost backup_mc."""
    cx = CAPEX if capex is None else capex
    nC = 5                                           # Cw, Cs, Pc, Pd, E
    iw, is_, ic, idis, isoc, ib = (nC + k * T for k in range(6))
    n = nC + 6 * T
    c = np.zeros(n)
    c[:nC] = [cx["wind"], cx["solar"], cx["electrolyser"], cx["fuel_cell"], cx["h2_store"]]
    c[idis:idis + T] = MC_DIS
    c[ib:ib + T] = backup_mc
    r = np.arange(T)
    I = sp.identity(T, format="csr")
    # balance: w + s + dis - ch = d
    A_bal = sp.hstack([sp.csr_matrix((T, nC)), I, I, -I, I, sp.csr_matrix((T, T)), I])
    # storage: soc_t - soc_{t-1} - eta_ch ch_t + dis_t / eta_dis = 0 (cyclic)
    shift = sp.csr_matrix((np.ones(T), (r, (r - 1) % T)), shape=(T, T))
    A_soc = sp.hstack([sp.csr_matrix((T, nC)), sp.csr_matrix((T, 2 * T)), -ETA_CH * I, I / ETA_DIS, I - shift,
                       sp.csr_matrix((T, T))])
    A_eq = sp.vstack([A_bal, A_soc]).tocsr()
    b_eq = np.concatenate([d, np.zeros(T)])
    # availability and capacity limits: x_t - cf_t * Cap <= 0
    def cap_block(col_cap: int, start: int, coef: np.ndarray) -> sp.csr_matrix:
        m = sp.lil_matrix((T, n))
        m[r, start + r] = 1.0
        m[r, col_cap] = -coef
        return m.tocsr()
    one = np.ones(T)
    A_ub = sp.vstack([cap_block(0, iw, cf_w), cap_block(1, is_, cf_s), cap_block(2, ic, one),
                      cap_block(3, idis, one), cap_block(4, isoc, one)]).tocsr()
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(5 * T), A_eq=A_eq, b_eq=b_eq,
                  bounds=[(0, None)] * (nC + 5 * T) + [(0, backup_mw)] * T, method="highs")
    assert res.status == 0, res.message
    x = res.x
    return {
        "obj": res.fun, "lam": res.eqlin.marginals[:T], "caps": x[:nC],
        "w": x[iw:iw + T], "s": x[is_:is_ + T], "ch": x[ic:ic + T], "dis": x[idis:idis + T],
        "backup": x[ib:ib + T],
    }


def check_no_overlap(fig: plt.Figure, ax: plt.Axes, artists: list, fontsize_pt: float) -> None:
    """Rule 6 and 11: no plotted point inside a legend/text box; gap to the frame >= 0.5 em."""
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    ax_bb = ax.get_window_extent(rend)
    gap_px = 0.5 * fontsize_pt * fig.dpi / 72
    pts = [ax.transData.transform(np.column_stack(l.get_data())) for l in ax.get_lines()]
    pts = np.vstack(pts) if pts else np.empty((0, 2))
    bbs = [a.get_window_extent(rend) for a in artists]
    for i, bi in enumerate(bbs):
        for bj in bbs[i + 1:]:
            assert not bi.overlaps(bj), "two legend/text boxes overlap"
    for a, bb in zip(artists, bbs):
        inside = ((pts[:, 0] > bb.x0) & (pts[:, 0] < bb.x1) & (pts[:, 1] > bb.y0) & (pts[:, 1] < bb.y1)).sum()
        gaps = min(bb.x0 - ax_bb.x0, ax_bb.x1 - bb.x1, bb.y0 - ax_bb.y0, ax_bb.y1 - bb.y1)
        assert inside == 0, f"{inside} data points inside a legend/text box"
        assert gaps >= gap_px, f"{type(a).__name__}: gap {gaps:.1f}px < {gap_px:.1f}px"


def main() -> None:
    d, cf_w, cf_s, spell = make_synthetic_year()
    sol = solve_lp(d, cf_w, cf_s)
    lam = sol["lam"]
    hourly_cost = d * lam                                  # EUR per hour
    total_value = hourly_cost.sum()
    print(f"objective (total annual system cost) = {sol['obj'] / 1e9:.3f} bn EUR")
    print(f"sum_t d_t*lambda_t                   = {total_value / 1e9:.3f} bn EUR")
    names = ["wind (MW)", "solar (MW)", "electrolyser (MW)", "fuel cell (MW)", "H2 store (MWh)"]
    for nm, v in zip(names, sol["caps"]):
        print(f"  {nm:18s} {v:,.0f}")

    # zero-profit check: market value of each technology vs its annual capex
    rev = {"wind": (lam * sol["w"]).sum(), "solar": (lam * sol["s"]).sum(),
           "storage chain": (lam * (sol["dis"] - sol["ch"])).sum()}
    capex = {"wind": CAPEX["wind"] * sol["caps"][0], "solar": CAPEX["solar"] * sol["caps"][1],
             "storage chain": CAPEX["electrolyser"] * sol["caps"][2] + CAPEX["fuel_cell"] * sol["caps"][3]
             + CAPEX["h2_store"] * sol["caps"][4] + MC_DIS * sol["dis"].sum()}
    for k in rev:
        print(f"  revenue/cost {k:14s} {rev[k] / 1e9:7.3f} / {capex[k] / 1e9:7.3f} bn EUR")

    # rolling 14-day sum of d*lambda
    cs = np.concatenate([[0.0], np.cumsum(hourly_cost)])
    roll = (cs[WINDOW_H:] - cs[:-WINDOW_H]) / total_value       # share of annual total, start index
    t0 = int(np.argmax(roll))
    ev = slice(t0, t0 + WINDOW_H)
    n_hours_ev_share = roll[t0]
    fc_rev_ev = (lam[ev] * sol["dis"][ev]).sum() / max((lam * sol["dis"]).sum(), 1.0)
    print(f"max 14-day window starts day {t0 / 24:.1f} (from 1 July), share = {n_hours_ev_share:.1%}")
    print(f"fuel-cell revenue earned inside that window = {fc_rev_ev:.1%}")
    print(f"days above threshold (window starts): {(roll >= THRESHOLD_SHARE).sum() / 24:.1f}")

    # perturbation check: lambda_t = d(objective)/d(d_t)
    checks = []
    for t_chk in [int(np.argmax(lam)), int(np.argsort(lam)[T // 2])]:
        d2 = d.copy()
        delta = 10.0                                        # MW for one hour = 10 MWh
        d2[t_chk] += delta
        dobj = (solve_lp(d2, cf_w, cf_s)["obj"] - sol["obj"]) / delta
        checks.append((t_chk, lam[t_chk], dobj))
        print(f"hour {t_chk}: lambda = {lam[t_chk]:,.1f} EUR/MWh, finite difference = {dobj:,.1f} EUR/MWh")

    # figure
    days = np.arange(T) / 24.0
    fig, axes = plt.subplots(3, 1, figsize=(160 / 25.4, 175 / 25.4), sharex=True,
                             gridspec_kw={"hspace": 0.12})
    a, b, c = axes
    def dmean(x: np.ndarray) -> np.ndarray:
        return x.reshape(-1, 24).mean(axis=1)
    dd = np.arange(T // 24) + 0.5
    a.plot(dd, dmean(d) / 1e3, color="0.15", lw=1.0, label="Demand d (daily mean)")
    a.plot(dd, dmean(cf_w * sol["caps"][0] + cf_s * sol["caps"][1]) / 1e3, color="tab:blue", lw=0.9,
           label="Available wind + solar (daily mean)")
    a.axvspan(spell.start / 24, spell.stop / 24, color="tab:orange", alpha=0.25, label="Inserted cold, calm spell")
    a.set_ylabel("Power (GW)")
    a.set_ylim(0, 1.75 * max(dmean(d).max(), dmean(cf_w * sol["caps"][0] + cf_s * sol["caps"][1]).max()) / 1e3)
    leg_a = a.legend(loc="upper left", frameon=False, ncol=1, borderaxespad=0.8)

    b.plot(days, np.clip(lam, 0.1, None), color="tab:red", lw=0.5, label="Shadow price λ (floor 0.1)")
    b.axvspan(ev.start / 24, ev.stop / 24, color="0.6", alpha=0.3, label="Most costly window")
    b.set_yscale("log")
    b.set_ylim(0.1, lam.max() * 1e4)
    b.set_ylabel("Shadow price (EUR MWh⁻¹)")
    leg_b = b.legend(loc="upper left", frameon=False, borderaxespad=0.8)
    txt_b = b.annotate(f"Peak hour: λ = {checks[0][1]:,.0f}\n"
                       f"Δcost/Δdemand = {checks[0][2]:,.0f}",
                       xy=(1, 1), xycoords="axes fraction", xytext=(-8, -8), textcoords="offset points",
                       ha="right", va="top")

    c.plot(days[:len(roll)], 100 * roll, color="tab:purple", lw=1.0,
           label="14-day Σ d·λ")
    c.axhline(100 * THRESHOLD_SHARE, color="k", ls="--", lw=0.8, label=f"Threshold {THRESHOLD_SHARE:.0%}")
    c.axvspan(ev.start / 24, ev.stop / 24, color="0.6", alpha=0.3, label="Most costly window")
    c.set_ylim(0, 100 * roll.max() * 1.9)
    c.set_ylabel("Share of annual Σ d·λ (%)")
    c.set_xlabel("Days since 1 July (synthetic year)")
    leg_c = c.legend(loc="upper left", frameon=False, borderaxespad=0.8)
    txt_c = c.annotate(
                   f"Total cost = {sol['obj'] / 1e9:.2f} bn EUR\n"
                   f"Annual Σ d·λ = {total_value / 1e9:.2f} bn EUR\n"
                   f"Most costly window: {n_hours_ev_share:.0%}\n"
                   f"Fuel-cell revenue in it: {fc_rev_ev:.0%}",
                   xy=(1, 1), xycoords="axes fraction", xytext=(-8, -8), textcoords="offset points",
                   ha="right", va="top")
    c.set_xlim(0, 365)
    for ax, arts in [(a, [leg_a]), (b, [leg_b, txt_b]), (c, [leg_c, txt_c])]:
        check_no_overlap(fig, ax, arts, 9)
    for ax, lab in zip(axes, "abc"):
        ax.text(0.005, 1.02, f"({lab})", transform=ax.transAxes, ha="left", va="bottom")
    out = OUT_DIR / "shadow_price_toy_lp_synthetic.png"
    fig.savefig(out, dpi=220, bbox_inches="tight")
    print(f"saved {out}")


if __name__ == "__main__":
    main()
