from odoo import _, api, fields, models

class DocumentType(models.Model):
    _name = "document.type"
    _description = "Document Type"

    name = fields.Char(string="Document Type", required=True)
    # code = fields.Selection([...])  # if you still want to store a fixed code
    company_ids = fields.Many2many('company.master', string="Allowed Companies")

    # code = fields.Selection([
    #     ('nda', 'NDA'),
    #     ('msa', 'MSA'),
    #     ('eula', 'EULA'),
    #     # ... more ...
    # ], string="Code")