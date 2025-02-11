from django.contrib import admin
from .models import Infrastructure, Faculty, Course, Catering

class InfrastructureAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'infrastructure_name', 'rating', 'description', 'submitted_at')
    search_fields = ('infrastructure_name', 'trainee__username')
    list_filter = ('rating', 'submitted_at')

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'faculty_name', 'rating', 'description', 'submitted_at')
    search_fields = ('faculty_name', 'trainee__username')
    list_filter = ('rating', 'submitted_at')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'course_name', 'rating', 'description', 'submitted_at')
    search_fields = ('course_name', 'trainee__username')
    list_filter = ('rating', 'submitted_at')

class CateringAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'catering_name', 'rating', 'description', 'submitted_at')
    search_fields = ('catering_name', 'trainee__username')
    list_filter = ('rating', 'submitted_at')

admin.site.register(Infrastructure, InfrastructureAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Catering, CateringAdmin)
