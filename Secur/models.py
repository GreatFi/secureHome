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
    LGA_CHOICES = [
        ('enugu-north', 'Enugu North'),
        ('enugu-south', 'Enugu South'), 
        ('enugu-east', 'Enugu East'),
    ]

    TOWN_BY_LGA= { 

        'enugu-north':[
            ('gra', 'GRA'),
            ('independence layout', 'Independence Layout'),
            ('new layout', 'New Layout'),
            ('coal camp', 'Coal Camp'),
            ('ogui nike', 'Ogui Nike'),
            ('iva valley', 'Iva Valley'),
            ('holy ghost', 'Holy Ghost'),
            ('asata', 'Asata'),
            ('rangers avenue', 'Rangers Avenue'),
        ],

        'enugu-south':[
        ('uwani', 'Uwani'),
        ('maryland', 'Maryland'),
        ('gariki', 'Gariki'),
        ('achara layout', 'Achara Layout'),
        ('Agbani Road area', 'Agbani Road area'),
        ('kenyatta', 'Kenyatta'),
        ],

        'enugu-east' : [
        ('abakpa', 'Abakpa'),
        ('trans-ekulu', 'Trans-Ekulu'),
        ('emene', 'Emene'),
        ('thinkers corner', 'Thinkers Corner'),
        ('liberty estate', 'Liberty Estate'),
        ('Nike lake', 'Nike Lake'),
        ],
    }

    TOWN_CHOICES = [
        town for towns in TOWN_BY_LGA.values()
        for town in towns
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    propertyName = models.CharField(max_length=100)
    image = models.ImageField(upload_to='properties/', null=True, blank=True)  # Allow null for existing rows
    description = models.TextField(null=True, blank=True)  # Allow null for existing rows
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    houseType = models.CharField(choices=HOUSE_TYPE_CHOICES, default='apartment', max_length=20)
    lga = models.CharField(choices=LGA_CHOICES, default="Choose an lga", max_length=20)
    Town = models.CharField(choices=TOWN_CHOICES, default="Choose the town", max_length=20)

    def __str__(self):
        return f"{self.propertyName} {self.user}"

class Listproperties(models.Model):

    HOUSE_TYPE_CHOICES= [
        ('apartment', 'Apartment'),
        ('bungalow', 'Bungalow'),
        ('duplex', 'Duplex'),
        ('land', 'Land'),
    ]

    PROP_CHOICES = [
        ('sale', 'Sale'),
        ('rent', 'Rent'),
    ]
    LGA_CHOICES = [
        ('enugu-north', 'Enugu North'),
        ('enugu-south', 'Enugu South'), 
        ('enugu-east', 'Enugu East'),
    ]

    TOWN_BY_LGA= { 

        'enugu-north':[
            ('gra', 'GRA'),
            ('independence layout', 'Independence Layout'),
            ('new layout', 'New Layout'),
            ('coal camp', 'Coal Camp'),
            ('ogui nike', 'Ogui Nike'),
            ('iva valley', 'Iva Valley'),
            ('holy ghost', 'Holy Ghost'),
            ('asata', 'Asata'),
            ('rangers avenue', 'Rangers Avenue'),
        ],

        'enugu-south':[
        ('uwani', 'Uwani'),
        ('maryland', 'Maryland'),
        ('gariki', 'Gariki'),
        ('achara layout', 'Achara Layout'),
        ('Agbani Road area', 'Agbani Road area'),
        ('kenyatta', 'Kenyatta'),
        ],

        'enugu-east' : [
        ('abakpa', 'Abakpa'),
        ('trans-ekulu', 'Trans-Ekulu'),
        ('emene', 'Emene'),
        ('thinkers corner', 'Thinkers Corner'),
        ('liberty estate', 'Liberty Estate'),
        ('Nike lake', 'Nike Lake'),
        ],
    }

    TOWN_CHOICES = [
        town for towns in TOWN_BY_LGA.values()
        for town in towns
    ]
    propertyName = models.CharField(max_length=100)
    prop_links = models.OneToOneField(Addproperty, on_delete=models.CASCADE, related_name="listing")
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.CharField(max_length=100, default='Enugu')
    is_negotiable = models.BooleanField(default=True)
    moreDescription = models.TextField(default='No additional description provided.', max_length=500)
    contact_phone = models.CharField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    prop_size = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, default=0.00)
    houseType = models.CharField(choices=HOUSE_TYPE_CHOICES, default='apartment', max_length=20)
    prop_choices = models.CharField(choices=PROP_CHOICES, default='sale', max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    lga = models.CharField(choices=LGA_CHOICES, default="Choose an lga", max_length=20)
    Town = models.CharField(choices=TOWN_CHOICES, default="Choose the town", max_length=20)

    def __str__(self):
        return f"{self.propertyName}, {self.location}"

