# Generated by Django 3.1.3 on 2021-01-30 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20210127_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
