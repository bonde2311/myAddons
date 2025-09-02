from odoo import api, fields, models


class SchoolClass(models.Model):
    _name = "school.classes"
    _description = "Class Records"

    name = fields.Char(string='Class Name', required=True)
    code = fields.Char(string='Code', required=True)
    cls_active = fields.Boolean(string='Class Status', default=True)

    # Relationships
    rel_student_id = fields.One2many('school.student', 'rel_class_id', string="Students")
    rel_admission_id = fields.Many2one('school.admission', 'rel_class_id')
    rel_department_id = fields.Many2one('school.department', string='Under Departments', required=True)
    rel_division_id = fields.One2many('school.division', 'rel_class_id', string='Under Divisions')

    # rel_division_id = fields.Many2many(
    #     'school.division',
    #     'class_division_rel',
    #     'class_id',
    #     'division_id',
    #     string='Under Divisions'
    # )