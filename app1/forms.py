from django import forms
from .models import User, Infrastructure, Faculty

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['firstname', 'email', 'username', 'password', 'phone_number']

class InfrastructureForm(forms.ModelForm):
    class Meta:
        model = Infrastructure
        fields = ['Trainee', 'infrastructure_name', 'rating', 'description']

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['Trainee', 'faculty_name', 'rating', 'description']