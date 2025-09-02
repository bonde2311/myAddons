from odoo import models, fields, api
from datetime import date

class MovieContract(models.Model):
    _name = 'movie.contract'
    _description = 'Movie Distribution Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    name = fields.Char(
        string="Contract Reference", required=True, copy=False, readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('movie.contract')
    )

    contract_type = fields.Selection([
        ('theatre', 'Theatre'),
        ('ott', 'OTT Platform'),
        ('actor', 'Actor'),
        ('crew', 'Crew')
    ], string="Contract Type", required=True)

    production_id = fields.Many2one('movie.production', string="Movie / Production", required=True)

    # Conditional fields
    theatre_id = fields.Many2one('movie.theatre', string="Theatre", domain="[('active', '=', True)]")
    ott_platform_id = fields.Many2one('ott.platform', string="OTT Platform", domain="[('active', '=', True)]")
    actor_id = fields.Many2one('movie.actor', string="Actor", domain="[('active', '=', True)]")
    crew_id = fields.Many2one('movie.crew', string="Crew Member", domain="[('active', '=', True)]")

    partner_id = fields.Many2one('res.partner', string="Contract Party", required=True)
    contract_date = fields.Date(string="Contract Signed Date", default=fields.Date.context_today)
    start_date = fields.Date(string="Release / Start Date", required=True)
    end_date = fields.Date(string="Contract End Date", required=True)

    contract_file = fields.Binary(string="Upload Contract File")
    contract_file_name = fields.Char(string="Filename")

    contract_terms = fields.Text(string="Contract Terms and Conditions")
    payment_terms = fields.Text(string="Payment Terms")
    amount_total = fields.Float(string="Total Contract Value")

    is_renewable = fields.Boolean(string="Renewable Contract?")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled')
    ], string="Contract Status", default='draft', tracking=True)

    status_message = fields.Char(string="Status Message", compute="_compute_status_message", store=True)
    signed_by = fields.Many2one('res.users', string="Signed By", default=lambda self: self.env.user)
    notes = fields.Text(string="Internal Notes")

    @api.depends('start_date', 'end_date')
    def _compute_status_message(self):
        today = date.today()
        for rec in self:
            if rec.start_date and rec.end_date:
                if today < rec.start_date:
                    rec.status_message = "Contract not yet started"
                    rec.status = 'draft'
                elif rec.start_date <= today <= rec.end_date:
                    rec.status_message = "Contract is Active"
                    rec.status = 'active'
                elif today > rec.end_date:
                    rec.status_message = "Contract has Ended"
                    rec.status = 'closed'
            else:
                rec.status_message = "Missing contract dates"

    @api.onchange('contract_type')
    def _onchange_contract_type(self):
        if self.contract_type == 'theatre':
            self.ott_platform_id = False
            self.actor_id = False
            self.crew_id = False
        elif self.contract_type == 'ott':
            self.theatre_id = False
            self.actor_id = False
            self.crew_id = False
        elif self.contract_type == 'actor':
            self.crew_id = False
        elif self.contract_type == 'crew':
            self.actor_id = False
