import logging
from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class SchoolAdmission(models.Model):
    _name = "school.admission"
    _description = "Admission Records"

    name = fields.Char(string='Admission ID', required=True, copy=False, readonly=True, default=lambda self: 'New')
    date = fields.Date(string='Admission Date', default=fields.Date.today)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('under_verification', 'Under Verification'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='pending')

    # Relationships
    rel_student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade', index=True)
    # rel_student_qualification_id = fields.One2many('student.qualification', 'rel_student_id',
    #                                                string='Student Qualifications')
    # rel_department_id = fields.Many2one('school.department', string='Department:', required=True)
    # rel_class_id = fields.Many2one('school.classes', string='Class:', required=True)
    rel_division_id = fields.Many2one('school.division', string='Assigned Division:', required=True)
    rel_fees_id = fields.One2many('school.fees', 'rel_admission_id')
    rel_attendance_id = fields.One2many('school.attendance', 'rel_admission_id', string='Attendance Records')

    # Fields for showing data
    # ssc_details = fields.Char(string="SSC Details", compute="_compute_qualifications_summary", store=True)
    # hsc_details = fields.Char(string="HSC Details", compute="_compute_qualifications_summary", store=True)
    # graduation_details = fields.Char(string="Graduation Details", compute="_compute_qualifications_summary", store=True)
    # post_graduation_details = fields.Char(string="Post Graduation Details", compute="_compute_qualifications_summary",
    #                                       store=True)

    student_id = fields.Char(string='Student ID')
    # qualification_id = fields.Char(string='qualification ID')
    student_name = fields.Char(string='Student Name')
    profile_pic = fields.Image(string="Student Image", compute="_compute_image", store=True)
    student_sign = fields.Image(string="Student Signature", compute="_compute_image", store=True)
    student_email = fields.Char(string="Email ID")
    student_mobile_no = fields.Char(string="Mobile Number")
    student_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    student_age = fields.Integer(string="Age")
    student_birth_date = fields.Date(string="Birthdate")
    student_dep = fields.Char(string='Department')
    student_cls = fields.Char(string='Class')

    @api.onchange('rel_student_id')
    def _onchange_rel_student_id(self):
        """Show a popup message if the student is already admitted."""
        if self.rel_student_id:
            # Check if the student is already admitted
            existing_admissions = self.env['school.admission'].search([('rel_student_id', '=', self.rel_student_id.id)])
            if existing_admissions:
                raise UserError(
                    f"Student '{self.rel_student_id.student_name}' is already admitted.\n\nClick OK to continue.")

            # Fetch values from student ID using relationship
            self.student_id = self.rel_student_id.student_id
            self.student_name = self.rel_student_id.student_name
            self.student_email = self.rel_student_id.email
            self.student_mobile_no = self.rel_student_id.mobile_no
            self.student_gender = self.rel_student_id.gender
            self.student_age = self.rel_student_id.age
            self.student_birth_date = self.rel_student_id.birth_date
            self.student_dep = self.rel_student_id.rel_department_id.dep_name
            self.student_cls = self.rel_student_id.rel_class_id.name

    # function for fetch student image & sign dynamic in admission model from student model
    @api.depends('rel_student_id')
    def _compute_image(self):
        for record in self:
            record.profile_pic = record.rel_student_id.profile_pic if record.rel_student_id else False
            record.student_sign = record.rel_student_id.student_sign if record.rel_student_id else False

    # Auto admission ID generator
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('school.admission') or ''
        admission = super(SchoolAdmission, self).create(vals)

        # Update student with admission information
        if admission.rel_student_id:
            admission.rel_student_id.write({
                # 'rel_class_id': admission.rel_class_id.id,
                # 'rel_department_id': admission.rel_department_id.id,
                'rel_division_id': admission.rel_division_id.id,
            })
        return admission

    def write(self, vals):
        result = super(SchoolAdmission, self).write(vals)

        for admission in self:
            if admission.rel_student_id:
                admission.rel_student_id.write({
                    # 'rel_class_id': admission.rel_class_id.id,
                    # 'rel_department_id': admission.rel_department_id.id,
                    'rel_division_id': admission.rel_division_id.id,
                })
        return result

    # unlike means remove student academic data if admission is cancel
    def unlink(self):
        for admission in self:
            if admission.rel_student_id:
                admission.rel_student_id.write({
                    'rel_class_id': False,
                    'rel_department_id': False,
                    'rel_division_id': False,
                })

        result = super(SchoolAdmission, self).unlink()
        return result

    # SQL constraint to ensure only one admission per student
    _sql_constraints = [
        ('unique_student_admission', 'unique(rel_student_id)', 'This student is already admitted.')
    ]

    # Filter selection based on cls
    @api.onchange('student_cls')
    def _onchange_student_cls(self):
        for divs in self:
            return {'domain': {'rel_division_id': [('rel_class_id', '=', divs.student_cls)]}}

    # Function for fetch all qualification details
    # Function to fetch all qualification details in dictionary format
    # @api.depends('rel_student_id')
    # def _compute_qualifications_summary(self):
    #     for record in self:
    #         qualifications = self.env['student.qualification'].search([
    #             ('rel_student_id', '=', record.rel_student_id.id)
    #         ])
    #
    #         qualification_dict = {'ssc': {}, 'hsc': {}, 'graduation': {}, 'post_graduation': {}}
    #
    #         for q in qualifications:
    #             qualification_info = {
    #                 'board_university': q.board_university or 'N/A',
    #                 'passing_year': q.passing_year or 'N/A',
    #                 'percentage': f"{q.percentage}%" if q.percentage else 'N/A',
    #                 'course_name': q.course_name if q.qualification_type in ['graduation', 'post_graduation'] else '',
    #                 'specialization': q.specialization if q.qualification_type in ['graduation',
    #                                                                                'post_graduation'] else '',
    #                 'college_name': q.college_name if q.qualification_type in ['graduation', 'post_graduation'] else ''
    #             }
    #
    #             if q.qualification_type in qualification_dict:
    #                 qualification_dict[q.qualification_type] = qualification_info
    #
    #         # Ensure it's a dictionary, not None or an empty string
    #         record.ssc_details = qualification_dict['ssc'] if qualification_dict['ssc'] else {}
    #
    #         _logger.info(f"Updated SSC Details: {record.ssc_details}")  # Debugging