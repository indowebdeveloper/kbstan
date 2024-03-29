# Generated by Django 3.0.8 on 2020-12-06 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateEdited', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Product display name')),
                ('slug', models.SlugField(unique=True, verbose_name='Product slug')),
                ('description', models.TextField(verbose_name='Product description')),
                ('sku', models.CharField(max_length=100, unique=True, verbose_name='SKU')),
                ('isFeatured', models.BooleanField(default=False)),
                ('purchaseOnlyViaEnquiry', models.BooleanField(default=False, verbose_name='Product sold only via enquiry')),
                ('price', models.PositiveIntegerField()),
                ('bottomPrice', models.PositiveIntegerField(verbose_name='Bottom price')),
                ('quantity', models.PositiveIntegerField()),
                ('purchasePrice', models.PositiveIntegerField(null=True, verbose_name='Latest purchasing price per unit')),
                ('cogs', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('stockThreshold', models.PositiveIntegerField(verbose_name='Minimum stock')),
                ('seoMetaTags', models.CharField(blank=True, max_length=200, null=True, verbose_name='SEO Tags (separate by comma "," )')),
                ('isVisible', models.BooleanField(default=True, verbose_name='Visible to public')),
                ('featured_image', models.ImageField(help_text='Recommended image dimentions are 300 x 300 pixel', upload_to='products/images')),
                ('categories', models.ManyToManyField(blank=True, to='products.Category')),
                ('relatedCarBrand', models.ManyToManyField(to='cars.CarBrand', verbose_name='Related to car brand')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSearchQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestampCreated', models.DateTimeField(auto_now_add=True)),
                ('queryData', models.TextField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('values', models.CharField(blank=True, max_length=200)),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Attribute')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
    ]
