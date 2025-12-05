import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
from common.pdf_extraction import extract_pdf

TEXTBOOK_GRADING_TEMPLATE = (
    "Pitanje:\n```\n{question_text}\n```\n"
    "\nOdgovor studenta:\n```\n{student_answer}\n```\n"
    "\nUdžbenik:\n```\n{textbook}\n```\n"
)


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
        textbook_src = row.get("textbook", "")
        logger.info(f"Fetching textbook for question: {row.get('question_text', '')[:50]}...")
        textbook_text = extract_pdf(textbook_src)
        if not textbook_text:
            logger.error(f"Failed to fetch textbook text from source: {textbook_src}")
            raise Exception(f"Failed to fetch textbook text from source: {textbook_src}")
        prompt = TEXTBOOK_GRADING_TEMPLATE.format(
            question_text=row["question_text"],
            textbook=textbook_text,
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

    in_path = Path(args.input_file)
    out_path = Path(args.output_file)

    write_with_additional_fields(
        in_path,
        out_path,
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
