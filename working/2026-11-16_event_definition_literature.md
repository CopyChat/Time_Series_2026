# 极端事件的定义：参考文献核对与面向投资问题的定义（2026-11-16）

- 用途：研究计划 Q1（事件定义）和第 6 节（数据）。文献只作参考；最终定义由研究问题决定，Chao 倾向**投资问题**（11-16）。
- 规则：出处写到节或表；阅读范围 [full text] / [notes only]；推断标 [INFERENCE]，提议标 [ASSUMPTION]。

## 1. 五篇参考文献的事件定义与数据

| 文献 | 事件怎样定义 | 变量与尺度 | 服务的问题 | 数据是否公开 | 阅读范围 |
|---|---|---|---|---|---|
| Grochowicz, Bloomfield & Victoria 2026（DTU） | 系统定义事件（SDE）：14 天窗口内，全系统"需求 × 影子价格"之和 ≥ C = 1000 亿欧元（约为年电费的 35%）。影子价格来自 PyPSA-Eur 对每个天气年做的容量扩展与调度联合优化（Methods，式 (1)–(2)）。窗口 T ≤ 336 h；互相重叠的候选窗口筛成一组互不重叠的事件；阈值的取法是使平均每年约 1 个事件、平均时长约 7 天（模型中储氢的放电时长）（Grochowicz 2024 §2.3） | ERA5 1941–2021，80 个天气年（7 月 1 日至次年 6 月 30 日），90 节点，逐时；需求随气温变化 | **投资**：SDE 是"大部分基础设施建设由它决定"的时段（Results 第 1 段） | 输入：ERA5 + atlite，公开。中间数据：Zenodo [10.5281/zenodo.20590389](https://doi.org/10.5281/zenodo.20590389)；代码：GitHub [aleks-g/stressed-system v1.0](https://github.com/aleks-g/stressed-system/tree/v1.0)（Data/Code availability） | full text（arXiv v2） |
| 同上：4 类 | 按 7 个系统量聚类（最高净负荷、平均净负荷、时长、燃料电池总放电 TWh、燃料电池最大放电 GW、平均相对负荷、风电容量因子距平），按 Silhouette 和 Calinski-Harabasz 分数取 4 类（Methods "Clustering of events"） | 41 个 SDE | 投资：区分功率缺口（需要备用容量 GW）和能量缺口（需要储能电量 TWh） | 同上 | full text |
| de Marco et al. 2025 | 每个气候年单独做投资与调度优化；逐时成本 C_t = Σ_n(电需求 × 电影子价格 + 热需求 × 热影子价格)；按 C_t 从高到低取小时，直到占全年总成本的 50%；间隔不到 48 小时的合并成一个事件；事件按累计成本排序，保留到占总成本的 50%（§2.2.1） | CESM2，SSP3-7.0，2080–2100，3 段 × 20 年 = 60 年；28 国（NUTS0），逐时；特征：供热需求、陆上风电、光伏、水库来水的 p5、中位数、p95 × 28 国 = 336 维，PCA 降到 47 维（§3.2） | **投资**（全新建设，2050 年净零） | 模型输入公开，含 60 个气候年的能源输入（光伏、陆上和海上风电、径流式水电、水库来水、供热需求、热泵 COP，NUTS0 逐时）：GitHub [ZEN-universe/ZEN-models，分支 Climate-resilience](https://github.com/ZEN-universe/ZEN-models/tree/Climate-resilience)（Data availability）。事件清单本身：原文没有说是否公开 | full text（补充材料未读） |
| Kapica et al. 2024 | 干旱日 = 日容量因子低于**基准期（1970–2020）**该区域、该季节的第 20 百分位；指标 N = 一个季节、一个时期内干旱日的总数；风光混合 CF = 0.5 × CF_PV/CF_PV,max + 0.5 × CF_WE/CF_WE,max（§2.2，式 (1)–(2)）。不定义事件（没有持续时间、合并规则） | C3S CDS 日容量因子，NUTS-2，8 组 EURO-CORDEX，RCP4.5/8.5；不含需求和水电 | 资源（不针对系统问题） | 输入在 C3S CDS 公开；派生数据"available on request"（Data availability） | full text |
| Aminimehr et al. 2026 | 风、光潜力取 1、3、5 日滑动平均 → 按月求边缘分布 → Clayton copula 联合（每个模式、窗口、格点用 1850–2100 全时段拟合）→ SREI = Φ⁻¹(C_θ(pv, w))；事件 = SREI 连续低于 **−1.28**（第 10 百分位）的日子；另用 −1.64、−1.96 分级；频率 = 30 年内事件数，持续时间 = 平均事件长度，强度 = 事件内平均 SREI（Methods "Quantification of RED"） | 11 个 CMIP6，SSP5-8.5，日，格点，全球；工业化前 1850–1879 对 1.5/2/3 °C；未做偏差订正；不含需求和水电 | 资源 | CMIP6（ESGF）、ERA5 公开；派生数据和代码：Zenodo [10.5281/zenodo.22657232](https://doi.org/10.5281/zenodo.22657232)（Data/Code availability） | full text（accepted preview） |
| Mostue et al. 2026 | 极端风事件用超阈值法（peak-over-threshold）定义：弱风事件 = 格点上 100 m 风速低于 3 m/s（风机切入风速），强风事件 = 高于 25 m/s（切出风速）；时间步长 6 小时，所以最短事件为 6 小时；原文没有合并规则。年频率 = 时段内事件数 ÷ 20 年；持续时间取事件平均值（STAR Methods "Extreme wind event definition"） | 5 个 CMIP6（CMCC-CM2-SR5、CMCC-ESM2、EC-Earth3、MPI-ESM1-2-HR、MRI-ESM2-0），SSP5-8.5，6 小时瞬时值，由模式层插值到 100 m，以 ERA5 为参照做分位数增量映射（QDM）订正，统一到 1.25° × 1.12° 网格；1980–1999 对 2040–2059、2080–2099；只有风 | 资源（阈值取自风机的运行范围） | 下载 GCM 数据和计算事件的代码在 Zenodo [10.5281/zenodo.18392113](https://doi.org/10.5281/zenodo.18392113)；输入为 ESGF 上的 CMIP6（Data and code availability） | full text（Europe PMC，PMC12972962） |

- 更正：11-11 笔记把 Aminimehr 的阈值写成 −1.0，原文是 −1.28，已改。
- 研究计划第 1 节对这几篇的描述，经原文核对成立：Grochowicz 2026 只用历史数据，并把变暖气候下的检验列为未来工作（Discussion："Future work using these runs will allow for benchmarking of the historical stress tests in a warmer climate"）；de Marco 只有一个模式、一个未来时段；Kapica、Aminimehr、Mostue 不做事件聚类、不含需求。

## 2. 三类定义方式的对比

| | 系统定义 | 供需平衡定义 | 资源强度定义 |
|---|---|---|---|
| 代表文献 | Grochowicz 2024/2026，de Marco 2025 | van Duinen 2025；本课题候选（第 4 节） | Kapica 2024，Aminimehr 2026，Mostue 2026 |
| 依据的量 | 每小时系统成本 = 需求 × 影子价格（欧元）；影子价格来自投资与调度联合优化 | 剩余负荷 = 需求 − 风电 − 光伏 − 径流式水电（GW） | 风光容量因子、100 m 风速、标准化指数（无量纲或 m/s） |
| 含需求、水电 | 含 | 含需求和径流式水电 | 都不含（Mostue 只有风） |
| 要不要跑模型 | 要，每个天气年一次大型优化（Grochowicz 2026：80 年 × 3 小时，60 GB） | 不要；要固定一个装机情景 | 不要 |
| 跨年可比，能否算概率 | 不能直接比：每年的系统单独优化，衡量标准随年份变化（Grochowicz 2026 Methods："cannot compare the severity of events across different optimisations"）；de Marco 的阈值是本年成本的 50%，每年按定义都有事件 | 能：装机和阈值固定后，所有年份用同一个标准衡量，可算频率、重现期 | 能：阈值固定在基准期（Kapica、Mostue）或固定的分布（Aminimehr） |
| 依赖哪些假设 | 成本数据、可选技术、储能表示方式、政策约束（CO2、输电扩建、自给率）、阈值、同一年里的其他压力时段 | 装机情景（总量和地区分布）、参考供给水平、需求模型 | 阈值、功率曲线或指数构造方式 |
| 能连到 | 电力分析和经济分析（欧元；触发哪类投资） | 电力分析（所需可调度容量 GW、储能电量 TWh、互联输电）；经济分析要另乘成本假设 | 气象与气候分析；不能直接连到电力量或经济量 |
| 气候变化下的代价 | 每个气候模式、情景、年份都要重新优化；系统随气候重新设计，气候信号与系统响应混在一起 [INFERENCE] | 只需换输入数据，可在多个模式上重复 | 只需换输入数据 |
| 在本课题中的角色 | 外部验证（Q3） | 事件定义的主体（研究计划 D6） | 对照：说明资源偏低与供需短缺的差别 |

- van Duinen et al. 2025（RSER 223:115993）[full text，§3.1]：剩余负荷逐日、按国家；能源干旱 = 7 日滑动平均剩余负荷最高、重现期 1 年的窗口（1600 年中每国 1600 个互不重叠的窗口），只保留 11–3 月。理由：7 天是天气尺度系统的时间尺度，也是储能难以应对的时间尺度；重现期 1 年代表"中等极端、但频繁到系统应当为它做准备"的事件；剩余负荷的峰值表示对非可再生发电的需求最大或储能耗尽。
- Grochowicz 2024 §3 对后两类的批评："As opposed to methods considering only peak load or net load …, using power system optimisation outputs … takes the complex interactions between storage and transmission into account"；"meteorologically extreme single days … do not reliably identify system-defining events"。

### 2.1 系统定义为什么取决于模型和假设（原文例子）

| 因素 | 原文中的结果（Grochowicz 2026） |
|---|---|
| 储能的表示方式 | 把储能的电量和功率分开优化后，同样的阈值下，事件频率从每 1.5 年一次变为每 2 年一次（Methods） |
| 政策约束 | 允许少量 CO2 排放时，既有燃气电厂取代全部储氢和燃料电池，影子价格下降，要把阈值降到 300 亿或 500 亿欧元才能找到同类事件（Methods；Fig. S6） |
| 阈值 | 阈值从 1000 亿降到 500 亿欧元，事件从 41 个增到 159 个（Fig. S7） |
| 事件类型的稳定性 | 严重功率缺口事件在各种敏感性设置下都能找到；能量缺口事件"less consistently identified across different configurations"（Results） |
| 同一年里的其他时段 | 筛选"skewed towards uneven conditions"：一段时期与同年其他时段差别越大越容易被识别；"the existence of another SDE during the same year can impact the classification"（Methods）；艰难年份如 1941/42 没有 SDE（Fig. 6 图注） |

### 2.2 玩具模型中的例子（合成数据）

脚本 [sde_dependence_experiments.py](../ai_workspace/event_definition/scripts/sde_dependence_experiments.py)，结果 [sde_dependence_toy_synthetic.csv](../ai_workspace/event_definition/figures/sde_dependence_toy_synthetic.csv)。1 月的冷而无风时段在四种情况下天气完全相同。

| 情况 | 1 月窗口的系统成本（亿欧元） | 占全年的比例 | 峰值影子价格（欧元/MWh） | 储氢罐（TWh） | 固定装机下 1 月的累计亏缺（TWh） / 峰值缺口（GW） |
|---|---|---|---|---|---|
| 基准 | 1079 | 39% | 90 500 | 167 | 75.7 / 397.5 |
| 储氢罐成本 × 4 | 3037 | 77% | 52 543 | 138 | 75.7 / 397.5 |
| 加入 60 GW 既有备用电厂 | 1087 | 39% | 61 906 | 137 | 75.7 / 397.5 |
| 1 月相同，2 月另有 20 天弱风 | 1075 | 34% | 90 500 | 307 | 75.7 / 397.5 |

- 只改成本假设，同一段天气的系统成本变为约 2.8 倍；同年 2 月更难时，1 月窗口的占比从 39% 降到 34%，按"占全年 35%"这类相对阈值就不再算事件。
- 固定装机后的累计亏缺和峰值缺口，在四种情况下都相同：它只取决于天气、需求和固定的装机。

## 3. 面向投资问题，事件要满足什么

- 调峰问题关心逐时的剩余负荷峰值和爬坡，时间尺度为小时到 1 天。
- 投资问题关心决定装机的量 [INFERENCE，依据 Grochowicz 2026 Table E1 的 4 类]：
  - 峰值缺口（GW）决定备用容量或可信容量；
  - 累计亏缺（TWh）决定储能电量；
  - 事件间隔决定储能能否充回；
  - 多国同时发生决定互联输电；
  - 这些量的重现水平决定按什么标准建设。
- 由此得到三条要求 [INFERENCE]：
  1. 阈值作用在**绝对量**（GW）上，不按季节去掉季节变化。夏季的资源距平，如果需求低，不会推动投资。
  2. 阈值在历史与未来之间**固定**，否则气候变化的信号会被阈值吸收。
  3. 一个事件要同时给出功率和能量两个量，才能区分功率缺口与能量缺口。

## 4. 候选定义（提议，[ASSUMPTION]，待先行检验，todo A11）

```
剩余负荷   RL_c,t = D_c,t − Σ_k Cap_k,c · CF_k,c,t − H_ror,c,t          (GW)
           c 国家或区域，t 小时，Cap 固定装机情景，k = 陆上风电、海上风电、光伏

参考供给   F_c = 历史全部记录中 RL_c 的某个分位数（多阈值：如 q90、q95、q98），未来沿用同一个 F_c

累计亏缺   S_c,t = max( 0 ,  S_c,t−1 + RL_c,t − F_c )                    (GWh)
           RL > F 时 S 增加（亏缺累积）；RL < F 时 S 减少（假定富余全部用于充回，效率 1）

事件       S_c,t > 0 的一段连续时间：S 离开 0 时开始，回到 0 时结束
           短暂缓解但没有把 S 清零的时段留在同一事件里 → 不需要另设合并间隔

特征       E   = max S_c,t                     储能电量需求          (TWh)
           P   = max (RL_c,t − F_c)            峰值缺口              (GW)
           P/E                                 功率型 ↔ 能量型
           持续时间、同时处于事件中的国家、季节、起始时间
```

- 这个递推式就是水库定容的序贯峰值算法（sequent peak algorithm）。
- 需要说明的假设：充回不受功率和效率限制（可以改为乘效率 η）；剩余负荷依赖一个固定的装机情景 Cap，装机情景要另做敏感性检验。

## 5. 需要先检验的前提

- Grochowicz 2026 写道，净负荷"can be used to determine severity of an extreme event, it is less suitable as a mode to identify extreme events"（Methods）；Grochowicz 2024 的结论相同（纯气象方法识别不出系统压力最大的事件）。
- 所以，选择投资问题后，Q3（数据定义的事件与 SDE 是否一致）是整个课题的前提，要放到第一步检验，不只是事后的验证。
- SDE 清单可能直接从 Zenodo 20590389 取得（todo B2）。Mopo 历史数据覆盖 1980–2021，与 SDE 的 1941–2021 重叠 42 年。

## 6. 可用于本课题的数据（补充研究计划第 6 节）

| 数据 | 内容 | 用途 |
|---|---|---|
| Grochowicz 2026 Zenodo + GitHub | SDE 清单与中间结果（具体文件待查） | Q3 的对照 |
| de Marco 2025 GitHub | CESM2 SSP3-7.0 2080–2100 的 60 年能源输入，含供热需求和水库来水 | 一个带需求和水电的未来数据集；只有一个模式 |
| Aminimehr 2026 Zenodo | 全球格点的风光干旱派生数据 | 用处小（只有风光，日尺度） |

## 7. 影子价格与"需求 × 影子价格"的含义（合成数据的玩具模型）

- 脚本 [shadow_price_toy_lp.py](../ai_workspace/event_definition/scripts/shadow_price_toy_lp.py)，图 [shadow_price_toy_lp_synthetic.png](../ai_workspace/event_definition/figures/shadow_price_toy_lp_synthetic.png)。数据为合成数据：一个节点，一年（7 月至次年 6 月），技术为风、光、电解槽 + 储氢 + 燃料电池，1 月插入 12 天冷而无风的时段。
- 计算结果：
  - 总成本 276.82 bn EUR，全年 Σ d·λ 也是 276.82 bn EUR，两者相等；
  - 风、光、储氢链各自按 λ 计算的收入，都等于各自的年化成本（160.40、19.01、97.41 bn EUR）；
  - 峰值小时 λ = 90 500 EUR/MWh，等于燃料电池每 MW 的年化投资 90 000 加上储能电量价值 500；把这一小时的需求加 10 MWh 后重新求解，成本的增量除以 10 也是 90 500；
  - 事件期间 λ = 500 EUR/MWh，等于储氢罐 250 EUR/MWh/年 ÷ 燃料电池效率 0.5；
  - 成本最高的 14 天窗口占全年 Σ d·λ 的 39%，燃料电池收入的 62% 在这个窗口内取得。
- Grochowicz 2024 的原文说明（§2.2、§3）：对偶值"indicate how much the objective function would decrease if the corresponding constraint was relaxed by one unit"；影子价格"largely driven by the need for renewable expansion in the model, not marginal operating costs"；全年 Σ d·λ 是模型中电力的总价值，与总系统成本的差别只来自既有设施。
