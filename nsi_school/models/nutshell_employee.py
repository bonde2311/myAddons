from odoo import fields, models, api


class NutshellEmployee(models.Model):
    _name = 'nutshell.employee'
    _description = 'Nutshell Employee'


    name = fields.Char('Employee Name:')
    emp_pic = fields.Binary(string="Employee Pic", attachment=True, store=True)

    # emp_id = fields.Char('Employee ID:', required=True, copy=False, readonly=True, default=lambda self: 'New')
    mobile_no = fields.Char('Mobile No:')
    work_email = fields.Char('Work Email:')
    email = fields.Char('Email:')
    department = fields.Selection(
        [('development', 'Development'), ('testing', 'Testing'), ('designer', 'UI/UX Designer')],
        string="Department")
    position = fields.Selection(
        [('intern', 'Intern'), ('hr', 'Hr'), ('jr_developer', 'Jr Developer')],
        string="Position")
    city = fields.Char('City')
    pincode = fields.Char('Pincode')

    # Relationships
    rel_nutshell_letters = fields.One2many('nutshell.letters', 'rel_emp_id', string="Nutshell Letter:")