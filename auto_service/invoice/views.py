from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from invoice.models import Invoice
from work_orders.models import WorkOrder


def create_pdf(request, pk):
    invoice = get_object_or_404(Invoice, invoice_number=pk)
    work_order = WorkOrder.objects.get(pk=invoice.work_order)
    customer = work_order.customer

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    margin = 12
    light_white = colors.Color(0.85, 0.85, 0.85)
    pdf.setLineWidth(2)
    pdf.rect(margin, margin, width - 2 * margin, height - 2 * margin)
    pdf.setFont('Helvetica-Bold', 40)
    pdf.drawString(width / 2 - 63.36, 770, "Invoice")
    pdf.line(30, 740, 566, 740)
    pdf.setLineWidth(1)
    pdf.setFillColor(light_white)
    pdf.rect(30, 600, width / 2 - 40, 125, stroke=1, fill=1)
    pdf.rect(width / 2 + 10, 600, width / 2 - 40, 125, stroke=1, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 12)
    pdf.drawString(36, 710, "Company: Rezos")
    pdf.drawString(36, 690, "Country:  Bulgaria")
    pdf.drawString(36, 670, "City:  Varna")
    pdf.drawString(36, 650, "Address: More 4 Me")
    pdf.drawString(36, 630, "VAT:0123456789")
    pdf.drawString(36, 610, "FLB: Stanislav")

    client_name = f"Company:  {customer.name}"
    client_country = f"Country:  {customer.country}"
    client_city = f"City:  {customer.city}"
    client_address = f"Address:  {customer.address}"
    vat_number = f"VAT:  {customer.vat}"
    flb = f"FLB:  {customer.flb}"
    pdf.drawString(width / 2 + 16, 710, client_name)
    pdf.drawString(width / 2 + 16, 690, client_country)
    pdf.drawString(width / 2 + 16, 670, client_city)
    pdf.drawString(width / 2 + 16, 650, client_address)
    pdf.drawString(width / 2 + 16, 630, vat_number)
    pdf.drawString(width / 2 + 16, 610, flb)

    pdf.setFillColor(light_white)
    pdf.rect(30, 570, width - 60, 15, stroke=1, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(36, 574, "No:")
    pdf.drawString(80, 574, "Part No:")
    pdf.drawString(140, 574, "Description:")
    pdf.drawString(250, 574, "Quantity:")
    pdf.drawString(330, 574, "Unit Price:")
    pdf.drawString(420, 574, "Discount:")
    pdf.drawString(500, 574, "Total:")

    row = 555
    count_no = 1
    segments = work_order.segment.all()
    pdf.setFont('Helvetica', 10)
    for seg in segments:
        parts = seg.spare_part.all()
        for part in parts:
            pdf.drawString(36, row, str(count_no))
            pdf.drawString(80, row, part.part_number)
            pdf.drawString(140, row, part.description)
            pdf.drawString(250, row, str(part.quantity))
            pdf.drawString(330, row, f"{str(part.price)} BGN")
            pdf.drawString(420, row, "")
            pdf.drawString(500, row, f"{str(part.total_price())} BGN")
            row -= 14
            count_no += 1

    y_position = 240
    distance = 40
    total_wo_price = f"Total: {str(work_order.total_price)} BGN"
    text_width = pdf.stringWidth(total_wo_price, "Helvetica", 10)
    x_position = width - text_width - distance
    pdf.drawString(x_position, y_position, total_wo_price)
    y_position += 20

    misc = str(work_order.mics_price)
    text_misc = f"Miscellaneous: {misc} BGN"
    if misc != "0.00":
        text_width = pdf.stringWidth(text_misc, "Helvetica", 10)
        x_position = width - text_width - distance
        pdf.drawString(x_position, y_position, text_misc)
        y_position += 20

    labor = work_order.labor_price
    labor_text = f"Labor: {str(labor)} BGN"
    if labor != 0:
        text_width = pdf.stringWidth(labor_text, "Helvetica", 10)
        x_position = width - text_width - distance
        pdf.drawString(x_position, y_position, labor_text)
        y_position += 20

    spare_parts = work_order.spare_part_price
    spare_parts_text = f"Spare Parts: {str(spare_parts)} BGN"
    if spare_parts != 0:
        text_width = pdf.stringWidth(spare_parts_text, "Helvetica", 10)
        x_position = width - text_width - distance
        pdf.drawString(x_position, y_position, spare_parts_text)
        y_position += 20

    pdf.rect(margin, 152, width - margin * 2, 70)
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(36, 210, "Notes :")
    note = work_order.description_work
    if note:
        pdf.drawString(36, 185, note)

    pdf.setFillColor(light_white)
    pdf.rect(margin, margin, width - margin * 2, 140, stroke=1, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(36, 135, "Bank Account: IBAN: BG80BNBG96611020345678, BIC/SWIFT: BNBGBGSD")
    pdf.drawString(36, 115, "Bank Name: Bank of Example")
    pdf.drawString(36, 95, f"Payment Method: {work_order.payment}")
    pdf.drawString(36, 75, 'Contact Details: Phone: +1-234-567-890, Email: support@example.com')
    pdf.drawString(36, 45, 'Signature of Issuing Person:.................')

    pdf.showPage()
    pdf.save()

    return response
