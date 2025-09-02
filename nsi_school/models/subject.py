from odoo import api, fields, models


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject Records'

    name = fields.Char(string='Subject Name', required=True)
    sub_code = fields.Char(string='Subject Code', required=True)

    # Relationships
    rel_teacher_id = fields.Many2many('school.teacher', 'teacher_subject_rel',
                                      'subject_id', 'teacher_id',
                                      string='Assigned Teachers')

    # @api.onchange('name')
    # def _onchange_subject_name(self):
    #     if self.name:s
    #         self.name = self.name.upper()
    #
    # @api.onchange('sub_code')
    # def _onchange_subject_code(self):
    #     if self.sub_code:
    #         self.sub_code = self.sub_code.upper()

    # when we used a create method that time in ui rapidly not seen the upper and lower case its shown only in tree
    @api.model
    def create(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].upper()  # Convert to uppercase
        if vals.get('sub_code'):
            vals['sub_code'] = vals['sub_code'].upper()  # Convert to uppercase
        return super(SchoolSubject, self).create(vals)
