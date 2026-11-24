# Time_Series_2026 待办

- 建立：2026年11月16日。汇总 [05](working/2026-11-10_meeting_notes_and_plan.md)、[06 §6](working/2026-11-11_Nayak2026_two-stage_adequacy_extremes.md)、[06 §9](working/2026-11-11_Nayak2026_two-stage_adequacy_extremes.md) 中还没完成的项，以及 2026年11月16日 新增的项。
- 会议准备见 [working/2026-11-17_week-1_subject_building.md](working/2026-11-17_week-1_subject_building.md)。
- 状态：⬜ 待做；🔄 进行中；✅ 完成；❓ 需要你提供或决定。
- 规则（2026年11月16日）：每次讨论后，决定写进 [01_research_plan.md](01_research_plan.md) 第 1 节，行动写进本文件；做完的项移到 E 组。

## A. 会议与决定

| # | 状态 | 内容 |
|---|---|---|
| A1 | ❓ | 课题范围："能随气候变化更新的能源极端事件数据集"（你的计划，会议准备第 3 节），会上与 Matti 确认 |
| A2 | ❓ | 已定：本课题不做代表年选择，平均部分不是研究内容（研究计划 D7）。还要定：交付的数据集是否附上别人方法得到的平均部分（例如 Nayak 的缩放或 van Duinen 的选年），还是只交付极端部分 |
| A3 | ❓ | RQ2 的表述：改为"历史事件集在未来气候下是否仍有代表性、何时失效、怎样更新"（研究计划 RQ2，待你确认） |
| A4 | ⬜ | 请 Matti 介绍 Aleksander Grochowicz、Marta Victoria（DTU Wind and Energy Systems），确认他们是否已在做 SDE 在变暖气候下的检验（CMIP7），避免重叠 |
| A5 | ⬜ | 11月17日 会后：把会上的决定写进研究计划第 1 节，清空"待确认" |
| A6 | ⬜ | 向 Shubham 提前发 [06 §9](working/2026-11-11_Nayak2026_two-stage_adequacy_extremes.md) 的 A 组问题（含 84 天与 24 天的矛盾） |
| A7 | ❓ | 你的能源干旱研究对应的项目或路径（原 T6） |
| A9 | ❓ | 岛屿贡献（第 3 版的 Réunion 迁移测试）在新课题中是否保留（研究计划第 8 节） |
| A10 | ❓ | 确认两层检验（研究计划第 6 节第 3 步）：核心是统计保真度检验，Nayak 极端年和 SDE 只作外部补充。若确认，RQ1 改写为"最少多少个带权重的代表事件，能在抽样不确定性以内再现全部事件目录的统计特征" |
| A11 | ⬜ | 定义事件目录（面向投资问题）：候选为固定的剩余负荷参考水平 F（多阈值）+ 累计亏缺递推 S_t = max(0, S_t−1 + RL_t − F)，特征为储能电量 E、峰值缺口 P、P/E、持续时间、国家、季节（[working/2026-11-16 §4](working/2026-11-16_event_definition_literature.md)）；还要定装机情景；检验用的统计量先加入 [metrics.py](metrics.py) |
| A13 | ⬜ | 定系统配置情景（D11）：装机 2–3 个水平 × 互联（无互联、完全互联；中间情形是否按实际输电容量取）；写进研究计划第 3 节"事件定义" |
| A14 | ⬜ | 在 [metrics.py](metrics.py) 中实现统计量矩阵（D12）：行 = 第 1 层统计量，列 = 国家 / 合并区域 × 系统配置，格 = 缩减数据集相对原始数据集的偏差，标出是否在自助法容许范围内 |
| A15 | ❓ | 11月23日 晨间讨论提出：充裕度目标下以系统层面回测（压缩设计放回完整序列，比较未满足电量、失负荷期望）为主要验收标准，统计指标作诊断；需要 LP 容量扩展模型，与 D1（不跑优化模型）和第 3 节第 4 层冲突。要你定：是否修改 D1；若修改，是否用 Kuepper/Teichgraeber 的 Julia 包或 PyPSA 做单节点最小版 |
| A16 | ✅ | 已定（研究计划 D16，2026年11月23日）：主干数据用 Balmorel_DTU，时期和年份同 Shubham（天气年 1982–2020，52 周年）；Mopo 作交叉检验。待你确认：事件识别在连续序列上进行、年边界不截断。理由和限制见 [working/2026-11-23 §6](working/2026-11-23_climate_adequacy_tools_validation.md) |
| A18 | ❓ | 定聚合方法（[working/2026-11-23_aggregation_methods.md §4](working/2026-11-23_aggregation_methods.md)）：建议主体为尾部单列（超过某一重现水平的事件各自作代表事件）+ 其余事件 k-medoids，权重 = 事件数份额；对照组为不单列尾部的 k-medoids、层次聚类、随机抽取、Shubham 的 tsam 周聚类、KKZ 有序选择，可选模拟退火。要你定：是否采用；尾部阈值取几年一遇。附带：问 Shubham 他安装的 tsam 版本 |
| A17 | ❓ | 要不要把热需求和热泵系数（同一合集 `heat_demand/`、`heat_pump_COP/`）按电气化情景转成电力需求，加到 classic 需求上；不加则事件目录没有“低温+低风”型事件，且气候变化部分没有需求响应（[数据理解 §10](01_data_understanding/data_understanding.html)） |
| A12 | ❓ | 11月17日 与 Matti 讨论事件定义（会议准备 Q9–Q13）：供需平衡一类、面向投资问题（D10）、装机情景、参考供给水平、分析类型、电量/气候/经济三类具体问题的取舍；数据定义的事件找不回 SDE 时课题怎样调整 |

## B. 数据

| # | 状态 | 内容 |
|---|---|---|
| B1 | ⬜ | 向 Shubham Nayak 要：39 年输入、39 个单年优化的成本排序、基线的逐年逐区域缺电量、基线各区域各技术的装机（06 §9 D1）；39 个单年优化的逐时影子价格（06 §9 D5） |
| B2 | ⬜ | Grochowicz 2026 的 SDE 清单 `sde_new_store_1941-2021_100bn_12-336h_90_elec_lc1.25_Co2L.csv`：论文的 Data availability 给出中间数据在 Zenodo doi:10.5281/zenodo.20590389，代码在 GitHub `aleks-g/stressed-system` v1.0。先查这两处是否单独提供这个文件；否则向作者要（Zenodo 上的 `results.tar.gz` 约 35 GB） |
| B7 | 🔄 | CorRES 网站（D13）：open-data 页面已读（11月20日，经 NAS 访问），只有风光数据集，清单见研究计划第 6 节。还要做：问 Matti 用哪一套（Mopo 还是 Balmorel 版，后者与 Shubham 的 Balmorel 一致）；是否申请网络服务的学术账号。DTU 访客 Wi-Fi（dtuguest）连不上 Risø 网段 130.226.56.x，要换网络或用 DTU 账号 |
| B6 | ⬜ | 下载 de Marco 2025 的 60 个未来气候年能源输入（GitHub ZEN-universe/ZEN-models 分支 Climate-resilience），核对变量、单位和时间范围 |
| B3 | ⬜ | （11月20日：CorRES 没有需求预估；Balmorel_DTU 数据只有历史 1980–2021；Mopo 气候预估只有风光、按 Mopo 区域。可考虑用 Shubham 的需求代码 `weather_to_balmorel` 加 PECD 4.2 预估气温推出未来需求，与历史需求同一方法）未来需求：比较三种做法（van der Most 框架的需求–气温拟合、Nayak 的度日法、Climate2Energy 的供热和制冷需求），选一种用于预估气温 |
| B4 | ✅ | 2026年11月23日核对 CDS 目录的约束表（见 [working/2026-11-23 §1](working/2026-11-23_climate_adequacy_tools_validation.md)）：PECD 4.2 的未来预估（2015–2100，6 个模式）**有**水电来水、水电发电量和人口加权气温，**没有**电力需求；气候模式只有 2015–2100 的预估，没有 2015 年以前的 CMIP6 历史时段（历史时段只有 ERA5）。后果：模式自己的参照时段只能取 2015 年以后的窗口 → 要定参照怎么取（见研究计划 U3） |
| B8 | ⬜ | 读 PECD 4.2 的方法文档：偏差订正以什么为目标、覆盖哪些变量（风速已知有新订正，气温、辐射、水电未核对）、订正后事件统计是否保留；决定模式阈值取 ERA5 历史还是模式 2015 年以后的窗口 |
| B5 | ⬜ | 未来水电来水的来源：PECD 4.2 的水电变量，或 Nayak 的 GloFAS 加随机森林模型能否用于预估径流 |

## C. 先行检验（会后 1–2 周）

| # | 状态 | 内容 |
|---|---|---|
| C1 | ✅ | 只用陆上风电给 39 年排序（2026年11月13日，见 06 §10） |
| C2a | ⬜ | **看历史数据第一步（Matti 建议，D14；2026年11月23日起主干数据改为 Balmorel_DTU、时期同 Shubham，见 D16，以下 Mopo 的描述作交叉检验用）**：Mopo 风光（陆上风、海上风、光伏）按区域乘 2025 装机，汇总成各国逐时发电（GW），按水文年划分。初查（11月20日）：1980–2021 逐时、UTC、126 个陆上区域、39 国、无缺测；海上 77 个区域按海域编码，要用 `Regional` 表对应到国家 |
| C2b | ⬜ | 原始数据的统计量矩阵第一版（D12 的框架）：行 = 年均、冬季均值、年际变率、低出力时段的频率和持续时间、14 天最低滑动均值；列 = 各国 + 欧洲合并 |
| C2c | ⬜ | 用数据检验 D11：同一段天气，在不同配置下（只风、只光、2025 风光比例；各国单独、各国合并）低出力事件的个数、持续时间和国家间同时发生矩阵 P(X\|Y) 怎样变化 |
| C2f | ❓ | 问 Shubham：(1) `classic_demand.csv` 的单位（MW？）；(2) 是否已施加年校正系数（Kruse 2023 附录 J.2）；(3) 是否就是 Kruse 论文的 classic 电力需求；(4) 水电来水的单位；(5) 风光装机（Existing_wind_capacities 等 Excel）能否给一份 |
| C2e | ⬜ | 量化 Shubham 的 52 周窗口丢掉的跨年周（1984、1990、1996、2001、2007、2012、2018 年末，各 7 天）：用连续序列和 52 周窗口分别识别事件，比较事件数和累计亏缺；并定 Balmorel 要求的 52 周年怎样接入跨年的代表事件（研究计划第 3 节“冬季跨年事件的探测与代表”） |
| C2d | ❓ | 历史需求：问 Matti 有没有与 1980–2021 天气年一致的逐时需求（Mopo 项目、ERAA 气候年需求或 DTU 的需求模型）；没有则按 B3 由气温推出。有了需求再算剩余负荷（C3）。11月20日 查到：Nayak 2026 §2.1.2 的电力需求由 ERA5 气温按 Kruse 2023（DTU 硕士论文）推出、供热需求用度日法，覆盖 39 年；公开的 Balmorel_data（GitHub，查了 `madsen_2025_eu-or-national`、`great_weather_year` 两个分支）只有一年的需求曲线 `DE_VAR_T.inc`（8736 小时）。→ 已找到：Shubham 的数据在 `~/local_data/Shubham_minimum_working_copy_p3/`（`classic_demand.csv` 1982–2021；水电、风光也在其中，见 [Time_Series_2026_DATA.md](Time_Series_2026_DATA.md)）。还要问 Shubham：(1) 年需求总量是否被固定（年际差 < 0.7%）；(2) "classic" 是否不含热泵和电动汽车，模型里的总电力需求怎样组成；(3) 德国 4 个区域怎样分配需求 |
| C3 | ⬜ | 有需求后：剩余负荷 + 累计亏缺递推，按会议准备第 4 节的指标识别多日事件，对照 Nayak 的极端年和 Grochowicz 2026 的 SDE（1982–2020 重叠部分） |

## D. 文献：深入阅读与核实

| # | 状态 | 内容 |
|---|---|---|
| D1 | ⬜ | **Kapica 2024、Aminimehr 2026、Mostue 2026 深入阅读**（正文已读）。要核对的三点：(1) 是否分析了多区域同时发生（空间范围）；(2) 阈值是否固定在基准期，平均值的移动与极端本身的变化是否分开；(3) 补充材料里的逐模式结果。已知（正文）：都不含需求，都不做事件聚类；Kapica 只统计 NUTS-2 的总干旱天数，Aminimehr 和 Mostue 统计格点上事件的频率、持续时间（Aminimehr 还有强度） |
| D2 | ⬜ | Dolores-Tesillos 2025：正式版与 arXiv v2 的差别；补充材料中 RCP8.5 的结果 |
| D3 | ❓ | 需要你下载：Plaga & Bertsch 2023（Applied Energy 331:120384）；Qiu et al. 2026（Nature Energy 11:1449） |
| D4 | ⬜ | de Marco 2025 补充材料：Fig. S2 中"5 类时平均相对误差 7%"的误差定义；SI §8 的聚类细节 |
| D5 | ⬜ | de Marco 引用的 5 篇统计选年方法（元数据已核对）读摘要或全文：Amorim 2020、Victoria & Gallego-Castillo 2019、Gil 2021、Jerez 2019、Bloomfield 2020 |
| D6 | ⬜ | ERAA 方法论（ACER Decision 24/2020）中充裕度的计算流程；可靠性标准部分已读（ACER Decision 23/2020 Annex I 第 18 条，2026年11月16日） |
| D7 | ⬜ | Moglianesi 2025、Öberg 2025、Rosendal 2025 的摘要或全文（目前只有 Nayak 的转述；原 T3d） |
| D8 | ⬜ | Hompes et al. 2025（arXiv 2508.21701）全文：CMIP6 中天气型不稳定，对"用历史分类套未来"的影响 |
| D9 | ⬜ | Nayak 稿件的投稿状态，以及 Crossref 作者列表的错误（原 T1b，会上问） |
| D10 | 🔄 | 你精读三篇（PDF 副本在 references/）：Nayak 2026、van Duinen 2026（预印本 v1）、Grochowicz 2026（预印本 v2）。阅读要点见 2026年11月16日 的回复 |
| D13 | ⬜ | Grochowicz 2024 补充材料：SDE 时长怎样确定（文件名中的 12–336 h） |
| D11 | ⬜ | 向 van Duinen 要选年结果（SA 选出的 5 年和 30 年），用于"代表年中极端事件是否偏少"的交叉检验；代码要在论文录用后才公开 |

| D14 | ✅ | Kuepper 2022 全文已读（2026年11月23日）：失负荷按总需求的比例；代码即 TimeSeriesClustering.jl 加 CapacityExpansion.jl；结论与讨论稿的差异见 [working/2026-11-23 §5](working/2026-11-23_climate_adequacy_tools_validation.md)。未核对：使用的求解器 |
| D15 | ✅ | Teichgraeber & Brandt 2019 全文已读：测试问题是运行优化不是容量扩展；质心与 medoid 的结论见笔记 §5；极端期选择为未来工作 |
| D16 | ⬜ | Google Scholar 补查回测式验证文献（time series aggregation、resource adequacy、backtesting），判断"极端事件 + 充裕度 + 岛屿"的验证框架是否仍有空间；同时查"Wasserstein / KS 用于聚合保真度"是否已有人做（讨论稿称没找到，未经核实） |

| D17 | ✅ | 五篇 PDF 已挂入 Zotero（2026年11月23日）：Teichgraeber 2019、Kuepper 2022、CapacityExpansion JOSS、Gøtske 2024、Göke 2022 |
| D19 | ❓ | 需要你下载：Cannon 2015（J. Climate 28:1260–1267，doi:10.1175/JCLI-D-14-00636.1，付费），读 KKZ 有序选择的算法步骤，作为聚合对照组（A18） |
| D18 | ❓ | 需要你下载：[Qiu et al. 2026（Nature Energy）](https://doi.org/10.1038/s41560-026-02109-3)，气候变化下的充裕度风险，用来核对笔记第 2 节第 10 点；另需核对 tsam 文档中 `extremePeriodMethod` 选项 |

## A'. 会上新增的问题

| # | 状态 | 内容 |
|---|---|---|
| A8 | 🔄 | 问 Matti：用"事件指标对应系统需求"加"已发表模型结果对照"，不自己跑模型，是否可行（会议准备 Q8）。11月18日：Matti 认为检验可以用缩减与原始数据集之间的统计量矩阵来做（D12）；第 4 层（完整模型）是否需要仍待定 |

## E. 已完成（2026年11月16日）

- Mostue 2026 全文从 Europe PMC（PMC12972962）读取：弱风事件 = 100 m 风速 < 3 m/s，6 小时步长，无合并规则；代码在 Zenodo 10.5281/zenodo.18392113。写入 [working/2026-11-16 §1](working/2026-11-16_event_definition_literature.md)。

- Grochowicz et al. 2024 的 PDF 已挂到 Zotero `PU99TUXJ`（Zotero commit `a7ff83a`）；原文核对了"purely meteorological approaches fail …"一句。
- 充裕度的定义与度量：ACER Decision 23/2020 Annex I 的 ENS、EENS、LOLE 定义，以及可靠性标准公式（第 18 条）。
- 06 笔记补注：Nayak"84 个代表日"与"8 周 × 3 天 = 24 天"不符。
- 文件夹整理：讨论记录移到 `working/`（加日期前缀），HTML 移到 `presentation/`；`metrics.py` 作为项目唯一的公式文件留在根目录。
- 研究计划改为第 4 版（能源极端事件 + 气候变化）；第 3 版存于 [working/2026-11-09_research_plan_v3.md](working/2026-11-09_research_plan_v3.md)。原 A5（"替换原来的 Q1、Q2"）由此完成。
