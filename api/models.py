# employees/models.py
from django.db import models
from django.contrib.auth.hashers import make_password

class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'HR'),
        ('Engineer', 'Engineer'),
        ('Sales', 'Sales'),
    ]

    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Developer', 'Developer'),
        ('Analyst', 'Analyst'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    department = models.CharField(
        max_length=20,
        choices=DEPARTMENT_CHOICES,
        null=True,
        blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.pk is None:  # Only hash the password when creating a new employee
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Joined: {self.date_joined})"
