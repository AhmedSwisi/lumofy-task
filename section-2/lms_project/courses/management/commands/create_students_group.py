from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course  # Replace 'your_app' with the name of your app

class Command(BaseCommand):
    help = 'Creates the Students group with permissions for viewing courses'

    def handle(self, *args, **kwargs):
        students_group, created = Group.objects.get_or_create(name='Students')
        course_content_type = ContentType.objects.get_for_model(Course)
        view_course_permission = Permission.objects.get(codename='view_course', content_type=course_content_type)
        students_group.permissions.add(view_course_permission)
        self.stdout.write(self.style.SUCCESS(f"'Students' group created with permission to view courses"))
