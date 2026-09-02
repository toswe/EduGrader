#!/usr/bin/env python3
"""Dijagram rasejanja: ocena nastavnika (x) naspram ocene sistema (y).

Svaki odgovor je jedna tacka; PRA i GRA rezim crtaju se razlicitim bojama.
Ocene su diskretne, pa se svakoj tacki dodaje mali slucajni pomeraj (jitter)
u opsegu (-0.4, 0.4) na obe ose, sa fiksiranim semenom radi reproduktivnosti.

Pokretanje (iz korena pipeline/):
    python3 plot_scatter.py --out ../thesis/slike/rasejanje-p2.pdf
"""
import argparse
import csv
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent

DEFAULT_DATASETS = ["p2_1", "p2_2", "p2_sept2"]


def safe_score(x: str):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if v >= 0 else None


def load_pairs(path: Path):
    """Vraca listu parova (ocena nastavnika 0-10, ocena sistema 0-10)."""
    pairs = []
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            prof = safe_score(row.get("professor_score"))
            system = safe_score(row.get("correct_answer_score"))
            if prof is None or system is None:
                continue
            pairs.append((prof, system / 10.0))
    return pairs


def jitter(pairs, rng, amount=0.4):
    return [
        (x + rng.uniform(-amount, amount), y + rng.uniform(-amount, amount))
        for x, y in pairs
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datasets", nargs="+", default=DEFAULT_DATASETS)
    parser.add_argument("--model", default="gpt-5")
    parser.add_argument("--strictness", default="default")
    parser.add_argument("--out", default="scatter_p2.pdf")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    pra, gra = [], []
    for dataset in args.datasets:
        graded = ROOT / "data" / dataset / "graded"
        pra += load_pairs(graded / f"graded.{args.strictness}.{args.model}.correct.csv")
        gra += load_pairs(graded / f"graded.generated.{args.strictness}.{args.model}.csv")
    print(f"PRA: {len(pra)} odgovora, GRA: {len(gra)} odgovora")

    rng = random.Random(args.seed)
    pra_j = jitter(pra, rng)
    gra_j = jitter(gra, rng)

    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    ax.plot([-0.6, 10.6], [-0.6, 10.6], color="gray", linewidth=0.8, zorder=1)
    ax.scatter(*zip(*pra_j), s=14, alpha=0.45, color="tab:blue", label="PRA", zorder=2)
    ax.scatter(*zip(*gra_j), s=14, alpha=0.45, color="tab:orange", label="GRA", zorder=2)
    ax.set_xlim(-0.6, 10.6)
    ax.set_ylim(-0.6, 10.6)
    ax.set_aspect("equal")
    ax.set_xticks(range(0, 11))
    ax.set_yticks(range(0, 11))
    ax.set_xlabel("Ocena nastavnika")
    ax.set_ylabel("Ocena sistema")
    ax.legend(loc="upper left")
    fig.tight_layout()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    print(f"Sacuvano: {out}")


if __name__ == "__main__":
    main()
