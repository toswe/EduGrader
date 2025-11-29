import argparse
import csv
import sys
from pathlib import Path
from typing import Tuple
import yaml
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from backend.grading.integrations.factory import get_integration

ERROR_SCORE = -1
SCORING_INSTRUCTIONS = """

Tvoj odgovor treba da bude ocena studentskog odgovora u sledećem formatu:
Prvi red treba da sadrži samo broj na skali od 0 do 100, gde je 100 najbolja ocena a 0 najgora.
Ostatak odgovora treba da sadrži obrazloženje ocene.

"""
CORRECT_ANSWER_GRADING_TEMPLATE = """Pitanje:\n```
{question_text}
```
\nTačan odgovor:\n```
{correct_answer}
```
\nOdgovor studenta:\n```
{student_answer}
```
"""

GRADING_TEMPLATE_TEXTBOOK = """Pitanje:\n```
{question_text}
```
\nOdgovor studenta:\n```
{student_answer}
```
```
\nRelevantni pasusi iz udžbenika:\n```
{textbook}
"""


def load_prompt_config(prompt_file: str) -> str:
    with open(prompt_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["prompt"]


def load_model_config(model_param: str) -> dict:
    with open(model_param, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {
        "integration": data["integration"],
        "model": data["model"],
        "temperature": data.get("temperature", 0.0),
    }


def parse_score_from_response(response_text: str):
    try:
        first_line, explanation = response_text.split("\n", 1)
        score = int(first_line.strip())
        return score, explanation.strip()
    except (ValueError, TypeError):
        return None, response_text


def grade_answer(
    prompt: str,
    grader: object,
    model: str,
    instructions: str,
    temperature: float = 0,
    max_retries: int = 3,
) -> Tuple[int, str, str]:
    full_instructions = instructions.strip() + "\n" + SCORING_INSTRUCTIONS

    for _ in range(max_retries):
        text, full_response = grader.prompt(
            prompt,
            model=model,
            instructions=full_instructions,
            temperature=temperature,
        )
        score, explanation = parse_score_from_response(text)
        if score is not None:
            return score, explanation, str(full_response)

    return ERROR_SCORE, text, str(full_response)


def grade(
    merged_path: Path,
    output_path: Path,
    integration: str,
    model: str,
    instructions_correct: str,
    instructions_textbook: str,
    temperature: float = 0,
):
    grader = get_integration(integration)

    with merged_path.open("r", encoding="utf-8") as fin, output_path.open(
        "w", newline="", encoding="utf-8"
    ) as fout:
        reader = csv.DictReader(fin)

        fieldnames = reader.fieldnames + [
            "correct_answer_score",
            "correct_answer_explanation",
            "correct_answer_response_raw",
            "textbook_score",
            "textbook_explanation",
            "textbook_response_raw",
        ]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Correct answer
            prompt_correct = CORRECT_ANSWER_GRADING_TEMPLATE.format(
                question_text=row["question_text"],
                correct_answer=row["correct_answer"],
                student_answer=row["student_answer"],
            )
            score_correct, explanation_correct, response_correct = grade_answer(
                prompt_correct,
                grader,
                model,
                instructions_correct,
                temperature,
            )

            # Textbook
            prompt_textbook = GRADING_TEMPLATE_TEXTBOOK.format(
                question_text=row["question_text"],
                textbook=row.get("textbook", ""),
                student_answer=row["student_answer"],
            )
            score_textbook, explanation_textbook, response_textbook = grade_answer(
                prompt_textbook,
                grader,
                model,
                instructions_textbook,
                temperature,
            )
            row.update(
                {
                    "correct_answer_score": score_correct,
                    "correct_answer_explanation": explanation_correct,
                    "correct_answer_response_raw": response_correct,
                    "textbook_score": score_textbook,
                    "textbook_explanation": explanation_textbook,
                    "textbook_response_raw": response_textbook,
                }
            )
            writer.writerow(row)


def main():
    load_dotenv(WORKSPACE_ROOT / ".env.dev", override=False)

    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_file", required=True)
    parser.add_argument("--out", dest="output_dir", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt_file", required=True)

    args = parser.parse_args()
    model_cfg = load_model_config(args.model)
    prompt_config = load_prompt_config(args.prompt_file)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    temperature = float(model_cfg.get("temperature", 0.0) or 0.0)
    temp_part = f"-t{str(temperature).replace('.', '_')}" if temperature != 0.0 else ""

    output_name = f"graded-{prompt_config["name"]}-{model_cfg["model"]}{temp_part}.csv"
    output_file = output_dir / output_name

    grade(
        Path(args.input_file),
        output_file,
        model_cfg["integration"],
        model_cfg["model"],
        prompt_config["correct_answer"],
        prompt_config["textbook"],
        temperature,
    )
    print(f"Grading complete. Output: {output_file}")


if __name__ == "__main__":
    main()
