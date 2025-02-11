from django import forms
from django.contrib.auth.models import User  # Use Django's built-in User model
from .models import Infrastructure, Faculty, Catering, Course

class InfrastructureForm(forms.ModelForm):
    class Meta:
        model = Infrastructure
        fields = ['trainee', 'infrastructure_name', 'rating', 'description']

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['trainee', 'faculty_name', 'rating', 'description']

class CateringForm(forms.ModelForm):
    class Meta:
        model = Catering
        fields = ['trainee', 'catering_name', 'rating', 'description']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['trainee', 'course_name', 'rating', 'description']
