from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator


class User(AbstractUser):       #* this is the custom user model that will be used as a new user model
    username = models.CharField(max_length=40, unique=False, default='')
    isCustomer = models.BooleanField(default=False)
    isStaff = models.BooleanField(default=False)

    phoneNumber = models.CharField(max_length=15, null=True, blank=True, verbose_name='Phone number', editable=False)   #* field is in DB however disable for now
    mobileNumber = models.CharField(max_length=15, null=True, blank=True, verbose_name='Mobile number')
    
    def get_absolute_url(self):
        return reverse('customer-details', kwargs={'pk': self.pk})
    
    def __str__(self):
        return str(self.email)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        if self.user:
            return str(self.user.phoneNumber)
        else:
            return '- no user -'

    def get_absolute_url(self):
        return reverse('customer-details', kwargs={'pk': self.pk})


class Address(models.Model):
    
    addressTypes = [
        ('home', 'home'),
        ('work', 'work'),
    ]

    stateChoices = [
        ("Jakarta","Jakarta"),
        ("Special Region of Yogyakarta","Special Region of Yogyakarta"),
        ("East Kalimantan","East Kalimantan"),
        ("Riau Islands","Riau Islands"),
        ("Bali","Bali"),
        ("Riau","Riau"),
        ("North Sulawesi","North Sulawesi"),
        ("Banten","Banten"),
        ("West Sumatra","West Sumatra"),
        ("West Java","West Java"),
        ("Aceh","Aceh"),
        ("Central Java","Central Java"),
        ("North Sumatra","North Sumatra"),
        ("South Sulawesi","South Sulawesi"),
        ("East Java","East Java"),
        ("Bangka Belitung Islands","Bangka Belitung Islands"),
        ("Bengkulu","Bengkulu"),
        ("Jambi","Jambi"),
        ("Southeast Sulawesi","Southeast Sulawesi"),
        ("North Kalimantan","North Kalimantan"),
        ("Central Kalimantan","Central Kalimantan"),
        ("South Kalimantan","South Kalimantan"),
        ("South Sumatra","South Sumatra"),
        ("Lampung","Lampung"),
        ("Central Sulawesi","Central Sulawesi"),
        ("Maluku","Maluku"),
        ("Gorontalo","Gorontalo"),
        ("North Maluku","North Maluku"),
        ("West Nusa Tenggara","West Nusa Tenggara"),
        ("West Kalimantan","West Kalimantan"),
        ("West Sulawesi","West Sulawesi"),
        ("East Nusa Tenggara","East Nusa Tenggara"),
        ("West Papua","West Papua"),
        ("Papua","Papua"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=4, choices=addressTypes, default='home', blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    houseNumber = models.CharField(max_length=5, verbose_name='House number', blank=True, null=True)
    # unitNumber = models.CharField(max_length=5, verbose_name='Unit number')     #* depricated after phase 1
    city = models.CharField(max_length=50, blank=True, null=True)
    zipCode = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(99999)])
    state = models.CharField(max_length=50, choices=stateChoices, blank=True, null=True, default='Jakarta')
    shippingCost = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name='Shipping cost')

    def get_absolute_url(self):
        return reverse('customer-details', kwargs={'pk': self.customer.pk})

    def __str__(self):
        return self.type

