# 会议页面讲解（中文）：`presentation/2026-11-10_Matti_meeting.html` 逐页说明

- 日期：2026-11-10
- 用途：让讲的人自己先完全看懂页面上的每个词和每句话。页面本身是英文的，给 Matti 看。
- 结构：第 0 节缩写总表；第 1 节讲 6 个核心概念，这是看懂后面所有内容的前提；第 2 节逐页详解，包括每篇引用文献研究了什么、结论、原因、数字和阅读范围；第 3 节是会前需要先想清楚的一个问题。
- **2026-11-10 第二次改版**：页面现为 4 页：第 1 页 Motivation，第 2 页两个科学问题，第 3 页 Q1（原 T3，从大陆到岛屿需要多少数据），第 4 页 Q2（原 T4，岛屿降尺度选年）。原 Q1（原 T2，代表性子集是否保住极端）已删除，因为它的两个前提都不成立，详见第 2 节"原 Q1"一节。两个问题都加了"Why it matters"。
- **2026-11-10 第一次改版**：会议页面只讨论科学问题，当时为 5 页：第 1 页 Motivation，第 2 页三个科学问题，第 3–5 页为 Q1–Q3。原来的 T1（路径空间压缩，是方法而不是科学问题）已从页面删除，标为**稍后讨论**；Q1 = 原 T2，Q2 = 原 T3，Q3 = 原 T4。各页的"候选算法"也已从页面删除，本文件中相应内容标为**稍后讨论**。
- 更新：2026-11-10 加入第 0 节和第 2 节详解；改正了 Mopo 数据量（原写约 0.9 TB 是 Zenodo 下载量统计）和第 1 页一处引用（Psarros 2023 换为 Fernández-Muñoz & Pérez-Díaz 2021）。
- 术语以 `French_2026/glossary/climate_energy_glossary_zh_en_fr.md` 为准，第一次出现时括号里给英文。

---

## ★ 会议页面定稿版说明（2026-11-10，请先读这一节）

页面 `presentation/2026-11-10_Matti_meeting.html` 现为 4 页：1 Motivation；2 Q1 空间；3 Q2 时间；4 讨论（提问 + 下游用途表）。以下逐页解释页面上每一句的含义、出处、数字的条件和阅读范围。后面第 0–3 节是早先版本的讲解，保留供参考；其中的"Q1、Q2"编号与这里不同，以本节为准。

### 文献重读记录（2026-11-10）

重读范围：Zotero 集合 `Projects/Time_Series_2026` 中的 19 篇全文，加上开放获取下载的 Frysztacki 2021、Reichenberg & Hedenus、Climate2Energy、Hawkins & Sutton 2012 全文；Jerez 2019、St. Martin 2015 只读到摘要。

| 文献 | 阅读范围 | 页面用到的说法 | 核对结果 |
|---|---|---|---|
| Pfenninger 2017, Appl. Energy 197:1 | full text | 同一英国模型、只换天气年：2014 年数据得海上风电 41.8 GW，2012 年得 55.9 GW | 与原文 Table 6、7 标题一致；条件是"90% 可再生"情景、逐时参考模型 |
| Ruhnau & Qvist 2022, ERL 17:044018 | abstract（两个开放链接都没返回 PDF） | 35 年记录中最大能量亏缺跨越 9 周 | 一致；注意计入储能损耗和充电限制后，决定储能的时段长达 12 周，页面用的是"最大能量亏缺"这一项 |
| Grochowicz et al. 2023, Energy Econ. 118:106496 | full text（arXiv） | 每国一节点、41 年、3 小时步长已到计算可行性极限 | 一致；原文没有给出运行时间数字 |
| St. Martin, Lundquist, Handschy 2015, ERL 10:044004 | abstract | 风速站间相关随距离下降；时间尺度越短，相关长度越短 | 一致：高通滤波时间常数短于约 38 h 时，相关长度至少按 τ⁻¹ 减小；数据为澳大利亚 29 个风电场、加拿大 117 站、美国西北 14 塔 |
| Kotzur et al. 2018a, Renew. Energy 117:474 | full text（arXiv） | 区域序列比单点序列容易聚合 | 一致（结论部分原文） |
| Frysztacki et al. 2021, Appl. Energy 291:116726 | full text（arXiv） | 欧洲模型跑到 1024 个节点 | 一致：37 到 1024 节点；只看资源分辨率时成本最多降 10%；网络分辨率低时忽略阻塞，成本低估 23% |
| Bodini et al. 2016, WES 1:115 | full text | 年际持续性使年容量因子 90% 范围宽 3 倍（加拿大 60 站） | 一致：CF 0.35、年际变率 6% 时，预期 0.32–0.38，实测 0.27–0.43 |
| Hawkins & Sutton 2012, GRL 39 | full text | 气候信号超过自然变率时"出现" | 一致：ToE 定义为信噪比 S/N 首次超过阈值（如 1 或 2）的年份；各模式估计的年际变率标准差可差 3 倍 |
| van Duinen et al. 2026, Appl. Energy 427:129090 | 约 1/3 原文 + 检索全文关键句 | 2016–2045 窗内假设没有趋势 | 一致；页面已收窄为"一项近期研究"，不推广为通行做法 |
| Jerez et al. 2019, Renew. Energy | abstract（HAL 链接没返回 PDF） | 风光合计变率的预估变化低于 ±5% | 一致：比较 2070–2099 与 1971–2000，区域和全欧尺度，"overall negligible (well below ±5%)" |
| Wohland et al. 2025, Environ. Res. Energy 2:041001（Climate2Energy） | full text（arXiv） | 供热需求 −10% 到 −50% | 一致：CESM2、SSP3-7.0；另有南欧水电 −10% 到 −40%、制冷需求增加超过 100%；芬兰光伏 CF 变化随成员在 −1% 到 +4% 之间 |

**重读中发现、需要记住的三点**
1. **Reichenberg & Hedenus 的区域结论主要反映模型性质**：全文中作者认为，区域装机结构偏差大，很可能因为"很多区域配置都接近最优"（最优点附近目标函数平坦）。所以它不能作为"小区域的数据需要更多时段"的证据，已从定稿页面删去。另外，它的正式出版信息是 Energy Systems 15:215–232（2024），2022 年在线发表。
2. **再分析会高估空间相关**：Murcia et al. 2022（DTU，全文）显示，风速空间相关长度普遍被高估，ERA5 高估 21%；1 小时爬坡的空间相关被高估更多。Luzia et al. 2023（DTU，全文）也发现，大多数 EURO-CORDEX 模式高估空间相关。所以 Q1 的尺度规律会受数据源影响，要比较 ERA5、CorRES（加了随机波动）和实测。
3. **Tapachès 2019 现在读了全文**：Réunion 面积 2512 km²，最大尺度不超过 70 km；用 2011 年 34 个日射表和卫星（5.4 km 像元）的逐时 GHI，比较不同平均范围下的光伏波动。这正是 Q1 在岛屿尺度上的一个现成例子（只有光伏、只有一年）。

### 第 1 页 Motivation

| 页面内容 | 解释 |
|---|---|
| "Many years are needed" | 两个例子：只换天气年，同一模型的海上风电结果从 41.8 GW 变成 55.9 GW（Pfenninger 2017）；储能由跨数周的累计亏缺决定（Ruhnau & Qvist 2022） |
| "Long records strain models" | 41 年、3 小时、每国一节点已到计算极限（Grochowicz 2023）。没有写"模型只能用几年"，因为 Gøtske 2024 用了 62 年（逐年分别优化） |
| "Part of the record is redundant" | 日循环和季节循环每年重复，这是事实；冗余有多大要测量，页面明确写成待测 |
| Aim | 两个问题合起来：需要多少数据（Q1，随空间尺度），全记录本身多可靠（Q2） |

### 第 2 页 Q1 空间

**直白地说**（页面上新加的一句）：科西嘉的风光序列是否比全欧洲的需要更多代表日？多多少？这个差别能否预测？

| 页面内容 | 解释 |
|---|---|
| 问题 | 对不同大小区域的空间平均（加总）序列，求所需的最少代表性时段 k\*，并检验能否由数据性质预测。缩减在时间上，空间平均范围是研究变量 |
| Known 1（St. Martin 2015） | 物理基础：站点距离越远相关越弱；短时间尺度的波动相关长度更短，所以较小的区域就能平滑短时波动。推论（待检验）：k\* 由"区域尺度 ÷ 各时间尺度上的相关长度"决定 |
| Known 2（Kotzur 2018a） | 区域加总比单点容易聚合，方向一致，但没有给出随面积变化的定量关系 |
| Open | 两次检索（OpenAlex + 扩展网页检索）都没有找到 k\* 随平均范围变化的定量研究；非穷尽，正式提出前要查 Scopus 和 Web of Science |
| Why it matters | 模型已能做到 1024 个节点（Frysztacki 2021），细分辨率需要知道每个区域要多少时段；岛屿规划需要"多少数据才够"的规则 |
| Input → Reduce → Output | 输入是不同平均范围的逐时需求、风、光序列（含 Réunion CorRES_2026）；每个区域单独求能保住分布、干旱、亏缺、爬坡的最少时段；输出 k\* 和它与面积的关系 |
| Expected（假设） | 面积小于相关长度后 k\* 增加，爬坡（短时间尺度）增加最多；依据是 St. Martin 2015 的时间尺度依赖，属推断 |
| Check | 在欧洲区域上拟合，预测 Réunion |
| 没写在页面上的风险 | 再分析高估空间相关（Murcia 2022、Luzia 2023）；k\* 依赖选法，需估计"可达到的最小 k\*"（方法，稍后讨论）；光伏和风电的规律可能不同（Tapachès 2019） |

### 第 3 页 Q2 时间

**2026-11-10 改写：页面上 Q2 分成两部分，并配了示意图（合成数据，不是结果）**：`ai_workspace/meeting_page/figures/Q2_illustration_synthetic.png`，脚本 `ai_workspace/meeting_page/scripts/q2_illustration.py`。

**直白地说**：所有缩减都拿"全记录"（如 1950–2024 年共 75 年）作标准答案。这个标准答案可能出两种问题：
1. **记录不够长**（Part 1）。75 年也只是天气的一次"抽样"，换一组 75 年，估出来的统计量会不一样。平均值很快稳定，但"20 年一遇的风光干旱"这种极端，每 20 年才出现一次左右，75 年里只有三四次，估计误差大。年际持续性还会让误差更大 [Bodini 2016, full text]。
2. **气候在变**（Part 2）。过去 75 年的统计规律，不一定适用于 2030–2060 年。问题是这种变化够不够大：如果比第 1 点的抽样误差还小，就测不出来，历史数据和一组固定代表期都可以继续用；如果超过了，就要改用气候预估数据，或者让代表期的权重随时间变化。

**要算的量**

```
 Part 1：记录长度
   θ        某个统计量（如平均容量因子、20 年一遇干旱的持续时间）
   θ̂(n)    用 n 年记录估出的 θ
   s(n)     θ̂(n) 的不确定性：从全记录中按整年分块重抽样，看 θ̂(n) 的离散程度（相对 θ 的百分比）
   n*       = min { n : s(n) ≤ ε }     达到目标精度 ε 需要的年数

 Part 2：气候变化
   Δθ(t)    以 t 为中心的 30 年窗口内的 θ，相对今天的变化（来自气候预估）
   ToE      = 第一个满足 |Δθ(t)| > 2 · s(30) 的年份     （"出现时间"，信噪比 > 2）
```

**示意图怎么读**（数字全是合成的）：
- 左图：误差随记录长度下降，均值下降得快，示意中 6 年就达到 5% 精度；极端下降得慢，示意中要 54 年。
- 右图：灰带是 30 年记录的噪声（示意 ±4.5%）。"类似需求"的统计量在示意的 2043 年离开灰带，"类似风光变率"的一直在带内。这对应 Jerez 2019（风光合计变率的变化低于 ±5%）和 Wohland 2025（供热需求 −10% 到 −50%）的方向，但图中数字不是这两篇的结果。

**和 Q1 的关系**：Part 1 的 s(n) 就是 Q1 判断"缩减后够不够"所需的阈值：缩减后的误差小于全记录自身的抽样误差，就算足够。


| 页面内容 | 解释 |
|---|---|
| 问题 | 两部分：① 记录要多长，缩减需要保住的统计量（年际方差、干旱重现水平、跨数周亏缺）才稳定；② 在规划时间窗内，气候变化信号是否超过这种抽样噪声，使一组固定代表期失效 |
| Known 1（Bodini 2016） | 年际持续性使多年统计量的不确定性比"各年独立"大得多（加拿大单站风速，90% 范围宽 3 倍）；欧洲区域能源序列的持续性要用本项目数据重新估计 |
| Known 2（Hawkins & Sutton 2012） | 出现时间（ToE）：信噪比首次超过阈值的年份。这一部分在气候科学中已成熟，Q2 不重复，只借用这一框架 |
| Known 3（van Duinen 2026） | 一项近期选年研究在 2016–2045 窗内假设无趋势；没有推广成"所有选法都这样" |
| Open | ① 欧洲能源统计量（含干旱）需要多长记录；② ToE 与缩减设计的联系（固定代表期的有效期）。两次检索未找到，非穷尽 |
| Why it matters | Q2 给所有缩减（含 Q1）提供参照和误差阈值；变化因变量而异：风光合计变率的预估变化低于 ±5%（Jerez 2019，2070–2099 对 1971–2000），供热需求 −10% 到 −50%（Wohland 2025，SSP3-7.0）；另有 DTU 的 Luzia 2023 发现 RCP8.5 下 2026–2065 年多数国家容量因子轻微下降（页面未列） |
| Input → Reduce → Output | PECD 4.2 的 ERA5 1950–2024 与气候预估、Réunion CorRES_2026；截取 5 到 75 年的记录、在预估中用滑动窗；输出每个统计量需要的年数，以及固定代表期能用多久 |
| Expected（假设） | 均值约十年稳定、干旱需要长得多；固定代表期对风光比对需求和水电更持久。"约十年"只是假设，没有文献支持 |
| Check | 用多模式拼接的长序列作已知真值；岛屿应用：Réunion 选哪几年降尺度 |
| 风险 | ERA5 早年数据质量和趋势；各模式的年际变率估计可差 3 倍（Hawkins & Sutton 2012），"噪声"本身不确定 |

### 第 4 页 讨论

| 页面内容 | 解释 |
|---|---|
| 提问 | 两个问题中哪个对 DTU 现在更有用；由 DTU 的哪种用途来决定缩减后必须保留什么 |
| 下游用途表 | 每种用途对应必须保留的特性；这是讨论用的对照表，不是研究结论 |

---

## 0. 缩写总表

| 缩写 | 全称 | 中文 | 在本课题中的含义 |
|---|---|---|---|
| TSA | time series aggregation | 时间序列聚合 | 把长序列缩减为少量代表性时段的方法总称 |
| VRE | variable renewable energy | 变动性可再生能源 | 风电、光伏这类出力随天气变化的电源 |
| PECD | Pan-European Climate Database | 泛欧气候数据库 | C3S 与 ENTSO-E 联合发布，4.2 版含 1950 年起的 ERA5 历史序列和到 2100 年的气候预估；风电部分由 DTU CorRES 生成 |
| C3S | Copernicus Climate Change Service | 哥白尼气候变化服务 | 欧盟气候数据服务，PECD 的发布方 |
| ERA5 | ECMWF Reanalysis v5 | 第五代 ECMWF 再分析资料 | 全球逐时再分析，约 0.25°（约 28 km） |
| CMIP6 | Coupled Model Intercomparison Project Phase 6 | 第六次耦合模式比较计划 | 全球气候模式的气候预估来源 |
| SSP | Shared Socioeconomic Pathway | 共享社会经济路径 | 排放情景，如 SSP2-4.5、SSP5-8.5 |
| GCM | global climate model | 全球气候模式 | 如 MPI-ESM1-2-HR、EC-Earth3 |
| ENTSO-E | European Network of Transmission System Operators for Electricity | 欧洲输电系统运营商联盟 | 发布实测负荷、发电、电价、潮流，并做 ERAA 和 TYNDP |
| ERAA | European Resource Adequacy Assessment | 欧洲资源充裕度评估 | ENTSO-E 每年做的供电充裕度评估，需要挑选气候年 |
| TYNDP | Ten-Year Network Development Plan | 十年电网发展规划 | ENTSO-E/ENTSOG 的规划，2026 版用 k-medoids 选天气年 |
| TSO | transmission system operator | 输电系统运营商 | 如 RTE、TenneT |
| DTU | Technical University of Denmark | 丹麦技术大学 | Matti 所在单位 |
| CorRES | Correlations in Renewable Energy Sources | — | DTU 的风光出力与预测误差模拟工具 |
| Mopo | — | — | Horizon Europe 项目（2023–2026，VTT 牵头，DTU 参与），发布泛欧逐时风光数据和规划工具 |
| Balmorel | — | — | 开源的电力与供热系统规划模型，DTU 参与开发；pybalmorel 是它的 Python 工具包 |
| tsam | time series aggregation module | — | 开源的时间序列聚合 Python 包，pybalmorel 的聚合功能基于它 |
| SpineOpt | — | — | Mopo 使用的开源能源系统模型 |
| PyPSA-Eur | Python for Power System Analysis – Europe | — | 开源欧洲电力（及多部门）系统模型；Grochowicz、Gøtske 用它 |
| Calliope | — | — | 开源能源系统建模框架；Pfenninger 2017 用它 |
| NUTS0 / NUTS2 | Nomenclature of Territorial Units for Statistics | 欧盟统计地域单元 | NUTS0 为国家级，NUTS2 为大区级（如 Corse、Sardegna） |
| GWA | Global Wind Atlas | 全球风能图谱 | 用于订正 ERA5 风速的高分辨率平均风速 |
| WRF | Weather Research and Forecasting model | — | 区域数值天气模式，用于动力降尺度 |
| CF | capacity factor | 容量因子 | 实际出力 ÷ 装机容量，0–1 |
| LCOE | levelized cost of electricity | 平准化度电成本 | 单位发电量的全生命周期成本 |
| P50 | — | — | 风资源评估中的长期年发电量中位数估计 |
| MMD | maximum mean discrepancy | 最大均值差异 | 两个分布之间的核距离，见 1.3 节 |
| RKHS | reproducing kernel Hilbert space | 再生核希尔伯特空间 | MMD 误差上界所适用的函数空间 |
| SWD / SSWD | sliced Wasserstein distance / seasonal SWD | 切片 Wasserstein 距离 / 季节切片 Wasserstein 距离 | van Duinen 2026 的选年准则 |
| SA | simulated annealing | 模拟退火 | 一种全局优化算法 |
| TMY | typical meteorological year | 典型气象年 | 逐月挑最接近长期分布的月份拼成一年 |
| KS | Kolmogorov–Smirnov | 科尔莫戈罗夫-斯米尔诺夫 | 两分布的最大累积概率差 |
| W₁ | Wasserstein-1 distance | Wasserstein 距离 | 两条累积分布函数之间的面积 |
| EVT | extreme value theory | 极值理论 | 描述超过高阈值部分的统计理论 |
| GPD | generalized Pareto distribution | 广义帕累托分布 | EVT 中超阈值量的分布 |
| KKZ | Katsavounidis–Kuo–Zhang algorithm | — | 选出覆盖集合范围的成员的算法（Cannon 2015 使用） |
| PCA | principal component analysis | 主成分分析 | 求数据的主要变化模态 |
| MODWT | maximal overlap discrete wavelet transform | 最大重叠离散小波变换 | 把序列按时间尺度分解 |
| ESS | effective sample size | 有效样本量 | 见第 2 节 van Duinen 2026 的定义 |
| D_max | maximum cumulative deficit | 最大累计亏缺 | 剩余负荷连续累加的最大值，决定长时储能规模 |
| d_eff | effective dimension | 有效维数 | 由 PCA 特征值算出，见 1.6 节 |
| n_eff | effective number of years | 有效年数 | 年际相关时的独立年份数，见 1.6 节 |
| k\* | required subset size | 所需子集大小 | 见 1.6 节 |
| SOM | self-organizing map | 自组织映射 | 一种聚类神经网络（Yeganefar 2020 使用） |
| ML | machine learning | 机器学习 | |
| ToE | time of emergence | 出现时间 | 气候变化信号首次超过自然变率的年份（Hawkins & Sutton 2012） |
| S/N | signal-to-noise ratio | 信噪比 | ToE 的判据 |
| CESM2 | Community Earth System Model version 2 | — | Climate2Energy 使用的气候模式 |
| RCP | Representative Concentration Pathway | 典型浓度路径 | CMIP5 时代的情景，如 RCP8.5 |

---

## 1. 六个核心概念

### 1.1 代表性时段与权重（representative period, weight）

- **是什么**：从全部数据中挑出 k 个真实的时段（天、周或整年），每个时段配一个权重 w_j，表示它代表全集合里多大比例的时段。
- **怎么用**：下游模型只算这 k 个时段，再把结果按权重加起来，得到"全年"或"全部年份"的近似值。

```
 全集合：N 个时段 x_1 … x_N（例：40 年逐日，N = 14 610）
 子集：  k 个时段 s_1 … s_k，权重 w_1 … w_k，  w_j ≥ 0，Σ w_j = 1

 任意按时段平均的量 f（如日发电量）：
            1   N                        k
   全集合：  ─── Σ f(x_i)   ≈   子集：   Σ  w_j · f(s_j)
            N  i=1                      j=1
```

例：k = 30 个代表日、权重相等时，每个代表日代表 14 610 ÷ 30 ≈ 487 个真实日。

### 1.2 数值分布与路径（distribution vs path）

- **数值分布**：只看出现过哪些数值、各占多少比例，不管先后顺序。负荷持续曲线（load duration curve）和 KS 检验比较的就是这个。
- **路径**（样本路径，sample path）：一个时段内多个变量随时间变化的整条轨迹，保留先后顺序。

```
 一天的路径：t ↦ ( 需求(t), 风电(t), 光伏(t), 水电来水(t) … ),  t = 0 … 23 h
```

- **区别**：同样 24 个小时值，顺序不同，数值分布完全一样，但爬坡、峰值时刻、低值持续时长完全不同。见合成数据示意图 `ai_workspace/concepts/figures/path_vs_distribution_synthetic.png`：两天的 KS 距离为 0，但滞后 1 小时自相关分别为 0.96 和 −0.10，最大爬坡分别为 14 和 56 MW/h。
- **结论**：储能、爬坡和备用取决于路径，不只取决于数值分布。所以页面上说"按路径匹配"（match the law of paths），意思是子集中各天的整条轨迹的分布要和全集合一致。

### 1.3 核函数与 MMD（kernel, maximum mean discrepancy）【方法，稍后讨论；明天不讲】

**核函数**：一个给两个时段打"相似度分数"的函数。最常用的高斯核：

```
                       ‖x − y‖²
 k(x, y) = exp( − ─────────── )        ‖x − y‖ = 两个时段对应时刻差值的欧氏长度
                        2 σ²
 两天完全相同 → k = 1；两天差别很大 → k → 0；σ 决定"多大差别算大"
```

**MMD**（最大均值差异）：衡量"全集合"和"加权子集"两个分布的差距：

```
          1    N   N                      2   N   k                       k   k
 MMD² = ───── Σ   Σ  k(x_i, x_i')  −  ─── Σ   Σ  w_j k(x_i, s_j)  +   Σ   Σ  w_j w_j' k(s_j, s_j')
          N²  i=1 i'=1                    N  i=1 j=1                     j=1 j'=1

        全集合内部的平均相似度        全集合与子集之间的相似度         子集内部的平均相似度
```

- **怎么读**：子集和全集合的分布越接近，三项越平衡，MMD 越接近 0。用高斯核时，MMD = 0 当且仅当两个分布完全相同。
- **为什么有用（误差保证）**：对于任何"足够光滑"的、按时段计算再平均的量 f，满足

```
 | 全集合平均 f − 子集加权平均 f |  ≤  ‖f‖ × MMD
```

  其中 ‖f‖ 是 f 在再生核希尔伯特空间（RKHS）中的范数，可以理解为"f 有多不光滑"的定量尺度。这个性质来自 Gretton et al. 2012 [abstract only]。
- **含义**：只要报告一个 MMD 数值，就同时给出了一整类用途的误差上界，不需要知道下游模型是什么。这就是页面上说的"certificate"（误差证书）。
- **局限**：只覆盖"按时段平均"的光滑量。像"多年中最长的一次干旱"或"整个序列的最大累计亏缺"这类依赖整段序列的极值量，不在保证范围内，所以需要 T2。

### 1.4 怎样选出子集：kernel herding、kernel thinning、support points【方法，稍后讨论；明天不讲】

这三种都是"让子集的 MMD（或能量距离）尽量小"的算法，暂无通行中文译名。

| 算法 | 做法 | 来源 |
|---|---|---|
| kernel herding | 贪心：从空集开始，每一步从全集合中挑一个能让 MMD 下降最多的时段加入，重复 k 次 | Chen, Welling, Smola 2010 [abstract only] |
| kernel thinning | 大致做法：反复把集合对半分，按核函数决定每对点保留哪一个，直到剩 k 个，最后再微调；摘要称其压缩效果优于独立随机抽样。具体步骤只读了摘要，要看全文确认 | Dwivedi & Mackey 2021 [abstract only] |
| support points | 用能量距离（energy distance）代替 MMD，求使能量距离最小的 k 个点 | Mak & Joseph 2018 [abstract only] |

选完时段后，权重 w_j 用一个小的二次规划求：在 w_j ≥ 0、Σ w_j = 1 的约束下使 MMD² 最小（MMD² 对 w 是二次函数）。

**本课题新在哪里**：这三种方法原本用于互相独立的点，例如 MCMC 样本；还没有找到把它们用于"带时间顺序的多变量能源时段"的研究。两次检索都没有找到，但检索不是穷尽的。

### 1.5 signature 核（signature kernel）【方法，稍后讨论；明天不讲】

**问题**：高斯核把一天的 24 个小时值当作 24 维向量比较，只看逐时刻的差值，对"先涨后跌还是先跌后涨"这类顺序信息不敏感。

**路径签名**（path signature）：用沿时间的迭代积分描述一条路径。以两个变量 X¹（如风电）、X²（如需求）为例：

```
 一阶项：  S¹ = ∫ dX¹ = X¹(终) − X¹(始)          （总变化量）
 二阶项：  S¹² = ∫∫_{s<t} dX¹(s) dX²(t)          （X¹ 先变、X² 后变的累积量）

 S¹² − S²¹ = 两条曲线围成的有向面积的 2 倍
           → 风电先降、需求后升，与需求先升、风电后降，这一项符号相反
```

- **作用**：阶数越高，记录的顺序信息越细。把时间本身也作为一个通道加进去后，完整的签名在相差一个平移的意义上唯一确定一条路径。这一条来自粗糙路径理论（rough path theory），所引文献不在本项目已核对的文献里，引用前要核实。
- **signature 核**：两条路径签名的内积，相当于"按整条轨迹（含顺序）比较的相似度"。用它算 MMD，比较的就是路径的分布。
- **怎么算**：Salvi et al. 2021 证明可以通过解一个偏微分方程（Goursat 问题）直接计算，不必展开签名 [abstract only]；有 Python 实现，具体软件包待核实。
- **代价**：计算量随时段数的平方增长。40 年逐日约 1.5 万个时段，需要截断或低秩近似。

### 1.6 另外几个页面上出现的量

| 量 | 定义 | 单位或范围 |
|---|---|---|
| KS 距离 | 两条累积分布函数之间的最大竖直差：D = max_v \|F(v) − F̃(v)\| | 0–1，无量纲 |
| Wasserstein 距离 W₁ | 两条累积分布函数之间的面积：W₁ = ∫ \|F(v) − F̃(v)\| dv | 与变量同单位，如 MW |
| 切片 Wasserstein（sliced Wasserstein） | 把多变量数据投到很多随机方向上，每个方向算一维 W₁，再取平均；van Duinen 2026 用的就是它，按冬、夏季分别算，取较大值 | 同上 |
| 剩余负荷（residual load） | r_t = 需求 − 风光发电 | MW |
| 最大累计亏缺 D_max | r_t 在某一连续区间上累加的最大值，即储能最多需要补的能量 | MWh |
| 有效维数 d_eff | 由主成分分析的特征值 λ_i 算出：d_eff = (Σλ_i)² ÷ Σλ_i²。只有 1 个主导模态时 d_eff = 1；p 个模态同样重要时 d_eff = p | 1 到变量数 |
| 有效样本量 n_eff | 年际有正相关时，n 年里独立信息相当于 n_eff 年：n_eff = n(1 − ρ₁)/(1 + ρ₁)，ρ₁ 为相邻年份年均值的相关系数 | 年 |
| 广义帕累托分布 GPD | 超过高阈值 u 的部分 y = X − u 近似服从 P(Y ≤ y) = 1 − (1 + ξy/σ)^(−1/ξ)；ξ 为形状参数，决定尾部多"重"，σ 为尺度参数 | ξ 无量纲，σ 与变量同单位 |
| 重现水平 | 平均每 T 年被超过一次的数值，由 GPD 参数算出 | 与变量同单位 |
| 块置换检验 | 把"全集合"和"子集"的标签按整年为单位随机打乱，重算 MMD 很多次；原始 MMD 大于多少比例的打乱结果，就得到 p 值 | p 值 0–1 |
| 小波变换（MODWT） | 把序列分解成不同时间尺度的分量（约 1–2 h、2–4 h、…、数周），各分量方差之和等于原序列方差 | 每个尺度一个分量 |
| k\* | 在给定时段长度 L、区域、方法和用途下，使所需统计量都落在阈值内的最小 k，且 k 再增大时一直满足 | 时段个数 |

---

## 2. 逐页详解

每条引用都按同一格式写：**研究对象**（数据、区域、模型）→ **结论** → **原因** → **数字**（含定义和条件）→ **阅读范围**。阅读范围为 [abstract only] 或 [snippet] 的文献，不能用来支撑摘要里没有的细节。

### 第 1 页：为什么要缩减多年代的能源与电力时间序列

**本页缩写**：TSA、VRE、PECD、ERA5、CMIP6、SSP、ENTSO-E、ERAA、TYNDP、Mopo、CorRES、tsam、PyPSA-Eur、Calliope、LCOE、CF（见第 0 节）。

**流程框的含义**
- **Data**：两类数据。① 气候驱动的序列：PECD 4.2 的风、光、水电、温度，从 1950 年起到 2100 年；CorRES 和 Mopo 的逐时风光出力。② 实测序列：ENTSO-E 发布的负荷、分类发电、电价、跨境潮流，只覆盖它开始发布以来的年份，没有几十年。
- **Models**：容量扩展、充裕度评估、机组组合等模型，通常只能在逐时分辨率下算几年。
- **Reduction**：从全部时段中挑出带权重的代表性时段。
- **Open question**：挑到多少才算够，对哪种用途够。

#### 第 1 栏 "Many years are needed"

**Pfenninger 2017**（Applied Energy 197:1–13）[full text]
- **研究对象**：英国（Great Britain）电力系统规划模型，用 Calliope 框架，20 个区域；输入为 1990–2014 年共 25 年的逐时风电、光伏模拟出力。比较三类降分辨率方法：降采样（如 6 小时一步）、聚类（k-means、层次聚类）、启发式选极端日。
- **结论 1：同一日历日的风电在不同年份差别极大**。原文："The average UK wind capacity factor can range from close to zero to almost one on the same calendar day across the 25 years"（§4.2.1）。也就是说，同一天的全英平均风电容量因子，在 25 年中可以从接近 0 变到接近 1。
- **结论 2：用不同单一年份做规划，结果相差很大**。在"90% 可再生"情景下（全时段至少 90% 的发电来自风光），同一模型、同样的逐时分辨率：
  - 用 2014 年数据：海上风电装机 41.8 GW，系统 LCOE 0.18 GBP/kWh（Table 6 标题）；
  - 用 2012 年数据：海上风电装机 55.9 GW，LCOE 0.19 GBP/kWh（Table 7 标题）；
  - 两者相差 14.1 GW，相当于 2014 年结果的 34%（这个差值和百分比是我根据两张表的标题算的，原文没有直接给出）。
  - 对 25 个年份分别做规划，海上风电装机分布很宽；去掉 1991 年这个离群年后，其余年份仍跨越 30 GW 的范围（§4.2.3）。
- **结论 3：在一年上验证过的聚类方法，在其他年份可能失效**。k-means 选 5 个典型日的方法"在某些年份表现好，在其他年份误差很大"，所以"只用一年数据验证聚类方法，会错误地高估它的稳健性"（§4.2.2）。
- **原因**：装机规模按当年的风光资源来定。资源年际差别大，按某一年设计的系统换一年就不再最优，甚至供电不足。可再生比例越高，这种影响越大：在 50% 情景下 6 小时分辨率的结果仍可接受，90% 情景下各方法之间的差别明显变大。
- **作者结论**："Model results with high shares of PV and wind generation using a single or few years of data are likely unreliable"（摘要）。

**Ruhnau & Qvist 2022**（Environ. Res. Lett. 17:044018）[abstract only；IOP 和 EconStor 的 PDF 链接都下载失败]
- **研究对象**：德国 100% 可再生电力系统，35 年逐时数据；同时做时间序列分析和系统成本优化。
- **结论与数字**（全部来自摘要）：
  - 持续稀缺期（风光都少）本身不超过 2 周；
  - 但最大能量亏缺跨越 9 周，因为几个稀缺期接连出现；
  - 计入储能损耗和充电功率限制后，决定储能规模的时段长达 12 周；
  - 这期间成本最优的储能需要供出 36 TWh 电量，约为最稀缺 2 周能量亏缺的 3 倍；储能主要是盐穴储氢，因为再发电有损失，库容为 55 TWh；
  - 只用单一年份优化时，储能需求的年际差别很大，"平均年份"需要的储能不到用全部 35 年算出的一半。
- **原因**：储能规模由连续若干周的累计亏缺决定，不由单个最坏的一天或一周决定；单一年份往往不含最长的那段累计亏缺。
- **对本课题的意义**：缩减时如果只保留分布、打乱时间顺序，就看不到这种"接连出现"的结构。这是 T2 关注累计亏缺 D_max 的依据。

**Kittel & Schill 2026**（Commun. Earth Environ. 7）[full text, arXiv v4]
- **研究对象**：38 个历史天气年（1982/83–2019/20）、欧洲 33 国的陆上风电、海上风电、光伏可用率逐时序列。干旱定义为可用率的滑动平均低于某个阈值（以长期平均的比例表示）的时段。数据集出自原文参考文献 [53]，具体来源未核对。
- **结论 1**：干旱的频率、持续时间、严重程度强烈依赖所选阈值，所以只用一个阈值的分析不可靠；作者用一系列阈值做分析。
- **结论 2**：风光组合（portfolio effect）和跨国平衡（balancing effect）能显著减少干旱。
- **结论 3（数字）**：在"全欧完全互联"的理想情形下，最极端的一次干旱发生在 1996/97 年冬季，持续 55 天，期间可再生可用率平均仍有长期平均的 47%。
- **结论 4**：这类决定储能的极端干旱会跨越新旧年之交，所以"以单一日历年为规划时段"不适合研究气候稳健的能源系统。
- **对本课题的意义**：选时段时，时段边界不能硬切在 1 月 1 日；这是计划中按"水文年"（4 月 1 日至 3 月 31 日）切分的依据之一。

**Gøtske et al. 2024**（Nat. Commun. 15:10680）[full text, arXiv v2]
- **研究对象**：PyPSA-Eur 多部门（电力、供热、交通、工业）欧洲模型，净零排放；用 1960–2021 年共 62 个天气年，每年各优化一次装机布局，再把每个布局放到所有 62 年里运行，检验充裕度和排放。
- **数字**：
  - 全部设计年平均系统成本 8030 亿欧元/年；最贵和最便宜的布局相差 ±10%；
  - 年风资源与系统总成本强负相关（r = −0.81），光伏较弱（r = −0.39）：风大的年份需要的风机少，所以成本低。
- **结论**：最贵的布局排放最低，但充裕度不是最高；用含"复合天气事件"的年份设计的布局最稳健、性价比最好；加一些排放 CO₂ 的备用电源是便宜的稳健措施，平均排放仍低于 1990 年的 1%。
- **对本课题的意义**：天气年的选择直接改变成本和设计；而"最有代表性"与"最稳健"不是一回事，这对应 L6 范围覆盖与 L2 分布匹配的区别。

#### 第 2 栏 "Models cannot take them all"

**Grochowicz et al. 2023**（Energy Econ. 118:106496）[full text, arXiv]
- **研究对象**：PyPSA-Eur 欧洲电力系统，每国一个节点，3 小时分辨率，41 个天气年（ERA5 再分析，经 Atlite 算容量因子）。
- **原文**："While an optimisation with 41 weather years is at the limits of computational feasibility, we use the near-optimal feasible spaces of single years …"（摘要）。所以作者没有一次性优化 41 年，而是每年单独算"近优解空间"，再求交集。
- **数字**：原文没有给出运行时间或内存的具体数字（我检索了 memory、CPU、hours，未找到），只有"已到计算可行性的极限"这一定性表述。

**Fernández-Muñoz & Pérez-Díaz 2021**（IET Renew. Power Gener. 15:30）[abstract only]
- **研究对象**：柴油、风电、抽水蓄能混合的孤立电力系统，建立两阶段随机混合整数线性规划的机组组合模型，第一阶段计入小时内的净负荷变化。
- **摘要原文**："To increase the model's computational efficiency, a solution approach … is proposed"（摘要在此处截断）。
- **支持的说法**：岛屿机组组合一旦计入小时内变化，就需要专门的求解方法才能算得动。这个案例在原文中对应 El Hierro 岛（据会议论文摘要）；具体计算时间只读了摘要，无法给出。
- **修正说明**：页面原先这里引用 Psarros & Papathanassiou 2023。那篇只看到搜索摘录，没有内容支持"难以求解"这一说法，已于 2026-11-10 换掉。

**Mopo 数据**（Zenodo 记录页）
- 历史数据：陆上风电 9 种、海上风电 4 种、光伏 3 种技术，共 16 种，另加"existing"情形；逐时；ERA5 + GWA。
- 气候预估：MPI-ESM1-2-HR、EC-Earth3 两个模式 × SSP2-4.5、SSP5-8.5 两个情景，2015–2100 年逐时。
- 压缩包：1.6 GB 和 12.6 GB。
- **修正说明**：页面原先写"解压后约 0.9 TB"，来自 Zenodo 页面的 "Data volume 295.6 GB / 581.1 GB"。那是记录被下载的累计流量统计，不是数据大小，已改正。

#### 第 3 栏 "The data are redundant"

- "日循环和季节循环每年重复，信息量远小于数据量"：`[INFERENCE]` 这是基于数据结构的推断，尚未用本项目数据验证。计划用 PCA 的有效维数 d_eff 来定量检验，见 T3。
- "要保留什么取决于用途"：各用途对应的统计量见 02 文件第 2.2 节的 L1–L6。
- "岛屿的反方向问题"：`[INFERENCE]` 依据是 km 级降尺度计算昂贵；没有引用具体文献。

#### "Gap in current practice" 框【2026-11-10 已从页面删除；以下文献内容保留在本文件中，供参考和回答提问】

**Cannon 2015**（J. Climate 28:1260）[abstract only]
- **研究对象**：从多模式气候集合（CMIP5）中挑选少数成员做影响评估。
- **摘要原文**："Clustering algorithms are, however, biased toward high-density regions of climate variable space and tend to select scenarios that describe the central tendency rather than the full spread of an ensemble." 聚类偏向高密度区域，选出的是集中趋势，不是整个集合的范围。作者提出用 KKZ 算法，选出覆盖变化范围的成员。
- **对本课题的意义**：在气候集合上，聚类会丢掉边缘，在能源时段上也同理会丢掉极端。后一点是推断：Cannon 研究的是气候模式选择，不是能源时段。

**Teichgraeber & Brandt 2022**（RSER 157:111984）[full text, optimization-online 预印本]
- **研究对象**：TSA 用于能源系统优化的综述。
- **相关原文**：
  - 用欧氏距离（ED）这类强调均值的距离做聚类，会把对储能重要的时段形状"抹平"（smoothed out）；
  - "Be extra careful with wind data. Aggregation has been shown to smooth out a lot of important variability."
  - 5 条建议：按优化结果评价并在全序列上验证；针对具体问题调整方法；风电数据格外小心；考虑给目标函数误差定界；在聚合时段之外加入真实的"极端日"。
- **没有数字**：这是综述。

**van Duinen et al. 2026**（Appl. Energy 427:129090）[full text, arXiv v1]
- **研究对象**：PECD 气候预估中 6 个模式在 SSP2-4.5 下的 2016–2045 年，共 180 个气候年；NUTS0 级日均值，变量包括风、光、水电、需求、剩余负荷。目标是选出一个整年子集，使冬季、夏季两个季节的切片 Wasserstein 距离中较大的那个（SSWD）最小；比较模拟退火、随机搜索、过滤随机搜索和 k-medoids。
- **原文**："Current practice, including ENTSO-E's European Resource Adequacy Assessment, relies on climate year selections that have not been validated against explicit representativeness criteria."（摘要）
- **数字**：
  - 模拟退火比次优方法的代价函数低 3–15%，比最差方法低 14–26%；
  - 代表性约为 ENTSO-E 现行做法的 2.5–3.5 倍；
  - **有效样本量**（ESS）定义：所选子集的 SSWD，相当于随机抽取多少年时得到的中位水平。荷兰 30 年子集相当于随机 140 年（4.67 倍）；欧洲 30 年子集相当于 130 年（4.33 倍）；欧洲 5 年子集相当于约 25 年（约 5 倍）。
- **局限**（与本课题的区别）：用日均值，不看日内和跨日结构；没有单独针对干旱和极端；只选整年；没有岛屿；只做统计评估。

**Teichgraeber & Brandt 2019**（Appl. Energy 239:1283）[abstract only]
- **研究对象**：比较 k-means、k-medoids、层次聚类、DBA 和 k-shape 选代表期。
- **结论**：聚类指标更好，不意味着优化目标值更准。
- **没有数字**：只读了摘要。

**Hilbers et al. 2023**（Appl. Energy 334:120624）[full text, arXiv]
- **研究对象**：带储能的容量扩展模型，用 40 段各 3 年的时间序列做实验，每 3 年聚合为 30 个代表日；参考设计（全序列结果）平均为基荷 71.5 GW、调峰 62.8 GW、风电 157.0 GW、输电 153.3 GW、储能 427.9 GWh。案例所在区域我没有核对。
- **摘要原文**："reducing statistical error metrics on input time series does not in general lead to more accurate model outputs. Furthermore, many aggregation schemes are unsuitable for models with storage since they distort chronology."
- **结论**：利用模型输出信息的"后验"（a posteriori）聚合优于只看输入的"先验"（a priori）聚合，主要因为它系统地找出并保留了相关的极端事件。
- **对本课题的意义**：这是对"只用统计检验"最直接的反对意见。本课题的回应是把累计亏缺、干旱这类与系统相关的量放进统计检验，并在论文中写明适用边界。

**Grochowicz, van Greevenbroek & Bloomfield 2024**（Environ. Res. Lett. 19:054038）[full text, arXiv v2]
- **研究对象**：PyPSA-Eur（0.6.1 版）欧洲电力系统，40 年 ERA5；用模型输出的影子价格（shadow price，节点电价的代理量）找出驱动投资的最困难时段。
- **结论**：
  - 这些时段由大尺度天气造成：欧洲上空高压静止，带来不同长度的低风、低温；
  - "purely meteorological approaches fail to identify which events lead to the largest system stress … due to the influence of subtle transmission bottlenecks and storage issues across multiple regions"；
  - 这些事件与传统的欧洲—大西洋天气型或北大西洋涛动指数关系不强。
- **对本课题的意义**：同 Hilbers 2023，属于反对意见；也说明 L4 空间同时性和 L5 累计亏缺必须纳入检验。

---

### 第 2 页：两个科学问题

**本页缩写**：k\*、NUTS0/NUTS2、ENTSO-E、ERAA、ML（见第 0 节）。

| 页面内容 | 详细解释 |
|---|---|
| 导语 "which question to study. The methods follow once a question is chosen" | 今天只定研究哪个问题；用什么方法，等问题定了再讨论 |
| 已知背景（表格上方一行） | "Known, and not repeated here"：聚类成典型时段会丢掉极端和跨数周的储能亏缺，常见补救是加入极端日或最严重干旱年（Kotzur 2018a；Yeganefar 2020；Gonzato 2021；Teichgraeber & Brandt 2022；Kittel & Schill 2026）。这是原 Q1 删除后保留下来的已知事实 |
| Q1（原 T3） | 从大陆到国家再到岛屿，所需的数据量怎样变化？能否只从数据本身预测？"Why it is open"：目前没有找到量化这种尺度依赖的研究（两次检索，非穷尽）；已知区域序列比单点序列容易缩减（Kotzur 2018a）。"Why it matters"：模型的空间分辨率在提高、岛屿被单独建模，但代表期个数通常不变 |
| Q2（原 T4） | 岛屿只能降尺度几年时，哪些年代表长期气候？连续几年的短序列有多大代表性？"Why it is open"：岛屿的数据缺口方向相反，高分辨率数据太少。"Why it matters"：短记录会使岛屿项目和规划的长期资源估计产生偏差 |
| 提问（"DTU link"和"Most useful?"两列已于 2026-11-10 删除） | 请 Matti 排序：哪个问题对 DTU 现在最有用；以及由 DTU 的哪种用途来决定缩减后| 下游用途与必须保留的特性（表） | 2026-11-10 代替原来的"Uses to rank"列表。缩减后的数据交给谁用，决定了评价代表性时以哪些统计特性为准：年发电量和资源评估看数值分布和长期平均；储能规模（如 Balmorel 中的储能）看时间顺序和跨数周的累计亏缺；充裕度评估（ERAA）看极端低出力以及高负荷与低风光同时出现的尾部；电网和跨境潮流看多国同时低出力的频率；平衡与备用看小时内和小时级爬坡；气候变化影响与风险研究看覆盖全部年份的变化范围。各用途在 DTU 的对应工具见 02 文件第 3 节 |el 的 TSA 模块正在开发）、Mopo/SpineOpt、ENTSO-E 的 PECD 选年、气候变化影响、平衡与预测误差、电网与概率潮流、ML 代理模型。各用途的数据、方法、目标、验证见 02 文件第 3 节 |
| 已删除的内容 | 原 T1 行、"Method contribution"列、"Proposal for the visit"一节、"DTU link"和"Most useful?"两列，均于 2026-11-10 删除；方法部分**稍后讨论** |

---

### 原 T1 有误差证书的路径空间压缩【已从页面删除；方法，稍后讨论】

**本页缩写**：MMD、RKHS、SA、SWD、TMY、tsam、k-medoids（见第 0 节）。

**方法文献**（都只读了摘要，用于说明方法是什么，不支撑具体性能数字）

| 文献 | 摘要中能确认的内容 |
|---|---|
| Gretton et al. 2012（JMLR 13:723） | 定义 MMD：在 RKHS 单位球内所有函数上，两个分布期望之差的最大值；可据此构造不依赖分布假设的两样本检验 |
| Király & Oberhauser 2019（JMLR 20） | 提出"序列化"方法，把任意核变成适用于序列（多变量时间序列、字符串、图序列）的核，基础是签名特征 |
| Salvi et al. 2021（SIAM J. Math. Data Sci. 3:873） | 证明 signature 核是一个 Goursat 型偏微分方程的解，从而可以直接数值计算 |
| Chen, Welling, Smola 2010（UAI；arXiv:1203.3472） | kernel herding 是确定性过程，用一组样本近似一个概率密度；对 RKHS 中函数的期望，误差按 O(1/T) 下降，而独立随机抽样为 O(1/√T)，T 为样本数 |
| Dwivedi & Mackey 2021（arXiv:2105.05842） | kernel thinning 压缩分布的效果优于独立随机抽样和标准稀疏化；具体误差率只读到摘要开头，未能确认 |
| Mak & Joseph 2018（Ann. Stat. 46:2562） | support points 通过最小化能量距离求代表点；收敛到原分布，对一大类函数的积分误差率优于蒙特卡罗方法；可用于"昂贵模拟中的不确定性传播" |

**O(1/T) 与 O(1/√T) 的含义**：要把误差减半，随机抽样需要 4 倍的样本，herding 只需要 2 倍。代表性时段越少，这个差别越重要。

**"effective sample size well above k" 的依据**：van Duinen 2026 在整年选择中，所选子集相当于 4.3–5 倍数量的随机年份（见第 1 页）。T1 的假设是在日或周尺度上也能做到类似程度；这是待检验的假设，不是已有结果。

**验证中"随机天气发生器"（stochastic weather generator）**：按已知的统计模型（如带季节项的自回归过程）生成合成序列。因为真分布已知，可以算出子集的真实误差，用来检查误差证书是否成立。

---

### 原 Q1（原 T2）代表性子集是否保住了极端【2026-11-10 从页面删除：前提不成立】

**删除原因**（Chao 2026-11-10 提出质疑，文献核实后成立）：
- **前提 1"通行做法是按分布选子集"不成立**：能源系统 TSA 中"聚类 + 加入极端时段"是常规做法：Kotzur 2018a 比较了加入极端日的几种方式 [full text]；Zatti et al. 2019（Energy，doi:10.1016/j.energy.2019.05.044）标题即"选择典型日和极端日" [只看了标题]；Yeganefar 2020 [abstract]；Teichgraeber & Brandt 2022 建议加入真实极端日 [full text]。选气候年时，Kittel & Schill 2026 建议纳入干旱最严重的年份 [full text]，Ullmark 2025 按净负荷幅度和持续时间选年 [abstract]，Hilbers 2019 的重要性子抽样刻意多抽极端时段 [abstract]。只按分布选的主要是 van Duinen 2026 和 ERAA（后者只见搜索摘录）。
- **前提 2"没人量化过对极端的忽略"不成立**：Gonzato 2021 发现长期储能投资可偏差 2 倍以上 [abstract]；Hilbers 2023 显示先验聚合下储能误差最大 [full text]；Ruhnau & Qvist 2022 发现"平均年份"所需储能不到 35 年整体规划的一半 [abstract]；另有 2022–2025 年几篇新论文专门处理极端值和时间顺序（只见搜索摘录，元数据未核对）："Wind data introduce error in time-series reduction for capacity expansion modelling"（Energy 2022）、"Capturing chronology and extreme values of representative days …"（arXiv:2310.04244）、"What are we clustering for? Establishing performance guarantees for time series aggregation in generation expansion planning"（arXiv:2510.09357）。
- **对以后方法讨论的提醒**：arXiv:2510.09357 讨论 TSA 的"性能保证"，可能与原 T1 的"误差证书"思路直接重叠，讨论方法前必须先读全文。

以下原 Q1 的内容保留供参考。

> **页面已简化（2026-11-10）**：页面上这一页去掉了公式、候选算法和风险，改为：输入数据 → 缩减 → 缩减后的数据；简化、聚合或选择了什么；必须保留哪些特征；预期结果；检验方法。下面的公式和文献细节保留在本文件中，供参考。


**本页缩写**：GPD、EVT、KKZ、D_max、n_eff（见第 0 节）。

**Bodini et al. 2016**（Wind Energy Sci. 1:115）[full text]
- **研究对象**：加拿大 60 个站点、每站 62 年的实测风速；比较"用前 42 年估计的 P50"与"后 20 年的实际表现"。
- **数字**（全部来自摘要）：
  - 后 20 年中超过 P50 的年数，一半站点少于 5 年或多于 15 年，即四分位距约 10 年；把各站历史数据随机打乱、强制年份独立后，四分位距只有约 4 年，窄 2.5 倍；
  - 对容量因子 0.35、年际变率 6% 的站点，若各年独立，预期 10 年中 9 年落在 0.32–0.38；实测的 90% 范围是 0.27–0.43，宽 3 倍；
  - 对这套数据，记录超过 4–5 年后 P50 误差不再改善，超过 20 年反而变差。
- **原因**：风速对平均值的偏离会持续数十年（年际序列相关），"多年平均"并不像独立样本那样快速收敛。
- **对本课题的意义**：选年时若假设年份独立，会低估不确定性；所以 T2 按整年块选，并用 n_eff 修正有效年数。注意：这是加拿大单站实测，欧洲区域聚合序列的持续性要用本项目数据重新估计。

**Yeganefar et al. 2020**（Appl. Energy 272:115224）[abstract only]【对照方法，已从页面删除，稍后讨论】
- **研究对象**：用自组织映射（SOM）聚类选代表日，并加入净负荷最高和最低的极端日；在 NREL-118 测试系统和比利时系统上，分单年和多年规划检验；给出确定代表日个数的简单方法。
- **用途**：T2 的对照方法"加极端日"。
- **没有数字**：只读了摘要。

**Cannon 2015**：见第 1 页。KKZ 是原 T2 的另一对照方法，目标是覆盖范围而非匹配分布【已从页面删除，稍后讨论】。

**Kittel & Schill 2026、Ruhnau & Qvist 2022**：见第 1 页。T2 的验证直接用前者的多阈值干旱目录方法和后者的最大累计亏缺概念。

**页面上 "a, b … assumption of the plan"**：剩余负荷 r_t = d_t − (a·w_t + b·s_t) 中，风电和光伏的装机倍数 a、b 是本计划自己设定的（使长期平均风光发电等于平均需求），文献中没有查到这种设定，因此在页面上标为假设。

---

### 第 3 页：Q1（原 T3）从大陆到岛屿需要多少数据

**问题表述（2026-11-10 定稿）**："How many representative periods does a spatially averaged energy series need, as the averaging area shrinks from Europe to a country to an island, and can that number be predicted from the data alone?" 空间上取不同大小区域的平均（加总）序列，时间上求所需的最少代表性时段数 k\*。"多国同时低出力"属于多区域联合序列，在页面上已移为扩展条目。

**这是研究聚合方法吗？** 不直接是。Q1 研究的是数据的性质：能源序列的可压缩性怎样随空间平均尺度变化；聚合方法只是测量 k\* 的工具。弱点是 k\* 依赖所用方法，所以要让 k\* 成为数据的性质，必须估计"能达到的最小 k"。由此引出两个方法贡献，**稍后讨论**：(a) 最小 k\* 的估计方法（接近最优的选时段算法，或由有效维数推出的下界）；(b) 按尺度自适应的聚合方法（给不同大小的区域分配不同数量的代表期）。

**Why it matters（页面上的说明，中文）**
- **应用**（2026-11-10 改写：原来写的"模型细化空间分辨率但代表期个数不变"没有依据，已删除）：模型在细化空间分辨率，Frysztacki et al. 2021（Applied Energy 291:116726）[abstract] 把欧洲模型从 37 个节点细化到 1024 个节点，只看风光资源分辨率时系统成本最多降低 10%；而区域层面的结果比系统总体结果难缩减得多：Reichenberg & Hedenus 2022（Energy Systems）[abstract] 发现系统成本用约 10 个代表日偏差约 5%，装机结构总量需要 50 个以上代表日（偏差约 20%），区域装机结构用 250 个代表日偏差仍超过 50%。注意后者测的是模型输出，不是数据本身的性质。一个经过检验的关系可以告诉建模者每个区域需要多少时段，告诉岛屿规划者需要几年数据。Pfenninger 2017 的结论是"没有通用的做法" [full text]，Q1 要把"因区域而异"变成可以计算的量。
- **科学**：把一个数据缩减参数（k\*）和天气的空间结构联系起来。物理过程：天气尺度（synoptic scale）系统约 1000 km、持续数天；区域远大于天气尺度时，区域内有多个互相独立的天气系统，加总后方差减小、状态种类变少，即空间平滑效应（spatial smoothing effect）；区域小于一个天气系统时，全区受同一系统和局地过程控制，相对波动大、极端多，需要更多时段。
- **一致的已有证据**：区域序列比单点序列容易聚合 [Kotzur 2018a, full text]；系统总成本用约 10 个代表日即可表示，区域装机组合用 250 个代表日偏差仍超过 50% [Reichenberg & Hedenus 2022, abstract]。
- **弱点**：如果只得到"区域越小需要越多"，会被认为是常识。必须给出定量关系，并在没参与拟合的区域（Réunion、Bornholm）上预测成功；还要解释例外，例如 Réunion 全岛分散布置光伏几乎消除天气造成的波动 [Tapachès 2019, abstract]，光伏和风电的尺度规律可能不同。

> **页面已简化（2026-11-10）**：页面上这一页去掉了公式、候选算法和风险，改为：输入数据 → 缩减 → 缩减后的数据；简化、聚合或选择了什么；必须保留哪些特征；预期结果；检验方法。下面的公式和文献细节保留在本文件中，供参考。


**本页缩写**：MODWT、PCA、d_eff、k\*、NUTS2、ERA5、GWA（见第 0 节）。

**Kotzur et al. 2018a**（Renew. Energy 117:474）[full text, arXiv 预印本]
- **研究对象**：三个能源系统设计问题（热电联产系统、住宅系统、高比例风光的孤立区域系统），比较平均、k-means、k-medoids、层次聚类，以及典型日、典型三日、典型周三种时段长度。
- **原文结论**：
  - "the series representing entire regions can be more easily aggregated than those for single locations, i.e., less typical periods, can be sufficiently representative"——区域加总的序列比单点序列更容易聚合，需要的典型时段更少；
  - 前两个系统在少于 12 个典型日时误差就小于 2%；孤立区域系统"即使 72 个典型日也看不到稳健收敛"；
  - 原因是"典型时段相互独立，不能交换能量"，储能无法正确体现；改用典型周略有改善，24 个典型周时误差仍在 2% 以上。
- **注意**：这个"孤立区域系统"是概念算例（光伏、风电、氢储能和电池，备用电源不超过需求的 10%），不是真实岛屿。
- **对本课题的意义**：直接支持 H2"区域越小、越接近单点，越难缩减"；也说明储能主导的系统需要保留跨时段的时间顺序。

**Tapachès et al. 2019**（IEEE PVSC, p. 2082）[abstract only]
- **研究对象**：Réunion 岛非互联电网中光伏电站的地理分散与储能。
- **结论**："Despite the small area of the Island … with dispersion at the total grid scale, the variability driven by weather conditions (unpredictable variability) is almost removed."
- **对本课题的意义**：岛屿上光伏的快速波动可以靠全岛分散布置平滑，所以光伏方面的岛屿与大陆差别可能小于风电。这是 T3 的风险之一。

**MODWT**【方法，已从页面删除，稍后讨论】：把一条逐时序列分解为若干分量，每个分量只含某一时间尺度（约 1–2 小时、2–4 小时、……、数周）的变化，各分量方差相加等于原序列方差。T3 在每个尺度上用适合该尺度的时段长度分别压缩。

**d_eff 举例**：若欧洲 30 国日剖面的 PCA 中第一个模态解释了绝大部分方差，d_eff 接近 1，说明各国同步变化，少量时段就能代表；岛屿单区域的情况要用数据算，本页的说法是假设。

---

### 第 4 页：Q2（原 T4）岛屿应该降尺度哪几年

**Why it matters（页面上的说明，中文）**
- **应用**：岛屿的资源评估和 km 级气候模拟只算得起几年。年际持续性使短记录不可靠：Bodini 2016 用加拿大 60 个站、每站 62 年的风速记录发现，年容量因子的实际 90% 范围比按年份独立预期的宽 3 倍（0.27–0.43 对 0.32–0.38，容量因子 0.35、年际变率 6% 的情形）[full text]。选好年份可以在不增加计算量的前提下减小这种偏差。
- **科学**：测量岛屿局地气候有多少由大尺度环流（large-scale circulation）决定。只能用大尺度信息选年，所以选年效果的上限就取决于这个比例；如果比例小，说明局地对流和地形过程占主导，任何挑选都代替不了多算几年降尺度，这本身是关于岛屿气候的结论。
- **弱点**：受众较窄，和 DTU 的联系比 Q1 远；只有一个岛屿时结论难推广，最好包括多个岛屿或多个地形区。

> **页面已简化（2026-11-10）**：页面上这一页去掉了公式、候选算法和风险，改为：输入数据 → 缩减 → 缩减后的数据；简化、聚合或选择了什么；必须保留哪些特征；预期结果；检验方法。下面的公式和文献细节保留在本文件中，供参考。


**本页缩写**：ERA5、MMD、CorRES（见第 0 节）。

**Kennard & Stone 1969**（Technometrics 11:137）[abstract only]【对照方法，已从页面删除，稍后讨论】
- **内容**：一种面向计算机的序贯试验设计方法，每一步都让已选的点均匀覆盖试验区域。
- **用途**：T4 的对照方法。它追求覆盖，不追求分布匹配，与 KKZ 同类。

**D-最优设计**（D-optimal design）【已从页面删除，稍后讨论】：让所选样本的信息矩阵行列式最大的试验设计方法，是统计学的标准方法；页面没有给它单独引用。

**"ERA5 underestimates wind in complex terrain"**：只有搜索摘录支持，来源是一篇关于英国的预印本（arXiv:2511.04781）和若干山区评估，都没有核对过元数据，也没有岛屿专门研究。页面上这句没有标引用，汇报时应说明它是待核实的一般性认识。

**伪真值实验**（pseudo-truth experiment）：用 CorRES 在 Réunion 的序列，在全部 ERA5 年份上都可得到，把它当作"局地场"。这样每一年都有真值，可以严格检验"按大尺度因子选年"的效果，再推广到真正的降尺度年份。

---

## 3. 会前需要先想清楚的一个问题【方法选择，稍后讨论；明天不讲】

T1 的方法核心是核方法：MMD、signature 核、kernel thinning。这些来自统计学和机器学习，能源文献里还没人用过，所以有新意，但也意味着：

- 汇报时要能讲清楚 1.3 到 1.5 节的内容，并回答"为什么不用聚类"；
- 实现上要处理 signature 核的计算量问题。

如果你对这条路线不放心，可以换一个更直接的方法核心，同样是数据处理方法上的创新：用"分布 + 时间结构 + 尾部"多个统计量做多目标选时段，给出帕累托前沿和 k\* 的定义与尺度律。也就是把 T2 和 T3 作为核心，签名核作为可选的扩展。

**建议在会上问 Matti**：DTU 组里有没有人熟悉核方法或 signature 方法？如果没有，第一篇论文用哪条路线更稳妥？
