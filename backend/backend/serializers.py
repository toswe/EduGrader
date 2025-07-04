from rest_framework import serializers

from backend.models import Question, Course, Test, StudentAnswer, StudentTest
from grading.serializers import AnswerGradeSerializer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ("course",)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if (
            (request := self.context.get("request"))
            and hasattr(request, "user")
            and request.user.is_professor()
        ):
            return data

        data["answer"] = ""
        return data


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

    # TODO Validation.
    # def validate(self, data):
    #     questions = data.get("questions")
    #     course = self.instance.course

    #     if not all(q.course == course for q in questions):
    #         error_message = "All questions must belong to the same course as the test."
    #         raise serializers.ValidationError(error_message)

    #     return data


class TestQuestionsSerializer(TestSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["questions"] = QuestionSerializer(many=True, read_only=True)


class StudentAnswerSerializer(serializers.ModelSerializer):
    grades = AnswerGradeSerializer(many=True, read_only=True)

    class Meta:
        model = StudentAnswer
        fields = "__all__"
        read_only_fields = (
            "student_test",
            "question",
        )


class StudentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTest
        fields = "__all__"
        read_only_fields = (
            "student",
            "test",
        )

class StudentTestAnswersSerializer(StudentTestSerializer):
    answers = StudentAnswerSerializer(many=True, read_only=True)
