from django.contrib import admin
from .models import *

admin.site.register(WorkOrder)
admin.site.register(WorkOrderSegment)
admin.site.register(WorkOrderSparePart)
admin.site.register(WorkOrderServiceLabor)
admin.site.register(WorkOrderMiscellaneous)