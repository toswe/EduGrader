import csv
from pathlib import Path
from typing import Tuple
import time
import yaml


ERROR_SCORE = -1

SCORING_INSTRUCTIONS = """

Tvoj odgovor treba da bude ocena studentskog odgovora u sledećem formatu:
Prvi red treba da sadrži samo broj na skali od 0 do 100, gde je 100 najbolja ocena a 0 najgora.
Ostatak odgovora treba da sadrži obrazloženje ocene.

"""


def load_prompt_config(prompt_file: str) -> dict:
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
    full_instructions = (instructions or "").strip() + "\n" + SCORING_INSTRUCTIONS

    last_text = ""
    last_full_response = None
    for attempt in range(max_retries):
        try:
            text, full_response = grader.prompt(
                prompt,
                model=model,
                instructions=full_instructions,
                temperature=temperature,
            )
            last_text, last_full_response = text, full_response
            score, explanation = parse_score_from_response(text)
            if score is not None:
                return score, explanation, str(full_response)
        except Exception as e:
            # transient API/connection error; backoff and retry
            last_text = f"ERROR: {e}"
            last_full_response = None
            if attempt < max_retries - 1:
                time.sleep(1.5 * (attempt + 1))
                continue
            break

    return ERROR_SCORE, last_text, str(last_full_response)


def write_with_additional_fields(in_file: Path, out_file: Path, extra_fields: list[str], row_updater):
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with in_file.open("r", encoding="utf-8") as fin, out_file.open(
        "w", newline="", encoding="utf-8"
    ) as fout:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + extra_fields
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            updated = row_updater(dict(row))
            writer.writerow(updated)
