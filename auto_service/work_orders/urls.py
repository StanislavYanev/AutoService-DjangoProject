from django.urls import path
from .views import *

app_name = 'work_orders'

urlpatterns = [path('work_order_list/', WorkOrderListView.as_view(), name="work_order_list"),
               path('workorder/add/', CombinedCreateWorkOrderView.as_view(), name="add_workorder"),
               path('workorder/search', WorkOrderSearchView.as_view(), name="work_orders_search"), ]
# path('workorder/<int:workorder_id>/segment/add', SegmentCreateWorkOrderView, name="segment_create_workorder"),]
