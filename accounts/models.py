from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)


class Property(models.Model):
    HOUSE_TYPE_CHOICES = [
        ('duplex', 'Duplex'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('other', 'Other')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    house_type = models.CharField(max_length=20, choices=HOUSE_TYPE_CHOICES)
    other_type = models.CharField(max_length=100, blank=True, null=True)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    balcony = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    playing_area = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.city}, {self.area} - {self.get_house_type_display()}"
