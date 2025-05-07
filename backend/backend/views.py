from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from authentification.permissions import IsProfessor, IsStudent
from authentification.decorators import professor_route, student_route
from backend.models import Question, Course, Test, StudentTest, StudentAnswer
from backend.serializers import (
    QuestionSerializer,
    CourseSerializer,
    TestSerializer,
    TestQuestionsSerializer,
    StudentTestSerializer,
)


class CourseRView(
    GenericAPIView,
    RetrieveModelMixin,
    ListModelMixin,
):
    permission_classes = (IsAuthenticated, IsProfessor)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(users=user)

    def get(self, request, *args, **kwargs):
        if kwargs.get("pk"):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class QuestionCRView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin,
):
    permission_classes = (IsAuthenticated, IsProfessor)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        course_pk = self.kwargs.get("pk")
        user = self.request.user
        return Question.objects.filter(course_id=course_pk, course__users=user)

    def perform_create(self, serializer):
        course_pk = self.kwargs.get("pk")
        course = Course.objects.get(pk=course_pk)
        serializer.save(course=course)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class QuestionRUDView(
    GenericAPIView,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    permission_classes = (IsAuthenticated, IsProfessor)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user = self.request.user
        return Question.objects.filter(course__users=user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TestCRView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = TestSerializer

    def get_queryset(self):
        course_pk = self.kwargs.get("pk")
        user = self.request.user
        return Test.objects.filter(course_id=course_pk, course__users=user)

    def perform_create(self, serializer):
        course_pk = self.kwargs.get("pk")

        course = Course.objects.get(pk=course_pk)
        # questions = []

        # serializer.save(course=course, questions=questions)
        serializer.save(course=course)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @professor_route
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TestRUDView(
    GenericAPIView,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = TestSerializer

    def get_queryset(self):
        user = self.request.user
        return Test.objects.filter(course__users=user)

    def get(self, request, *args, **kwargs):
        if request.query_params.get("full_data", "false").lower() == "true":
            self.serializer_class = TestQuestionsSerializer

        return self.retrieve(request, *args, **kwargs)

    @professor_route
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @professor_route
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StudentTestCRView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentTestSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = StudentTest.objects.all()

        if test_id := self.request.query_params.get("test", False):
            queryset = queryset.filter(test_id=test_id)

        if course_id := self.request.query_params.get("course", False):
            queryset = queryset.filter(test__course_id=course_id)

        if user.is_student():
            return queryset.filter(student=user)

        courses = user.courses.all()
        return queryset.filter(test__course__in=courses)

    def _create_answers(self, student_test):
        # TODO This logic should be moved to a serializer.
        answers = self.request.data.get("answers", [])
        for answer_data in answers:
            question_id = answer_data.get("question")
            answer_text = answer_data.get("answer")
            if not question_id:
                continue

            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                continue

            StudentAnswer.objects.create(
                test=student_test,
                question=question,
                student=self.request.user,
                question_text=question.question,
                answer=answer_text,
            )

    def perform_create(self, serializer):
        test_pk = self.request.data.get("test")
        test = Test.objects.get(pk=test_pk)

        student_test = serializer.save(student=self.request.user, test=test)
        self._create_answers(student_test)

        # TODO This logic should be moved.
        from threading import Thread
        from grading.grader import grade_student_test

        Thread(target=grade_student_test, args=(student_test.id,)).start()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @student_route
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UpcomingTestsView(
    GenericAPIView,
    ListModelMixin,
):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = TestSerializer

    def get_queryset(self):
        user = self.request.user
        return Test.objects.filter(course__users=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
