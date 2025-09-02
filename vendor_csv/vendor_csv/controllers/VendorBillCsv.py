from odoo import http
from odoo.http import request
import csv
from io import StringIO


class VendorBillCsv(http.Controller):

    @http.route('/export/vendor_bills', type='http', auth='user')
    def export_vendor_bills_csv(self, from_date=None, to_date=None):
        domain = [('move_type', '=', 'in_invoice')]
        if from_date and to_date:
            domain += [('invoice_date', '>=', from_date), ('invoice_date', '<=', to_date)]

        bills = request.env['account.move'].sudo().search(domain)

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'Number', 'Invoice Partner', 'GSTIN', 'Invoice/Bill Date', 'Due Date',
            'Reference', 'Activities', 'Untaxed Amount Signed', 'CGST',
            'SGST', 'IGST', 'Total Signed', 'Total in Currency Signed',
            'Payment Status', 'Status'
        ])

        for bill in bills:
            cgst = sgst = igst = 0.0
            for line in bill.invoice_line_ids:
                for tax in line.tax_ids:
                    tax_amount = tax.amount / 100.0 * line.price_subtotal
                    tax_name = tax.name.upper()
                    if 'CGST' in tax_name:
                        cgst += tax_amount
                    elif 'SGST' in tax_name:
                        sgst += tax_amount
                    elif 'IGST' in tax_name:
                        igst += tax_amount

            writer.writerow([
                bill.name or '',
                bill.partner_id.display_name or '',
                bill.partner_id.vat or '',
                bill.invoice_date or '',
                bill.invoice_date_due or '',
                bill.ref or '',
                ', '.join(bill.activity_ids.mapped('summary')) or '',
                bill.amount_untaxed_signed or 0.0,
                round(cgst, 2),
                round(sgst, 2),
                round(igst, 2),
                bill.amount_total_signed or 0.0,
                bill.amount_total or 0.0,
                bill.payment_state or '',
                bill.state or ''
            ])

        filename = 'vendor_bills.csv'
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Disposition', f'attachment; filename={filename}'),
                ('Content-Type', 'text/csv')
            ]
        )
