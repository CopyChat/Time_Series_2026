# 第 1 周：确定课题（2026-11-17 会议准备）

- 起草：2026-11-16。用于 2026-11-17 的讨论（与 Matti，或与 Shubham；Shubham 的细节问题见 [2026-11-11_Nayak2026_two-stage_adequacy_extremes.md §9](2026-11-11_Nayak2026_two-stage_adequacy_extremes.md)）。
- 依据：[2026-11-11_Nayak2026_two-stage_adequacy_extremes.md](2026-11-11_Nayak2026_two-stage_adequacy_extremes.md)（Nayak 精读、充裕度、文献排查），[2026-11-10_meeting_notes_and_plan.md](2026-11-10_meeting_notes_and_plan.md)（11-10 会议记录）。
- 待办统一放在 [todo.md](../todo.md)。
- 规则：每条说法注明出处和阅读范围；推断标 `[INFERENCE]`。

## 1. 会议要带走的三个决定

1. **课题定位**：是否认可"能随气候变化更新的能源极端事件数据集"（第 3 节）。
2. **基准数据**：能否拿到 Nayak 的 39 年输入、逐年成本排序和逐年 LOLE/EENS（[2026-11-11 §9 D1](2026-11-11_Nayak2026_two-stage_adequacy_extremes.md)）；未来气候用 PECD 4.2 还是 Mopo 预估。
3. **验证方式**：只用统计指标加已发表的模型结果做对照，还是 DTU 能用 Balmorel 或 PyPSA 跑一次。
4. **事件定义**（2026-11-16 加入）：用供需平衡一类（固定装机的剩余负荷、累计亏缺）定义事件，面向投资问题；系统定义事件只作验证。装机情景、参考供给水平、分析类型怎样定。背景见研究计划第 3 节"事件定义"和 [2026-11-16_event_definition_literature.md](2026-11-16_event_definition_literature.md)。

## 2. 一句话课题（英文，可直接念）

```
Nayak's two-stage framework reinforces the baseline on four extreme years chosen
by model cost, using historical weather only. I propose to build a weighted set of
energy extreme events (wind, solar, hydro inflow, demand; multi-country), defined
from the data alone, whose indicators map onto system needs (firm capacity,
storage energy, interconnection). I will check it once against published model
results (Nayak's cost and adequacy rankings, Grochowicz et al. 2026 system-defining
events), and test when a historical event set stops representing a warmer climate,
so that the set can be updated with climate projections.
```

## 3. 课题范围：能随气候变化更新的能源极端事件数据集

| 内容 | 说明 |
|---|---|
| 研究对象 | 风、光、水电来水和需求共同造成的多国、多日能源短缺事件，只用数据定义（研究计划 D6） |
| 做什么 | 事件识别 → 带权重的事件类型 → 在未来气候下的代表性检验 → 更新准则 |
| 检验 | 对照已发表的模型结果：Nayak 的成本和充裕度排序、Grochowicz 2026 的 SDE 清单；再看已知代表年子集（van Duinen 2026、ERAA25）中各类事件的频率是否与全部年份一致 |
| 与已有工作的关系 | 补上 Grochowicz 2026（只有历史 SDE，把变暖气候下的检验列为未来工作）和 van Duinen 2026（代表年，假定无趋势，承认极端需另外加权 [§5.1]）留下的部分 [INFERENCE] |

## 4. "只用统计"如何保住能源电力的讨论

思路：选的事件指标，每一个都对应一种系统需求。下表的对应关系是我的推断 [INFERENCE]，依据是 Grochowicz 2026 对功率缺口和能量缺口的区分 [Methods，full text]。

| 事件指标（只用数据就能算） | 对应的系统需求 | 对应 Grochowicz 2026 的事件类型 |
|---|---|---|
| 峰值剩余负荷（GW） | 可信容量、备用容量 | 功率缺口 / 严重功率缺口 |
| 事件期间累计能量亏缺（TWh） | 长时储能的电量 | 能量缺口 |
| 持续时间、两次事件的间隔 | 储能能否在两次事件之间充回 | 连锁事件 |
| 多国同时发生的程度 | 互联输电能否缓解 | 原文：系统影响的范围大于天气异常的范围 [图 5] |
| 季节、年尺度的累计亏缺 | 风光装机、水库调度（长时压力） | 原文的"long-term resilience" |

已有的支持证据：
- [2026-11-11 §10](2026-11-11_Nayak2026_two-stage_adequacy_extremes.md) 的先行检验：只用陆上风电容量因子，冬季平均最低的 3 年 = Nayak 成本最高的 3 年（1985、2010、1987，顺序不同）；最低 14 天滑动平均则对不上。样本很小，不能当结论。
- Grochowicz 2026：长时压力年份（总成本高）与"年均风光容量因子低、冬季负荷高"基本一致，例如 1962/63、1941/42 [§Short- vs. long-term，full text]。

反面证据（必须在课题里正面回应）：
- Hilbers et al. 2023：先验聚合中"加入每区域最大需求日和最小风日"的做法（方法 C）没有改善设计；原文："this heuristic appears unable to determine those events that truly drive installed capacities" [§4.5，full text，arXiv v1]。
- Grochowicz et al. 2024：系统定义事件与按缺电量识别的事件一致，但与只按净负荷选出的事件不同；"purely meteorological approaches fail to identify which events lead to the largest system stress … due to the influence of subtle transmission bottlenecks and storage issues across multiple regions" [摘要与 §3，full text]。
- 合起来的读法 [INFERENCE]：简单统计量对长时压力有效，对短时、多区域的功率缺口较弱。课题的方法贡献就放在后者：多变量、多国、按持续时间累积的统计描述，能找回多少。

## 5. 投资模型能用的最少时段：对数据聚合的要求

| 来源 | 模型能吃下的时间长度 | 阅读范围 |
|---|---|---|
| Nayak（Balmorel，泛欧、多部门） | 投资模型"能用的数据少于 1 年"；每年取代表日、3 小时分辨率（原文写 84 天，但按规则只有 24 天，待核实） | full text |
| Grochowicz 2026（PyPSA-Eur，90 节点） | 每次 1 个天气年、逐时；60 GB 内存，每年约 3 小时，80 年共 80 × 3 小时 | full text |
| van Duinen 2026 | 详细的电力系统模型通常只能用 1–30 个气候年；ERAA25 用 36 年；投资规划类研究约 5 年 | full text（预印本） |
| Hilbers 2023 | 30 年不聚合按外推需超过一年的求解时间；聚成 120 个代表日可解 | full text（预印本） |
| de Marco 2025（ZEN-garden） | 每个情景 8760 小时，随机优化中用 5 个代表年 | full text |

对本课题的要求 [INFERENCE]：
1. **预算**：交付的数据必须装进上面的规模，即每年几十到几百个代表日，或少数几个完整年份。
2. **格式**：带权重的代表期，或完整的连续年份（van Duinen 2026 用水文年，4 月 1 日到次年 3 月 31 日）。
3. **时序**：长时压力依赖储能和水库的连续演变，极端事件必须带着前后的连续时段一起交付，不能只给事件窗口（Grochowicz 2026；de Marco 2025 图 9 显示储氢在事件前要提前充满）。
4. **矛盾即动机**：极端统计量需要长记录，而模型只能吃短数据，这正是要做聚合的原因。

## 6. 讨论主题与问题清单（英文，可直接问）

| # | 问题 | 为什么问 |
|---|---|---|
| Q1 | Does a climate-updatable set of energy extreme events, defined from data only but checked against published model results, fit what DTU needs now? | 第 1 个决定 |
| Q2 | Could I get the 39-year inputs, the cost ranking of the 39 single-year optimisations and the yearly LOLE/EENS of the baseline? | 第 2 个决定；详见 2026-11-11 §9 D1 |
| Q3 | For future climate, PECD 4.2 (6 CMIP6 models × 4 SSPs) or the Mopo projections (2 models × 2 SSPs, wind and solar only)? Is there a demand model at DTU that I could apply to projected temperature? | 未来需求只能由预估气温推算（[06 §5](2026-11-11_Nayak2026_two-stage_adequacy_extremes.md)）；水电来水也要问 |
| Q4 | Is a statistics-only evaluation acceptable, or could someone run Balmorel or PyPSA once with my event set? | 第 3 个决定 |
| Q5 | Aleksander Grochowicz and Marta Victoria (DTU Wind and Energy Systems) list the re-evaluation of system-defining events in a warmer climate (CMIP7) as future work. Could you introduce me? Is anyone already working on it? | 避免重叠，并寻求合作 |
| Q6 | In the second stage of Nayak et al., are the extreme years represented by the same selected days or by the full year? (84 days in the text, 24 by the rule.) | 如果仍是固定日，极端年里真正的极端事件可能不在其中；详见 2026-11-11 笔记 §9 A1、A2 |
| Q7 | Target journal, and what is a realistic scope by 5 February 2027? | 时间线 |
| Q8 | I want to avoid running a power system model myself. My idea: each event indicator stands for one system need (peak residual load for firm capacity, cumulative energy deficit for storage energy, simultaneous occurrence across countries for interconnection), and the event set is checked once against published model results (Nayak's cost and adequacy rankings, the system-defining events of Grochowicz et al. 2026). Is this credible enough for an energy-system audience, or would reviewers require at least one model run? | 决定"只用统计"能否成立（第 4 节）；与 Q4 一起问 |

### 6.1 事件定义（2026-11-16 加入，对应第 4 个决定）

| # | 问题 | 为什么问 |
|---|---|---|
| Q9 | I will estimate the probability of energy extreme events (frequency, return period, change under climate change). System-defining events based on shadow prices cannot be compared across weather years, because each year has its own optimised system. I therefore plan to define events from residual load with one fixed capacity layout (cumulative deficit above a fixed reference supply level), and to use the system-defining events of Grochowicz et al. 2026 and Nayak's extreme years only for validation. Does this make sense to you? | 定义类别是整个课题的基础；理由见研究计划第 3 节 |
| Q10 | The study targets investment needs (firm capacity, storage energy, interconnection), not short-term peak operation. Is that the right focus for DTU's work? | 研究计划 D10，todo A12 |
| Q11 | Which fixed capacity layout would you use for the residual load: the Mopo 2025 regional layout scaled to two or three renewable shares, the Nayak baseline system, or a TYNDP/ERAA scenario? Should hydro reservoirs and existing dispatchable plants enter the reference supply level? | 剩余负荷和事件都依赖装机；历史与未来要用同一组装机 |
| Q12 | The analysis would stay in power quantities (GW, TWh), use meteorology to explain drivers and climate change, and compare with published costs only. Is that enough for an energy-system journal? | 分析类型；与 Q4、Q8 一起问 |
| Q13 | I listed concrete questions for three analyses (power quantities P1–P6, climate C1–C6, economics E1–E4; research plan section 2). Which ones matter most for DTU, and which can be left out within 12 weeks? | 定范围；问题清单见研究计划第 2 节"按分析类型列出的具体问题" |

## 7. 关于 Grochowicz 2026 的作者与数据

- 作者：**Aleksander Grochowicz**（通讯作者，DTU Wind and Energy Systems）、**Hannah C. Bloomfield**（Newcastle University）、**Marta Victoria**（DTU Wind and Energy Systems）。Nature Sustainability，DOI 10.1038/s41893-026-01897-6；读的是 arXiv v2（2026-06-08）。
- 2024 年那篇（ERL 19:054038）的作者：Aleksander Grochowicz、Koen van Greevenbroek、Hannah C. Bloomfield（按 PDF 首页核对，2026-11-16；PDF 已挂到 Zotero `PU99TUXJ`）。
- 数据和代码：Zenodo 10.5281/zenodo.20590389（CC-BY-4.0）；GitHub `aleks-g/stressed-system` v1.0。SDE 清单文件 `sde_new_store_1941-2021_100bn_12-336h_90_elec_lc1.25_Co2L.csv` 在 `results.tar.gz`（约 35 GB）里。可以先看 GitHub 仓库里是否另有这个文件，或者直接向作者要。
- 他们明确写的未来工作："Future work using these [CMIP7] runs will allow for benchmarking of the historical stress tests in a warmer climate"；"it remains to be seen whether frequency, severity or weather risks of SDEs will shift"。

## 8. 会后 1–2 周的先行检验

1. 把 [2026-11-11 §10](2026-11-11_Nayak2026_two-stage_adequacy_extremes.md) 的风电排序扩展到剩余负荷：加上光伏、海上风电，以及用气温推出的需求。
2. 改用水文年（4 月 1 日到次年 3 月 31 日），避免一个冬季被拆到两个年份。
3. 用第 4 节的指标识别多日事件，对照 Nayak 的极端年（拿到 D1 数据后对照全部 39 年的排序）和 Grochowicz 2026 的 SDE 清单（1982–2020 重叠的部分）。
4. 结果决定方法路线：
   - 统计排序能复现模型排序 → 走纯统计路线，方法往多变量、带权重、非平稳方向加深；
   - 不能复现 → 走统计预筛选加少量模型运行的混合路线。
