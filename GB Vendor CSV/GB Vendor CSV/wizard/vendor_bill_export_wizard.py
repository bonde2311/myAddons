from odoo import models, fields

class VendorBillExportWizard(models.TransientModel):
    _name = 'vendor.bill.export.wizard'
    _description = 'Vendor Bill Export Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    def action_export(self):
        url = f'/export/vendor_bills?start_date={self.start_date}&end_date={self.end_date}'
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
