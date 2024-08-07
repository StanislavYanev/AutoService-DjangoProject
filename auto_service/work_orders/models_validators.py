from django.core.exceptions import ValidationError
from datetime import time

def start_work_validator(value):
    start_time = time(8, 30)
    if value < start_time:
        raise ValidationError("Work hours must start from  8 and 30.")
    return value


def end_work_validator(value):
    end_time = time(19, 30)
    if value > end_time:
        raise ValidationError("Work hours must end from  19 and 30.")
    return value

