from django.db import models
from authentification.models import User


class Course(models.Model):
    users = models.ManyToManyField(User, related_name="courses")

    name = models.CharField(max_length=200)


class Question(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)

    question = models.TextField()
    answer = models.TextField()


class Test(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    questions = models.ManyToManyField("Question", related_name="tests")

    is_active = models.BooleanField(default=False)


class StudentTest(models.Model):
    student = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    test = models.ForeignKey(Test, null=True, on_delete=models.SET_NULL)

    awnsers = models.JSONField(default=list)
