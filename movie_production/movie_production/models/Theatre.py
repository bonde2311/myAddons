from odoo import models, fields,api
from odoo.exceptions import ValidationError
from datetime import datetime


# Durgesh Bagul & Gaurav Bonde (23/05/2025)
class MovieTheatre(models.Model):
    _name = 'movie.theatre'
    _description = 'Theatre'

    name = fields.Char(string="Theatre Name", required=True)
    location = fields.Char(string="Location", required=True)
    screen_count = fields.Integer(string="Number of Screens", required=True)
    seating_capacity = fields.Integer(string="Total Seating Capacity")
    has_3d_screen = fields.Boolean(string="3D Screen Available")
    has_imax = fields.Boolean(string="IMAX Enabled")
    contact_number = fields.Char(string="Contact Number")
    email = fields.Char(string="Email")
    manager_name = fields.Char(string="Manager Name")
    opening_time = fields.Char(string="Opening Time", time=True)
    closing_time = fields.Char(string="Closing Time", time=True)
    active = fields.Boolean(default=True)

    @api.constrains('opening_time', 'closing_time')
    def _check_time_order(self):
        for record in self:
            if record.opening_time and record.closing_time:
                if record.opening_time >= record.closing_time:
                    raise ValidationError("Closing Time must be after Opening Time.")
