from rest_framework import serializers

from backend.models import Question, Course, Test


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ("course",)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"
        read_only_fields = ("course",)
        extra_kwargs = {"questions": {"required": False}}
