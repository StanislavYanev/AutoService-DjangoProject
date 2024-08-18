from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
def validate_invoice_number(value):
    if value <= 10:
        return  value.zfill(10)
    else:
        raise ValidationError("Wrong Invoice Number")

class Invoice(models.Model):
    invoice_number = models.IntegerField(unique=True, validators=[validate_invoice_number])
    invoice_date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        self.invoice_number = validate_invoice_number(self.pk)

        super().save(*args, **kwargs)
    work_order = models.IntegerField(max_length=10, unique=True)

