from django.contrib import admin
from .models import User, Infrastructure, Faculty

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'firstname', 'phone_number')

class InfrastructureAdmin(admin.ModelAdmin):
    list_display = ('Trainee', 'infrastructure_name', 'description')

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('Trainee', 'faculty_name', 'rating', 'description')

admin.site.register(User, UserAdmin)
admin.site.register(Infrastructure, InfrastructureAdmin)
admin.site.register(Faculty, FacultyAdmin)