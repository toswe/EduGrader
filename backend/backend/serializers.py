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

    # def validate(self, data):
    #     questions = data.get("questions")
    #     course = self.instance.course

    #     if not all(q.course == course for q in questions):
    #         error_message = "All questions must belong to the same course as the test."
    #         raise serializers.ValidationError(error_message)

    #     return data
