from odoo import fields, models, api


class NutshellLetters(models.Model):
    _name = 'nutshell.letters'
    _description = 'Nutshell Letters'

    name = fields.Selection(
        [('offer_letter', 'Offer Letter'), ('joining_letter', 'Joining Letter'),
         ('internship_certification', 'Internship Certification'), ('other_letter', 'Other Letter')],
        string="Letter Type", required=True, store=True, default='offer_letter')

    letter_category = fields.Selection(
        [('internship', 'Internship'), ('job', 'Job')],
        string="Letter Category", default='internship')

    # com_name = fields.Char('Company Name:')
    # com_name = fields.Selection(
    #     [('nutshell', 'Nutshell InfoSoft PVT LTD Nashik(MH)'), ('', '')],
    #     string="Company Name:")

    subject = fields.Char('Subject:')
    join_date = fields.Date('Joining Date:')
    cur_date = fields.Date('Current Date:', default=fields.Date.today)
    acceptance_date = fields.Date('Acceptance Date:')
    location = fields.Char('Company Location:')
    # hr_name = fields.Char('CEO Name:')
    designation = fields.Char(string="Designation:", compute="_compute_employee", store=True)
    header_map = fields.Char()
    current_user_work_email = fields.Char('HR email:')

    # Fields for showing data
    # emp_name = fields.Char('Employee Name:')
    mobile_no = fields.Char('Mobile No:')
    work_email = fields.Char('Work Email:')
    email = fields.Char('Email:')
    department = fields.Selection(
        [('development', 'Development'), ('testing', 'Testing'), ('designer', 'UI/UX Designer')],
        string="Department")
    position = fields.Selection(
        [('intern', 'Intern'), ('hr', 'Hr'), ('jr_developer', 'Jr Developer')],
        string="Position")
    city = fields.Char('City:')
    pincode = fields.Char('Pincode:')

    # Relationships
    company_id = fields.Many2one('res.company', string="Company", ondelete="cascade")
    rel_emp_id = fields.Many2one('nutshell.employee', string="Employee", ondelete="cascade")
    # Relation to get the employee record linked to the user
    employee_id = fields.Many2one('hr.employee', string="Employee", compute="_compute_employee", store=True)
    # Relation to get the logged-in user
    current_user_id = fields.Many2one('res.users', string="Current User", default=lambda self: self.env.user,
                                      readonly=True)

    @api.onchange('rel_emp_id')
    def _onchange_rel_emp_id(self):
        if self.rel_emp_id:
            self.mobile_no = self.rel_emp_id.mobile_no
            self.work_email = self.rel_emp_id.work_email
            self.email = self.rel_emp_id.email
            self.department = self.rel_emp_id.department
            self.position = self.rel_emp_id.position
            self.city = self.rel_emp_id.city
            self.pincode = self.rel_emp_id.pincode

    # Set Fees Amount Based on Fees Type
    @api.onchange("name")
    def _onchange_name(self):
        # letter_mapping = {
        #     "offer_letter": "Offer Letter for Trainee Software Developer – Internship ",
        #     "joining_letter": 'Joining Letter for Trainee Software Developer',
        #     "internship_certification": 'Internship Certificate',
        #     "other_letter": '',
        # }
        # if self.name:
        #     self.subject = letter_mapping.get(self.name)

        header_mapping = {
            "offer_letter": "Nutshell Offer Letter",
            "joining_letter": 'Nutshell Joining Letter',
            "internship_certification": 'Nutshell Internship Certificate',
            "other_letter": 'Nutshell Other letter ',
        }
        if self.name:
            self.header_map = header_mapping.get(self.name)

    #
    show_joining_details = fields.Boolean(compute="_compute_visibility")
    show_certification_details = fields.Boolean(compute="_compute_visibility")
    show_offer_details = fields.Boolean(compute="_compute_visibility")

    #
    @api.depends('name', 'letter_category')
    def _compute_visibility(self):
        for record in self:
            record.show_offer_details = record.name == "offer_letter"
            record.show_joining_details = record.name == "joining_letter"
            record.show_certification_details = record.name == "internship_certification"

    #
    @api.depends('current_user_id')
    def _compute_employee(self):
        """Fetch employee linked to the current user and get their job designation."""
        for record in self:
            employee = self.env['hr.employee'].search([('user_id', '=', record.current_user_id.id)], limit=1)
            record.employee_id = employee.id
            record.designation = employee.job_id.name if employee.job_id else "No Designation"
            record.current_user_work_email = employee.work_email if employee.work_email else "No Email"