# from odoo import models, fields, api
#
#
# class MovieContract(models.Model):
#     _name = 'movie.contract'
#     _description = 'Actor/Crew Contract'
#     _order = 'start_date desc'
#
#
#     name = fields.Char(string="Contract Title", required=True)
#     production_id = fields.Many2one('movie.production', string="Production", required=True)
#
#     actor_id = fields.Many2one('movie.actor', string="Actor")
#     crew_id = fields.Many2one('movie.crew', string="Crew Member")
#     theatre_id = fields.Many2one('movie.theatre', string="Theatre")
#     ott_platform_id = fields.Many2one('movie.ott.platform', string="OTT Platform")
#     partner_id = fields.Many2one('res.partner', string="Partner")
#
#     start_date = fields.Date(string="Start Date", required=True)
#     end_date = fields.Date(string="End Date")
#
#     contract_type = fields.Selection([
#         ('full_time', 'Full Time'),
#         ('part_time', 'Part Time'),
#         ('temporary', 'Temporary'),
#         ('freelancer', 'Freelancer'),
#     ], string="Contract Type", default='temporary')
#
#     agreed_amount = fields.Monetary(string="Agreed Amount", required=True)
#     currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
#
#     terms = fields.Text(string="Terms and Conditions")
#     status = fields.Selection([
#         ('draft', 'Draft'),
#         ('active', 'Active'),
#         ('completed', 'Completed'),
#         ('terminated', 'Terminated'),
#     ], string="Status", default='draft')
#
#     signed = fields.Boolean(string="Signed", default=False)
#     notes = fields.Text(string="Notes")
#
#     payment_ids = fields.One2many('movie.payment', 'contract_id', string="Payments")
#
#
# class MoviePayment(models.Model):
#     _name = 'movie.payment'
#     _description = 'Contract Payment'
#     _order = 'payment_date desc'
#
#     contract_id = fields.Many2one('movie.contract', string="Contract", required=True, ondelete='cascade')
#     production_id = fields.Many2one(related='contract_id.production_id', store=True)
#
#     actor_id = fields.Many2one(related='contract_id.actor_id', store=True)
#     crew_id = fields.Many2one(related='contract_id.crew_id', store=True)
#
#     payment_type = fields.Selection([
#         ('salary', 'Salary'),
#         ('advance', 'Advance'),
#         ('bonus', 'Bonus'),
#         ('other', 'Other')
#     ], string="Payment Type", required=True)
#
#     total_amount = fields.Monetary(string="Amount", required=True)
#     currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
#
#     payment_date = fields.Date(string="Payment Date", default=fields.Date.today)
#     is_paid = fields.Boolean(string="Is Paid?", default=True)
#     remarks = fields.Text(string="Remarks")
#
#     remaining_amount = fields.Monetary(string="Remaining Amount", compute='_compute_remaining', store=True)
#
#     @api.depends('contract_id.agreed_amount', 'contract_id.payment_ids.amount', 'contract_id.payment_ids.is_paid')
#     def _compute_remaining(self):
#         for payment in self:
#             if not payment.contract_id:
#                 payment.remaining_amount = 0
#                 continue
#
#             # Total paid up to this payment (ordered by date)
#             sorted_payments = payment.contract_id.payment_ids.filtered(
#                 lambda p: p.is_paid
#             ).sorted(key=lambda p: (p.payment_date or fields.Date.today(), p.id))
#
#             total_paid = 0.0
#             for p in sorted_payments:
#                 total_paid += p.amount
#                 if p.id == payment.id:
#                     break
#
#             payment.remaining_amount = payment.contract_id.agreed_amount - total_paid
