from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolFees(models.Model):
    _name = "school.fees"
    _description = "Fees Records"

    name = fields.Char(string='Fee Receipt Num:', required=True, copy=False, readonly=True, default=lambda self: 'New')
    fee_date = fields.Date(string='Fee Date', default=fields.Date.today, required=True)

    fees_type = fields.Selection([
        ('eligibility_fees', 'Eligibility Fees'),
        ('exam_fees', 'Exam Fees'),
        ('admission_fees', 'Admission Fees'),
    ], string='Fees Type', required=True, store=True)

    due_date = fields.Date(string="Due Date")
    total_fee = fields.Float(string="Total Fee", required=True, default=0.0)
    paid_amount = fields.Float(string="Paid Amount", required=True)
    remaining_amount = fields.Float(string="Remaining Amount", compute="_compute_payment_status", store=True)

    payment_status = fields.Selection(
        [('unpaid', 'Unpaid'), ('partially_paid', 'Partially Paid'), ('paid', 'Paid')],
        string="Payment Status",
        compute="_compute_payment_status",
        store=True,
        default="unpaid"
    )

    remark = fields.Char(string='Remark')

    # Relationships
    rel_student_id = fields.Many2one('school.student', string='Student ID')
    # rel_division_id = fields.Many2one('school.division')
    # rel_department_id = fields.Many2one('school.department')
    rel_admission_id = fields.Many2one('school.admission', string='Admission ID', required=True)
    # rel_class_id = fields.Many2one('school.classes')

    # Fields for displaying student information
    student_id = fields.Char(string='Student ID:', store=True)
    student_name = fields.Char(string='Student Name:', store=True)
    student_department = fields.Char(string='Department:', store=True)
    student_class = fields.Char(string='Class:', store=True)
    student_division = fields.Char(string='Division:', store=True)

    # Fetch student details from admission ID
    @api.onchange('rel_admission_id')
    def _onchange_rel_admission_id(self):
        if self.rel_admission_id:
            student = self.rel_admission_id
            self.student_id = student.student_id
            self.student_name = student.student_name
            self.student_department = student.student_dep
            self.student_class = student.student_cls
            self.student_division = student.rel_division_id.name if student.rel_division_id else "No Data"

    # Auto-generate receipt number
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('school.fees') or 'New'
        return super(SchoolFees, self).create(vals)

    # Compute payment status and remaining amount
    @api.depends('total_fee', 'paid_amount')
    def _compute_payment_status(self):
        for record in self:
            if record.paid_amount < 0:
                raise ValidationError("Paid amount cannot be negative.")

            if record.paid_amount == 0:
                record.payment_status = 'unpaid'
            elif round(record.paid_amount, 2) >= round(record.total_fee, 2):  # Avoid floating-point errors
                record.payment_status = 'paid'
                record.remaining_amount = 0.0
            else:
                record.payment_status = 'partially_paid'
                record.remaining_amount = record.total_fee - record.paid_amount

    # Set Fees Amount Based on Fees Type
    @api.onchange("fees_type")
    def _onchange_fees_type(self):
        fees_mapping = {
            "eligibility_fees": 2000,
            "admission_fees": 50000,
            "exam_fees": 4000,
        }
        if self.fees_type and not self.paid_amount:  # Don't change if payment is already made
            self.total_fee = fees_mapping.get(self.fees_type, 0)

    # SQL constraint to ensure paid amount is non-negative
    _sql_constraints = [
        ('paid_amount_positive', 'CHECK (paid_amount >= 0)', 'Paid amount must be zero or positive.')
    ]

    # This function for print receipt
    def action_print_receipt(self):
        if self.payment_status == 'unpaid':
            raise ValidationError("You cannot print a receipt for unpaid fees. Please make a payment first.")
        self.ensure_one()
        return self.env.ref('nsi_school.report_student_fees_action').report_action(self)