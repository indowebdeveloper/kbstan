from django.db import models
from django.urls import reverse
from cars.models import CarBrand
from customers.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from promotions.models import Promotion
from django.db.models import Max, Q
# from django.contrib.postgres.fields import JSONField    #todo activate once migrated to Postgres

class Attribute(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to='categories')
    # isVisibleToPublic = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateEdited = models.DateTimeField(auto_now=True)
    
    name = models.CharField(max_length=100, verbose_name='Name')
    slug = models.SlugField(unique=True, verbose_name='Product slug') 
    description = models.TextField(verbose_name='Description')
    # sku = models.CharField(max_length=100, unique=True, verbose_name='SKU')
    isFeatured = models.BooleanField(default=False, verbose_name='Is featured')
    purchaseOnlyViaEnquiry = models.BooleanField(default=False, verbose_name='Product sold only via enquiry')
    price = models.PositiveIntegerField()
    # latestPurchasingPrice = models.PositiveIntegerField(blank=True, null=True, editable=False)    #? depricated?
    bottomPrice = models.PositiveIntegerField(verbose_name='Bottom price')
    quantity = models.PositiveIntegerField()
    purchasePrice = models.PositiveIntegerField(verbose_name='Latest purchasing price per unit', null=True)
    cogs = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12)
    stockThreshold = models.PositiveIntegerField(verbose_name='Minimum stock')
    seoMetaTags = models.CharField(max_length=200, blank=True, null=True, verbose_name='SEO Tags (separate by comma "," )')
    isVisible = models.BooleanField(default=True, verbose_name='Visible to public')
    categories = models.ManyToManyField(Category, blank=True)
    relatedCarBrand = models.ManyToManyField(CarBrand, verbose_name='Related to car brand', blank=True, null=True)
    featured_image = models.ImageField(upload_to='products/images', help_text='Recommended image dimentions are 300 x 300 pixel')

    def save(self, *args, **kwargs):    # automatically saving the slug once the product has been saved
        if not self.slug:   # save slug only in the first time. If slug already exists, need to change manually if desired to avoid broken links in the future and bad SEO
            
            self.slug = slugify(self.name)
            
            recent_product = Product.objects.filter(slug=self.slug).last()
            if recent_product:
                self.slug += str(1)

        # when creating a product set the COGS and create creation history
        if not self.cogs:
            self.cogs = self.purchasePrice
            self.latestPurchasingPrice = self.purchasePrice

        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    @property
    def sku(self):
        return self.id

    @property
    def discount_amount(self):
        
        prodCategories = Category.objects.filter(product=self)
        promotions = Promotion.objects.filter(
            Q(products=self) |
            Q(categories__in=prodCategories)
        )

        if not promotions:
            return 0
        else:
            maxDiscount = promotions.aggregate(Max('discount'))['discount__max']
            return maxDiscount

    @property
    def discount_price(self):
        discountPrice = round(self.price * (1- self.discount_amount/100))
        return discountPrice

    #? meant to be used to overwrite the propery value without returning an error, but when trying to overwrite the value stays the same..
    # @discount_price.setter
    # def discount_price(self, value):
    #     self._discount_price = value


class ProductAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, blank=True, null=True)
    values = models.CharField(max_length=200, blank=True) #, help_text='Separate values by comma (,)')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.values)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images', blank=True, null=True)

    def __str__(self):
        return self.product.name

  
class ProductSearchQuery(models.Model):
    timestampCreated = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    queryData = models.TextField()      #todo change this to JSONFIeld once migrated to Postgres
