from rest_framework import serializers
from grading.models import AnswerGrade

class AnswerGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerGrade
        fields = "__all__"