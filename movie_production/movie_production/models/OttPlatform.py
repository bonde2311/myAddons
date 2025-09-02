from odoo import models, fields

# Durgesh Bagul & Gaurav Bonde (22/05/2025)
class OttPlatform(models.Model):
    _name = 'ott.platform'
    _description = 'OTT Platform'

    name = fields.Char(string="Platform Name", required=True)
    platform = fields.Char(string="Provider")
    website = fields.Char(string="Website URL")
    subscription_type = fields.Selection([
        ('free', 'Free'),
        ('subscription', 'Subscription'),
        ('pay_per_view', 'Pay Per View')
    ], string="Subscription Type")
    contact_email = fields.Char(string="Contact Email")
    logo = fields.Image(string="Platform Logo")
    active = fields.Boolean(default=True)

    production_ids = fields.Many2many('movie.production', string="Available Productions")