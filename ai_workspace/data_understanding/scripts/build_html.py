"""Build 01_data_understanding/data_understanding.html from tables/results.json and the CSV tables."""
from __future__ import annotations

import html
import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT: Path = Path(__file__).resolve().parents[3] / "01_data_understanding"
def _num(x):
    """Convert numeric strings written by json default=str back to floats."""
    if isinstance(x, dict):
        return {k: _num(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_num(v) for v in x]
    if isinstance(x, str):
        try:
            return float(x)
        except ValueError:
            return x
    return x


R: dict = _num(json.loads((OUT / "tables" / "results.json").read_text()))
SD: dict = _num(json.loads((OUT / "tables" / "supply_demand_heat.json").read_text()))
T = OUT / "tables"


def tbl(df: pd.DataFrame, fmt: dict[str, str] | None = None, cls: str = "") -> str:
    fmt = fmt or {}
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in df.columns)
    rows = []
    for _, r in df.iterrows():
        cells = []
        for c in df.columns:
            v = r[c]
            if isinstance(v, (bool, np.bool_)):
                cells.append(f"<td class='{'yes' if v else 'no'}'>{'✓' if v else '–'}</td>")
            elif isinstance(v, float) and pd.isna(v):
                cells.append("<td>–</td>")
            elif c in fmt and isinstance(v, (int, float)):
                cells.append(f"<td class='num'>{fmt[c].format(v)}</td>")
            else:
                cells.append(f"<td>{html.escape(str(v))}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"<div class='tw'><table class='{cls}'><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


def fig(name: str, caption: str) -> str:
    return f"<figure><img src='figures/{name}.png' alt='{html.escape(name)}'><figcaption>{caption}</figcaption></figure>"


dem = pd.read_csv(T / "demand_by_region_1982-2020.csv")
wind = pd.read_csv(T / "cf_wind_by_region_1982-2020.csv")
pv = pd.read_csv(T / "cf_pv_by_region_1982-2020.csv")
off = pd.read_csv(T / "cf_offshore_by_region_1982-2020.csv")
hyd = pd.read_csv(T / "hydro_inflow_by_area_1982-2020.csv")
cov = pd.read_csv(T / "coverage_by_region.csv")
inv = pd.read_csv(T / "vre_files_inventory.csv")
gap = pd.read_csv(T / "shubham_52week_gap_weeks.csv")

d_cv = R["dem_tot_annual_CV_pct"]
ws, ps, os_ = R["cf_wind_summary"], R["cf_pv_summary"], R["cf_offshore_summary"]
wk = R["dem_weekday_effect_GW"]
vre_anom = dict(R["vre_daily_anom_std_pct"])
top_demand_days = ", ".join(f"{d} ({v:.1f} GW)" for d, v in R["dem_top_days"][:3])
dpk = R["dem_peak_dates"]

summary = f"""
<ol class="key">
<li><b>数据是什么。</b>DTU Data 合集“Pan-European weather dependent generation and demand time series for Balmorel Energy system modelling”（Nayak、Koivisto、Kanellas 2025，doi:10.11583/DTU.c.7964141），逐时、GMT，全部由同一套 ERA5 天气驱动；与 Shubham 使用的是同一批文件（2026年11月20日 MD5 核对）。本课题使用的时期：1982年1月1日至2020年12月31日，共 {R['window'][2]:,} 小时（39 个天气年）。</li>
<li><b>为什么选它（决定 D17）。</b>需要电力需求：这是已找到的唯一与天气年一致、逐时、覆盖多国的需求；同一合集还有水电来水和风光，区域和时期相同，并可与 Shubham Nayak 的结果直接对照。</li>
<li><b>需求主要由日历决定，其中最大的是星期效应，不是季节。</b>日历指“一年中的第几天”（季节）、“星期几”和节假日。26 个区域合计日平均需求的方差中：季节（一年中的第几天的多年平均）只解释 {100*(1-R['dem_resid_doy_std_GW']**2/R['dem_daily_std_GW']**2):.0f}%，星期效应再解释 {100*(R['dem_resid_doy_std_GW']**2-R['dem_resid_doy_wd_std_GW']**2)/R['dem_daily_std_GW']**2:.0f}%，剩余 {100*R['dem_resid_doy_wd_std_GW']**2/R['dem_daily_std_GW']**2:.0f}%（含天气响应、节假日和随机项，本数据无法再分开）；扣除后日标准差只有 {R['dem_resid_doy_wd_std_GW']:.2f} GW（占均值 {100*R['dem_resid_doy_wd_std_GW']/R['dem_daily_mean_GW']:.1f}%），而陆上风电日距平标准差占均值 {vre_anom['onshore wind']:.0f}%。每个季节的需求峰值都落在 12 月 {dpk['day_min']}–{dpk['day_max']} 日的 {dpk['hour_set'][0]}:00 GMT，年际差只有 {100*(R['dem_peak_season_range_GW'][1]-R['dem_peak_season_range_GW'][0])/R['dem_peak_season_range_GW'][0]:.2f}%。</li>
<li><b>年需求几乎不变。</b>26 个区域合计年需求变异系数 {d_cv:.2f}%（陆上风电区域平均容量因子年均值为 {R['E_annual_CV_onshore wind']:.1f}%，光伏 {R['E_annual_CV_PV']:.1f}%）。“classic”需求不含电采暖、电动汽车、电转 X 和氢（Kruse 2023 §4.1），所以与低温有关的电力需求增加不在其中。</li>
<li><b>风光都是逐时容量因子（0–1）。</b>陆上风电 SP277_HH150 的区域平均容量因子随资源等级从 RGA 的 {R['rg_means_wind'][0]:.3f} 降到 RGC 的 {R['rg_means_wind'][2]:.3f}；选哪种技术和资源等级直接改变发电量，装机要另给。</li>
<li><b>水电来水</b>：水库式为周常数、径流式为日常数（由日或周来水展开为逐时），25 个区域，readme 没有写单位，本页的数值按“10⁶ 单位”报告。</li>
<li><b>极端</b>：区域平均陆上风电最低的 7 日平均容量因子出现在 {R['wind_lowest_7d_winter'][1]} 前后（{R['wind_lowest_7d_winter'][0]:.3f}）；各冬季的最低风与最高需求基本无关（r = {R['season_corr_lowwind_highdemand']:.2f}，n = {R['season_sample']}），因为需求峰值由日历决定。</li>
<li><b>Shubham 的 52 周天气年窗口</b>在 7 个年边界各丢掉 7 天（共 {R['gap_days_total']} 天，1984、1990、1996、2001、2007、2012、2018 年末），所以事件识别不用它，用连续序列。</li>
<li><b>还没核实的：</b>需求和水电的单位（readme 没写，按量级推断为 MW 和 MWh h⁻¹）；风光装机；热需求和热泵系数文件本页没有分析；气候预估没有对应的需求。</li>
</ol>
"""

prov = pd.DataFrame([
    ["天气驱动", "ERA5 再分析（逐时），所有部件用同一套天气，保持变量间相关", "Nayak et al. 2026 §2.1 [全文已读]；Hersbach et al. 2020"],
    ["风电、光伏", "CorRES 模拟；微尺度订正用全球风图集 GWA2，用替代功率曲线考虑风电场内尾流；多种风机技术（比功率、轮毂高度）和资源等级", "Nayak et al. 2026 §2.1.1；验证见 Nayak et al. 2025（Applied Energy 402:126882，未读）"],
    ["电力需求（classic）", "ERA5 气温、星期、节假日、日照时长、小时的线性回归，由 ENTSO-E 2015–2018 年总负荷拟合、2019 年样本外检验（多数区域 MAPE 3–6%），用中心估计（确定性）；只含传统用电，不含电采暖、电动汽车、电转 X、氢", "Kruse 2023 硕士论文 §4.1、§4.2、§6.1.2 [第 4 章与 6.1 已读]；Nayak et al. 2026 §2.1.2 引用此方法。DTU 文件与该论文模型是同一版本：[推断，未核实]"],
    ["供热需求、热泵性能系数", "加权度日法（75% 随气温变化，25% 与气温无关），再按 Balmorel 情景的年需求缩放；热泵参照 Ruhnau et al. 2019", "Nayak et al. 2026 §2.1.2；Kruse 2023 §4.3。本页未分析"],
    ["水电来水", "GloFAS-ERA5 v4.0 河流流量，用 ENTSO-E 2015–2025 历史水库和径流发电数据，经随机森林加岭回归混合模型估计各天气年来水；留一年交叉验证", "Nayak et al. 2026 §2.1.3；数据 Liu & Rahmlow 2026（doi:10.5281/zenodo.18632738，未读）。Balmorel_DTU 的 readme 给出生成代码 github.com/Yil2/hydro_mopo"],
    ["区域与时间", "Balmorel 区域（北欧按竞价区，德国分 4 个区域，其余每国一个区域）；GMT 时间戳", "Nayak et al. 2026 §3、图 4；readme"],
], columns=["部件", "怎样生成", "出处与读取范围"])

invtab = pd.DataFrame([
    ["电力需求 classic_demand.csv", "electricity_demand/", R["n_regions_demand"], "1982-01-01 至 2021-12-31", "逐时", "未写明（量级与德国峰值负荷一致，推断为 MW）", "无"],
    ["陆上风电 SP277_HH150_RGB.csv（及 11 个同类文件）", "wind_onshore/", R["cov"]["wind"], "1980-01-01 至 2021-12-31", "逐时", "容量因子 0–1", "无"],
    ["陆上风电 Existing.csv（2020 年现有风电场）", "wind_onshore/", 45, "1980-01-01 至 2022-12-31", "逐时", "容量因子 0–1", "无"],
    ["海上风电 SP316_HH155_RGB.csv（固定式）", "wind_offshore/Future_bottom_fixed/", R["cov"]["offshore"], "1980-01-01 至 2021-12-31", "逐时", "容量因子 0–1", "无"],
    ["光伏（9 个文件：屋顶、公用事业无跟踪、有跟踪 × RGA–RGC）", "solar_PV/", R["cov"]["pv"], "1980-01-01 至 2021-12-31", "逐时", "容量因子 0–1", "无"],
    ["水库式来水 res_inflow.csv", "hydro_inflow/", R["hydro_areas"]["res"], "1980-01-01 至 2021-12-31", "逐时（周常数）", "未写明", "无"],
    ["径流式来水 ror_inflow.csv", "hydro_inflow/", R["hydro_areas"]["ror"], "1980-01-01 至 2021-12-31", "逐时（日常数）", "未写明", "无"],
    ["年校正系数 *_flh_fac.csv", "hydro_inflow/", 25, "1980–2021（逐年）", "年", "无量纲", "无"],
    ["供热需求、热泵性能系数", "heat_demand/、heat_pump_COP/", "–", "1980/1982–2021", "逐时", "–", "未分析"],
], columns=["数据", "目录（~/local_data/Balmorel_DTU/raw/）", "区域数", "覆盖时期", "时间分辨率", "单位", "缺测"])

covmat = cov.rename(columns={"region": "区域", "demand": "需求", "onshore_wind": "陆上风电", "PV": "光伏", "offshore_wind": "海上风电", "hydro": "水电"})

# demand table
dtab = dem[["region", "mean_GW", "P1_GW", "P99_GW", "max_GW", "max_time", "min_GW", "annual_TWh", "annual_CV_pct", "DJF_over_JJA"]].copy()
dtab.columns = ["区域", "均值 (GW)", "1% 分位 (GW)", "99% 分位 (GW)", "最大 (GW)", "最大出现时刻 (GMT)", "最小 (GW)", "年需求 (TWh)", "年需求变异系数 (%)", "冬季/夏季"]

wtab = wind[["region", "mean", "std", "P5", "P50", "P95", "max", "DJF", "JJA", "annual_mean_min", "annual_mean_max", "annual_CV_pct"]].copy()
wtab.columns = ["区域", "均值", "标准差", "5% 分位", "中位数", "95% 分位", "最大", "冬季均值", "夏季均值", "年均最小", "年均最大", "年均变异系数 (%)"]
ptab = pv[["region", "mean", "std", "P95", "max", "share_below_0p01", "DJF", "JJA", "annual_CV_pct"]].copy()
ptab.columns = ["区域", "均值", "标准差", "95% 分位", "最大", "CF<0.01 的小时占比", "冬季均值", "夏季均值", "年均变异系数 (%)"]
otab = off[["region", "mean", "std", "P5", "P95", "max", "DJF", "JJA", "annual_CV_pct"]].copy()
otab.columns = ["区域", "均值", "标准差", "5% 分位", "95% 分位", "最大", "冬季均值", "夏季均值", "年均变异系数 (%)"]

inv2 = inv[["series", "n_regions", "first", "last", "min", "max", "mean_CF_window", "mean_CF_common29"]].copy()
inv2.columns = ["序列", "区域数", "起", "止", "最小", "最大", "1982–2020 平均 CF（全部区域）", "1982–2020 平均 CF（29 个公共区域）"]

hyd_s = hyd.copy()
hyd_s["type"] = hyd_s["type"].map({"res": "水库式", "ror": "径流式"})
hyd_s = hyd_s[["area", "type", "annual_sum_1e6", "annual_CV_pct", "peak_month", "trough_month", "max_hourly", "zero_share"]]
hyd_s.columns = ["区域", "类型", "年来水 (10⁶ 单位)", "年来水变异系数 (%)", "来水最大月", "来水最小月", "逐时最大值", "零值占比"]

gap2 = gap.copy()
gap2.columns = ["年末", "缺口起", "缺口止", "平均需求 (GW)", "平均风电 CF（区域平均）", "最低日均风电 CF"]

page = f"""<!doctype html>
<html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>数据理解：Balmorel_DTU 数据（需求、风光、水电）</title>
<style>
:root{{--bg:#fafaf8;--fg:#1d1d1b;--mut:#5a5a55;--line:#d8d8d2;--acc:#0b6e8a;--box:#eef5f7;--warn:#fdf3e3;--warnl:#e3b86a}}
@media (prefers-color-scheme: dark){{:root{{--bg:#16181a;--fg:#e8e8e4;--mut:#a4a4a0;--line:#3a3d40;--acc:#5fc0d9;--box:#1f2a2f;--warn:#2d2616;--warnl:#8a6d2b}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,"Segoe UI","PingFang SC","Noto Sans SC",sans-serif;margin:0}}
main{{max-width:1080px;margin:0 auto;padding:24px 16px 80px}}
h1{{font-size:26px;margin:.2em 0}} h2{{font-size:20px;margin-top:2.2em;border-bottom:1px solid var(--line);padding-bottom:.25em}} h3{{font-size:16px;margin-top:1.6em}}
.sub{{color:var(--mut)}} nav{{background:var(--box);padding:10px 14px;border-radius:6px;margin:14px 0;font-size:14px}} nav a{{color:var(--acc);margin-right:12px;text-decoration:none}}
.tw{{overflow-x:auto;margin:10px 0}} table{{border-collapse:collapse;font-size:12.5px;min-width:100%}} th,td{{border-bottom:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}}
th{{position:sticky;top:0;background:var(--bg);border-bottom:2px solid var(--line)}} td.num{{text-align:right;font-variant-numeric:tabular-nums}} td.yes{{color:var(--acc);text-align:center}} td.no{{color:var(--mut);text-align:center}}
figure{{margin:16px 0}} figure img{{max-width:100%;height:auto}} figcaption{{font-size:13px;color:var(--mut);margin-top:4px}}
.box{{background:var(--box);border-left:4px solid var(--acc);padding:10px 14px;border-radius:4px;margin:14px 0}} .warn{{background:var(--warn);border-left:4px solid var(--warnl);padding:10px 14px;border-radius:4px;margin:14px 0}}
ol.key li{{margin:.5em 0}} code{{font-size:12.5px;background:var(--box);padding:1px 4px;border-radius:3px}} .small{{font-size:13px;color:var(--mut)}}
@media (max-width:600px){{h1{{font-size:21px}}}}
</style></head><body><main>
<h1>数据理解：Balmorel_DTU 数据（需求、风、光、水电）</h1>
<p class="sub">项目 Time_Series_2026 · 更新：2026年11月23日 · 数据位置 <code>~/local_data/Balmorel_DTU/raw/</code>（只读）· 统计窗口：1982年1月1日 00:00 至 2020年12月31日 23:00（GMT）· 计算脚本 <code>ai_workspace/data_understanding/scripts/</code>，表格在 <code>01_data_understanding/tables/</code>，图在 <code>01_data_understanding/figures/</code></p>
<nav><a href="#s0">要点</a><a href="#s1">来源</a><a href="#s2">有哪些数据</a><a href="#s3">覆盖区域</a><a href="#s4">质量检查</a><a href="#s5">需求</a><a href="#s6">风光</a><a href="#s7">水电</a><a href="#s7b">供需总图</a><a href="#s7c">供热与热泵</a><a href="#s7d">RG 与装机</a><a href="#s8">极端</a><a href="#s9">52 周窗口缺口</a><a href="#s10">对研究的含义</a><a href="#s11">未核实</a><a href="#s12">参考文献</a></nav>

<h2 id="s0">要点</h2>
{summary}

<h2 id="s1">1. 数据从哪里来、怎样生成</h2>
<p>下表只列已经读过的出处；读取范围标在最后一列。</p>
{tbl(prov)}
<div class="box"><b>选这套数据的原因（D17）：</b>需要需求数据。本课题的事件定义用剩余负荷（需求 − 风 − 光 − 径流式水电），没有与天气年一致的逐时需求就无法定义事件。该合集提供了已找到的唯一这样的需求，水电来水、风、光在同一套区域和同一时期里，还是 Shubham Nayak 使用的数据，第 3 层验证可以与已发表结果直接对照。</div>

<h2 id="s2">2. 有哪些数据（available）</h2>
{tbl(invtab)}
<p class="small">本页统计一律限于 1982年1月1日至2020年12月31日；需求文件从 1982年1月1日开始，风光和水电从 1980年1月1日开始，所以 1980–1981 年没有需求，不进入事件目录。需求文件共 {R['demand_file_span'][2]:,} 行，等于 40 年（含 10 个闰年）的小时数。</p>
<h3>风光序列清单（11 个文件的逐列统计）</h3>
{tbl(inv2, {"最小":"{:.4f}","最大":"{:.3f}","1982–2020 平均 CF（全部区域）":"{:.3f}","1982–2020 平均 CF（29 个公共区域）":"{:.3f}"})}
<p class="small">光伏序列中夜间有极小的负值（最小 {R['vre_neg_max']:.4f}），是数值噪声，使用前要截断为 0。没有大于 1 的值。</p>

<h2 id="s3">3. 覆盖区域</h2>
<p>需求 {R['n_regions_demand']} 个区域（其中德国 4 个区域 DE4-E/N/S/W 的列完全相同，每列都是全国需求，合计时只取一列，所以独立区域 {R['n_unique_demand']} 个）；陆上风电 {R['cov']['wind']} 个区域、光伏 {R['cov']['pv']} 个、海上风电 {R['cov']['offshore']} 个；水库式来水 {R['hydro_areas']['res']} 个、径流式来水 {R['hydro_areas']['ror']} 个（水电德国 4 个区域同样完全相同；两类来水的区域不完全相同：只有水库式的 {', '.join(R['hydro_cols_only_res'])}，只有径流式的 {', '.join(R['hydro_cols_only_ror'])}）。需求区域全部有陆上风电和光伏列，所以 {R['common_regions']} 个需求区域可作公共区域集。</p>
{tbl(covmat)}
<p class="small">水电区域名与需求区域名不同（如 NO2_A1 对应 NO2，SE2A 对应 SE2，FinA 对应 FIN），上表已按名称对应；LV_Other_DH 与 LV_RigaR 都归入拉脱维亚。</p>

<h2 id="s4">4. 质量检查</h2>
<ul>
<li>缺测：需求、风光、水电全部为 0 个缺测值（水电 {R['hydro_nan']} 个）。</li>
<li>时间连续：需求文件逐时无间断（{R['demand_hourly_continuous']}）；时间戳为 GMT，没有夏令时间断。</li>
<li>需求无零或负值（{R['demand_nonpositive']} 个）。</li>
<li>德国 4 个区域的需求列完全相同（{R['de4_identical']}），水电来水同样（{R['hydro_de4_identical']}）。</li>
<li>水库式来水每个 ISO 周内取值个数的中位数为 {R['hydro_res_distinct_per_isoweek_median']:.0f}（周常数）；径流式为 {R['hydro_ror_distinct_per_isoweek_median']:.0f}（日常数）。因此水电在日内和周内没有变化，事件识别在小时尺度上看到的水电变化是展开造成的。</li>
<li>风光容量因子上限：陆上和海上风电最大 0.95，现有风电场 0.90（功率曲线的饱和）。</li>
</ul>

<h2 id="s5">5. 电力需求（classic_demand）</h2>
<div class="box">需求是什么：<b>传统用电</b>（家庭、商业、工业），<b>不含</b>电采暖、电动汽车、电转 X 和氢 [Kruse 2023 §4.1]。由气温、星期、节假日、日照时长和小时回归得到的<b>中心估计</b>，没有随机残差 [Kruse 2023 §6.1.2]。所以它具有很强的日历结构、很弱的天气信号。</div>
<h3>5.1 总体统计（26 个独立区域合计）</h3>
<ul>
<li>平均 {R['dem_tot_mean_GW']:.1f} GW；年需求 {R['dem_tot_annual_TWh']:.0f} TWh（单位若为 MW）；年需求变异系数 {d_cv:.2f}%，年需求范围 {R['dem_tot_annual_range_TWh'][0]:.0f}–{R['dem_tot_annual_range_TWh'][1]:.0f} TWh（{R['dem_tot_annual_range_TWh'][2]}年最小、{R['dem_tot_annual_range_TWh'][3]}年最大）；线性趋势 {R['dem_tot_trend_pct_per_decade']:.2f}% 每十年。各区域年需求变异系数 {R['dem_region_annual_CV_range_pct'][0]:.2f}–{R['dem_region_annual_CV_range_pct'][1]:.2f}%（中位数 {R['dem_region_annual_CV_range_pct'][2]:.2f}%）。德国年需求 {R['de_annual_TWh'][0]:.0f} TWh（{R['de_annual_TWh'][1]:.0f}–{R['de_annual_TWh'][2]:.0f}）。</li>
<li>小时极值：最大 {R['dem_tot_max_GW'][0]:.1f} GW（{R['dem_tot_max_GW'][1][:13]}），最小 {R['dem_tot_min_GW'][0]:.1f} GW（{R['dem_tot_min_GW'][1][:13]}）；1%–99% 分位 {R['dem_tot_P1_P99_GW'][0]:.0f}–{R['dem_tot_P1_P99_GW'][1]:.0f} GW。最大日平均需求的前三天 {top_demand_days}；日平均需求最大的 100 天全部在 12 月。</li>
<li>日需求的方差主要来自星期效应（日历的一部分）：日平均需求标准差 {R['dem_daily_std_GW']:.1f} GW；扣除“一年中的第几天”的多年平均后 {R['dem_resid_doy_std_GW']:.1f} GW；再扣除星期效应后 {R['dem_resid_doy_wd_std_GW']:.2f} GW（占均值 {100*R['dem_resid_doy_wd_std_GW']/R['dem_daily_mean_GW']:.2f}%）；季节解释 {100*(1-R['dem_resid_doy_std_GW']**2/R['dem_daily_std_GW']**2):.0f}%、星期效应解释 {100*(R['dem_resid_doy_std_GW']**2-R['dem_resid_doy_wd_std_GW']**2)/R['dem_daily_std_GW']**2:.0f}%，剩余 {100*R['dem_resid_doy_wd_std_GW']**2/R['dem_daily_std_GW']**2:.0f}%。<b>“日历”是什么：</b>这里指一年中的第几天（季节循环，包含该日多年平均的气温和日照）、星期几、节假日；日需求变化的其他来源有：天气（气温、风、云，通过采暖、制冷、照明；本数据的 classic 需求只保留气温的响应）、经济活动和结构性变化（年际趋势）、随机波动（本数据为确定性中心估计，没有）。注意“扣除第几天的多年平均”同时扣除了季节平均气温的作用，所以“季节”这一项里已含气温的气候态；“剩余”里才有当天气温偏离气候态的作用。星期效应（周一至周日，相对均值，GW）：{', '.join(f'{b:+.1f}' for b in wk)}。各区域扣除后的日标准差占其均值的 {R['dem_resid_region_pct_range'][0]:.1f}–{R['dem_resid_region_pct_range'][1]:.1f}%（中位数 {R['dem_resid_region_pct_range'][2]:.1f}%）。作比较，区域平均的陆上风电、光伏、海上风电的日距平标准差分别占其均值的 {vre_anom['onshore wind']:.0f}%、{vre_anom['PV']:.0f}%、{vre_anom['offshore wind']:.0f}%。</li>
<li>每个季节（7月1日至次年6月30日，1982–2019 共 {R['dem_peak_season_n']} 个）的最高小时需求出现在 12 月 {dpk['day_min']}–{dpk['day_max']} 日、{dpk['hour_set'][0]}:00 GMT，且为周三至周五；数值 {R['dem_peak_season_range_GW'][0]:.2f}–{R['dem_peak_season_range_GW'][1]:.2f} GW，年际差 {100*(R['dem_peak_season_range_GW'][1]-R['dem_peak_season_range_GW'][0])/R['dem_peak_season_range_GW'][0]:.2f}%。冬季最高的 7 日平均需求只取 {', '.join(f'{v:.1f}' for v in R['dem_high7_distinct_values'])} GW 这几个值，取决于圣诞节落在星期几。</li>
</ul>
{fig("demand_overview", "图 1 需求总体：(a) 月平均（灰带为 39 年的最小–最大）；(b) 年需求相对 1982–2020 均值的比值，年需求按每年平均功率计算（避免闰年多一天）；(c) 冬季（12–2 月）与夏季（6–8 月）的日内平均曲线。26 个独立区域合计，德国只计一列。")}
{fig("demand_distribution_extremes", "图 2 需求分布与极值：(a) 总需求相对年均值的累积分布；(b) 每个季节（7 月至次年 6 月）的最高小时总需求。")}
<h3>5.2 各区域统计</h3>
<p class="small"><b>年需求变异系数的定义：</b>对 1982–2020 的每一年取全年平均功率，得到 39 个年值；变异系数 = 这 39 个年值的标准差（样本标准差，自由度 39−1）÷ 它们的平均值 × 100%。表中不同区域差别大（{R['dem_region_annual_CV_range_pct'][0]:.2f}%–{R['dem_region_annual_CV_range_pct'][1]:.2f}%），原因本页没有查明：意大利（0.66%）、西班牙（0.55%）、荷兰（0.37%）较大，荷兰的年值从 1984–86 年约 0.995 升到 2018–20 年约 1.01，有上升趋势，说明至少部分来自趋势或区域回归对气温的响应强弱不同；要核对需要各区域气温，PECD 气温尚未下载。</p>
{tbl(dtab, {"均值 (GW)":"{:.2f}","1% 分位 (GW)":"{:.2f}","99% 分位 (GW)":"{:.2f}","最大 (GW)":"{:.2f}","最小 (GW)":"{:.2f}","年需求 (TWh)":"{:.1f}","年需求变异系数 (%)":"{:.2f}","冬季/夏季":"{:.2f}"})}
<p class="small">表中“DE4”是 DE4-E/N/S/W 四列中的一列（四列相同）。单位按量级推断为 MW，统计量转为 GW。完整表见 <code>tables/demand_by_region_1982-2020.csv</code>。</p>

<h2 id="s6">6. 风电和光伏的容量因子（CF）</h2>
<div class="box">CF = 逐时发电功率 ÷ 装机容量（无量纲，0–1）。发电量 = CF × 装机，装机不在这套数据里（Mopo 提供 2020 年和 2025 年的区域装机）。陆上、海上、光伏各有多种技术：文件名中的 SP 是比功率、HH 是轮毂高度，RGA/RGB/RGC 是资源等级（技术所在地理位置的分级，readme）；本数据中 CF 按 RGA、RGB、RGC 依次降低（见下）[Nayak et al. 2026 §2.1.1]。</div>
<h3>6.1 总体统计（陆上 SP277_HH150_RGB、光伏公用事业无跟踪 RGB、海上固定式 SP316_HH155_RGB）</h3>
<ul>
<li>陆上风电：29 个公共区域平均 CF {ws['mean_of_region_means']:.3f}；最低 {ws['min_region'][0]} {ws['min_region'][1]:.3f}，最高 {ws['max_region'][0]} {ws['max_region'][1]:.3f}；冬季/夏季 {ws['DJF_over_JJA']:.2f}；各区域年均 CF 的变异系数 {ws['CV_annual_range'][0]:.1f}–{ws['CV_annual_range'][1]:.1f}%（中位数 {ws['CV_annual_median']:.1f}%）。区域平均序列的年均 CF 变异系数 {R['E_annual_CV_onshore wind']:.1f}%（{R['E_annual_range_onshore wind'][2]}年 {R['E_annual_range_onshore wind'][0]:.1f}%，{R['E_annual_range_onshore wind'][3]}年 +{R['E_annual_range_onshore wind'][1]:.1f}%）。</li>
<li>光伏：29 个公共区域平均 CF {ps['mean_of_region_means']:.3f}；最低 {ps['min_region'][0]} {ps['min_region'][1]:.3f}，最高 {ps['max_region'][0]} {ps['max_region'][1]:.3f}；冬季/夏季 {ps['DJF_over_JJA']:.2f}；约 {100*ps['zero_share_mean']:.0f}% 的小时 CF 小于 0.01（夜间）；区域平均序列年均 CF 变异系数 {R['E_annual_CV_PV']:.1f}%。</li>
<li>海上风电：{R['cov']['offshore']} 个区域平均 CF {os_['mean_of_region_means']:.3f}；最低 {os_['min_region'][0]} {os_['min_region'][1]:.3f}，最高 {os_['max_region'][0]} {os_['max_region'][1]:.3f}；区域平均序列年均 CF 变异系数 {R['E_annual_CV_offshore wind']:.1f}%。</li>
<li>资源等级和技术的影响（29 个公共区域平均）：陆上 SP277_HH150 为 RGA {R['rg_means_wind'][0]:.3f}、RGB {R['rg_means_wind'][1]:.3f}、RGC {R['rg_means_wind'][2]:.3f}；光伏无跟踪为 RGA {R['rg_means_pv'][0]:.3f}、RGB {R['rg_means_pv'][1]:.3f}、RGC {R['rg_means_pv'][2]:.3f}。现有风电场（2020 年）为陆上 {inv.loc[inv.series=='onshore existing 2020 fleet','mean_CF_common29'].iloc[0]:.3f}、海上 {inv.loc[inv.series=='offshore existing 2020 fleet','mean_CF_window'].iloc[0]:.3f}（海上现有风电场区域数少，未限于公共区域）。</li>
<li>风电 CF 的小时分布在满发附近（约 0.95）有尖峰，在 0 附近也集中；这是功率曲线的饱和与切入所致，不是缺测。</li>
<li>空间相关：29 个区域日平均陆上风电 CF 的两两相关系数平均 {R['wind_corr_pairs']['mean']:.2f}（10% 分位 {R['wind_corr_pairs']['P10']:.2f}，90% 分位 {R['wind_corr_pairs']['P90']:.2f}），冬季（12–2 月）平均 {R['wind_corr_pairs_DJF_mean']:.2f}；伊比利亚（ES、PT）与北欧、中欧几乎不相关。</li>
</ul>
<p class="small"><b>图 3(a) 的检验：</b>区域平均陆上风电 1 月 CF 的多年平均 0.53、最大 0.67（1983 年），我用独立代码重算得到相同结果，所以算法没有错。数值偏高的原因是：(1) 这是未来技术（比功率 277 W m⁻²、轮毂高 150 m）的 RGB 序列，不是现有机组；同样 29 个区域的 2020 年现有风电场 1 月平均 0.38、全年 0.28；(2) 简单平均给每个区域相同权重，英国 1 月平均 0.66，而葡萄牙 0.33；(3) 灰带是单月、39 年中的最大值。全年 0.41 的未来陆上风电与现有机组相比偏高，是否合理要对照 Nayak et al. 2025 的验证论文（未读）。</p>
{fig("vre_overview", "图 3 风光总体：(a) 区域平均 CF 的月平均（陆上风电的灰带为 39 年最小–最大）；(b) 年均 CF 相对多年均值的距平；(c) 区域平均小时 CF 的累积分布。陆上风电和光伏为 29 个公共区域的简单平均，海上风电为全部 38 个区域的简单平均，未按装机加权。")}
{fig("vre_distribution_resource_grade", "图 4 区域分布与资源等级：(a) 5 个区域的陆上风电小时 CF 概率密度；(b) 光伏小时 CF 的累积分布；(c) 资源等级对 29 个区域平均 CF 的影响。")}
{fig("wind_spatial_correlation", "图 5 29 个区域日平均陆上风电 CF 的相关系数矩阵（区域按需求文件的顺序排列）。")}
<h3>6.2 各区域统计</h3>
<p><b>陆上风电 SP277_HH150_RGB（29 个公共区域）</b></p>
{tbl(wtab, {c:"{:.3f}" for c in wtab.columns[1:11]} | {"年均变异系数 (%)":"{:.1f}"})}
<p><b>光伏 公用事业无跟踪 RGB（29 个公共区域）</b></p>
{tbl(ptab, {c:"{:.3f}" for c in ptab.columns[1:8]} | {"年均变异系数 (%)":"{:.1f}"})}
<p><b>海上风电 SP316_HH155_RGB（38 个区域）</b></p>
{tbl(otab, {c:"{:.3f}" for c in otab.columns[1:8]} | {"年均变异系数 (%)":"{:.1f}"})}

<h2 id="s7">7. 水电来水</h2>
<div class="box">两类来水：水库式（<code>res</code>）和径流式（<code>ror</code>）。逐时文件，但水库式在每个 ISO 周内为常数、径流式在每天内为常数，由周或日来水展开。单位 readme 未写明；挪威 NO2 水库式年来水量级（约 {hyd[(hyd.area=='NO2_A1')&(hyd.type=='res')].annual_sum_1e6.iloc[0]:.0f}×10⁶）与该区域水电年发电量（数十 TWh）一致，推断为 MWh h⁻¹，<b>未核实</b>。<code>*_flh_fac.csv</code> 是逐年、逐区域的年满负荷小时数校正系数。来水不是发电：径流式近似为不可调的发电，水库式要经过水库容量和调度才变成发电。</div>
<ul>
<li>合计（德国只计一次；水库式 {R['hydro_unique']['res']} 个、径流式 {R['hydro_unique']['ror']} 个独立区域）：年来水水库式 {R['hydro_total_annual_1e6']['res']:.0f}、径流式 {R['hydro_total_annual_1e6']['ror']:.0f}（10⁶ 单位）；年来水变异系数水库式 {R['hydro_total_annual_CV']['res']:.1f}%、径流式 {R['hydro_total_annual_CV']['ror']:.1f}%；最小年水库式 {R['hydro_total_range_res'][2]}、径流式 {R['hydro_total_range_ror'][2]}，最大年水库式 {R['hydro_total_range_res'][3]}、径流式 {R['hydro_total_range_ror'][3]}。</li>
<li>季节性：北欧（NO2、SE2）水库式来水在 5–6 月（融雪）最大，冬季最小；阿尔卑斯（AT）6 月最大；西班牙（ES）冬春最大、夏季最小。北欧水库式来水在冬季（1–3 月）最少，与 12 月需求峰值同在冬季。</li>
</ul>
{fig("hydro_overview", "图 6 水电来水：(a) 水库式和 (b) 径流式来水的月平均相对年均值；(c) 合计年来水相对多年均值。")}
<h3>各区域统计</h3>
{tbl(hyd_s, {"年来水 (10⁶ 单位)":"{:.2f}","年来水变异系数 (%)":"{:.1f}","逐时最大值":"{:.0f}","零值占比":"{:.3f}"})}

<h2 id="s7b">7b. 供需总图（基于当前数据）</h2>
<div class="warn">这是用 2025 年装机说明量级的示意图，不是研究的情景。装机取 Mopo 2025 年国家总装机（陆上风电 {SD['cap_used_GW']['onshore']:.0f} GW、海上风电 {SD['cap_used_GW']['offshore']:.0f} GW、光伏 {SD['cap_used_GW']['pv']:.0f} GW，限于 26 个需求区域所在国），按国家内有序列的区域平分；风电用 2020 年现有风电场的容量因子，光伏没有现有机组序列，用公用事业无跟踪 RGB 的序列；径流式水电用来水代替发电（单位按 MWh h⁻¹ 假设）；水库式来水不是发电，只在右下图单独标出；NO5 没有现有风电序列，其装机未计入（挪威装机平分到 NO1–NO4）。</div>
{fig("supply_demand", "图 8 供需总图（26 个独立区域合计，1982–2020）：(a) 各月平均功率，堆叠为供给，黑线为需求，红虚线为剩余负荷；(b) 低风的两周（1989年12月27日起）逐时供需；(c) 需求与剩余负荷的持续曲线；(d) 年能量。")}
<ul>
<li>年能量：需求 {SD['annual_TWh']['demand']:.0f} TWh；陆上风电 {SD['annual_TWh']['onshore']:.0f}、海上风电 {SD['annual_TWh']['offshore']:.0f}、光伏 {SD['annual_TWh']['pv']:.0f}、径流式来水 {SD['annual_TWh']['ror']:.0f} TWh；风光合计占需求 {SD['vre_share_of_demand_pct']:.0f}%；剩余负荷平均 {SD['resid_stats_GW']['mean']:.0f} GW，最大 {SD['resid_stats_GW']['max']:.0f} GW（{SD['resid_stats_GW']['max_time'][:13]}），最小 {SD['resid_stats_GW']['min']:.0f} GW（{SD['resid_stats_GW']['neg_hours_pct']:.1f}% 的小时为负，即风光多于需求）。最大的连续 7 日平均剩余负荷 {SD['resid_max_7d_GW'][0]:.0f} GW，在 {SD['resid_max_7d_GW'][1][:10]} 前后。</li>
<li>现有风电场的平均容量因子：陆上 {SD['mean_CF_fleet']['onshore']:.2f}、海上 {SD['mean_CF_fleet']['offshore']:.2f}、光伏 {SD['mean_CF_fleet']['pv']:.2f}（按这里的装机加权）。</li>
<li>供给的日内形状：光伏每天一个尖峰，风电变化缓慢，水电（径流式）近似常数；需求有日内两峰和周内周期。</li>
<li>这个示意不含供热、电采暖、电动汽车、电转 X（见第 7c 节和第 10 节）。</li>
</ul>

<h2 id="s7c">7c. 供热需求、热泵性能系数（COP）</h2>
<ul>
<li><b>供热需求（<code>heat_demand/</code>）是什么：</b>各 Balmorel 区域或区域内的区域供热/个体供热的逐时<b>归一化曲线</b>（形状），不是绝对量；readme：未按年需求缩放，使用时要按年热需求缩放，另有逐年校正系数（<code>heat_yearly_corr_factors_*.csv</code>）。生成方法：度日法，75% 随气温变化（采暖）、25% 与气温无关（热水）[Kruse 2023 §4.3；Nayak et al. 2026 §2.1.2]。</li>
<li><b>是否只在冬天有：</b>不是，但强烈集中在冬季。个体住宅采暖曲线（{SD['heat_cols']} 个区域）：冬季（12–2 月）日均值是夏季（6–8 月）的中位数 {SD['heat_DJF_over_JJA_median']:.0f} 倍；6–8 月合计只占年量的 {SD['heat_JJA_share_pct_median']:.1f}%（中位区域）；约 {SD['heat_zero_hours_pct_median']:.0f}% 的小时为零（气温高于度日阈值）。1 月占全年 {SD['heat_month_share_median_pct'][0]:.1f}%，7 月 {SD['heat_month_share_median_pct'][6]:.1f}%（图 9a）。</li>
<li><b>热泵性能系数（COP，<code>heat_pump_COP/</code>）：</b>热泵每消耗 1 单位电能输出的热量，COP = 供热量 ÷ 耗电量，无量纲。热泵从室外空气取热，室外越冷，COP 越低，所以冬季 COP 低、夏季高：空气源热泵 COP 取值 {SD['cop_airwater_range'][0]:.2f}–{SD['cop_airwater_range'][1]:.2f}；月平均的中位区域从 1 月 {SD['cop_airwater_month_median'][0]:.1f} 升到 7 月 {SD['cop_airwater_month_median'][6]:.1f}（图 9b）。方法参照 Ruhnau et al. 2019 [Nayak et al. 2026 §2.1.2]。<b>本数据里空气-水热泵与空气-空气热泵的 COP 文件数值完全相同</b>（逐值核对前 5000 小时），所以两类热泵没有区分。</li>
<li><b>“什么时候用热泵”：</b>只有有热需求时才用，热需求集中在冬季，所以热泵用电集中在冬季，而冬季恰是 COP 最低的时候。热泵用电 ≈ 供热量 ÷ COP（图 9c）：1 月占全年热量的 {SD['heat_share_month_matched_pct'][0]:.1f}%，换算成电量占 {SD['hp_elec_share_month_pct'][0]:.1f}%，冬季比热量更集中；逐月峰值之比 {SD['hp_elec_peak_over_heat_peak']:.2f}。这是 {SD['n_matched_heat_cop']} 个可与 COP 对应的区域的中位值，只是形状；绝对用电量要用 Balmorel 基础数据里的年热需求和各技术的占比（本地未取得）。</li>
</ul>
{fig("heat_cop", "图 9 供热与热泵：(a) 个体住宅采暖曲线的月份占年量的比例（灰带为 10–90% 区域）；(b) 热泵 COP 月平均（空气-水与空气-空气相同，曲线重合）；(c) 热量与热泵电量（热量 ÷ COP）的月份占比。")}

<h2 id="s7d">7d. RGA、RGB、RGC 是什么；这些输入会不会给出装机</h2>
<ul>
<li><b>资源等级（resource grade，RG）：</b>某技术的候选安装地点按资源好坏分级：RG A = 最好的 10% 地点，RG B = 次好的 10–50%，RG C = 最差的 50% [Mopo 项目文件 Info_about_VRE_time_series，陆上风电和光伏页]。每个 RG 有自己的容量因子序列（本数据中 A &gt; B &gt; C）。在 Shubham Nayak 的 Balmorel 设置中，RGA/RGB/RGC 对应模型的 RG1/RG2/RG3（`config.yml`）。Mopo 公开数据只模拟了 RG B。</li>
<li><b>这些输入会不会给出装机：</b>不会。文件是容量因子曲线，不含装机。Balmorel 把每种技术和 RG 的组合当作投资候选：容量因子曲线决定每单位装机能发多少电，加上成本（`VRE_Tech_Costs`）和各区域各 RG 的潜力上限（`VRE_Potentials`，由可用面积 × 装机密度得到：陆上 1 MW km⁻²、海上 1.5 MW km⁻²、光伏 4 MW km⁻² [Mopo 项目文件 Info_about_VRE_costs_potentials…]），由模型<b>优化</b>出各区域各技术各 RG 的装机；也就是说装机是模型的输出，不是这些输入的结果。已有装机（2020、2025 年）是另一组输入（Mopo 的 capacity_*-existing.xlsx，国家和 Mopo 区域层面）。</li>
<li>对本课题的含义：不跑 Balmorel（D1），装机由我们设定（情景），同一套 CF 曲线配不同装机就得到不同的剩余负荷（D11）。</li>
</ul>

<h2 id="s8">8. 极端</h2>
<ul>
<li><b>低风</b>：区域平均陆上风电日均 CF 的最低值 {R['wind_lowest_day'][0]:.3f}（{R['wind_lowest_day'][1]}，夏季）。冬季（11 月至次年 3 月）最低的 7 日平均 CF 为 {R['wind_lowest_7d_winter'][0]:.3f}，在 {R['wind_lowest_7d_winter'][1]} 前后；按冬季分，最低的三个冬季是 {', '.join(f"{y}/{str(y+1)[2:]}（{v:.3f}）" for y, v in R['wind_low7_top3'])}。</li>
<li>冬季日均 CF 的 10% 分位 {R['wind_winter_P10_daily_CF']:.3f}；连续低于它的最长时段（天，起始日）：{', '.join(f'{n} d，{d}' for n, d in R['wind_winter_longest_runs'][:4])}。这是 29 个区域的简单平均，空间平均会缩短并减弱单个区域的低风时段；多国同时低风的特征要在事件目录里按国家单独计算。</li>
<li><b>需求与低风基本无关</b>：区域平均日均风电 CF 与总需求的相关系数在冬季为 {R['corr_dem_wind_DJF']:.2f}、全年为 {R['corr_dem_wind_all']:.2f}（去除季节循环后冬季 {R['corr_dem_wind_DJF_anom']:.2f}）；光伏与需求冬季 {R['corr_dem_pv_DJF']:.2f}、全年 {R['corr_dem_pv_all']:.2f}。各冬季的最低 7 日风电 CF 与最高 7 日需求的相关系数 {R['season_corr_lowwind_highdemand']:.2f}（n = {R['season_sample']}）。</li>
</ul>
{fig("winter_extremes_wind_demand", "图 7 冬季极端：(a) 每个冬季（11–3 月）区域平均陆上风电 CF 的最低 7 日平均；(b) 冬季最低 7 日风电 CF 与最高 7 日总需求的关系（每个冬季一点，需求取值集中在少数几个值，因为它由圣诞节落在星期几决定）。")}

<h2 id="s9">9. Shubham 的 52 周天气年窗口：丢掉的跨年周</h2>
<p>他的规则（<code>rep_period_functions.py</code>）：每年从 1 月第一个星期一 00:00 起取 52 周（8736 小时）。逐年计算得出，39 个年边界中 32 个首尾相接，7 个出现 7 天缺口；1982 年 1 月 1–3 日也在窗口之外。</p>
{tbl(gap2, {"平均需求 (GW)":"{:.1f}","平均风电 CF（区域平均）":"{:.3f}","最低日均风电 CF":"{:.3f}"})}
<p class="small">作比较：12 月 28 日至 1 月 6 日的多年平均需求 {R['clim_dem_late_dec_early_jan_GW']:.1f} GW，区域平均陆上风电 CF {R['clim_wind_late_dec_early_jan_CF']:.3f}；冬季（12–2 月）平均需求 {R['dem_winter_DJF_mean_GW']:.1f} GW。被丢掉的周落在冬季中间，其中 1984、1996 年末的风电 CF 低于这一多年平均。这些周内是否有事件，要等事件目录建立后用连续序列和 52 周窗口各算一遍才知道（todo C2e）。</p>

<h2 id="s10">10. 对研究的含义（Implication）</h2>
<ol>
<li><b>事件由风光变化和系统配置决定，需求主要提供季节与日历背景。</b>剩余负荷的变化主要来自风光（日距平标准差占均值 {vre_anom['onshore wind']:.0f}% 对 {100*R['dem_resid_doy_wd_std_GW']/R['dem_daily_mean_GW']:.0f}%）。按剩余负荷定义的事件仍然成立，但事件的“冬季集中”主要是风光季节性和需求日历的叠加，不要把它解释为低温驱动的高需求 [推断：由需求的日历占比 94% 和日距平标准差对比得出，未做归因检验]。</li>
<li><b>不能用“需求最大的日子”当极端天气日。</b>需求峰值是日历量（12 月 {dpk['day_min']}–{dpk['day_max']} 日，周三至周五，{dpk['hour_set'][0]}:00 GMT），年际几乎不变；先验加入最大需求日对本课题的事件识别没有天气信息（与 Hilbers 2023 的结论一致的方向，未在此核实）。</li>
<li><b>为什么 classic 需求不含电采暖、电动汽车、电转 X 和氢，影响是什么。</b>原因：这些负荷取决于系统的电气化程度，是模型要内生决定的量，不应预先写进输入的电力曲线；热需求单独给出、可调度，而 classic 电力被当作不可调 [Kruse 2023 §4.1]。影响：(1) 冬季没有热泵和电采暖用电，真实的 2050 年系统里这部分叠加在冬季晚间，会抬高冬季需求峰值；图 9c 显示热泵电量比热量更集中在冬季；(2) 低温与低风同时发生的事件在本数据的需求里体现不出来，事件会低估；(3) 年需求变异系数 0.15% 与气温几乎无关，电气化后需求才有明显的气温响应，也会改变 D4 里“需求的气候变化信号”；(4) 水电解、电动汽车是可调的，应当作灵活负荷处理，不是固定需求。这些都需要你决定是否加入（待办 A17）。<br>原条目：classic 需求不含电采暖、电动汽车、电转 X。低温时的电力需求增加（热泵、电采暖）不在其中；热需求和热泵性能系数在同一合集的 <code>heat_demand/</code>、<code>heat_pump_COP/</code>，要用电气化情景才能转成电力需求。要不要加、怎样加，决定了事件目录是否包含“冷+无风”型事件，需要你决定（待办 C2d、B3 的延伸）。</li>
<li><b>气候变化部分（Q4）</b>：classic 需求对气温的响应很弱，未来预估只能改变风光和水电；若需要需求的气候响应，必须另外建气温–需求模型，并保证历史与未来用同一方法。D4（需求和水电的气候变化信号比风光大）所指的气温响应主要在供热和制冷，不在 classic 需求里，要用热需求文件另行检验。</li>
<li><b>年需求几乎不变（变异系数 {d_cv:.2f}%）</b>：需求的年际变率在这套数据里被压低；与风光年均 CF 的变异系数 {R['E_annual_CV_onshore wind']:.1f}%（风）和 {R['E_annual_CV_PV']:.1f}%（光）相比可以忽略。含义：在年尺度上，剩余负荷的年际变化来自风光和水电。</li>
<li><b>技术和资源等级是情景选择。</b>同一区域 CF 从 RGA 到 RGC 变化约 {100*(R['rg_means_wind'][0]-R['rg_means_wind'][2])/R['rg_means_wind'][1]:.0f}%（相对 RGB），因此计划里的“系统配置情景”必须同时写明风光的技术和资源等级，结论要对这个选择做敏感性检验（U2）。</li>
<li><b>区域集</b>：以 {R['common_regions']} 个需求区域为公共集；水电只覆盖部分，其余区域的剩余负荷不含水电；德国只计一份；瑞士、希腊、巴尔干、爱尔兰有风光无需求，不进入事件目录。互联取各国合并时，要用独立的 {R['n_unique_demand']} 个区域。</li>
<li><b>水电时间分辨率</b>：周（水库式）和日（径流式）常数，事件识别里水电的小时变化是展开的结果；径流式水电在剩余负荷里给出的是日尺度的变化。</li>
<li><b>跨年冬季事件</b>：事件识别用连续序列，不用 Shubham 的 52 周窗口（第 9 节）；自助法按 4 月 1 日至次年 3 月 31 日的冬季完整年份分块（研究计划第 3 节）。</li>
<li><b>时期</b>：1982–2020，39 个天气年，需求文件限制了起点；风光和水电多出 1980–1981 年和 2021 年，可用于交叉检验但不进入事件目录。</li>
</ol>

<h2 id="s11">11. 尚未核实或需要决定的</h2>
<div class="warn"><ul>
<li>需求和水电来水的单位（readme 未写明）；风光装机量的来源（Mopo 2025 年区域装机与 Balmorel 区域的对应）。</li>
<li>DTU 文件的需求是否就是 Kruse 2023 论文中的 classic 电力需求，以及是否施加了年校正系数：论文附录 J.2 给出的 classic 校正系数多在 1.000 ± 0.01 以内（1982–2007 年的表），与本文件的年需求变异系数同量级，但这一对应没有核实。</li>
<li>热需求和热泵系数文件没有分析；电气化情景没有定。</li>
<li>水电来水数据（Liu & Rahmlow 2026）和风光验证论文（Nayak et al. 2025）没有读。</li>
<li>区域平均的风光是简单平均，没有按装机加权；多国事件的特征要按国家计算。</li>
<li>2020 年 12 月之后的数据（2021 年）不在统计窗口。</li>
</ul></div>

<h2 id="s12">12. 参考文献与读取范围</h2>
<ul class="small">
<li>Nayak S., Liu Y., Bahmani M., Olsen B.T., Amelin M., Koivisto M.J. (2026). Integrating long-term weather distributions into continental-scale energy system planning: impacts on adequacy and investment decisions. SSRN preprint, <a href="https://doi.org/10.2139/ssrn.7455543">doi:10.2139/ssrn.7455543</a>. [全文已读；§2.1、§2.2、§4.2、§5.2]</li>
<li>Nayak S., Koivisto M.J., Kanellas P. (2025). Pan-European weather dependent generation and demand time series for Balmorel energy system modelling. DTU Data collection, <a href="https://doi.org/10.11583/DTU.c.7964141">doi:10.11583/DTU.c.7964141</a>. [各数据项 readme 已读；数据本身已统计]</li>
<li>Kruse J.C.R. (2023). Resilience of weather dependent energy systems under extreme generation and demand scenarios. Master’s thesis, DTU. <a href="https://www.ea-energianalyse.dk/wp-content/uploads/2024/04/JensChrKruse_thesis.pdf">PDF</a>. [第 4 章、§6.1、附录 J.2 已读，其余未读]</li>
<li>Grochowicz A., Bloomfield H.C., Victoria M. (2025/2026). Preparing for the worst / Resilience metrics to guide back-up investments in the power system during extreme weather. arXiv:<a href="https://arxiv.org/abs/2508.05163">2508.05163</a>. [引言、讨论已读；用于“冬季事件多发于 11–2 月”]</li>
<li>Nayak S., Simutis E., Murcia Leon J.P., Olsen B.T., Koivisto M.J. (2025). Validation of European wind generation time series simulation. Applied Energy 402:126882, <a href="https://doi.org/10.1016/j.apenergy.2025.126882">doi:10.1016/j.apenergy.2025.126882</a>. [元数据已核对 Crossref；未读]</li>
<li>Ruhnau O., Hirth L., Praktiknjo A. (2019). Time series of heat demand and heat pump efficiency for energy system modeling. Scientific Data 6. <a href="https://doi.org/10.1038/s41597-019-0199-y">doi:10.1038/s41597-019-0199-y</a>. [元数据已核对；未读]</li>
<li>Hersbach H. et al. (2020). The ERA5 global reanalysis. Q. J. R. Meteorol. Soc. 146:1999–2049, <a href="https://doi.org/10.1002/qj.3803">doi:10.1002/qj.3803</a>. [元数据已核对；未读]</li>
<li>Liu Y., Rahmlow U.M. (2026). Mopo Pan-European Hydropower Data. Zenodo, <a href="https://doi.org/10.5281/zenodo.18632738">doi:10.5281/zenodo.18632738</a>. [引自 Nayak et al. 2026；未读]</li>
</ul>
<p class="small">图按项目的图规则绘制：图例在坐标框内、无边框，坐标轴有量和单位，字号小于正文，统计量标在图上；保存为 220 dpi。图中数值与文中数值来自同一次计算（<code>tables/results.json</code>）。</p>
</main></body></html>
"""
(OUT / "data_understanding.html").write_text(page, encoding="utf-8")
print("written", len(page))
