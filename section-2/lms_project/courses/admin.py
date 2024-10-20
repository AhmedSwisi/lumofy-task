from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')  # Customize the displayed fields
    search_fields = ('title', 'description')  # Add search functionality by title and description
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate the slug field from the title
    list_filter = ('created_at',)  # Add filters for created_at field

# Register the Course model with the customized CourseAdmin class
admin.site.register(Course, CourseAdmin)