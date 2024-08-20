from django.urls import path
from .views import *

app_name = 'work_orders'

urlpatterns = [path('work_order_list/', WorkOrderListView.as_view(), name="work_order_list"),
               path('workorder/add/', CombinedCreateWorkOrderView.as_view(), name="add_workorder"),
               path('workorder/search', WorkOrderSearchView.as_view(), name="work_orders_search"),
               path('workorder/<int:pk>/', WorkOrderDetailView.as_view(), name="workorder_detail"),
               path('workorder/<int:pk>/delete', delete_work_order_view, name="workorder_delete"),
               path('workorder/create-new-segment/<int:pk>/', add_segment_to_work_order,
                    name="segment_create_workorder"),
               path('workorder/delete-segment/<int:pk>/', delete_segment_from_work_order,
                    name="segment_delete_workorder"),
               path('workorders/delete-segment/<int:pk>/', delete_segment_view, name="segment_delete"),
               path('workorder/labor-menu/<int:pk>/', labor_segment_list, name="labor_menu"),
               path('workorder/add-labor-to-seg/<int:pk>', add_labor_to_segment, name="add_labor_to_segment"),
               path('workorder/edit-labor/<int:pk>', edit_labor_in_segment_view, name="edit_labor_in_segment"),
               path('workorder/delete-labor/<int:pk>', delete_labor_in_segment_view, name="delete_labor_in_segment"),
               path("workorder/mics/<int:pk>",misc_detail_view, name="mics_menu"),
               path("workorder/add-misc/<int:pk>",misc_add_to_segment_view, name="add_misc"),
               path("workorder/delete-misc/<int:pk>", misc_delete_labor_in_segment_view, name="delete_misc"),
               path("workorder/edit-misc/<int:pk>", misc_edit_labor_in_segment_view, name="edit_misc"),
               path('workorder/spareparts/<int:pk>',spare_parts_list_view, name="spare_parts_menu"),
               path('workorder/delete_spare-part/<int:pk>',delete_spare_part_view, name="delete_spare_part"),
               path('workorder/edit-spare-part/<int:pk>',edit_spare_part_view, name="edit_spare_parts"),
               path('workorder/add-parts<int:pk>', add_spare_part_view, name="add_spare_parts"),
               path('workorder/add-part-to-work-order<int:pk>/<int:seg_id>', add_spare_to_work_order_view, name="add_part_to_work_order"),
               path('invoice/<int:pk>/', invoice_work_order, name="invoice"),
               path('invoice-file/<int:pk>/', invoice_file_view, name="invoice-file"),]
