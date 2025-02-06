from django import forms
from .models import User, Infrastructure, Faculty, Catering, Course

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

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'rating', 'Trainee', 'description']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Ensure that `Trainee` is assigned as a `User` instance
        if isinstance(self.cleaned_data['Trainee'], User):
            instance.Trainee = self.cleaned_data['Trainee']
        else:
            raise ValueError("Trainee must be a User instance")
        if commit:
            instance.save()
        return instance