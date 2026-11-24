# 期刊选择：Time Series 2026（能源极端事件的聚合与气候变化）

- 写于 2026-11-20。参照 [XGBoost_CF_2025 的期刊清单](../../../XGBoost_CF_2025/doc/publication/journal/journal_list.md) 和 [CNU Section 61 关键词](../../../XGBoost_CF_2025/doc/publication/v3.Journal_selection/section_61.md)。
- 影响因子（IF）是 JCR 2025（2026 年 6 月发布）的数值，取自第三方汇总网站，各网站数值不一致，这里给出范围；Clarivate 官方数值未核对。投稿前以 JCR 为准。
- 对"Section 61 评审怎样看待某期刊"的判断都是推断，标 ⚠️，没有成文依据。

## 1. Nayak et al. 2026（Shubham 的文章）现在的状态

| 项目 | 结果 | 来源 |
|---|---|---|
| 类型 | SSRN 预印本，未经同行评审 | Crossref：type = posted-content，subtype = preprint，group-title = SSRN |
| 日期 | SSRN 上标为 2026-08-19 | SSRN 题录（搜索结果） |
| 期刊 | **查不到已发表的期刊版本**：Crossref 按标题检索只有这条预印本；OpenAlex 只有 "SSRN Electronic Journal" 一个出处 | Crossref、OpenAlex，2026-11-20 |
| 投给了哪个期刊 | 未知。SSRN 页面拒绝自动访问（403），没能读到页面上可能有的"submitted to"说明。Crossref 的出版者写的是 Elsevier BV，但 SSRN 本身属于 Elsevier，所以这一项不能说明投给了哪个期刊 | — |

**它在 Section 61 是什么水平**：预印本本身不算发表，在评审材料里没有期刊等级。最终水平取决于它发在哪里，要问 Shubham（todo D9），或你在浏览器里打开 SSRN 页面看有没有"submitted to"一行。

⚠️ 推断：这篇文章的参考文献和方法属于能源系统建模（Balmorel、充裕度、容量规划）。如果发在 Applied Energy 一类的能源期刊，在能源领域是 Q1 的好期刊；但在 Section 61，能源期刊算"应用期刊"，分量不如 IEEE Transactions 或运筹学期刊。这一判断没有成文依据。

## 2. 本研究与 Section 61 的对应

本研究（多国、多日能源极端事件的识别、聚类成带权重的代表事件、统计保真度检验、气候变化下的失效时间）能对应的 Section 61 关键词：

| Section 61 分支 | 关键词（第 3 层） | 本研究中的对应 |
|---|---|---|
| Automatique | Aide à la décision；Planification | 为充裕度投资规划提供极端天气输入 |
| Automatique | Incertitudes et risques | 极端事件的频率、重现期，自助法抽样不确定性 |
| Automatique | Modélisation；Recherche opérationnelle | 代表事件的选取（场景缩减）、两阶段规划 |
| Automatique | Durabilité-soutenabilité | 能源转型、气候变化 |
| Traitement du Signal | Sciences des données；Classification；Apprentissage | 事件目录的聚类、代表事件和权重 |
| Traitement du Signal | Estimation；Détection | 事件识别（累计亏缺）、尾部估计、失效时间（信噪比） |

⚠️ 推断：电力系统和能源本身是 CNU 62（能量学）和 63（电气工程）的核心领域。要在 Section 61 里得到承认，文章要突出数据科学和统计方法（聚合、保真度检验、不确定性），而不只是能源结论。

## 3. 推荐期刊

排序综合考虑：本研究的主题匹配、Section 61 的认可程度、以及没有完整模型验证（研究计划 U4）时被接受的可能。

| # | 期刊 | 出版者 | IF（JCR 2025，汇总网站） | 主题匹配 | Section 61 匹配 ⚠️ | 说明 |
|---|---|---|---|---|---|---|
| 1 | **Applied Energy** | Elsevier | 11.0–12.2 | 很高：时间序列聚合、代表期、能源系统规划的主要期刊之一 | 中：能源应用期刊 | 接受纯数据分析加简化计算（第 1–3 层验证）的可能性最大；Nayak 的参考文献多来自这类期刊 |
| 2 | **IEEE Transactions on Power Systems** | IEEE PES | 8.7–10.5 | 高：充裕度、规划、代表期 | 高：IEEE Transactions，对应 Planification、Incertitudes | 审稿人很可能要求系统模型验证（第 4 层）；与 Shubham 合作跑 Balmorel 后再投 |
| 3 | **IEEE Transactions on Sustainable Energy** | IEEE PES | 约 10（另一来源 12.5） | 高：可再生能源变率、气候影响 | 高 | 与 #2 相同，也需要系统层面的结论 |
| 4 | **Energy and AI** | Elsevier | 9.6–10.8 | 中高：数据驱动方法用于能源 | 高：IA、Sciences des données | 文章若突出聚类和统计检验方法，适合这里；开放获取（有版面费） |
| 5 | **European Journal of Operational Research** | Elsevier（EURO） | 约 6.0（JCR 2024） | 中：场景缩减和代表期是运筹学课题 | 很高：Recherche opérationnelle | 要求方法本身有运筹学贡献（如新的事件缩减方法及其误差界）；门槛高 |
| 6 | **Renewable and Sustainable Energy Reviews** | Elsevier | 16.3（JCR 2024）；18.0（未核实） | 中高 | 中 | 以综述为主，也收原创研究；适合同时有方法比较和气候变化结论的长文 |
| 7 | **Sustainable Energy, Grids and Networks** | Elsevier | 约 6.6 | 中高 | 中 | 备选；审稿较快的能源系统期刊 ⚠️（审稿时间未查） |
| 8 | **Electric Power Systems Research** / **Int. J. of Electrical Power & Energy Systems** | Elsevier | 4.3–5.6 / 约 5.3 | 中 | 中 | 备选 |

**不作首选**：Weather and Climate Extremes、Environmental Research Letters 等气候期刊。主题上适合气候分析部分（C1–C6），但属于 CNU 37（气象）的期刊，Section 61 分量弱 ⚠️。

**建议**（⚠️ 判断）：
- 只有第 1–3 层验证（不跑模型）时：首投 **Applied Energy**；方法部分写得强时考虑 **Energy and AI**。
- 若能和 Shubham 合作完成第 4 层（Balmorel 验证）：首投 **IEEE Transactions on Power Systems**，转投 IEEE Transactions on Sustainable Energy 或 Applied Energy。
- 这一选择和研究计划的 U4（不跑完整模型的验证能否被接受）相关，等与 Matti 讨论后再定。

## 4. 来源

- Nayak 2026 状态：[SSRN 题录](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7455543)（页面未能读取，只看到搜索结果的标题和日期）；Crossref `api.crossref.org/works/10.2139/ssrn.7455543`；OpenAlex `api.openalex.org/works/doi:10.2139/ssrn.7455543`
- Applied Energy：[journalmetrics.org](https://www.journalmetrics.org/journal/applied-energy-2)（11.0）、[journalsearches.com](https://journalsearches.com/journal.php?title=applied+energy)（12.2）
- IEEE TPWRS：[bioxbio](https://www.bioxbio.com/journal/IEEE-T-POWER-SYST)（8.7）、[scijournal](https://scijournal.org/ieee-t-power-syst)（10.5）
- IEEE TSTE：[journalmetrics.org](https://www.journalmetrics.org/journal/ieee-transactions-on-sustainable-energy)（10.0）、[IEEE PES](https://ieee-pes.org/publications/transactions-on-sustainable-energy/)（10）、[scijournal](https://scijournal.org/ieee-t-sustain-energ)（12.5）
- Energy and AI：[journalmetrics.org](https://www.journalmetrics.org/journal/energy-and-ai-2)（9.6）、[scijournal](https://www.scijournal.org/impact-factor-of-energy-ai.shtml)（10.8）
- EJOR：[EURO 2025 报告](https://www.euro-online.org/media_site/reports/EJOR_2025.pdf)（JCR 2024：6.0）
- RSER：[Wikipedia](https://en.wikipedia.org/wiki/Renewable_and_Sustainable_Energy_Reviews)（16.3，JCR 2024）、[bioxbio](https://www.bioxbio.com/journal/RENEW-SUST-ENERG-REV)（18.0）
- SEGAN：[scijournal](https://www.scijournal.org/sustainable-energy-grids-networks)（6.57）
- EPSR：[scijournal](https://scijournal.org/electr-pow-syst-res)（5.56）、[bioxbio](https://www.bioxbio.com/journal/ELECTR-POW-SYST-RES)（4.3）；IJEPES：[bioxbio](https://www.bioxbio.com/journal/INT-J-ELEC-POWER)（5.3）
