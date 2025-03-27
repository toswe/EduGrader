from django.db import models


class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()
    course = models.ForeignKey("Course", on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=200)


class Test(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    questions = models.ManyToManyField("Question", related_name="tests")
