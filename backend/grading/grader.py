from grading.integrations import openai
from backend.models import StudentAnswer, Test, StudentTest
from grading.models import AnswerGrade

openai_grader = openai.OpenAI()

DEFAULT_INSTRUCTIONS = """
Ti si profesor visokog obrazovanja i treba da oceniš odgovor studenta na postavljeno pitanje.
Dobijaš odgovor studenta i pitanje na koje je student odgovarao, kao i tačan odgovor.
""".strip()
SCORING_INSTRUCTIONS = """

Tvoj odgovor treba da bude ocena studentskog odgovora u sledećem formatu:
Prvi red treba da sadrži samo broj na skali od 0 do 100, gde je 100 najbolja ocena a 0 najgora.
Ostatak odgovora treba da sadrži obrazloženje ocene.

"""
QUESTION_WRAPPER = """
Pitanje:
```
{question_text}
```
"""
CORRECT_ANSWER_WRAPPER = """
Tačan odgovor:
```
{correct_answer}
```
"""
STUDENT_ANSWER_WRAPPER = """
Odgovor studenta:
```
{student_answer}
```
"""


def _grade_answer(answer, instructions=DEFAULT_INSTRUCTIONS, **kwargs):
    instructions += SCORING_INSTRUCTIONS
    prompt = [
        QUESTION_WRAPPER.format(question_text=answer.question_text),
        CORRECT_ANSWER_WRAPPER.format(correct_answer=answer.question.answer),
        STUDENT_ANSWER_WRAPPER.format(student_answer=answer.answer),
    ].join("\n")

    result = openai_grader.prompt(prompt, instructions=instructions, **kwargs)
    score = int(result.output[0].content[0].text.split("\n")[0])

    AnswerGrade.objects.create(
        student_answer=answer,
        prompt=prompt,
        llm_response=result.to_dict(),
        score=score,
    )


def grade_student_test(student_test_id):
    student_answers = StudentAnswer.objects.filter(test=student_test_id)
    student_test = StudentTest.objects.get(id=student_test_id)

    for answer in student_answers:
        _grade_answer(answer, **student_test.test.configuration)


def grade_test(test_id):
    student_answers = StudentAnswer.objects.filter(test__test_id=test_id)
    test = Test.objects.get(id=test_id)

    for answer in student_answers:
        _grade_answer(answer, **test.configuration)
