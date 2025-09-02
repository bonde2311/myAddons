# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'School Student Records'

    _rec_name = "student_id"
    student_id = fields.Char(string="Student ID", required=True, copy=False, readonly=True, default=lambda self: 'New')
    student_name = fields.Char(string="Student Name", required=True)
    profile_pic = fields.Binary(string="Profile Picture", attachment=True, store=True)
    student_sign = fields.Binary(string="Student Sign", attachment=True, store=True)
    email = fields.Char(string="Email ID", required=True)
    mobile_no = fields.Char(string="Mobile Number", required=True, store=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string="Gender",
    )
    birth_date = fields.Date(string="Birthdate", required=True)
    age = fields.Integer(string="Age", required=True)
    aadhar_file = fields.Binary(string="Upload Aadhar Card: ", attachment=True, )
    pan_card = fields.Binary(string="Pan Card:(Optional) ", attachment=True, )
    father_name = fields.Text(string="Father Name: ")
    mother_name = fields.Text(string="Mother Name: ")

    # Relationships
    rel_teacher_id = fields.Many2one('school.teacher', string="Assigned Teacher")
    rel_subject_id = fields.Many2one('school.subject', string='Assigned Subject')
    rel_department_id = fields.Many2one('school.department', string='Department')
    rel_class_id = fields.Many2one('school.classes', string="Class")
    rel_division_id = fields.Many2one('school.division', string='Assigned Division')

    # Relating One-to-Many (Many2one with unique constraint)
    # rel_student_qualification_id = fields.One2many('student.qualification', 'rel_student_id', string="Qualifications")
    rel_admission_id = fields.One2many('school.admission', 'rel_student_id', string="Admission")
    rel_attendance_id = fields.One2many('school.attendance', 'rel_student_id', string='Assigned Attendance')
    rel_fees_id = fields.One2many('school.fees', 'rel_student_id', string='Fees Structure')

    # for auto student id generator
    @api.model
    def create(self, vals):
        if vals.get('student_id', 'New') == 'New':  # Only assign if 'New'
            vals['student_id'] = self.env['ir.sequence'].next_by_code('school.student') or 'New'
            vals['student_name'] = vals['student_name'].upper()
            vals['email'] = vals['email'].lower()
        return super(SchoolStudent, self).create(vals)

    # @api.onchange('student_name')
    # def _onchange_student_name(self):
    #     if self.student_name:
    #         self.student_name = self.student_name.upper()

    # Filter selection based on department
    @api.onchange('rel_department_id')
    def _onchange_rel_department_id(self):
        for cls in self:
            return {'domain': {'rel_class_id': [('rel_department_id', '=', cls.rel_department_id.id)]}}