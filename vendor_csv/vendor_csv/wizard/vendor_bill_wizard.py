from odoo import models, fields

class VendorBillExportWizard(models.TransientModel):
    _name = 'vendor.bill.export.wizard'
    _description = 'Vendor Export Wizard'

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)

    def action_export(self):
        url = f'/export/vendor_bills?from_date={self.from_date}&to_date={self.to_date}'
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
