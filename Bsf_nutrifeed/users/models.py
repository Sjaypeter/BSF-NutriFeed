from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ("farmer", "Farmer"),
        ("admin", "Admin"),
        ("supervisor", "Supervisor"),
    ]

    role =models.CharField(max_length=20,choices=ROLE_CHOICES, default="farmer")
    phone_number =models.CharField(max_length=20, blank=True)
    farm_name = models.CharField(max_length=120, blank=True)
    farm_location = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-date_joined"]

    
    def __str__(self):
        return f"{self.username} ({self.role})"
    