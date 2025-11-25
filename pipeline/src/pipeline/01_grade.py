import argparse
import csv
import json
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Add the workspace root to Python path so we can import from backend
workspace_root = Path(__file__).resolve().parents[3]
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

from backend.grading.integrations.factory import get_integration


QUESTION_WRAPPER = """
Pitanje:
```
{question_text}
```
"""
CORRECT_ANSWER_WRAPPER = """
Tačan odgovor:
```
{correct_answer}
```
"""
STUDENT_ANSWER_WRAPPER = """
Odgovor studenta:
```
{student_answer}
```
"""

SCORING_INSTRUCTIONS = """

Tvoj odgovor treba da bude ocena studentskog odgovora u sledećem formatu:
Prvi red treba da sadrži samo broj na skali od 0 do 100, gde je 100 najbolja ocena a 0 najgora.
Ostatak odgovora treba da sadrži obrazloženje ocene.

"""


def load_prompt(prompt_file: str) -> str:
    with open(prompt_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["prompt"]["text"].strip()


def load_model_config(model_param: str) -> dict:
    with open(model_param, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return {
        "integration": data["integration"],
        "model": data["model"],
        "temperature": data.get("temperature", 0.0),
    }


def build_prompt(question_text: str, correct_answer: str, student_answer: str) -> str:
    question = QUESTION_WRAPPER.format(question_text=question_text)
    correct = CORRECT_ANSWER_WRAPPER.format(correct_answer=correct_answer)
    student = STUDENT_ANSWER_WRAPPER.format(student_answer=student_answer)
    return "\n".join([question, correct, student])


def parse_score_from_response(response_text: str) -> tuple[int | None, str]:
    try:
        first_line, explanation = response_text.split("\n", 1)
        score = int(first_line.strip())
        return score, explanation.strip()
    except (ValueError, TypeError):
        return None, response_text


def grade_answer(
    question: str,
    correct_answer: str,
    student_answer: str,
    integration_name: str,
    model: str,
    instructions: str,
    temperature: float = 0,
    max_retries: int = 3,
) -> tuple[int, str, str]:
    full_instructions = instructions + SCORING_INSTRUCTIONS
    prompt = build_prompt(question, correct_answer, student_answer)
    grader = get_integration(integration_name)
    
    for _ in range(max_retries):
        text, full_response = grader.prompt(
            prompt, model=model, instructions=full_instructions, temperature=temperature
        )
        
        score, explanation = parse_score_from_response(text)
        if score is not None:
            raw = json.dumps(full_response, ensure_ascii=False, default=str)
            return score, explanation, raw
    
    # After max_retries, return -1 with full text
    raw = json.dumps(full_response, ensure_ascii=False, default=str)
    return -1, text, raw


def process_questions_and_answers(
    questions_path: Path,
    answers_path: Path,
    output_path: Path,
    integration_name: str,
    model: str,
    instructions: str,
    temperature: float = 0,
):
    """Load & validate both CSVs, then grade all answers.

    Strict expectations:
      questions.csv headers MUST include: Question, Text, Answer
      student_answers.csv headers MUST include: Student, Question, Answer
      Optional headers: Score, ignore

    Validation performed BEFORE any grading:
      - All required headers present
      - No duplicate Question values in questions.csv
      - Every answer row's Question exists in questions set
      - (Optional) We allow questions without answers (no error)
    On failure: raise ValueError with concise diagnostic.
    """

    # ---- Load questions ----
    with questions_path.open("r", encoding="utf-8") as fq:
        q_reader = csv.DictReader(fq)
        required_q_cols = {"Question", "Text", "Answer"}
        if not required_q_cols.issubset(set(q_reader.fieldnames or [])):
            raise ValueError(
                f"questions.csv missing required columns {required_q_cols - set(q_reader.fieldnames or [])}"
            )
        questions: dict[str, dict[str, str]] = {}
        duplicates: list[str] = []
        for row in q_reader:
            # Fail fast on missing keys rather than silent defaulting.
            try:
                q_number = row["Question"].strip()
            except KeyError:
                raise ValueError("questions.csv row missing 'Question' column")
            if not q_number:
                raise ValueError("questions.csv contains empty 'Question' value")
            if q_number in questions:
                duplicates.append(q_number)

            # Required textual fields
            try:
                question_text = row["Text"].strip()
            except KeyError:
                raise ValueError(f"questions.csv row for Question={q_number} missing 'Text'")
            if not question_text:
                raise ValueError(f"Question {q_number} has empty 'Text' value")

            try:
                correct_answer = row["Answer"].strip()
            except KeyError:
                raise ValueError(f"questions.csv row for Question={q_number} missing 'Answer'")
            if not correct_answer:
                raise ValueError(f"Question {q_number} has empty 'Answer' value")

            long_id = row.get("ignore", "").strip()

            questions[q_number] = {
                "question_text": question_text,
                "correct_answer": correct_answer,
                "long_id": long_id,
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
        answers_rows: list[dict[str, str]] = []
        missing_ref_questions: set[str] = set()
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

    # ---- Grading phase (after validation) ----
    with output_path.open("w", newline="", encoding="utf-8") as f_out:
        fieldnames = [
            "student_id",
            "question_id",
            "question_long_id",
            "question_text",
            "correct_answer",
            "student_answer",
            "professor_score",
            "llm_score",
            "llm_explanation",
            "llm_response_raw",
        ]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for a in answers_rows:
            qinfo = questions[a["question_id"]]
            llm_score, llm_explanation, llm_response_raw = grade_answer(
                qinfo["question_text"],
                qinfo["correct_answer"],
                a["student_answer"],
                integration_name,
                model,
                instructions,
                temperature,
            )
            writer.writerow({
                **a,
                "question_long_id": qinfo["long_id"],
                "question_text": qinfo["question_text"],
                "correct_answer": qinfo["correct_answer"],
                "llm_score": llm_score,
                "llm_explanation": llm_explanation,
                "llm_response_raw": llm_response_raw,
            })


def main():
    workspace_root = Path(__file__).resolve().parents[3]
    dotenv_path = workspace_root / ".env.dev"
    if dotenv_path.is_file():
        load_dotenv(dotenv_path, override=False)

    parser = argparse.ArgumentParser(description="Grade student answers using an LLM")
    parser.add_argument("--in", dest="input_root", required=True)
    parser.add_argument("--out", dest="output_root", required=True)
    parser.add_argument("--model", dest="model_param", required=True)
    parser.add_argument("--prompt_file", required=True)
    args = parser.parse_args()

    input_root = Path(args.input_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    model_cfg = load_model_config(args.model_param)
    instructions = load_prompt(args.prompt_file)

    questions_file = input_root / "questions.csv"
    answers_file = input_root / "student_answers.csv"
    if not questions_file.is_file() or not answers_file.is_file():
        raise FileNotFoundError(
            "Expected questions.csv and student_answers.csv in input directory; legacy formats are no longer supported."
        )
    out_path = output_root / "student_answers.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Joining & grading {questions_file.name} + {answers_file.name} -> {out_path}")
    process_questions_and_answers(
        questions_file,
        answers_file,
        out_path,
        model_cfg["integration"],
        model_cfg["model"],
        instructions,
        model_cfg["temperature"],
    )


if __name__ == "__main__":
    main()
