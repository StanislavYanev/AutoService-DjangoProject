# Generated by Django 5.0.7 on 2024-07-27 08:31

import data.my_validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparepart',
            name='quantity',
            field=models.IntegerField(null=True, validators=[data.my_validators.quantity_validator]),
        ),
    ]