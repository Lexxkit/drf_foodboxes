from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField(max_length=256, null=True)
    phone_number = models.CharField(max_length=16)
    address = models.CharField(max_length=1024)
