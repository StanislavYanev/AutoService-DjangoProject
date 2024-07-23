from django.core.exceptions import ValidationError

def vat_number_validator(value):
    if len(str(value)) > 10:
        raise ValidationError('VAT number is too long')
    elif len(str(value)) < 10:
        raise ValidationError('VAT number is too short')