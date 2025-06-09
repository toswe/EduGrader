from django.core.management.base import BaseCommand, CommandError
from grading.grader import grade_test
from backend.models import Test


class Command(BaseCommand):
    help = "Grade all student answers for a given test ID"

    def add_arguments(self, parser):
        parser.add_argument("test_id", type=int, help="ID of the test to grade")

    def handle(self, *args, **options):
        test_id = options["test_id"]

        # Validate test
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise CommandError(f"Test with ID {test_id} does not exist.")

        self.stdout.write(self.style.SUCCESS(f"Grading test: {test.name} (ID: {test.id})"))

        # Call the grading function
        grade_test(test_id)

        self.stdout.write(
            self.style.SUCCESS("Successfully graded all student answers for the test.")
        )
