from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Rating validation function
def validate_rating(value):
    if value < 1 or value > 5:
        raise ValidationError(f"Rating must be between 1 and 5. You provided {value}.")

class Infrastructure(models.Model):
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    infrastructure_name = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(validators=[validate_rating])  
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.infrastructure_name} rated {self.rating}/5 by {self.trainee.username if self.trainee else 'Unknown'}"

class Faculty(models.Model):
    trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(validators=[validate_rating])  
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty_name} rated {self.rating}/5 by {self.trainee.username if self.trainee else 'Unknown'}"


class Course(models.Model):
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(validators=[validate_rating])
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name} rated {self.rating}/5 by {self.trainee.username if self.trainee else 'Unknown'}"

class Catering(models.Model):
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    catering_name = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(validators=[validate_rating])
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.catering_name} rated {self.rating}/5 by {self.trainee.username if self.trainee else 'Unknown'}"
