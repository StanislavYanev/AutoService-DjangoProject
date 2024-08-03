import uuid
from datetime import datetime, timedelta

from django.db import models

from data.models import Customer, Car, ServiceMan


class WorkOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    payment = models.CharField(max_length=30, blank=True, choices=[('Credit', "Credit"), ("Cash", "Cash")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} - {self.customer} - {self.car}"


class Segment(models.Model):
    WORK_DESCRIPTION = [("Maintenance", "Maintenance"),
                        ("Engine Repair", "Engine Repair"),
                        ("Transmission Repair", "Transmission Repair"),
                        ("Body and Painting", "Body and Painting"),
                        ("Suspension Repair", "Suspension Repair"), ]
    work_order = models.ForeignKey(WorkOrder, related_name='segment', on_delete=models.CASCADE)
    description_work = models.CharField(max_length=20, choices=WORK_DESCRIPTION)

    def __str__(self):
        return f"Segment{WorkOrder.objects.filter(pk=self.pk).count() + 1} --> {self.description_work}"


class SparePart(models.Model):
    work_order_segment = models.ForeignKey(Segment, related_name="spare_part", on_delete=models.CASCADE)
    part_number = models.CharField(max_length=20)
    description = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.part_number} - {self.description} - {self.quantity} - {self.price}"


class Labor(models.Model):
    LABOR_CHOICES = [("REP", "Repair"),
                     ("MNT", "Maintenance"),
                     ("BNP", "Body and Paint")
                     ]
    work_order_segment = models.ForeignKey(Segment, related_name='labor', on_delete=models.CASCADE)
    service_man_number = models.OneToOneField(ServiceMan, on_delete=models.CASCADE)
    date_of_service = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    labor_type = models.CharField(max_length=20, choices=LABOR_CHOICES)

    def duration(self):
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)
        duration = end_datetime - start_datetime
        return duration

    def __str__(self):
        return f"{self.service_man_number} - {self.duration()}"


class Miscellaneous(models.Model):
    MISC_CODE_CHOICES = [("CON", "Consumables"),
                         ("KLM", "Kilometers")]
    work_order_segment = models.ForeignKey(Segment, related_name="misc", on_delete=models.CASCADE)
    miss_code = models.CharField(max_length=30, choices=MISC_CODE_CHOICES)
    description = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.miss_code} - {self.description} - {self.price}"
