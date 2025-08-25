from django.db import models

from backend.models import StudentAnswer


class AnswerGrade(models.Model):
    student_answer = models.ForeignKey(StudentAnswer, on_delete=models.CASCADE, related_name="grades")
    instructions = models.TextField(null=True, blank=True)
    prompt = models.TextField(null=True, blank=True)
    llm_response = models.JSONField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
