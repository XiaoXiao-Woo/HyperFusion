#!/usr/bin/env python3
"""按 datasets/catalog.yaml 下载可直链获取的遥感数据集。

用法：
    python tools/download_datasets.py --list                      # 列出所有条目及获取方式
    python tools/download_datasets.py --out data --name pavia_u   # 下载指定条目
    python tools/download_datasets.py --out data --all            # 下载全部 access=direct 条目

仅 access 为 direct 的条目可自动下载；其余条目会打印官方页面供手动获取。
依赖：PyYAML（pip install pyyaml）。
"""
from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("缺少 PyYAML，请先执行: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "datasets" / "catalog.yaml"


def load_catalog() -> list[dict]:
    with CATALOG.open(encoding="utf-8") as f:
        return yaml.safe_load(f)["datasets"]


def list_entries(entries: list[dict]) -> None:
    width = max(len(e["id"]) for e in entries)
    for e in entries:
        print(f"{e['id']:<{width}}  [{e.get('access', '?'):<12}] {e['name']}")
        print(f"{'':<{width}}  {e.get('homepage', e.get('doi', ''))}")


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  已存在，跳过: {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    print(f"  下载 {url}\n    -> {dest}")

    def hook(blocks: int, block_size: int, total: int) -> None:
        done = blocks * block_size
        if total > 0:
            pct = min(100.0, done * 100.0 / total)
            print(f"\r    {done / 2**20:8.1f} MB / {total / 2**20:8.1f} MB ({pct:5.1f}%)", end="")
        else:
            print(f"\r    {done / 2**20:8.1f} MB", end="")

    urllib.request.urlretrieve(url, tmp, reporthook=hook)
    print()
    tmp.rename(dest)


def fetch(entry: dict, out: Path) -> None:
    print(f"[{entry['id']}] {entry['name']}")
    if entry.get("access") != "direct" or not entry.get("files"):
        print(f"  该数据集需手动获取（{entry.get('access')}）: {entry.get('homepage', entry.get('doi'))}")
        return
    for f in entry["files"]:
        download(f["url"], out / f["path"])


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="列出清单")
    p.add_argument("--all", action="store_true", help="下载全部可直链条目")
    p.add_argument("--name", nargs="*", default=[], help="按 id 下载")
    p.add_argument("--out", type=Path, default=ROOT / "data", help="输出目录（默认 ./data）")
    args = p.parse_args()

    entries = load_catalog()
    if args.list or not (args.all or args.name):
        list_entries(entries)
        return

    by_id = {e["id"]: e for e in entries}
    unknown = [n for n in args.name if n not in by_id]
    if unknown:
        sys.exit(f"未知数据集 id: {unknown}，使用 --list 查看。")

    targets = [e for e in entries if e.get("access") == "direct"] if args.all else [by_id[n] for n in args.name]
    for e in targets:
        fetch(e, args.out)


if __name__ == "__main__":
    main()
