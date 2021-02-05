from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from products.models import Category, Product

class Service(models.Model):
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateEdited = models.DateTimeField(auto_now=True)
 
    name = models.CharField(max_length=100, verbose_name='Service display name')
    slug = models.SlugField(unique=True, verbose_name='Service slug') 
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    # sku = models.CharField(max_length=100, unique=True, verbose_name='SKU')
    price = models.PositiveIntegerField(default=0)
    seoMetaTags = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO Tags (separate by comma "," )')
    isVisible = models.BooleanField(default=True, verbose_name='Visible to public')
    # categories = models.ManyToManyField(Category, blank=True)  #? categoeries are not required as it is more relevant to which product categories do these services belong to

    relatedCategories = models.ManyToManyField(Category, blank=True)
    relatedProducts = models.ManyToManyField(Product, blank=True)

    def save(self, *args, **kwargs):    # automatically saving the slug once the product has been saved
        if not self.slug:   # save slug only in the first time. If slug already exists, need to change manually if desired to avoid broken links in the future and bad SEO
            self.slug = slugify(self.name)

        super(Service, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    @property
    def sku(self):
        return self.id