from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

from work_orders.forms import WorkOrderForm
from work_orders.models import WorkOrder


class WorkOrderListView(ListView):
    model = WorkOrder
    template_name = 'work_orders/work-order-list.html'
    context_object_name = "work_orders"

    def get_queryset(self):
        return WorkOrder.objects.all()

class WorkOrderCreateView(CreateView):
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = "work_orders/create-work-order.html"
    success_url = reverse_lazy('home')
