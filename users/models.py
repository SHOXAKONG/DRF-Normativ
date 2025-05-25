from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email
