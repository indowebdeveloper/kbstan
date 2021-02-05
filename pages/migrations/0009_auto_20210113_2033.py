# Generated by Django 3.0.8 on 2021-01-13 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20210112_2201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailcontent',
            old_name='page',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='content',
            field=models.TextField(null=True, verbose_name='Page content'),
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='name',
            field=models.CharField(choices=[('About', 'About'), ('T&C', 'Terms & Conditions'), ('Privacy', 'Privacy Policy')], max_length=20, verbose_name='Page name'),
        ),
    ]
