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
    quality = models.PositiveSmallIntegerField(validators=[validate_rating])
    resources = models.PositiveSmallIntegerField(validators=[validate_rating])
    maintenance = models.PositiveSmallIntegerField(validators=[validate_rating])
    safety = models.PositiveSmallIntegerField(validators=[validate_rating])
    satisfaction = models.PositiveSmallIntegerField(validators=[validate_rating])
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        avg_rating = round((
            self.quality + self.resources + self.maintenance + 
            self.safety + self.satisfaction
        ) / 5, 2)
        
        return f"{self.infrastructure_name} rated {avg_rating}/5 by {self.trainee.username if self.trainee else 'Unknown'}"

class Faculty(models.Model):
    trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=255)
    behavior = models.PositiveSmallIntegerField(validators=[validate_rating])
    knowledge = models.PositiveSmallIntegerField(validators=[validate_rating])
    interaction = models.PositiveSmallIntegerField(validators=[validate_rating])
    clarity = models.PositiveSmallIntegerField(validators=[validate_rating])
    response = models.PositiveSmallIntegerField(validators=[validate_rating])
    examples = models.PositiveSmallIntegerField(validators=[validate_rating])
    motivation = models.PositiveSmallIntegerField(validators=[validate_rating])
    satisfaction = models.PositiveSmallIntegerField(validators=[validate_rating])
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        avg_rating = round((
            self.behavior + self.knowledge + self.interaction + 
            self.clarity + self.response + self.examples + 
            self.motivation + self.satisfaction
        ) / 8, 2)
        
        return f"{self.faculty_name} rated {avg_rating}/5 by {self.trainee.username if self.trainee else 'Unknown'}"


class Course(models.Model):
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=255)
    content = models.PositiveSmallIntegerField(validators=[validate_rating])
    instructor = models.PositiveSmallIntegerField(validators=[validate_rating])
    materials = models.PositiveSmallIntegerField(validators=[validate_rating])
    satisfaction = models.PositiveSmallIntegerField(validators=[validate_rating])
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        avg_rating = round((
            self.content + self.instructor + self.materials + self.satisfaction
        ) / 4, 2)
        
        return f"{self.course_name} rated {avg_rating}/5 by {self.trainee.username if self.trainee else 'Unknown'}"

class Catering(models.Model):
    trainee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    catering_name = models.CharField(max_length=255)
    food_quality = models.PositiveSmallIntegerField(validators=[validate_rating])
    service_quality = models.PositiveSmallIntegerField(validators=[validate_rating])
    Cleanliness = models.PositiveSmallIntegerField(validators=[validate_rating])
    Affordable = models.PositiveSmallIntegerField(validators=[validate_rating])
    overall_satisfaction = models.PositiveSmallIntegerField(validators=[validate_rating])
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        avg_rating = round((
            self.food_quality + self.service_quality + self.Cleanliness + self.Affordable + self.overall_satisfaction
        ) / 5, 2)
        
        return f"{self.catering_name} rated {avg_rating}/5 by {self.trainee.username if self.trainee else 'Unknown'}"