from work_orders.models import WorkOrder, Segment
from .serializers import WorkOrderSerializer, SegmentSerializer, CustomerSerializer
from data.models import Customer,Car
from django.utils.timezone import now

def work_order_json_response():
    work_order = WorkOrder.objects.all()
    segment = Segment.objects.all()
    customer = Customer.objects.all()
    work_order_serializer = WorkOrderSerializer(work_order, many=True)
    segment_serializer = SegmentSerializer(segment, many=True)
    customer_serializer = CustomerSerializer(customer, many=True)

    work_orders = work_order_serializer.data
    segments = segment_serializer.data
    customers = customer_serializer.data
    # print(customers)
    # print(work_orders)
    active_work_orders = []
    for work_order in work_orders:
        for customer in customers:
            if customer["id"] == work_order["customer"]:
                work_order["customer"] = customer
                break
        if work_order["is_active"] == True:
            for segment in segments:
                if segment["work_order"] == work_order["id"]:
                    if "segments" not in work_order:
                        work_order["segments"] = []
                    work_order["segments"].append(segment)
            active_work_orders.append(work_order)
    # print(active_work_orders)

    return active_work_orders

def create_work_order(data):
    customer_data = data.get("customer")
    car_data = data.get("car")
    description_work = data.get("description", "")
    labor_price = data.get("labor_price", 0)
    spare_part_price = data.get("spare_part_price", 0)
    mics_price = data.get("mics_price", 0)
    payment = data.get("payment", "Credit")
    customer = Customer.objects.get(id=customer_data["id"])
    car = Car.objects.get(id=car_data["id"])

    new_work_order = WorkOrder(
        customer=customer,
        car=car,
        payment=payment,
        description_work=description_work,
        labor_price=labor_price,
        spare_part_price=spare_part_price,
        mics_price=mics_price,
        created_at=now(),
    )
    new_work_order.save()
    new_work_order_segment = Segment(
        work_order= new_work_order,
        description_work= "New Work Task",
    )
    new_work_order_segment.save()
    print("Success")