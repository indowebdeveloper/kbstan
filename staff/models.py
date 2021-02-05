from django.db import models
from customers.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #? field depricated through django permissions
    ACCESS_CHOICES = (
        # ('dashboard', 'Dashboard'),
        ('products-view', 'Products viewing'),
        # ('products-edit', 'Products editing'),
        ('orders', 'Orders'),
        ('customers', 'Customers'),
        ('cars', 'Cars'),
        ('staff', 'Staff'),
        ('stores', 'Stores'),
        ('coupons', 'Coupons'),
        ('promotions', 'Promotions'),
    )
    sectionsAccess = MultiSelectField(choices=ACCESS_CHOICES, blank=True, null=True, verbose_name="Access to")

    def __str__(self):
        return str(self.user)
