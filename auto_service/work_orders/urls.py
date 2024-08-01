from django.urls import path
from .views import *

app_name = 'work_orders'

urlpatterns = [path('work_order_list/', WorkOrderListView.as_view(), name="work_order_list"),
               path('workorder/add/', CombinedCreateWorkOrderView.as_view(), name="add_workorder"),]