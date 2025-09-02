from odoo import api, fields, models

class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "School Teacher Records"
    _rec_name = "teacher_name"

    # name = fields.Char(string='Teacher Name', required=True)
    teacher_id = fields.Char(string='Teacher ID:', required=True, copy=False, readonly=True, default=lambda self: 'New')
    teacher_name = fields.Char(string='Teacher Name', required=True)
    email = fields.Char(string='Email ID:', required=True)
    mobile_no = fields.Char(string='Mobile Number:', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    teacher_pic = fields.Binary(string="Teacher Picture", attachment=True, store=True)
    teacher_sign = fields.Binary(string="Teacher Sign", attachment=True, store=True)


    # Relationships
    rel_attendance_id = fields.One2many('school.attendance', 'rel_teacher_id', string='Assigned Attendance')
    rel_student_id = fields.One2many('school.student', 'rel_teacher_id', string='Assigned Teacher')

    rel_department_id = fields.Many2one('school.department', string='Department')

    rel_subject_id = fields.Many2many('school.subject', 'teacher_subject_rel',
                                      'teacher_id', 'subject_id',
                                      string='Subject Specialist')

    # for auto teacher id generator
    @api.model
    def create(self, vals):
        if vals.get('teacher_id', 'New') == 'New':  # Only assign if 'New'
            vals['teacher_id'] = self.env['ir.sequence'].next_by_code('school.teacher') or 'New'
            vals['teacher_name'] = vals['teacher_name'].upper()
            vals['email'] = vals['email'].lower()
        return super(SchoolTeacher, self).create(vals)