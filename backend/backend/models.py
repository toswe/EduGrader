from django.db import models
from authentification.models import User


class Course(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, related_name="courses")


class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()
    course = models.ForeignKey("Course", on_delete=models.CASCADE)


class Test(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    questions = models.ManyToManyField("Question", related_name="tests")
