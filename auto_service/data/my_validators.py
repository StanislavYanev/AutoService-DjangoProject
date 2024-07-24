from django.core.exceptions import ValidationError


def vat_number_validator(value):
    if len(str(value)) > 10:
        raise ValidationError('VAT number is too long')
    elif len(str(value)) < 10:
        raise ValidationError('VAT number is too short')
    return value


def credit_limit_validator(value):
    if value < 0:
        raise ValidationError('Credit limit cannot be negative')
    elif value == 0:
        raise ValidationError('Credit limit cannot be zero')
    return value


def rating_validator(value):
    if value < 0:
        raise ValidationError('Rating cannot be zero')
    elif value > 5:
        raise ValidationError('Rating cannot be greater than 5')
    return value


def phone_number_validator(value):
    if len(str(value)) < 10:
        raise ValidationError('Phone number is too short')
    return value

