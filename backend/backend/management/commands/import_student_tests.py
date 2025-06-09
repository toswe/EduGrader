import os
import csv
from django.core.management.base import BaseCommand, CommandError
from backend.models import Test, Question, StudentAnswer, StudentTest
from authentification.models import User  # Import User model


class Command(BaseCommand):
    help = "Import student tests from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the CSV file")
        parser.add_argument("test_id", type=int, help="ID of the test")

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        test_id = options["test_id"]

        if not os.path.exists(csv_path):
            raise CommandError(f"The file {csv_path} does not exist.")

        # Validate test
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise CommandError(f"Test with ID {test_id} does not exist.")

        self.stdout.write(self.style.SUCCESS(f"Using test: {test.name} (ID: {test.id})"))

        # Extract student name from filename
        student_name = os.path.splitext(os.path.basename(csv_path))[0]

        # Create or get the student
        student, _ = User.objects.get_or_create(username=student_name)
        self.stdout.write(
            self.style.SUCCESS(f"Using student: {student.username} (ID: {student.id})")
        )

        # Read CSV and create student answers
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != 2:
                    self.stdout.write(self.style.WARNING(f"Skipping invalid row: {row}"))
                    continue

                question_text, answer_text = row

                # Match question by text
                try:
                    question = Question.objects.get(question=question_text, course=test.course)
                except Question.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"Question not found for text: {question_text}")
                    )
                    continue

                # Create StudentAnswer
                student_test, _ = StudentTest.objects.get_or_create(student=student, test=test)
                StudentAnswer.objects.create(
                    student=student,
                    test=student_test,
                    question=question,
                    question_text=question_text,
                    answer=answer_text,
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported student answers."))
