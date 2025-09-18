from grading.integrations.factory import get_integration
from backend.models import StudentAnswer, Test, StudentTest
from grading.models import AnswerGrade

DEFAULT_INSTRUCTIONS = """
Ti si profesor visokog obrazovanja i treba da oceniš odgovor studenta na postavljeno pitanje.
Dobijaš odgovor studenta i pitanje na koje je student odgovarao, kao i tačan odgovor.
""".strip()
HARD_INSTRUCTIONS = """
Ti si strog profesor visokoakademske institucije i treba da ocenis odgovore studenata.
Dobijas pitanje, tacan odgovor kao i odgovor studenta,
i treba da proveris da li je odgovor studenta adekvatan.
Svako nepoklapanje se kaznjava sa oduzimanjem petine ukupnih poena.
Fokusiraj se na stavke koje se ne poklapaju sa studentovim odgovorom.
""".strip()
SOFT_INSTRUCTIONS = """
Ti si blag profesor visokog obrazovanja i treba da ocenis odgovore studenata.
Dobijas pitanje, tacan odgovor kao i odgovor studenta,
i treba da proveris da li je odgovor studenta adekvatan.
Fokusiraj se na stavke koje se poklapaju sa studentovim odgovorom.
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


def _grade_answer(
    answer,
    grader,
    instructions=DEFAULT_INSTRUCTIONS,
    use_correct_answer=True,
    **kwargs,
):
    instructions += SCORING_INSTRUCTIONS

    question = QUESTION_WRAPPER.format(question_text=answer.question_text)
    correct_answer = CORRECT_ANSWER_WRAPPER.format(correct_answer=answer.question.answer)
    student_answer = STUDENT_ANSWER_WRAPPER.format(student_answer=answer.answer)

    prompt = "\n".join(
        [
            question,
            *([correct_answer] if use_correct_answer else []),
            student_answer,
        ]
    )

    print(f"Grading {answer.id}")
    result, response = grader.prompt(prompt, instructions=instructions, **kwargs)

    try:
        score = int(result.split("\n")[0])
    except ValueError:
        raise ValueError("Failed to parse score from the response.")

    return AnswerGrade.objects.create(
        student_answer=answer,
        prompt=prompt,
        instructions=instructions,
        llm_response=response,
        score=score,
    )


def _grade_answers(
    student_answers,
    integration="openai",
    model="gpt-4o",
    instructions=DEFAULT_INSTRUCTIONS,
):
    grader = get_integration(integration)
    return [
        _grade_answer(
            answer,
            grader=grader,
            instructions=instructions,
            model=model,
        )
        for answer in student_answers
    ]


def grade_student_test(student_test_id):
    student_answers = StudentAnswer.objects.filter(test=student_test_id)
    student_test = StudentTest.objects.get(id=student_test_id)

    print(f"Grading student test {student_test.id} for {student_answers.count()} answers")
    return _grade_answers(student_answers, student_test.test)


def grade_test(
    test_id,
    integration,
    model,
    instructions,
):
    student_answers = StudentAnswer.objects.filter(test__test_id=test_id)

    print(f"Grading test {test_id} for {student_answers.count()} answers")
    return _grade_answers(
        student_answers,
        integration=integration,
        model=model,
        instructions=instructions,
    )
