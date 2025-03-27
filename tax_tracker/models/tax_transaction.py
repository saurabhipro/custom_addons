from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TaxTransaction(models.Model):
    _name = 'tax.transaction'
    _description = 'Tax Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        default='New'
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        tracking=True
    )
    
    upic_id = fields.Char(
        string='UPIC ID',
        required=True,
        tracking=True,
        index=True,
        help="Unique Property Identification Code"
    )
    
    tax_type_id = fields.Many2one(
        'tax.type',
        string='Tax Type',
        required=True,
        tracking=True
    )
    
    date = fields.Date(
        string='Transaction Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    
    amount = fields.Monetary(
        string='Amount',
        required=True,
        tracking=True
    )
    
    tax_amount = fields.Monetary(
        string='Tax Amount',
        compute='_compute_tax_amount',
        store=True,
        tracking=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    payment_date = fields.Date(
        string='Payment Date',
        tracking=True
    )
    
    payment_reference = fields.Char(
        string='Payment Reference',
        tracking=True
    )
    
    notes = fields.Text(
        string='Notes',
        tracking=True
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    _sql_constraints = [
        ('upic_tax_type_date_uniq', 
         'unique(upic_id, tax_type_id, date)', 
         'Only one transaction per UPIC ID, tax type and date is allowed!')
    ]

    @api.depends('amount', 'tax_type_id.rate')
    def _compute_tax_amount(self):
        for record in self:
            record.tax_amount = record.amount * (record.tax_type_id.rate / 100)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tax.transaction') or 'New'
        return super().create(vals_list)

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_mark_paid(self):
        for record in self:
            if not record.payment_date:
                record.payment_date = fields.Date.context_today(self)
            record.state = 'paid'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def action_reset_to_draft(self):
        for record in self:
            record.state = 'draft'

    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount <= 0:
                raise ValidationError('Amount must be greater than zero.')
