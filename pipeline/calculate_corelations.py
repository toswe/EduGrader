#!/usr/bin/env python3
import csv
import math
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


ROOT = Path(__file__).resolve().parent


def load_datasets(params_path: Path) -> List[str]:
    with open(params_path, "r", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    datasets = params.get("datasets", [])
    if not isinstance(datasets, list) or not datasets:
        raise ValueError("No datasets defined in params.yaml")
    return datasets


def list_graded_files(dataset: str) -> List[Path]:
    graded_dir = ROOT / "data" / dataset / "graded"
    if not graded_dir.exists():
        return []
    return sorted([p for p in graded_dir.glob("*.csv") if p.is_file()])


def count_original_rows(dataset: str) -> Optional[int]:
    """Count rows in the original input used for grading.

    Prefer the merged file produced in the pipeline stage:
    data/<dataset>/interim/merged.csv
    """
    merged = ROOT / "data" / dataset / "interim" / "merged.csv"
    if not merged.exists():
        return None
    try:
        with open(merged, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            # assume header present
            header = next(reader, None)
            return sum(1 for _ in reader)
    except Exception:
        return None


FNAME_PATTERNS = [
    # DVC-generated: graded.<strictness>.<model>.<method>.csv
    re.compile(r"^graded\.(?P<strictness>[^.]+)\.(?P<model>[^.]+)\.(?P<method>correct|textbook)\.csv$"),
]


def parse_filename(fname: str) -> Optional[Dict[str, str]]:
    name = Path(fname).name
    for pat in FNAME_PATTERNS:
        m = pat.match(name)
        if m:
            return {
                "strictness": m.group("strictness"),
                "model": m.group("model"),
                "method": m.group("method"),
            }
    return None


def safe_float(x: str) -> Optional[float]:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def pearson(x: List[float], y: List[float]) -> Optional[float]:
    n = len(x)
    if n == 0 or len(y) != n:
        return None
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
    den_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    den = den_x * den_y
    if den == 0:
        return None
    return num / den


def compute_metrics(csv_path: Path) -> Dict[str, Optional[float]]:
    prof: List[float] = []
    llm: List[float] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Try common column names from backend export and pipeline results
        prof_keys = ["professor_score", "prof_score", "teacher_score"]
        llm_keys = ["llm_score", "correct_answer_score", "textbook_score"]

        for row in reader:
            # Determine llm score field present in row
            llm_val = None
            for k in llm_keys:
                if k in row:
                    llm_val = safe_float(row[k])
                    if llm_val is not None:
                        break
            prof_val = None
            for k in prof_keys:
                if k in row:
                    prof_val = safe_float(row[k])
                    if prof_val is not None:
                        break

            if prof_val is not None and llm_val is not None:
                prof.append(prof_val)
                llm.append(llm_val)

    # Scale LLM scores from 0-100 to 0-10 to match professor scale
    llm = [v / 10.0 for v in llm]
    n = len(prof)
    corr = pearson(prof, llm) if n > 1 else None
    avg_prof = sum(prof) / n if n else None
    avg_llm = sum(llm) / n if n else None
    avg_ratio = (avg_llm / avg_prof) if (avg_llm is not None and avg_prof not in (None, 0)) else None
    rmse = math.sqrt(sum((px - lx) ** 2 for px, lx in zip(prof, llm)) / n) if n else None
    # population stddev for professor scores
    if n:
        mean_prof = avg_prof if avg_prof is not None else 0.0
        var_prof = sum((px - mean_prof) ** 2 for px in prof) / n
        stddev_prof = math.sqrt(var_prof)
    else:
        stddev_prof = None
    rmse_std_ratio = (rmse / stddev_prof) if (rmse is not None and stddev_prof not in (None, 0)) else None
    return {
        "correlation": corr,
        "average_professor_score": avg_prof,
        "average_llm_score": avg_llm,
        "average_score_ratio": avg_ratio,
        "rmse": rmse,
        "professor_stddev": stddev_prof,
        "rmse_stddev_ratio": rmse_std_ratio,
    }


def write_dataset_results(dataset: str, rows: List[Dict[str, str]]) -> None:
    out_path = ROOT / "data" / dataset / "graded" / "correlation_results.csv"
    fieldnames = [
        "dataset_name",
        "model_name",
        "strictness_level",
        "method",
        "correlation",
        "average_professor_score",
        "average_llm_score",
        "average_score_ratio",
        "rmse",
        "professor_stddev",
        "rmse_stddev_ratio",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def append_global_summary(all_rows: List[Dict[str, str]]) -> None:
    out_path = ROOT / "data" / "correlation_summary.csv"
    fieldnames = [
        "dataset_name",
        "model_name",
        "strictness_level",
        "method",
        "correlation",
        "average_professor_score",
        "average_llm_score",
        "average_score_ratio",
        "rmse",
        "professor_stddev",
        "rmse_stddev_ratio",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in all_rows:
            w.writerow(r)


def main() -> None:
    datasets = load_datasets(ROOT / "params.yaml")
    global_rows: List[Dict[str, str]] = []

    for dataset in datasets:
        graded_files = list_graded_files(dataset)
        original_n = count_original_rows(dataset)
        dataset_rows: List[Dict[str, str]] = []
        for f in graded_files:
            meta = parse_filename(f.name)
            if not meta:
                # skip unrelated CSVs
                continue
            # Enforce full coverage: only process if all rows graded
            if original_n is not None:
                try:
                    with open(f, "r", encoding="utf-8") as fh:
                        reader = csv.reader(fh)
                        next(reader, None)  # header
                        graded_n = sum(1 for _ in reader)
                    if graded_n != original_n:
                        # skip partial results
                        continue
                except Exception:
                    continue

            metrics = compute_metrics(f)
            row = {
                "dataset_name": dataset,
                "model_name": meta["model"],
                "strictness_level": meta["strictness"],
                "method": "correct_answer" if meta["method"] == "correct" else "textbook_based",
                "correlation": "" if metrics["correlation"] is None else f"{metrics['correlation']:.6f}",
                "average_professor_score": "" if metrics["average_professor_score"] is None else f"{metrics['average_professor_score']:.6f}",
                "average_llm_score": "" if metrics["average_llm_score"] is None else f"{metrics['average_llm_score']:.6f}",
                "average_score_ratio": "" if metrics["average_score_ratio"] is None else f"{metrics['average_score_ratio']:.6f}",
                "rmse": "" if metrics["rmse"] is None else f"{metrics['rmse']:.6f}",
                "professor_stddev": "" if metrics["professor_stddev"] is None else f"{metrics['professor_stddev']:.6f}",
                "rmse_stddev_ratio": "" if metrics["rmse_stddev_ratio"] is None else f"{metrics['rmse_stddev_ratio']:.6f}",
            }
            dataset_rows.append(row)
            global_rows.append(row)

        # write per-dataset results
        write_dataset_results(dataset, dataset_rows)

    # write global summary
    append_global_summary(global_rows)


if __name__ == "__main__":
    main()
# This script should do the same as calculate_corelations.py in the root/scripts directory
# But it should loop through all datasets defined in params.yaml
# Besides the columns in the original script, it should also store:
# - dataset_name
# - model_name
# - strictness_level
# - correct_answer or textbook_based (indicating which grading method was used)
#
# It should read all of the files in the graded directory for each dataset
# And write the correlation results to data/<dataset_name>/graded/correlation_results.csv
# After that, it should also write a summary file data/correlation_summary.csv
# That file should contain all of the correlation results for all datasets
