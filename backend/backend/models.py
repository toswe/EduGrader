from django.db import models


class Question(models.Model):
    question = models.TextField()
    awnser = models.TextField()
    course = models.ForeignKey("Course", on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=200)
