from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from .tasks import send_status_update_email
from .utils import send_notification_to_user
# Create your models here.

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
class signup(models.Model):
    GENDER_CHOICES= [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    dob = models.DateField()

    def __str__(self):
        return f"{self.user.username}"


    
class Addproperty(models.Model):

    HOUSE_TYPE_CHOICES= [
        ('apartment', 'Apartment'),
        ('bungalow', 'Bungalow'),
        ('duplex', 'Duplex'),
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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    propertyName = models.CharField(max_length=100)
    image = models.ImageField(upload_to='properties/', null=True, blank=True)  # Allow null for existing rows
    description = models.TextField(null=True, blank=True)  # Allow null for existing rows
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    houseType = models.CharField(choices=HOUSE_TYPE_CHOICES, default='apartment', max_length=20)
    lga = models.CharField(choices=LGA_CHOICES, default="Choose an lga", max_length=20)
    Town = models.CharField(choices=TOWN_CHOICES, default="Choose the town", max_length=20)

    def save(self, *args, **kwargs ):
        create_notification(
            user=self.user,
            notification_type='property_uploaded',
            message=f'your property {self.propertyName} has been uploaded sucessfully'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.propertyName} {self.user}"

class Listproperties(models.Model):
    STATUS = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('declined', 'Declined'),
    ]
    HOUSE_TYPE_CHOICES= [
        ('apartment', 'Apartment'),
        ('bungalow', 'Bungalow'),
        ('duplex', 'Duplex'),
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
    RENT_DURATION = {
        'rent':[
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("yearly", "Yearly")
        ],
    }
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

    Duration_Choices = [
        duration for durations in RENT_DURATION.values()
        for duration in durations
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
    contact_phone = models.CharField(null=True, blank=True, max_length=11)
    email = models.EmailField(null=True, blank=True)
    prop_size = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, default=0.00)
    houseType = models.CharField(choices=HOUSE_TYPE_CHOICES, default='apartment', max_length=20)
    prop_choices = models.CharField(choices=PROP_CHOICES, default='sale', max_length=20)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    lga = models.CharField(choices=LGA_CHOICES, default="Choose an lga", max_length=20)
    Town = models.CharField(choices=TOWN_CHOICES, default="Choose the town", max_length=20)
    duration = models.CharField(choices=Duration_Choices, default="select a timeframe", max_length=20, null=True, blank=True)
    status = models.CharField(choices=STATUS, blank=True, null=True, default="pending", max_length=20)
    reasonText = models.TextField(max_length=250, blank=True, null=True)
    view_count = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        if self.pk:
            old_property = Listproperties.objects.get(pk=self.pk)
            if self.status in ['approved', 'declined'] and old_property.status != self.status:
                send_status_update_email.delay(
                    self.user.email,
                    self.propertyName,
                    self.status
                )
                if self.status == 'approved':
                    message = f"Your property {self.propertyName} has been approved!"
                else:
                    message = f"Your property {self.propertyName} has been declined!. Reason: {self.reasonText}"

                create_notification(
                    user=self.user,
                    notification_type=f'property_{self.status}',
                    message=message,
                    property_link=self
                )
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            create_notification(
                user=self.user,
                notification_type='property_listed',
                message=f"Your property {self.propertyName} has been listed. Please wait for verification",
                property_link=self
            )
        
    
    def __str__(self):
        return f"{self.propertyName}, {self.location}"
    
    class Meta:
        indexes = [
            models.Index(fields=['lga', 'prop_choices']),
            models.Index(fields=['price'])
        ]
        

class SavedProperty(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listproperties, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)  

    
    class Meta:
        unique_together = ('user', 'listing')
    
    def save(self, *args, **kwargs):
        create_notification(
            user = self.user,
            notification_type = 'property_saved',
            message = f"You have saved the property: {self.listing.propertyName}",
            property_link=self.listing
        )
        create_notification(
            user = self.listing.user,
            notification_type = 'property_saved',
            message = f"The property {self.listing.propertyName} has been saved by {self.user}",
            property_link=self.listing
        )
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.listing}"    
    

class Property_View(models.Model):
    Propname = models.ForeignKey(Listproperties, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.Propname}, {self.viewed_at}"
    

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('property_uploaded', 'Property Uploaded'),
        ('property_approved', 'Property Approved'),
        ('property_declined', 'Property Declined'),
        ('property_listed', 'Property Listed'),
        ('property_saved', 'Property Saved'),
        ('property_unsaved', 'Property Unsaved'),
        ('property_delisted', 'Property Delisted'),
        ('property_deleted', 'Property Deleted'),
        ('property_flagged', 'Property Flagged'),
    ]

    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    property_link = models.ForeignKey(Listproperties, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"
    

def create_notification(user, notification_type, message, property_link=None):
    
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message,
        property_link=property_link
    )
    
    # commented out for later
    
    # send_notification_to_user(
    #     user.id,
    #     notification_type,
    #     message,
    #     notification.created_at
    # )
    
    return notification


class OTPVerification(models.Model):
    user_verification = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    def __str__(self):
        return f"OTP for {self.email} - {self.otp_code}"
