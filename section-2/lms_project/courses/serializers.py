from rest_framework import serializers
from .models import Course, Lesson, LessonProgress, CourseEnrollment
from django.contrib.auth.models import User, Group


class RegistrationSerializer(serializers.ModelSerializer):
    # 'role' is not a field on the User model, but we'll use it for group assignment
    role = serializers.ChoiceField(choices=[('student', 'Student'), ('teacher', 'Teacher')], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}  # Make sure the password is write-only
        }

    def create(self, validated_data):
        # Pop the 'role' from validated data as it's not part of the User model
        role = validated_data.pop('role')
        
        # Create the user with the remaining validated data
        user = User.objects.create_user(**validated_data)

        # Assign the user to the appropriate group based on the 'role'
        if role == 'student':
            student_group, created = Group.objects.get_or_create(name='Students')
            student_group.user_set.add(user)
        elif role == 'teacher':
            teacher_group, created = Group.objects.get_or_create(name='Teacher')
            teacher_group.user_set.add(user)

        return user
class LessonSerializer(serializers.ModelSerializer):
    video = serializers.FileField(required=False, write_only=True)
    thumbnail = serializers.ImageField(required=False, write_only=True)
    class Meta:
        model = Lesson 
        fields = ['id', 'title','slug', 'content', 'order', 'video_url', 'thumbnail_url','video_duration','video','thumbnail']
        read_only_fields = ['slug','course','video_url', 'thumbnail_url']
    def validate_video(self, value):
        allowed_video_types = ['video/mp4', 'video/mpeg', 'video/quicktime']
        if value.content_type not in allowed_video_types:
            raise serializers.ValidationError('Only MP4, MPEG, and QuickTime video files are allowed.')
        return value

    def validate_thumbnail(self, value):
        allowed_image_types = ['image/jpeg', 'image/png', 'image/gif']
        if value.content_type not in allowed_image_types:
            raise serializers.ValidationError('Only JPEG, PNG, and GIF image files are allowed.')
        return value

class CourseSerialzier(serializers.ModelSerializer):
    teachers = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )
    lessons = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teachers', 'lessons']

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['student', 'is_completed','completed_at','watched_duration','id','lesson',]
        read_only_fields = ['student', 'completed_at','lesson']
    
class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = ['id', 'student', 'enrollment_date', 'is_completed', 'completion_date']
        read_only_fields = ['student', 'enrollment_date', 'course']