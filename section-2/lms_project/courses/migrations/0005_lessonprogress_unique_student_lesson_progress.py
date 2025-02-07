# Generated by Django 5.1.2 on 2024-10-19 17:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_courseenrollment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='lessonprogress',
            constraint=models.UniqueConstraint(fields=('student', 'lesson'), name='unique_student_lesson_progress'),
        ),
    ]
