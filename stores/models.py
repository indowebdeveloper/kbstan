from django.db import models
import re

class Store(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=8)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)
    opening_hours = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='stores', blank=True, null=True)
    map_embedding_code = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stores-list')

    def save(self, *args, **kwargs): 
        
        if self.map_embedding_code:
            map_code = re.search(r'src="\S*"', self.map_embedding_code)

            if map_code:
                self.map_embedding_code = map_code.group().replace('src="', '')[:-1]

        super(Store, self).save(*args, **kwargs) 
