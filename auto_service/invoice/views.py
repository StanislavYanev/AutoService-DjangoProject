from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from data.models import Customer
from invoice.models import Invoice
from work_orders.models import WorkOrder


def create_pdf(request, pk):
    invoice = get_object_or_404(Invoice, invoice_number=pk)
    work_order = WorkOrder.objects.get(pk=invoice.work_order)
    customer = work_order.customer
    print(customer.vat)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    margin = 12
    pdf.setLineWidth(2)
    pdf.rect(margin, margin, width - 2 * margin, height - 2 * margin)
    pdf.setFont('Helvetica-Bold', 40)
    pdf.drawString(width/2 - 63.36, 770, "Invoice")
    pdf.line(30, 740, 566, 740)
    pdf.setLineWidth(1)
    pdf.rect(30,610,width/2 - 40,120)
    pdf.rect(width/2+10,610,width/2 - 40,120)
    pdf.setFont('Helvetica', 12)
    pdf.drawString(36,710, "Company Name:")
    pdf.drawString(36,690, "Company Address:")
    pdf.drawString(36,670, "VAT:")
    client_name = f"Company Name:{customer.name}"
    client_address = f"Company Address:{customer.address}"
    vat_number = f"VAT:{customer.vat}"
    pdf.drawString(width/2+16,710, client_name)
    pdf.drawString(width/2+16,690, client_address)
    pdf.drawString(width/2+16,670, vat_number)

    pdf.showPage()
    pdf.save()

    return response
