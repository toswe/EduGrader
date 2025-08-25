import random

from django.core.management.base import BaseCommand

from backend.models import Test, StudentTest, StudentAnswer
from authentification.models import User
from grading.integrations.gemini import Gemini


class Command(BaseCommand):
    help = """
This command takes a test ID, an optional student ID and na optional glag to generate false answers.

If the student ID is provided, it simulates answering the test for that student.
If no student ID is provided, it creates a mock student and simulates answering the test for that student.

The command uses the Gemini LLM Integration to generate mock answers for each question in the test.

    """

    def add_arguments(self, parser):
        parser.add_argument("test_id", type=int, help="ID of the test to simulate")
        parser.add_argument(
            "--student_id",
            type=int,
            help="Optional ID of the student to simulate answering the test for",
        )

    def _simulate_student_test(self, student, test):
        questions = test.questions.all()
        gemini = Gemini()

        # Create a StudentTest instance
        student_test, created = StudentTest.objects.get_or_create(student=student, test=test)

        print(f"Simulating test for student: {student.username} on test: {test.name}")
        print()
        print()
        print()
        print()
        print("#######################################")

        print(questions)
        print(len(questions))
        print()
        print()
        print()

        for question in questions:
            print(f"Simulating answer for question: {question.question}")
            response, _ = gemini.prompt(
                question.question + f"(Odgovoriti u manje od 100 reči, jednostavno formatirano.)"
            )
            print(f"Generated response: {response}")
            print()
            print("---------------")
            print()
            StudentAnswer.objects.create(
                student=student,
                test=student_test,
                question=question,
                question_text=question.question,
                answer=response,
            )

        print(f"Simulated answers for student {student.username} on test {test.name}.")

    def handle(self, *args, **options):
        test_id = options["test_id"]
        student_id = options.get("student_id")

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Test with ID {test_id} does not exist."))
            return

        if student_id:
            student = User.objects.get(id=student_id)
        else:
            student = User.objects.create(
                username=f"mock_student_{random.randint(1, 1000000)}",
                type="STUDENT",
            )

        self._simulate_student_test(student, test)
