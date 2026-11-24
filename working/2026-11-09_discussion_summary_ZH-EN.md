# 讨论总结：欧洲能源与电力时间序列的统计代表性缩减 / Discussion summary: statistically representative reduction of European energy and electricity time series

- 日期 Date：2026-11-09；用于 2026-11-10 与 Matti Koivisto（DTU Wind and Energy Systems）的会面 / for the meeting with Matti Koivisto (DTU Wind and Energy Systems) on 2026-11-10
- 相关文件 Related files：`2026-10-15_topic_keywords_references.md`（25 篇 TSA 文献 / 25 TSA papers）、`01_research_plan.md`（研究计划第 3 版 / research plan v3）
- 标记 Labels：`[QUOTE]` 原文 / quoted from the source；`[INFERENCE]` 推断 / inference, basis stated；`[ASSUMPTION]` 假设 / assumption。阅读范围 Read scope：[full text] / [abstract only] / [snippet]（仅搜索摘要 / search snippet only）/ [not accessed]

---

## 1. 已形成的共识 / Points settled so far

| # | 中文 | English |
|---|---|---|
| D1 | 课题：多年代欧洲能源与电力时间序列的统计代表性缩减，范围包括需求、风光、水电来水、温度驱动负荷、电价、跨境潮流，不只是风光；目标是顶级期刊论文 | Topic: statistically representative reduction of multi-decade European energy and electricity time series (demand, wind, solar, hydro inflow, temperature-driven load, prices, cross-border flows), not only wind and solar; target: a top-tier journal paper |
| D2 | 缩减结果只用统计检验评估，不把能源系统优化模型放进评估环节 | The reduced series are judged by statistical tests only; no energy system optimisation model in the evaluation loop |
| D3 | 用途不限于 ML，包括规划、充裕度、气候影响、电网和 ML | Uses are not limited to ML: planning, adequacy, climate impact, grid studies and ML |
| D4 | 统计依据：分布距离（MMD、能量距离）小 ⇒ 一大类函数的期望误差小，与具体模型无关 [Gretton 2012；Mak & Joseph 2018，abstract only] | Statistical basis: a small distribution distance (MMD, energy distance) bounds the error of expectations of a broad class of functions, whatever the model [Gretton 2012; Mak & Joseph 2018, abstract only] |
| D5 | 已知反对意见：只看统计会漏掉系统应力最大的时段 [Grochowicz 2024]；只用指标评估缩减序列，可能造成很大误差 [Kotzur 2018a, full text] | Known objections: statistics alone miss the periods of highest system stress [Grochowicz 2024]; judging aggregated series by indicators alone can lead to large errors [Kotzur 2018a, full text] |
| D6 | 回应：加入与系统相关的统计量（剩余负荷、累计能量亏缺、多阈值干旱），这些量直接从时间序列算出，不需要优化模型；论文明确写出适用边界 | Answer: add system-relevant statistics (residual load, cumulative energy deficit, multi-threshold droughts), computed from the series without an optimisation model; state the scope limit in the paper |

---

## 2. 共用的数据、方法和统计检验组 / Shared data, methods and test battery

### 2.1 数据 / Data

| 数据 Data | 中文 | English |
|---|---|---|
| CorRES Mopo（Zenodo 2026, doi:10.5281/zenodo.17950648） | 逐时风电（陆上 9 种、海上 4 种技术）和光伏（3 种）；ERA5 + GWA；CC-BY-4.0；年份和分区页面未写明 | Hourly wind (9 onshore, 4 offshore technologies) and PV (3); ERA5 + GWA; CC-BY-4.0; years and zones not stated on the record |
| Mopo 气候预估 / Mopo projections（doi:10.5281/zenodo.18549865） | MPI-ESM1-2-HR、EC-Earth3 × SSP2-4.5/SSP5-8.5，2015–2100 逐时 | MPI-ESM1-2-HR, EC-Earth3 × SSP2-4.5/SSP5-8.5, hourly 2015–2100 |
| PECD 4.2（doi:10.24381/cds.f323c5ec） | 风光容量因子（风电由 CorRES 生成）、水电、温度；ERA5 1950 年起，6 个 CMIP6 模式 × 4 个 SSP；NUTS0、NUTS2、PEON、P2ON 分区 | Wind/solar capacity factors (wind by CorRES), hydro, temperature; ERA5 from 1950, 6 CMIP6 × 4 SSP; NUTS0, NUTS2, PEON, P2ON zones |
| CorRES_2026 Réunion | ERA5 + GWA2 风电，与 Mopo 同一模型链 | ERA5 + GWA2 wind, same model chain as Mopo |

### 2.2 统计检验组（不需要优化模型）/ Test battery (no optimisation model needed)

| 层 Layer | 中文 | English |
|---|---|---|
| L1 | 边缘分布：KS 统计量、Wasserstein W₁、持续曲线 NRMSE、P1/P99 | Marginal distributions: KS, Wasserstein W₁, duration-curve NRMSE, P1/P99 |
| L2 | 联合分布：能量距离、MMD（块置换检验） | Joint distribution: energy distance, MMD (block permutation test) |
| L3 | 时间结构：自相关（滞后 1–48 h）、爬坡分布、日内剖面 | Temporal structure: autocorrelation (lags 1–48 h), ramp distribution, diurnal profile |
| L4 | 空间同时性：相关矩阵误差、多区域同时低出力的频率 | Spatial co-occurrence: correlation-matrix error, frequency of simultaneous low output |
| L5 | 极端与累计亏缺：多阈值干旱的频率和时长、最大累计能量亏缺 | Extremes and cumulative deficit: multi-threshold drought frequency and duration, maximum cumulative energy deficit |
| L6 | 范围覆盖：子集覆盖的全集合年际指标范围所占比例 | Envelope coverage: share of the full-set range of annual indices covered by the subset |

```
 能量距离 / Energy distance:
   E(P, Q) = 2·E‖X − Y‖ − E‖X − X'‖ − E‖Y − Y'‖ ≥ 0,   = 0 当且仅当 / if and only if P = Q

 剩余负荷与最大累计亏缺 / Residual load and maximum cumulative deficit:
   r_t = d_t − ( a·w_t + b·s_t )
                       t₂
   D_max  =   max      Σ  r_t
            t₁ < t₂   t=t₁

 年际持续性下的有效样本量 / Effective sample size under inter-annual persistence (AR(1)):
                  1 − ρ₁
   n_eff  =  n · ────────
                  1 + ρ₁

 所需子集大小 / Required subset size:
   k*(L, 区域 region) = min { k : 所需各层统计量都低于阈值 / all required layers below threshold }
```

`[ASSUMPTION]` a、b 取使长期平均 VRE 发电等于平均需求；这是本计划的设定，文献里没有查到。/ a and b are set so that mean VRE output equals mean demand; this is a choice of this plan, not taken from the literature.

### 2.3 选择方法 / Selection methods【稍后讨论 / to be discussed later】

| 中文 | English |
|---|---|
| 随机（基准）；TMY 式逐月拼接（Finkelstein–Schafer）；k-medoids（TYNDP 做法）；模拟退火最小化季节切片 Wasserstein 距离（van Duinen 2026）；KKZ 范围覆盖（Cannon 2015）；support points（Mak & Joseph 2018）；以上方法加入极端时段 | Random (baseline); TMY-style monthly composite (Finkelstein–Schafer); k-medoids (TYNDP practice); simulated annealing on seasonal sliced Wasserstein distance (van Duinen 2026); KKZ envelope (Cannon 2015); support points (Mak & Joseph 2018); each with added extreme periods |
| 选择单元长度 L ∈ {1 天, 1 周, 1 个月, 1 个水文年} | Period length L ∈ {1 day, 1 week, 1 month, 1 hydrological year} |

---

## 3. DTU 可能的用途：逐项详解 / Possible uses at DTU, one by one

以下"预期结果"都是**待检验的假设**，不是已有结果。优先级要由 Matti 确认。
The "expected results" below are **hypotheses to test**, not findings. Priorities are to be confirmed by Matti.

### U1. Balmorel 欧洲容量扩展规划 / Balmorel pan-European capacity expansion

| 项目 Item | 中文 | English |
|---|---|---|
| 背景与证据 Evidence | pybalmorel 有基于 tsam 的 TSA 模块（contiguous、averaging、kmeans），文档写明"正在开发和测试"[pybalmorel 文档页] | pybalmorel has a tsam-based aggregation module (contiguous, averaging, kmeans); the documentation says it is "under development and being tested" [pybalmorel docs] |
| 数据 Data | CorRES Balmorel 数据（2025）或 Mopo；NUTS0 或 Balmorel 区域；多个天气年 | CorRES Balmorel data (2025) or Mopo; NUTS0 or Balmorel regions; multiple weather years |
| 方法 Method | 对 pybalmorel 现有的三种选项和 2.3 节的方法做统计比较；输出 Balmorel 格式的季节（S）与时段（T） | Compare the three current pybalmorel options with the methods of §2.3 statistically; output seasons (S) and terms (T) in Balmorel format |
| 预期目标 Goal | 给 Balmorel 用户一条有依据的规则：几个季节、多长时段、加不加极端期 | A documented rule for Balmorel users: how many seasons, which period length, whether to add extreme periods |
| 预期结果 Expected results | 只按分布选的 S/T 组合 L1 误差小，但 L5（累计亏缺）误差大；加入极端期后 L5 改善 | Distribution-only S/T choices give small L1 error but large L5 (cumulative-deficit) error; adding extreme periods improves L5 |
| 验证 Validation | 留出年检验：在未参与选择的天气年上重算 L1–L6；不同随机种子重复 25 次 | Held-out years: recompute L1–L6 on weather years not used in the selection; 25 repetitions with different seeds |
| 关键层 Key layers | L1、L3、L5 | L1, L3, L5 |

### U2. Mopo 泛欧规划平台与 SpineOpt / Mopo pan-European planning platform and SpineOpt

| 项目 Item | 中文 | English |
|---|---|---|
| 背景与证据 Evidence | Mopo 是 Horizon Europe 项目（2023–2026，VTT 牵头，DTU 参与），目标是"时间、空间、技术表达高度灵活"的规划工具，以及逐时、NUTS2 的泛欧数据集 [CORDIS 101095998] | Mopo is a Horizon Europe project (2023–2026, led by VTT, DTU a partner) aiming at a planning tool with "highly flexible representation of temporal, spatial and technological aspects" and an hourly, NUTS2-capable pan-European data set [CORDIS 101095998] |
| 数据 Data | CorRES Mopo 数据（陆上 9 种 + 海上 4 种 + 光伏 3 种技术） | CorRES Mopo data (9 onshore + 4 offshore + 3 PV technologies) |
| 方法 Method | 多技术、多区域的联合缩减：同一子集要同时代表所有技术和区域；检验 L2、L4 | Joint reduction across technologies and regions: one subset must represent all of them; test L2 and L4 |
| 预期目标 Goal | 随 Mopo 数据发布一个"代表性子集 + 检验报告"，作为数据产品的一部分 | Release a representative subset with its test report as part of the Mopo data product |
| 预期结果 Expected results | 技术之间（陆上、海上、光伏）的相关结构使所需的 k 大于单技术的情形 | Correlation between technologies (onshore, offshore, PV) makes the required k larger than for a single technology |
| 验证 Validation | 对每种技术和每个区域分别检验；在 NUTS0 和 NUTS2 两级比较 | Test per technology and per region; compare NUTS0 and NUTS2 levels |
| 关键层 Key layers | L2、L4 | L2, L4 |

### U3. PECD 与 ENTSO-E 充裕度评估中的气候年选择 / Climate-year selection for PECD and ENTSO-E adequacy

| 项目 Item | 中文 | English |
|---|---|---|
| 背景与证据 Evidence | PECD 4.2 的风电和 CSP 序列由 CorRES 生成 [CorRES open-data 页面]。ERAA 2025 用 Wasserstein 距离选情景子集 [snippet]。van Duinen 2026 认为现行选年做法没有按明确的代表性准则验证过 [摘自原文] | PECD 4.2 wind and CSP series are made with CorRES [CorRES open-data page]. ERAA 2025 picks scenario subsets by Wasserstein distance [snippet]. van Duinen 2026 states that current climate-year selections have not been validated against explicit representativeness criteria [from the text] |
| 数据 Data | PECD 4.2 历史（ERA5 1950 年起）和预估；剩余负荷要有需求序列（PECD 温度—需求关系） | PECD 4.2 historical (ERA5 from 1950) and projections; residual load needs demand (PECD temperature–demand relation) |
| 方法 Method | 在 van Duinen 的分布准则上加入 L3、L5、L6；比较 ERAA、TYNDP、模拟退火和本框架选出的子集 | Add L3, L5, L6 to van Duinen's distribution criterion; compare subsets from ERAA, TYNDP, simulated annealing and this framework |
| 预期目标 Goal | 一套可以直接给 ENTSO-E 和 TSO 使用的多准则选年方法 | A multi-criterion year-selection method that ENTSO-E and TSOs can apply |
| 预期结果 Expected results | 按分布最优的子集低估最长干旱和最大累计亏缺 [依据：Ruhnau & Qvist 2022 的最大亏缺跨越 9 周；Kittel & Schill 2026 的干旱跨年] | Distribution-optimal subsets underestimate the longest droughts and the maximum cumulative deficit [basis: maximum deficit spanning 9 weeks in Ruhnau & Qvist 2022; droughts crossing year boundaries in Kittel & Schill 2026] |
| 验证 Validation | 与全序列的干旱目录和 D_max 比较；按水文年和日历年两种切法重复 | Compare with the full-set drought catalogue and D_max; repeat with hydrological and calendar years |
| 关键层 Key layers | L5、L6、L2 | L5, L6, L2 |

### U4. 气候变化影响 / Climate change impact

| 项目 Item | 中文 | English |
|---|---|---|
| 背景与证据 Evidence | Mopo 提供 2015–2100 逐时预估；Koivisto、Nayak、Kanellas 报告泛欧风电的气候变化影响为低到中等 [WISO25 摘要]；Craig 2022 呼吁建立面向能源系统的气候数据集 | Mopo provides hourly projections 2015–2100; Koivisto, Nayak and Kanellas report a low-to-moderate climate-change impact on pan-European wind [WISO25 abstract]; Craig 2022 calls for energy-system-tailored climate data sets |
| 数据 Data | Mopo 预估（2 模式 × 2 SSP），PECD 4.2 预估（6 模式 × 4 SSP） | Mopo projections (2 models × 2 SSP), PECD 4.2 projections (6 models × 4 SSP) |
| 方法 Method | ① 用历史数据选出的子集，计算它与 2041–2070 年预估的分布距离；② 用 KKZ（Cannon 2015）选出覆盖模式离散范围的子集，与分布匹配的子集比较 | ① Distance between a historically selected subset and 2041–2070 projections; ② KKZ subsets covering the model spread (Cannon 2015) compared with distribution-matching subsets |
| 预期目标 Goal | 回答"选出的代表年能否沿用到未来"，以及做风险研究时应选哪种代表性 | Answer whether historical representative years remain valid in the future, and which representativeness to use for risk studies |
| 预期结果 Expected results | 风电变化小，所以子集基本可以沿用；光伏和需求变化较大，需要重新选择 `[INFERENCE]`，依据是 WISO25 摘要（仅风电） | Wind changes little, so subsets largely transfer; PV and demand change more and need re-selection `[INFERENCE]`, basis: WISO25 abstract (wind only) |
| 验证 Validation | 模式间留一交叉验证：在 5 个模式上选，在第 6 个模式上检验 | Leave-one-model-out: select on 5 models, test on the 6th |
| 关键层 Key layers | L6、L1、L2 | L6, L1, L2 |

### U6. 平衡与预测误差 / Balancing and forecast errors

| 项目 Item | 中文 | English |
|---|---|---|
| 背景与证据 Evidence | CorRES 生成一致的风光出力和预测误差序列，分辨率可到分钟 [Koivisto 2019，abstract only]；关心爬坡和高出力分布时，建议加入随机波动和停机模拟 [Nayak 2025，abstract only] | CorRES produces consistent generation and forecast-error series down to minutes [Koivisto 2019, abstract only]; stochastic fluctuations and unavailability are advised when ramps and high-output distributions matter [Nayak 2025, abstract only] |
| 数据 Data | CorRES 亚小时序列和预测误差序列（需 DTU 内部数据） | CorRES sub-hourly and forecast-error series (DTU internal) |
| 方法 Method | 把 L3 扩展到 5–15 分钟爬坡和预测误差的分布；比较逐时平均后再选与直接按亚小时选两种做法 | Extend L3 to 5–15 min ramps and forecast-error distributions; compare selection after hourly averaging with selection at sub-hourly resolution |
| 预期目标 Goal | 确定备用和平衡研究需要多少天、哪些天的亚小时数据 | Determine how many and which days of sub-hourly data reserve and balancing studies need |
| 预期结果 Expected results | 逐时代表性好的子集，亚小时爬坡尾部仍有偏差 | Subsets that are representative hourly still miss the tails of sub-hourly ramps |
| 验证 Validation | 比较亚小时爬坡的 P99 和 P99.9；在留出月份上检验 | Compare P99 and P99.9 of sub-hourly ramps; test on held-out months |
| 关键层 Key layers | L3 | L3 |

### U7. 电网与概率潮流 / Grid and probabilistic power flow

| 项目 Item | 中文 | English |
|---|---|---|
| 背景与证据 Evidence | Dalton、Bekker、Koivisto 2021：按大气状态聚类出的运行场景，比不聚类的基准状态更能减少概率潮流的模拟不确定性（南非 11 个风电场）[abstract only] | Dalton, Bekker and Koivisto 2021: operating scenarios clustered by atmospheric state reduce simulation uncertainty in probabilistic power flow versus an unclustered base state (11 wind farms, South Africa) [abstract only] |
| 数据 Data | 站点或 NUTS2 级风光；电网节点映射 | Site or NUTS2 wind and solar; mapping to grid nodes |
| 方法 Method | 以 L4（空间同时性）为主要准则选运行状态；与天气型（van der Wiel 2019 ERL）和 targeted circulation types（Bloomfield 2020）比较 | Select operating states mainly on L4; compare with weather regimes (van der Wiel 2019 ERL) and targeted circulation types (Bloomfield 2020) |
| 预期目标 Goal | 给电网研究一组保留空间相关的代表状态 | A set of representative states that keeps spatial dependence for grid studies |
| 预期结果 Expected results | 按天气型分组不足以代表极端短缺，因为每种天气型里都会出现极端 [van der Wiel 2019 ERL，abstract only] | Grouping by weather regime does not capture extreme shortfall, since extremes occur in every regime [van der Wiel 2019 ERL, abstract only] |
| 验证 Validation | 相关矩阵误差、多节点同时低出力的频率 | Correlation-matrix error, frequency of simultaneous low output at several nodes |
| 关键层 Key layers | L4、L2 | L4, L2 |

### U8. ML 代理模型的训练和验证 / ML surrogate training and validation

| 项目 Item | 中文 | English |
|---|---|---|
| 背景与证据 Evidence | Quick et al. 2024（DTU）用多输出支持向量回归作欧洲电价代理模型 [abstract only]；Gaugl et al. 2026 的欧洲潮流代理模型只用 2009 一个气候年训练 [snippet] | Quick et al. 2024 (DTU): multi-output SVR surrogate for European prices [abstract only]; Gaugl et al. 2026 trained a European flow surrogate on climate year 2009 only [snippet] |
| 数据 Data | 用作代理模型输入的 CorRES 序列 | CorRES series used as surrogate inputs |
| 方法 Method | 按 L2 和 L6（覆盖）选训练集，按整年留出验证集（块交叉验证，Roberts 2017）；与随机选择和单年选择比较 | Training sets chosen on L2 and L6 (coverage); validation by held-out whole years (block cross-validation, Roberts 2017); compare with random and single-year choices |
| 预期目标 Goal | 给代理模型提供一条选训练年和验证年的统计准则 | A statistical rule for choosing training and validation years for surrogates |
| 预期结果 Expected results | 按准则选的训练集在极端时段上样本外误差更低 | Criterion-based training sets give lower out-of-sample error in extreme periods |
| 验证 Validation | 只用 ML 模型本身的样本外误差，不用能源模型 | Out-of-sample error of the ML model itself, no energy model |
| 关键层 Key layers | L2、L6 | L2, L6 |

`[INFERENCE]` 依据现有材料，U1、U3 的证据最直接：Balmorel 正在开发 TSA，PECD 选年直接服务 ENTSO-E。（原 U5 HyDesign 已删除：它属于另一个研究项目，2026-11-09）
`[INFERENCE]` Based on the material at hand, U1 and U3 have the most direct evidence: Balmorel is building TSA, and PECD year selection serves ENTSO-E directly. (Former U5 HyDesign removed: it belongs to a separate research project, 2026-11-09)

---

## 4. 岛屿弱电网是否也需要聚合？问题是否和大陆一样？/ Do weak island grids also need aggregated data? Is the problem the same as on the continent?

### 4.1 简短回答 / Short answer

**中文**：需要，但原因和关键统计量不同。统计框架可以通用，瓶颈、主导时间尺度、数据来源和规划准则都不同。所以"同一框架在大陆和岛屿上给出不同的结果"本身就是一个可以发表的问题。

**English**: Yes, but for different reasons and with different key statistics. The statistical framework carries over; the bottleneck, the dominant time scales, the data source and the planning criteria differ. That contrast is itself a publishable question: one framework, different answers for continent and island.

### 4.2 岛屿为什么也需要缩减 / Why islands also need reduction

| # | 中文 | English | 依据 Evidence |
|---|---|---|---|
| R1 | **运行约束让模型变重**：机组组合、备用、频率和惯量约束，以及 15 分钟分辨率 | **Operational constraints make models heavy**: unit commitment, reserves, frequency and inertia constraints, 15-min resolution | Psarros & Papathanassiou 2023（综述，含频率动态）；Liu et al. 2024（数据驱动的频率最低点约束机组组合）；Rajabdorri et al. 2021（频率指标纳入短期调度的可行性）[abstract/snippet] |
| R2 | **小时内变率影响结果**：考虑小时内净负荷变化后，El Hierro 的调度弃风明显减少 | **Intra-hour variability matters**: accounting for intra-hourly net-demand variability changes El Hierro schedules and lowers wind curtailment | Fernández-Muñoz & Pérez-Díaz 2021（两阶段随机 MILP）[abstract + snippet] |
| R3 | **反方向的缩减**：0.25° 再分析分辨不出岛屿地形，需要 km 级降尺度，但只算得起几年。要问的是算哪几年，以及已有几年是否代表长期气候 | **Reduction in the other direction**: 0.25° reanalysis cannot resolve island relief, km-scale downscaling is affordable for only a few years. The questions are which years to simulate and whether those years represent the long-term climate | ERA5 在复杂地形中低估风速 [snippet，非岛屿专门研究]；`[INFERENCE]` |
| R4 | **储能决定设计时，需要保留时间顺序** | **Storage-driven design needs chronology** | Kotzur 2018a [full text]：孤立区域系统（光伏、风电、氢和电池储能，备用 ≤ 10% 需求）"即使 72 个典型日也看不到稳健收敛"；原因是"典型期相互独立，不能交换能量"[QUOTE] |

**注意 Note**：Kotzur 2018a 的"island system"是概念性的孤立区域系统，不是真实岛屿；不收敛的原因是储能和时段独立，不是岛屿本身。The "island system" of Kotzur 2018a is a conceptual isolated regional system, not a real island; the non-convergence comes from storage and independent periods, not from islandness itself.

### 4.3 与大陆的异同 / Similarities and differences

| 方面 Aspect | 大陆 Continent | 岛屿 Island | 依据 Evidence |
|---|---|---|---|
| 计算瓶颈 Bottleneck | 节点多、几十年 → 优化模型太大 / many nodes, decades → model too large | 节点少，但运行约束多、分辨率细 / few nodes, but detailed operational constraints and fine resolution | Fernández-Muñoz & Pérez-Díaz 2021；Grochowicz 2023（41 年、3 小时已接近计算极限 / 41 years at 3-hourly is at the limit） |
| 数据瓶颈 Data | 长序列现成 / long series available (ERA5, PECD) | 需要降尺度，只有几年 / downscaling needed, few years | `[INFERENCE]` |
| 空间平滑 Spatial smoothing | 大陆尺度，可跨国 / continental, cross-border | **存在但范围小**：Réunion 全岛分散布置光伏几乎消除天气造成的波动；Guadeloupe 小时内灵活性需求按最大单个电站算约 60 MW，计入空间平滑后约 26 MW / **present but over a small area**: island-wide PV dispersion on Réunion almost removes weather-driven variability; Guadeloupe intra-hour need about 60 MW at single-plant behaviour versus about 26 MW with smoothing | Tapachès 2019 [abstract]；David 2014 [abstract]；EDF SEI 2023 幻灯片 / slides [snippet] |
| 天气尺度事件 Synoptic events | 可通过互联缓解，但效果有限 / partly buffered by interconnection, limited | 全岛同时受影响（多日低风、热带气旋）/ whole island hit at once (multi-day low wind, cyclones) | `[INFERENCE]`；van der Wiel 2019 RSER：大陆上空间分散布局也不能消除极端事件 / spatial spreading does not prevent extreme events even on the continent |
| 主导时间尺度 Time scales | 数周的 Dunkelflaute、跨年累计亏缺 / multi-week droughts, cross-year deficit | 分钟到小时级爬坡、数日事件 / minute-to-hour ramps, multi-day events | Ruhnau & Qvist 2022；Kittel & Schill 2026；Fernández-Muñoz 2021 |
| 空间分辨率的影响 Effect of resolution | 区域加总后更容易缩减 / regional aggregates are easier to reduce | 单点或小区域更难 / single sites and small areas are harder | Kotzur 2018a [full text]：区域序列比单点序列更容易聚合 / regional series aggregate more easily than single locations；Reichenberg & Hedenus 2022：系统成本用 10 个代表日就能达到约 5% 偏差，但区域装机组合即使 250 个代表日偏差仍 > 50% [snippet] |
| 规划准则 Planning criterion | 分布匹配（ERAA、van Duinen）/ distribution matching | 最坏年或稳健设计（La Gomera，20 年海洋气象数据）/ worst case or robust design (La Gomera, 20 years of metocean data) | Giorcelli et al. 2026 [abstract] |
| 气候预估 Projections | PECD、Mopo 现成 / PECD and Mopo ready | 文献很少（Azores 研究只用 3 个 CMIP6 模式）/ sparse (an Azores study uses only 3 CMIP6 models) | Meirelles et al. 2022 [abstract + snippet] |
| 最重要的检验层 Key layers | L2、L4、L5（长时段 / long duration） | L3（亚小时 / sub-hourly）、L5（短时段 / short duration）、L6 | `[INFERENCE]` |

### 4.4 欧洲境内的岛屿算例 / Island cases inside Europe

| 岛屿 Island | 中文 | English | 来源 Source |
|---|---|---|---|
| Bornholm（丹麦 / Denmark） | DTU PowerLabDK 的全尺度测试系统；约占丹麦面积、人口和能耗的 1%；通过海底电缆与瑞典相连，可孤岛运行；约 28 000 用户，峰值 55 MW；有 1 s 分辨率量测 | DTU PowerLabDK full-scale test system; about 1% of Denmark's area, population and energy use; submarine cable to Sweden, can run islanded; about 28,000 customers, 55 MW peak; 1 s measurements | DTU Wind 网页、PowerLabDK 单页 [snippet] |
| Corse、Sardegna、Sicilia、Kriti、Illes Balears | NUTS2 区域，可从 PECD 4.2 的 NUTS2 聚合中取出（是否在数据范围内未核实） | NUTS2 regions, available from PECD 4.2 NUTS2 aggregation (coverage not verified) | PECD 4.2 CDS 页面 |
| Malta、Cyprus | 国家级（NUTS0） | Country level (NUTS0) | 同上 / same |
| El Hierro、La Gomera（加那利 / Canary） | 运行和规划的文献案例 | Literature cases for operation and planning | Fernández-Muñoz 2021；Giorcelli 2026 |
| Samsø、Orkney、Madeira | 岛屿转型路径比较 | Comparison of island transition pathways | Marczinkowski et al. 2019 [abstract] |

---

## 5. 研究动机：为什么要缩减？/ Motivation: why reduce at all?

**中文**：动机有四种可能，作用不同。算力不足是直接起因；数据冗余是可以利用的条件；科学问题是"对某个用途来说，什么是必要的"；岛屿上还有反方向的问题：数据不够，需要决定生产哪些数据。

**English**: There are four candidate motivations, playing different roles. Limited compute is the trigger; redundancy is the lever; the scientific question is what is necessary for a given use. On islands there is also the reverse case: too little data, so one must decide which data to produce.

| # | 动机 Motivation | 中文 | English | 证据 Evidence | 判断 Verdict |
|---|---|---|---|---|---|
| M-a | 数据太多（存储、读写）/ Too much data (storage, I/O) | Mopo 两个压缩包分别为 1.6 GB 和 12.6 GB（2026-11-10 修正：原写的 296 GB、581 GB 是 Zenodo 的累计下载量统计，不是数据大小）；PECD 4.2 为 6 模式 × 4 SSP × 85 年 × 多级分区 | The Mopo archives are 1.6 GB and 12.6 GB zipped (corrected 2026-11-10: the 296 GB and 581 GB first quoted are Zenodo download statistics, not data size); PECD 4.2 is 6 models × 4 SSP × 85 years × several zone levels | Zenodo 记录 / records；CDS 页面 / page | 真实但次要：存储便宜，单靠它不足以成为科学问题 / Real but secondary: storage is cheap; not a scientific question on its own |
| M-b | 算力不够 / Not enough compute | 下游模型吃不下全部数据：欧洲模型用 41 年、3 小时分辨率已接近计算极限；岛屿调度加入频率约束后计算时间高 | Downstream models cannot take all of it: a European model with 41 years at 3-hourly is at the limit of feasibility; island scheduling with frequency constraints is slow | Grochowicz 2023 [full text]；Fernández-Muñoz & Pérez-Díaz 2021 [abstract]（2026-11-10：Psarros 2023 只见搜索摘录，不再用于支撑此句） | **直接起因** / **The trigger** |
| M-c | 排除非必要数据（冗余）/ Remove what is not needed (redundancy) | 多年代逐时数据高度冗余：日循环和季节循环每年重复，PCA 有效维数远小于名义维数。缩减就是去掉冗余、保留用途所需的信息；"所需"取决于用途 | Multi-decade hourly data are highly redundant: the diurnal and seasonal cycles repeat every year, and the PCA effective dimension is far below the nominal one. Reduction removes redundancy and keeps what the use needs; "what is needed" depends on the use | Pfenninger 2017（#6，多年代数据的时间步缩减 / time-step reduction of multi-decade data）；`[INFERENCE]` 有效维数的论断待用数据验证 / the effective-dimension claim is to be checked on the data | **科学核心** / **Scientific core** |
| M-d | 数据不够（岛屿）/ Too little data (islands) | km 级降尺度很贵，只能算几年；要选生产哪几年，并判断已有几年是否代表长期气候 | km-scale downscaling is expensive, so only a few years are run; one must choose which years to produce and judge whether existing years represent the long-term climate | `[INFERENCE]`；ERA5 在复杂地形中低估风速 [snippet] / ERA5 underestimates wind in complex terrain [snippet] | 岛屿特有，是方法的第二个出口 / Island-specific; a second outlet for the method |

**结论 Conclusion**

- **中文**：论文的动机应写成：*算力限制迫使缩减（M-b），数据冗余使缩减可行（M-c），而缩减到什么程度才"足够"，目前没有一个与具体模型无关、带误差保证的准则*。这正好是数据处理方法的问题，见第 6 节。
- **English**: The motivation should read: *compute limits force reduction (M-b), redundancy makes it possible (M-c), but there is no model-independent criterion, with an error guarantee, for when a reduction is "sufficient"*. That is a data-processing method question; see §6.

---

## 6. 方法创新的定位（CNU section 61）/ Positioning the method contribution (CNU section 61)【稍后讨论；2026-11-10 会面不讲 / to be discussed later, not at the 10 Nov meeting】

**中文**：section 61（信息、自动化与信号处理）的顶刊论文要求数据处理方法上的创新，不能只是把已有方法用在新数据上。下面把课题定位为一个**方法问题**：*在路径空间上对多变量气候—能源时间序列做分布压缩，并按用途给出误差保证*。

**English**: For CNU section 61 (computer science, control, signal processing), a top-journal paper needs a new data-processing method, not an existing method applied to new data. The topic is therefore posed as a **method problem**: *distribution compression of multivariate climate–energy time series on path space, with use-specific error guarantees*.

### 6.1 现有方法的局限 / Limits of current methods

| 现有方法 Existing | 局限 Limit (中文) | Limit (English) | 来源 Source |
|---|---|---|---|
| k-means、k-medoids、层次聚类（tsam、pybalmorel、TYNDP）/ clustering | 按欧氏距离把每天当作独立向量，没有分布意义上的误差界；聚类偏向高密度区，丢掉极端 | Treats each day as an independent vector under Euclidean distance; no distributional error bound; biased to high-density regions, loses extremes | Cannon 2015；Teichgraeber 2022（#2） |
| 季节切片 Wasserstein + 模拟退火 / seasonal sliced Wasserstein + SA | 用日均值，丢掉日内和跨日的时间结构；只选整年 | Daily means drop intra-day and multi-day temporal structure; selects whole years only | van Duinen 2026（部分原文 / partial full text） |
| TMY（Finkelstein–Schafer）| 逐变量、逐月比较边缘分布，月份拼接破坏连续性 | Per-variable, per-month marginal comparison; monthly splicing breaks continuity | Finkelstein & Schafer 1971；ISO 15927-4 |
| 场景缩减（Kantorovich/Fortet-Mourier 距离）/ scenario reduction | 为随机规划设计，度量定义在情景向量上，不针对长时间序列的路径结构 | Built for stochastic programming; metric on scenario vectors, not on the path structure of long series | Dupačová 2003；Heitsch & Römisch 2003（[not accessed]，据标题和 TLDR / title and TLDR only） |
| Support points、kernel herding、kernel thinning | 统计学和 ML 中最先进的分布压缩，有误差界；但针对的是独立点，不是带时间顺序、跨尺度、需要保留尾部的路径 | State-of-the-art distribution compression with error bounds, but for i.i.d. points, not for ordered, multi-scale paths whose tails must be kept | Mak & Joseph 2018；Chen 2010；Dwivedi & Mackey 2021；Riabiz 2022 [abstract only] |
| Signature 核 / signature kernel | 能比较随机过程的分布（路径空间上的 MMD），但已有应用在金融生成模型和预测评估 | Compares laws of stochastic processes (MMD on path space); existing uses are financial generative models and forecast evaluation | Király & Oberhauser 2019；Chevyrev & Oberhauser 2018；Salvi 2021；Alden 2025 [abstract only] |

**空白 Gap**：两次检索（OpenAlex，以及 2026-11-09 的扩展网页检索）都没有找到把 signature 核 MMD、kernel thinning 或 support points 用于选择能源代表期或天气年的研究。这不是穷尽检索，需在 Scopus 和 Web of Science 中复查。
Two searches (OpenAlex and an extended web search, 2026-11-09) found no work that uses signature-kernel MMD, kernel thinning or support points to select representative energy periods or weather years. The searches were not exhaustive; to be re-checked in Scopus and Web of Science.

### 6.2 拟提出的方法 / Proposed method

```
 输入 Input:   X = {x_1, …, x_n}，每个 x_i 是长度为 L 的多变量路径 / each x_i a multivariate path of length L
               (风、光、需求，多区域 / wind, PV, demand, several regions)
 输出 Output:  加权子集 / weighted subset  S = {(x_j, w_j)}, |S| = k ≪ n,  Σ w_j = 1

 目标 Objective (path-space MMD with signature kernel k_sig):
   S* = argmin  MMD²_k_sig ( P_n , Σ_j w_j δ_{x_j} )  +  λ · R_tail(S)
          S, w

   P_n     = 全集合的经验分布 / empirical law of the full set
   R_tail  = 尾部惩罚：剩余负荷和累计亏缺的超阈值分布（GPD 参数或高分位数）的偏差
             tail penalty: mismatch of the exceedance distribution (GPD parameters or high quantiles)
             of residual load and cumulative deficit

 误差保证 Guarantee (Gretton 2012, reproducing property):
   对 RKHS 单位球内任意 f / for any f in the RKHS unit ball:
   | E_P[f(X)] − Σ_j w_j f(x_j) |  ≤  MMD_k_sig ( P_n , S )
   → 一个数就给出"对一整类用途"的误差上界 / one number bounds the error for a whole class of uses
```

| 方法要素 Component | 中文 | English | 新在哪里 What is new |
|---|---|---|---|
| C1 路径空间准则 / path-space criterion | 用 signature 核 MMD 比较整段路径的分布，同时包含日内结构、爬坡和跨日持续性 | Signature-kernel MMD compares laws of whole paths, covering diurnal structure, ramps and multi-day persistence | 代替日均值的 SWD 和手工统计量 / replaces daily-mean SWD and hand-picked statistics |
| C2 压缩算法 / compression algorithm | 在路径空间上做 kernel herding 或 kernel thinning，带权重 | Kernel herding or kernel thinning on path space, with weights | 已有算法针对独立点；本课题扩展到路径和块结构 / existing algorithms target i.i.d. points; here extended to paths and block structure |
| C3 尾部与持续性约束 / tail and persistence constraint | 加入极值理论约束，并按年块处理年际持续性（n_eff） | Extreme-value constraint plus year blocks for inter-annual persistence (n_eff) | 现有分布压缩不保证尾部 `[INFERENCE]` / existing compression does not guarantee tails `[INFERENCE]` |
| C4 误差证书 / error certificate | 每个子集给出 MMD 值及其对应的误差上界；块置换检验给出 p 值 | Each subset comes with its MMD value, the implied error bound and a block-permutation p-value | 把"代表性"变成可报告、可检验的数 / turns "representativeness" into a reportable, testable number |
| C5 多尺度 / multi-scale | 小波或多分辨率分解；不同尺度用不同长度的路径（岛屿用分钟到小时，大陆用周） | Wavelet or multiresolution decomposition; path length by scale (minutes–hours for islands, weeks for the continent) | 一个框架同时适用于大陆和岛屿 / one framework for continent and island |

**风险 Risks**
- **中文**：① signature 核的计算量随样本数平方增长，长序列需要截断或近似（已有加速方法，ETH 报告 2025 [snippet]）；② MMD 的误差界只覆盖 RKHS 单位球内的函数，储能优化这类非光滑输出不在保证范围内，与 D5 的反对意见一致，论文要明确写出这一边界。
- **English**: (1) signature-kernel cost grows quadratically with sample size, so long series need truncation or approximation (speed-ups exist, ETH report 2025 [snippet]); (2) the MMD bound covers only functions in the RKHS unit ball; non-smooth outputs such as storage optimisation are outside the guarantee, consistent with objection D5, and the paper must state this limit.

---

## 7. 四个候选选题（以方法为核心）/ Four candidate topics (method-centred)

**2026-11-10 会面版 / Meeting version**：会议页面只讨论两个科学问题：Q1 = T3，Q2 = T4。T2（代表性子集是否保住极端）已删除：它假设通行做法只按分布选、且没人量化过对极端的忽略，这两个前提都与文献不符（见 04 文件"原 Q1"一节）。/ The meeting page covers two scientific questions: Q1 = T3, Q2 = T4. T2 was dropped because both of its premises (that current practice selects on distributions only, and that the loss of extremes has not been quantified) are contradicted by the literature. 早先的版本为 / Earlier version: Q1 = T2，Q2 = T3，Q3 = T4。T1 是方法，不是科学问题，已从页面删除，**稍后讨论**。下表中"方法创新"一行和 T1 一列，以及原"建议"一段（Proposal for the visit），都**稍后讨论**。/ The meeting page covers the scientific questions only: Q1 = T2, Q2 = T3, Q3 = T4. T1 is a method, not a scientific question; it was removed from the page and is **to be discussed later**, as are the method-novelty row, the T1 column and the former recommendation (Proposal for the visit).

| | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| 题目 Title | **Certified path-space compression**：用 signature 核 MMD 加 kernel thinning 选择多变量能源与电力序列的代表期 / signature-kernel MMD and kernel thinning for representative periods of multivariate energy and electricity series | **Tail-preserving compression**：保留极端、干旱和累计亏缺的分布压缩 / distribution compression that keeps extremes, droughts and cumulative deficits | **Multi-scale compression from continent to island**：多分辨率缩减与尺度律 k\*(d_eff) / multiresolution reduction and the scaling law k\*(d_eff) | **Proxy-based selection of years to downscale**：用大尺度预报因子选择岛屿降尺度年份，并给出迁移误差界 / choosing island downscaling years from large-scale predictors, with a transfer bound |
| 方法创新 Method novelty | C1 + C2 + C4：新准则、新算法、误差证书 / new criterion, algorithm and certificate | C3：极值约束加块持续性 / EVT constraint and block persistence | C5：多尺度路径压缩；可证伪的尺度律 / multi-scale path compression; testable scaling law | 在预报因子空间做压缩，研究误差怎样传到局地场 / compression in predictor space, with error transfer to the local field |
| 数据 Data | PECD 4.2 / Mopo，NUTS0 | 同 T1 + 剩余负荷 / same + residual load | NUTS0 + NUTS2 岛屿 + Réunion | ERA5 长序列 + CorRES_2026 Réunion / long ERA5 + CorRES_2026 Réunion |
| 基准对比 Baselines | k-medoids、tsam、van Duinen SA-SWD、TMY、随机 / random | T1 方法加或不加尾部项 / T1 with and without the tail term | 单尺度方法 / single-scale methods | 随机、按年均值选、Kennard–Stone / random, by annual mean, Kennard–Stone |
| 验证 Validation | 留出年 MMD、L1–L6、块置换检验；合成数据上已知真值的实验 / held-out-year MMD, L1–L6, block permutation; synthetic data with known truth | 尾部分位数、GPD 参数、D_max 误差 / tail quantiles, GPD parameters, D_max error | 欧洲拟合 k\*–d_eff，在 Réunion 上检验 / fit on Europe, test on Réunion | 伪真值实验：以全部 ERA5 年份的 CorRES_2026 序列为局地场 / pseudo-truth: CorRES_2026 series over all ERA5 years as the local field |
| DTU 契合 DTU fit | U1、U2、U3、U8 | U1、U3 | Bornholm、CorRES | CorRES 区域算例 / CorRES regional runs |
| 岛屿 Island | 间接 / indirect | 间接 / indirect | **核心** / **core** | **核心（Réunion）** / **core (Réunion)** |
| 风险 Risk | 计算量大；需证明优于 van Duinen / compute cost; must beat van Duinen | 尾部样本少 / few tail samples | 岛屿区域可能不在数据中 / island zones may be missing | 降尺度年份太少，验证样本小 / few downscaled years, small validation set |
| 目标期刊 Journal | IEEE Trans. Power Syst. / Appl. Energy / Joule | 同 T1 / same | Nature Commun. / ERL | Renewable Energy / Appl. Energy |

**建议 Recommendation**【稍后讨论 / to be discussed later】

- **中文**：以 **T1 为方法核心，T2 作为它的扩展**（尾部项本来就是目标函数的一部分），**T3 作为应用层面的主要科学结论**，三者合成一篇论文：方法（路径空间压缩加误差证书）、发现（大陆到岛屿的尺度律）、产品（随 PECD 和 Mopo 发布的代表子集）。T4 是回 Réunion 后的第二篇方法论文。
- **English**: Use **T1 as the method core, T2 as its extension** (the tail term is part of the same objective), and **T3 as the main scientific finding**, combined into one paper: method (path-space compression with a certificate), finding (continent-to-island scaling law), product (representative subsets released with PECD/Mopo). T4 is a second method paper back on Réunion.

---

## 8. 明天与 Matti 讨论的话题 / Topics for tomorrow's discussion with Matti

| # | 话题 Topic | 中文要点 | English points |
|---|---|---|---|
| 1 | 数据 Data | Mopo、PECD 4.2 还是内部 CorRES？哪些年份？有没有 NUTS2 岛屿和 Bornholm？ | Mopo, PECD 4.2 or internal CorRES? Which years? NUTS2 islands and Bornholm included? |
| 2 | 用途优先级 Use priority | 请 Matti 给 U1–U8 排序 | Ask Matti to rank U1–U8 |
| 3 | 动机 Motivation | 确认动机：算力是直接起因，冗余是条件，"什么是足够的"是科学问题 | Confirm: compute is the trigger, redundancy the lever, sufficiency the scientific question |
| 4 | 方法定位 Method | 论文以新方法为核心（路径空间压缩加误差证书），而不是比较现有方法 | The paper is built on a new method (path-space compression with a certificate), not a comparison of existing ones |
| 5 | 只用统计评估 Stats-only | 是否接受以统计评估为核心，最多在最后用模型检查？ | Is a statistics-only assessment acceptable as the core, with model runs at most as a final check? |
| 6 | 与已有研究的重叠 Overlap | van Duinen 2026、Grochowicz 2024 | van Duinen 2026, Grochowicz 2024 |
| 7 | 选题 Topic | T1–T4 中选哪一个或哪种组合？ | Which of T1–T4, or which combination? |
| 8 | 岛屿 Islands | 欧洲岛屿、Réunion、Bornholm | European islands, Réunion, Bornholm |
| 9 | 产出与作者 Output and authorship | 期刊、作者顺序；代码放在 CorRES 还是 pybalmorel | Journal, author order; code in CorRES or pybalmorel |
| 10 | 实际安排 Practical | 账号和服务器、计算资源、每周会面时间 | Accounts and servers, compute, weekly meeting slot |

### 8.1 可直接念的英文问题 / English questions ready to use

```
1. Which data set do you have in mind: the Mopo pan-European CorRES runs, PECD 4.2, or an internal CorRES run? Which weather years, and which regions? Are NUTS2 island zones (Corsica, Sardinia, Sicily, Crete, Balearics), Malta, Cyprus or Bornholm included?
2. Which downstream use matters most to the group: Balmorel planning (the pybalmorel aggregation module), Mopo/SpineOpt, PECD climate-year selection for ENTSO-E, balancing and forecast errors, grid studies, or ML surrogates?
3. As I see it, compute limits force the reduction, the strong redundancy of multi-decade hourly data makes it possible, and the open question is when a reduction is sufficient, independently of the downstream model. Do you agree with this framing?
4. [Later / 稍后讨论] I would like the paper to rest on a new method: compressing the distribution of multivariate wind, solar and demand paths with a signature-kernel MMD and kernel thinning, with an error certificate and a tail-preserving term. Does that fit the group, or would you prefer a different emphasis?
5. Is a purely statistical assessment acceptable as the core, with model runs at most as a final check?
6. How do you see the overlap with van Duinen et al. (2026, Applied Energy) and Grochowicz et al. (2024, ERL)?
7. Of three scientific questions (do representative subsets keep the extremes; how much record is needed from continent to island; which years to downscale for an island), which one, or which combination, would you pursue?
8. Would European islands, Réunion and possibly Bornholm fit the group's interests? Could Bornholm data be used?
9. What output do you expect: which journal, author order, and should the code go into CorRES or pybalmorel?
10. Practical points: DTU account and server access after the security incident, compute resources, and a regular meeting slot.
```

---

## 9. 参考文献 / References

元数据 Metadata：除另注外，均与 OpenAlex/Crossref 的同一条记录一致（VERIFIED，2026-11-06 至 11-09）。Unless noted, every entry matches one OpenAlex/Crossref record (VERIFIED, 2026-11-06 to 11-09). 阅读范围见每条末尾 / read scope at the end of each entry.

**统计与 TSA 方法 / Statistics and TSA methods**
- Gretton, Borgwardt, Rasch, Schölkopf, Smola (2012). A kernel two-sample test. JMLR 13:723. [abstract only]
- Mak, Joseph (2018). Support points. Ann. Stat. 46:2562. doi:10.1214/17-AOS1629. [abstract only]
- Finkelstein, Schafer (1971). Improved goodness-of-fit tests. Biometrika 58:641. doi:10.1093/biomet/58.3.641. [abstract only]
- Cannon (2015). Selecting GCM scenarios that span the range of changes in a multimodel ensemble. J. Climate 28:1260. doi:10.1175/JCLI-D-14-00636.1. [abstract only]
- Mendlik, Gobiet (2016). Selecting climate simulations for impact studies based on multivariate patterns of climate change. Climatic Change 135:381. doi:10.1007/s10584-015-1582-0. [abstract only]
- Kotzur, Markewitz, Robinius, Stolten (2018a). Impact of different time series aggregation methods on optimal energy system design. Renew. Energy 117:474. doi:10.1016/j.renene.2017.10.017. [full text, arXiv preprint 1708.00420]
- Hoffmann et al. (2021). Typical periods or typical time steps? Appl. Energy 304:117825. doi:10.1016/j.apenergy.2021.117825. [abstract only]
- Wogrin (2023). Time series aggregation for optimization: one-size-fits-all? IEEE Trans. Smart Grid 14:2489. doi:10.1109/TSG.2023.3242467. [abstract only]
- Reichenberg, Hedenus (2022). The error induced by using representative periods in capacity expansion models. Energy Systems. doi:10.1007/s12667-022-00533-4. [snippet；仅 Crossref 标题检索，未逐字段核对 / Crossref title search only, fields not checked one by one]
- Roberts et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40:913. doi:10.1111/ecog.02881. [abstract only]

**欧洲多年代风光与选年 / European multi-decade wind–solar and year selection**
- van Duinen, van der Wiel, Thorey, Stoop (2026). Bridging the climate to energy data gap. Appl. Energy 427:129090. doi:10.1016/j.apenergy.2026.129090. [约 1/3 原文 / about 1/3 of the full text]
- Ullmark, Göransson, Johnsson (2025). Representing net load variability… Energy 316:134346. doi:10.1016/j.energy.2024.134346. [abstract only]
- Kittel, Schill (2026). Multi-threshold time series analysis… Commun. Earth Environ. 7. doi:10.1038/s43247-026-03251-2. [abstract only]
- Schill, Kittel, Roth (2025). Coping with the Dunkelflaute. EGU25-20413. doi:10.5194/egusphere-egu25-20413. [abstract]
- Ruhnau, Qvist (2022). Storage requirements in a 100% renewable electricity system. ERL 17:044018. doi:10.1088/1748-9326/ac4dc8. [abstract only]
- Gøtske, Andresen, Neumann, Victoria (2024). Nat. Commun. 15:10680. doi:10.1038/s41467-024-54853-3. [abstract only]
- Grochowicz, van Greevenbroek, Benth, Zeyringer (2023). Energy Econ. 118:106496. doi:10.1016/j.eneco.2022.106496. [abstract only]
- Grochowicz, van Greevenbroek, Bloomfield (2024). ERL 19:054038. doi:10.1088/1748-9326/ad374a. [abstract only]
- van der Wiel et al. (2019a). RSER 111:261. doi:10.1016/j.rser.2019.04.065. [abstract only]
- van der Wiel et al. (2019b). ERL 14:094010. doi:10.1088/1748-9326/ab38d3. [abstract only]
- Bloomfield et al. (2016). ERL 11:124025. doi:10.1088/1748-9326/11/12/124025. [abstract only]
- Bloomfield, Brayshaw, Charlton-Perez (2020). Meteorol. Appl. 27:e1858. doi:10.1002/met.1858. [abstract only]
- Staffell, Pfenninger (2018). Energy 145:65. doi:10.1016/j.energy.2017.12.051. [abstract only]
- Bodini, Lundquist, Zardi, Handschy (2016). Wind Energy Sci. 1:115. doi:10.5194/wes-1-115-2016. [abstract only]
- Craig et al. (2022). Joule 6:1405. doi:10.1016/j.joule.2022.05.010. [abstract only]

**DTU 相关 / DTU related**
- Koivisto et al. (2019). WIREs Energy Environ. 8:e329. doi:10.1002/wene.329. [abstract only]
- Murcia et al. (2022). Appl. Energy 305:117794. doi:10.1016/j.apenergy.2021.117794. [abstract only]
- Luzia, Koivisto, Hahmann (2023). Renew. Energy 217:118989. doi:10.1016/j.renene.2023.118989. [abstract only]
- Nayak, Simutis, Murcia Leon, Olsen, Koivisto (2025). Appl. Energy 402:126882. doi:10.1016/j.apenergy.2025.126882. [abstract only]
- Dalton, Bekker, Koivisto (2021). Energy Rep. 7:3775. doi:10.1016/j.egyr.2021.06.060. [abstract only]
- Quick et al. (2024). Electr. Power Syst. Res. 234:110675. doi:10.1016/j.epsr.2024.110675. [abstract only]
- Gaugl, Insunza, Portela, Wogrin (2026). Appl. Energy 427:128946. doi:10.1016/j.apenergy.2026.128946. [snippet]
- 数据 Data：Mopo（doi:10.5281/zenodo.17950648、10.5281/zenodo.18549865）；PECD 4.2（doi:10.24381/cds.f323c5ec）。工具 Tools：pybalmorel 文档 / docs；Mopo CORDIS 101095998；Bornholm PowerLabDK 网页 / web pages [snippet]。

**岛屿 / Islands**
- Psarros, Papathanassiou (2023). Generation scheduling in island systems with variable renewable energy sources: a literature review. Renew. Energy 205:1105. doi:10.1016/j.renene.2023.01.099. [snippet]
- Fernández-Muñoz, Pérez-Díaz (2021). Unit commitment in a hybrid diesel/wind/pumped-storage isolated power system considering the net demand intra-hourly variability. IET Renew. Power Gener. 15:30. doi:10.1049/rpg2.12003. [abstract only]
- Liu et al. (2024). Frequency nadir constrained unit commitment for high renewable penetration island power systems. IEEE Open Access J. Power Energy 11:141. doi:10.1109/OAJPE.2024.3370504. [abstract only]
- Rajabdorri, Lobato, Sigrist (2021). Viability of including frequency metrics in short-term scheduling of island power systems. 会议论文，无 DOI / conference paper, no DOI. [snippet]
- David, Ramahatana, Liandrat (2014). Spatial and temporal variability of PV output in an insular grid: case of Reunion Island. Energy Procedia 57:1275. doi:10.1016/j.egypro.2014.10.117. [abstract only]
- Tapachès, Perez, Lauret, Perez, David (2019). Mitigation of the variability of a PV fleet via geographical dispersion and energy storage systems on the Reunion Island non-interconnected grid. IEEE PVSC, p. 2082. doi:10.1109/PVSC40753.2019.8981214. [abstract only]
- Giorcelli, De Clerck, Pasta (2026). Assessing long-term metocean data variability for optimal energy system planning via static robust optimization approach. Appl. Ocean Res. 170:105015. doi:10.1016/j.apor.2026.105015. [abstract only]
- Meirelles et al. (2022). Climate change and impact on renewable energies in the Azores. Sustainability 14:15174. doi:10.3390/su142215174. [abstract only]
- Marczinkowski, Østergaard, Djørup (2019). Transitioning island energy systems. Energies 12:3484. doi:10.3390/en12183484. [abstract only]
- EDF SEI (2023). BESS projects France, Clean Energy for EU Islands workshop 3. 幻灯片，未做元数据核对 / slides, metadata not checked. [snippet]


**分布压缩与路径空间方法 / Distribution compression and path-space methods**（2026-11-09 核对，元数据来自 OpenAlex / metadata from OpenAlex）
- Dwivedi, Mackey (2021). Kernel thinning. arXiv:2105.05842. doi:10.48550/arXiv.2105.05842. 期刊版本未核对 / journal version not checked. [abstract only]
- Riabiz, Chen, Cockayne, Swietach, et al. (2022). Optimal thinning of MCMC output. J. R. Stat. Soc. B 84:1059. doi:10.1111/rssb.12503. [abstract only]
- Király, Oberhauser (2019). Kernels for sequentially ordered data. JMLR 20. [abstract only]
- Chevyrev, Oberhauser (2018). Signature moments to characterize laws of stochastic processes. arXiv:1810.10971. 期刊版本未核对 / journal version not checked. [abstract only]
- Salvi, Cass, Foster, Lyons (2021). The signature kernel is the solution of a Goursat PDE. SIAM J. Math. Data Sci. 3:873. doi:10.1137/20M1366794. [abstract only]
- Alden, Horvath, Issa (2025). Signature maximum mean discrepancy two-sample statistical tests. Springer book chapter, p. 161. doi:10.1007/978-3-031-97239-3_5. [abstract only]
- Bachem, Lucic, Krause (2017). Practical coreset constructions for machine learning. arXiv:1703.06476. [abstract only]
- Chen, Welling, Smola (2010). Super-samples from kernel herding. UAI; arXiv:1203.3472. [abstract only]

**核对说明 / Verification notes**
- 所有文献都没有读全文，Kotzur 2018a 除外（arXiv 预印本全文）；van Duinen 2026 读了约三分之一。表中的数字引用前要读全文核实。/ No full text was read except Kotzur 2018a (arXiv preprint); about a third of van Duinen 2026 was read. Numbers in the tables must be checked against full texts before citing.
- 第 7 节以前列出的已核对文献都已加入 Zotero 集合 `Projects/Time_Series_2026` 并打了标签（2026-11-09）；方法类文献见下一条。尚未生成 `.bib`。/ Verified references listed before this update are in the Zotero collection `Projects/Time_Series_2026` with tags (2026-11-09); method papers, see next line. No `.bib` yet.
