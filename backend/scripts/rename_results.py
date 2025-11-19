#!/usr/bin/env python3
"""
Rename benchmark result files inside data/**/results according to rules:

  - result.openai.<name>.csv   -> <name>.csv
  - result.deepseek.<name>.csv -> <name>.csv

Features:
  - Dry-run by default: shows what would change
  - --apply to perform changes
  - --overwrite to allow replacing existing targets
  - Skips files that don't match or would be no-ops

Usage examples:
  Dry run:  python rename_results.py
  Apply:    python rename_results.py --apply
  Apply + overwrite collisions: python rename_results.py --apply --overwrite
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


@dataclass
class PlanItem:
    src: Path
    dst: Path
    reason: str


PREFIXES = (
    "11.result.openai.",
    "11.result.deepseek.",
)


def compute_destination(p: Path) -> Path | None:
    """Return destination path if file name matches, else None.

    We only change the file name; the directory remains the same.
    """
    name = p.name
    for prefix in PREFIXES:
        if name.startswith(prefix):
            # Strip the prefix
            new_name = name[len(prefix) :]
            # Only process .csv files
            if not new_name.endswith(".csv"):
                return None
            return p.with_name(new_name)
    return None


def find_candidates(base: Path) -> list[PlanItem]:
    items: list[PlanItem] = []
    for results_dir in base.rglob("results"):
        if not results_dir.is_dir():
            continue
        for file in results_dir.glob("*.csv"):
            dst = compute_destination(file)
            if dst is None or dst == file:
                continue
            # prevent self overwrite if names are equal after trim
            items.append(PlanItem(src=file, dst=dst, reason="prefix-strip"))
    return items


def parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform renames (default is dry-run)",
    )
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting existing destination files",
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=DATA_DIR,
        help="Root directory to scan (default: ./data)",
    )
    return ap.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    base: Path = args.root

    if not base.exists():
        print(f"Root directory does not exist: {base}", file=sys.stderr)
        return 2

    plan = find_candidates(base)
    if not plan:
        print("No files to rename. Nothing to do.")
        return 0

    # Summarize plan
    print(f"Found {len(plan)} file(s) to rename under {base}:")
    collisions = 0
    for item in plan:
        exists = item.dst.exists()
        if exists:
            collisions += 1
        status = "EXISTS" if exists else "ok"
        print(f"  - {item.src} -> {item.dst}  [{status}]")

    if not args.apply:
        print("\nDry-run only. Re-run with --apply to perform these changes.")
        return 0

    if collisions and not args.overwrite:
        print(
            f"\nAborting: {collisions} destination file(s) already exist. "
            "Use --overwrite to allow replacing them.",
            file=sys.stderr,
        )
        return 3

    # Execute renames
    performed = 0
    skipped = 0
    for item in plan:
        try:
            if item.dst.exists() and not args.overwrite:
                skipped += 1
                continue
            # Ensure parent dir exists (it should), but be safe
            item.dst.parent.mkdir(parents=True, exist_ok=True)
            item.src.replace(item.dst)
            performed += 1
        except Exception as e:
            skipped += 1
            print(f"Failed to rename {item.src} -> {item.dst}: {e}", file=sys.stderr)

    print(
        f"\nDone. Performed {performed} rename(s), skipped {skipped}. "
        f"Root scanned: {base}"
    )
    return 0 if performed or skipped == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
