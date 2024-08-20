from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
def validate_invoice_number(value):
    if len(value) <= 10:
        raise ValidationError("Wrong Invoice Number")

def generate_unique_invoice_number(self):
        last_invoice = Invoice.objects.order_by('-invoice_number').first()
        if last_invoice:
            return str(int(last_invoice.invoice_number) + 1).zfill(10)
        return str(1).zfill(10)

class Invoice(models.Model):
    invoice_date = models.DateField(auto_now_add=True)
    work_order = models.IntegerField(unique=False)
    invoice_number = models.CharField(max_length= 10 ,null=True, unique=True, validators=[validate_invoice_number])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invoice_number = generate_unique_invoice_number(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice No:{self.invoice_number}"
