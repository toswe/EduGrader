import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
import csv
import time

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

COMMON_SRC = Path(__file__).resolve().parents[1]
if str(COMMON_SRC) not in sys.path:
    sys.path.insert(0, str(COMMON_SRC))

from backend.grading.integrations.factory import get_integration
from common.grading import (
    load_model_config,
)
from common.pdf_extraction import extract_pdf

ANSWER_GENERATION_INSTRUCTIONS = (
    "Ti si profesor visokog obrazovanja i treba da odgovoriš na pitanje "
    "na osnovu relevantnog sadržaja iz udžbenika. "
    "Generiši koncizan odgovor koji direktno odgovara na postavljeno pitanje. "
    "Odgovor treba da bude precizan i dužine od 2 do 5 rečenica."
)

ANSWER_GENERATION_TEMPLATE = (
    "Pitanje:\n```\n{question_text}\n```\n"
    "\nUdžbenik:\n```\n{textbook}\n```\n"
)


def generate_answer(
    prompt: str,
    grader: object,
    model: str,
    instructions: str,
    temperature: float = 0,
    max_retries: int = 3,
) -> tuple[str, str]:
    
    last_text = ""
    last_full_response = None
    for attempt in range(max_retries):
        try:
            text, full_response = grader.prompt(
                prompt,
                model=model,
                instructions=instructions,
                temperature=temperature,
            )
            return text.strip(), str(full_response)
        except Exception as e:
            # transient API/connection error; backoff and retry
            last_text = f"ERROR: {e}"
            last_full_response = None
            if attempt < max_retries - 1:
                time.sleep(1.5 * (attempt + 1))
                continue
            break

    return last_text, str(last_full_response)


def main():
    load_dotenv(PROJECT_ROOT / ".env.dev", override=False)

    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", dest="questions_file", required=True)
    parser.add_argument("--out", dest="output_file", required=True)
    parser.add_argument("--model", required=True)

    args = parser.parse_args()
    model_cfg = load_model_config(args.model)

    grader = get_integration(model_cfg["integration"])
    temperature = float(model_cfg.get("temperature", 0.0) or 0.0)

    # Generate questions CSV with generated answers replacing the correct answers
    # Same format as questions.csv: Question, Text, Answer, Textbook
    Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(args.questions_file, "r", encoding="utf-8") as fin, open(
        args.output_file, "w", newline="", encoding="utf-8"
    ) as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=["Question", "Text", "Answer", "Textbook"])
        writer.writeheader()
        
        for row in reader:
            question_id = row["Question"].strip()
            question_text = row["Text"].strip()
            textbook_src = row["Textbook"].strip()
            
            textbook_text = extract_pdf(textbook_src)
            if not textbook_text:
                raise Exception(f"Failed to fetch textbook text from source: {textbook_src}")
            
            prompt = ANSWER_GENERATION_TEMPLATE.format(
                question_text=question_text,
                textbook=textbook_text,
            )
            
            answer, response = generate_answer(
                prompt,
                grader,
                model_cfg["model"],
                ANSWER_GENERATION_INSTRUCTIONS,
                temperature,
            )
            
            # Write same structure as questions.csv but with generated answer
            writer.writerow({
                "Question": question_id,
                "Text": question_text,
                "Answer": answer,
                "Textbook": textbook_src,
            })

    print(f"Answer generation complete. Output: {args.output_file}")


if __name__ == "__main__":
    main()
