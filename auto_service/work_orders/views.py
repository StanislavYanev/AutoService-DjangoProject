from datetime import timezone

from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from work_orders.forms import WorkOrderForm, SegmentForm, LaborForm, SparePartForm, MiscellaneousForm, \
    WorkOrderSearchForm, SparePartsSearchForm, WorkOrderNoteForm
from work_orders.models import WorkOrder, Segment, Labor, SparePart, Miscellaneous
from django.db.models import Q
from data.models import SparePartWarehouse
from invoice.models import Invoice


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


# class WorkOrderDeleteView(DeleteView):
#     model = WorkOrder
#     template_name = 'work_orders/work-order-delete.html'
#     success_url = reverse_lazy('work_orders:work_order_list')
#
#     def delete(self, request, *args, **kwargs):
#         can_delete = []
#         print("test")
#         for i in self.object.segments.all():
#             if i.calculate_seg_total() == 0:
#                 can_delete.append(True)
#                 print("test")
#             else:
#                 can_delete.append(False)
#         if False in can_delete:
#             return self.success_url
#         else:
#             self.object.delete()
#         print(can_delete)
#         return super().delete(request, *args, **kwargs)


def delete_work_order_view(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    can_delete = []
    if request.method == 'POST':
        for i in work_order.segment.all():
            if i.calculate_seg_total() == 0:
                can_delete.append(True)
                print("True")
            else:
                can_delete.append(False)
        if False in can_delete:
            return redirect('home')
        else:
            work_order.delete()
            print(can_delete)
            return redirect('work_orders:work_orders_search')
    return render(request, "work_orders/work-order-delete.html", {"work_order": work_order})


def delete_segment_view(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    work_order = segment.work_order
    if request.method == 'POST':
        segment.delete()
        work_order.update_total()
        return redirect('work_orders:workorder_detail', pk=work_order.pk)
    return render(request, "work_orders/work-order-segment-delete.html", {"segment": segment, "work_order": work_order})


def labor_segment_list(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    work_order = segment.work_order
    labors = Labor.objects.filter(work_order_segment=segment.pk)
    return render(request, 'work_orders/labor-menu.html',
                  {'work_order': work_order, 'segment': segment, 'labors': labors})


def add_labor_to_segment(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    work_order = segment.work_order
    if request.method == 'POST':
        form = LaborForm(request.POST)
        if form.is_valid():
            labor = form.save(commit=False)
            labor.work_order_segment = segment
            labor.save()
            segment.work_order.update_total()
            return redirect('work_orders:labor_menu', pk=segment.pk)
    else:
        form = LaborForm()
    return render(request, 'work_orders/add-labor-to-seg.html',
                  {'form': form, 'segment': segment, 'work_order': work_order})


def edit_labor_in_segment_view(request, pk):
    labor = get_object_or_404(Labor, pk=pk)
    segment = labor.work_order_segment
    work_order = segment.work_order
    if request.method == 'POST':
        form = LaborForm(request.POST, instance=labor)
        if form.is_valid():
            labor = form.save(commit=False)
            labor.work_order_segment = segment
            labor.save()
            segment.work_order.update_total()
            return redirect('work_orders:labor_menu', pk=segment.pk)
        else:
            print("Form is invalid", form.errors)
    else:
        form = LaborForm(instance=labor)
    return render(request, "work_orders/edit-labor.html", {'form': form, 'labor': labor, "segment": segment})


def delete_labor_in_segment_view(request, pk):
    labor = get_object_or_404(Labor, pk=pk)
    segment = labor.work_order_segment
    labor.delete()
    segment.work_order.update_total()
    return redirect('work_orders:labor_menu', pk=segment.pk)


def misc_detail_view(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    work_order = segment.work_order
    misc = Miscellaneous.objects.filter(work_order_segment=segment.pk)
    context = {'segment': segment, 'work_order': work_order, 'misc': misc}
    return render(request, "work_orders/misc-menu.html", context)


def misc_add_to_segment_view(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    work_order = segment.work_order
    if request.method == 'POST':
        form = MiscellaneousForm(request.POST)
        if form.is_valid():
            miscellaneous = form.save(commit=False)
            miscellaneous.work_order_segment = segment
            miscellaneous.save()
            segment.work_order.update_total()
            return redirect('work_orders:mics_menu', pk=segment.pk)
    else:
        form = MiscellaneousForm()
    context = {'segment': segment, 'work_order': work_order, "form": form}
    return render(request, "work_orders/add-mics.html", context)


def misc_edit_labor_in_segment_view(request, pk):
    misc = get_object_or_404(Miscellaneous, pk=pk)
    segment = misc.work_order_segment
    work_order = segment.work_order
    if request.method == 'POST':
        form = MiscellaneousForm(request.POST, instance=misc)
        if form.is_valid():
            misc = form.save(commit=False)
            misc.work_order_segment = segment
            misc.save()
            work_order.update_total()
            return redirect('work_orders:mics_menu', pk=segment.pk)
    else:
        form = MiscellaneousForm(instance=misc)
    return render(request, "work_orders/add-mics.html", {'form': form, 'segment': segment})


def misc_delete_labor_in_segment_view(request, pk):
    misc = get_object_or_404(Miscellaneous, pk=pk)
    segment = misc.work_order_segment
    misc.delete()
    segment.work_order.update_total()
    return redirect('work_orders:mics_menu', pk=segment.pk)


def spare_parts_list_view(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    work_order = segment.work_order
    spare_parts = SparePart.objects.filter(work_order_segment=segment.pk)
    return render(request, "work_orders/spare-parts-menu.html",
                  {'spare_parts': spare_parts, "segment": segment, "work_order": work_order})


def delete_spare_part_view(request, pk):
    spare_part = get_object_or_404(SparePart, pk=pk)
    segment = spare_part.work_order_segment
    spare_warehouse = SparePartWarehouse.objects.filter(part_number=spare_part.part_number)
    spare_part_one = spare_warehouse.first()
    spare_part_one.quantity += spare_part.quantity
    spare_part_one.save()
    spare_part.delete()
    segment.work_order.update_total()
    return redirect('work_orders:spare_parts_menu', pk=segment.pk)


def edit_spare_part_view(request, pk):
    spare_part = get_object_or_404(SparePart, pk=pk)
    segment = spare_part.work_order_segment
    work_order = segment.work_order
    if request.method == 'POST':
        form = SparePartForm(request.POST, instance=spare_part)
        if form.is_valid():
            spare_part = form.save(commit=False)
            form.work_order_segment = segment
            form.save()
            work_order.update_total()
            return redirect('work_orders:spare_parts_menu', pk=segment.pk)
    else:
        form = SparePartForm(instance=spare_part)
    contex = {"spare_part": spare_part, "segment": segment, "form": form}
    return render(request, "work_orders/edit-spare-parts.html", contex)


def search_query(query):
    query = query.replace("-", "")
    return query


def add_spare_part_view(request, pk):
    segment = get_object_or_404(Segment, pk=pk)
    query = ""
    results = []
    if request.method == 'GET':
        form = SparePartsSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            query = search_query(query)
            results = SparePartWarehouse.objects.filter(part_number__icontains=query)
    else:
        form = SparePartsSearchForm()

    contex = {"query": query, "results": results, "form": form, "segment": segment}
    return render(request, "work_orders/add-spare-parts.html", contex)


def add_spare_to_work_order_view(request, pk, seg_id):
    part = get_object_or_404(SparePartWarehouse, pk=pk)
    segment = get_object_or_404(Segment, pk=seg_id)
    quantity = int(request.POST['quantity'])

    wo_part, create = SparePart.objects.get_or_create(part_number=part.part_number,
                                                      defaults={'quantity': quantity, "price": part.customer_price,
                                                                "work_order_segment": segment,
                                                                'description': part.description})

    if create:
        wo_part.quantity = quantity
        part.quantity -= quantity

    else:
        if float(part.customer_price) == float(wo_part.price):
            wo_part.quantity += quantity
            part.quantity -= quantity

        else:
            print("TEST")
            wo_part = SparePart.objects.create(part_number=part.part_number, quantity=0, price=part.customer_price,
                                               work_order_segment=segment, description=part.description)
            wo_part.quantity += quantity
            part.quantity -= quantity

    part.save()
    wo_part.save()
    segment.work_order.update_total()

    return redirect('work_orders:spare_parts_menu', pk=segment.pk)


def invoice_work_order(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    work_order.update_total()
    if request.method == 'POST':
        form = WorkOrderNoteForm(request.POST, instance=work_order)
        if form.is_valid():
            work_order.description_work = form.cleaned_data['description_work']
            work_order.save()
        else:
            print(form.errors)
    else:
        form = WorkOrderNoteForm(instance=work_order)
    context = {"work_order": work_order, "form": form}
    return render(request, "work_orders/invoice.html", context)


def invoice_file_view(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    work_order.update_total()
    work_order.is_active = False
    work_order.invoiced = True
    work_order.save()
    invoice = Invoice.objects.create(work_order=work_order.pk)
    invoice.save()
    return render(request, "work_orders/invoice-confirm.html", {"work_order": work_order, "invoice": invoice})
