#!/usr/bin/env python3
"""统计 datasets/catalog.yaml 中各数据集的体积。

用法：
    python tools/dataset_stats.py              # 按类别 / 获取方式汇总
    python tools/dataset_stats.py --detail     # 同时逐条列出
    python tools/dataset_stats.py --markdown   # 输出 Markdown 表格（用于文档）

清单字段：
    size_gb       : 下载体积（GB）。按景分发的数据源（access=registration 的卫星门户）填 size_per_scene_gb。
    size_note     : 体积依据或估算说明。
    size_estimated: true 表示估算值。
依赖：PyYAML。
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("缺少 PyYAML，请先执行: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "datasets" / "catalog.yaml"

CATEGORY_NAMES = {
    "hsi_msi": "高光谱-多光谱融合",
    "real_pairs": "真实卫星配对 / 数据源",
    "pansharpening": "全色锐化",
    "multimodal": "HSI+LiDAR/SAR 多模态",
    "spatiotemporal": "时空融合",
    "sar_optical": "SAR-光学",
    "downstream": "下游任务 / 2D 视觉定位",
    "general": "通用遥感基准",
    "city3d": "城市级 3D 场景",
}


def fmt(gb: float | None) -> str:
    if gb is None:
        return "—"
    if gb >= 1000:
        return f"{gb / 1000:.1f} TB"
    if gb >= 1:
        return f"{gb:.1f} GB"
    return f"{gb * 1024:.0f} MB"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--detail", action="store_true", help="逐条列出")
    p.add_argument("--markdown", action="store_true", help="输出 Markdown 表格")
    args = p.parse_args()

    entries = yaml.safe_load(CATALOG.open(encoding="utf-8"))["datasets"]

    by_cat: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_cat[e["category"]].append(e)

    rows = []
    total = 0.0
    total_est = 0.0
    n_sized = n_scene = n_unknown = 0
    for cat in CATEGORY_NAMES:
        if cat not in by_cat:
            continue
        subtotal = 0.0
        sub_est = 0.0
        for e in by_cat[cat]:
            gb = e.get("size_gb")
            if gb is not None:
                subtotal += gb
                n_sized += 1
                if e.get("size_estimated"):
                    sub_est += gb
            elif e.get("size_per_scene_gb") is not None:
                n_scene += 1
            else:
                n_unknown += 1
        total += subtotal
        total_est += sub_est
        rows.append((cat, len(by_cat[cat]), subtotal, sub_est))

    if args.markdown:
        print("| 类别 | 条目数 | 合计体积 | 其中估算值 |")
        print("|---|---|---|---|")
        for cat, n, sub, est in rows:
            print(f"| {CATEGORY_NAMES[cat]} | {n} | {fmt(sub)} | {fmt(est)} |")
        print(f"| **合计** | {len(entries)} | **{fmt(total)}** | {fmt(total_est)} |")
    else:
        print(f"{'类别':<24}{'条目':>5}{'合计体积':>12}{'其中估算':>12}")
        for cat, n, sub, est in rows:
            print(f"{CATEGORY_NAMES[cat]:<24}{n:>5}{fmt(sub):>12}{fmt(est):>12}")
        print(f"{'合计':<24}{len(entries):>5}{fmt(total):>12}{fmt(total_est):>12}")
        print(f"\n有体积数据 {n_sized} 条，按景分发 {n_scene} 条，未知 {n_unknown} 条。")

    by_access: dict[str, float] = defaultdict(float)
    for e in entries:
        if e.get("size_gb") is not None:
            by_access[e.get("access", "?")] += e["size_gb"]
    print("\n按获取方式：")
    for k, v in sorted(by_access.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<14}{fmt(v)}")

    if args.detail or args.markdown:
        print()
        if args.markdown:
            print("| id | 名称 | 体积 | 依据 |")
            print("|---|---|---|---|")
        for cat in CATEGORY_NAMES:
            for e in by_cat.get(cat, []):
                if e.get("size_gb") is not None:
                    size = fmt(e["size_gb"]) + ("（估算）" if e.get("size_estimated") else "")
                elif e.get("size_per_scene_gb") is not None:
                    size = f"每景 {fmt(e['size_per_scene_gb'])}"
                else:
                    size = "—"
                note = e.get("size_note", "")
                if args.markdown:
                    print(f"| {e['id']} | {e['name']} | {size} | {note} |")
                else:
                    print(f"  {e['id']:<22}{size:<18}{note}")


if __name__ == "__main__":
    main()
