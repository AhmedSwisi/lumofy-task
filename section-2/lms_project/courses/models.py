from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    teachers = models.ManyToManyField(User, related_name='courses')
    def save(self, *args, **kwargs):
            if not self.slug:
                slug_base = slugify(self.title)
                slug = slug_base
                num = 1
                while Course.objects.filter(slug=slug).exists():
                    slug = f"{slug_base}-{num}"
                    num += 1
                self.slug = slug
            super(Course, self).save(*args, **kwargs)
    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.IntegerField()
    video_url = models.URLField(max_length=500, blank=True, null=True)
    thumbnail_url = models.URLField(max_length=500, blank=True, null = True)
    video_duration = models.DurationField(null=True, blank=True)
    video = models.FileField(upload_to='lessons/videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='lessons/thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
            if not self.slug:
                slug_base = slugify(self.title)
                slug = slug_base
                num = 1
                while Lesson.objects.filter(slug=slug).exists():
                    slug = f"{slug_base}-{num}"
                    num += 1
                self.slug = slug
            super(Lesson, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class LessonProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched_duration = models.DurationField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null = True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'lesson'], name='unique_student_lesson_progress')
        ]
    def __str__(self):
        return f"{self.student.username}'s progress on {self.lesson.title}"

class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
