from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class signup(models.Model):
    GENDER_CHOICES= [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    gender = models.CharField(choices=GENDER_CHOICES)
    dob = models.DateField()

    def __str__(self):
        return f"{self.user.username}"

    
class Addproperty(models.Model):

    HOUSE_TYPE_CHOICES= [
        ('apartment', 'Apartment'),
        ('bungalow', 'Bungalow'),
        ('duplex', 'Duplex'),
        ('land', 'Land'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    propertyName = models.CharField(max_length=100)
    image = models.ImageField(upload_to='properties/', null=True, blank=True)  # Allow null for existing rows
    description = models.TextField(null=True, blank=True)  # Allow null for existing rows
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    houseType = models.CharField(choices=HOUSE_TYPE_CHOICES, default='apartment', max_length=20)
    def __str__(self):
        return f"{self.propertyName} {self.user}"


class Listproperties(models.Model):

    HOUSE_TYPE_CHOICES= [
        ('apartment', 'Apartment'),
        ('bungalow', 'Bungalow'),
        ('duplex', 'Duplex'),
        ('land', 'Land'),
    ]

    propertyName = models.CharField(max_length=100)
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.CharField(max_length=100, default='Enugu')
    is_negotiable = models.BooleanField(default=True)
    moreDescription = models.TextField(default='No additional description provided.', max_length=500)
    contact_phone = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    prop_size = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, default=0.00)
    houseType = models.CharField(choices=HOUSE_TYPE_CHOICES, default='apartment', max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.propertyName}, {self.location}"
