from django.db import models
from customers.models import Customer
from django.urls import reverse

class CarBrand(models.Model):
    brand = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.brand

#? depricated model? can be deleted after deployment
class CarType(models.Model):
    carBrand = models.ForeignKey(CarBrand, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=50, unique=True)
    buildYear = models.IntegerField()
    details = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.type)


class CustomerCar(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    carBrand = models.ForeignKey(CarBrand, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Car brand')
    carModel = models.CharField(max_length=100, blank=True, null=True, verbose_name='Car model')
    licensePlate = models.CharField(max_length=10, blank=True, null=True, verbose_name='License plate')

    def get_absolute_url(self):
        return reverse('customer-details', kwargs={'pk': self.customer.pk})

    def __str__(self):
        return self.licensePlate
