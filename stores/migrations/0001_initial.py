# Generated by Django 3.0.8 on 2020-12-06 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('zipCode', models.CharField(max_length=8)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('opening_hours', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='stores')),
                ('map_embedding_code', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
