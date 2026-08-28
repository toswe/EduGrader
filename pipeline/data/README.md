# Podaci

Studentski odgovori nisu deo javnog repozitorijuma (dostupni na zahtev, uz saglasnost nastavnika).
Ignorisani su kroz `.gitignore` i uklonjeni iz git istorije 26.08.2026.

Da bi `dvc repro` / `run_all_models.py` / `calculate_*.py` radili, u lokalnu kopiju treba staviti:

- `pipeline/data/<skup>/raw/student_answers.csv` (ulaz; `questions.csv` je u repou)
- `pipeline/data/<skup>/graded/graded.*.csv` (izlazi ocenjivanja; potrebni samo za `calculate_correlations.py` bez novih API poziva)
- `data/<skup>/results/gpt-4o.default.t-*.csv` u korenu (eksperiment sa temperaturom, `calculate_temperature.py`)
