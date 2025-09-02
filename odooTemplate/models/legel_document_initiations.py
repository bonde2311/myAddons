# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from lxml import etree


class LegelDocumentInitiations(models.Model):
    _name = 'legel.document.initiations'
    _description = 'Sample Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Sequence", default=lambda self: _('New'),
                       help='Sequence number for the visiting')

    # document_type = fields.Selection([
    #     ('nda', 'NDA'),
    #     ('quote_form', 'Quote Form'),
    #     ('msa', 'MSA - Master Service Agreement'),
    #     ('support_maintenance', 'Support Maintenance Agreement'),
    #     ('test_agreement', 'Test Agreement'),
    #     ('eula', 'EULA'),
    #     ('independent_contract', 'Independent Contract - 1099'),
    #     ('ncnr', 'NCNR'),
    #     ('mou', 'MOU'),
    #     ('loi', 'LOI'),
    #     ('other', 'Other'),
    #     ('patent', 'Patent'),
    #     ('trademark', 'Trademark'),
    #     ('partnership_agreement', 'Partnership Agreement'),
    #     ('evaluation_agreement', 'Evaluation Agreement'),
    # ], string="Document Type")

    document_type_id = fields.Many2one(
        'document.type',
        string="Document Type",
        domain="[('company_ids', 'in', rel_company_ids)]"
    )



    rel_partner_id = fields.Many2one('custom.partner', string="Customer/Vendor")
    # rel_partner_id = fields.Many2one('res.partner', string="Customer/Vendor")

    subject = fields.Char(string="Subject")
    purpose = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External'),
    ], string="Purpose")

    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string="Priority", default="medium")

    screening_complete = fields.Boolean(string="Screening Complete - 1099 Only")

    rel_company_ids = fields.Many2many(
        'company.master',
        'legel_doc_company_rel',
        'document_id',
        'company_id',
        string="Company Name",
        domain=lambda self: [('id', 'in', self.env.user.allowed_company_ids.ids)]
    )

    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('confirmed', 'Confirmed'),
    #     ('done', 'Done')
    # ], string='State', default='draft', tracking=True)

    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string="Status", default="draft")

    requested_delivery_date = fields.Date(string="Requested Delivery Date")
    rel_requester_id = fields.Many2one("custom.requester", string="Requester")

    legal_review_inprogress = fields.Boolean(string="Legal Review InProgress")
    legal_review_completed = fields.Boolean(string="Legal Review Completed")
    signed = fields.Boolean(string="Signed")
    countersigned = fields.Boolean(string="Counter signed")

    # Comments
    user_comments = fields.Text(string="User Description/Comments")
    legal_comments = fields.Text(string="Legal Comments")

    # Terms
    terms = fields.Char(string="Terms")
    term_expiration_date = fields.Date(string="Term Expiration Date")
    confidentiality_terms = fields.Char(string="Confidentiality Terms (NDA only)")
    confidentiality_term_expiration_date = fields.Date(string="Confidentiality Term Expiration Date")



    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])

        for node in doc.xpath("//field[@name='rel_company_ids']"):
            allowed_ids = self.env.user.allowed_company_ids.ids
            node.set('domain', "[('id', 'in', %s)]" % allowed_ids)

        res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """Creating sequence"""
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'legel.document.initiations') or _('New')
        return super().create(vals_list)



