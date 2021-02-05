from django.db import models

class ProductBrand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(verbose_name='Brand logo')
    rank = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True) 

    def __str__(self):
        return self.name

class ProductSection(models.Model):
    title = models.CharField(max_length=100)
    isActive = models.BooleanField(default=True, verbose_name='Is active')
    rank = models.PositiveIntegerField(blank=True, null=True)
    products = models.ManyToManyField(to='products.Product', blank=True)
    categories = models.ManyToManyField(to='products.Category', blank=True)

    def __str__(self):
        return self.title

class PageContent(models.Model):
    PAGE_CHOICES = (
        ('About', 'About'),
        ('T&C', 'Terms & Conditions'),
        ('Privacy', 'Privacy Policy'),
    )
    name = models.CharField(choices=PAGE_CHOICES, max_length=20, verbose_name='Page name')
    content = models.TextField(null=True, verbose_name='Page content')

class EmailContent(models.Model):
    PAGE_CHOICES = (
        # ('Sign up & Email Confirmation', 'Sign up & Email Confirmation'),
        ('Awaiting Bank Transfer', 'Order Confirmed - Awaiting Bank Transfer'),
        ('Awaiting payment in store', 'Order Confirmed - Awaiting payment in store'),
        ('Awaiting payment on delivery', 'Order Confirmed - Awaiting payment on delivery'),
        # ('Awaiting Indodana payment', 'Awaiting Indodana payment'),
        # ('Reserved', 'Reserved'),
        # ('Paid on website', 'Paid on website'),
        # ('Paid in store', 'Paid in store'),
        ('Shipped', 'Order Shipped'),
        # ('Delivered', 'Delivered'),
        ('Cancelled', 'Order Cancelled'),
        # ('Refund in process', 'Refund in process'),
        ('Refunded', 'Order Refunded'),
    )
    name = models.CharField(choices=PAGE_CHOICES, unique=True, max_length=30, verbose_name='Page name')
    subject = models.CharField(max_length=200)
    content = models.TextField(verbose_name='Text Block Content')
