from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    type = models.CharField(
        max_length=20,
        choices=[
            ("STUDENT", "Student"),
            ("PROFESSOR", "Professor"),
        ],
    )

    def is_student(self):
        return self.type == "STUDENT"

    def is_professor(self):
        return self.type == "PROFESSOR"
