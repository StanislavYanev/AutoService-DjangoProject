# Generated by Django 5.0.7 on 2024-08-04 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
