from odoo import models, fields, api

class PropertyType(models.Model):
    _name = 'smkc.property.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property Type'

    name = fields.Char(string='Type', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True) 