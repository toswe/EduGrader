from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from backend.models import Question, Course, Test
from backend.serializers import QuestionSerializer, CourseSerializer, TestSerializer


class QuestionCRView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        course_pk = self.kwargs.get("pk")
        return Question.objects.filter(course_id=course_pk)

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
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CourseRView(
    GenericAPIView,
    RetrieveModelMixin,
    ListModelMixin,
):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        if kwargs.get("pk"):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class TestCRView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = TestSerializer

    def get_queryset(self):
        course_pk = self.kwargs.get("pk")
        return Test.objects.filter(course_id=course_pk)

    def perform_create(self, serializer):
        course_pk = self.kwargs.get("pk")

        course = Course.objects.get(pk=course_pk)
        questions = []

        serializer.save(course=course, questions=questions)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
