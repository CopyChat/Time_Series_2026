# 聚合结果怎样检验；在气候变化下何时失效（2026-11-16）

- 用途：研究计划 Q2（聚合保真度）和 Q4（气候变化）；"检查什么"一节的文献依据。
- 规则：出处写到节、图或表；阅读范围 [full text]；推断标 [INFERENCE]。

## 1. 文献怎样检验聚合

### 1.1 输入层：不跑模型，比较聚合数据与全部数据

| 文献 | 检验什么 | 阅读范围 |
|---|---|---|
| Poncelet et al. 2017（IEEE Trans. Power Syst.） | 四个方面：年总量和平均容量因子（相对能量误差）；每条序列的取值分布（持续曲线的归一化均方根误差，"the most important criterion"）；序列之间的相关（相关误差）；每条序列的变率（爬坡）。原文承认没有给"medium-term dynamics"设指标（§II） | full text |
| Kotzur et al. 2018（Renewable Energy 117:474–487；2026年11月23日 用 PDF 核对原句后改正，原写 Applied Energy） | 两个指标：归一化逐时曲线的均方根误差；持续曲线的均方根误差（§3.2）。它们的好处是"allow an evaluation … before any optimization" | full text |
| van Duinen et al. 2026（Applied Energy，预印本 v1） | 代价函数：季节性切片 Wasserstein 距离（冬季和夏季取大）。基准：同样大小的随机子集。"有效样本量"= 达到同样得分所需的随机抽取年数；最好的 30 年子集相当于中等质量的 130 年随机抽取，即 4.33 倍（§4） | full text |

### 1.2 输出层：跑模型，比较用聚合数据与用全部数据设计出的系统

| 文献 | 做法与结论 | 阅读范围 |
|---|---|---|
| Kotzur et al. 2018 | 结论："Merely assessing the aggregated time series by performance indicators can lead to significant deviation from an optimal design"；依赖储能的系统，独立的典型日、典型周都不能正确表示（§6） | full text |
| Hilbers et al. 2023（Applied Energy，预印本 v1） | 指标：各类装机相对"全序列最优解"的误差，以及该设计在全序列上的缺电量（§4.3）。重复 40 次，每次按年有放回重抽样得到不同的多年序列。先验加入"最大需求日、最小风日"（方法 C）"does not further enhance performance"；按缺电量或发电成本后验找出极端日（方法 D、E），缺电量明显更低 | full text |
| Hoffmann et al. 2020（Energies 综述） | 后验方法的理由：输入中的极端值不一定是系统中的关键时刻，因为储能会平滑它们（§4.2）。列出的开放问题：应保留哪些统计特征；能否在不跑完整模型时给出精度的界；能否不靠经验找出最关键的时段（§5） | full text |

### 1.3 对本课题的含义 [INFERENCE]

1. 聚合对象是事件目录，不是时间序列。上面的输入层检验可以对应过来：
   - 取值分布 → 事件特征的分布（单个特征用 Wasserstein 距离，全部特征用能量距离）；
   - 序列之间的相关 → 国家之间同时发生的概率；
   - 变率和中期动态 → 持续时间、事件间隔、季节分布（正是 Poncelet 没有指标的部分）；
   - 尾部 → 重现水平（Yu & Vautard 2025 用 10 000 次自助法给置信区间）。
2. 容许范围：按年分块的自助法给出抽样不确定性。再加 van Duinen 的随机子集基准：随机抽多少个事件（或年份）才能达到与代表事件集相同的误差，换算成"有效样本量"。
3. Kotzur 2018 和 Hilbers 2023 都说明只看输入指标可能误导。不跑模型时的两个补救：
   - 用不需要模型的系统量检验：在全部目录和代表事件集上分别算所需储能电量（累计亏缺的最大值）和峰值缺口的高分位数；
   - 外部对照：系统定义事件（Grochowicz 2026）、Nayak 的逐年缺电量。
   - 最强的检验仍是跑一次模型（会议准备 Q4、Q8）。
4. 样本外：留出年份（Hilbers 的按年重抽样）、留出气候模式。

## 2. 气候变化下何时失效

### 2.1 文献中的做法

| 文献 | 做法与结果 | 阅读范围 |
|---|---|---|
| van Duinen et al. 2026 | 180 个气候年（6 模式 × 2016–2045，SSP2-4.5），"We assume there is no relevant forced climate signal or trend in the dataset"（§2）。代表性在有趋势时是否成立没有检验 | full text |
| Grochowicz et al. 2026 | "historical data … may under-represent the frequency of future extreme events predicted by climate models"；变暖气候下的检验列为未来工作（Discussion） | full text |
| Yu & Vautard 2025（ERL） | 概率比：用早期时段的阈值，数后期时段超过它的次数。1971–2000 年 10.3 年一遇的低风冬季，现在约 10 年一遇，2041–2070 约 6.6 年一遇；升温 1.5、2、3、4 °C 时概率比分别大于 1.13、1.46、1.53、1.60（摘要）；置信区间用 10 000 次自助法 | full text |
| Kapica et al. 2024 | 阈值固定在基准期（1970–2020）；结论按"8 个模式中有几个同意变化方向"给出 | full text |
| Mostue et al. 2026 | 每个模式的未来时段与其自身的历史时段比较；5 个模式中至少 4 个同意变化方向才算稳健（STAR Methods） | full text |
| Aminimehr et al. 2026 | 信噪比 = 多模式平均变化 ÷ 模式间标准差；再用 t 检验（5% 水平）判断变化是否显著（Methods） | full text |
| Hawkins & Sutton 2012（GRL） | 出现时间（time of emergence）= 信噪比首次超过阈值（如 1 或 2）的年份；信号由本地量对平滑后的全球平均气温回归得到；噪声取季节或年平均的年际标准差；模式间差异与内部变率分开处理（§2） | full text（Reading 大学机构库版本） |

### 2.2 对本课题的含义 [INFERENCE]

1. **失效的定义**（借用出现时间的思路）：
   - 信号 = 历史代表事件集与未来某一滑动窗口（如 30 年）事件目录之间的距离；
   - 噪声 = 同一距离在历史时段内按年自助重抽样得到的离散程度；
   - 失效时间 = 信噪比首次超过 1（或 2）的窗口。
2. **参照用模式自身的历史时段**，不用 ERA5，以免把模式偏差当成气候变化（Mostue、Kapica 的做法）。
3. **多模式**：每个模式单独算失效时间，再报告模式之间的一致程度（Kapica、Mostue）和信噪比（Aminimehr）。按升温水平分窗口，便于跨模式比较（Aminimehr、Yu & Vautard）。
4. **怎样更新**：先只重算各类事件的权重，保留原有代表事件。
   - 如果误差回到容许范围内，只需更新权重；
   - 如果仍超出，说明出现了新的事件类型或旧类型的形态变了，需要更新代表事件本身。
5. 局限：出现时间的方法原本针对气温；用到事件统计量上，是本课题的推广。
