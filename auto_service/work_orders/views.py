from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from work_orders.forms import WorkOrderForm, SegmentForm, LaborForm, SparePartForm, MiscellaneousForm, \
    WorkOrderSearchForm
from work_orders.models import WorkOrder, Segment, Labor, SparePart, Miscellaneous
from django.db.models import Q
from django.contrib import messages


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


def add_segment_to_work_order(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    if request.method == 'POST':
        form = SegmentForm(request.POST)
        if form.is_valid():
            segment = form.save(commit=False)
            segment.work_order = work_order
            segment.save()
            return redirect('work_orders:workorder_detail', pk=work_order.pk)
    else:
        form = SegmentForm()
    return render(request, "work_orders/create-segment.html", {'form': form, 'work_order': work_order})


def delete_segment_from_work_order(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    work_order = segment.work_order
    print(work_order)
    if request.method == 'POST':
        segment.delete()
        return redirect('work_orders:workorder_detail', pk=work_order.pk)
    return render(request, "work_orders/work-order-segment-delete.html", {"segment": segment, "work_order": work_order})


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


class WorkOrderDetailView(DetailView):
    model = WorkOrder
    template_name = 'work_orders/work-order-details.html'
    context_object_name = 'work_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segments'] = Segment.objects.filter(work_order=self.object)
        return context


class WorkOrderDeleteView(DeleteView):
    model = WorkOrder
    template_name = 'work_orders/work-order-delete.html'
    success_url = reverse_lazy('work_orders:work_order_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return super().delete(request, *args, **kwargs)

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
