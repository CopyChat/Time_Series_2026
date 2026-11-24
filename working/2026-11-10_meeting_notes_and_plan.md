# 2026-11-10 与 Matti 会面：记录与待办计划

- 会面：2026-11-10，Chao Tang 与 Matti Koivisto（DTU Wind and Energy Systems）
- 状态：**计划已写好，联网后执行**。本文件写于离线状态，下面的文献检索、Zotero 导入、核对都还没有做。
- 规则：执行时遵守"不写无出处的全称判断"（记忆 `no-unsupported-sweeping-claims`）；所有文献按 Crossref/OpenAlex 核对元数据，并注明阅读范围。

---

## 1. 会面要点（根据 Chao 的口述）

| # | 要点 | 说明或待确认 |
|---|---|---|
| M1 | 关键词：**two-stage modelling** 与 **data aggregation** | "两阶段"在 Nayak et al. 的稿件里指：第一阶段用长期天气分布做基线规划，第二阶段针对剩余的供电不足做针对性加强（见第 2 节）。这是否就是 Matti 说的意思，下次确认 |
| M2 | 两个方向：① **基于平均行为的情景构建**（scenario building on average behaviour）；② **能源极端**（energy extremes） | 与 Nayak et al. 两阶段框架的两步一一对应 |
| M3 | Chao 更感兴趣**极端**，并希望与自己的**能源干旱研究**相联系 | 需要 Chao 补充：能源干旱研究对应哪个项目或文件夹（见第 5 节问题） |
| M4 | 先读 **Shubham Nayak 的稿件**（`~/Downloads/ssrn-7455543.pdf`），放入 Zotero | 见待办 T1 |
| M5 | 应用分两类：**调度建模**（dispatch modelling）与**投资分析**（investment analysis） | 两类对缩减数据的要求不同：调度看时序和爬坡，投资看分布、极端和充裕度。待文献核实 |
| M6 | **供给与需求都在变化**（supply / demand changing） | 两边都要纳入：风、光、水电和温度驱动的需求 |
| M7 | 听到的词 "indequet" = **adequacy / inadequacy**（充裕度 / 供电不足） | 已由稿件要点确认（"remaining inadequacies"）。充裕度常用指标：LOLE（loss of load expectation，失负荷期望）、EENS（expected energy not served，期望缺供电量）。指标定义待从 ENTSO-E ERAA 方法论核实 |
| M8 | 气候变化：**风光平均变化小，水电和需求变化大** | 与已读文献方向一致：Jerez et al. 2019 风光合计变率的预估变化低于 ±5% [abstract]；Wohland et al. 2025（Climate2Energy）供热需求 −10% 到 −50%、南欧水电 −10% 到 −40% [full text] |

## 2. Shubham 的稿件（离线只读了第一页）

- **标题**：Integrating Long-Term Weather Distributions into Continental-Scale Energy System Planning: Impacts on Adequacy and Investment Decisions
- **作者**：Shubham Nayak, Yi Liu, Mohammadhassan Bahmani, Bjarke Tobias Olsen, Mikael Amelin, Matti Juhani Koivisto
- **来源**：SSRN 预印本 7455543（文件名推断；DOI 和元数据待联网核对）
- **第一页要点**（原文，阅读范围：仅 Highlights）：
  - 基于单一天气年的规划，在系统和区域层面都会给天气相关的资源和需求带来显著偏差；
  - 提出一种计算高效的**缩放方法**，把长期天气分布纳入容量扩展规划，显著减少这些偏差；
  - 一个**两阶段框架**针对缩放基线**剩余的供电不足**（inadequacies）做针对性加强，充裕度可与基于单个极端天气年的设计相当。
- **与本课题的关系**（推断，读全文后核实）：
  - 第一阶段（平均行为）对应"情景构建"，与 Q1 的代表性问题相关；
  - 第二阶段（极端与供电不足）对应 Chao 感兴趣的"极端"和能源干旱，与 Q2 Part 1（极端统计量需要多长记录）直接相关。

## 3. 对研究问题的影响（初步，读完文献后再定）

- 会面后的重点从"缩减方法本身"转向 **"两阶段规划中，极端部分该怎样选取和验证"**，并与能源干旱研究相连。
- 候选方向（**新颖性尚未核实**，执行 T2–T4 后再判断）：
  - **E1**：两阶段框架第二阶段使用的"极端"，应该怎样从多年数据中选？现有做法（单一极端年、最严重干旱年）够不够？极端的定义（干旱、需求峰值、供需同时极端）如何影响充裕度结果？
  - **E2**：能源干旱的统计量（持续时间、重现期、累计亏缺）需要多长记录才稳定？这是 Q2 Part 1 的极端版本。
  - **E3**：气候变化下，水电和需求的变化较大，极端（干旱与高需求同时出现）的频率怎样变？
- 注意：已知"聚类会丢掉极端、需要另加极端时段"是有文献记载的（Kotzur 2018a、Yeganefar 2020、Teichgraeber & Brandt 2022 等），E1 不能再以"没人处理极端"为前提。

## 4. 待办清单（联网后按顺序执行）

| # | 任务 | 步骤 | 完成标准 |
|---|---|---|---|
| T1 | **导入并精读 Shubham 的稿件** | ① 用 `zlib/add.py pdf … --project Time_Series_2026` 导入，必要时用 `--doi 10.2139/ssrn.7455543` 并核对 SSRN 元数据；② 打标签（`field:energy`、`topic:energy-system-optimization`、`topic:resource-variability`、`topic:energy-drought`、`location:Europe`）；③ 读全文，写阅读笔记：数据（CorRES？年份？区域？）、缩放方法、两阶段框架、极端的定义、充裕度指标、主要数字 | Zotero 中有条目和 PDF；`05` 文件中有阅读笔记，每个数字注明出处页码或章节 |
| T2 | **两阶段规划与情景构建文献** | 检索：two-stage stochastic capacity expansion + weather years；scenario reduction for capacity expansion；"average behaviour" scaling vs extreme-year design；已知起点：Göke et al. 2024 EJOR（两阶段随机规划、Benders 分解）、Hilbers 2019/2023、Gøtske 2024、Kebrich et al. 2026（迭代补强供电缺口） | 候选清单，每篇核对元数据并注明阅读范围；不在已读文献中的说法不写成结论 |
| T3 | **能源极端、充裕度与干旱文献** | 检索：resource adequacy + weather years + Dunkelflaute；extreme period selection for adequacy；LOLE/EENS 定义（ENTSO-E ERAA 方法论原文）；已知起点：Kittel & Schill 2026、Grochowicz 2024、van der Wiel 2019、Ruhnau & Qvist 2022、Stoop et al. 2024（CREDI 指数） | 核实"adequacy"相关术语，并补入术语表；整理"极端怎样定义、怎样选"的现有做法 |
| T4 | **调度与投资两类用途的要求** | 检索两类模型对缩减数据要求的比较（时序、爬坡、分布、极端）；已知起点：Teichgraeber & Brandt 2022、Hoffmann 2021、Kotzur 2021 | 一张表：用途 → 必须保留的特性 → 文献依据 |
| T5 | **供需变化与气候变化**（水电、需求 vs 风光） | 核实并补充：PECD 4.2 中水电和温度驱动需求的变量；Climate2Energy、Bloomfield 2022、Dubus 2022、Luzia 2023 | 每个变量的变化方向和幅度，附出处和情景 |
| T6 | **把会面结论接到能源干旱研究** | 找到 Chao 的能源干旱项目（需 Chao 提供路径），对比已有结果与 E1–E3 | 写出 E1–E3 中哪个能直接利用已有干旱结果 |
| T7 | **新颖性核查与问题定稿** | 对 E1–E3 各做 OpenAlex + 扩展网页检索，写明检索词和范围；结论按"找到 / 未找到（非穷尽）"表述 | 1–2 个研究问题定稿，附已知、未知、为什么重要 |
| T8 | **更新文件** | 更新 `01_research_plan.md`、`2026-11-09_discussion_summary_ZH-EN.md`、`2026-11-10_Matti_meeting_explained_zh.md`；必要时更新 `03` 会议页面；`Time_Series_2026_DATA.md` 补水电和需求变量 | 文件之间的编号和结论一致 |
| T9 | **（可选）给 Matti 的会后邮件** | 简短确认：两阶段、两个方向、Chao 侧重极端、下一步阅读 Shubham 的稿件 | 草稿放在代码块中，等 Chao 确认后再发 |

## 5. 需要 Chao 补充的信息（只有你知道）

1. 你的**能源干旱研究**是哪个项目？文件夹路径或项目名是什么？
2. Matti 是否指定了**数据**（Mopo、PECD 4.2、Shubham 稿件里用的数据）？
3. 会上是否定了**时间节点**或下次会面的时间？
4. Shubham 是否会参与合作？是否需要和他单独讨论？
5. 会上还有没有其他听不清的词？
