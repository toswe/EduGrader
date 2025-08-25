import os
import csv
from django.core.management.base import BaseCommand, CommandError
from backend.models import Course, Question, Test


class Command(BaseCommand):
    help = "Import tests from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        csv_path = options["csv_path"]

        if not os.path.exists(csv_path):
            raise CommandError(f"The file {csv_path} does not exist.")

        course_name = os.path.basename(os.path.dirname(csv_path))
        course, created = Course.objects.get_or_create(name=course_name)

        self.stdout.write(self.style.SUCCESS(f"Using course: {course.name} (ID: {course.id})"))

        # Read CSV and create questions
        questions = []
        updated_rows = []
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames

            if "ID" not in fieldnames:
                fieldnames.append("ID")

            for row in reader:
                if "ID" in row:
                    # TODO Update existing question if needed
                    updated_rows.append(row)
                    continue

                question_text = row.get("Tekst")
                answer_text = row.get("Tačan odgovor")

                if not question_text or not answer_text:
                    self.stdout.write(self.style.WARNING(f"Skipping invalid row: {row}"))
                    updated_rows.append(row)
                    continue

                question = Question.objects.create(
                    course=course, question=question_text, answer=answer_text
                )
                questions.append(question)  # Add the created question to the list
                row["ID"] = question.id
                updated_rows.append(row)

        # Write back to the CSV file with updated IDs
        with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

        if not questions:
            raise CommandError("No valid questions found in the CSV file.")

        # Create test
        test_name = f"Test for {course.name}"
        test = Test.objects.create(course=course, name=test_name)
        test.questions.set(questions)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created test '{test.name}' (ID: {test.id}) with {len(questions)} questions."
            )
        )

        return test
