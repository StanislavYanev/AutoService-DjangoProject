from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views import View
from work_orders.forms import WorkOrderForm, SegmentForm, LaborForm, SparePartForm, MiscellaneousForm, WorkOrderSearchForm
from work_orders.models import WorkOrder, Segment, Labor, SparePart, Miscellaneous
from django.db.models import Q

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


class SegmentCreateWorkOrderView(CreateView):
    model = Segment
    form_class = SegmentForm
    template_name = 'work_orders/create-work-order.html'

    def form_valid(self, form):
        form.instance.work_order_id = self.kwargs['work_order_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home', kwargs={'work_order_id': self.kwargs['work_order_id']})


class WorkOrderSearchView(ListView):
    model = WorkOrder
    template_name = 'work_orders/edit-work-order.html'
    context_object_name = 'work_orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query', None)
        if query:
            queryset = queryset.filter(Q(id__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = WorkOrderSearchForm(self.request.GET)
        return context












# class LaborCreateView(CreateView):
#     model = Labor
#     form_class = LaborForm
#     template_name = ""  # to do template for this
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         segment = Segment.objects.get(pk=self.kwargs['pk'])
#         form.instance.segment = segment
#         return super().form_valid(form)
#
#
# class SparePartsCreateView(CreateView):
#     model = SparePart
#     form_class = SparePartForm
#     template_name = ""  # to do template for this
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         segment = Segment.objects.get(pk=self.kwargs['pk'])
#         form.instance.segment = segment
#         return super().form_valid(form)
#
#
# class MicsCreateView(CreateView):
#     model = Miscellaneous
#     form_class = MiscellaneousForm
#     template_name = ""
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         segment = Segment.objects.get(pk=self.kwargs['pk'])
#         form.instance.segment = segment
#         return super().form_valid(form)
