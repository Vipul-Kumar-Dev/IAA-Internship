from django.contrib import admin
from .models import Infrastructure, Faculty, Course, Catering

class InfrastructureAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'infrastructure_name', 'quality', 'resources', 'maintenance', 'safety', 'satisfaction', 'description', 'submitted_at')
    search_fields = ('infrastructure_name', 'trainee__username')
    list_filter = ('quality', 'resources', 'maintenance', 'safety', 'satisfaction', 'submitted_at')

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'faculty_name', 'behavior', 'knowledge', 'interaction', 'clarity', 'response', 'examples', 'motivation', 'satisfaction', 'description', 'submitted_at')
    search_fields = ('faculty_name', 'trainee__username')
    list_filter = ('behavior', 'knowledge', 'interaction', 'clarity', 'response', 'examples', 'motivation', 'satisfaction', 'submitted_at')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'course_name', 'content', 'instructor', 'materials', 'satisfaction', 'description', 'submitted_at')
    search_fields = ('course_name', 'trainee__username')
    list_filter = ('content', 'instructor', 'materials', 'satisfaction', 'submitted_at')

class CateringAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'food_quality', 'service_quality', 'Cleanliness', 'Affordable', 'overall_satisfaction', 'description', 'submitted_at')
    search_fields = ('trainee__username',)
    list_filter = ('food_quality', 'service_quality', 'Cleanliness', 'Affordable', 'overall_satisfaction', 'submitted_at')

admin.site.register(Infrastructure, InfrastructureAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Catering, CateringAdmin)
