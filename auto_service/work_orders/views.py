from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

from work_orders.forms import WorkOrderForm, SegmentForm, LaborForm, SparePartForm, MiscellaneousForm
from work_orders.models import WorkOrder, Segment, Labor, SparePart, Miscellaneous


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
    success_url = reverse_lazy('work_orders:work-order_createseg')


class SegmentCreateView(CreateView):
    model = Segment
    form_class = SegmentForm
    template_name = "work_orders/create-segment.html"
    success_url = reverse_lazy('home')  # to create  html tor success with detail info

    def form_valid(self, form):
        work_order = WorkOrder.objects.get(pk=self.kwargs['pk'])
        print(work_order)
        form.instance.work_order = work_order
        return super().form_valid(form)


class LaborCreateView(CreateView):
    model = Labor
    form_class = LaborForm
    template_name = ""  # to do template for this
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        segment = Segment.objects.get(pk=self.kwargs['pk'])
        form.instance.segment = segment
        return super().form_valid(form)


class SparePartsCreateView(CreateView):
    model = SparePart
    form_class = SparePartForm
    template_name = "" # to do template for this
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        segment = Segment.objects.get(pk=self.kwargs['pk'])
        form.instance.segment = segment
        return super().form_valid(form)


class MicsCreateView(CreateView):
    model = Miscellaneous
    form_class = MiscellaneousForm
    template_name = ""
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        segment = Segment.objects.get(pk=self.kwargs['pk'])
        form.instance.segment = segment
        return super().form_valid(form)

