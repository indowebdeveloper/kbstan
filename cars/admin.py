from django.contrib import admin
from .models import CarType, CarBrand, CustomerCar

admin.site.register(CarType)
admin.site.register(CarBrand)
admin.site.register(CustomerCar)