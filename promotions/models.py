from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class Promotion(models.Model):
    name = models.CharField(max_length=100)
    discount = models.PositiveIntegerField(
        verbose_name='Discount in percent',
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    bannerImage = models.ImageField(upload_to='promotions/images', blank=True, null=True, help_text='Recommended banner image dimentions are 1100 x 300 pixel')
    
    dateStart = models.DateField(default=datetime.now)    #* reference: https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    dateEnd = models.DateField(blank=True, null=True)

    isFeatured = models.BooleanField(default=False, verbose_name='Is featured')
    isActive = models.BooleanField(default=True, verbose_name='Is active')

    products = models.ManyToManyField(to='products.Product', blank=True)
    categories = models.ManyToManyField(to='products.Category', blank=True)

    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
