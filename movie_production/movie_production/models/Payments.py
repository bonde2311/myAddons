from odoo import models, fields, api

class MoviePaymentLine(models.Model):
    _name = 'movie.payment.line'
    _description = 'Actor and Crew Payment Line'

    production_id = fields.Many2one('movie.production', string='Movie', ondelete='cascade')

    crew_id = fields.Many2one('movie.crew', string='Crew Name', ondelete='cascade')
    actor_id = fields.Many2one('movie.actor', string='Actor Name', ondelete='cascade')

    is_actor = fields.Boolean(string="Is Actor", compute='_compute_type_flags', store=True)
    is_crew = fields.Boolean(string="Is Crew", compute='_compute_type_flags', store=True)

    role = fields.Selection([
        ('actor', 'Actor'),
        ('crew', 'Crew'),
    ], string='Role', required=True)

    total_amount = fields.Float(string='Total Agreed Payment', required=True)
    advance_paid = fields.Float(string='Advance Paid')
    other_deductions = fields.Float(string='Other Deductions')

    remaining_amount = fields.Float(string='Remaining Payment', compute='_compute_remaining', store=True)
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
    ], string='Payment Status', compute='_compute_status', store=True)

    @api.depends('role')
    def _compute_type_flags(self):
        for rec in self:
            rec.is_actor = rec.role == 'actor'
            rec.is_crew = rec.role == 'crew'

    @api.depends('total_amount', 'advance_paid', 'other_deductions')
    def _compute_remaining(self):
        for rec in self:
            rec.remaining_amount = max(0.0, rec.total_amount - rec.advance_paid - rec.other_deductions)

    @api.depends('remaining_amount', 'total_amount')
    def _compute_status(self):
        for rec in self:
            if rec.remaining_amount == 0:
                rec.payment_status = 'paid'
            elif rec.remaining_amount == rec.total_amount:
                rec.payment_status = 'pending'
            else:
                rec.payment_status = 'partial'
