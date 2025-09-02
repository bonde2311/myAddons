from odoo import models, fields

# Durgesh Bagul & Gaurav Bonde (23/05/2025)

class MovieProductionHouse(models.Model):
    _name = 'movie.production.house'
    _description = 'Production House'

    name = fields.Char(string="Production House Name", required=True)
    owner_name = fields.Char(string="Owner Name")
    address = fields.Text(string="Address")
    city = fields.Char(string="City")
    state = fields.Char(string="State")
    country = fields.Many2one('res.country', string="Country")
    email = fields.Char(string="Email")
    contact = fields.Char(string="Contact Number")
    website = fields.Char(string="Website")
    established_date = fields.Date(string="Established Date")
    logo = fields.Image(string="Logo")
    biography = fields.Html(string="About the Production House")
    is_active = fields.Boolean(string="Is Active", default=True)

    # Relations
    production_ids = fields.One2many('movie.production', 'production_house_id', string="Produced Movies")
