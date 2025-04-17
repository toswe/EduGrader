from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from backend.models import Question, Course, Test, StudentTest
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
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (IsAuthenticated,)
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

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

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
        print(user)
        return StudentTest.objects.filter(student=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class StudentTestRUDView(
#     GenericAPIView,
#     RetrieveModelMixin,
#     UpdateModelMixin,
#     DestroyModelMixin,
# ):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = StudentTestSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return StudentTest.objects.filter(student=user)

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class UpcomingTestsView(
    GenericAPIView,
    ListModelMixin,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = TestSerializer

    def get_queryset(self):
        user = self.request.user
        return Test.objects.filter(course__users=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
