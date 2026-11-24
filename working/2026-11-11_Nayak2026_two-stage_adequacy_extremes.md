# Nayak 等稿件精读、两阶段规划与能源极端文献（2026-11-11；第 8–10 节 2026-11-16 加入）

- 用途：2026-11-10 会面后的背景阅读（见 `2026-11-10_meeting_notes_and_plan.md`，待办 T1–T5）。
- 规则：每条说法注明出处和阅读范围 [full text] / [abstract only] / [title only] / [SF 记录]（SF = Science_Frontier_2026 的条目，记录本身注明了它的阅读范围）；推断标 `[INFERENCE]`；不同研究的结论不合并。
- 新文献均已加入 Zotero 集合 `Projects/Time_Series_2026`（commit `cae2890`）。

---

## 1. Nayak 等稿件讲了什么

**书目**：Nayak S., Liu Y., Bahmani M., Olsen B.T., Amelin M., Koivisto M.J. *Integrating Long-Term Weather Distributions into Continental-Scale Energy System Planning: Impacts on Adequacy and Investment Decisions*. SSRN 预印本，doi:10.2139/ssrn.7455543（未经同行评审）。DTU Wind and Energy Systems 与 KTH 合作，Mopo 项目资助。**阅读范围：full text**（正文、表、图注，附录图注；图本身未看）。

⚠️ 元数据：Crossref 上这条 DOI 的作者列表与 PDF 不一致（"Lui"、把 "Matti" 当作姓、多出 "Simutis"）。Zotero 按 PDF 的 6 位作者录入，并标 `meta:needs-check`。

### 1.1 要解决的问题

- 大多数能源系统规划用**单一天气年**做投资优化（§1.1）。
- 风电开发商评估单个项目时，用的是 20–30 年的长期风气候（测量结合 ERA5 等长期参照，按 IEC 61400-15 的流程）。所以作者认为，规划模型的做法和实际投资决策不一致（§1.1）。
- 只用单一天气年，会扭曲投资信号：陆上风电的 LCOE 偏差最多约 20%，光伏 15%，海上风电 25%（§5.1）。即使选一个"平均偏差最小"的年份（如 2012），个别区域仍有偏差：葡萄牙 +7%，丹麦 −4% 到 −5%（§4.1）。

### 1.2 数据和模型

| 项目 | 内容（出处） |
|---|---|
| 天气 | ERA5 逐时，**1982–2020 年共 39 年**；所有天气相关输入用同一气象源，以保留变量之间的相关（§2.1） |
| 风、光 | CorRES 模拟，GWA2 微尺度订正，加风电场内部尾流的代理功率曲线（§2.1.1） |
| 需求、热泵 | 由 ERA5 的 2 m 气温推出：供热需求用度日法，电力需求和热泵 COP 按文献模型（§2.1.2） |
| 水电来水 | GloFAS-ERA5 河流流量，用随机森林加岭回归在 ENTSO-E 2015–2025 年的数据上训练；KGE 为 0.85（水库）和 0.91（径流式）（§2.1.3，图 A.16） |
| 模型 | Balmorel（DTU 参与开发），泛欧、多部门（电、热、氢），2050 年绿地投资（§2.3.1） |
| 投资模型的时间表示 | 原文写"84 个代表日"：第 2、8、15、21、28、34、41、47 周的周四到周六，3 小时分辨率（§3）。⚠️ 按这条规则只有 8 × 3 = 24 天，与 84 不符，待向作者核实（见第 9 节 A1，2026-11-16 补注）。原文说 Balmorel 能用的数据少于 1 年（§2.2） |
| 调度模型 | 容量固定，按年逐年求解，分三步：① 全年 4 小时分辨率、完全预见，确定长期储能水位和检修；② 随机强迫停运模型；③ 逐日滚动、逐时调度（§2.3.1） |

### 1.3 关键方法一：缩放（scaling）

本质上是**分位数映射**（quantile mapping）。对每个区域、每个天气相关变量：

```
              p*  =  F_full⁻¹ ( F_short ( p ) )                        原文式 (2)

  p          选出的代表日上的原始值
  F_short    代表日数据的经验累积分布函数
  F_full     39 年全部数据的经验累积分布函数
  p*         缩放后的值：代表日的边缘分布与 39 年的边缘分布相同
```

- **保留了什么**：每个变量自身的分布，因而长期年发电量和出力分布与 39 年一致（§2.2）。
- **没有保留什么**（作者原文明确写出）："does not guarantee that the dependency structures, such as temporal and spatial correlations and diurnal and seasonal structures are similar"（§2.2）。也就是说，时间自相关、空间相关、变量之间的相关不保证。
- 例子：DK1 区陆上风电，用 1995 年数据时缩放影响很小；用 1985 年数据时容量因子变化明显，但时间结构基本不变（§2.2，图 2）。

### 1.4 关键方法二：两阶段框架（§2.3.2，图 3）

```
 第一阶段（基线投资，代表"平均行为"）
   对 39 个天气年中的每一年：选 84 个代表日 → 缩放到 39 年分布 → 投资优化
   → 得到 39 个系统，取总成本的中位数系统作基线（1995 年）

 压力测试
   基线容量固定，对 39 年逐年做调度
   → 用"备用燃气机组被调用"作为供电不足的代理，计算 LOLE、EENS

 第二阶段（针对极端补强）
   基线容量固定，允许增加投资；分别对 4 个极端年各做一次优化（用原始数据，不缩放）
   极端年 = 单一年份不缩放优化时系统总成本最高的 4 年：1985、2010、1987、1996（§4.1.1）

 对照：直接用单一极端年（不缩放）做投资优化
 两种方案都再对 39 年做调度压力测试，比较成本和充裕度
```

**充裕度指标**（表 1）：系统失负荷（GWh，按年、按时刻，所有区域相加）；失负荷期望 LOLE（h/年，每区域）；期望缺供电量 EENS（GWh/年，每区域）。可靠性标准取 LOLE 3 h/年，出自原文参考文献 [23] Rosendal et al. 2025。备用机组成本没有按失负荷价值（VoLL）设定，而是由天然气价格和 CO₂ 税决定（§2.3.1）。

### 1.5 主要结果（全部出自原文）

1. **基线系统并不充裕**：99% 以上的时间充裕，但少数小时的缺电超过 100 GWh；不足主要发生在冬季，而且集中在少数几年（§4.2，图 8）。
2. 缺电最多的 3 年，正是单一年份优化成本最高的 3 年；1996 年成本第四高，缺电量只排第八（§4.2）。
3. **空间分布**：不足集中在以风电为主的欧洲大陆和西北欧；北欧较低，作者认为可能和大量水电有关（§4.2，图 9）。
4. **两阶段方案**：所有区域的 LOLE 都低于 3 h/年；第二阶段**不增加风光装机**，补强靠长时储氢、燃料电池和输电（§4.3，图 10、11）。
5. **单一极端年方案**：风光装机随所选年份变化；只有 1985 年方案的充裕度和两阶段方案相当（§4.3）。
6. **成本**：1985 年单一年份方案的期望总成本约 3557 亿欧元，两阶段方案为 3590–3682 亿欧元（§4.3）。按这两个数算，两阶段方案贵 0.9%–3.5%（这个比例是我算的，原文没有给出）。

### 1.6 作者自述的局限（§5.2），也就是研究机会

1. **缩放只保留边缘分布，不保留时空依赖结构**。原文建议今后构建"representative baseline"时，"preserve not only marginal distributions but also time-series dependence and spatial correlations"。这和本项目的聚合研究（Q1、Q2）直接相关。
2. 调度用了完全预见，没有考虑预报误差。
3. **只用再分析，没用气候预估**："climate change may alter temperature distributions, wind regimes, hydro inflows … the input data would need to be based on climate change projections"。
4. 停运概率可能本身依赖天气（洪水、热浪、风暴）。
5. 热和氢两个部门还没有公认的可靠性标准。

---

## 2. 为什么分两个阶段，为什么不一起做

**作者给的理由**（§1.1、§5.1）：
- **理想做法是一起做**："investments would be co-optimized jointly over all 40 weather years"。但作者说这"rarely possible"，因为计算量太大，Balmorel 的投资模型只能用不到 1 年的数据（§2.2）。
- **两类决策需要的天气信息不同**：
  - 风光装机这类"大宗投资"，应该反映长期平均气候，这和开发商的做法一致，所以第一阶段用缩放到 39 年分布的数据；
  - 充裕度由少数极端年决定，所以第二阶段专门针对极端补强。
- **实证上的理由**：直接用极端年做投资，会让风光装机随年份大幅变化（§4.3）；两阶段方案的风光装机在不同极端年下都稳定，补强由灵活性资源承担（§6）。

**我的解读** `[INFERENCE]`：
- 分开做，把一个"既要代表平均、又要覆盖极端"的数据缩减问题，拆成了两个容易处理的问题：第一阶段只需保住平均和分布，第二阶段只需挑对极端。
- 代价是结果不是联合最优：两阶段方案比 1985 年单一年份方案贵 0.9%–3.5%（按 §4.3 的数字算），作者认为换来的是更现实、更稳定的风光投资。
- 拆开以后也暴露出两个数据问题：第一阶段的代表日只保留了分布，没保留依赖结构（作者自己指出）；第二阶段的极端年是按"单一年份优化的成本最高"挑的，这要先跑一轮完整的模型。这两点都是聚合研究可以切入的地方。

---

## 3. 两阶段规划：原理与操作步骤（背景知识）

### 3.1 两种"两阶段"

| 类型 | 原理 | 例子 |
|---|---|---|
| **两阶段随机规划**（two-stage stochastic programming） | 第一阶段决策（装机 x）要在不确定性揭晓前做出，对所有情景相同；第二阶段决策（调度 y_s，有时也包括追加投资）在每个情景 s 揭晓后做出。目标是第一阶段成本加上第二阶段的期望成本 | de Marco et al. 2025（5 个带概率的代表情景，详见第 7.1 节）[full text]；Göke et al. 2024，用 Benders 分解求解 [abstract only] |
| **顺序式两步**（先优化、再固定、再补强） | 先用一套数据求基线，然后固定基线，在另一套数据（极端年）上只允许追加投资 | Nayak（本稿）[full text]；Öberg et al. 2025（英国，第二阶段只允许 OCGT、电锅炉、电池、储氢，据 Nayak §1.1 的描述）[title only] |

两阶段随机规划的数学形式：

```
            ⎡                                                    ⎤
   min      ⎢   cᵀ x     +     Σ   π_s · q_sᵀ y_s                 ⎥
  x, y_s    ⎣  投资成本         s   情景 s 的概率 × 运行成本         ⎦

   约束：  A x ≤ b                         （投资约束）
           T_s x + W y_s ≤ h_s   对每个 s   （每个情景下的运行约束：供需平衡、容量上限…）

   x    第一阶段决策（所有情景相同）
   y_s  第二阶段决策（随情景变化）
   π_s  情景权重，Σ π_s = 1
```

情景越多，问题越大，所以要把天气数据缩减成少量带权重的情景。de Marco 2025 的做法是"system-informed scenario reduction"（SISR），先把 60 个气候年缩减为 5 个带概率的代表年，再做随机优化 [full text，步骤见第 7.1 节]。

### 3.2 一般操作步骤（以 Nayak 稿件为例）

| 步骤 | 内容 | 数据聚合在哪里 |
|---|---|---|
| 1 | 生成多年的天气相关输入：风、光、水电来水、需求、热泵 COP | — |
| 2 | 为投资模型选代表时段（代表日、周） | **聚合一：代表"平均行为"** |
| 3 | 投资优化，得到基线装机 | — |
| 4 | 对全部年份逐年调度，做压力测试 | — |
| 5 | 找出供电不足的年份或事件 | **聚合二：从多年数据中挑选"极端"** |
| 6 | 第二阶段：固定基线，针对极端追加投资 | — |
| 7 | 再次对全部年份压力测试，比较成本与充裕度 | — |

**会上 Matti 说的两个关键词**，分别对应第 2 步（基于平均行为的情景构建）和第 5、6 步（能源极端）。

---

## 4. 充裕度（adequacy）及其与聚合研究的关系

### 4.1 定义

- **充裕度**（resource adequacy）：发电、储能、进口和需求响应在所有时刻满足需求的能力，用风险指标衡量。Ruggles et al. 2024 的说法是"ensuring that electricity supply reliably meets demand" [abstract only]。
- **常用指标**（Nayak 表 1）：
  - LOLE（loss of load expectation，失负荷期望）：每年预期有多少小时供电不足，单位 h/年；
  - EENS（expected energy not served，期望缺供电量）：每年预期缺多少电，单位 GWh/年；
  - Nayak 采用 LOLE ≤ 3 h/年作为可靠性标准。
- ENTSO-E ERAA 方法论中的正式定义还没有核对（待办 T3）。

### 4.2 和你要做的聚合研究有什么关系

1. **充裕度是一个尾部性质。** 不足集中在少数年份、冬季和低风高需求时段（Nayak §4.2）。所以为充裕度缩减数据时，必须保留极端的强度、持续时间、频率、先后顺序、空间分布和季节性。Nayak 引言就列出了这几个方面："intensity, duration, frequency, sequence, spatial distribution, and seasonality"（§1.1）。
2. **两阶段框架把聚合问题分成了两半**：
   - 第一阶段只需代表平均，Nayak 用了分位数映射；
   - 第二阶段要挑选极端，Nayak 用"成本最高的年份"，这要先跑完整个模型。
   
   第二阶段的"极端怎样选、怎样聚合"，正是你想做的方向。
3. **现有选择极端的几种做法**（各自的阅读范围见第 5 节）：
   - 按模型成本选年份：Nayak；
   - 按模型的影子价格识别压力事件：Grochowicz et al. 2024 [full text]；
   - 按系统响应聚类出压力事件模式：de Marco et al. 2025，欧洲 5 种多日短缺模式 [full text]；
   - 按气象或资源指标识别干旱：Kittel & Schill 2026 [full text]、Ostraszewski et al. 2027 [SF: full text]；
   - 按大集合中同时发生的干旱聚类：van Duinen et al. 2025 [abstract only]。
4. **气候变化进入这些框架的程度**（2026-11-11 读完 de Marco 全文后更正）：
   - Nayak 只用再分析，并在局限中明确指出这一点（§5.2）；van der Most 2024 的 1600 年只代表当前气候 [preprint full text]。
   - **de Marco 2025 用的是未来气候**：CESM2，SSP3-7.0，2080–2100 年的 3 段 20 年模拟，共 60 个气候年，每年看作独立、等概率的情景（§3.1）[full text]。所以"按系统响应聚合压力事件"已经在**一个未来时段**上做过。
   - 但 de Marco **没有**比较当前与未来：没有历史基准期，只有一个模式、一个情景、一个时段，60 年在该时段内看作平稳（§3.1，§5 局限中也没有讨论这一点）[full text]。
   - Kapica 2024 比较了当前（1970–2020）与未来（2048–2098），8 组 EURO-CORDEX 模式，RCP4.5 和 RCP8.5，但只统计风、光各自的"干旱总天数"，没有事件聚合，也没有需求和水电 [full text，见第 7.2 节]。

### 4.3 可能的研究方向（新颖性尚未核实）

> **能源极端的聚合，以及气候变化下这些极端的变化**：从多年代或大集合数据中，把风、光、水电和需求共同造成的极端事件聚合成少数几类事件（带权重）；再在气候预估下，看各类事件的频率、持续时间、强度和同时发生程度怎样变化，并据此调整权重或事件本身；用"能否保住充裕度相关的尾部统计量"来检验聚合结果。

- 最接近的已有工作：
  - de Marco 2025：按系统响应把压力事件聚成 5 类，**只在一个未来时段**（CESM2 SSP3-7.0，2080–2100）[full text]；
  - Kapica 2024：当前对未来的能源干旱天数变化，多模式，但不聚合事件、只有风光 [full text]；
  - van Duinen 2025：大集合中同时发生干旱的聚类，当前气候 [abstract only]；
  - Nayak：按成本选极端年，再分析 [full text]。
- **读完两篇全文后，哪些已经有人做了**（只就这两篇而言）：
  - "把多日能源短缺事件聚成少数几类、带概率"：已做（de Marco）。
  - "在未来气候数据上做这件事"：已做（de Marco，单模式单情景单时段）。
  - "多模式比较当前与未来的能源干旱"：已做，但只是逐区域的天数统计（Kapica）。
- **这两篇都没有做的**（是否真是空白，还要查其他文献，T7）：
  1. 同一套事件聚类在**当前与未来之间**怎样变化：每类事件的概率（权重）、持续时间、强度、空间范围、季节有没有移动；有没有新类型出现、旧类型消失。
  2. 这种变化在**多个模式和情景**之间是否一致（Kapica 已证明单个模式的天数变化方向不可靠：Fig. 3–10）。
  3. 事件定义**不依赖某一个优化模型**：de Marco 的事件来自影子价格，而影子价格来自为该年单独优化的系统，换模型或换装机，事件就变。可以比较"统计定义的事件"与"系统定义的事件"，看前者能否作为不跑模型时的替代。
  4. **水电和需求**作为驱动变量：de Marco 的特征里有供热需求和水库来水，但没有分析它们随气候变化的作用；Kapica 完全没有。会上 Matti 说的"水电和需求的变化更大"正对应这一点（Wohland 2025 的数字见第 5.3 节）。
  5. 聚合结果的检验：de Marco 只报告"5 类时平均相对误差 7%"（Fig. S2，补充材料未读），没有检验尾部统计量。
- ⚠️ 以上 1–5 是根据两篇全文推出的候选空白 **[INFERENCE]**。
- **T7 排查结果（2026-11-11，又读了 9 篇，见第 7.3 节）**，逐条核对：

| 候选空白 | 排查中最接近的工作 | 判断 |
|---|---|---|
| 1. 事件类型及其权重从当前到未来的变化 | Grochowicz 2026 把 SDE 分 4 类，但只用 ERA5 历史，并把"变暖气候下的检验"列为未来工作；de Marco 只有一个未来时段；van Duinen 2025 按国家聚类、只有当前气候 | 9 篇中无人做 [INFERENCE] |
| 2. 多模式、多情景的一致性 | Kapica、Dolores-Tesillos、Aminimehr、Mostue、Yu & Vautard 都做了多模式，但对象是格点或区域的干旱天数、频率、持续时间，不是事件类型 | 对"事件类型"而言无人做 [INFERENCE] |
| 3. 统计定义的事件与系统定义的事件对比 | Hilbers 2023 显示纯输入启发式（最大需求日、最小风日）不如按成本选的极端日；Grochowicz 2024 结论相同；但都在历史数据上 | 在气候变化背景下无人做 [INFERENCE] |
| 4. 水电和需求作为驱动 | van Duinen 2025 含需求与径流式水电（当前气候）；Aminimehr、Mostue、Kapica、Dolores-Tesillos 都不含需求；Qiu 2026（美国）含制冷需求 [abstract only] | 欧洲未来气候下的"需求 + 水电 + 风光"事件聚类未见 [INFERENCE] |
| 5. 聚合结果对尾部的检验 | van Duinen 2026 用 SSWD 检验整体分布代表性，明确说极端要另行加权；Hilbers 2023 用缺电量检验 | "保尾部 + 非平稳"的代表期选择未见 [INFERENCE] |

- **新的重要事实**：
  - Grochowicz 2026 来自 **DTU Wind and Energy Systems**（Matti 所在部门），作者明确把"在变暖气候中重新检验历史压力事件"留作未来工作。这是你与 DTU 现有工作的直接接口。
  - van Duinen 2026 的数据就是 **PECD 4.2**（你在 `Time_Series_2026_DATA.md` 里列的数据），并且**假定 2016–2045 无趋势**。所以"代表年选择在非平稳气候下是否仍然代表"也是一个开放点，和 Q2 直接相关。
- **仍未排查**：Plaga & Bertsch 2023 综述（付费，未取得）；Qiu 2026 只读了摘要；Effenberger 2025 仍只读了摘要。

---

## 5. 天气、气候极端与能源（风、光、水电、需求）的文献

### 5.1 能源极端的定义与刻画

| 文献 | 内容 | 阅读范围 |
|---|---|---|
| Ostraszewski et al. 2027, RSER 244:117463 | 129 项研究的综述；区分供给干旱与平衡干旱，二者不一定同时发生（西欧供给干旱多在夏末，平衡干旱多在冬季）；阈值从第 5 到第 20 百分位不等，直接影响事件个数和持续时间；气候变化的预估影响"remain uncertain and depend on scenario assumptions, regional context, and RE portfolio composition" | SF: full text |
| Kittel & Schill 2026, Commun. Earth Environ. 7 | 38 年、33 国；多阈值方法；最极端的一次在 1996/97 冬季，持续 55 天，期间可用率仍有长期均值的 47% | full text |
| van Duinen et al. 2025, RSER 223:115993 | KNMI-LENTIS（EC-Earth3）160 × 10 年 = 1600 年，**当前气候**（2000–2009 强迫）；24 国日剩余负荷（需求 − 风 − 光 − 径流式水电）；能源干旱 = 7 日滑动平均剩余负荷最高、重现期 1 年的窗口（每国 1600 个，限 11–3 月）；用 UPGMA 按同时发生概率把**国家**聚成 5 个区；NAO− 与 Blocking 风险最高，NAO− 下北欧风险约为气候态的 2 倍，伊比利亚反而降低 | full text（第 7.3 节） |
| van der Wiel et al. 2019, RSER 111:261 | 3 × 2000 年模拟；1、7、14 日低出力和高短缺事件及其气象条件 | abstract only |
| Otero et al. 2022, Meteorol. Appl. | 欧洲可再生能源复合事件，逻辑回归方法 | 只看了标题（Nayak 引用） |
| Allen et al. 2023, Renew. Energy 217:119206 | 能源干旱标准化指数 | title only |

### 5.2 水电与复合（多年）极端

| 文献 | 内容 | 阅读范围 |
|---|---|---|
| van der Most et al. 2024, Nature Energy 9:1474 | 160 组 × 10 年 = 1600 年，**当前气候**；6 个水电大国（挪威、法国、意大利、西班牙、瑞士、瑞典）；春季水库来水偏低使长时间能源干旱的概率提高到 4 倍；在南欧，夏季能源干旱的风险最高可达正常情况的 4 倍；识别出 3 种复合条件和多年能源干旱 | preprint full text |
| Fälth et al. 2025, RSER 214:115519 | 瑞典水电一周内可维持装机的 77%–96%（春季较高），约 3 GW、相当于平均需求的 20%；主要限制是河段最大流量规定 | abstract only |
| Lei et al. 2024, Renew. Energy 230:120845 | 水风光互补系统中能源干旱的频率、持续时间、严重度及其传播 | title only |
| Nayak（本稿） | 北欧缺电少，作者认为可能与大量水电有关 | full text |

### 5.3 气候变化对能源极端的影响

| 文献 | 内容 | 阅读范围 |
|---|---|---|
| Lin et al. 2026, Nature Climate Change 16:1187 | 全球"闪电式"能源干旱；SSP1-2.6 下持续时间增加：风电 25.6%，光伏 29.8%，复合事件 155.7%；约 70.8% 的风光装机面临频率和持续时间同时上升；基准期和事件定义摘要中没有给出 | SF: abstract only |
| Aminimehr et al. 2026, Commun. Earth Environ. | 11 个 CMIP6 模式（SSP5-8.5，未做偏差订正），日数据、格点；Clayton copula 构造风光联合指数 SREI，干旱 = SREI < −1.28（第 10 百分位；2026-11-16 对原文 Methods 更正，原写 −1.0）；对比工业化前（1850–1879）与 1.5/2/3 °C 升温；3 °C 时持续时间、频率、强度显著变化的陆地面积分别为 69.4%、74.0%、50.2%；XGBoost 归因：太阳辐射是主导因子；不含需求、水电 | full text（第 7.3 节） |
| Mostue et al. 2026, iScience 29:115075 | 5 个 CMIP6 模式，SSP5-8.5，6 小时、100 m 风速（模式层插值，QDM 订正）；弱风事件 = 风速 < 3 m/s；1980–1999 对 2040–2059、2080–2099；年频率增加 10%（世纪中）到 10%–20%（世纪末，英国约 20%）；冬季北欧持续时间增加约 30%；只有风 | full text（第 7.3 节） |
| Yu & Vautard 2025, ERL 20:044046 | 10 组 EURO-CORDEX，RCP8.5；指标为冬季最小月平均负荷因子；当前气候 10 年一遇的低风冬季，在 2041–2070 变为约 6.6 年一遇（概率比 1.5）；4 °C 时概率比 1.60；只有风、季节尺度 | full text |
| Dolores-Tesillos et al. 2025, ERL 20 | 同 Kapica 的数据（C3S，8 组 EURO-CORDEX，1970–2020 对 2048–2098）；标准化能源生产指数 SREPI < −1.28；冬季光伏干旱日增加 37%（柏林）；北欧光伏干旱更频、更长、更强，与云量增加一致；建议研究阻塞对未来能源干旱的作用 | full text（arXiv v2 预印本） |
| Qiu et al. 2026, Nature Energy 11:1449 | 美国新英格兰与得州，12 km 气候预估加县级系统优化；到世纪中充裕度不足的频率最多增加 5 倍；按气候预估调整选址可低成本缓解 | abstract only（付费） |
| Effenberger et al. 2025, arXiv 2512.07429 | 用机器学习模拟器把 CMIP6 降尺度到中欧；**到本世纪末，风光同时干旱的天数减少**，可能因为风能干旱的季节发生了移动；区域模式给出的复合干旱天数多于驱动它的全球模式 | abstract only（据检索摘录） |
| Effenberger & Knutti 2026, Environ. Res. Commun. 8:081009 | 31 组区域—全球模式组合（阿尔卑斯）；风速的预估变化主要由全球模式决定，山区例外；太阳辐射的不确定性来源随季节变化 | abstract only |
| Zheng et al. 2024, Nat. Commun. 15:5225 | 1980–2022 年**历史**趋势：极端短缺事件在频率、持续时间、强度上都在上升；极端低可靠事件的持续时间在 1980–2000 与 2001–2022 之间增加 4.1 h | abstract only |
| Kapica et al. 2024, RSER 189:114011 | C3S 日容量因子，NUTS-2，8 组 EURO-CORDEX，RCP4.5/8.5；1970–2020 对 2048–2098；干旱日 = 低于基准期该季节第 20 百分位；多数模式预估 40°N 以北光伏干旱天数增加、南欧减少；风电的模式一致性低；结论按"几个模式同意变化方向"给出。详见第 7.2 节 | full text |
| Liu et al. 2024, GRL | 美国西部与得州：历史干旱的模拟对模式偏差比对分辨率更敏感；分辨率影响未来变化的模拟结果 | abstract only |
| Zuo et al. 2024, Renew. Energy 225:120308 | 中国，基于 CMIP6 的未来能源干旱风险 | title only |
| Broomandi et al. 2026, Energy Rep. 16:109722 | 全球综述；对气候变化信号比 Ostraszewski 更肯定，两者有分歧 | SF: full text |
| Wohland et al. 2025（Climate2Energy） | CESM2，SSP3-7.0：供热需求 −10% 到 −50%，南欧水电 −10% 到 −40%，制冷需求增加超过 100% | full text |
| Jerez et al. 2019 | 风光合计变率的预估变化很小，低于 ±5%（2070–2099 对 1971–2000） | abstract only |

⚠️ **这些结论不能合并成一个结论**：Effenberger 2025 发现中欧风光同时干旱的天数减少，Lin 2026 发现全球闪电式干旱的持续时间增加，Aminimehr 2026 说升温加剧复合干旱。三者的事件定义、区域、情景和模式都不同，Ostraszewski 2027 也认为气候变化信号仍不确定。

### 5.4 需求侧极端

| 文献 | 内容 | 阅读范围 |
|---|---|---|
| Mudhar et al. 2026, Meteorol. Appl. | 平流层爆发性增温（SSW）之后，北欧和中欧出现约 120% 气候态的极端电力需求的概率高 1.5–3 倍 | SF: abstract only |
| van der Most et al. 2024 | 南欧夏季的能源干旱由制冷需求增加和来水减少共同造成 | preprint full text |

### 5.5 规划中怎样使用极端（与聚合最相关）

| 文献 | 内容 | 阅读范围 |
|---|---|---|
| **de Marco et al. 2025**, Adv. Appl. Energy 19:100235 | CESM2 SSP3-7.0 2080–2100 的 60 个未来气候年；影子价格定义压力事件，Wasserstein 距离加 k-medoids 聚成 5 类带概率的代表年；随机优化加 EENS 约束；相同 EENS 下平均便宜 148 亿欧元；陆上风电加储氢是有效的应对。详见第 7.1 节 | full text（补充材料未读） |
| Grochowicz et al. 2024, ERL 19:054038 | 40 年，用影子价格识别驱动投资的困难时段；纯气象方法识别不出哪些事件造成最大系统压力 | full text |
| **Grochowicz, Bloomfield & Victoria 2026**, Nature Sustainability（DOI 10.1038/s41893-026-01897-6），**DTU Wind and Energy Systems** | PyPSA-Eur，90 节点，ERA5 1941–2021 共 80 年（**只有历史**）；影子价格定义 SDE，按系统影响分成 4 类（严重功率缺口 6 次、功率缺口、连锁 9 次、能量缺口 14 次）；作者写明："Future work using these [CMIP7] runs will allow for benchmarking of the historical stress tests in a warmer climate"，"it remains to be seen whether frequency, severity or weather risks of SDEs will shift" | full text（arXiv v2，2026-06-08） |
| **van Duinen et al. 2026/27**, Appl. Energy（DOI 10.1016/j.apenergy.2026.129090） | 从 PECD 4.2 的 180 个气候年（6 个 CMIP6 模式 × 2016–2045，SSP2-4.5，**假定无趋势**）中选代表年；代价函数为季节性切片 Wasserstein 距离（SSWD，冬夏取大）；模拟退火优于随机搜索、过滤随机搜索和 k-medoids；有效样本量为子集的 4–5 倍；比 ERAA25 的 36 年代表 2.5–3.5 倍；作者承认 k-medoids 可能漏掉极端，关注极端的研究需要在其上"weigh custom-chosen extremes more heavily" | full text（arXiv v1 预印本，非正式版） |
| Hilbers, Brayshaw & Gandy 2023, Appl. Energy 334:120624 | 后验时间序列聚合：先粗算设计，再跑全序列调度，按发电成本或缺电量把 5% 的"极端日"单独聚合，保持时序以表示储能；30 年聚成 120 个代表日时缺电量约降为 1/20；数据为 1980–2017 历史序列；作者称这是"a step towards the use of climate model data" | full text（arXiv v1） |
| Plaga & Bertsch 2023, Appl. Energy 331:120384 | 能源系统模型中处理气候不确定性方法的系统综述 | **not accessed**（付费，无摘要） |
| Ruggles et al. 2024, Adv. Appl. Energy 15:100185 | 只有风、光和储能时，规划出高度可靠的系统（十年零失负荷）需要近 40 年的天气数据；若允许可调度电源供应 5% 的需求，15 年即可；考虑的年份越多，提高充裕度的边际成本越高 | abstract only |
| Gøtske et al. 2024, Nat. Commun. 15:10680 | 62 个天气年；用含复合事件的年份设计的系统更稳健 | full text |
| Moglianesi et al. 2025, J. Clean. Prod. 536:147180 | 比利时：投资模型中纳入 Dunkelflaute 事件，增加氢能电厂或小型模块堆，年成本增加 14%–23%（据 Nayak §1.1 的转述） | title only |
| Öberg et al. 2025, Energy 335:137780 | 英国：跨年两阶段策略，以 10 年天气检验稳健性（据 Nayak §1.1 的转述） | title only |
| Kebrich et al. 2026, iScience 29:114929 | 按单一年份优化，在其他天气年下发现供电缺口就迭代修改，德国 40 个运行年 | abstract only |
| Karkossa et al.（arXiv） | 85 年再分析；从天气到功率的建模选择几乎不改变干旱发生的频率，但能使所需装机变化多达 480 GW | SF: abstract only |

### 5.6 极端统计量需要多长记录（Q2 Part 1）

| 文献 | 内容 | 阅读范围 |
|---|---|---|
| Ruggles et al. 2024 | 同上：高可靠系统需要近 40 年数据 | abstract only |
| Gökalp & Yeşilyurt 2026, SETA 94:105452 | 土耳其 25 年 ERA5：同样 2020–2024 这段记录，阈值按全记录估计还是按窗口自身估计，广泛干旱天数会从每年 4.8 天变为 6.8 天 | SF: abstract only |
| Bodini et al. 2016 | 年际持续性使多年统计量的 90% 范围宽 3 倍（加拿大单站风速） | full text |

---

## 6. 待办更新（接 `05` 文件的 T1–T9）

| # | 状态 | 内容 |
|---|---|---|
| T1 | ✅ 已完成 | Nayak 稿件已导入 Zotero（`WJBRN68C`），作者按 PDF 录入并标 `meta:needs-check`；精读笔记见本文件第 1 节 |
| T1b | 待做 | 向 Matti 或 Shubham 确认稿件的投稿状态，以及 Crossref 作者列表的错误 |
| T3a | ✅ 2026-11-11 | de Marco et al. 2025 全文已读，PDF 已挂到 Zotero `2X9K7QUP`；笔记见第 7.1 节。补充材料（Fig. S2 误差、SI §8 聚类细节）未读 |
| T3b | ✅ 2026-11-11 | Kapica et al. 2024 全文已读（Zotero `FWF4MTZI`）；笔记见第 7.2 节 |
| T3c | 待做 | ENTSO-E ERAA 方法论中充裕度指标（LOLE、EENS、可靠性标准）的正式定义 |
| T3d | 待做 | Moglianesi 2025、Öberg 2025、Rosendal 2025 的摘要或全文（目前只有 Nayak 的转述） |
| T6 | 待做，**需要你提供** | 你的能源干旱研究对应的项目或路径 |
| T7 | ✅ 2026-11-11 | 读完 van Duinen 2025、Aminimehr 2026、Mostue 2026、van Duinen 2026、Grochowicz 2026、Hilbers 2023、Yu & Vautard 2025、Dolores-Tesillos 2025 全文，Mockert 2023 摘要与方法，Qiu 2026 摘要；结果见第 4.3 节表格与第 7.3 节。Zotero commit `28379cf` |
| T7c | 待做，**需要你下载** | Plaga & Bertsch 2023 综述全文；Qiu et al. 2026 全文（两篇都付费） |
| T7b | 元数据 ✅（Crossref 5/5 一致），内容未读 | de Marco 引言列出的纯统计选年方法，可作为"统计定义事件"的对照：据 de Marco 参考文献表：[26] Amorim et al. 2020, Energy 206:118089（干湿年）；[29] Victoria & Gallego-Castillo 2019, Appl. Energy 233–234:674（按相关性选）；[30] Gil et al. 2021, Energies 14:241（智利水电来水）；[31] Jerez et al. 2019, Renew. Energy 139:251（时间变率分解）；[32] Bloomfield et al. 2020, Meteorol. Appl. 27:e1858（targeted circulation types）。2026-11-11 已逐条对 Crossref 核对：5 条的标题、作者、期刊、卷、页全部一致（Bloomfield 2020 在 Crossref 中 issued 为 2019，即在线日期）。内容未读 |

---

## 7. 两篇全文精读（2026-11-11）

### 7.1 de Marco et al. 2025, Advances in Applied Energy 19:100235 [full text；补充材料未读]

**要解决的问题**（§1）：气候年的选择决定系统设计。作者把已有做法分成两类：
- 纯统计选择（干湿年、按相关性、按变率分解、按环流型聚类等），共同的不足是"selection is solely based on input data and does not consider how energy systems respond"；
- Grochowicz 2024 用系统输出识别压力时段，但没有把这些事件放进设计。

作者的目标是把"系统定义的压力事件"做成带概率的代表情景，再用随机优化设计系统。

**数据**（§3）：
- CESM2（CMIP6），SSP3-7.0，三段 20 年模拟，覆盖 2080–2100，共 60 个"未来天气年"。每年看作独立情景，"Due to internal variability … each simulated year exhibits distinct weather patterns"。
- 用 Climate2Energy 换算成需求、容量因子和水电来水。
- 模型是 ZEN-garden，欧洲 28 个国家节点（NUTS0），8760 小时，**不做时间序列聚合**，全新建设（greenfield），2050 年净零，水电装机固定。

**方法：系统感知情景缩减（SISR）**（§2.1–2.2）

```
第 1 步  对每个气候年 i 单独优化一次系统，取节点能量平衡约束的影子价格 λ

         C_t,i = Σ_n ( λᴱ_n,t,i · dᴱ_n,t,i  +  λᴴ_n,t,i · dᴴ_n,t,i )
                 （电与热的需求 × 各自的影子价格，即每小时的系统能量成本）

第 2 步  把小时按 C_t,i 从大到小排序，取到累计成本达到总成本的 50% 为止 → 压力小时
第 3 步  间隔少于 48 小时的压力小时合并为一个事件 e
第 4 步  事件按累计成本排序，保留到累计成本超过总成本的 50%

                    Σ_{t∈e} C_t,i
         g_e,i  =  ─────────────────      （事件 e 在第 i 年中的成本份额）
                    Σ_{t}   C_t,i

第 5 步  每个事件用特征向量描述：供热需求、陆上风电容量因子、光伏容量因子、水库来水，
         各取 p5、中位数、p95，× 28 个国家 = 336 维，PCA 降到 47 维
第 6 步  每一年 = 一"袋"事件向量（权重 g_e,i）；年与年之间的距离 = 两袋之间的 Wasserstein 距离
第 7 步  k-medoids 聚成 5 类；每类的中心年（medoid）作为代表年，概率 π = 该类年数 / 60
```

- 选 5 类的理由："a good balance between accuracy and complexity"，5 类时"average relative error of only 7% compared to the full 60-scenario reference"（Fig. S2，补充材料，未读；误差的具体定义未核对）。

**随机优化**（§2.3）：在 5 个代表年上做两阶段随机规划，装机对所有年相同。目标函数里没有缺电罚金，而是加约束 EENS ≤ EENS_max；改变 EENS_max 得到 16 个"韧性系统"。EENS_max = 0 即鲁棒解。

**结果**（§4）：

| 代表类 | 事件特征（原文 Table 3） | 概率 | 单年系统的 EENS 均值 |
|---|---|---|---|
| Freezing Days | 全欧供热需求高；中北部少风，南部少光 | 2/60 | 0.3% |
| Sunny but Still | 中南部光照好；北部供热需求高；西部和北部少风 | 8/60 | 5.9% |
| Calm Continent | 中北部少风；北部少光 | 14/60 | 2.2% |
| Dark North, Cold South | 北部少风；南部供热需求最高 | 18/60 | 2.2% |
| Fragmented Dunkelflaute | 南北少风；中部少光 | 18/60 | 4.8% |

- 严重事件集中在 11 月到 3 月，持续时间中位数 9.7 天（四分位距 6.7–14 天）。
- 60 个单年系统之间装机差别很大：光伏 676–1054 GW，陆上风电 512–840 GW，电池 0.5–1.3 TWh，储氢 4.7–19.5 TWh（§5）。
- 相同 EENS 下，韧性系统比单年系统平均便宜 148 亿欧元（§4.2.1）。
- 边际韧性成本：EENS > 1% 时每降低 1 个百分点约 58 亿欧元；EENS < 1% 时约 290 亿欧元（§4.2.1）。
- 单年系统平均多装光伏 20%、陆上风电 7%、燃气轮机 171%、电池 75%、储氢 130%（§5）。
- 长时储能：储氢在高韧性区成为最有效的手段，电池只做日循环（Fig. 9）。

**作者自述的局限**（§5）：单年、全新建设，不含转型路径；每个情景内是完全预见（perfect foresight），可能高估极端事件中的表现。未来工作：转型路径、制冷和交通、需求响应、基础设施受损、其他地区与空间尺度。

**和你的方向的关系**（我的判断）：
- [QUOTE] 它聚合的对象就是"多日能源短缺事件"，而且是在未来气候数据上。所以"把能源极端聚合成少数带权重的事件类"本身已经有人做了。
- [INFERENCE] 它的事件是**模型内生**的：影子价格来自"为该年单独优化的系统"（第 1 步）。换一个模型、换一个装机，事件集合就会变。文中没有检验事件对模型设定的敏感性。
- [INFERENCE] 它只有**一个时段**，没有基准期，所以回答不了"气候变化使哪类事件变多、变长、变强"。60 年在 2080–2100 内被当作平稳样本，原文没有讨论这一假设。
- [INFERENCE] 单一模式（CESM2）、单一情景（SSP3-7.0）。Kapica 2024 显示不同模式对干旱变化的方向经常不一致，所以单模式得到的 5 类事件及其概率，模式间是否稳定是一个开放问题。
- [QUOTE] 作者在讨论（§5）末尾把"applying the methodology to other world regions and at different spatial scales"列为未来工作，这和你的岛屿/空间尺度问题有联系。

### 7.2 Kapica et al. 2024, Renewable and Sustainable Energy Reviews 189:114011 [full text]

**研究问题**（§1，原文三问）：到 2048–2098 年，光伏、风电和风光混合的能源干旱总天数怎样变化；未来干旱的空间分布；不同气候模式是否一致。

**数据**（§2.1）：
- C3S Climate Data Store 的能源数据集：**日**容量因子，NUTS-2 区域平均，已做偏差订正，只有陆上风电（Vestas V136，100 m 轮毂）。
- 8 组 EURO-CORDEX 区域—全球模式组合（Table 1），RCP4.5 和 RCP8.5。
- 基准期 1970–2020，未来期 2048–2098，原文称"Using 49-year periods"；"Sensitivity tests show that the historical results are not sensitive to the choice of reference period"。

**方法**（§2.2）：

```
阈值  = 基准期内、该区域、该季节容量因子的第 20 百分位（未来期沿用同一阈值）

          ⎧ 0   CF(d) ≥ 阈值
DR(d) =   ⎨
          ⎩ 1   CF(d) < 阈值

N = Σ DR(d)       某季节、某时期的干旱总天数
ΔN = N_未来 − N_基准

混合系统：CF_H,d = a · CF_PV,d / CF_PV,max + (1 − a) · CF_WE,d / CF_WE,max，a = 0.5
```

- 结论按"8 个模式中有几个预估增加"给出：≥ 5 视为多数增加，≤ 3 视为多数减少，4 为各半。

**结果**（§3、§5）：
- 光伏：多数模式预估 40°N 以北（西欧、中欧、东欧）干旱总天数增加，南西班牙、意大利、希腊、土耳其减少。冬季和秋季增加约 +20 到 +70 天，RCP8.5 下东北部超过 +100 天；夏季法国大部分地区减少超过 100 天（Fig. 5）。
  - 这些是 49 年、一个季节的**累计**天数。原文说"100 days is around 1 % of the total days observed in each period, so these are relatively minor changes"。[INFERENCE] 按 100 ÷ 49 计算，约等于每年 2 天。
- 风电：模式间一致性明显较低，中欧尤其如此；夏季西班牙和土耳其多数模式预估减少。
- 混合：冬季多数模式预估增加 +10 到 +70 天；结果接近风电，但变化的可能性更低。
- 模式选择是关键："using one climate change projection is not enough to gain rigorous results concerning system reliability"（§3）。

**作者对模式不一致的解释**（§4）：
- 风光的气候变化信号小于年际变率（引 Bloomfield 2021）；
- 少数极端模式年份影响结果；
- NUTS-2 区域可能只有几个模式格点，空间平均引入噪声。

**局限**（§4）：只用当前技术的功率曲线；不考虑未来装机布局；只有陆上风电；只有 8 组模式，EURO-CORDEX 的土地利用是静态的（引 Wohland）。未来工作：加入海上风电，与系统模型合作识别关键时段，**加入电力需求**，用更多预估。

**和你的方向的关系**（我的判断）：
- [QUOTE] 它是"多模式比较当前与未来能源干旱"的直接先例，结论是风电干旱变化的模式一致性低。
- [INFERENCE] 它的指标只是**超阈值的总天数**，没有事件（持续时间、强度、空间同时性），没有需求、水电，也没有聚合。所以它回答"有多少干旱日"，不回答"哪些类型的事件变了"。
- [INFERENCE] 阈值固定在基准期，所以 ΔN 同时包含平均值移动和变率变化，两者没有分开。如果你的研究要区分"均值变化"和"极端本身的变化"，这里是一个可以改进的点。
- [INFERENCE] 两篇互补：de Marco 有事件聚类、没有当前对未来；Kapica 有当前对未来和多模式、没有事件和聚类。把两者连接起来（多模式下，事件类型及其权重的变化）是一个候选研究问题；T7 排查结果见第 4.3 节。

### 7.3 T7 排查读到的其他文献（2026-11-11）

| 文献 | 数据与时段 | 事件定义 | 聚合/分类 | 气候变化 | 与你方向的关系 [INFERENCE] | 阅读范围 |
|---|---|---|---|---|---|---|
| van Duinen et al. 2025, RSER | LENTIS 1600 年，24 国，日 | 7 日剩余负荷最高、重现期 1 年 | 国家按同时发生概率聚类（UPGMA），天气型（4 类，Z500 EOF + k-means）分配事件 | 无，当前气候 | 方法（天气型 + 风险比）可直接搬到未来气候；作者建议多模式 | full text |
| Aminimehr et al. 2026, CEE | 11 个 CMIP6，SSP5-8.5，日，格点，全球 | SREI（Clayton copula）< −1.28（2026-11-16 更正），1/3/5 日滑动 | 无聚合；XGBoost 归因 | 工业化前对 1.5/2/3 °C | 窗口越长（5 日），持续时间和频率的变化越大，说明变暖主要影响多日持续的条件；无需求、无偏差订正 | full text（accepted preview） |
| Mostue et al. 2026, iScience | 5 个 CMIP6，SSP5-8.5，6 小时，100 m | 风速 < 3 m/s | 无 | 1980–1999 对两个未来期 | 只有风；模式间差别大于两个未来期之差 | full text |
| Yu & Vautard 2025, ERL | 10 组 EURO-CORDEX，RCP8.5 | 冬季最小月平均负荷因子 | 无 | 1971–2000、2000–2029、2041–2070；升温水平 | 季节尺度、只有风；给出重现期的变化 | full text |
| Dolores-Tesillos et al. 2025, ERL | 同 Kapica | SREPI < −1.28 | 无 | 1970–2020 对 2048–2098 | 用标准化指数重做 Kapica；只有风光；明确建议研究阻塞和剩余负荷（SRLI） | full text（预印本 v2） |
| van Duinen et al. 2026/27, Appl. Energy | PECD 4.2，180 年（6 模式 × 30 年，SSP2-4.5） | 不定义事件 | 代表年选择（模拟退火 + SSWD） | 假定无趋势 | 你的 Q2 和"极端保留"都在其局限之外 | full text（预印本 v1） |
| Grochowicz, Bloomfield & Victoria 2026, Nat. Sustain.（DTU） | ERA5 80 年，PyPSA-Eur 90 节点 | 影子价格 SDE | 4 类 SDE | 无，明确列为未来工作 | 直接接口：同一部门，同一事件框架，缺的是气候变化 | full text（预印本 v2） |
| Hilbers et al. 2023, Appl. Energy | 1980–2017，6 区模型 | 发电成本或缺电量最高的 5% 日 | 极端日与普通日分开聚合 | 无，称是走向气候模式数据的一步 | "保极端的聚合"已有方法，但在平稳历史数据上 | full text（预印本 v1） |
| Mockert et al. 2023, Meteorol. Appl. | ERA5 1979–2018，德国 | 48 h 滑动平均容量因子 < 0.06 | 7 类天气型 | 无 | 德国 Dunkelflaute 多在 European Blocking 下、且天气型持续时间长于常态 | abstract + methods（预印本 v1） |
| Qiu et al. 2026, Nature Energy | 美国，12 km 预估 | 充裕度不足 | — | 有，到世纪中频率最多 ×5 | 证明"气候变化改变充裕度风险"在美国已有顶刊结果；欧洲事件聚合层面仍未见 | abstract only |

- **不能合并的结论**：Aminimehr 认为太阳辐射是全球干旱加剧的主导因子；Dolores-Tesillos 在北欧也看到光伏干旱增加最多；Mostue、Yu & Vautard 看到风的弱风事件增加。它们的指标（SREI、SREPI、< 3 m/s、最小月负荷因子）、模式和区域都不同，不能写成"欧洲能源干旱将增加"这样的合并结论。

---

## 8. 补充解读（2026-11-16）：代表日、缩放、方案比较与物理理解

阅读范围：full text（PDF 文字，图只看图注）。推断标 [INFERENCE]。

### 8.1 代表日怎样选

- 按固定日历规则选，不按天气挑：每年取第 2、8、15、21、28、34、41、47 周的周四、周五、周六，3 小时分辨率；选 8 个分散的周是为保留季节变化，每周连续 3 天是为保留星期结构（§3，引原文参考文献 [28]）。
- 39 个年份用同样的日历位置，只是数据来自不同年份。
- 原文写"84 个代表日"，按规则只有 24 天（第 9 节 A1）。

### 8.2 缩放之后各年还有什么不同

- 缩放是分位数映射，对每个区域、每个变量分别做（§2.2，式 (2)）：代表日中某个值在本年代表日里排第几，就换成 39 年全部逐时数据中同一分位上的值。
- 由公式推出，并用数值检验过（随机序列，两个"年份"各 192 个时间步）：
  - 每年代表日个数相同，所以缩放后**取值集合完全相同**，各年只是排列不同；
  - 本年原有的高低排序保持不变。
- 年际差异只来自依赖结构，原文："harmonizes marginal distributions but does not standardize the joint spatiotemporal dependence across weather-driven supply and demand; consequently, different realizations with the same marginals can still yield different system outcomes"（§4.1.1）。四种来源：

| 来源 | 例子 |
|---|---|
| 时间上的排列 | 低风值集中在连续几天（持续静风期）还是分散在各周 |
| 地区之间的同时性 | 德国低风时英国、法国是否也低风 |
| 变量之间的同时性 | 低风是否与最高供热需求同时出现 |
| 季节位置 | 低值落在冬季还是夏季的代表周 |

- 缩放后 39 个系统的成本差别比用原始数据时小得多，最贵的年份也换了一批（§4.1.1，图 6）。
- [INFERENCE] 日历位置固定，所以一年中的极端时段如果不在这 8 周里，第一阶段完全看不到。

### 8.3 两阶段方案与单一年份方案怎样比较

1. **单一年份方案**：每一年用原始数据（不缩放）各做一次投资优化，得到 39 个系统；总成本最高的 4 年（1985、2010、1987、1996）定为极端年（§2.3.2、§4.1.1）。
2. **两阶段方案**：第一阶段，各年代表日缩放到 39 年分布后做投资优化，取成本居中的 1995 年系统为基线；第二阶段，基线装机固定，只允许追加投资，分别在 4 个极端年的原始数据上各优化一次（§2.3.2）。第二阶段用全年还是代表日，原文没有写明（第 9 节 A2）。
3. **共同的压力测试**：两类方案的装机都固定，在 39 个年份上逐年调度（全年 4 小时完全预见定储能水位和检修 → 随机强迫停运 → 逐日滚动逐时调度）；备用燃气机组容量不限、运行成本由燃气价格和碳税决定、不按失负荷价值设定，被调用即视为供电不足，由此算各区域的失负荷期望和期望缺供电量（§2.3.1，表 1）。
4. **比较三样**：装机（图 10）；充裕度，39 年平均、各区域分布（图 11）；总成本 = 投资 + 第二阶段追加投资 + 39 年平均运行成本（图 12）。

| 结论 | 依据（§4.3） |
|---|---|
| 风光投资稳定 | 4 个加强系统的风光装机几乎相同，第二阶段允许投资但没有追加风光；单一年份方案的风光装机随年份变化 |
| 靠灵活性补强 | 两阶段方案的长时储氢、燃料电池、输电和热泵更多；单一年份方案热电联产更多 |
| 充裕度更好 | 两阶段方案所有区域失负荷期望低于每年 3 小时；单一年份方案只有 1985 年达到 |
| 略贵 | 单一年份方案的期望总成本都更低，差额主要是第二阶段追加投资，运行成本略低只抵消一部分；只有充裕度相当的 1985 年可公平比较："only the 1985 weather-year based model should be used for a meaningful comparison"，约 3557 亿欧元对 3590–3682 亿欧元（按此算贵 0.9%–3.5%，比例是本笔记算的） |

- 作者的论点（§5.1）：两阶段方案贵得不多，但风光投资不随单一年份的天气变化，更符合开发商按长期气候评估项目的做法。

### 8.4 物理上怎样理解 [INFERENCE，依据写在每条后面]

1. **第一阶段风光稳定**：投资主要看长期发电量；缩放后各地的平均容量因子都等于长期平均，所以风光投资只反映长期资源（§1.1、§5.1）。
2. **基线不充裕**：缺电来自持续多天、多国同时、又逢高需求的低风期，而缩放恰好不保留这些依赖结构；原文结果与此一致：缺电集中在冬季、少数年份、以风电为主的大陆和西北欧，水电多的北欧较少（§4.2）。
3. **第二阶段不加风光，而加储氢、燃料电池和输电**：静风期风机本身几乎不发电。假设数字：静风期容量因子 0.05、全年平均 0.30，补 10 GW 缺口要多建约 200 GW 风电，而它在其余时间每年多发约 500 TWh，大部分用不上。更便宜的是把平时多余的电存成氢（储氢罐提供 TWh，燃料电池提供 GW），并从没有受影响的地区输电（结果见 §4.3，图 10；与 Grochowicz 2026 的功率缺口和能量缺口区分一致）。
4. **更贵**：先后设计，第二阶段不能回头改基线；追加的燃料电池和储氢一年只用很少时间，投资只靠少数几天回收。1985 年单一年份方案是对所有设备一起优化，恰好也能应对其他年份。
5. **其他单一年份方案不稳、不充裕**：优化只看到那一年的天气，风光装机跟着那一年的资源走；那一年没经历的极端，系统就没有准备；只有经历过最严苛天气的 1985 年方案能应对其他年份。

### 8.5 读结论时要注意的点

1. 成本结论只有一个对照（1985 年方案）（§4.3）。
2. 不足的代价由燃气价格和碳税决定，不是失负荷价值（§2.3.1）；[INFERENCE] 备用运行费用计入 39 年平均运行成本，若改用失负荷价值，成本差可能改变；原文没有做这项敏感性检验。
3. 极端年按"单一年份优化的总成本"选，属于每年单独优化的系统定义，不能跨年比较；成本排第 4 的 1996 年，缺电只排第 8（§4.2）。
4. 第二阶段的时间表示原文没有写明（第 9 节 A2）。
5. 只用 1982–2020 年再分析，气候变化列为局限（§5.2）。


---

## 9. 与 Shubham Nayak 会面：问题清单（2026-11-13 起草，2026-11-16 更新）

- 本节由原 `2026-11-13_Shubham_meeting_questions.md` 并入，该文件已删除。
- 会面时间：2026-11-16 这一周，待定。
- 本课题的立场（[01_research_plan.md](../01_research_plan.md)）：不跑优化模型（D1）；事件用供需平衡定义——剩余负荷、装机情景固定、各年用同一标准，可以算概率（D6）；面向投资问题（D10）；Nayak 的极端年和逐年缺电量只作验证（D8）。
- 标 ★ 的是时间不够时也要问的 8 个问题。2026-11-16 新增：A5、B5、C5、D1 的 (d)、D5。

### 9.1 会面目标

1. 弄清稿件里没有写明的设定（A 组）。
2. 确认"极端年怎样选"和"代表日怎样选"两处，能否由本课题的事件目录接上（B、C 组）。
3. 拿到做验证所需的数据，并确定分工（D 组）。

### 9.2 建议的顺序（约 60 分钟）

| 时间 | 内容 |
|---|---|
| 5 分钟 | 一页介绍本课题：多国、多日能源短缺事件的目录、概率和气候变化，只用数据定义 |
| 10 分钟 | A 组：核对事实 |
| 20 分钟 | B 组：极端年的选取 |
| 15 分钟 | C 组：缩放与代表日 |
| 10 分钟 | D 组：数据、分工、下一步 |

### 9.3 A 组：核对稿件里没有写明的设定

| # | 问题（英文，可直接问） | 为什么问 |
|---|---|---|
| A1 ★ | The paper says 84 representative days, but 8 weeks × Thursday–Saturday gives 24 days. Which is correct? | 时间步个数决定投资模型能看到多长的连续时段（按 24 天算是 3 天），是判断"长事件在第一阶段是否可见"的前提（§3） |
| A2 ★ | In the second stage, does the capacity optimisation use the same selected days of the extreme year, or the full year? Are all other settings the same as in the first stage? | 若仍是 24 天，第二阶段也看不到超过 3 天的事件，极端年起作用的只是数值水平和同时性；原文只说第二阶段数据"not scaled"（§2.3.2） |
| A3 | Is the backup technology also available in the capacity optimisation? Is there any adequacy constraint (LOLE or EENS) in the investment model? | 确认充裕度只在事后检验，没有进入优化；对比：de Marco 2025 把期望缺供电量写成约束 |
| A4 ★ | Were the extreme years selected by single-year system cost (Section 4.1.1) or by the stress test of the baseline (Section 1.2)? Why four years? | 原文两处说法不同（§1.2 写"as identified from the stress-test of the baseline system"，§4.1.1 写按单年成本）；两种排序也不同：1996 年成本第 4、缺电第 8（§4.2） |
| A5 | The backup cost is set by gas price and CO2 tax, not by a value of lost load. Is the backup operation included in the expected operational cost of Figure 12? Did you test a VoLL-based cost? | 两阶段方案与 1985 年方案只差 0.9%–3.5%，这个差别是否稳健，取决于不足怎样计价（§2.3.1、§4.3） |

### 9.4 B 组：极端年的选取

| # | 问题 | 为什么问 |
|---|---|---|
| B1 ★ | Did you try to rank the 39 years, or identify multi-day events, with statistics computed directly from the input data (residual load, cumulative energy deficit) and compare with the cost ranking or the loss-of-load ranking? | 本课题的切入点：数据定义的事件若能对上模型的极端，就不必先跑 39 次优化；第 10 节的风电初步排序可作开场 |
| B2 ★ | What makes 1985, 2010 and 1987 extreme: a low annual level, simultaneous low wind over many regions, or long events? When and where does the loss of load occur in these years (dates, duration, regions)? | 三种来源对应边缘分布、空间同时性、持续时间三类统计量；稿件只给出"冬季、少数几年、风电为主的区域"（§4.2） |
| B3 | Why is 1996 fourth in cost but only eighth in inadequacy? | "成本极端"与"充裕度极端"不是同一件事 |
| B4 | Which of the four second-stage systems would you recommend? Did you try to use the four extreme years jointly in one second-stage optimisation? | 若联合使用，问题就变成"选哪几个极端时段、各给多少权重"，正是聚合问题 |
| B5 | Only the 1985 single-year model reaches the same adequacy. Did you consider imposing the same adequacy level on all single-year models before comparing costs? | 成本结论目前只有一个对照（§4.3） |

### 9.5 C 组：缩放与代表日

| # | 问题 | 为什么问 |
|---|---|---|
| C1 | How were the 8 weeks and Thursday–Saturday chosen? Did you test other selections, for example by clustering or by a distribution distance? | 稿件承认代表时间步的选取仍然重要（§2.2），但用的是固定日历规则 |
| C2 | After scaling, did you check how much the spatial and cross-variable correlations (wind against demand) change? | 缩放后各年取值集合相同，差异只来自依赖结构（第 8.2 节）；改变了多少，本课题可直接量化 |
| C3 | In Figure 6, how large is the remaining spread of total system cost between the 39 scaled systems, and which years are most expensive after scaling? | 原文说缩放后最贵的年份换了一批（§4.1.1），但图中数字需要作者给出 |
| C4 | Why did you not compare with typical days plus extreme days, or with importance subsampling? | 了解作者的取舍，帮助本课题定位 |
| C5 ★ | Did the loss of load of the baseline occur inside or outside the 8 selected weeks? | [INFERENCE] 固定日历的代表日可能漏掉极端时段，这可能是基线不充裕的原因之一（第 8.2 节） |

### 9.6 D 组：数据、分工和下一步

| # | 问题 | 为什么问 |
|---|---|---|
| D1 ★ | Could I use (a) the 39-year hourly input series for all variables and regions, (b) the total system cost of each single-year optimisation, (c) the hourly loss of load of the baseline per region for the 39 years, and (d) the installed capacities of the baseline system per region and technology? | (a)(b)(c) 用于验证（Q3）；(d) 可作为本课题剩余负荷的一个固定装机情景（研究计划第 4 节） |
| D5 ★ | Can Balmorel export the hourly electricity shadow prices of the 39 single-year optimisations? | 有了它，可以按 Grochowicz 的方法从他们的结果中算出系统定义事件，与本课题的数据定义事件对照，而本课题不必自己跑模型 |
| D2 | How long does one capacity optimisation take? Would it be possible to run Balmorel with a set of events or periods that I provide? | 统计检验之后若能用模型验证一次，结论更有说服力 |
| D3 | What is the status of the manuscript? The author list registered at Crossref differs from the PDF. | 引用要用正确的元数据；Zotero 中这一条标了 `meta:needs-check` |
| D4 | Section 5.2 proposes a representative baseline that preserves temporal and spatial dependence, and the use of climate projections. Is someone already working on these? | 避免重复，确定本课题负责的部分 |

### 9.7 会前准备

1. 一页课题介绍（英文）：尚未做。
2. 各年排序的初步图：已做（2026-11-13），见第 10 节。
3. 把 A 组问题提前用邮件发给 Shubham，会上直接讨论 B、C 组：尚未做（todo A6）。


---

## 10. 初步结果：只用输入数据的统计量给 39 年排序（用于第 9 节 B1、B2；2026-11-13）

- 图：`ai_workspace/shubham_meeting/figures/year_rank_wind_onshore_indicators_1h_Mopo-regions_1982-2020_CorRES-Mopo_EUR.png`；数值在同名 `.csv`；脚本 `ai_workspace/shubham_meeting/scripts/year_ranking_wind_indicators.py`；公式在 `metrics.py`。
- 数据：Mopo pan-European VRE data（doi:10.5281/zenodo.17950648），陆上风电 SP277-HH100，逐时，UTC，1982–2020，126 个区域列，按 2025 年各区域陆上风电装机加权成一条欧洲序列（39 年平均容量因子 0.329）。
- 排名 1 = 最紧张。稿件的极端年按单年优化总成本排序为 1985、2010、1987、1996 [Nayak §4.1.1]。

| 指标 | 1985 | 2010 | 1987 | 1996 | 1995（基线） |
|---|---|---|---|---|---|
| 年平均容量因子 | 12 | 1 | 6 | 4 | 31 |
| 冬季（1、2、11、12 月）平均容量因子 | 3 | 2 | 1 | 9 | 33 |
| 最低 14 天滑动平均 | 34 | 16 | 26 | 27 | 20 |
| 冬季低于 39 年第 10 百分位（0.172）的小时数 | 1 | 25 | 4 | 6 | 14 |

- 读法：
  - 冬季平均容量因子最低的 3 年，正是稿件成本最高的 3 年（顺序不同）；1996 年排第 9。稿件中 1996 年成本第 4、缺电第 8 [§4.2]。
  - 最低 14 天滑动平均与稿件的极端年不对应（4 年排在第 16–34 位）。
  - 冬季低风小时数把 1985 年排第 1，但把 2010 年排第 25。
- 限制，会上要说明：
  1. 只有陆上风电一种技术；没有需求、水电、光伏和海上风电，所以不是剩余负荷。
  2. 权重用 2025 年装机，不是稿件 2050 年系统的装机分布。
  3. 稿件只给出成本最高的 4 年，没有给出 39 年的完整排序，所以只能核对这 4 年，不能算秩相关。需要第 9 节 D1 的数据。
  4. 按日历年划分，一个冬季被分到两个年份里。
  5. 这是 4 个指标对 4 个年份的对照，样本很小；"冬季平均最低的 3 年 = 成本最高的 3 年"可能含偶然成分，不能当作结论。
