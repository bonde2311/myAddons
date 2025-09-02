from odoo import api, fields, models


class SchoolDivision(models.Model):
    _name = "school.division"
    _description = "Division Records"

    name = fields.Char(string='Division', required=True)

    # Relationships
    rel_student_id = fields.One2many('school.student', 'rel_division_id', string='Students')

    rel_class_id = fields.Many2one('school.classes', string='Class')

    # rel_class_id = fields.Many2many(
    #     'school.classes',
    #     'class_division_rel',
    #     'division_id',
    #     'class_id',
    #     string='Under Classes'
    # )