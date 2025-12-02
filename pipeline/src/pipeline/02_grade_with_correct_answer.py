import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

COMMON_SRC = Path(__file__).resolve().parents[1]
if str(COMMON_SRC) not in sys.path:
    sys.path.insert(0, str(COMMON_SRC))

from backend.grading.integrations.factory import get_integration
from common.grading import (
    load_model_config,
    load_prompt_config,
    grade_answer,
    write_with_additional_fields,
)

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


def main():
    load_dotenv(PROJECT_ROOT / ".env.dev", override=False)

    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_file", required=True)
    parser.add_argument("--out", dest="output_file", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt_file", required=True)

    args = parser.parse_args()
    model_cfg = load_model_config(args.model)
    prompt_config = load_prompt_config(args.prompt_file)

    grader = get_integration(model_cfg["integration"])
    temperature = float(model_cfg.get("temperature", 0.0) or 0.0)

    def row_updater(row: dict):
        prompt = CORRECT_ANSWER_GRADING_TEMPLATE.format(
            question_text=row["question_text"],
            correct_answer=row["correct_answer"],
            student_answer=row["student_answer"],
        )
        score, explanation, response = grade_answer(
            prompt,
            grader,
            model_cfg["model"],
            prompt_config["correct_answer"],
            temperature,
        )
        row.update(
            {
                "correct_answer_score": score,
                "correct_answer_explanation": explanation,
                "correct_answer_response_raw": response,
            }
        )
        return row

    write_with_additional_fields(
        Path(args.input_file),
        Path(args.output_file),
        [
            "correct_answer_score",
            "correct_answer_explanation",
            "correct_answer_response_raw",
        ],
        row_updater,
    )

    print(f"Grading (correct_answer) complete. Output: {args.output_file}")


if __name__ == "__main__":
    main()
