from odoo import models, fields, api, _

class Zone(models.Model):
    _name = 'smkc.zone'
    _description = 'Zone'

    name = fields.Char(string="Zone Name")


class Ward(models.Model):
    _name = 'smkc.ward'
    _description = 'Ward'

    name = fields.Char(string="Ward Name")
    zone = fields.Many2one('smkc.zone', string="Zone")

class PropertyType(models.Model):
    _name = 'smkc.property.type'
    _description = 'Property Type'

    name = fields.Char(string="Type")





