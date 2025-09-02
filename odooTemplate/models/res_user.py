from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_company_ids = fields.Many2many(
        'company.master',
        string='Legal Initiation Companies'
    )
