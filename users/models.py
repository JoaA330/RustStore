from django.db import models
from django.contrib.auth.models import AbstractUser

class Status(models.TextChoices):
    CIVIL = "Civil", "Civil"
    WARRIOR = "Warrior", "Warrior"
    ARCHERY = "Archery", "Archery"
    WIZARD = "Wizard", "Wizard"




class User(AbstractUser):
    money = models.IntegerField(default=0)
    online = models.BooleanField(default=False)
    status = models.CharField( choices= Status.choices ,max_length=60, default=Status.CIVIL)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=60, null=True, blank=True)
