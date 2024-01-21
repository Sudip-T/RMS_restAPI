from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):

    username = None
    email = models.EmailField(max_length=100, unique=True)
    otp = models.CharField(max_length=5, blank=True, null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
