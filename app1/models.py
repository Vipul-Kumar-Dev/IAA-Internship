from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, firstname=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, firstname=firstname)
        user.set_password(password)
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)  # Add this line if missing
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

def validate_rating(value):
    if value < 1 or value > 5:
        raise ValidationError(f"Rating must be between 1 and 5. You provided {value}.")

class Infrastructure(models.Model):
    Trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    infrastructure_name = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=5, 
        decimal_places=0,
        validators=[validate_rating]
    )
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.infrastructure_name} rated {self.rating}/5 by {self.Trainee.username}"

class Faculty(models.Model):
    Trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=5, 
        decimal_places=0, 
        validators=[validate_rating]
    )
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty_name} rated {self.rating}/5 by {self.Trainee.username}"
    
class Course(models.Model):
    Trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=5, 
        decimal_places=0, 
        validators=[validate_rating]
    )
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name} rated {self.rating}/5 by {self.Trainee.username}"
    
class Catering(models.Model):
    Trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    catering_name = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=5, 
        decimal_places=0, 
        validators=[validate_rating]
    )
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.catering_name} rated {self.rating}/5 by {self.Trainee.username}"