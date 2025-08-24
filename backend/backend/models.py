from django.db import models
from authentification.models import User


class Course(models.Model):
    users = models.ManyToManyField(User, related_name="courses")

    name = models.CharField(max_length=200)


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    question = models.TextField()
    answer = models.TextField()


class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question, related_name="tests")
    configuration = models.JSONField(default=dict, blank=True)

    is_active = models.BooleanField(default=False)


class StudentTest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, null=True, on_delete=models.SET_NULL)


class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(StudentTest, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)

    question_text = models.TextField()
    answer = models.TextField()

    score = models.FloatField(null=True, blank=True)
