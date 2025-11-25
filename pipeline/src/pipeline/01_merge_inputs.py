import argparse
import csv
from pathlib import Path

# This script validates and merges questions.csv and student_answers.csv into a single merged file for grading.
def validate_and_merge(questions_path: Path, answers_path: Path, merged_path: Path):
    # ---- Load questions ----
    with questions_path.open("r", encoding="utf-8") as fq:
        q_reader = csv.DictReader(fq)
        required_q_cols = {"Question", "Text", "Answer"}
        if not required_q_cols.issubset(set(q_reader.fieldnames or [])):
            raise ValueError(
                f"questions.csv missing required columns {required_q_cols - set(q_reader.fieldnames or [])}"
            )
        questions = {}
        duplicates = []
        for row in q_reader:
            q_number = row["Question"].strip()
            if not q_number:
                raise ValueError("questions.csv contains empty 'Question' value")
            if q_number in questions:
                duplicates.append(q_number)
            question_text = row["Text"].strip()
            correct_answer = row["Answer"].strip()
            questions[q_number] = {
                "question_text": question_text,
                "correct_answer": correct_answer,
            }
        if duplicates:
            raise ValueError(f"Duplicate Question IDs in questions.csv: {', '.join(duplicates)}")

    # ---- Load answers ----
    with answers_path.open("r", encoding="utf-8") as fa:
        a_reader = csv.DictReader(fa)
        required_a_cols = {"Student", "Question", "Answer"}
        if not required_a_cols.issubset(set(a_reader.fieldnames or [])):
            raise ValueError(
                f"student_answers.csv missing required columns {required_a_cols - set(a_reader.fieldnames or [])}"
            )
        answers_rows = []
        missing_ref_questions = set()
        for row in a_reader:
            q_number = (row.get("Question") or "").strip()
            if not q_number:
                raise ValueError("Encountered answer row without 'Question' value")
            if q_number not in questions:
                missing_ref_questions.add(q_number)
            answers_rows.append({
                "student_id": (row.get("Student") or "").strip(),
                "question_id": q_number,
                "student_answer": (row.get("Answer") or "").strip(),
                "professor_score": (row.get("Score") or "").strip(),
            })
        if missing_ref_questions:
            raise ValueError(
                "Answers reference unknown Question IDs: "
                + ", ".join(sorted(missing_ref_questions))
            )

    # ---- Merge phase ----
    merged_path.parent.mkdir(parents=True, exist_ok=True)
    with merged_path.open("w", newline="", encoding="utf-8") as f_out:
        fieldnames = [
            "student_id",
            "question_id",
            "question_text",
            "correct_answer",
            "student_answer",
            "professor_score",
        ]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for a in answers_rows:
            qinfo = questions[a["question_id"]]
            writer.writerow({
                **a,
                "question_text": qinfo["question_text"],
                "correct_answer": qinfo["correct_answer"],
            })


def main():
    parser = argparse.ArgumentParser(description="Validate and merge questions and answers CSVs.")
    parser.add_argument("--questions", required=True, help="Path to questions.csv")
    parser.add_argument("--answers", required=True, help="Path to student_answers.csv")
    parser.add_argument("--out", required=True, help="Path to output merged CSV (in interim dir)")
    args = parser.parse_args()

    validate_and_merge(Path(args.questions), Path(args.answers), Path(args.out))
    print(f"Merged and validated to {args.out}")

if __name__ == "__main__":
    main()
