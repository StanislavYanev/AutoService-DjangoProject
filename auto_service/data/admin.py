from django.contrib import admin
from .models import Car, Customer, Influencer, ServiceMan
# Register your models here.

admin.site.register(Customer)
admin.site.register(Car)
admin.site.register(Influencer)
admin.site.register(ServiceMan)