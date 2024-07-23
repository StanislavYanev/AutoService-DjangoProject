from django.contrib import admin
from .models import Car, Customer, ServiceMan, Influencer
# Register your models here.

admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(ServiceMan)
admin.site.register(Influencer)
