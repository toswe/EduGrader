import os
import csv
from django.core.management.base import BaseCommand, CommandError
from backend.models import Test, Question, StudentAnswer, StudentTest
from authentification.models import User


class Command(BaseCommand):
    help = "Import student test answers from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the CSV file")
        parser.add_argument("test_id", type=int, help="ID of the test")

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        test_id = options["test_id"]

        if not os.path.exists(csv_path):
            raise CommandError(f"The file {csv_path} does not exist.")

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise CommandError(f"Test with ID {test_id} does not exist.")

        self.stdout.write(self.style.SUCCESS(f"Using test: {test.name} (ID: {test.id})"))

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            folder_name = os.path.basename(os.path.dirname(csv_path))
            for row in reader:
                student_name_in_file = row["Student"]
                question_id = row["ID"]
                answer_text = row["Odgovor"]
                score = row["Broj poena"]

                student_name = f"{folder_name}_{student_name_in_file}"

                student, _ = User.objects.get_or_create(username=student_name)
                self.stdout.write(self.style.SUCCESS(f"Using student: {student.username} (ID: {student.id})"))

                student_test, _ = StudentTest.objects.get_or_create(student=student, test=test)

                try:
                    question = Question.objects.get(id=question_id)
                except Question.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Question not found: {question_id}"))
                    continue

                StudentAnswer.objects.create(
                    student=student,
                    test=student_test,
                    question=question,
                    question_text=question.question,
                    answer=answer_text,
                    score=score,
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported student answers."))
