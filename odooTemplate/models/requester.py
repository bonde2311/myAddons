from odoo import models, fields

class Requester(models.Model):
    _name = "custom.requester"
    _description = "Requester Master"

    name = fields.Char(string="Requester Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
