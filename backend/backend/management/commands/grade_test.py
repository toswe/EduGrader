from django.core.management.base import BaseCommand, CommandError
from grading.grader import grade_test, HARD_INSTRUCTIONS, DEFAULT_INSTRUCTIONS, SOFT_INSTRUCTIONS
from backend.models import Test
import csv

INSTRUCTIONS_MAP = {
    DEFAULT_INSTRUCTIONS: "default",
    HARD_INSTRUCTIONS: "hard",
    SOFT_INSTRUCTIONS: "soft",
}
CONFIGS = [
    {
        "integration": "deepseek",
        "model": "deepseek-chat",
        "instructions": DEFAULT_INSTRUCTIONS,
    },
    {
        "integration": "openai",
        "model": "gpt-4o-mini",
        "instructions": DEFAULT_INSTRUCTIONS,
    },
    {
        "integration": "openai",
        "model": "gpt-5",
        "instructions": DEFAULT_INSTRUCTIONS,
    },
]

class Command(BaseCommand):
    help = "Grade all student answers for a given test ID"

    def add_arguments(self, parser):
        parser.add_argument("test_id", type=int, help="ID of the test to grade")

    def export_results(self, results, path):
        with open(path, "w", newline="", encoding="utf-8") as csvfile:
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
                try:
                    response_text = response["output"][0]["content"][0]["text"]
                except (KeyError, IndexError):
                    response_text = "N/A"
                writer.writerow(
                    {
                        "student_id": answer_grade.student_answer.test.student.id,
                        "question_id": answer_grade.student_answer.question.id,
                        "correct_answer": answer_grade.student_answer.question.answer,
                        "student_answer": answer_grade.student_answer.answer,
                        "professor_score": answer_grade.student_answer.score,
                        "llm_score": answer_grade.score,
                        "llm_response": response_text,
                        "llm_response_raw": response,
                    }
                )

    def grade_using_config(self, test_id, config):
        integration = config["integration"]
        model = config["model"]
        instructions = config["instructions"]

        self.stdout.write(f"Using config: {config}")
        result = grade_test(
            test_id, integration=integration, model=model, instructions=instructions
        )

        self.stdout.write(self.style.SUCCESS("Successfully graded all student answers."))

        path = f"result.{integration}.{model}.{INSTRUCTIONS_MAP[instructions]}.csv"
        self.export_results(result, path)

    def handle(self, *args, **options):
        test_id = options["test_id"]

        # Validate test
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise CommandError(f"Test with ID {test_id} does not exist.")

        self.stdout.write(self.style.SUCCESS(f"Grading test: {test.name} (ID: {test.id})"))

        for config in CONFIGS:
            try:
                self.grade_using_config(test_id, config)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error grading with config {config}: {e}"))
