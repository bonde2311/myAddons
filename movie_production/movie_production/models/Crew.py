from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


# Durgesh Bagul & Gaurav Bonde (21/05/2025)

class MovieCrew(models.Model):
    _name = 'movie.crew'
    _description = 'Crew Member'

    name = fields.Char(string="Name", required=True)

    position_ids = fields.One2many(
        'movie.crew.position',
        'crew_ids',
        string="Crew Positions",
        required=True
    )

    experience = fields.Integer(string="Years of Experience")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)  # ✅ Computed Age Field
    active = fields.Boolean(string="Active", default=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")

    contact = fields.Char(string="Contact Number")
    email = fields.Char(string="Email")
    biography = fields.Text(string="Biography")
    image = fields.Image(string="Photo")
    is_active = fields.Boolean(string="Is Active", default=True)

    attendance_ids = fields.One2many('movie.attendance', 'crew_id', string="Attendances")
    production_ids = fields.Many2many('movie.production', string="Assigned Productions")

    @api.depends('dob')
    def _compute_age(self):
        today = date.today()
        for crew in self:
            if crew.dob and crew.dob <= today:
                age = today.year - crew.dob.year
                if (today.month, today.day) < (crew.dob.month, crew.dob.day):
                    age -= 1
                crew.age = max(age, 0)
            else:
                crew.age = 0

    @api.constrains('dob')
    def _check_dob_not_future(self):
        for crew in self:
            if crew.dob and crew.dob > fields.Date.today():
                raise ValidationError("Date of Birth cannot be in the future.")


class MovieCrewRole(models.Model):
    _name = 'movie.crew.position'
    _description = 'Crew Position'

    name = fields.Char(string="Position Name", required=True)
    description = fields.Text(string="Description")
    is_technical = fields.Boolean(string="Is Technical position?", default=False)
    active = fields.Boolean(string="Active", default=True)

    # Many2many back-reference to crew members
    crew_ids = fields.Many2one(
        'movie.crew',
        string="Crew Members"
    )

