from odoo import models, fields, api

class TaxType(models.Model):
    _name = 'tax.type'
    _description = 'Tax Type'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True
    )
    
    code = fields.Char(
        string='Code',
        required=True
    )
    
    rate = fields.Float(
        string='Rate (%)',
        required=True
    )
    
    description = fields.Text(
        string='Description'
    )
    
    category = fields.Selection([
        ('property', 'Property Tax'),
        ('water', 'Water Tax'),
        ('commercial', 'Commercial Tax')
    ], string='Tax Category', required=True)
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    transaction_count = fields.Integer(
        string='Transaction Count',
        compute='_compute_transaction_count'
    )

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Tax type code must be unique!')
    ]

    @api.depends('transaction_ids')
    def _compute_transaction_count(self):
        for record in self:
            record.transaction_count = len(record.transaction_ids)

    transaction_ids = fields.One2many(
        'tax.transaction',
        'tax_type_id',
        string='Transactions'
    )
