from odoo import models, fields

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    planned_date = fields.Datetime(string='Planned Date')
