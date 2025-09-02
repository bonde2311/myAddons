from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

# Durgesh Bagul & Gaurav Bonde (21/05/2025)

class MovieCateringQuotation(models.Model):
    _name = 'movie.catering.quotation'
    _description = 'Catering Quotation'
    _inherit = ['mail.thread']

    name = fields.Char(string="Quotation Reference", required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('movie.catering.quotation'))
    vendor_id = fields.Many2one('res.partner', string="Vendor", required=True)
    production_id = fields.Many2one('movie.production', string="Production", required=True)
    quotation_date = fields.Date(string="Quotation Date", default=fields.Date.context_today)
    line_ids = fields.One2many('movie.catering.quotation.line', 'quotation_id', string="Quotation Lines")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], string="Status", default='draft', tracking=True)

    def action_send(self):
        if not self.line_ids:
            raise UserError("Please add at least one quotation line before sending.")
        self.state = 'sent'

    def action_accept(self):
        if self.state != 'sent':
            raise UserError("Only sent quotations can be accepted.")
        self.state = 'accepted'

    def action_reject(self):
        if self.state != 'sent':
            raise UserError("Only sent quotations can be rejected.")
        self.state = 'rejected'

    def action_generate_order(self):
        if self.state != 'accepted':
            raise UserError("Only accepted quotations can generate an order.")
        if not self.line_ids:
            raise UserError("Cannot generate order without lines.")

        order = self.env['movie.catering.order'].create({
            'quotation_id': self.id,
            'vendor_id': self.vendor_id.id,
            'production_id': self.production_id.id,
            'order_date': fields.Date.today(),
            'line_ids': [(0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'unit_price': line.unit_price,
            }) for line in self.line_ids]
        })
        return {
            'name': 'Catering Order',
            'type': 'ir.actions.act_window',
            'res_model': 'movie.catering.order',
            'view_mode': 'form',
            'res_id': order.id,
        }


class MovieCateringQuotationLine(models.Model):
    _name = 'movie.catering.quotation.line'
    _description = 'Catering Quotation Line'

    quotation_id = fields.Many2one('movie.catering.quotation', string="Quotation")
    product_id = fields.Many2one('product.product', string="Meal Item", required=True)
    quantity = fields.Integer(string="Plates", default=1)
    unit_price = fields.Float(string="Price per Plate")
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.constrains('quantity', 'unit_price')
    def _check_positive_values(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError("Quantity must be greater than 0.")
            if line.unit_price < 0:
                raise ValidationError("Unit price cannot be negative.")


class MovieCateringOrder(models.Model):
    _name = 'movie.catering.order'
    _description = 'Catering Order'
    _inherit = ['mail.thread']

    name = fields.Char(string="Order Reference", required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('movie.catering.order'))
    order_date = fields.Date(string="Order Date", default=fields.Date.context_today)
    amount_total = fields.Float(string="Total Amount", compute='_compute_total', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval', 'Waiting Approval'),
        ('approved', 'Approved'),
        ('ordered', 'Ordered'),
        ('invoiced', 'Invoiced'),
    ], string="Status", default='draft', tracking=True)

    quotation_id = fields.Many2one('movie.catering.quotation', string="Quotation", ondelete='cascade')
    vendor_id = fields.Many2one('res.partner', string="Vendor", required=True)
    production_id = fields.Many2one('movie.production', string="Production", required=True)
    line_ids = fields.One2many('movie.catering.order.line', 'order_id', string="Order Lines")

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.amount_total = sum(rec.line_ids.mapped('subtotal'))

    def action_request_approval(self):
        if not self.line_ids:
            raise UserError("Add at least one line before requesting approval.")
        self.state = 'waiting_approval'

    def action_approve(self):
        if self.state != 'waiting_approval':
            raise UserError("Only orders waiting for approval can be approved.")
        self.state = 'approved'

    def action_confirm_order(self):
        if self.state != 'approved':
            raise UserError("Only approved orders can be confirmed.")
        self.state = 'ordered'

    def action_create_invoice(self):
        if not self.vendor_id:
            raise UserError("Please select a Vendor before creating an invoice.")
        if not self.line_ids:
            raise UserError("Invoice cannot be created without order lines.")

        invoice_lines = []
        for line in self.line_ids:
            product = line.product_id
            category = product.categ_id
            income_account = category.property_account_income_categ_id

            if not product:
                raise UserError("Please select a product in all order lines.")
            if not category:
                raise UserError(f"Assign a category to the product '{product.display_name}'.")
            if not income_account:
                raise UserError(f"Configure an income account for category '{category.display_name}'.")

            invoice_lines.append((0, 0, {
                'product_id': product.id,
                'name': product.name,
                'quantity': line.quantity,
                'price_unit': line.unit_price,
                'account_id': income_account.id,
            }))

        invoice = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.vendor_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_origin': self.name,
            'invoice_line_ids': invoice_lines,
        })
        self.state = 'invoiced'
        return {
            'name': 'Vendor Bill',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }


class MovieCateringOrderLine(models.Model):
    _name = 'movie.catering.order.line'
    _description = 'Catering Order Line'

    quantity = fields.Integer(string="Plates", default=1)
    unit_price = fields.Float(string="Price per Plate")
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal', store=True)

    order_id = fields.Many2one('movie.catering.order', string="Order", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Meal Item", required=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.constrains('quantity', 'unit_price')
    def _check_positive_values(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError("Quantity must be greater than 0.")
            if line.unit_price < 0:
                raise ValidationError("Unit price cannot be negative.")
