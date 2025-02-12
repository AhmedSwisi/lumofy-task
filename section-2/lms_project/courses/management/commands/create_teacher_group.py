from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course

class Command(BaseCommand):
    help = 'Creates the Teacher group with permissions for managing courses'

    def handle(self, *args, **kwargs):
        teacher_group, created = Group.objects.get_or_create(name='Teacher')
        course_content_type = ContentType.objects.get_for_model(Course)
        permissions = Permission.objects.filter(content_type=course_content_type)
        teacher_group.permissions.add(*permissions)

        self.stdout.write(self.style.SUCCESS(f"'Teacher' group created with the following permissions: {', '.join([perm.codename for perm in permissions])}"))
