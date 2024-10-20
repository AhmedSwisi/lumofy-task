from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Course, Lesson, LessonProgress, CourseEnrollment
from .serializers import CourseSerialzier, LessonProgressSerializer, LessonSerializer, RegistrationSerializer, CourseEnrollmentSerializer
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTeacherOrReadOnly, IsTeacher
from django.utils.text import slugify
from rest_framework.exceptions import PermissionDenied, NotFound
from django.utils.timezone import now
from django.db.models import Count, Case, When, IntegerField
import boto3
from botocore.config import Config
import os
from botocore.exceptions import ClientError

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL for uploading a file to Cloudflare R2.
    """
    s3_client = boto3.client(
        's3',
        endpoint_url=os.getenv('R2_PUBLIC_ENDPOINT'),
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
    )

    try:
        response = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "message": "User registered successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzier
    permission_classes=[IsAuthenticated, IsTeacherOrReadOnly ]
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsTeacher] 
        else:
            self.permission_classes = [IsAuthenticated, IsTeacherOrReadOnly] 
        return super(CourseViewSet, self).get_permissions()
    

    def perform_create(self, serializer):
        course = serializer.save()
        course.teachers.add(self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        if 'title' in serializer.validated_data:
            course.slug = slugify(serializer.validated_data['title'])

            base_slug = course.slug
            num = 1
            while Course.objects.filter(slug=course.slug).exclude(pk=course.pk).exists():
                course.slug = f"{base_slug}-{num}"
                num += 1

            course.save()
    
    def get_queryset(self):
        if self.request.user.groups.filter(name='Teacher').exists():
            return self.queryset.filter(teachers=self.request.user)
        return self.queryset
    
    def destroy(self, request, *args, **kwargs):
        course = self.get_object()
        self.perform_destroy(course)
        return Response({"detail": "Course deleted successfully."}, status=status.HTTP_200_OK)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]
    lookup_field = 'slug'  

    def shift_lessons(self, course, order):
        """
        Shift the order of the lessons in the course if the order already exists.
        All lessons with an order >= the new lesson's order will be shifted by 1.
        """
        lessons_to_shift = Lesson.objects.filter(course=course, order__gte=order).order_by('order')
        for lesson in lessons_to_shift:
            lesson.order += 1
            lesson.save()

    def get_queryset(self):
        """
        Return lessons for the courses the teacher has created.
        """
        queryset = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name='Teacher').exists():
            return queryset.filter(course__teachers=user)
        return queryset.none()

    def perform_create(self, serializer):
        """
        Handle the file upload and save the lesson with the video and thumbnail URL.
        """
        try:
            course = Course.objects.get(slug=self.kwargs['course_slug'])
        except Course.DoesNotExist:
            raise NotFound("Course not found.")
        
        if not self.request.user in course.teachers.all():
            raise PermissionDenied("You are not allowed to add lessons to this course.")

        lesson = serializer.save(course=course)

        video_file = self.request.FILES.get('video')
        if video_file:
            lesson.video_url = self.upload_to_r2(video_file, f'lessons/videos/{lesson.slug}.mp4')

        thumbnail_file = self.request.FILES.get('thumbnail')
        if thumbnail_file:
            lesson.thumbnail_url = self.upload_to_r2(thumbnail_file, f'lessons/thumbnails/{lesson.slug}.jpg')

        lesson.save()

    def upload_to_r2(self, file, file_path):
        """
        Upload a file to Cloudflare R2 and return a presigned URL for the file.
        """
        config = Config(
            signature_version='s3v4', 
            retries={'max_attempts': 10, 'mode': 'standard'}
        )
        
        s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv('R2_PUBLIC_ENDPOINT'),
            aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
            config=config
        )

        content_type = file.content_type  

        s3_client.upload_fileobj(
            file,
            os.getenv('R2_BUCKET_NAME'),
            file_path,
            ExtraArgs={'ContentType': content_type}
        )

        # Generate a presigned URL valid for 1 hour (3600 seconds)
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': os.getenv('R2_BUCKET_NAME'),
                'Key': file_path
            },
            ExpiresIn=3600  
        )

        return presigned_url

    def perform_update(self, serializer):
        """
        Generate and update presigned URLs for video and thumbnail if necessary.
        """
        lesson = self.get_object()
        if not self.request.user in lesson.course.teachers.all():
            raise PermissionDenied("You are not allowed to update lessons in this course.")

        updated_lesson = serializer.save()

        if 'video' in self.request.FILES:
            updated_lesson.video_url = generate_presigned_url(bucket_name=os.getenv('R2_BUCKET_NAME'), object_name=f'lessons/videos/{updated_lesson.slug}.mp4')
        if 'thumbnail' in self.request.FILES:
            updated_lesson.thumbnail_url = generate_presigned_url(bucket_name=os.getenv('R2_BUCKET_NAME'), object_name=f'lessons/thumbnails/{updated_lesson.slug}.jpg')
        
        updated_lesson.save()

class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict the queryset to only the student's own progress for a specific lesson.
        """
        lesson_slug = self.kwargs['lesson_slug']  
        user = self.request.user

        if user.groups.filter(name='Students').exists():
            try:
                lesson = Lesson.objects.get(slug=lesson_slug)
            except Lesson.DoesNotExist:
                raise NotFound("Lesson not found.")
            
            return LessonProgress.objects.filter(student=user, lesson=lesson)
        
        return LessonProgress.objects.none()

    def perform_create(self, serializer):
        """
        Automatically assign the student to the lesson progress record.
        If progress already exists for the student and lesson, update it.
        """
        lesson_slug = self.kwargs['lesson_slug']
        try:
            lesson = Lesson.objects.get(slug=lesson_slug)
        except Lesson.DoesNotExist:
            raise NotFound("Lesson not found.")
        
        if not self.request.user.groups.filter(name='Students').exists():
            raise PermissionDenied("Only students can track lesson progress.")
        
        existing_progress = LessonProgress.objects.filter(student=self.request.user, lesson=lesson).first()

        if existing_progress:
            serializer.update(existing_progress, serializer.validated_data)
        else:
            lesson_progress = serializer.save(student=self.request.user, lesson=lesson)
        
        if existing_progress and existing_progress.is_completed and not existing_progress.completed_at:
            existing_progress.completed_at = now()
            existing_progress.save()
        elif not existing_progress and lesson_progress.is_completed and not lesson_progress.completed_at:
            lesson_progress.completed_at = now()
            lesson_progress.save()

class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically enroll the student in the course.
        """
        try:
            course = Course.objects.get(slug=self.kwargs['course_slug'])
        except Course.DoesNotExist:
            raise NotFound("Course not found.")

        if CourseEnrollment.objects.filter(student=self.request.user, course=course).exists():
            raise PermissionDenied("You are already enrolled in this course.")
        
        serializer.save(student=self.request.user, course=course)

class CourseProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_slug):
        """
        Return the total progress percentage of all students enrolled in a given course.
        """
        try:
            course = Course.objects.get(slug=course_slug)
        except Course.DoesNotExist:
            raise NotFound("Course not found.")

        if not request.user in course.teachers.all():
            raise PermissionDenied("You are not allowed to view progress for this course.")

        total_lessons = course.lessons.count()

        if total_lessons == 0:
            return Response({"detail": "This course has no lessons."})

        progress = (
            LessonProgress.objects.filter(lesson__course=course)
            .values('student')
            .annotate(
                completed_lessons=Count(Case(When(is_completed=True, then=1), output_field=IntegerField()))
            )
            .annotate(total_lessons=Count('lesson'))
        )

        progress_data = [
            {
                "student_id": p['student'],
                "completed_lessons": p['completed_lessons'],
                "total_lessons": total_lessons,
                "progress_percentage": round((p['completed_lessons'] / total_lessons) * 100, 2)
            }
            for p in progress
        ]

        return Response(progress_data)

class StudentCourseProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_slug):
        """
        Return the total progress percentage for the logged-in student in a given course.
        """
        try:
            course = Course.objects.get(slug=course_slug)
        except Course.DoesNotExist:
            raise NotFound("Course not found.")

        if not request.user.groups.filter(name='Students').exists():
            raise PermissionDenied("Only students can view their progress.")

        total_lessons = course.lessons.count()

        if total_lessons == 0:
            return Response({"detail": "This course has no lessons."})

        student_progress = LessonProgress.objects.filter(student=request.user, lesson__course=course)

        completed_lessons = student_progress.filter(is_completed=True).count()

        progress_percentage = round((completed_lessons / total_lessons) * 100, 2)

        return Response({
            "student_id": request.user.id,
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
            "progress_percentage": progress_percentage
        })
    

