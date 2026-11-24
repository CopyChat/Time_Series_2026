# Time Series 2026：研究计划（第 3 版，2026-11-09）

DTU Wind 访问：2026-11-10 至 2027-02-05（约 12 周），合作者 Matti Koivisto。
第 1 版（话题、关键词、25 篇 TSA 文献）见 `working/2026-10-15_topic_keywords_references.md`。第 2 版把用途限定为 ML 训练和验证；第 3 版取消这个限定（Chao，2026-11-09）。

## 0. 讨论结论

| # | 结论 | 来源 |
|---|---|---|
| D1 | 题目：多年欧洲能源与电力时间序列（需求、风光、水电、温度驱动负荷、电价、跨境潮流）的统计代表性缩减；范围不限于风光（Chao 2026-11-09） | 邮件 2026-09-30 / 10-05；Chao 2026-11-09 |
| D2 | 缩减结果只用统计检验评估，不用能源系统优化模型 | Chao 2026-11-06 |
| D3 | 用途不限于 ML：资源评估、储能规模、充裕度、电网、气候变化影响、ML 训练，都是缩减数据的下游用途 | Chao 2026-11-09 |
| D4 | 统计依据：分布距离（MMD、能量距离、Wasserstein）小 ⇒ 一大类函数的期望误差小，与具体模型无关 | Gretton 2012；Mak & Joseph 2018（[abstract only]） |
| D5 | 已知反对意见：① 只看统计，系统应力最大的时段可能被漏掉；② 对优化模型，统计好 ≠ 优化结果好。本课题的回应是加入"系统相关的统计量"（剩余负荷、累计能量亏缺），这些量仍可直接从时间序列计算，不需要优化模型 | Grochowicz 2024；Hoffmann 2021；Wogrin 2023 |
| D6 | 岛屿贡献：欧洲数据中的岛屿区域加上 Réunion 迁移测试 | 第 2 版 |

## 1. 欧洲数据（候选）

| 数据 | 内容 | 状态 |
|---|---|---|
| **CorRES Mopo pan-European VRE data**（Koivisto et al., Zenodo 2026, doi:10.5281/zenodo.17950648, CC-BY-4.0） | 逐时风电（陆上 9 种、海上 4 种技术 + existing）和光伏（3 种）；ERA5 + GWA | 公开，1.6 GB zip；年份和分区页面未写明 |
| **Mopo 气候预估**（doi:10.5281/zenodo.18549865） | MPI-ESM1-2-HR、EC-Earth3 × SSP2-4.5/SSP5-8.5，2015–2100 逐时 | 公开，12.6 GB zip |
| **PECD 4.2**（C3S + ENTSO-E, doi:10.24381/cds.f323c5ec） | 风光容量因子（风电由 CorRES 生成）、水电、温度；ERA5 1950 年起，6 个 CMIP6 模式 × 4 个 SSP；NUTS0、NUTS2、PEON、P2ON 分区 | 公开（CDS） |
| CorRES_2026 Réunion 算例 | ERA5 + GWA2 风电，与 Mopo 同一模型链 | 本人服务器已有 |

岛屿 NUTS2 区域：Corse FRM0、Sicilia ITG1、Sardegna ITG2、Kriti EL43、Illes Balears ES53；Malta、Cyprus 是国家级。这些区域是否在数据中**未核实**。

## 2. 文献：七个研究方向里的"代表性"

"代表性"在不同领域含义不同。课题的核心就是把这些含义放进同一套统计框架。

### 2.1 典型年（TMY）：集中趋势

- **做法**：每个月从多年中挑出与长期分布最接近的那个月（Finkelstein–Schafer 统计量，Finkelstein & Schafer 1971），12 个月拼成一年。光伏、建筑能耗普遍使用（ISO 15927-4、PVGIS），美国有 Typical Solar/Wind Years 数据（Argonne 2024，仅见数据目录）。
- **局限**：月份拼接破坏跨月的时间连续性；只代表平均状态，不含极端；风的"参考年"没有公认方法（仅见搜索摘要）。

### 2.2 欧洲天气年和气候年的选择：分布匹配

- **van Duinen et al. (2026, Appl. Energy 427:129090)**：从 PECD 预估的 180 年中用模拟退火选出整年子集，最小化冬夏两季的切片 Wasserstein 距离（NUTS0 日均值）。代表性约为 ENTSO-E 现行做法的 2.5–3.5 倍。只做统计评估，没有检验逐时结构、干旱和岛屿。
- **ERAA 2025**：用 Wasserstein 距离选天气情景子集（仅见搜索摘要）。**TYNDP 2026**：k-medoids 聚类（仅见搜索摘要）。
- **Ullmark et al. (2025, Energy 316:134346)**：按净负荷的幅度和持续时间，从 39 年中选少数天气年（北欧），并用模型验证。

### 2.3 气候模式集合的子集：覆盖范围

- **Cannon (2015, J. Climate 28:1260)**：聚类偏向高密度区，选出的是集中趋势而不是全集合的范围；KKZ 算法选出的子集能覆盖集合的变化范围，而且有序（5 个的解包含在 6 个的解里）。
- **Mendlik & Gobiet (2016, Climatic Change 135:381)**：PCA 加聚类，再从每类中抽样，以保留模式离散度。
- **对本课题的意义**：代表性至少有两种定义，即**分布匹配**和**范围覆盖**，两者给出的子集可能不同。`[INFERENCE]` 依据上面两组文献；能源 TSA 文献没有讨论过这一点。

### 2.4 多年变率与极端：哪些统计量对系统重要

- **Ruhnau & Qvist (2022, ERL 17:044018)**：德国 35 年逐时数据；短缺期不超过 2 周，但最大能量亏缺跨越 9 周，因为几个短缺期接连出现。决定储能规模的是**累计亏缺**，不是单个事件。
- **Kittel & Schill (2026, Commun. Earth Environ. 7)**：VRE 干旱特征强烈依赖阈值；干旱可以跨年，日历年不适合作规划时段。Schill, Kittel, Roth (EGU 2025)：极端干旱事件决定长期储能的运行和投资。
- **van der Wiel et al. (2019, RSER 111:261)**：基于 3 × 2000 年模拟天气，筛选 1 天、7 天、14 天的低出力和高短缺事件；空间上分散布局不能消除这些事件（据 KNMI 页面摘要）。van der Wiel et al. (2019, ERL 14:094010)：阻塞型天气型平均短缺更高，但每种天气型里都会出现极端短缺。
- **Bloomfield et al. (2016, ERL 11:124025)**：说明为什么必须用多年代数据；风电比例越高，年际变率的影响越大。Bloomfield et al. (2020, Meteorol. Appl. 27:e1858)：targeted circulation types，把系统敏感性和大气环流结构结合起来。
- **Staffell & Pfenninger (2018, Energy 145:65)**：英国逐时爬坡率扩大 50%（2030 情景）。
- **Grochowicz, van Greevenbroek, Bloomfield (2024, ERL 19:054038)**：用 40 年再分析驱动的欧洲模型的影子价格找出最困难的时段；这些时段**不能只从气象或只从电力系统角度理解**。这是对纯统计方法最直接的反对意见。
- **Gøtske et al. (2024, Nat. Commun. 15:10680)**：62 个天气年，总成本变化 ±10%；按复合事件年设计的系统更稳健。Grochowicz et al. (2023, Energy Econ. 118:106496)：41 年、3 小时分辨率的欧洲模型已接近计算极限。
- **Zeyringer et al. (2018, Nat. Energy 3:395)**：英国 2050 年系统对时空和年际变率的稳健设计（摘要未取得，只能凭标题引用）。

### 2.5 资源评估：记录长度与持续性

- **Bodini et al. (2016, Wind Energy Sci. 1:115)**：加拿大 60 个站点、62 年记录；风速偏离平均值的状态会持续数十年，使不确定性比"各年独立"的假设大约 2.5 倍。
- **对本课题的意义**：如果年与年之间相关，"选 k 年"所含的独立信息少于 k 年，需要的子集就更大。`[INFERENCE]`

### 2.6 合成与生成式时间序列：另一条路线

- Chen et al. (2018, IEEE TPWRS 33:3265)：GAN 生成风光情景，保留时空模式。Strnad et al. (2026, Environ. Data Sci. 5:e11)：用生成式深度学习降尺度 CMIP6，评估德国未来的 Dunkelflaute。
- **对本课题的意义**：生成模型的结果同样需要统计检验。本课题的检验组可以直接用于检验生成序列。`[INFERENCE]`

### 2.7 能源与气候建模的衔接、ML 用途、岛屿

- **Craig et al. (2022, Joule 6:1405)**：议程之一是建立"面向能源系统的气候数据集"。缩减后的代表性子集就属于这一类。
- **Gaugl et al. (2026, Appl. Energy 427:128946)**：欧洲 ML 代理模型只用 2009 一个气候年训练（仅见搜索摘要）。
- **Nayak et al. (2025, Appl. Energy 402:126882)**：DTU 的风电验证；关心爬坡和高出力分布时，建议加入随机波动和停机模拟。
- **岛屿**：Giorcelli et al. (2026, Appl. Ocean Res. 170:105015)：La Gomera（加那利），20 年逐时海洋气象数据，按最坏年设计多技术组合；摘要指出小型非互联岛屿直接暴露于资源的自然变率。一篇 2017 年的岛屿 TSA 研究报告，72 个典型日仍不收敛（作者未核实，仅见搜索摘要）。

## 3. 研究空白

1. **代表性的不同定义没有被放在一起比较过。** 分布匹配（van Duinen、ERAA）、范围覆盖（Cannon）、集中趋势（TMY）、极端和累计亏缺（Ruhnau & Qvist、Kittel & Schill）各自使用。同一个子集在这些准则之间是否冲突，没有定量结果。
2. **没有研究给出所需子集大小怎样随空间尺度变化。** 尺度从欧洲到国家再到岛屿，变率的空间平滑逐级减小。
3. **代表性的时间稳定性。** 用历史数据选出的子集，对未来气候是否仍有代表性？van Duinen 假设 2016–2045 年没有趋势。
4. **年际持续性的影响。** 年际持续性（Bodini 2016）使有效样本量小于名义年数；它对代表性子集大小的影响在欧洲尺度上没有量化。

## 4. 研究主题与研究问题

**暂定题目**

> What does "representative" mean for multi-decade energy and electricity time series? A statistical framework for reducing pan-European energy data, from continent to islands

**主研究问题**

> 对多年代的欧洲能源与电力序列（CorRES/PECD 的风光、水电、温度驱动需求及剩余负荷，以及 ENTSO-E 的负荷、电价、跨境潮流等实测序列），能否找到一个缩减子集，同时满足各种用途所要求的代表性（集中趋势、范围覆盖、时间结构、干旱与累计亏缺、空间同时性）？如果这些准则相互冲突，冲突有多大？所需的子集大小怎样随空间尺度（欧洲 → 国家 → 岛屿）和气候（历史 → 未来）变化？

**子问题与可证伪假设**

| 子问题 | 假设 H | 否定 H 的结果 | 优先级 |
|---|---|---|---|
| RQ1 准则冲突：针对一种准则最优的子集，在其他准则上表现如何？ | H1：分布匹配的子集低估干旱和累计亏缺；范围覆盖的子集使分布失真。准则之间存在 Pareto 前沿 | 有一个子集同时位于所有准则的阈值以内 | 核心 |
| RQ2 空间尺度：k\* 与区域面积、PCA 有效维数 d_eff 的关系 | H2：岛屿的 k\* 大于国家，国家大于欧洲；k\* 随 d_eff 增加 | k\* 与尺度无关 | 核心 |
| RQ3 时段长度：日、周、月、整年、水文年之间的权衡 | H3：同样的数据量下，长时段的累计亏缺误差更小，短时段的分布误差更小 | 无权衡 | 核心（作为实验维度） |
| RQ4 持续性：年际自相关怎样改变有效样本量和 k\* | H4：持续性强的区域 n_eff 明显小于 n | 各区域 ρ₁ ≈ 0 | 扩展 |
| RQ5 气候变化：历史数据选出的子集对 2050 年附近的预估是否仍有代表性 | H5：分布距离显著增大，尤其是光伏和需求 | 距离不变 | 扩展（第二篇论文） |

## 5. 方法【稍后讨论；2026-11-10 会面只讨论科学问题】

**选择单元**：长度 L ∈ {1 天, 1 周, 1 个月, 1 个水文年（4 月 1 日至 3 月 31 日）}，每个单元带权重 w_c。

**选择方法**：
- 随机（基准）
- TMY 式逐月拼接（Finkelstein–Schafer 统计量）
- k-medoids（TYNDP 做法）
- 模拟退火最小化季节切片 Wasserstein 距离（van Duinen 2026）
- KKZ 范围覆盖（Cannon 2015）
- support points（能量距离）
- 加入极端时段

**统计检验组（均直接从时间序列计算，不用优化模型）**

| 层 | 代表性的类型 | 统计量 | 对应用途 |
|---|---|---|---|
| L1 | 集中趋势与边缘分布 | KS 统计量 D、Wasserstein W₁、持续曲线 NRMSE、P1/P99 分位数 | 资源评估、发电量 |
| L2 | 联合分布 | 能量距离、MMD（块置换检验） | ML、通用 |
| L3 | 时间结构 | 自相关（滞后 1–48 h）、爬坡 Δx 分布、日内剖面 | 运行、灵活性 |
| L4 | 空间同时性 | 相关矩阵误差 ‖R − R̃‖_F ÷ ‖R‖_F、多区域同时低出力的频率 | 电网、互联 |
| L5 | 极端与累计亏缺 | 多阈值干旱的频率和时长、最大累计能量亏缺 | 储能、充裕度 |
| L6 | 范围覆盖 | 子集覆盖的全集合年际指标范围（最小值到最大值）所占比例 | 风险、气候影响 |

```
 能量距离:
   E(P, Q) = 2·E‖X − Y‖ − E‖X − X'‖ − E‖Y − Y'‖ ≥ 0,   当且仅当 P = Q 时为 0

 PCA 有效维数:
              ( Σ λ_i )²
   d_eff  =  ───────────
               Σ λ_i²

 年际持续性下的有效样本量（AR(1) 近似）:
                  1 − ρ₁
   n_eff  =  n · ────────          ρ₁ = 年均值的滞后 1 年自相关系数
                  1 + ρ₁

 剩余负荷与最大累计亏缺:
   r_t = d_t − ( a·w_t + b·s_t )          a, b 取使长期平均 VRE 发电 = 平均需求
                       t₂
   D_max  =   max      Σ  r_t
            t₁ < t₂   t=t₁

 所需子集大小:
   k*(L, 区域) = min { k : 所需各层统计量都低于阈值 }
```

`[ASSUMPTION]`：r_t 中的 a、b 按"年均能量平衡"取值，这是本计划自己的设定，文献里没有查到，可以改。

## 6. 对岛屿能源转型的贡献

- 给出孤立小系统需要多长、多少、哪些时段，才能分别满足各种代表性准则；同时指出哪些准则在岛屿上冲突更严重。
- **Réunion 迁移测试**：CorRES_2026 序列（与 Mopo 同一模型链）用同一组检验，检验欧洲拟合的 k\*–d_eff 关系。

## 7. 时间表

| 周 | 时间 | 任务 | 检验标准 |
|---|---|---|---|
| 1 | 11-10 – 11-14 | 与 Matti 确定数据、年份、分区和岛屿；从 RQ1–RQ5 中定下核心问题 | 书面确认 |
| 2–3 | 11-17 – 11-28 | 下载与质量检查；建 `metrics.py`（L1–L6）；建空间尺度梯度 | 容量因子与 Nayak 2025 的验证值一致 |
| 4–6 | 12-01 – 12-19 | 选择方法 × L × k × 区域的实验矩阵（服务器 worker pool） | 各区域得到完整的 k\* 曲线和 Pareto 前沿 |
| 7–8 | 01-05 – 01-16 | RQ1–RQ3 分析；RQ4 持续性 | 假设检验结果和置信区间 |
| 9–10 | 01-19 – 01-30 | Réunion 迁移测试；时间允许时做 RQ5 的初步结果 | k\* 预测偏差 |
| 11–12 | 02-02 – 02-05 及之后 | 论文初稿（Applied Energy 或 Renewable and Sustainable Energy Reviews）和代码 | 初稿交给 Matti |

DTU 在网络攻击后关闭了外部访问（Vivi 邮件，2026-10-23）。拿不到内部数据时，先用公开的 Mopo/PECD 4.2。

## 8. 第 1 周要问 Matti 的问题（2026-11-10 会面用）

### 8.1 DTU 的工具和项目中，缩减数据可能的用途（优先级待 Matti 确认）

| # | 用途 | DTU 工具/项目 | 证据（阅读范围） | 关键的代表性类型 |
|---|---|---|---|---|
| U1 | 欧洲容量扩展规划 | Balmorel（pybalmorel） | pybalmorel 有 TSA 模块（基于 tsam，contiguous/averaging/kmeans），文档写明"正在开发和测试"（文档页） | L1、L3、L5（储能） |
| U2 | 泛欧规划平台与数据 | Mopo（Horizon Europe，2023–2026，VTT 牵头，DTU 参与）；SpineOpt；CorRES Mopo 数据 | CORDIS 写明目标是"时间、空间、技术表达高度灵活"的规划工具，以及逐时、NUTS2 的泛欧数据集（项目页） | L1、L2、L4 |
| U3 | 充裕度评估中的气候年选择 | PECD 4.2 for ENTSO-E（风电由 CorRES 生成）→ ERAA/TYNDP | CorRES open-data 页面；ERAA 2025 用 Wasserstein 选子集（仅见搜索摘要） | L5、L6、L2 |
| U4 | 气候变化影响 | Mopo 气候预估（2 模式 × 2 SSP，2015–2100）；Luzia 2023 | Koivisto, Nayak, Kanellas（WISO25 摘要）：泛欧风电的气候变化影响为低到中等 | L6、RQ5 |
| U6 | 平衡与预测误差 | CorRES 预测误差模拟；BalancingToolChain | Koivisto 2019（[abstract only]）；Nayak 2025：关心爬坡时需要随机波动 | L3（亚小时级爬坡） |
| U7 | 电网与概率潮流 | Dalton, Bekker, Koivisto 2021 | 按大气状态聚类出运行场景（[abstract only]） | L4、L2 |
| U8 | ML 代理模型 | Quick et al. 2024（电价代理） | [abstract only] | L2、L6（覆盖） |

`[INFERENCE]` 依据现有材料，U1、U3 证据最直接：Balmorel 正在开发 TSA，PECD 选年直接服务 ENTSO-E。优先级需要 Matti 确认。（U5 已删除：HyDesign 属于另一个项目，2026-11-09）

### 8.2 英文提问清单

```
1. Which data set do you have in mind: the Mopo pan-European CorRES runs, PECD 4.2, or an internal CorRES run? Which weather years, and which regions (any NUTS2 island zones such as Corsica, Sardinia, Sicily, Crete, Balearics, or Malta and Cyprus)?
2. Which downstream use matters most to the group: Balmorel planning (the pybalmorel aggregation module), Mopo/SpineOpt, PECD climate-year selection for ENTSO-E, balancing and forecast errors, or ML surrogates?
3. Is a purely statistical assessment of the reduced series (no energy model in the loop) acceptable as the core of the paper, with model runs at most as a later check?
4. How do you see the overlap with van Duinen et al. (2026, Applied Energy) on climate-year selection from PECD, and with Grochowicz et al. (2024, ERL)?
5. Target output: one journal paper (which journal), a tool in CorRES or pybalmorel, or a selection guide attached to the DTU data sets?
6. Would a comparison of continental regions with small isolated island systems, including Réunion, fit the group's interests?
```

## 8.3 岛屿弱电网是否也需要聚合数据

**结论**：需要，但瓶颈和关键统计量都与大陆不同。数学框架相同，各准则的权重和数据来源不同。

| 方面 | 大陆互联系统 | 小型孤立岛屿 | 依据 |
|---|---|---|---|
| 计算瓶颈从哪来 | 节点多、技术多、几十年 → 优化模型太大 | 节点少；但运行约束多：机组组合、频率和惯量约束、亚小时分辨率（15 min） | 岛屿调度文献：频率约束的计算时间高，运营方仍多用逐时机组组合（仅见搜索摘要）；El Hierro：考虑小时内净负荷变化后，弃风明显减少（仅见搜索摘要） |
| 数据瓶颈 | 长序列现成（ERA5、PECD） | 0.25° 再分析分辨不出岛屿地形，需要 km 级降尺度（如 WRF），只能算几年 | `[INFERENCE]` Réunion 约 2500 km²，最高约 3000 m，而 0.25° ≈ 28 km |
| 缩减的方向 | 长序列 → 少数代表期 | 还要反过来问：只算得起几年降尺度时，算哪几年；已有的几年是否代表长期气候 | `[INFERENCE]` 与 van Duinen 2026"弥合气候—能源数据缺口"的动机一致 |
| 空间平滑 | 大，站点间相关性低 | 存在但范围小：Réunion 全岛分散布置光伏几乎消除天气造成的波动；天气尺度事件（多日低风、气旋）仍全岛同时发生 | Tapachès 2019；EDF SEI 2023（snippet）；van der Wiel 2019（修正于 2026-11-09，原写"几乎没有"） |
| 关键时间尺度 | 数周的 Dunkelflaute、跨年累计亏缺 | 分钟到小时级爬坡（云、风）、数日事件、热带气旋 | Ruhnau & Qvist 2022；Kittel & Schill 2026；岛屿调度文献 |
| 缩减难度 | 少量典型期即可 | 储能主导时更难：Kotzur et al. 2018a（#3）的孤立区域系统（概念算例，不是真实岛屿）到 72 个典型日仍不稳健收敛，原因是典型期相互独立、不能交换能量 | Kotzur 2018a [full text，arXiv 预印本]（修正于 2026-11-09） |
| 规划常用准则 | 分布匹配（ERAA、van Duinen） | 最坏年或稳健设计（La Gomera 20 年，最坏情况优化） | Giorcelli 2026（[abstract only]） |
| 最重要的检验层 | L2、L4、L5（长时段） | L3（亚小时）、L5（短时段）、L6（极端和覆盖） | `[INFERENCE]` |

**对论文的意义**：同一套统计框架在两类系统上给出不同的 k\* 和不同的准则冲突，这本身就可以作为主要结果（RQ1 × RQ2）。岛屿还多一个独立问题：已有的几年降尺度数据是否代表长期气候。

## 9. 文献核对状态（2026-11-09）

- **元数据**：第 2 节的 24 篇期刊论文和会议摘要（另有第 0 节的 4 篇，已于 2026-11-06 核对），标题、作者、年份、期刊、卷号和页码（或文章号）都与 OpenAlex/Crossref 的同一条记录一致（VERIFIED）。
  - Cannon 2015：OpenAlex 记为 2014，Crossref 记为 2015，以 Crossref 为准。
  - ERAA 2025、TYNDP 2026、Argonne TSY/TWY、ISO 15927-4 是报告或标准，未做元数据核对。
- **阅读范围**：全部为 [abstract only] 或更少。
  - van Duinen 2026：子代理读了约三分之一原文。
  - Zeyringer 2018：摘要未取得。
  - Gaugl 2026、ERAA、TYNDP：仅见搜索摘要。
  - 表中所有数字引用前都要读全文核实。
- 尚未加入 Zotero，`.bib` 尚未生成。
