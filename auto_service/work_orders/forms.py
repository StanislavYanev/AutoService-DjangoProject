from django import forms
from work_orders.models import WorkOrder, Segment, Labor, SparePart, Miscellaneous


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ["customer", "car", "payment"]


class SegmentForm(forms.ModelForm):
    class Meta:
        model = Segment
        fields = ["description_work"]


class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = "__all__"


class MiscellaneousForm(forms.ModelForm):
    class Meta:
        model = Miscellaneous
        fields = "__all__"


class LaborForm(forms.ModelForm):
    class Meta:
        model = Labor
      # fields = "__all__"
        fields = ['service_man_number', 'date_of_service', 'start_time', 'end_time', 'labor_type']


class WorkOrderSearchForm(forms.Form):
    query = forms.CharField(label='Search Work Orders by number', max_length=255, required=False)
