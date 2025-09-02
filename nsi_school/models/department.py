from odoo import api, fields, models

class SchoolDepartment(models.Model):
    _name = "school.department"
    _description = "School Department Records"
    _rec_name = "dep_name"

    dep_name = fields.Char(string='Department Name', required=True)
    dep_Code = fields.Char(string='Department Code', required=True)
    description = fields.Text(string='Description')

    # Relationships
    rel_teacher_id = fields.One2many('school.teacher','rel_department_id', string='Under Teacher')
    rel_student_id = fields.One2many('school.student','rel_department_id', string='Students')
    # rel_class_id = fields.Many2many('school.classes', 'rel_department_id', 'rel_department_id','class_id',string='Under Classes')
    rel_class_id = fields.One2many('school.classes', 'rel_department_id', string='Under Classes')