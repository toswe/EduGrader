from django.db import models

from backend.models import StudentAnswer


class AnswerGrade(models.Model):
    student_answer = models.ForeignKey(StudentAnswer, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    llm_response = models.JSONField(null=True, blank=True)
