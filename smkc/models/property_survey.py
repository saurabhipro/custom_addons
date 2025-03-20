from odoo import models, fields

class SurveyParameters(models.Model):
    _name = 'smkc.property.survey'
    _description = 'Survey Parameters'
    
    # Property Information
    property_id = fields.Many2one('smkc.property.info', 'Property ID', required=True)
    
    # Address Information
    address_line_1 = fields.Char('Address Line 1', required=True)
    address_line_2 = fields.Char('Address Line 2')
    colony_name = fields.Char('Colony Name')
    street = fields.Char('Street')
    house_number = fields.Char('House Number')
    unit = fields.Char('Unit')
    
    # Property Details
    total_floors = fields.Char('Total Floors')
    floor_number = fields.Char('Floor Number')
    
    # Owner Information
    owner_name = fields.Char('Owner Name')
    father_name = fields.Char('Father Name')
    
    # Area Information
    area = fields.Float('Area (in Sq. Ft.)')
    area_code = fields.Char('Area Code')
    
    # Location Information
    longitude = fields.Char('Longitude')
    latitude = fields.Char('Latitude')
    
    # Survey & Installer Information
    surveyer_id = fields.Many2one('res.users', string='Surveyor')
    installer_id = fields.Many2one('res.users', string='Installer')

    # Constraints can be added as needed, for example:
    _sql_constraints = [
        ('unique_property_id', 'UNIQUE(property_id)', 'The Property ID must be unique.')
    ]
