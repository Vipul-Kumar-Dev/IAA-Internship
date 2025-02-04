from django.contrib import admin
from .models import User, Infrastructure, Faculty, Course, Catering

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'phone_number')

class InfrastructureAdmin(admin.ModelAdmin):
    list_display = ('Trainee', 'infrastructure_name', 'rating', 'description', 'submitted_at')
    search_fields = ('infrastructure_name', 'Trainee__username')  # Allow search by infra name and trainee username
    list_filter = ('rating', 'submitted_at')
    def submitted_at(self, obj):
        return obj.created_at  # Assuming you have a 'created_at' field in the Faculty model
    submitted_at.admin_order_field = 'created_at'

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('Trainee', 'faculty_name', 'rating', 'description', 'submitted_at')
    search_fields = ('faculty_name', 'Trainee__username')
    list_filter = ('rating', 'submitted_at')
    def submitted_at(self, obj):
        return obj.created_at 
    submitted_at.admin_order_field = 'created_at'

class CourseAdmin(admin.ModelAdmin):
    list_display = ('Trainee', 'course_name', 'rating', 'description', 'submitted_at')
    search_fields = ('course_name', 'Trainee__username')
    list_filter = ('rating', 'submitted_at')
    def submitted_at(self, obj):
        return obj.created_at
    submitted_at.admin_order_field = 'created_at'

class CateringAdmin(admin.ModelAdmin):
    list_display = ('Trainee', 'catering_name', 'rating', 'description', 'submitted_at')
    search_fields = ('catering_name', 'Trainee__username')
    list_filter = ('rating', 'submitted_at')
    def submitted_at(self, obj):
        return obj.created_at
    submitted_at.admin_order_field = 'created_at'


admin.site.register(User, UserAdmin)
admin.site.register(Infrastructure, InfrastructureAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Catering, CateringAdmin)