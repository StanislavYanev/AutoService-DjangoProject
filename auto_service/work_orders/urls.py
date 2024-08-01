from django.urls import path
from .views import *

app_name = 'work_orders'

urlpatterns = [path('work_order_list/', WorkOrderListView.as_view(), name="work_order_list"),
               path('work_order_create/', WorkOrderCreateView.as_view(), name="work_order_create"),
               path('work-order-createseg', SegmentCreateView.as_view(), name="work-order_createseg"), ]
