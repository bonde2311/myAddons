from odoo import api, fields, models, exceptions

class SchoolAttendance(models.Model):
    _name = "school.attendance"
    _description = "Attendance Records"

    status = fields.Selection([('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')],
                              string='Status', default='absent')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)

    # Relationships
    _rec_name = "rel_student_id"
    rel_student_id = fields.Many2one('school.student', string='Student ID: ', ondelete='cascade')
    rel_teacher_id = fields.Many2one('school.teacher', string='Subject Teacher')
    # rel_class_id = fields.Many2one('school.classes', string="Select Class")
    # rel_division_id = fields.Many2one('school.division')
    # rel_department_id = fields.Many2one('school.department')
    rel_admission_id = fields.Many2one('school.admission')

    # fields for showing data
    student_name = fields.Char(string="Student Name")
    student_department = fields.Char(string='Student Department:')
    student_class = fields.Char(string='Student Class:')
    student_division = fields.Char(string='Student Division:')
    student_admission_id = fields.Char(string='Student Admission ID:')

    # onchange function its fetch values from student id using reference through relationship
    @api.onchange('rel_student_id')
    def _onchange_rel_student_id(self):
        if self.rel_student_id:
            self.student_name = self.rel_student_id.student_name
            self.student_department = self.rel_student_id.rel_department_id.dep_name
            self.student_class = self.rel_student_id.rel_class_id.name
            self.student_division = self.rel_student_id.rel_division_id.name
            self.student_admission_id = self.rel_student_id.rel_admission_id.name

        # Override create method to prevent saving attendance if admission_id is null

    # @api.model
    # def create(self, vals):
    #     if 'rel_admission_id' not in vals or not vals['rel_admission_id']:
    #         raise exceptions.ValidationError("Cannot save your attendance: Admission ID is required for attendance.")
    #     return super(SchoolAttendance, self).create(vals)
    #
    # # Override write method to prevent updating attendance if admission_id is null
    # def write(self, vals):
    #     if 'rel_admission_id' in vals and not vals['rel_admission_id']:
    #         raise exceptions.ValidationError("Cannot update attendance: Admission ID is required.")
    #     return super(SchoolAttendance, self).write(vals)
    #
    # # Constraint to prevent saving attendance without admission ID
    # _sql_constraints = [
    #     ('check_admission_id_not_null', 'CHECK(rel_admission_id IS NOT NULL)',
    #      'Cannot save your attendance: Admission ID is required for attendance.')
    # ]