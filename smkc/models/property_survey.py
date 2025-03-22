from odoo import models, fields

class SurveyParameters(models.Model):
    _name = 'smkc.property.survey'
    _description = 'Survey Parameters'
    
    property_id = fields.Many2one('smkc.property.info', 'Property ID', required=True)
    address_line_1 = fields.Char('Address Line 1', required=True)
    address_line_2 = fields.Char('Address Line 2')
    colony_name = fields.Char('Colony Name')
    street = fields.Char('Street')
    house_number = fields.Char('House Number')
    unit = fields.Char('Unit')
    total_floors = fields.Char('Total Floors')
    floor_number = fields.Char('Floor Number')
    owner_name = fields.Char('Owner Name')
    father_name = fields.Char('Father Name')
    area = fields.Float('Area (in Sq. Ft.)')
    area_code = fields.Char('Area Code')
    longitude = fields.Char('Longitude')
    latitude = fields.Char('Latitude')
    surveyer_id = fields.Many2one('res.users', string='Surveyor')
    installer_id = fields.Many2one('res.users', string='Installer')
    property_image = fields.Binary() 
    property_image1 = fields.Binary() 

    