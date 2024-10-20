"""
URL configuration for lms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from courses.views import CourseViewSet, LessonProgressViewSet, RegisterView, LessonViewSet, CourseEnrollmentViewSet, CourseProgressView, StudentCourseProgressView
from courses.section_3 import register_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'courses',CourseViewSet,basename='course')

lessons_router = routers.NestedDefaultRouter(router, r'courses', lookup='course')
lessons_router.register(r'lessons', LessonViewSet, basename='lesson')

# Nested router for lesson progress under lessons
progress_router = routers.NestedDefaultRouter(lessons_router, r'lessons', lookup='lesson')
progress_router.register(r'progress', LessonProgressViewSet, basename='lesson-progress')

api_urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('bad-register/', register_user, name='register_user'),
    path('', include(router.urls)),
    path('', include(lessons_router.urls)),
    path('', include(progress_router.urls)),
    path('courses/<slug:course_slug>/lessons/<slug:lesson_slug>/progress/', LessonProgressViewSet.as_view({'post': 'create'}), name='lesson-progress'),
    path('courses/<slug:course_slug>/enroll/', CourseEnrollmentViewSet.as_view({'post': 'create'}), name='course-enrollment'),
    path('courses/<slug:course_slug>/progress/', CourseProgressView.as_view(), name='course-progress'),
    path('courses/<slug:course_slug>/my-progress/', StudentCourseProgressView.as_view(), name='student-course-progress'),
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),  # Group all API routes under 'api/'
    path('admin/', admin.site.urls),  # Admin doesn't need 'api/' prefix
]

