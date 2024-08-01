from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views import View
from work_orders.forms import WorkOrderForm, SegmentForm, LaborForm, SparePartForm, MiscellaneousForm
from work_orders.models import WorkOrder, Segment, Labor, SparePart, Miscellaneous


class WorkOrderListView(ListView):
    model = WorkOrder
    template_name = 'work_orders/work-order-list.html'
    context_object_name = "work_orders"

    def get_queryset(self):
        return WorkOrder.objects.all()


class CombinedCreateWorkOrderView(View):
    template_name = 'work_orders/create-work-order.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        work_order_form = WorkOrderForm()
        segment_form = SegmentForm()
        return render(request, self.template_name, {'work_order_form': work_order_form, 'segment_form': segment_form})

    def post(self, request, *args, **kwargs):
        work_order_form = WorkOrderForm(request.POST)
        segment_form = SegmentForm(request.POST)
        if work_order_form.is_valid() and segment_form.is_valid():
            work_order = work_order_form.save()
            segment = segment_form.save(commit=False)
            segment.work_order = work_order
            segment.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'work_order_form': work_order_form, 'segment_form': segment_form})



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
    template_name = ""  # to do template for this
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
