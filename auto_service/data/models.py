from django.db import models
from .my_validators import *


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
    PAYMENT_CHOICES = [("cash", "Cash"),
                       ("credit", "Credit")]
    PAYMENT_TERMS_CHOICES = [('COD', 'Cash on Delivery'), ('CIA', 'Cash in Advance'), ('Net_15', '15 days'),
                             ('Net_30', '30 days')]
    name = models.CharField(max_length=100)
    vat = models.IntegerField(validators=[vat_number_validator])
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,
                                       validators=[credit_limit_validator])
    payment_terms = models.CharField(max_length=30, choices=PAYMENT_TERMS_CHOICES)
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
    customer = models.ForeignKey(Customer, related_name='car', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} - {self.model}"


class ServiceMan(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField(validators=[phone_number_validator])
    email = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True, validators=[rating_validator])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SparePart(models.Model):
    CURRENCY_CHOICES = [("BGN", "Bulgarian lev"),
                        ("EUR", "Euro"), ]
    AVAILABILITY_CHOICES = [
        ("IN_STOCK", 'In Stock'),
        ("PRE_ORDER", 'Pre Order'),
    ]
    part_number = models.CharField(max_length=20)
    description = models.CharField(max_length=30)
    quantity = models.IntegerField(null=True, validators=[quantity_validator])
    availability = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES)

    @property
    def availability_status(self):
        if self.quantity > 0:
            return "IN_STOCK"
        else:
            return "PRE_ORDER"

    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=15, choices=CURRENCY_CHOICES)

    @property
    def customer_price(self):
        value = float(self.delivery_price)
        if self.currency == "EUR":
            value /= 1.95583
            self.currency = "BGN"
        return f"{value * 1.3}:2.f"

    part_code = models.CharField(max_length=5, blank=True,null=True)

    def __str__(self):
        return f"{self.part_number} {self.description}"
