from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
def validate_invoice_number(value):
    if value <= 10:
        return  str(value).zfill(10)
    else:
        raise ValidationError("Wrong Invoice Number")

def generate_unique_invoice_number(self):
        last_invoice = Invoice.objects.order_by('-invoice_number').first()
        if last_invoice:
            return last_invoice.invoice_number + 1
        return 1

class Invoice(models.Model):
    invoice_date = models.DateField(auto_now_add=True)
    work_order = models.IntegerField(unique=True)
    invoice_number = models.IntegerField(null=True, unique=True, validators=[validate_invoice_number])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invoice_number = generate_unique_invoice_number(self)
        super().save(*args, **kwargs)


