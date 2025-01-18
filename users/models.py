from django.db import models

class Status(models.TextChoices):
    CIVIL = "Civil", "Civil"
    WARRIOR = "Warrior", "Warrior"
    ARCHERY = "Archery", "Archery"
    WIZARD = "Wizard", "Wizard"




class User(models.Model):
    userName = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=60)
    money = models.IntegerField()
    name = models.CharField(max_length=80)
    online = models.BooleanField(default=False)
    lastname = models.CharField(max_length=90)
    u_status = models.CharField( choices= Status.choices ,max_length=60, default="Warrior")
    location = models.CharField(max_length=60)
