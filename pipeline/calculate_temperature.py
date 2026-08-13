#!/usr/bin/env python3
"""Pairs temperature-sweep runs (outside pipeline/data) with the matching
baseline run and reports the same metrics as calculate_corelations.py."""
import csv
import math
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, cast

from calculate_corelations import pearson, safe_float


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent

DATASET_MAP = {
    "p2": "p2_1",
    "p2_jul_2": "p2_2",
    "uu": "uu",
    "dzp": "dzp",
}

BASELINE_FILE = "graded.default.gpt-4o.correct.csv"
BASELINE_SCORE_COLUMN = "correct_answer_score"
TEMPERATURES = ["0.5", "1"]

OUT_PATH = ROOT / "data" / "temperature_summary.csv"
FIELDNAMES = [
    "dataset_name",
    "model_name",
    "strictness_level",
    "method",
    "temperature",
    "correlation",
    "average_professor_score",
    "average_llm_score",
    "average_score_ratio",
    "rmse",
    "professor_stddev",
    "rmse_stddev_ratio",
]


def sort_key(row: Dict[str, str]) -> Tuple[int, float]:
    student = re.search(r"\d+", row.get("student_id") or "")
    question = safe_float(row.get("question_id") or "")
    return (int(student.group()) if student else -1, question if question is not None else -1.0)


def read_scores(path: Path, score_column: str) -> List[Tuple[Optional[float], Optional[float]]]:
    with open(path, "r", encoding="utf-8") as f:
        rows = sorted(csv.DictReader(f), key=sort_key)
    return [
        (safe_float(r.get("professor_score") or ""), safe_float(r.get(score_column) or ""))
        for r in rows
    ]


def metrics_from_pairs(prof: List[float], llm: List[float]) -> Dict[str, Optional[float]]:
    llm = [v / 10.0 for v in llm]
    n = len(prof)
    if not n:
        return {k: None for k in FIELDNAMES[5:]}
    avg_prof = sum(prof) / n
    avg_llm = sum(llm) / n
    rmse = math.sqrt(sum((p - l) ** 2 for p, l in zip(prof, llm)) / n)
    stddev = math.sqrt(sum((p - avg_prof) ** 2 for p in prof) / n)
    return {
        "correlation": pearson(prof, llm) if n > 1 else None,
        "average_professor_score": avg_prof,
        "average_llm_score": avg_llm,
        "average_score_ratio": (avg_llm / avg_prof) if avg_prof else None,
        "rmse": rmse,
        "professor_stddev": stddev,
        "rmse_stddev_ratio": (rmse / stddev) if stddev else None,
    }


def collect() -> Dict[str, Dict[str, List[Tuple[float, float]]]]:
    collected: Dict[str, Dict[str, List[Tuple[float, float]]]] = {}

    for session, dataset in DATASET_MAP.items():
        baseline_path = ROOT / "data" / dataset / "graded" / BASELINE_FILE
        if not baseline_path.exists():
            raise SystemExit(f"Missing baseline run: {baseline_path}")
        runs = {"default": read_scores(baseline_path, BASELINE_SCORE_COLUMN)}

        for temperature in TEMPERATURES:
            path = REPO_ROOT / "data" / session / "results" / f"gpt-4o.default.t-{temperature}.csv"
            if not path.exists():
                raise SystemExit(f"Missing temperature run: {path}")
            runs[temperature] = read_scores(path, "llm_score")

        lengths = {len(rows) for rows in runs.values()}
        if len(lengths) != 1:
            raise SystemExit(
                f"{dataset}: runs have different row counts {sorted(lengths)}, cannot align"
            )

        for temperature, rows in runs.items():
            if temperature == "default":
                continue
            mismatched = sum(
                1 for (p1, _), (p2, _) in zip(runs["default"], rows) if p1 != p2
            )
            if mismatched:
                raise SystemExit(
                    f"{dataset}: teacher scores differ in {mismatched} rows for temperature "
                    f"{temperature}, the two sources are not aligned"
                )

        def graded(row: Tuple[Optional[float], Optional[float]]) -> bool:
            professor_score, model_score = row
            return professor_score is not None and model_score is not None and model_score >= 0

        usable = [
            i
            for i in range(len(runs["default"]))
            if all(graded(rows[i]) for rows in runs.values())
        ]
        collected[dataset] = {
            temperature: cast(
                List[Tuple[float, float]], [(rows[i][0], rows[i][1]) for i in usable]
            )
            for temperature, rows in runs.items()
        }

    return collected


def format_row(dataset: str, temperature: str, metrics: Dict[str, Optional[float]]) -> Dict[str, str]:
    row = {
        "dataset_name": dataset,
        "model_name": "gpt-4o",
        "strictness_level": "default",
        "method": "correct_answer",
        "temperature": temperature,
    }
    row.update(
        {k: "" if metrics[k] is None else f"{metrics[k]:.6f}" for k in FIELDNAMES[5:]}
    )
    return row


def print_table(title: str, metrics_by_temperature: Dict[str, Dict[str, Optional[float]]], n: int) -> None:
    print(f"\n{title} ({n} answers)")
    print(f"  {'temperature':<14}{'PCC':>8}{'score ratio':>14}{'RMSE/STDDEV':>14}")
    for temperature, metrics in metrics_by_temperature.items():
        label = "default" if temperature == "default" else temperature
        values = [metrics["correlation"], metrics["average_score_ratio"], metrics["rmse_stddev_ratio"]]
        cells = "".join("           n/a" if v is None else f"{v:>14.4f}" for v in values[1:])
        pcc = "     n/a" if values[0] is None else f"{values[0]:>8.4f}"
        print(f"  {label:<14}{pcc}{cells}")


def main() -> None:
    collected = collect()
    rows: List[Dict[str, str]] = []
    pooled: Dict[str, List[Tuple[float, float]]] = {t: [] for t in ["default"] + TEMPERATURES}

    for dataset, runs in collected.items():
        metrics_by_temperature = {}
        for temperature, pairs in runs.items():
            pooled[temperature].extend(pairs)
            metrics = metrics_from_pairs([p for p, _ in pairs], [l for _, l in pairs])
            metrics_by_temperature[temperature] = metrics
            rows.append(format_row(dataset, temperature, metrics))
        print_table(dataset, metrics_by_temperature, len(runs["default"]))

    combined = {}
    for temperature, pairs in pooled.items():
        metrics = metrics_from_pairs([p for p, _ in pairs], [l for _, l in pairs])
        combined[temperature] = metrics
        rows.append(format_row("all", temperature, metrics))
    print_table("all datasets combined", combined, len(pooled["default"]))

    with open(OUT_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWritten to {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
