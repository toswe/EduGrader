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

TEXTBOOK_GRADING_TEMPLATE = """Pitanje:\n```
{question_text}
```
\nOdgovor studenta:\n```
{student_answer}
```
\Udžbenik:\n```
{textbook}
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
        prompt = TEXTBOOK_GRADING_TEMPLATE.format(
            question_text=row["question_text"],
            textbook=row.get("textbook", ""),
            student_answer=row["student_answer"],
        )
        score, explanation, response = grade_answer(
            prompt,
            grader,
            model_cfg["model"],
            prompt_config["textbook"],
            temperature,
        )
        row.update(
            {
                "textbook_score": score,
                "textbook_explanation": explanation,
                "textbook_response_raw": response,
            }
        )
        return row

    write_with_additional_fields(
        Path(args.input_file),
        Path(args.output_file),
        [
            "textbook_score",
            "textbook_explanation",
            "textbook_response_raw",
        ],
        row_updater,
    )

    print(f"Grading (textbook) complete. Output: {args.output_file}")


if __name__ == "__main__":
    main()
