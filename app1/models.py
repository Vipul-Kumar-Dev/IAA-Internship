from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username


class Infrastructure(models.Model):
    Trainee = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-One Relationship
    infrastructure_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Infrastructure of {self.user.username}"

class Faculty(models.Model):
    Trainee = models.ForeignKey(User, on_delete=models.CASCADE)  # Student's username
    faculty_name = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=5, decimal_places=0)  # Rating out of 5.00
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty_name} rated {self.rating}/5 by {self.trainee.username}"