from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MovieSponsor(models.Model):
    _name = 'movie.sponsor'
    _description = 'Sponsor / Brand Partner'

    name = fields.Char(string='Sponsor Name', required=True)
    company_name = fields.Char(string='Company Name')
    logo = fields.Image(string="Logo")
    contact_person = fields.Char(string='Contact Person')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    website = fields.Char(string='Website')

    sponsor_type = fields.Selection([
        ('finance', 'Finance'),
        ('brand', 'Brand Collaboration'),
        ('product', 'Product Placement'),
        ('media', 'Media Sponsor'),
    ], string='Sponsorship Type')

    # Dynamic Flags
    is_finance = fields.Boolean(compute='_compute_type_flags', store=True)
    is_brand = fields.Boolean(compute='_compute_type_flags', store=True)
    is_product = fields.Boolean(compute='_compute_type_flags', store=True)
    is_media = fields.Boolean(compute='_compute_type_flags', store=True)

    @api.depends('sponsor_type')
    def _compute_type_flags(self):
        for rec in self:
            rec.is_finance = rec.sponsor_type == 'finance'
            rec.is_brand = rec.sponsor_type == 'brand'
            rec.is_product = rec.sponsor_type == 'product'
            rec.is_media = rec.sponsor_type == 'media'

    # Finance fields
    finance_payment_mode = fields.Selection([('cash', 'Cash'), ('bank', 'Bank Transfer'), ('cheque', 'Cheque')],
                                            string="Payment Mode", default='cash')


    # Brand Collaboration fields
    brand_product = fields.Char("Product Name")
    brand_logo = fields.Binary("Brand Logo")
    brand_duration = fields.Char("Collaboration Duration")
    brand_mention_type = fields.Selection([('verbal', 'Verbal'), ('visual', 'Visual'), ('both', 'Both')], string="Mention Type")
    brand_social_handles = fields.Char("Brand Introducer Name")

    # Product Placement fields
    product_name = fields.Char("Product Name")
    product_category = fields.Char("Category")
    product_quantity_provided = fields.Integer("Quantity Provided")
    product_used_scenes = fields.Text("Used in Scenes")

    # Media Sponsor fields
    media_channel = fields.Char("Channel Name")
    media_airing_schedule = fields.Text("Airing Schedule")
    media_ad_type = fields.Selection([('banner', 'Banner'), ('video', 'Video'), ('scroll', 'Scroll Text')], string="Ad Type")
    media_slot_duration = fields.Float("Slot Duration (sec)")
    media_total_slots = fields.Integer("Total Slots")


    # Payment Fields
    sponsorship_amount = fields.Float(string="Total Sponsorship Amount")
    paid_amount = fields.Float(string="Paid Amount")
    due_amount = fields.Float(string="Due Amount", compute='_compute_due_amount', store=True)
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid')
    ], string="Payment Status", default='pending')
    payment_terms = fields.Text(string="Payment Terms")

    # Legal
    contract_signed = fields.Boolean(string="Contract Signed?")
    contract_number = fields.Char(string="Contract Number")
    agreement_date = fields.Date(string="Agreement Date")
    contract_attachment = fields.Binary(string="Contract Document")
    contract_attachment_name = fields.Char(string="Contract File Name")

    # Other
    notes = fields.Text(string='Notes')
    production_ids = fields.Many2many('movie.production', string="Movie Productions")
    # Visibility control flags
    show_cash_fields = fields.Boolean(compute='_compute_payment_mode_flags', store=True)
    show_cheque_fields = fields.Boolean(compute='_compute_payment_mode_flags', store=True)
    show_bank_fields = fields.Boolean(compute='_compute_payment_mode_flags', store=True)

    # Common Fields
    finance_bank_name = fields.Char("Bank Name")
    finance_account_number = fields.Char("Account Number")

    # Cash-specific
    cash_amount = fields.Float("Cash Amount")
    cash_paid_by = fields.Float("Cash Paid By")
    cash_receipt_number = fields.Char("Cash Receipt Number")


    # Cheque-specific
    cheque_number = fields.Char("Cheque Number")
    cheque_holder_name = fields.Char("Cheque Holder Name")
    cheque_amount = fields.Integer("Cheque Amount")
    cheque_date = fields.Date("Cheque Date")
    cheque_due_date = fields.Date("Cheque Due Date")

    # Bank Transfer-specific
    account_number = fields.Integer("Bank Account Number")
    bank_transfer_amount = fields.Integer("Bank Transfer Amount")
    transfer_by = fields.Char("Transferred By")
    transaction_id = fields.Char("Transaction ID")
    transfer_date = fields.Date("Transfer Date")


    @api.depends('sponsorship_amount', 'paid_amount')
    def _compute_due_amount(self):
        for sponsor in self:
            sponsor.due_amount = max(sponsor.sponsorship_amount - sponsor.paid_amount, 0)

    @api.onchange('paid_amount', 'sponsorship_amount')
    def _onchange_payment_status(self):
        for sponsor in self:
            if sponsor.paid_amount > sponsor.sponsorship_amount:
                sponsor.paid_amount = sponsor.sponsorship_amount
                return {
                    'warning': {
                        'title': "Invalid Paid Amount",
                        'message': "Paid amount cannot exceed the total sponsorship amount.",
                    }
                }
            if sponsor.paid_amount <= 0:
                sponsor.payment_status = 'pending'
            elif sponsor.paid_amount < sponsor.sponsorship_amount:
                sponsor.payment_status = 'partial'
            else:
                sponsor.payment_status = 'paid'

    @api.depends('finance_payment_mode')
    def _compute_payment_mode_flags(self):
        for rec in self:
            rec.show_cash_fields = rec.finance_payment_mode == 'cash'
            rec.show_cheque_fields = rec.finance_payment_mode == 'cheque'
            rec.show_bank_fields = rec.finance_payment_mode == 'bank_transfer'

    @api.onchange('finance_payment_mode')
    def _onchange_payment_mode(self):
        self._compute_payment_mode_flags()

    @api.constrains('paid_amount', 'sponsorship_amount')
    def _check_paid_amount(self):
        for sponsor in self:
            if sponsor.paid_amount > sponsor.sponsorship_amount:
                raise ValidationError("Paid amount cannot exceed the total sponsorship amount.")
