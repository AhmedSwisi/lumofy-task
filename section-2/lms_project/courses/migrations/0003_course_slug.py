# Generated by Django 5.1.2 on 2024-10-19 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_lesson_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
