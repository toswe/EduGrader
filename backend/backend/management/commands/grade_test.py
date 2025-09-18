from django.core.management.base import BaseCommand, CommandError
from grading.grader import grade_test
from backend.models import Test
import csv


class Command(BaseCommand):
    help = "Grade all student answers for a given test ID"

    def add_arguments(self, parser):
        parser.add_argument("test_id", type=int, help="ID of the test to grade")

    def export_results(self, results):
        with open("tmp.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "student_id",
                "question_id",
                "correct_answer",
                "student_answer",
                "professor_score",
                "llm_score",
                "llm_response",
                "llm_response_raw",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for answer_grade in results:
                response = answer_grade.llm_response
                writer.writerow(
                    {
                        "student_id": answer_grade.student_answer.test.student.id,
                        "question_id": answer_grade.student_answer.question.id,
                        "correct_answer": answer_grade.student_answer.question.answer,
                        "student_answer": answer_grade.student_answer.answer,
                        "professor_score": answer_grade.student_answer.score,
                        "llm_score": answer_grade.score,
                        "llm_response": response["output"][0]["content"][0]["text"],
                        "llm_response_raw": response,
                    }
                )

    def handle(self, *args, **options):
        test_id = options["test_id"]

        # Validate test
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise CommandError(f"Test with ID {test_id} does not exist.")

        self.stdout.write(self.style.SUCCESS(f"Grading test: {test.name} (ID: {test.id})"))

        # Call the grading function
        result = grade_test(test_id, integration="openai", model="gpt-4o", instructions=None)

        self.stdout.write(
            self.style.SUCCESS("Successfully graded all student answers for the test.")
        )

        self.export_results(result)
