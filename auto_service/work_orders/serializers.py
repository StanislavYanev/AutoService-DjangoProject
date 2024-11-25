from rest_framework import serializers
from .models import WorkOrder,Segment
from data.models import Customer, Car

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id","name","vat", "city"]

class WorkOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = WorkOrder
        fields = "__all__"


class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = "__all__"



class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


