from django.urls import path
from .views import *

app_name = 'work_orders'

urlpatterns = [path('work_order_list/', WorkOrderListView.as_view(), name="work_order_list"),
               path('workorder/add/', CombinedCreateWorkOrderView.as_view(), name="add_workorder"),
               path('workorder/search', WorkOrderSearchView.as_view(), name="work_orders_search"),
               path('workorder/<int:pk>/', WorkOrderDetailView.as_view(), name="workorder_detail"),
               path('workorder/<int:pk>/delete', WorkOrderDeleteView.as_view(), name="workorder_delete"),
               path('workorder/create-new-segment/<int:pk>/', add_segment_to_work_order,
                    name="segment_create_workorder"),
               path('workorder/delete-segment/<int:pk>/', delete_segment_from_work_order,
                    name="segment_delete_workorder"),
               path('workorder/labor-menu/<int:pk>/', labor_segment_list, name="labor_menu"),
               path('workorder/add-labor-to-seg/<int:pk>', add_labor_to_segment, name="add_labor_to_segment"),]
