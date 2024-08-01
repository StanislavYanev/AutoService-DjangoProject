from django import forms
from work_orders.models import WorkOrder, Segment, Labor, SparePart, Miscellaneous


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'


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
        fields = "__all__"
