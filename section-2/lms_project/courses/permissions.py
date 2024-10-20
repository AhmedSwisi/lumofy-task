from rest_framework import permissions
from .models import Lesson

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to allow only teachers to create courses.
    """

    def has_permission(self, request, view):
        # Allow read-only access to all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is authenticated and belongs to the Teacher group
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Teacher').exists()


class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow teachers of a course to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # For lessons, check the related course's teachers
        if isinstance(obj, Lesson):
            return request.user in obj.course.teachers.all()

        # For courses, check the course's teachers
        return request.user in obj.teachers.all()
