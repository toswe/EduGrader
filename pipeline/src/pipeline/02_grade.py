import argparse
import csv
import json
import sys
from pathlib import Path
import yaml
from dotenv import load_dotenv

# Add the workspace root to Python path so we can import from backend
def add_workspace_to_path():
    workspace_root = Path(__file__).resolve().parents[3]
    if str(workspace_root) not in sys.path:
        sys.path.insert(0, str(workspace_root))
add_workspace_to_path()

from backend.grading.integrations.factory import get_integration

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
    return f"""Pitanje:\n```
{question_text}
```
\nTačan odgovor:\n```
{correct_answer}
```
\nOdgovor studenta:\n```
{student_answer}
```
"""

def parse_score_from_response(response_text: str):
    try:
        first_line, explanation = response_text.split("\n", 1)
        score = int(first_line.strip())
        return score, explanation.strip()
    except (ValueError, TypeError):
        return None, response_text

def grade_answer(question, correct_answer, student_answer, integration_name, model, instructions, temperature=0, max_retries=3):
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
    raw = json.dumps(full_response, ensure_ascii=False, default=str)
    return -1, text, raw

def grade_merged_csv(merged_path: Path, output_path: Path, integration_name: str, model: str, instructions: str, temperature: float = 0):
    with merged_path.open("r", encoding="utf-8") as fin, output_path.open("w", newline="", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ["llm_score", "llm_explanation", "llm_response_raw"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            llm_score, llm_explanation, llm_response_raw = grade_answer(
                row["question_text"],
                row["correct_answer"],
                row["student_answer"],
                integration_name,
                model,
                instructions,
                temperature,
            )
            row.update({
                "llm_score": llm_score,
                "llm_explanation": llm_explanation,
                "llm_response_raw": llm_response_raw,
            })
            writer.writerow(row)

def main():
    workspace_root = Path(__file__).resolve().parents[3]
    dotenv_path = workspace_root / ".env.dev"
    if dotenv_path.is_file():
        load_dotenv(dotenv_path, override=False)
    parser = argparse.ArgumentParser(description="Grade merged student answers CSV using an LLM")
    parser.add_argument("--in", dest="input_file", required=True, help="Path to merged input CSV")
    parser.add_argument("--out", dest="output_file", required=True, help="Path to output graded CSV")
    parser.add_argument("--model", dest="model_param", required=True)
    parser.add_argument("--prompt_file", required=True)
    args = parser.parse_args()
    model_cfg = load_model_config(args.model_param)
    instructions = load_prompt(args.prompt_file)
    grade_merged_csv(
        Path(args.input_file),
        Path(args.output_file),
        model_cfg["integration"],
        model_cfg["model"],
        instructions,
        model_cfg["temperature"],
    )
    print(f"Grading complete. Output: {args.output_file}")

if __name__ == "__main__":
    main()
