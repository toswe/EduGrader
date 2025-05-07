from grading.integrations import openai
from backend.models import StudentAnswer
from grading.models import AnswerGrade

openai_grader = openai.OpenAI()


def _grade_answer(answer):
    instructions = """
Ti si profesor visokog obrazovanja i treba da oceniš odgovor studenta na postavljeno pitanje.
Dobijaš odgovor studenta i pitanje na koje je student odgovarao, kao i tačan odgovor.
Na osnovu toga treba da oceniš odgovor studenta i da odgovoriš na sledeći način:
1. Ako je odgovor tačan, odgovori sa "T"
2. Ako je odgovor netačan, odgovori sa "N"
"""

    prompt = f"""
Pitanje:
```
{answer.question_text}
```

Tačan odgovor:
```
{answer.question.answer}
```

Odgovor studenta:
```
{answer.answer}
```
"""
    result = openai_grader.prompt(prompt, instructions=instructions)
    is_correct = result.output[0].content[0].text == "T"

    AnswerGrade.objects.create(
        student_answer=answer,
        is_correct=is_correct,
        llm_response=result.to_dict(),
    )


def grade_student_test(student_test_id):
    student_answers = StudentAnswer.objects.filter(test=student_test_id)

    for answer in student_answers:
        _grade_answer(answer)
