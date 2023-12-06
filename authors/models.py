from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
