# WorldView 全色锐化训练数据扩充：交接文档

> 用途：交给另一个会话核对后，用于扩充 PanCollection WV3 / WV2 的训练数据。
> 文档分三部分：① 现状与目标格式；② 候选数据清单（每条标注"已核实"或"待核对"）；③ 核对清单与处理流程。
> 整理日期：2026-10-16。整理环境只能访问 github.com，其余链接与体积来自搜索摘要或估算，**请逐条核对后再用**。
> 配套文件：`datasets/catalog.yaml`（机器可读清单，`category: worldview` 与 `pansharpening`）、`docs/datasets.md` 第 2 节与第 12 节。

---

## 1. 现状与目标

### 1.1 已有数据（不需核对）

已在用 PanCollection 全部四个子集：WV3（训练约 1 万组、验证约 1,080 组、测试 20+20 景）、WV2（测试 20+20 景）、QB 与 GF2（各约 2 万组训练 + 20+20 景测试，4 波段），以及 DLPan-Toolbox。WV3 / WV2 为 8 波段，比例 4，11 bit，归一化除以 2047，波段顺序 Coastal, Blue, Green, Yellow, Red, Red Edge, NIR1, NIR2。本文档只讨论**在此基础上新增**的 WorldView 数据。

**PanCollection WV3 测试景位置（已知）**：来自里约热内卢（Rio de Janeiro）与的黎波里（Tripoli）两座城市。全分辨率（FR）测试集全部在的黎波里；降分辨率（RR）测试集两城都有。因此**新增训练数据须排除这两座城市及其周边**，含 WV-2 影像（避免跨传感器评估时泄漏）。

### 1.2 目标格式（新数据须转成此格式）

新数据须与现有 `train_wv3.h5` 完全同构。下表是常见约定，**以手头文件为准**（`h5py` 打开看 `keys()`、`shape`、`dtype`、数值范围）：

| 键 | 含义 | 形状（WV3 训练块） | 生成方式 |
|---|---|---|---|
| `gt` | 参考高分 MS | N × 8 × 256 × 256 | 原始 MS 裁块 |
| `ms` | 低分 MS | N × 8 × 64 × 64 | `gt` 经 MTF 匹配高斯模糊 + 4 倍抽取 |
| `lms` | 上采样 MS | N × 8 × 256 × 256 | `ms` 经 23 抽头多项式插值上采样 4 倍 |
| `pan` | 降分辨率 PAN | N × 1 × 256 × 256 | 原始 PAN（1024×1024）经 MTF 模糊 + 4 倍抽取 |

全分辨率测试集（`test_*_OrigScale_*.h5`）不含 `gt`，`ms` 为原始 MS，`pan` 为原始 PAN。
MTF 奈奎斯特增益直接用已有 DLPan-Toolbox 的设置（下表为其默认值，仅作参考）：

| 传感器 | MS 各波段 | PAN |
|---|---|---|
| WV3 | 0.325, 0.355, 0.360, 0.350, 0.365, 0.360, 0.350, 0.315 | 0.5 |
| WV2 | 0.35 ×7, 0.27 | 0.11 |

Wald 协议生成（`MTF`、`interp23tap`）与评估（`Q2n`、`SAM`、`ERGAS`、`HQNR`）直接用已有的 DLPan-Toolbox，不需另找工具。

### 1.3 扩充原则

1. 只收**同时含原始 PAN 与 8 波段 MS** 的 WV-2 / WV-3 数据；已锐化的 RGB 产品（xView、xBD、Google Earth 类）不可用。
2. 与 PanCollection 测试景**地理不重叠**：排除里约热内卢与的黎波里（见 §1.1）。
3. 辐射量级统一到 11 bit DN 或统一归一化；SpaceNet 与 Maxar ARD 部分产品为大气校正后的反射率，需单独处理。
4. 许可允许用于科研训练；派生数据是否可再分发按各自许可。

---

## 2. 候选数据清单

状态标记：✅ 已核实（GitHub README 或官方文件列表）；⚠️ 待核对（搜索摘要 / 文献 / 估算）。

### 2.1 首选：原始 PAN + 8 波段 MS，同传感器

#### A. Maxar Open Data Program（ARD）

| 项 | 内容 | 状态 |
|---|---|---|
| 传感器 | WV-1（仅 PAN）、WV-2、WV-3（8 波段）、GeoEye-1（4 波段） | ⚠️ 各事件实际传感器需从 STAC 元数据读取 |
| 产品 | 每瓦片三个 COG：`pan_analytic`（PAN）、`ms_analytic`（MS，WV-2/3 为 8 波段）、`visual`（RGB）；附云掩膜等数据掩膜 | ⚠️ 搜索摘要称 MS "可能有 8 波段"，需打开一个瓦片确认波段数与顺序 |
| 瓦片 | 5 km 网格，约 0.3 m 归一化分辨率，16,384 px 加 512 px 外扩 | ⚠️ |
| 辐射 | ARD 为大气校正反射率（analytic），非原始 DN | ⚠️ 核对位深与缩放系数 |
| 覆盖 | 数十个灾害事件（2017 年至今），如 Kahramanmaras-turkey-earthquake-23、Maui-Hawaii-fires-Aug-23 | ✅ STAC 根目录 https://maxar-opendata.s3.amazonaws.com/events/catalog.json |
| 体积 | 单事件 3–50 GB（Maui 约 3.5 GB）；全部约 500 GB（估算） | ⚠️ |
| 许可 | CC BY-NC 4.0（AWS 登记页、Maxar 博客）；Maxar 概览页写法不同 | ⚠️ 核对现行条款 |
| 入口 | https://registry.opendata.aws/maxar-open-data/ ；https://maxar.com/open-data ；Python 工具 https://github.com/opengeos/maxar-open-data （leafmap 可按事件检索与下载） | ✅ |
| 优点 | 免费、地理多样、WV-2/3 都有、含掩膜 | |
| 风险 | 灾后影像含烟雾 / 云 / 损毁区，需用掩膜与 NDVI 等过滤；反射率产品与 DN 分布不同；事件若覆盖里约或的黎波里（如 2024 年利比亚相关事件）须跳过 | |

#### B. SpaceNet 1–5（WV-2 / WV-3）

| 期 | 城市 | 传感器与产品 | 体积（估算） | 状态 |
|---|---|---|---|---|
| SN1 | Rio de Janeiro | WV-2，PAN 0.5 m + 8 波段 MS | 约 3 GB | ❌ **排除**：与 PanCollection WV3 RR 测试景同城（里约） |
| SN2 | Las Vegas、Paris、Shanghai、Khartoum | WV-3，PAN 0.3 m + MUL 8 波段 1.2 m + MUL-PanSharpen；常引用瓦片 PAN 650×650 / MUL 163×163 | 约 30 GB | ⚠️ 瓦片尺寸与 11 bit 待核对 |
| SN3 | 同 SN2 四城（道路） | WV-3，PAN + MUL，瓦片 1300×1300 | 约 50 GB | ⚠️ 与 SN2 影像部分重叠 |
| SN4 | Atlanta | WV-2，27 个离轴角（7°–54°），PAN + 8 波段 MS | 约 180 GB | ⚠️ |
| SN5 | Moscow、Mumbai、San Juan 等 | WV-3，PAN + MUL | 约 60 GB | ⚠️ |
| SN6 | Rotterdam | WV-2，PAN 0.5 m + **4 波段** 2 m（大气校正反射率） | 约 40 GB | ✅ 论文确认 4 波段，不满足 8 波段要求 |

- 入口：https://spacenet.ai/datasets/ ；AWS `s3://spacenet-dataset/`（Registry of Open Data https://registry.opendata.aws/spacenet/ ，需 AWS 账号 requester-pays 或免费层）。
- 许可：CC BY-SA 4.0 ✅。
- 风险：SN2/SN3 瓦片间无重叠但按 AOI 密铺，裁块时按城市划分训练 / 验证；PAN 与 MUL 为同一景的切片，配准可信。
- SN1（里约）因与测试景同城而排除；SN2–5 的城市（Las Vegas、Paris、Shanghai、Khartoum、Atlanta、Moscow、Mumbai、San Juan）均不与测试景重叠。

#### C. IARPA MVS3DM（WV-3，阿根廷 San Fernando）

- 50 景 WV-3 PAN + 8 波段 VNIR，2015-01 至 2016-01，多日期多角度，约 100 km²；附机载雷达 DSM 真值。⚠️
- 入口：https://spacenet.ai/iarpa-multi-view-stereo-3d-mapping/ （SpaceNet on AWS 托管）。⚠️ 核对 S3 路径与产品级别（NITF L1B？）
- 体积：约 20–60 GB（估算）。
- 许可：公开。⚠️
- 价值：同一区域多日期多角度，适合做视角 / 季节鲁棒性；非城市地物（农田、水体）多。

#### D. IARPA CORE3D 与 US3D / DFC2019（WV-3，Jacksonville / Omaha / UCSD / Atlanta）

- CORE3D：WV-3 多视影像 + 机载 LiDAR，三站点；入口 https://github.com/pubgeo/core3d-open → https://spacenet.ai/core3d/ 。✅ 仓库存在；⚠️ 文件列表、体积（估算 100 GB）、许可未核实。
- US3D / DFC2019：由 CORE3D 派生，IEEE DataPort https://ieee-dataport.org/open-access/urban-semantic-3d-dataset ，需账号。⚠️ **各 Track 是否提供原始 PAN 未核实**（可能只有 8 波段 MSI 与锐化 RGB）。体积估算 100–300 GB。
- 引用要求：Hagstrom et al., IGARSS 2021；Le Saux et al., GRSM 2019。

#### E. PAirMax（WV-2 / WV-3 / GeoEye-1）

- Maxar 9 对（WV-2、WV-3、GE-1）+ Airbus 5 对（Pléiades、SPOT-7，4 波段）；每对含全分辨率与 Wald 降分辨率版本。✅
- 入口：Maxar https://resources.maxar.com/product-samples/pansharpening-benchmark-dataset （接受评估许可）；Airbus https://zenodo.org/records/7706102 （加密，需向 Airbus 申请密码）。✅
- 体积：Maxar 386 MB + Airbus 154 MB。✅
- 许可：Maxar Evaluation License / Airbus License，**禁止再分发**；可用于训练但派生 h5 不能公开。⚠️ 核对条款
- 注意：主要用途是评估；若用于训练，必须确认 9 对 Maxar 场景中没有里约或的黎波里（PanCollection WV3 测试景同样来自 Maxar 样例，可能是同一批影像）。

#### F. 整景来源（需自行建数据集）

| 来源 | 内容 | 条件 | 状态 |
|---|---|---|---|
| Maxar 产品样例 https://resources.maxar.com/product-samples | WV-2/3/Legion/GE-1 各城市样例景，PAN + MS，部分含 SWIR | 填表，评估许可，禁止再分发 | ✅ 页面存在；⚠️ 当前样例城市列表待核对 |
| ESA Third Party Missions WorldView 档案 https://earth.esa.int/eogateway/catalog/worldview-esa-archive | WV-1/2/3/4，PAN、4/8 波段、SWIR，2009–2020 | EO Sign In 注册后申请，约 2 天审批；面向 ESA/EU 成员国及 Dragon 计划（含中国）科研用户，有配额 | ⚠️ 申请资格与配额以 EUSI Terms of Applicability 为准 |
| 国内代理购买 | WV-2/3 存档或新采 | 商业 | — |

### 2.2 可用但波段不匹配（仅 4 波段）

| 数据 | 内容 | 体积 | 入口 | 状态 |
|---|---|---|---|---|
| PanBench | 10 颗卫星 5,898 对；WV2 578、WV3 567、WV4 500 对；MS 256×256 **4 波段**（RGB+NIR），PAN 1024×1024 | WV 子集约 4 GB，全集约 15 GB（估算） | arXiv 2311.12083（Remote Sensing 2024, 16(16), 2899）；代码与数据链接在论文中 | ⚠️ 下载链接待核对 |
| PAirMax Airbus 子集 | Pléiades / SPOT-7，4 波段 | 154 MB | 同 §2.1 E | ✅ |

用途：与已有的 QB / GF2 同属 4 波段，可并入现有 4 波段训练流程；对 8 波段 WV3 模型则需改输入层或做波段自适应。PanBench 的 WV2 / WV3 / WV4 子集虽是 WorldView 影像，但只保留了 RGB+NIR，对 8 波段任务价值有限。

### 2.3 不可用于训练（仅锐化 RGB）

xView（WV-3 RGB，20.7 GB）、xBD / xView2（Maxar RGB，10–30 GB）、LEVIR-CD、DOTA、QXS-SAROPT 光学部分、CityDreamer GoogleEarth 等。它们没有原始 PAN / MS，无法构造训练对；但可作为全分辨率视觉对比或下游任务评测。

### 2.4 体积汇总

| 组合 | 内容 | 下载量 |
|---|---|---|
| 最小扩充 | PAirMax + SpaceNet 2 | 约 31 GB |
| 中等 | 再加 Maxar Open Data 5–10 个事件 + MVS3DM | 约 140 GB |
| 全量 | 上表全部（含 SN4、US3D） | 约 1.2 TB |

以上均为**新增下载量**，不含已有的 PanCollection。

裁成 64×64 / 256×256 训练块并写成 h5 后，有效数据通常只占下载量的 20%–40%。

---

## 3. 核对清单（交给核对会话）

按优先级排列，每项写明核对方法与通过标准。

| # | 待核对项 | 方法 | 通过标准 |
|---|---|---|---|
| 1 | ~~PanCollection WV3 测试景所在城市~~ **已提供**：里约热内卢 + 的黎波里（FR 全在的黎波里，RR 两城都有） | — | 新数据排除这两座城市；WV2 测试景城市若已知也一并排除 |
| 2 | Maxar ARD `ms_analytic` 的**波段数、顺序、位深、缩放** | 用 leafmap / rasterio 打开任一 WV-3 事件瓦片，读 `count`、`dtype`、STAC `eo:bands` | WV-2/3 瓦片为 8 波段且顺序与 §1.1 一致；记录反射率缩放系数 |
| 3 | Maxar Open Data **许可**现行文本 | 读 https://maxar.com/open-data 与 AWS 登记页 | 确认 CC BY-NC 4.0 及是否允许派生数据再分发 |
| 4 | SpaceNet 2/3/5 的**瓦片尺寸、位深、MS 波段数**、S3 路径 | 读 https://spacenet.ai/datasets/ 各期页面；`aws s3 ls s3://spacenet-dataset/` | 确认 PAN 0.3 m + MUL 8 波段 11 bit；记录每期体积 |
| 5 | SpaceNet 4 Atlanta 是否提供**原始 PAN + 8 波段 MS**（非仅锐化） | 同上 | 是则纳入，否则移至 §2.3 |
| 6 | MVS3DM 的 S3 路径、产品级别、体积、许可 | 读 SpaceNet 页面与 AWS 列表 | 得到可下载路径与实际体积 |
| 7 | US3D / DFC2019 各 Track 是否含**原始 PAN** | 登录 IEEE DataPort 看文件清单 / README | 有则纳入 |
| 8 | PAirMax Maxar 9 对的**城市**中是否含里约或的黎波里 | 读 PAirMax 论文（Vivone et al., JSTARS 2021）表 1 | 不含方可用于训练 |
| 9 | PanBench 下载链接与 WV 子集实际体积 | 读 arXiv 2311.12083 代码链接 | 得到链接 |
| 10 | ESA TPM 对 Dragon 计划（中国）用户的申请资格与配额 | 读 EUSI Terms of Applicability | 明确是否可申请 |

---

## 4. 处理流程（核对通过后执行）

### 4.1 下载与筛选

0. **地理排除**：所有来源先按经纬度剔除里约热内卢（约 22.9°S, 43.2°W）与的黎波里（约 32.9°N, 13.2°E）各 50 km 范围内的影像。
1. **Maxar Open Data**：用 `leafmap.maxar_search()` 按事件列出瓦片，筛选 `platform` 为 WV02 / WV03、`off_nadir` < 25°、云量 < 10%；下载 `pan_analytic`、`ms_analytic` 与掩膜。优先取**灾前**影像，灾后影像用掩膜去除损毁区。
2. **SpaceNet 2/3/5**：按城市下载 `PAN/` 与 `MUL/` 目录（不下载 `MUL-PanSharpen/` 与 `RGB-PanSharpen/`）。
3. **MVS3DM / CORE3D**：下载 PAN 与 MS NITF，用 GDAL 读 RPC 元数据，按同一景裁剪。
4. **PAirMax**：只在确认与测试景不重叠后使用。

### 4.2 预处理（每景）

1. 读取 PAN 与 MS，检查配准（PAN 与 MS 的地理范围、像元比例恰为 4；ARD 与 SpaceNet 已对齐，整景 NITF 需按 RPC 正射或裁同一区域）。
2. 去除 nodata、云、烟雾、水体饱和区；按云掩膜与 PAN 饱和阈值过滤。
3. 辐射统一：原始 DN（11 bit）直接用；反射率产品乘以缩放系数回到 0–2047 量级，或在归一化阶段统一到 [0, 1]。记录每个来源的处理方式。
4. Wald 协议：
   - `gt` = 原始 MS 裁 256×256；
   - `ms` = `gt` 经各波段 MTF 高斯核（§1.2 增益，核 41×41）模糊后 4 倍抽取 → 64×64；
   - `lms` = `ms` 经 `interp23tap` 上采样 4 倍 → 256×256；
   - `pan` = 原始 PAN 裁 1024×1024，经 PAN MTF 模糊后 4 倍抽取 → 256×256。
5. 裁块步长 128（MS 像元），丢弃方差过低（平坦海面、沙漠）与饱和占比 > 5% 的块。
6. 按**城市 / 事件**划分训练 / 验证（9:1），不按随机块划分，避免相邻块泄漏。
7. 写入 h5：`train_wv3_ext.h5`、`valid_wv3_ext.h5`，键与维度同 §1.2，`float32` 或 `uint16` 与原文件一致。另存一份 `meta.json` 记录每块的来源、事件、日期、离轴角。

### 4.3 质量验收

1. 用 PanCollection 上已训练的基线模型（如 PNN / PanNet / FusionNet 的公开权重）在新验证集上推理，SAM / ERGAS / Q8 的分布应与 PanCollection 验证集同量级；若系统性偏差大，优先怀疑辐射量级或 MTF 设置。
2. 混合训练（PanCollection + 新数据）后，在 PanCollection 原测试集（降分辨率 20 景 + 全分辨率 20 景）上评估，指标不应下降；再在新数据的保留城市上评估泛化。
3. 全分辨率用 HQNR / D_λ / D_s（DLPan-Toolbox 已有实现）。

### 4.4 许可与发布

- Open Data 派生数据：CC BY-NC 4.0，不可商用。
- SpaceNet 派生数据：CC BY-SA 4.0，发布需同许可。
- PAirMax / Maxar 样例派生数据：不可再分发，只能本地使用。
- 发布混合数据集时按来源分文件，各附许可说明。

---

## 5. 参考

- Deng et al., Machine Learning in Pansharpening: A Benchmark, from Shallow to Deep Networks, IEEE GRSM 2022（PanCollection）
- Vivone et al., A Benchmarking Protocol for Pansharpening: Dataset, Preprocessing, and Quality Assessment, IEEE JSTARS 2021（PAirMax）
- Vivone et al., Full-resolution quality assessment for pansharpening, arXiv 2108.06144（WV2 / WV3 FR 测试协议）
- Van Etten et al., SpaceNet: A Remote Sensing Dataset and Challenge Series, arXiv 1807.01232
- Wang et al., PanBench: Towards High-Resolution and High-Performance Pansharpening, arXiv 2311.12083
- Maxar ARD 用户指南 https://ard.maxar.com/docs/about/
