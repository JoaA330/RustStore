from django.db import models

class Charge(models.TextChoices):
    LIGHT = "Light", "Light"
    HEAVY = "Heavy", "Heavy"
    VERYHEAVY = "VeryHeavy", "Very Heavy"

class Recommended(models.TextChoices):
    CIVIL = "Civil", "Civil"
    WIZARD = "Wizard", "Wizard"
    WARRIOR = "Warrior", "Warrior"
    ARCHER = "Archer", "Archer"
    
class GunType(models.TextChoices):
    SWORD = "Sword", "Sword"
    POLEARM = "Polearm", "Polearm"
    ARCHER = "Archer", "Archer"
    MAGICAL = "Magical", "Magical"

class Category(models.TextChoices):
    GUNS = "Guns", "Guns"
    TOOLS = "Tools", "Tools"
    ARMOR = "Armor", "Armor"
    TRANSPORT = "Transport", "Transport"
    
#-----------------------
#-----------------------

class Product(models.Model):
    name = models.CharField(max_length=120)
    category = models.CharField(choices=Category.choices , max_length=50)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    used = models.BooleanField(default=False)
    recommendedFor = models.CharField(default= "Civil" ,choices= Recommended.choices, max_length=50)
    seller = models.CharField(max_length=50, default="NULL")
    
    
class Gun(Product):
    author = models.CharField(max_length=100)
    type = models.CharField(choices= GunType.choices, max_length=50)
    
    
class Tool(Product):
    agricultural = models.BooleanField(default=False)
    
    
    
class Armor(Product):
    protectionForMagic = models.BooleanField(default=False)
    protectionForCourts = models.BooleanField(default=False)
    protectionForHits = models.BooleanField(default=False)


class Transport(Product):
    maxSpeed = models.IntegerField()
    chargeLevel = models.CharField(max_length=30 ,choices= Charge.choices)
