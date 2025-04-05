from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Zone(models.Model):
    _name = 'smkc.zone'
    _description = 'Zone'
    
    name = fields.Char(string="Zone Name", required=True)

    # _sql_constraints = [
    #     ('unique_name', 'UNIQUE(name)', 'The Zone must be unique.')
    # ]

    # @api.constrains('name')
    # def _check_unique_zone_name(self):
    #     for record in self:
    #         normalized_name = record.name.strip().lower() if record.name else ''
    #         print("normalized_name - ", normalized_name)
            
    #         existing_zone = self.search([
    #             ('id', '!=', record.id)
    #         ])
    #         for zone in existing_zone:
    #             print("(existing_zone.name).lower - ",(zone.name).strip().lower())
    #             if (zone.name).strip().lower() == normalized_name:
                
    #                 raise ValidationError(f"A zone with the name '{record.name}' already exists.")

class Ward(models.Model):
    _name = 'smkc.ward'
    _description = 'Ward'

    name = fields.Char(string="Ward Name", required=True)
    zone = fields.Many2one('smkc.zone', string="Zone", required=True)

    # @api.constrains('name', 'zone')
    # def _check_unique_ward_name_in_zone(self):
    #     for record in self:
    #         existing_ward = self.search([
    #             ('zone', '=', record.zone.id),
    #             ('name', '=', record.name),
    #             ('id', '!=', record.id)
    #         ])

    #         for ward in existing_ward:
    #             if (ward.name).strip().lower() == (record.name).strip().lower():
    #                 raise ValidationError(f"A ward with the zone '{record.zone.name}' already exists.")

    # def action_print_property_plate_template(self):
    #     return self.env.ref('smkc.report_property_detail_qweb').report_action(self)



class PropertyType(models.Model):
    _name = 'smkc.property.type'
    _description = 'Property Type'

    name = fields.Char(string="Type")





