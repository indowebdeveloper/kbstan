# Generated by Django 3.0.8 on 2020-12-06 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('discount', models.PositiveIntegerField(verbose_name='Discount in percent')),
                ('bannerImage', models.ImageField(blank=True, help_text='Recommended banner image dimentions are 1100 x 300 pixel', null=True, upload_to='promotions/images')),
                ('isFeatured', models.BooleanField(default=False)),
                ('isActive', models.BooleanField(default=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, to='products.Category')),
                ('products', models.ManyToManyField(blank=True, to='products.Product')),
            ],
        ),
    ]
