# 数据可比性：与 Shubham Nayak 的结果、与 Grochowicz 2026 的 SDE 清单（2026年11月27日）

决定 D19（研究计划）：当前使用的数据就是 [数据理解页](../01_data_understanding/data_understanding.html) 分析的 Balmorel_DTU 数据，也是与 Shubham Nayak 结果对比的数据。

## 1. 与 Shubham Nayak 的结果

| 层 | 状态 |
|---|---|
| 天气与需求输入（风光容量因子、来水、classic 需求、供热曲线、热泵性能系数，1982–2020） | 相同文件（2026年11月20日 MD5 核对） |
| 装机 | `MainResults.gdx`（2050 年，19 国），是否为论文的 1995 基线未知 |
| 电气化负荷 | 本课题自己构造（D18），不是他的逐时结果 |
| 模型事件（逐时调度、缺电量） | 12月1日（周二）后由 Shubham 提供（todo B1） |

收到后：核对输入文件一致；用他的逐时需求和装机替换自己构造的电气化负荷，再识别事件。

## 2. 与 Grochowicz et al. 2026 的 SDE 清单

来源：论文 Methods "Open model…"、"Weather data"、"Shadow prices…" [full text]；Grochowicz et al. 2024 §2.1.1–2.1.2 [full text]。

| 项目 | Grochowicz 2026 | 本课题 | 可比？ |
|---|---|---|---|
| 气象数据 | ERA5 1941–2021，天气年 7 月 1 日至次年 6 月 30 日 | ERA5 驱动，1982–2020，连续逐时 | 同源；重叠 1982–2020 |
| 风光转换 | atlite：100 m 风速对数律外推，Vestas V112 3 MW 功率曲线；光伏固定 35° 倾角，另有单轴跟踪和漂浮式海上风电 [2024 §2.1.1；2026 Weather data] | CorRES：GWA2 微尺度订正，多种风机技术，资源等级 | 方法不同，量级和变率可能不同；未比较 |
| 水电来水 | atlite | DTU 合集（Nayak 方法） | 方法不同 |
| 需求 | ENTSO-E 历史负荷，按采暖/制冷度日调整（van der Most 2022；Frysztacki 需求计算器），只含电力部门 | classic（回归中心估计）+ 电气化负荷（电转热、电动汽车） | **组成不同**：对方没有新增的电气化负荷 |
| 空间与输电 | 90 节点，输电量可扩 25% | 29 个区域，全欧铜板 | 不同 |
| 系统 | 每个天气年单独优化的净零电力系统；既有核电、生物质、水电约 300 GW 固定；燃料电池作备用 | 固定的 2050 年 Balmorel 装机 | 不同 |
| 事件定义 | 14 天内全系统 Σ 需求 × 影子价格 ≥ 1000 亿欧元 | 累计亏缺 > 0 的连续时段 | 不同 |

结论：输入不一样，只能比较**事件发生的时段**（召回率），不能比较事件量级。要确定输入是否可比，需要对方的逐时输入：在 `results.tar.gz`（35 GB）的预解网络里。

## 3. SDE 起止日与初步重叠

- 41 个 SDE 的起止日从论文补充材料图 S10–S12 的标注读出（41 个，与正文的事件数一致）：[sde_periods_from_pdf.txt](../ai_workspace/grochowicz_comparability/tmp/sde_periods_from_pdf.txt)。1982–2020 年内 21 个。
- 与数据理解页第 8b 节的累计亏缺事件（4433 个，全欧铜板，按最大累计亏缺排序）对照，看有无时间重叠：前 21 个事件重叠 7/21 个 SDE；前 42 个重叠 16/21；前 100 个重叠 20/21。只是初步结果：本页的事件是简化计算，SDE 起止日只精确到天。

![SDE recall](../ai_workspace/grochowicz_comparability/figures/sde_recall_1h_copperplate-29reg_1982-2020_BalmorelDTU-Grochowicz2026_EUR.png)

图：按最大累计亏缺取前 N 个事件时，21 个 SDE 中有时间重叠的比例（脚本 [sde_overlap_recall.py](../ai_workspace/grochowicz_comparability/scripts/sde_overlap_recall.py)）。
