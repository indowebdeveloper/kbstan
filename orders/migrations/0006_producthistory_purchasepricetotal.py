# Generated by Django 3.0.8 on 2020-11-08 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20201108_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthistory',
            name='purchasePriceTotal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
