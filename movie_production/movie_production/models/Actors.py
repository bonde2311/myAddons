from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

# Durgesh Bagul & Gaurav Bonde (20/05/2025)

class MovieActor(models.Model):
    _name = 'movie.actor'
    _description = 'Movie Actor'

    name = fields.Char(string="Full Name", required=True)
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    nationality = fields.Char(string="Nationality")
    contact_number = fields.Char(string="Contact Number")
    email = fields.Char(string="Email")
    act_Image = fields.Image(string="Actor Image")
    address = fields.Text(string="Address")
    biography = fields.Text(string="Biography")
    cast = fields.Text(string="Cast Description")
    manager_contact = fields.Char(string="Manager Contact")
    is_active = fields.Boolean(string="Currently Active", default=True)
    active = fields.Boolean(string="Active", default=True)

    production_id = fields.Many2many('movie.production', string="Associated Productions")
    schedule_ids = fields.Many2many('movie.schedule', string="Scheduled Scenes")
    portfolio_id = fields.One2many('actor.portfolio', 'actor_id', string='Portfolios')
    role_ids = fields.One2many('movie.actor.role', 'actor_ids', string="Actor Roles")

    employee_id = fields.Many2one('hr.employee', string="Related Employee", readonly=True)
    attendance_ids = fields.One2many('movie.attendance', 'actor_id', string='Attendances')

    @api.depends('dob')
    def _compute_age(self):
        today = date.today()
        for actor in self:
            if actor.dob and actor.dob <= today:
                age = today.year - actor.dob.year
                if (today.month, today.day) < (actor.dob.month, actor.dob.day):
                    age -= 1
                actor.age = max(age, 0)
            else:
                actor.age = 0

    @api.constrains('dob')
    def _check_dob(self):
        for actor in self:
            if actor.dob and actor.dob > fields.Date.today():
                raise ValidationError("Date of Birth cannot be in the future.")

    @api.model
    def create(self, vals):
        actor = super(MovieActor, self).create(vals)

        employee_vals = {
            'name': actor.name,
            'work_email': actor.email,
            'work_phone': actor.contact_number,
            'job_title': "Actor",
            'image_1920': actor.act_Image,
        }
        employee = self.env['hr.employee'].create(employee_vals)
        actor.employee_id = employee.id

        return actor
