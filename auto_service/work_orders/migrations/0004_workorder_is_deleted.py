# Generated by Django 5.0.7 on 2024-08-04 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0003_workorder_invoiced'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]