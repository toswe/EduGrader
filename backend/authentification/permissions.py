from rest_framework.permissions import BasePermission


class IsProfessor(BasePermission):
    message = "Forbidden: Professors only."

    def has_permission(self, request, view):
        return request.user.is_professor()


class IsStudent(BasePermission):
    message = "Forbidden: Students only."

    def has_permission(self, request, view):
        return request.user.is_student()
