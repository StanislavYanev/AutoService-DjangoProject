from django.db import models
from .my_validators import vat_number_validator, credit_limit_validator, rating_validator,phone_number_validator


class Customer(models.Model):
    COUNTRY_CHOICES = [
        ("Bulgaria", "Bulgaria"),
        ("Albania", "Albania"),
        ("Bosnia and Herzegovina", "Bosnia and Herzegovina"),
        ("Greece", "Greece"),
        ("Kosovo", "Kosovo"),
        ("North Macedonia", "North Macedonia"),
        ("Montenegro", "Montenegro"),
        ("Romania", "Romania"),
        ("Serbia", "Serbia"),
        ("Turkey", "Turkey"),
        ("Croatia", "Croatia"),
        ("Slovenia", "Slovenia")
    ]

    name = models.CharField(max_length=100)
    vat = models.IntegerField(validators=[vat_number_validator])
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,
                                       validators=[credit_limit_validator])
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Influencer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField(validators=[phone_number_validator])
    email = models.CharField(max_length=100, blank=True)
    company = models.ManyToManyField(Customer)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    COLOR_CHOICES = [
        ("Black", "Black"),
        ("White", "White"),
        ("Gray", "Gray"),
        ("Silver", "Silver"),
        ("Red", "Red"),
        ("Blue", "Blue"),
        ("Brown", "Brown"),
        ("Green", "Green"),
        ("Yellow", "Yellow"),
        ("Other", "Other"),
    ]
    ENGINE_CHOICES = [
        ("Diesel", "Diesel"),
        ("Gasoline", "Gasoline"),
        ("Gas", "Gas"),
        ("Hybrid", "Hybrid")

    ]
    make = models.CharField(max_length=55)
    model = models.CharField(max_length=55)
    color = models.CharField(max_length=55, blank=True, choices=COLOR_CHOICES)
    engine = models.CharField(max_length=55, blank=True, choices=ENGINE_CHOICES)
    date_built = models.DateField(blank=True, null=True)
    vin_number = models.CharField(max_length=55, blank=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} - {self.model}"


class ServiceMan(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField(validators=[phone_number_validator])
    email = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True,validators=[rating_validator])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
