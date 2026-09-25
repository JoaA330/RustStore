from django.db import models
from django.conf import settings

class Charge(models.TextChoices):
    LIGHT = "Light", "Light"
    HEAVY = "Heavy", "Heavy"
    VERYHEAVY = "VeryHeavy", "Very Heavy"

class Recommended(models.TextChoices):
    CIVIL = "Civil", "Civil"
    WIZARD = "Wizard", "Wizard"
    WARRIOR = "Warrior", "Warrior"
    ARCHER = "Archer", "Archer"
    
class Gun_Type(models.TextChoices):
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
    category = models.CharField(choices=Category.choices , max_length=50, null=True, blank=True)
    #usamos integerField ya que el concepto de dinero sera monedas de oro y no tiene sentido usar decimales
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    used = models.BooleanField(default=True)
    sold = models.BooleanField(default=False)
    material = models.CharField(max_length=50, null=True, blank=True)
    recommended_for = models.CharField(default= "Civil" ,choices= Recommended.choices,max_length=50)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='products_sold')
    sold_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='products_bought')
    sold_at = models.DateTimeField(null=True, blank=True)
    
    
class Gun(Product):
    crafted_by = models.CharField(max_length=100, default="NULL", null=True, blank=True)
    type = models.CharField(choices= Gun_Type.choices, max_length=50)
    
    
class Tool(Product):
    agricultural = models.BooleanField(default=False)
    
    
    
class Armor(Product):
    protection_for_magic = models.BooleanField(default=False)
    protection_for_courts = models.BooleanField(default=False)
    protection_for_hits = models.BooleanField(default=False)


class Transport(Product):
    charge_level = models.CharField(max_length=30 ,choices= Charge.choices)
