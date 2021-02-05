# Generated by Django 3.0.8 on 2020-12-06 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_auto_20201206_1322'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='relatedCarBrand',
            field=models.ManyToManyField(blank=True, null=True, to='cars.CarBrand', verbose_name='Related to car brand'),
        ),
    ]
