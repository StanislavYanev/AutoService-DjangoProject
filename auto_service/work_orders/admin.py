from django.contrib import admin
from .models import *


class SegmentInline(admin.StackedInline):
    model = Segment
    extra = 1


class SpareParInline(admin.StackedInline):
    model = SparePart
    extra = 1


class LaborInline(admin.StackedInline):
    model = Labor
    extra = 1


class MicsInline(admin.StackedInline):
    model = Miscellaneous
    extra = 1


class WorkOrderAdmin(admin.ModelAdmin):
    inlines = [SegmentInline]


class SegmentAdmin(admin.ModelAdmin):
    inlines = [SpareParInline, LaborInline, MicsInline]


admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Segment, SegmentAdmin)
admin.site.register(SparePart)
admin.site.register(Labor)
admin.site.register(Miscellaneous)
