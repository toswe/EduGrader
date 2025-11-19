"""
Parses student test answer text files and converts them to CSV format.

Extracts question numbers, answers, and professor scores from structured
text files (P2T_*.txt) and outputs them to odgovori.csv for database import
and automated grading analysis.
"""
import os
import csv
import re

input_folder = "data/p2_jul_2"
output_csv = "data/p2_jul_2/odgovori.csv"

files = [f for f in os.listdir(input_folder) if f.startswith("P2T") and f.endswith(".txt")]

student_id = 1
rows = []

for filename in files:
    with open(os.path.join(input_folder, filename), encoding="utf-8") as f:
        lines = f.read().splitlines()
        content = "\n".join(lines[1:])
        print(f"Processing student {student_id}, file {filename}")

        # Improved regex: match question number, answer (greedy, up to br_poena), then score
        pattern = r"\n(\d+)\.\s*([\s\S]*?)(?:br_poena:\s*([\d\.]+))"
        matches = re.findall(pattern, content)
        fail = False
        if len(matches) != 12:
            print("Warning! failed to parse questions.")
            print(len(matches))
            fail = True
        for index, (qnum, qans, qscore) in enumerate(matches):
            qans = qans.strip()
            # Remove trailing question numbers or br_poena from answer if present
            qans = re.sub(r"\n*\d+\.\s*$", "", qans)
            if fail:
                print(qnum)
            rows.append([filename, student_id, qnum, qans, qscore])

    student_id += 1

with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Fajl", "Student", "Pitanje", "Odgovor", "Broj poena"])
    writer.writerows(rows)

print(f"Done! Output written to {output_csv}")
