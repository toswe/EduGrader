from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def _check_user_type(method):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user
            has_permission = getattr(user, method)()

            if not has_permission:
                return Response(
                    {"detail": f"Forbidden: '{user.type}' user type cannot access this resource."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            return view_func(self, request, *args, **kwargs)

        return _wrapped_view

    return decorator


professor_route = _check_user_type("is_professor")
student_route = _check_user_type("is_student")
