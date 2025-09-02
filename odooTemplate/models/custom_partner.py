from odoo import models, fields

class CustomPartner(models.Model):
    _name = "custom.partner"
    _description = "Custom Customer/Vendor"

    name = fields.Char(string="Name", required=True)
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('both', 'Customer & Vendor')
    ], string="Type", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
