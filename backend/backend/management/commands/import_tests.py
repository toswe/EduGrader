import os
import csv
from django.core.management.base import BaseCommand, CommandError
from backend.models import Course, Question, Test


class Command(BaseCommand):
    help = "Import tests from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the CSV file")
        parser.add_argument("--course_id", type=int, help="Optional course ID")

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        course_id = options.get("course_id")

        if not os.path.exists(csv_path):
            raise CommandError(f"The file {csv_path} does not exist.")

        # Determine course
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                raise CommandError(f"Course with ID {course_id} does not exist.")
        else:
            course_name = os.path.splitext(os.path.basename(csv_path))[0]
            course = Course.objects.create(name=course_name)

        self.stdout.write(self.style.SUCCESS(f"Using course: {course.name} (ID: {course.id})"))

        # Read CSV and create questions
        questions = []
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != 2:
                    self.stdout.write(self.style.WARNING(f"Skipping invalid row: {row}"))
                    continue

                question_text, answer_text = row
                question = Question.objects.create(
                    course=course, question=question_text, answer=answer_text
                )
                questions.append(question)

        if not questions:
            raise CommandError("No valid questions found in the CSV file.")

        # Create test
        test_name = f"Test for {course.name}"
        test = Test.objects.create(course=course, name=test_name)
        test.questions.set(questions)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created test '{test.name}' with {len(questions)} questions."
            )
        )
