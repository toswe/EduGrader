import argparse
import csv
from collections import Counter
from pathlib import Path


def vallidate_columns(required_cols: set, reader: csv.DictReader):
    for col in required_cols:
        if col not in (reader.fieldnames or []):
            raise ValueError(f"questions.csv missing required column: {col}")


def validate_questions(questions_path: Path) -> dict:
    with questions_path.open("r", encoding="utf-8") as fq:
        q_reader = csv.DictReader(fq)
        required_q_cols = {"Question", "Text", "Answer"}
        vallidate_columns(required_q_cols, q_reader)

        questions = {}
        for row in q_reader:
            q_number = row["Question"].strip()
            if not q_number:
                raise ValueError("questions.csv contains empty 'Question' value")
            if q_number in questions:
                raise ValueError(f"Duplicate Question ID found in questions.csv: {q_number}")
            question_text = row["Text"].strip()
            if not question_text:
                raise ValueError(f"Question {q_number} has empty 'Text' value")
            correct_answer = row["Answer"].strip()
            if not correct_answer:
                raise ValueError(f"Question {q_number} has empty 'Answer' value")
            questions[q_number] = {
                "question_text": question_text,
                "correct_answer": correct_answer,
            }

        return questions


def validate_answers(answers_path: Path, questions: dict) -> list[dict]:
    with answers_path.open("r", encoding="utf-8") as fa:
        a_reader = csv.DictReader(fa)
        required_a_cols = {"Student", "Question", "Answer", "Score"}
        vallidate_columns(required_a_cols, a_reader)

        answers_rows = []
        for row in a_reader:
            q_number = row["Question"].strip()
            if q_number not in questions:
                raise ValueError(f"answers.csv references unknown Question ID: {q_number}")
            answers_rows.append(
                {
                    "student_id": row["Student"].strip(),
                    "question_id": q_number,
                    "student_answer": row["Answer"].strip(),
                    "professor_score": row["Score"].strip(),
                }
            )

        expected = len(questions)
        answers_count = Counter(a["student_id"] for a in answers_rows)
        for student_id, count in answers_count.items():
            if count != expected:
                raise ValueError(f"Student {student_id} has {count} answers, expected {expected}")

        return answers_rows


def merge(questions_path: Path, answers_path: Path, merged_path: Path):
    questions = validate_questions(questions_path)
    answers_rows = validate_answers(answers_path, questions)

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
            writer.writerow(
                {
                    **a,
                    "question_text": qinfo["question_text"],
                    "correct_answer": qinfo["correct_answer"],
                }
            )


def main():
    parser = argparse.ArgumentParser(description="Validate and merge questions and answers CSVs.")
    parser.add_argument("--questions", required=True, help="Path to questions.csv")
    parser.add_argument("--answers", required=True, help="Path to student_answers.csv")
    parser.add_argument("--out", required=True, help="Path to output merged CSV (in interim dir)")
    args = parser.parse_args()

    merge(Path(args.questions), Path(args.answers), Path(args.out))
    print(f"Merged and validated to {args.out}")


if __name__ == "__main__":
    main()
