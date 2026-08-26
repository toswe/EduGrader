#!/usr/bin/env python3
"""Average length (words, characters) of instructor reference answers,
student answers and generated reference answers, over all datasets.

Instructor and student answers are read from the PRA run of one model
(the columns are identical across models); generated reference answers are
read from the neutral GRA run of each model. Rows whose generated answer is
an API error message (the textbook exceeded the model's context window, so
no answer was generated) are excluded from the generated-answer averages
and reported separately."""
import csv
from pathlib import Path

from calculate_correlations import load_datasets

ROOT = Path(__file__).resolve().parent

REFERENCE_FILE = "graded.default.gpt-5.correct.csv"
GENERATED_PATTERN = "graded.generated.default.{model}.csv"
MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-5", "deepseek-chat", "deepseek-reasoner"]
ERROR_PREFIX = "ERROR:"

OUT_PATH = ROOT / "data" / "length_summary.csv"
FIELDNAMES = ["source", "model_name", "n", "n_error", "avg_words", "avg_chars"]


def read_rows(dataset: str, filename: str) -> list:
    path = ROOT / "data" / dataset / "graded" / filename
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def summarize(texts: list) -> tuple:
    n = len(texts)
    if n == 0:
        return 0, 0.0, 0.0
    words = sum(len(t.split()) for t in texts) / n
    chars = sum(len(t) for t in texts) / n
    return n, words, chars


def main() -> None:
    datasets = load_datasets(ROOT / "params.yaml")
    results = []

    instructor, student = [], []
    for ds in datasets:
        for row in read_rows(ds, REFERENCE_FILE):
            instructor.append(row["correct_answer"])
            student.append(row["student_answer"])
    for source, texts in (("instructor", instructor), ("student", student)):
        n, w, c = summarize(texts)
        results.append((source, "", n, 0, w, c))

    for model in MODELS:
        generated, errors = [], 0
        for ds in datasets:
            for row in read_rows(ds, GENERATED_PATTERN.format(model=model)):
                text = row["correct_answer"]
                if text.startswith(ERROR_PREFIX):
                    errors += 1
                else:
                    generated.append(text)
        n, w, c = summarize(generated)
        results.append(("generated", model, n, errors, w, c))

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDNAMES)
        for source, model, n, n_err, w, c in results:
            writer.writerow([source, model, n, n_err, f"{w:.1f}", f"{c:.1f}"])
            label = f"{source} {model}".strip()
            print(f"{label:32s} n={n:4d} errors={n_err:4d} words={w:6.1f} chars={c:7.1f}")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
