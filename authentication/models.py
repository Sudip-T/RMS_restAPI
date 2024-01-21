from django.db import models
# from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager



class CustomUser(AbstractUser):

    username = None
    email = models.EmailField(max_length=100, unique=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
