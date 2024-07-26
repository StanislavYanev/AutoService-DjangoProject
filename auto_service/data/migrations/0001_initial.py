# Generated by Django 5.0.7 on 2024-07-26 16:39

import data.my_validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('vat', models.IntegerField(validators=[data.my_validators.vat_number_validator])),
                ('country', models.CharField(choices=[('Bulgaria', 'Bulgaria'), ('Albania', 'Albania'), ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'), ('Greece', 'Greece'), ('Kosovo', 'Kosovo'), ('North Macedonia', 'North Macedonia'), ('Montenegro', 'Montenegro'), ('Romania', 'Romania'), ('Serbia', 'Serbia'), ('Turkey', 'Turkey'), ('Croatia', 'Croatia'), ('Slovenia', 'Slovenia')], max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('credit_limit', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, validators=[data.my_validators.credit_limit_validator])),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('credit', 'Credit')], max_length=100)),
                ('payment_terms', models.CharField(choices=[('COD', 'Cash on Delivery'), ('CIA', 'Cash in Advance'), ('Net_15', '15 days'), ('Net_30', '30 days')], max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceMan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField(validators=[data.my_validators.phone_number_validator])),
                ('email', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('rating', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True, validators=[data.my_validators.rating_validator])),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=55)),
                ('model', models.CharField(max_length=55)),
                ('color', models.CharField(blank=True, choices=[('Black', 'Black'), ('White', 'White'), ('Gray', 'Gray'), ('Silver', 'Silver'), ('Red', 'Red'), ('Blue', 'Blue'), ('Brown', 'Brown'), ('Green', 'Green'), ('Yellow', 'Yellow'), ('Other', 'Other')], max_length=55)),
                ('engine', models.CharField(blank=True, choices=[('Diesel', 'Diesel'), ('Gasoline', 'Gasoline'), ('Gas', 'Gas'), ('Hybrid', 'Hybrid')], max_length=55)),
                ('date_built', models.DateField(blank=True, null=True)),
                ('vin_number', models.CharField(blank=True, max_length=55)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='data.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Influencer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField(validators=[data.my_validators.phone_number_validator])),
                ('email', models.CharField(blank=True, max_length=100)),
                ('company', models.ManyToManyField(to='data.customer')),
            ],
        ),
    ]
