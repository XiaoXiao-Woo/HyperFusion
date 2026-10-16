# HyperFusion

高光谱 / 多光谱 / 全色遥感图像融合。

## 数据集

- [`docs/datasets.md`](docs/datasets.md)：遥感融合数据集目录（HSI-MSI 融合、全色锐化、多模态、时空融合、SAR-光学、下游任务及城市级 3D 场景），含传感器参数、下载链接与许可说明。
- [`datasets/catalog.yaml`](datasets/catalog.yaml)：同一清单的机器可读版本。
- [`tools/download_datasets.py`](tools/download_datasets.py)：按清单下载可直链获取的数据集。

```bash
pip install pyyaml
python tools/download_datasets.py --list
python tools/download_datasets.py --out data --name pavia_u cave harvard
```
