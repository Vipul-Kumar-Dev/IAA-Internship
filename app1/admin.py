from django.contrib import admin
from .models import User, Infrastructure, Faculty

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'firstname', 'phone_number')

class InfrastructureAdmin(admin.ModelAdmin):
    list_display = ('Trainee', 'infrastructure_name', 'description')

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('Trainee', 'faculty_name', 'rating', 'description', 'submitted_at')
    search_fields = ('faculty_name', 'trainee__username')
    list_filter = ('rating', 'submitted_at')
    def submitted_at(self, obj):
        return obj.created_at  # Assuming you have a 'created_at' field in the Faculty model
    submitted_at.admin_order_field = 'created_at'


admin.site.register(User, UserAdmin)
admin.site.register(Infrastructure, InfrastructureAdmin)
admin.site.register(Faculty, FacultyAdmin)