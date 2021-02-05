# Generated by Django 3.0.8 on 2021-01-27 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_auto_20201207_2020'),
        ('products', '0005_auto_20210117_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='relatedCarBrand',
            field=models.ManyToManyField(to='cars.CarBrand', verbose_name='Related to car brand'),
        ),
    ]
