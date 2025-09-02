from odoo import models, fields

class CompanyMaster(models.Model):
    _name = 'company.master'
    _description = 'Company Master'

    name = fields.Char(string="Company Name", required=True)
    address = fields.Char(string="Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    user_ids = fields.Many2many(
        'res.users',
        'res_users_company_master_rel',
        'company_id',
        'user_id',
        string='Assigned Users',
        compute='_compute_user_ids',
        store=False
    )

    def _compute_user_ids(self):
        for record in self:
            record.user_ids = self.env['res.users'].search([
                ('allowed_company_ids', 'in', record.id)
            ])



