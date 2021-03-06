# Generated by Django 3.0.8 on 2020-11-08 06:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='categories',
            field=models.ManyToManyField(blank=True, to='products.Category'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='customersUsedCoupons',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coupon',
            name='products',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
    ]
