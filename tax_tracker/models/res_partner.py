from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    upic_id = fields.Char(
        string='UPIC ID',
        copy=False,
        index=True,
        help="Unique Property Identification Code"
    )

    _sql_constraints = [
        ('upic_id_uniq', 
         'unique(upic_id)', 
         'UPIC ID must be unique!')
    ]
