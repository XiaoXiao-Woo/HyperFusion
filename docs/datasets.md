# 遥感融合数据集目录

> 面向 HyperFusion（高光谱 / 多光谱 / 全色 / 多模态遥感图像融合）整理的公开数据集清单。
> 机器可读版本见 [`datasets/catalog.yaml`](../datasets/catalog.yaml)，可直接下载的条目可用
> [`tools/download_datasets.py`](../tools/download_datasets.py) 获取。
> 整理日期：2026-10-16。链接与规格以各数据集官方页面为准，使用前请核对许可证并按要求引用。

## 目录

1. [高光谱–多光谱融合（HSI-MSI Fusion / HSI 超分）](#1-高光谱多光谱融合hsi-msi-fusion--hsi-超分)
   - 1.1 [近景 / 实验室高光谱库](#11-近景--实验室高光谱库)
   - 1.2 [机载 / 星载高光谱场景（仿真融合基准）](#12-机载--星载高光谱场景仿真融合基准)
   - 1.3 [真实卫星 HSI-MSI-PAN 配对](#13-真实卫星-hsi-msi-pan-配对)
   - 1.4 [高光谱卫星数据源（自行配对）](#14-高光谱卫星数据源自行配对)
2. [多光谱全色锐化（Pansharpening）](#2-多光谱全色锐化pansharpening)
3. [高光谱 + LiDAR / SAR 多模态融合](#3-高光谱--lidar--sar-多模态融合)
4. [时空融合（Spatiotemporal Fusion）](#4-时空融合spatiotemporal-fusion)
5. [SAR–光学融合 / 云去除](#5-sar光学融合--云去除)
6. [高光谱下游任务（解混 / 异常检测 / 变化检测 / 去噪）](#6-高光谱下游任务解混--异常检测--变化检测--去噪)
7. [通用遥感基准（分类 / 分割 / 检测 / 变化检测）](#7-通用遥感基准分类--分割--检测--变化检测)
8. [城市级 3D 场景与视觉定位（点云 / 多视图）](#8-城市级-3d-场景与视觉定位点云--多视图)
9. [仿真协议与评价指标](#9-仿真协议与评价指标)
10. [建议的数据目录结构](#10-建议的数据目录结构)
11. [数据体积统计](#11-数据体积统计)
12. [WorldView 数据专题](#12-worldview-数据专题)

---

## 1. 高光谱–多光谱融合（HSI-MSI Fusion / HSI 超分）

### 1.1 近景 / 实验室高光谱库

这些库不是遥感影像，但因为真值（GT）干净、尺寸规整，是 HSI-MSI 融合论文最常用的仿真基准。

| 数据集 | 来源 / 传感器 | 规模 | 空间尺寸 | 波段 | 光谱范围 | 下载 | 许可 |
|---|---|---|---|---|---|---|---|
| **CAVE** | Columbia University（Cooled CCD + 可调滤光片） | 32 景 | 512×512 | 31 | 400–700 nm，10 nm 步长 | https://www.cs.columbia.edu/CAVE/databases/multispectral/ | 研究用途免费 |
| **Harvard** | Harvard（Nuance FX 液晶可调滤光相机） | 50 景（日光）+ 27 景（室内/混合光） | 1392×1040 | 31 | 420–720 nm | https://vision.seas.harvard.edu/hyperspec/ | 非商业研究 |
| **ICVL** | Ben-Gurion University（Specim PS Kappa DX4） | 201 景 | 1392×1300 | 519（原始）/ 31（常用） | 400–1000 nm（31 波段版 400–700 nm） | https://icvl.cs.bgu.ac.il/hyperspectral/ ；镜像 https://huggingface.co/datasets/danaroth/icvl | 研究用途 |
| **ARAD_1K**（NTIRE 2022） | Ben-Gurion University | 1000 景（900/50/50） | 482×512 | 31 | 400–700 nm | https://codalab.lisn.upsaclay.fr/competitions/721 ；代码仓 https://github.com/caiyuanhao1998/MST-plus-plus 提供链接 | 研究用途 |

常用划分：CAVE 20 训练 / 12 测试；Harvard 常取 50 景日光子集；ICVL 常用 31 波段 `.mat` 版本。

### 1.2 机载 / 星载高光谱场景（仿真融合基准）

按 Wald 协议把下列高光谱场景作为参考 HR-HSI，经高斯模糊 + 下采样得到 LR-HSI，经传感器光谱响应（SRF）得到 HR-MSI 后进行训练与评估。

| 数据集 | 传感器 / 平台 | 空间尺寸 | 波段 | 光谱范围 | GSD | 下载 | 备注 |
|---|---|---|---|---|---|---|---|
| **Pavia University** | ROSIS-03（机载） | 610×340 | 103 | 430–860 nm | 1.3 m | https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes | 9 类 GT；融合论文最常用 |
| **Pavia Centre** | ROSIS-03 | 1096×715 | 102 | 430–860 nm | 1.3 m | 同上 | 9 类 GT |
| **Washington DC Mall** | HYDICE（机载） | 1280×307 | 210（常用 191） | 400–2400 nm | ~2.8 m | https://engineering.purdue.edu/~biehl/MultiSpec/hyperspectral.html | Purdue MultiSpec 发布 |
| **Chikusei** | Headwall Hyperspec-VNIR-C（机载，日本筑西） | 2517×2335 | 128 | 363–1018 nm | 2.5 m | https://naotoyokoya.com/Download.html | 19 类 GT；ENVI/MATLAB 格式；CC 许可，需致谢 SAL-UTokyo |
| **Houston 2013**（DFC2013） | ITRES CASI-1500（机载） | 349×1905 | 144 | 380–1050 nm | 2.5 m | https://hyperspectral.ee.uh.edu/?page_id=459 | 附 LiDAR DSM；15 类；需邮件申请 |
| **Houston 2018**（DFC2018） | ITRES CASI-1500 | 601×2384（HSI） | 48 | 380–1050 nm | 1 m | https://ieee-dataport.org/open-access/2018-ieee-grss-data-fusion-challenge-fusion-multispectral-lidar-and-hyperspectral-data | 附多光谱 LiDAR（0.5 m）与 5 cm RGB；20 类 |
| **Indian Pines** | AVIRIS（机载） | 145×145 | 224（常用 200） | 400–2500 nm | 20 m | ehu.eus（同上） | 16 类 |
| **Salinas** | AVIRIS | 512×217 | 224（常用 204） | 400–2500 nm | 3.7 m | ehu.eus | 16 类 |
| **KSC** | AVIRIS | 512×614 | 176 | 400–2500 nm | 18 m | ehu.eus | 13 类 |
| **Botswana** | EO-1 Hyperion（星载） | 1476×256 | 145 | 400–2500 nm | 30 m | ehu.eus | 14 类 |
| **Cuprite** | AVIRIS | 250×190（ehu 裁剪版） | 188 | 400–2500 nm | ~20 m | ehu.eus；原始数据 https://aviris.jpl.nasa.gov/ | 矿物解混经典场景 |
| **WHU-Hi-LongKou** | Headwall Nano-Hyperspec（无人机） | 550×400 | 270 | 400–1000 nm | 0.463 m | https://rsidea.whu.edu.cn/resource_WHUHi_sharing.htm | 9 类；农田 |
| **WHU-Hi-HanChuan** | Headwall Nano-Hyperspec（无人机） | 1217×303 | 274 | 400–1000 nm | 0.109 m | 同上 | 16 类 |
| **WHU-Hi-HongHu** | Headwall Nano-Hyperspec（无人机） | 940×475 | 270 | 400–1000 nm | 0.043 m | 同上 | 22 类 |
| **Xiong'an（雄安马蹄湾）** | 机载多模态成像光谱仪（上海技物所） | 3750×1580 | 250 | 400–1000 nm | 0.5 m | https://geodoi.ac.cn/WebEn/doi.aspx?Id=1687 （DOI 10.3974/geodb.2021.01.02.V1） | 19 类；中文数据论文《遥感学报》2020 |
| **Urban** | HYDICE | 307×307 | 210（常用 162） | 400–2500 nm | 2 m | https://rslab.ut.ac.ir/data （镜像众多） | 解混基准，附 4/5/6 端元 GT |

ehu.eus 场景的直链（`.mat`）已写入 `datasets/catalog.yaml`，可用脚本批量下载。

### 1.3 真实卫星 HSI-MSI-PAN 配对

真实配对数据用于全分辨率（无参考）评估与跨传感器泛化测试。

| 数据集 | 卫星 / 传感器 | 内容 | 分辨率 | 下载 | 备注 |
|---|---|---|---|---|---|
| **WHU-MHF** | 资源一号 02D（ZY1-02D）AHSI + VNIC | 6 组 LR-HSI / HR-MSI 配对，含仿真与真实子集 | HSI 30 m，MSI 10 m | https://rsidea.whu.edu.cn/WHU-MHF.htm | 武汉大学 RSIDEA 发布 |
| **ZY1-02D Real HSI/MSI/PAN**（CSSNet） | ZY1-02D | 空间配准的真实 HSI（76 VNIR 波段，原 166）/ MSI（8 波段）/ PAN | HSI 30 m，MSI 10 m，PAN 2.5 m | https://github.com/rs-lsl/CSSNet （AI Studio / 百度网盘 / Kaggle / Google Drive 链接在 README） | 2023 年发布 HSI-PAN 与 HSI-MSI 配对，2024 年发布三模态 |
| **PRISMA 高光谱全色锐化基准** | ASI PRISMA | WHISPERS 2022 挑战赛 FR1/FR2（全分辨率 12 km×12 km）与 RR1/RR2（降分辨率） | HSI 30 m（239 波段 VNIR+SWIR），PAN 5 m | 影像需在 https://prisma.asi.it 注册后按需申请；工具箱 https://github.com/matciotola/hyperspectral_pansharpening_toolbox 提供申请与预处理说明 | ASI 数据政策禁止转发；工具箱含 HyperPNN、HSpeNet、R-PNN 等方法 |
| **C2Seg-AB / Berlin–Augsburg 多模态** | EnMAP 仿真 HSI（由 HyMap / HySpex 合成）+ Sentinel-2 + Sentinel-1 | 柏林、奥格斯堡两城 | HSI 30 m，S2 10 m | https://mediatum.ub.tum.de/1657312 （约 35 GB，CC BY-SA 4.0） | 可用于 HSI-MSI 融合与跨城市分割 |
| **EnMAP + Sentinel-2 配对** | EnMAP（30 m，224 波段）+ Sentinel-2（10 m） | 需自行按同期过境配对 | 30 m / 10 m | EnMAP：https://www.enmap.org/data_access/ ；S2：https://dataspace.copernicus.eu | 两者均免费开放，是当前最易获取的真实星载 HSI-MSI 组合 |
| **Hyperion + ALI 配对** | EO-1 Hyperion（30 m，242 波段）+ ALI（PAN 10 m，MS 30 m） | 同平台同时成像，天然配准 | 30 m / 10 m | https://earthexplorer.usgs.gov （EO-1 存档） | 经典真实高光谱锐化数据源 |

### 1.4 高光谱卫星数据源（自行配对）

| 卫星 / 传感器 | 波段 | 光谱范围 | GSD | 幅宽 | 获取 |
|---|---|---|---|---|---|
| **PRISMA**（ASI，意大利） | 239（VNIR 66 + SWIR 173）+ PAN | 400–2500 nm | 30 m / PAN 5 m | 30 km | https://prisma.asi.it （注册申请） |
| **EnMAP**（DLR，德国） | 224 | 420–2450 nm | 30 m | 30 km | https://www.enmap.org/data_access/ |
| **EO-1 Hyperion**（NASA/USGS，已退役） | 242（198 定标） | 400–2500 nm | 30 m | 7.7 km | https://earthexplorer.usgs.gov |
| **高分五号 GF-5 / GF-5B AHSI** | 330 | 400–2500 nm | 30 m | 60 km | 中国资源卫星应用中心 https://data.cresda.cn |
| **资源一号 ZY1-02D / 02E AHSI** | 166 | 400–2500 nm | 30 m（同平台 MSI 10 m / PAN 2.5 m） | 60 km | https://data.cresda.cn |
| **DESIS**（DLR/Teledyne，ISS） | 235 | 400–1000 nm | 30 m | 30 km | https://www.dlr.de/eoc |
| **HISUI**（JAXA，ISS） | 185 | 400–2500 nm | 20×31 m | 20 km | https://www.jspacesystems.or.jp |
| **AVIRIS / AVIRIS-NG**（NASA JPL，机载） | 224 / 425 | 400–2500 nm | 4–20 m / 1–8 m | — | https://aviris.jpl.nasa.gov/dataportal/ （免费） |
| **珠海一号 OHS**（欧比特） | 32 | 400–1000 nm | 10 m | 150 km | 商业获取 |

---

## 2. 多光谱全色锐化（Pansharpening）

| 数据集 | 卫星 | 波段 | 分辨率（PAN / MS） | 规模 | 下载 | 许可 / 备注 |
|---|---|---|---|---|---|---|
| **PanCollection** | WorldView-3 | 8 | 0.31 m / 1.24 m | 训练约 1 万块（MS 64×64，PAN 256×256，`.h5`）；测试 20 景降分辨率（256）+ 20 景全分辨率（512） | 主页 https://liangjiandeng.github.io/PanCollection.html ；代码 https://github.com/liangjiandeng/PanCollection ；PyPI `pancollection`（https://github.com/XiaoXiao-Woo/PanCollection）；镜像 https://huggingface.co/datasets/elsting/PanCollection | GPL-2.0；引用 Deng et al., IEEE GRSM 2022 |
| **PanCollection** | QuickBird | 4 | 0.61 m / 2.44 m | 训练约 1.7–1.9 万块 | 同上 | 同上 |
| **PanCollection** | GaoFen-2 | 4 | 0.8 m / 3.2 m | 训练约 2 万块 | 同上 | 同上 |
| **PanCollection** | WorldView-2 | 8 | 0.46 m / 1.84 m | 用于跨传感器泛化测试 | 同上 | 同上 |
| **PAirMax** | WorldView-2/3、GeoEye-1（Maxar 9 组）；Pléiades、SPOT-7（Airbus 5 组） | 4 / 8 | 比例 4:1 | 14 组全分辨率 + 14 组降分辨率 | Maxar：https://resources.maxar.com/product-samples/pansharpening-benchmark-dataset ；Airbus：https://zenodo.org/records/7706102 （加密，需向 Airbus Sandbox 申请密码） | Vivone et al., IEEE TGRS 2021 基准协议 |
| **DLPan-Toolbox** | — | — | — | 深度 / 传统方法 MATLAB + PyTorch 工具箱，含 Q2n、QNR、SAM、ERGAS 等评估代码 | https://github.com/liangjiandeng/DLPan-Toolbox | 与 PanCollection 配套 |
| **Landsat-8 / 9 OLI** | Landsat | 8 MS + PAN | 15 m / 30 m | 全球免费 | https://earthexplorer.usgs.gov | 公共领域 |
| **GF-1 / GF-2 / GF-6 / GF-7** | 高分系列 | 4（GF-6 WFV 8） | GF-2：0.8 m / 3.2 m；GF-1：2 m / 8 m | 中国区域 | https://data.cresda.cn | 需注册 |
| **Maxar / Airbus 样例影像** | WorldView、GeoEye、Pléiades Neo、SPOT | 4–8（WV3 另有 8 SWIR） | 0.3–1.5 m | 若干景 | https://resources.maxar.com/product-samples ；https://intelligence.airbus.com/imagery/sample-imagery/ | 评估许可，不可再分发 |

---

## 3. 高光谱 + LiDAR / SAR 多模态融合

| 数据集 | 模态 | 尺寸 / 波段 | GSD | 类别数 | 下载 |
|---|---|---|---|---|---|
| **Houston 2013** | HSI（CASI，144 波段）+ LiDAR DSM | 349×1905 | 2.5 m | 15 | https://hyperspectral.ee.uh.edu/?page_id=459 ；整理版 https://github.com/danfenghong/ISPRS_S2FL |
| **Houston 2018** | HSI（48 波段，1 m）+ 多光谱 LiDAR（0.5 m）+ RGB（5 cm） | 601×2384（HSI） | 1 m | 20 | https://ieee-dataport.org/open-access/2018-ieee-grss-data-fusion-challenge-fusion-multispectral-lidar-and-hyperspectral-data |
| **Trento** | HSI（AISA Eagle，63 波段）+ LiDAR | 600×166 | 1 m | 6 | https://github.com/tyust-dayu/Trento |
| **MUUFL Gulfport** | HSI（CASI-1500，64 波段）+ LiDAR | 325×220 | 1 m | 11 | https://github.com/GatorSense/MUUFLGulfport |
| **Berlin** | HSI（EnMAP 仿真，244 波段）+ Sentinel-1 SAR（4 通道） | 1723×476 | 30 m | 8 | https://github.com/danfenghong/ISPRS_S2FL |
| **Augsburg** | HSI（HySpex，180 波段）+ Sentinel-1 SAR + DSM | 332×485 | 30 m | 7 | https://github.com/danfenghong/ISPRS_S2FL |
| **rs-fusion-datasets**（统一加载器） | 上述 Houston / Trento / MUUFL / Berlin / Augsburg | — | — | — | `pip install rs-fusion-datasets`，https://github.com/songyz2019/rs-fusion-datasets |

---

## 4. 时空融合（Spatiotemporal Fusion）

| 数据集 | 传感器对 | 配对数 | 尺寸 | 时间跨度 | 下载 | 备注 |
|---|---|---|---|---|---|---|
| **CIA**（Coleambally Irrigation Area，澳大利亚） | Landsat-7 ETM+（25 m）/ MODIS MOD09GA（500 m） | 17 | 1720×2040 | 2001-10 ~ 2002-05 | CSIRO Data Access Portal，DOI 10.4225/08/5111AC0BF1229 | Emelyanova et al., RSE 2013；农田物候变化 |
| **LGC**（Lower Gwydir Catchment，澳大利亚） | Landsat-5 TM / MODIS | 14 | 3200×2720 | 2004-04 ~ 2005-04 | CSIRO Data Access Portal，DOI 10.4225/08/5111AD2B7FEE6 | 含 2004-12 洪水突变 |
| **AHB**（内蒙古阿鲁科尔沁旗） | Landsat / MODIS | 27 | 2480×2800 | 2013–2018 | Li et al., Science China Inf. Sci. 2020（DOI 10.1007/s11432-019-2785-y）论文附数据链接 | 物候 + 土地覆盖变化 |
| **Tianjin**（天津） | Landsat / MODIS | 27 | 2100×1970 | 2013–2019 | 同上 | 快速城市化 |
| **Daxing**（北京大兴） | Landsat / MODIS | 27 | 1640×1640 | 2013–2019 | 同上 | 城乡混合 |
| **Wuhan Dataset** | GF-1（高分）/ Landsat | 8 | — | 7 年以上 | https://github.com/lixinghua5540/Wuhan-dataset | 高分辨率时空融合，GRSL 2024 |
| **Sentinel-2 / Sentinel-3 OLCI 基准** | S2（10 m）/ S3 OLCI（300 m） | 689+ | — | — | https://zenodo.org/records/7970845 ；https://doi.org/10.5281/zenodo.14860220 | 开放许可，适合深度学习大规模训练 |

---

## 5. SAR–光学融合 / 云去除

| 数据集 | 传感器 | 规模 | 尺寸 / 分辨率 | 下载 | 许可 |
|---|---|---|---|---|---|
| **SEN12MS** | Sentinel-1（VV/VH）+ Sentinel-2（13 波段）+ MODIS 土地覆盖 | 180,662 组三元组 | 256×256，10 m | https://mediatum.ub.tum.de/1474000 | CC BY 4.0 |
| **SEN1-2** | Sentinel-1 + Sentinel-2（RGB） | 282,384 对 | 256×256，10 m | https://mediatum.ub.tum.de/1436631 | CC BY 4.0 |
| **SEN12MS-CR / CR-TS** | Sentinel-1 + 有云 / 无云 Sentinel-2 | 约 12 万组（CR）；时序版 CR-TS | 256×256 | https://patrickTUM.github.io/cloud_removal/ | CC BY 4.0 |
| **QXS-SAROPT** | GF-3 SAR（1 m）+ Google Earth 光学 | 20,000 对 | 256×256 | https://github.com/yaoxu008/QXS-SAROPT | 研究用途 |
| **WHU-OPT-SAR** | GF-1 光学（5 m）+ GF-3 SAR（5 m） | 100 对，7 类语义标注 | 5556×3704 | https://github.com/AmberHen/WHU-OPT-SAR | 研究用途 |
| **So2Sat LCZ42** | Sentinel-1 + Sentinel-2，42 城局部气候区标签 | 40 万+ 块 | 32×32 | https://mediatum.ub.tum.de/1454690 | CC BY 4.0 |

---

## 6. 高光谱下游任务（解混 / 异常检测 / 变化检测 / 去噪）

| 任务 | 数据集 | 传感器 | 尺寸 / 波段 | 下载 |
|---|---|---|---|---|
| 解混 | **Samson** | — | 95×95×156 | https://rslab.ut.ac.ir/data |
| 解混 | **Jasper Ridge** | AVIRIS | 100×100×198 | 同上 |
| 解混 | **Urban** | HYDICE | 307×307×162 | 同上 |
| 解混 | **Cuprite** | AVIRIS | 250×190×188 | ehu.eus |
| 异常检测 | **ABU**（Airport-Beach-Urban） | AVIRIS / ROSIS，13 景 | 100×100 ~ 150×150 | http://xudongkang.weebly.com/data-sets.html |
| 异常检测 | **San Diego** | AVIRIS | 100×100×189 | 同上 |
| 异常检测 | **HAD100** | 多传感器，100 景 | 64×64 | https://github.com/zhaoxuli123/HAD100 |
| 变化检测 | **Hermiston** | Hyperion，2004/2007 | 307×241×154 | https://citius.usc.es/t/17 |
| 变化检测 | **Bay Area** | AVIRIS，2013/2015 | 600×500×224 | 同上 |
| 变化检测 | **Santa Barbara** | AVIRIS，2013/2014 | 984×740×224 | 同上 |
| 变化检测 | **Farmland（江苏盐城）** | Hyperion，2006/2007 | 450×140×155 | 多篇 CD 论文代码仓附带 |
| 去噪 | **ICVL / CAVE / WDC / Houston** | 见上文 | — | 常用高斯 / 条带 / 混合噪声仿真 |
| 分类基准整合包 | **Hyperspectral benchmark（IEEE DataPort）** | 含 Indian Pines、PaviaU、Houston、Pavia（异常）、San Diego（目标）、Bay Area / Hermiston / Santa Barbara（变化）、Urban（解混） | `.mat` | https://ieee-dataport.org （DOI 10.21227/6re8-3h84） |

---

## 7. 通用遥感基准（分类 / 分割 / 检测 / 变化检测）

| 任务 | 数据集 | 规模 | 尺寸 / 分辨率 | 类别 | 下载 |
|---|---|---|---|---|---|
| 场景分类 | **UC Merced** | 2,100 | 256×256，0.3 m | 21 | http://weegee.vision.ucmerced.edu/datasets/landuse.html |
| 场景分类 | **AID** | 10,000 | 600×600，0.5–8 m | 30 | https://captain-whu.github.io/AID/ |
| 场景分类 | **NWPU-RESISC45** | 31,500 | 256×256，0.2–30 m | 45 | https://gcheng-nwpu.github.io/ |
| 场景分类 | **EuroSAT** | 27,000 | 64×64，Sentinel-2 13 波段 | 10 | https://github.com/phelber/EuroSAT |
| 多标签分类 | **BigEarthNet（v2）** | 590,326 | 120×120，Sentinel-1/2 | 19 | https://bigearth.net |
| 语义分割 | **ISPRS Potsdam / Vaihingen** | 38 / 33 幅 | 6000×6000，5 cm / 9 cm，含 DSM | 6 | https://www.isprs.org/education/benchmarks/UrbanSemLab/ |
| 语义分割 | **LoveDA** | 5,987 | 1024×1024，0.3 m | 7 | https://github.com/Junjue-Wang/LoveDA |
| 语义分割 | **GID** | 150 幅 GF-2 | 6800×7200，4 m | 5 / 15 | https://x-ypan.github.io/GID/ |
| 目标检测 | **DOTA v1.0 / v2.0** | 2,806 / 11,268 | 800–20000 px | 15 / 18 | https://captain-whu.github.io/DOTA/ |
| 目标检测 | **DIOR** | 23,463 | 800×800 | 20 | https://gcheng-nwpu.github.io/ |
| 变化检测 | **LEVIR-CD** | 637 对 | 1024×1024，0.5 m | 建筑 | https://justchenhao.github.io/LEVIR/ |
| 变化检测 | **WHU-CD** | 1 对大图（32507×15354） | ~0.2 m | 建筑 | http://gpcv.whu.edu.cn/data/building_dataset.html |
| 变化检测 | **S2Looking** | 5,000 对 | 1024×1024，0.5–0.8 m | 建筑 | https://github.com/S2Looking/Dataset |

---

## 8. 城市级 3D 场景与视觉定位（点云 / 多视图）

来源：Urbex（arXiv 2610.18356，NeurIPS 2026）及其前序工作 CityRefer、CityAnchor。此类数据由无人机倾斜摄影 / 航空 LiDAR 得到城市级点云或网格，部分附自然语言描述，用于城市尺度 3D 视觉定位（3D visual grounding）、语义 / 实例分割、航空导航与具身问答；可作为 HyperFusion 中多视图、BEV 与 3D 模态融合的扩展基准。

### 8.1 城市级 3D 视觉定位（Urbex 相关）

| 数据集 | 内容 | 规模 | 下载 | 许可 / 引用 |
|---|---|---|---|---|
| **SensatUrban** | 英国 3 座城市（Birmingham、Cambridge、York）无人机摄影测量点云，13 类语义标注 | 约 30 亿点，7.6 km² | https://github.com/QingyongHu/SensatUrban ；http://point-cloud-analysis.cs.ox.ac.uk/ （需填表申请） | Hu et al., CVPR 2021 / IJCV 2022 |
| **CityRefer** | 基于 SensatUrban 场景的 3D 视觉定位标注：对象自然语言描述 + 与 OpenStreetMap 同步的地标标签 | 约 35k 条描述，5k 地标 | https://github.com/ATR-DBI/CityRefer （Google Drive，可用 gdown） | MIT（代码）；Miyanishi et al., NeurIPS 2023 D&B |
| **STPLS3D** | 合成 + 真实航空摄影测量点云，语义（最多 18 类）与实例（14 类）标注 | 合成 62 景约 16 km²；真实约 1.27 km² | https://github.com/meidachen/STPLS3D ；https://www.stpls3d.com/ （Google Forms 申请） | 未声明许可；Chen et al., BMVC 2022 |
| **STPLS3D-Refer** | 基于 STPLS3D 合成场景的 3D 视觉定位标注，Urbex 用于零样本跨场景评估 | — | 随 CityAnchor（https://github.com/WHU-USI3DV/CityAnchor ）与 Urbex 数据包发布 | Li et al., ICLR 2025 |
| **Urbex-Data** | Urbex 训练 / 评估数据包：CityRefer 与 STPLS3D 的 BEV 图像、倾斜视图缓存、候选框与划分（`cityrefer_ND`、`cityrefer_NO`、`stpls3d`）；原始点云需另行从 SensatUrban 申请 | — | https://huggingface.co/datasets/vvangfaye/Urbex-Data （`scripts/data/download.sh`，带校验和）；代码 https://github.com/AMAP-ML/Urbex ；模型 https://huggingface.co/vvangfaye/Urbex-4B | Apache-2.0；Wang et al., NeurIPS 2026 |

说明：Urbex 将城市级 3D 定位视为主动搜索任务，由视觉语言模型智能体在多视图间探索并经强化学习决定"看哪里、如何细化、何时作答"，不依赖预先计算的实例候选。

**城市级语言-3D 推理基准（CitySTAR 及同期工作）**

CitySTAR（arXiv 2609.19911，Zhang 等）把城市级 3D 定位视为推理而非匹配：无需训练，先把大规模城市点云转为开放词汇对象的场景图，用代码生成式 LLM 工具收集属性与空间关系证据，再为查询与每个候选周边分别构建超图做双向拓扑一致性校验，最后结合 2D 视觉证据反思决策。它在 CityRefer 与 CityAnchor（即 STPLS3D-Refer）上评估，并提出新基准 CitySTAR-3D。

| 数据集 | 内容 | 规模 | 下载 | 许可 / 引用 |
|---|---|---|---|---|
| **CitySTAR-3D** | 面向推理型开放词汇定位：更广语义覆盖、更完整实例框、含属性 / 上下文实体 / 包含关系 / 邻接关系 / 空间布局的复杂描述 | 1,286 组文本-对象对（SensatUrban 686 + STPLS3D 600），15 个语义组 | 截至整理日未发布，关注 arXiv 2609.19911 | Zhang et al., 2026 |
| **3DCity-LLM-1.2M / City-3DQA** | 基于 SensatUrban、UrbanBIS、City-BIS 点云构建的城市级 3D 问答指令数据与基准 | 约 120 万条 QA | https://github.com/SYSU-3DSTAILab/3D-City-LLM | Zhou et al., arXiv 2603.23447 |
| **GeoEval3D**（GeoProg3D） | 基于分层 3D 高斯的城市级 3D 语言场评测：定位、空间推理、比较、计数、测量 | 952 组问答 | 代码链接见 arXiv 2506.23352 | Yasuki et al., ICCV 2025 |
| **OpenCity3D 基准** | 由航拍网格渲染 RGB-D 构建语言增强点云，评测建筑年代、房价、人口密度等城市问答 | — | https://opencity3d.github.io | Bieri et al., WACV 2025 |
| **OpenUrban3D** | 大规模城市点云无标注开放词汇语义分割（方法，基于 SensatUrban 等） | — | 见 arXiv 2509.10842 | 2025 |

### 8.2 城市级点云 / 网格语义与实例分割

| 数据集 | 采集方式 | 规模 | 类别 | 下载 | 许可 / 引用 |
|---|---|---|---|---|---|
| **UrbanBIS** | 无人机倾斜摄影（6 个真实城市场景） | 25 亿点，10.78 km²，3,370 栋建筑实例 | 语义 + 建筑实例 | https://vcc.tech/UrbanBIS | Yang et al., SIGGRAPH 2023 |
| **WHU-Urban3D** | 机载 LiDAR + 车载 MLS | 多城区，语义 + 实例标注 | — | https://whu3d.com ；`pip install pywhu3d`（百度网盘 / Google Drive） | 武汉大学 |
| **DALES** | 机载 LiDAR（加拿大 Surrey） | 5 亿点，10 km² | 8 | https://udayton.edu/engineering/research/centers/vision_lab/research/was_data_analysis_and_processing/dale.php | Varney et al., CVPRW 2020 |
| **Hessigheim 3D (H3D)** | 无人机 LiDAR + 多视立体，点云 + 带纹理网格 | 1.25 亿点，0.19 km² | 11 | https://ifpwww.ifp.uni-stuttgart.de/benchmark/hessigheim/default.aspx | Kölle et al., ISPRS OJPRS 2021 |
| **SUM（Semantic Urban Meshes）** | 赫尔辛基带纹理三角网格 + 采样点云 | 约 4 km² | 6 | https://3d.bk.tudelft.nl/opendata/sum/ | Gao et al., ISPRS JPRS 2021 |
| **Campus3D** | 无人机摄影测量点云（NUS 校园），分层标签 | 约 1 km² | 分层多级 | https://github.com/shinke-li/Campus3D ；http://www.aicampus3d.com/ | Li et al., ACM MM 2020 |
| **Toronto-3D** | 车载 LiDAR（Teledyne Optech Maverick） | 7,830 万点，约 1 km 道路 | 8 | https://github.com/WeikaiTan/Toronto-3D （OneDrive / 百度网盘） | CC BY-NC 4.0；Tan et al., CVPRW 2020 |
| **Paris-Lille-3D** | 车载 LiDAR（巴黎、里尔） | 1.43 亿点，约 2 km | 9（粗）/ 50（细） | https://npm3d.fr/paris-lille-3d | Roynard et al., IJRR 2018 |
| **Semantic3D** | 地面站式 LiDAR（瑞士城乡） | 约 40 亿点 | 8 | http://www.semantic3d.net/ | Hackel et al., ISPRS Annals 2017 |
| **ISPRS Vaihingen 3D** | 机载 LiDAR | 约 120 万点 | 9 | https://www.isprs.org/education/benchmarks/UrbanSemLab/ | 与第 7 节 Potsdam/Vaihingen 同源 |

### 8.3 语言驱动的航空导航 / 具身问答 / 城市视频

| 数据集 | 内容 | 规模 | 环境 | 下载 | 许可 / 引用 |
|---|---|---|---|---|---|
| **CityNav** | 语言目标航空导航，建立在 SensatUrban 点云 + CityRefer 对象之上 | 32,637 条人类演示轨迹与描述 | 真实城市点云栅格化 | https://github.com/water-cookie/citynav ；https://water-cookie.github.io/city-nav-proj/ | 数据 CC BY 4.0；Lee et al., 2024 |
| **AerialVLN** | 无人机视觉语言导航 | 8,446 条飞行路径 × 3 条指令 | 25 个城市级 UE/AirSim 场景 | https://github.com/AirVLN/AirVLN | Liu et al., ICCV 2023 |
| **OpenFly** | 航空 VLN 平台 + 大规模基准 + OpenFly-Agent | 10 万条轨迹，18 个场景 | UE、AirSim、GTA V、Google Earth、3DGS | https://github.com/SHAILAB-IPEC/OpenFly-Platform ；https://huggingface.co/datasets/IPEC-COMMUNITY/OpenFly | MIT；Gao et al., 2025 |
| **EmbodiedCity** | 城市具身智能基准平台（北京国贸区域，含真实人车流） | 多任务数据集 | UE + AirSim 仿真器 | https://github.com/tsinghua-fib-lab/EmbodiedCity | Gao et al., 2024 |
| **CityEQA-EC** | 城市空间具身问答 | 1,412 个人工标注任务，6 类 | 基于 EmbodiedCity 仿真器 | https://github.com/tsinghua-fib-lab/CityEQA | Zhao et al., EMNLP 2025 |
| **UrbanVideo-Bench** | 无人机第一视角城市视频的具身认知评测 | 1,500 段视频，5,200 道选择题 | 真实 + 仿真 | https://github.com/EmbodiedCity/UrbanVideo-Bench | Zhao et al., ACL 2025 |

### 8.4 城市级多视图三维重建（NeRF / 3DGS）

| 数据集 | 内容 | 规模 | 下载 | 许可 / 引用 |
|---|---|---|---|---|
| **UrbanScene3D** | 真实 + 合成城市场景的高分辨率航拍影像、LiDAR、网格与 UE/AirSim 仿真器 | 12.8 万张影像，16 个场景，约 136 km² | https://vcc.tech/UrbanScene3D | Lin et al., ECCV 2022 |
| **MatrixCity** | UE5 City Sample 渲染的合成城市，航拍 + 街景，含深度 / 法线 / 材质 / 点云 | Small City 2.7 km²，Big City 25.3 km² | https://github.com/city-super/MatrixCity ；https://huggingface.co/datasets/BoDai/MatrixCity | Apache-2.0（代码）；Li et al., ICCV 2023 |
| **Mill-19（Mega-NeRF）** | 无人机航拍的 Building、Rubble 两个场景 | 每场景约 2 千张影像 | https://github.com/cmusatyalab/mega-nerf | Turki et al., CVPR 2022 |
| **GauU-Scene** | 无人机 + Zenmuse L1 LiDAR 采集的大场景 3DGS 基准 | 约 1.5–6.5 km²（论文版本间不一致） | 见论文 arXiv 2404.04880 项目页 | Xiong et al., 2024 |
| **BlendedMVS / DroneDeploy 等** | 通用多视图立体数据，含部分航拍场景 | — | https://github.com/YoYo000/BlendedMVS | 作为补充 |

### 8.5 卫星 / 航空三维重建与 3D 变化检测

| 数据集 | 内容 | 规模 | 下载 | 许可 / 引用 |
|---|---|---|---|---|
| **DFC2019 / US3D（Urban Semantic 3D）** | WorldView-3 多视卫星影像 + 机载 LiDAR + 语义标签 + DSM，覆盖 Jacksonville、Omaha、Atlanta | 数千组瓦片 | https://ieee-dataport.org/open-access/urban-semantic-3d-dataset | 需 IEEE DataPort 账号；Le Saux et al., GRSM 2019 |
| **WHU-TLC（SatMVS）** | ZY-3 三线阵三视卫星影像 + RPC + 5 m DSM 真值 | 多区域 | https://gpcv.whu.edu.cn/data/whu_tlc.html | Gao et al., ICCV 2021 |
| **WHU-Stereo** | GF-7 卫星立体像对 + LiDAR DSM | 1,757 对 | https://github.com/Sheng029/WHU-Stereo | Li et al., 2023 |
| **Urb3DCD / V2 / Cls** | 仿真城市点云 3D 变化检测 | 多难度子集 | https://ieee-dataport.org （检索 Urb3DCD）；代码 https://github.com/wangle53/3DCDNet-Urb3DCD | de Gélis et al., Remote Sensing 2021 |

### 8.6 遥感影像 2D 视觉定位 / 指代分割

与城市级 3D 定位任务同源的 2D 版本：给定自然语言描述，在遥感影像中定位目标框或分割掩码。

| 数据集 | 任务 | 规模 | 影像来源 | 下载 | 许可 / 引用 |
|---|---|---|---|---|---|
| **DIOR-RSVG** | 视觉定位（框） | 38,320 条描述，17,402 张影像 | DIOR | https://github.com/ZhanYang-nwpu/RSVG-pytorch | Zhan et al., IEEE TGRS 2023 |
| **OPT-RSVG** | 视觉定位（框） | 48,952 条描述 | 多源光学 | https://github.com/like413/OPT-RSVG | Li et al., 2024 |
| **VRSBench** | 描述 + VQA + 定位 | 29,614 张影像，52,472 条定位，123,221 条 QA | DOTA 等 | https://github.com/lx709/VRSBench ；https://huggingface.co/datasets/xiang709/VRSBench | 文本 CC BY 4.0；影像限学术；Li et al., NeurIPS 2024 D&B |
| **RRSIS-D** | 指代分割（掩码） | 17,402 组影像-描述-掩码 | DIOR | https://github.com/Lsan2401/RMSIN （Google Drive / 百度网盘） | Liu et al., CVPR 2024 |
| **RefSegRS** | 指代分割（掩码） | 4,420 组 | SkyScapes 航拍 | https://github.com/zhu-xlab/rrsis ；https://huggingface.co/datasets/JessicaYuan/RefSegRS | CC BY 4.0；Yuan et al., IEEE TGRS 2024 |

### 8.7 卫星 / 航拍视角 3D 场景生成（GS-Voxel 相关）

来源：GS-Voxel（arXiv 2608.17988，Qian 等，高德 / 浙大 / 北大）。该方法把已重建的航拍 3DGS 场景（200 m × 200 m 瓦片，可超过 300 万个高斯基元）无需逐场景优化地转为稀疏体素，用分解式 VAE 编码为结构化潜变量，再以卫星视角影像为条件用流模型生成，并通过重叠感知的分块推理扩展到大范围。论文未确认公开其训练用航拍 3DGS 数据。以下为同方向可用的公开数据集。

| 数据集 | 内容 | 规模 | 下载 | 许可 / 引用 |
|---|---|---|---|---|
| **Aerial-Earth3D**（EarthCrafter） | Google Earth 多视帧重建的航拍场景，每景含位姿标注的多视图影像、深度、法线、25 类语义分割；布局输入含 OSM 道路、DEM 与建筑高度 | 50,000 景，每景 600 m × 600 m，约 4,500 万帧，覆盖美国本土 | https://github.com/whiteinblue/EarthCrafter ；代码 https://github.com/alibaba-damo-academy/earthcrafter | 数据发布"视公司规定而定"，截至整理日未开放；Zhou et al., AAAI 2026 |
| **CityDreamer OSM + GoogleEarth** | OSM 城市布局（高度图 / 语义图）与 Google Earth 渲染的多视图影像，附建筑实例标注 | 实例标注生成约需 1 TB 磁盘 | https://github.com/hzxie/CityDreamer （gateway.infinitescript.com） | NTU S-Lab License 1.0；Xie et al., CVPR 2024 |
| **OmniCity** | 纽约市卫星影像 + 全景与单视街景，像素级标注，多层级多视角对齐 | 10 万+ 张标注影像，2.5 万个地理位置 | https://city-super.github.io/omnicity/ | Li et al., CVPR 2023 |
| **Sat2City 合成数据集** | 合成大规模 3D 城市与卫星视角高度图配对，用于单张卫星影像生成 3D 城市 | — | 见论文 arXiv 2507.04403 项目页 | Hua et al., ICCV 2025 |
| **CULTURE3D** | 文化地标与地形的摄影测量数据（RGB-D + 点云），面向 3DGS 大场景渲染评测 | 41,006 张影像 | 见论文 arXiv 2501.06927 项目页 | 2025 |
| **GauU-Scene / UrbanScene3D / MatrixCity / Mill-19** | 见 8.4 节，可作为航拍 3DGS 重建与生成的输入场景 | — | — | — |

相关方法（供对比）：Sat2Scene（CVPR 2024，卫星到 3D 城市扩散生成，在 OmniCity 上测试泛化）、Sat2Density / Sat2Density++、Sat3DGen（2026，在 VIGOR-OOD 上评估）。

---

## 9. 仿真协议与评价指标

**Wald 协议（降分辨率评估）**
1. 参考 HR-HSI → 高斯模糊（常用 σ 使 MTF 增益 ≈ 0.3 或 3×3 / 7×7 核）→ 下采样 r 倍（r = 4、8、16、32）得到 LR-HSI。
2. 参考 HR-HSI × 传感器 SRF 得到 HR-MSI。常用 SRF：Landsat-8 OLI、WorldView-3、Sentinel-2、Nikon D700（CAVE/Harvard）、IKONOS。
3. 融合结果与参考 HR-HSI 对比。

**全分辨率评估（无参考）**：QNR 系列（D_λ、D_s、QNR）、HQNR、R-Q2n；或使用真实配对（第 1.3 节）做视觉与一致性检验。

**常用指标**

| 指标 | 含义 | 理想值 |
|---|---|---|
| PSNR / SSIM | 逐波段空间保真 | 越大越好 |
| SAM | 光谱角（度） | 0 |
| ERGAS | 全局相对误差 | 0 |
| Q2n（Q4 / Q8） | 多波段 UIQI 扩展 | 1 |
| CC / UIQI | 相关系数 | 1 |
| RMSE | 均方根误差 | 0 |
| D_λ / D_s / QNR | 全分辨率光谱 / 空间失真 | 0 / 0 / 1 |

---

## 10. 建议的数据目录结构

```
data/
├── hsi_msi/            # 1.1 / 1.2 仿真基准
│   ├── CAVE/
│   ├── Harvard/
│   ├── PaviaU/
│   ├── Chikusei/
│   └── ...
├── real_pairs/         # 1.3 真实配对
│   ├── WHU-MHF/
│   ├── ZY1-02D/
│   └── PRISMA/
├── pansharpening/      # 2
│   ├── PanCollection/{wv3,qb,gf2,wv2}/{train,valid,test}
│   └── PAirMax/
├── multimodal/         # 3
├── spatiotemporal/     # 4
├── sar_optical/        # 5
├── downstream/         # 6 / 7
└── city3d/             # 8
```

获取方式说明：
- **直链**（ehu.eus、CAVE、Harvard 等）：`python tools/download_datasets.py --out data/ --name pavia_u cave harvard`
- **需注册**（PRISMA、EnMAP、CRESDA、USGS、Houston）：按表中链接注册申请后手动放入对应目录。
- **网盘 / 云盘**（PanCollection、ZY1-02D、WHU-Hi）：从官方页面的 Google Drive / 百度网盘链接下载。

---

## 11. 数据体积统计

以下体积来自官方页面、Hugging Face / Zenodo / IEEE DataPort / mediaTUM 文件列表或镜像站标注；标"估算"者由像元数 / 点数 / 影像数与典型字节数推算，置信度较低。按景分发的卫星门户（PRISMA、EnMAP、Hyperion、GF-5、AVIRIS）只给出每景体积，不计入合计。合计数由 `python tools/dataset_stats.py --markdown` 从 `datasets/catalog.yaml` 生成。

### 11.1 按类别汇总

| 类别 | 条目数 | 合计体积 | 其中估算值 |
|---|---|---|---|
| 高光谱-多光谱融合 | 14 | 113.9 GB | 100.8 GB |
| 真实卫星配对 / 数据源 | 8 | 8.8 GB | 8.8 GB |
| 全色锐化 | 3 | 20.6 GB | 31 MB |
| HSI+LiDAR/SAR 多模态 | 6 | 3.7 GB | 3.2 GB |
| 时空融合 | 5 | 19.8 GB | 14.2 GB |
| SAR-光学 | 6 | 889.0 GB | 14.5 GB |
| 下游任务 / 2D 视觉定位 | 11 | 45.2 GB | 18.7 GB |
| 通用遥感基准 | 11 | 273.2 GB | 187.5 GB |
| 城市级 3D 场景 | 37 | 23.9 TB | 3.4 TB |
| WorldView 专题 | 9 | 1.1 TB | 1.0 TB |
| **合计** | 110 | **26.3 TB** | 4.8 TB |

按获取方式：需注册 / 申请约 20.2 TB，网盘 / 云盘约 4.8 TB，直链约 161 GB，GitHub 托管约 94 GB。

几点说明：
- **城市级 3D 场景占 95%**，主要来自 UrbanScene3D（约 18 TB，含 12.8 万张原始影像，子场景可单独下载）、OpenFly（约 2.4 TB）和 MatrixCity（全量约 2 TB，仅点云 29 GB）。若只做城市级 3D 定位，SensatUrban + CityRefer + STPLS3D 合计约 50 GB 即可。
- **SAR-光学类**体积集中在 SEN12MS（452 GB）、SEN12MS-CR（272 GB）和 So2Sat（107 GB）。
- **高光谱融合主线**（第 1 节与第 2 节）合计约 150 GB，其中 ICVL 全集约 75 GB，ARAD_1K 约 25 GB，PanCollection 约 20 GB；ehu.eus 经典场景全部不到 400 MB。
- 未发布或未统计：CitySTAR-3D、Aerial-Earth3D（估计 15–25 TB）、Sat2City 合成数据集、OpenCity3D 基准、GS-Voxel 训练数据。

### 11.2 逐条明细

| id | 名称 | 体积 | 依据 |
|---|---|---|---|
| cave | CAVE Multispectral Image Database | 819 MB（估算） | 官方 complete_ms_data.zip 未标体积，估算 0.5–1 GB；IEEE DataPort 镜像 2.51 GB |
| harvard | Harvard Real-World Hyperspectral Images Database | 7.5 GB | CZ_hsdb.tgz 5.3 GB + CZ_hsdbi.tgz 2.2 GB（官方下载页） |
| icvl | ICVL Hyperspectral Database | 75.0 GB（估算） | 31 波段 .mat 估算 60–90 GB；含原始 ENVI 全集约 335 GB（HF ICVL-BGU/ICVL_HS_2016） |
| arad_1k | ARAD_1K (NTIRE 2022 Spectral Recovery) | 25.0 GB（估算） | 估算：950 张 482×512×31 float32 ≈29 GB，压缩后约 20–25 GB |
| pavia_u | Pavia University | 34 MB | PaviaU.mat 33.2 MB（ehu.eus） |
| pavia_c | Pavia Centre | 127 MB | Pavia.mat 123.6 MB（ehu.eus） |
| indian_pines | Indian Pines | 6 MB | Indian_pines_corrected.mat 5.7 MB（ehu.eus） |
| salinas | Salinas | 26 MB | Salinas_corrected.mat 25.3 MB（ehu.eus） |
| ksc | Kennedy Space Center | 58 MB | KSC.mat 56.8 MB（ehu.eus） |
| botswana | Botswana | 81 MB | Botswana.mat 78.9 MB（ehu.eus） |
| wdc_mall | Washington DC Mall | 148 MB | dc.tif 145 MB（Purdue MultiSpec 页面） |
| chikusei | Chikusei | 2.4 GB | ENVI zip ≈1.0 GB + MATLAB zip ≈1.4 GB（SAL-UTokyo；hyper.ai 镜像列 1.0 + 2.33 GB） |
| whu_hi | WHU-Hi (LongKou / HanChuan / HongHu) | 1.0 GB | 三景 .mat 合计约 0.9–1.1 GB（Kaggle 886 MB / HF 镜像 1.14 GB） |
| xiongan | Xiong'an (马蹄湾村) 航空高光谱 | 1.8 GB | geodoi 6 个文件压缩 1.75 GB，解压 2.83 GB |
| whu_mhf | WHU-MHF | 5.0 GB（估算） | 估算：7 景 HSI(148 波段)+MSI(8 波段) uint16 未压缩 |
| zy1_02d_cssnet | ZY1-02D Real HSI/MSI/PAN (CSSNet) | 2.0 GB（估算） | 估算：HSI 76 波段+MSI 8 波段+PAN 2.5 m，1–3 GB |
| prisma_hp | PRISMA Hyperspectral Pansharpening (WHISPERS 2022 / toolbox) | 205 MB（估算） | 每景 L2D ≈1 GB（prismaread 文档）；WHISPERS 2022 挑战集 ≈0.2 GB 估算 |
| c2seg_ab | C2Seg-AB / Berlin–Augsburg EnMAP-S2-S1 | 1.6 GB（估算） | 估算：Berlin+Augsburg 242 波段 int16 未压缩；mediaTUM 页未列体积 |
| enmap | EnMAP | 每景 1.2 GB | 每景 L2A ≈1–1.5 GB（EnMAP 产品规范：光谱影像上限 639 MB + 质量层） |
| hyperion_ali | EO-1 Hyperion + ALI | 每景 512 MB | 每景 Hyperion L1 ≈0.3–0.5 GB，ALI ≈0.1–0.2 GB |
| gf5_ahsi | GF-5 / GF-5B AHSI | 每景 2.6 GB | 每景估算：2000×2000×330×2B |
| aviris | AVIRIS / AVIRIS-NG Data Portal | 每景 1.5 GB | 每条航线 AVIRIS-NG ≈1.1 GB zip / 2 GB 解压；Classic ≈1.5–3 GB；Classic L2 全集 25.7 TB |
| pancollection | PanCollection (WV3 / QB / GF2 / WV2) | 20.0 GB | HF 镜像：训练 GF2 6 GB + QB 5.19 GB + WV3 5.57 GB + WV2 168 MB，验证 ≈1.9 GB，测试 ≈1–2 GB |
| pairmax | PAirMax | 553 MB | Maxar 9 对 386 MB + Airbus 5 对 153.9 MB（Zenodo 7706102） |
| dlpan_toolbox | DLPan-Toolbox | 31 MB（估算） | 纯代码仓库，无数据 |
| houston2013 | Houston 2013 (IEEE GRSS DFC 2013) | 205 MB（估算） | 估算：349×1905×144 uint16 ≈191 MB + DSM；官网需申请 |
| houston2018 | Houston 2018 (IEEE GRSS DFC 2018) | 3.0 GB（估算） | 未公布总量；栅格部分 ≈0.7 GB（含 5 cm RGB 410 MB），含多光谱 LiDAR 点云估计数 GB |
| trento | Trento HSI + LiDAR | 12 MB | Italy_hsi.mat 11.5 MB + LiDAR 0.4 MB（GitHub） |
| muufl | MUUFL Gulfport | 95 MB | 四个 .mat 合计约 93 MB（GitHub） |
| berlin_augsburg_s2fl | Berlin / Augsburg HSI + SAR (S2FL) | 389 MB | Berlin + Augsburg 合集 378.72 MB（figshare 28112405） |
| rs_fusion_datasets | rs-fusion-datasets（统一加载器） | 0 MB | 加载器，按需拉取上述数据集 |
| cia | CIA (Coleambally Irrigation Area) | 1.4 GB（估算） | 估算：17 对 Landsat+MODIS 6 波段 uint16 未压缩 |
| lgc | LGC (Lower Gwydir Catchment) | 2.9 GB（估算） | 估算：14 对，3200×2720 |
| ahb_tianjin_daxing | AHB / Tianjin / Daxing | 8.9 GB（估算） | 估算：AHB 4.5 + Tianjin 2.7 + Daxing 1.7 GB 未压缩（各 27 对） |
| wuhan_stf | Wuhan Dataset (GF / Landsat) | 1.0 GB（估算） | 估算：8 对 GF/Landsat，仓库内 train/test 目录 |
| s2_s3_stf | Sentinel-2 / Sentinel-3 OLCI STF benchmark | 5.6 GB | Zenodo 14860220 各站点 zip 合计 5.6 GB |
| sen12ms | SEN12MS | 452.0 GB | 论文 421.3 GiB；mediaTUM 列 510 GB |
| sen1_2 | SEN1-2 | 43.7 GB | mediaTUM 1436631：43.7 GB，564,770 文件 |
| sen12ms_cr | SEN12MS-CR / CR-TS（云去除） | 272.0 GB | SEN12MS-CR 272 GB（mediaTUM 1554803）；CR-TS 另约 663 GB 下载 / 2 TB 解压 |
| qxs_saropt | QXS-SAROPT | 2.5 GB（估算） | 估算：20,000 对 256×256 PNG ≈2–3 GB（未压缩 5.2 GB） |
| whu_opt_sar | WHU-OPT-SAR | 12.0 GB（估算） | 估算：100×5556×3704×6 通道 8 位未压缩 |
| so2sat_lcz42 | So2Sat LCZ42 | 106.8 GB | h5：train 51.76 + val 55.07 + test 3.32 GB；mediaTUM v3 列 165 GB |
| unmixing_rslab | Samson / Jasper Ridge / Urban（解混） | 24 MB | Samson 3.4 MB + Jasper Ridge 2.8 MB + Urban 16.9 MB |
| abu | ABU (Airport-Beach-Urban) 异常检测 | 44 MB（估算） | 13 个 .mat 各 1.5–8.2 MB，合计约 40–45 MB |
| had100 | HAD100 异常检测 | 1.7 GB（估算） | 估算：AVIRIS-NG 训练集 ≈1.45 GB + 100 幅测试图 0.2–0.5 GB |
| hsi_cd_citius | Hermiston / Bay Area / Santa Barbara（高光谱变化检测） | 1.0 GB（估算） | Bay Area ≈196 MB + Hermiston ≈134 MB（DataPort 镜像）+ Santa Barbara 估算 ≈650 MB |
| levir_cd | LEVIR-CD | 2.5 GB | zip 2.46 GB（Kaggle 镜像与官方 Google Drive 同源） |
| whu_cd | WHU Building Change Detection | 3.4 GB | 官方页标注 3.4 GB；IEEE DataPort 裁剪版 1.78 GB |
| dior_rsvg | DIOR-RSVG | 6.0 GB（估算） | 估算：17,402 张 800×800 JPEG，与 RRSIS-D 同源 |
| opt_rsvg | OPT-RSVG | 10.0 GB（估算） | 估算：25,452 张影像，尺寸 152² 至 8935×10569 |
| vrsbench | VRSBench | 11.5 GB | VRSBench.zip 11.52 GB（hyper.ai 镜像） |
| rrsis_d | RRSIS-D | 6.1 GB | rrsis.zip 6.07 GB（hyper.ai 镜像） |
| refsegrs | RefSegRS | 3.0 GB | Hugging Face 下载量 2.97 GB（parquet 1.01 GB） |
| uc_merced | UC Merced Land Use | 328 MB | 317 MiB（TensorFlow Datasets 目录） |
| aid | AID | 2.6 GB（估算） | 估算：10,000 张 600×600 JPEG，AID.zip 常见约 2.6 GB |
| nwpu_resisc45 | NWPU-RESISC45 | 410 MB（估算） | 估算：31,500 张 256×256 JPEG，.rar 约 405 MB |
| eurosat | EuroSAT (RGB / MS) | 2.2 GB | Zenodo 7711810：RGB 94.7 MB + MS 2.1 GB |
| bigearthnet | BigEarthNet (v1 S2/S1, v2 reBEN) | 120.0 GB（估算） | v1 S2 65.2 GB（tar.gz，已知）+ S1 ≈55 GB（估算）；v2 reBEN ≈120 GB（估算） |
| isprs_potsdam_vaihingen | ISPRS Potsdam / Vaihingen 2D | 29.3 GB | ISPRS 页面：Potsdam 13.3 GB + Vaihingen 16.0 GB |
| loveda | LoveDA | 18.5 GB | Zenodo 5706578：Train 6.66 + Val 8.92 + Test 2.91 GB |
| gid | GID (Gaofen Image Dataset) | 50.0 GB（估算） | 估算：large-scale 150 幅 GF-2 ≈16 GB + fine 30,000 块 ≈35 GB |
| dota | DOTA v1.0 / v2.0 | 35.4 GB | v1.0 含 test 共 35.38 GB（hyper.ai）；train+val 约 18 GB |
| dior | DIOR | 7.5 GB（估算） | 估算：23,463 张 800×800 JPEG，DIOR.zip 常见约 7.3 GB |
| s2looking | S2Looking | 7.0 GB（估算） | 估算：5,000 对 1024×1024 双时相 PNG + 标签 |
| sensaturban | SensatUrban | 30.0 GB（估算） | 估算：28.5 亿点 PLY ≈45 GB 解压，zip 约 25–35 GB；官方 data_release.zip 未标体积 |
| cityrefer | CityRefer | 512 MB（估算） | 估算：仅标注 JSON / box3d，<1 GB；点云另取 SensatUrban |
| stpls3d | STPLS3D | 18.0 GB（估算） | 估算：点云 15–20 GB；含源影像约 50–100 GB |
| stpls3d_refer | STPLS3D-Refer | 307 MB（估算） | 估算：仅文本 / 框标注，<0.5 GB；需 STPLS3D 点云 |
| urbex_data | Urbex-Data | 20.0 GB（估算） | 估算：BEV 图 + 斜视缓存 10–30 GB；HF 卡片本环境不可达 |
| urbanbis | UrbanBIS | 50.0 GB（估算） | 估算：点云 ASCII 100–150 GB 解压 / 压缩 40–60 GB；113k 张影像另 >1.5 TB |
| whu_urban3d | WHU-Urban3D | 15.0 GB（估算） | 估算：标注点云 + ALS/MLS 原始点云 + 全景影像 10–20 GB |
| dales | DALES | 6.0 GB（估算） | 估算：5.05 亿点 LAS 约 12–15 GB 解压，tar.gz 5–7 GB；提供 LAS/PLY/BIN |
| h3d | Hessigheim 3D (H3D) | 17.0 GB（估算） | 估算：3 期点云 ≈11 GB + 纹理网格，15–20 GB |
| sum_meshes | SUM (Semantic Urban Meshes) | 30.0 GB（估算） | 估算：300 pts/m² 点云 ≈24 GB + 30 pts/m² 2.4 GB + 64 块纹理网格 |
| campus3d | Campus3D | 17.0 GB（估算） | 估算：9.37 亿点 PLY 15–19 GB；reduced 版 2–4 GB |
| toronto3d | Toronto-3D | 1.1 GB | Toronto_3D.zip 1.07 GB（hyper.ai 镜像） |
| paris_lille_3d | Paris-Lille-3D | 4.0 GB（估算） | 估算：1.43 亿训练点 + 测试 PLY 3–5 GB |
| semantic3d | Semantic3D | 20.0 GB（估算） | 估算：40 亿点 ASCII ≈140 GB 解压，7z 压缩 15–25 GB |
| citynav | CityNav | 12.0 GB（估算） | 估算：data.tar.gz（RGB/深度/GSAM）5–20 GB；另需 SensatUrban 点云 |
| aerialvln | AerialVLN | 35.0 GB | README：模拟器约 35 GB，标注数据 <100 MB |
| openfly | OpenFly | 2.4 TB | 维护者在 issue #11 称数据集共约 2.4 TB；DataGen 环境另约 50–150 GB（估算） |
| embodiedcity | EmbodiedCity | 20.0 GB（估算） | 估算：UE 打包北京商务区场景 10–30 GB；VLN 文本 <100 MB |
| cityeqa | CityEQA-EC | 10 MB | 仓库 Data/ 仅 JSON；需 EmbodiedCity 模拟器 |
| urbanvideo_bench | UrbanVideo-Bench | 40.0 GB（估算） | 估算：1,547 段 720p 视频 20–60 GB |
| urbanscene3d | UrbanScene3D | 18.0 TB | 论文补充材料：影像 16,860 GB + 重建模型 656 GB + 纹理 507 GB，子场景可单独下载 |
| matrixcity | MatrixCity | 2.0 TB（估算） | 点云 27.8 + 1.64 GB 已知；全量 RGB + 深度估算 1.5–2.5 TB，仅 RGB ≈0.8 TB |
| mill19 | Mill-19 (Mega-NeRF) | 20.0 GB（估算） | 估算：building 1,940 张 + rubble 1,678 张 4608×3456 JPEG |
| us3d | DFC2019 / US3D (Urban Semantic 3D) | 200.0 GB（估算） | 估算：DFC2019 Track 1–4 + Atlanta 扩展 100–300 GB；DataPort 需订阅查看 |
| whu_tlc | WHU-TLC (SatMVS) | 20.0 GB（估算） | 估算：三线阵 5120×5120 + RPC + DSM + 裁块 10–30 GB |
| whu_stereo | WHU-Stereo | 8.0 GB（估算） | 估算：1,757 对 1024×1024 uint16 PNG + 视差，约 5 MB/对 |
| urb3dcd | Urb3DCD / V2 / Cls | 1.8 GB | DataPort：V1 1.02 GB + V2 0.45 GB + Cls 0.31 GB |
| aerial_earth3d | Aerial-Earth3D (EarthCrafter) | — | 未发布；按 4,500 万帧估算 15–25 TB |
| citydreamer_osm_ges | CityDreamer OSM + GoogleEarth | 4.3 GB | OSM + GoogleEarth 合包 4.31 GB（hyper.ai 镜像） |
| omnicity | OmniCity | 75.0 GB（估算） | 估算：2.5 万地点 × 卫星切片 + 全景 + 单视图，50–100 GB |
| sat2city_synth | Sat2City synthesized city dataset | — | 未发布（thua919/Sat2City-release 标 Coming soon） |
| culture3d | CULTURE3D | 800.0 GB（估算） | 估算：41,006 张 48 MP JPEG ≈600 GB + COLMAP + 纹理网格，0.6–1 TB |
| gs_voxel | GS-Voxel（方法，训练数据未公开） | — | 训练数据未公开 |
| citystar_3d | CitySTAR-3D | — | 未发布；标注文本本身预计 <50 MB，点云取自 SensatUrban / STPLS3D |
| city3dqa | 3DCity-LLM-1.2M / City-3DQA | 1.0 GB（估算） | 估算：120 万条 QA 文本约 1 GB；点云另取自 SensatUrban / UrbanBIS |
| geoeval3d | GeoEval3D (GeoProg3D) | 10 MB（估算） | 952 组问答文本，<10 MB；3D 高斯场景需自行重建 |
| opencity3d | OpenCity3D benchmark | — | 基准数据未单独发布；依赖航拍网格渲染 |
| maxar_product_samples | Maxar 产品样例影像（WV-2 / WV-3 / WV Legion / GeoEye-1） | 每景 1.0 GB | 每景样例约 0.3–3 GB（PAN + 8 波段 MS，GeoTIFF/NITF）；PAirMax 与 Adelaide/Mexico City 全分辨率测试图均源于此 |
| maxar_open_data | Maxar Open Data Program（灾害事件 ARD 影像） | 500.0 GB（估算） | 估算：STAC 目录覆盖数十个事件，单事件数 GB 至数十 GB（如 Maui 火灾 2023 约 3.5 GB）；总量随事件持续增长 |
| esa_tpm_worldview | ESA Third Party Missions WorldView 档案 | 每景 1.5 GB | 每景约 0.5–3 GB；档案覆盖 2009–2020 年 ESA 资助项目的申请区域 |
| spacenet | SpaceNet 1–8 | 400.0 GB（估算） | 估算：SN1 Rio ≈3 GB，SN2 四城 ≈30 GB，SN3 道路 ≈50 GB，SN4 Atlanta 离轴 ≈180 GB，SN5 ≈60 GB，SN6 ≈40 GB，SN7 ≈23 GB，SN8 ≈20 GB |
| xview | xView（目标检测） | 20.7 GB | 挑战赛站点下载约 20.7 GB（Ultralytics 文档） |
| xbd | xBD / xView2（建筑损毁评估） | 30.3 GB | 挑战赛数据约 10 GB 压缩（baseline README）；含 tier3 全集约 30.3 GB（hyper.ai 镜像） |
| mvs3dm | IARPA MVS3DM（多视立体，阿根廷） | 40.0 GB（估算） | 估算：50 景 WV3 PAN + 8 波段 NITF，约 20–60 GB；含机载雷达真值 DSM |
| core3d | IARPA CORE3D 开放数据（Jacksonville / Omaha / UCSD） | 100.0 GB（估算） | 估算：三个站点的 WV3 多视影像；US3D / DFC2019 由此派生 |
| wv3_fr_test_tiles | WV2 / WV3 全分辨率测试图（Washington、Stockholm、Adelaide、Mexico City） | 1.0 GB（估算） | 估算：各 20 块 512×512 全分辨率与 2048×2048 降分辨率瓦片（Vivone 等 2021 全分辨率评估协议） |

---

## 12. WorldView 数据专题

WorldView 系列（DigitalGlobe，现 Maxar）是全色锐化、亚米级目标检测与卫星多视立体最常用的商业影像来源。本节汇总传感器参数、可免费获取的渠道，以及以 WorldView 影像为底的公开数据集（目录其他章节中的 PanCollection WV3/WV2、PAirMax、US3D 也属此类）。

### 12.1 传感器参数

| 卫星 | 发射 | 全色 GSD（星下点） | 多光谱 | SWIR / 其他 | 幅宽 | 备注 |
|---|---|---|---|---|---|---|
| **WorldView-1** | 2007 | 0.50 m | 无 | — | 17.7 km | 仅全色 |
| **WorldView-2** | 2009 | 0.46 m | 8 波段 1.84 m（Coastal、B、G、Y、R、Red Edge、NIR1、NIR2） | — | 16.4 km | PanCollection WV2、PAirMax、SpaceNet 1 |
| **WorldView-3** | 2014 | 0.31 m | 8 波段 1.24 m | SWIR 8 波段 3.7 m（1195–2365 nm）；CAVIS 12 波段 30 m | 13.1 km | PanCollection WV3、xView、SpaceNet 2–7、US3D、MVS3DM；16 波段 VNIR+SWIR 融合研究 |
| **WorldView-4** | 2016（2019 年失效） | 0.31 m | 4 波段 1.24 m | — | 13.1 km | 存档影像可经 ESA TPM 申请 |
| **WorldView Legion** | 2024 起 | 0.29 m | 8 波段 1.16 m | — | 9 km | 6 星星座，Maxar 样例可申请 |
| GeoEye-1 / QuickBird | 2008 / 2001 | 0.41 m / 0.61 m | 4 波段 1.65 m / 2.44 m | — | 15.2 / 16.8 km | PanCollection QB、PAirMax GE1 同为 Maxar 系列 |

商业标准产品每景（约 25 km² 以上条带）约 1–3 GB（PAN + 8 波段 MS，GeoTIFF / NITF，11 bit）。

### 12.2 获取渠道

| 渠道 | 内容 | 条件 / 许可 | 链接 |
|---|---|---|---|
| **Maxar 产品样例** | WV-2 / WV-3 / Legion / GeoEye-1 各城市样例景（PAN + MS，部分含 SWIR） | 填表申请，Maxar Evaluation License，禁止再分发 | https://resources.maxar.com/product-samples |
| **Maxar Open Data Program** | 灾害事件前后 ARD 影像（COG 瓦片 + STAC 目录），数十个事件 | 免费，CC BY-NC 4.0，OSM 例外 | https://registry.opendata.aws/maxar-open-data/ ；工具 https://github.com/opengeos/maxar-open-data |
| **ESA Third Party Missions** | WV-1/2/3/4 档案（2009–2020，ESA 资助项目申请过的区域），PAN、4/8 波段、SWIR | EO Sign In 注册后提交申请，约 2 天审批；面向 ESA / EU 成员国及 Dragon 计划（含中国）科研用户，有配额 | https://earth.esa.int/eogateway/catalog/worldview-esa-archive |
| **NASA CSDA** | Maxar 档案与新采集影像 | 仅限 NASA 资助的美国研究人员 | https://www.earthdata.nasa.gov/esds/csda |
| **USGS 商业影像（NextView / EOCL）** | WV 存档 | 仅限美国联邦政府及其承包方 | https://earthexplorer.usgs.gov |
| **SpaceNet on AWS** | SpaceNet、CORE3D、MVS3DM 等已脱敏 WV2/WV3 影像 | 免费，CC BY-SA 4.0 | https://registry.opendata.aws/spacenet/ |
| **国内代理** | 按景购买 WV-2/3 新采或存档 | 商业，约数百元/km² 量级 | 北京揽宇方圆、航天星图等 |

另：以 Google Earth 为来源的数据集（LEVIR-CD、QXS-SAROPT 光学部分、DOTA 部分、CityDreamer GoogleEarth）在亚米级区域多为 Maxar WorldView 影像的再分发，可作为"间接 WorldView"数据，但无原始波段与辐射定标。

### 12.3 以 WorldView 影像为底的公开数据集

| 数据集 | 任务 | 卫星 | 规模 | 体积 | 下载 | 许可 |
|---|---|---|---|---|---|---|
| **PanCollection WV3 / WV2** | 全色锐化 | WV-3 8 波段（0.31 / 1.24 m）、WV-2 | WV3 训练约 1 万块 + 20/20 测试景；WV2 用于泛化 | WV3 ≈5.6 GB，WV2 ≈0.2 GB | 见第 2 节 | GPL-2.0 |
| **PAirMax** | 全色锐化基准 | WV-2、WV-3、GeoEye-1（Maxar 9 对） | 14 对 FR + RR | 0.54 GB | 见第 2 节 | Maxar / Airbus 评估许可 |
| **WV2 / WV3 全分辨率测试图** | 全分辨率 QA 协议 | WV-2（Washington、Stockholm）、WV-3（Adelaide、Mexico City） | 各 20 块 512×512 FR + 2048×2048 RR | ≈1 GB（估算） | https://github.com/liangjiandeng/DLPan-Toolbox | 源于 Maxar 样例 |
| **WV3 VNIR+SWIR 16 波段融合** | 多波段锐化 | WV-3 8 VNIR + 8 SWIR | 仿真 + 真实 WV3 | — | Vivone et al., Information Fusion 2020（数据随 Maxar 样例） | 评估许可 |
| **SpaceNet 1–8** | 建筑 / 道路提取、多时相、SAR-光学 | WV-2（Rio），WV-3（Las Vegas、Paris、Shanghai、Khartoum、Atlanta、Moscow、Mumbai 等），Capella SAR | 81 万建筑、2 万 km 道路，约 2.7 万 km² | ≈400 GB（估算） | https://spacenet.ai/datasets/ | CC BY-SA 4.0 |
| **xView** | 目标检测 | WV-3 0.3 m | 100 万目标，60 类，1,400 km² | 20.7 GB | https://challenge.xviewdataset.org | CC BY-NC-SA 4.0 |
| **xBD / xView2** | 建筑损毁评估（双时相） | Maxar WV-2/3 等 | 85 万建筑标注，45,362 km²，19 个灾害事件 | 10 GB（挑战赛）/ 30.3 GB（含 tier3） | https://xview2.org | CC BY-NC-SA 4.0 |
| **DFC2019 / US3D** | 卫星多视立体 + 语义 | WV-3 PAN + 8 波段，Jacksonville / Omaha / Atlanta | 约 100 km²，数千瓦片 | ≈200 GB（估算） | 见 8.5 节 | IEEE DataPort |
| **IARPA CORE3D** | 城市 3D 重建 | WV-3 多视 + 机载 LiDAR，Jacksonville / Omaha / UCSD | — | ≈100 GB（估算） | https://github.com/pubgeo/core3d-open | 公开 |
| **IARPA MVS3DM** | 多视立体 | WV-3 50 景，阿根廷 San Fernando，2015–2016 | 100 km²，8 个可重建站点，机载雷达 DSM 真值 | ≈40 GB（估算） | https://spacenet.ai/iarpa-multi-view-stereo-3d-mapping/ | 公开 |
| **Maxar Open Data** | 灾害变化检测、建筑提取 | WV-1/2/3、GeoEye-1 ARD | 数十个事件（如 2023 土耳其地震、Maui 火灾） | 单事件数 GB 至数十 GB | https://registry.opendata.aws/maxar-open-data/ | CC BY-NC 4.0 |

与 HyperFusion 的关系：WV-3 的 8 波段 VNIR 加 8 波段 SWIR 是目前唯一商业化的"多光谱 + 短波红外 + 亚米级全色"组合，可作为高光谱锐化的低维近似基准；PanCollection WV3 与 PAirMax 已是本项目全色锐化的默认训练与评估数据。

