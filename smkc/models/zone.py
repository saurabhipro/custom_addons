from odoo import models, fields, api

class Zone(models.Model):
    _name = 'smkc.zone'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Zone'

    name = fields.Char(string='Zone Name', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True) 