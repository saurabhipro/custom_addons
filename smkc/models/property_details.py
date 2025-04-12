from odoo import models, fields, api
import base64
from io import BytesIO
try:
    import qrcode
except ImportError:
    qrcode = None  # If not installed, you'll need to pip install qrcode[pil]

class PropertyInfo(models.Model):
    _name = 'smkc.property.info'
    _description = 'Property Information'
    _inherit = ['mail.thread']
    _rec_name = "upic_no"


    # Owner Information
    property_status = fields.Selection([
        ('new', 'New'),
        ('uploaded','Uploaded'),
        ('pdf_downloaded','PDF Downloaded'),
        ('plate_installed', 'Plate Installed'),
        ('surveyed', 'Surveyed'),
        ('unlocked','Unlocked'),
        ('discovered', 'Discovered')
         ], string="Property Status", default="uploaded")
    
    owner_id = fields.Char('Owner ID')
    upic_no = fields.Char('UPIC NO')

    _sql_constraints = [
        ('unique_upic_no', 'UNIQUE(upic_no)', 'The UPICNO must be unique.')
    ]

    survey_line_ids = fields.One2many('smkc.property.survey', 'property_id', string="Survey Line")

    address_line_1 = fields.Char(string="Address 1")
    address_line_2 = fields.Char(string="Address 2")
    colony_name = fields.Char(string="Colony Name")
    house_number = fields.Char(string="H.No")
    surveyer_id = fields.Many2one(string="Surveyor")
    
    # Zone and Ward Information
    zone = fields.Char('Zone')
    new_zone_no = fields.Many2one('smkc.zone', string='New Zone No')
    new_ward_no = fields.Many2one('smkc.ward',string='New Ward No')
    new_property_no = fields.Char('New Property No')
    new_partition_no = fields.Char('New Partition No')
    new_city_survey_no = fields.Char('New CityServey No')
    new_plot_no = fields.Char('New Plot No')
    old_zone_no = fields.Char('Old Zone No')
    old_ward_no = fields.Char('Old Ward No')
    old_property_no = fields.Char('Old Property No')
    
    # Billing Information
    bill_no = fields.Char('Bill No')
    property_description = fields.Text('Property Description')
    
    # Plot Information
    plot_area = fields.Float('Plot Area')  # In Sq. Ft. or desired unit
    mobile_no = fields.Char('Mobile No')
    
    # Old Rent Information
    old_rental_value = fields.Float('Old Rental Value')
    old_rv = fields.Float('Old RV')
    old_property_tax = fields.Float('Old Property Tax')
    old_total_tax = fields.Float('Old Total Tax')
    
    # New Property Information
    new_toilet_no = fields.Char('New Toilet No')
    plot_taxable_area_sqft = fields.Char('Plot Taxable Area SqFt')
    
    # Marathi Names
    marathi_owner_name = fields.Char('Marathi Owner Name')
    marathi_renter_name = fields.Char('Marathi Renter Name')
    marathi_occupier_name = fields.Char('Marathi Occupier Name')
    marathi_owner_patta = fields.Char('Marathi Owner Patta')
    marathi_owner_dukan_imarate_nav = fields.Char('Marathi Owner Dukan Imarate Nav')
    marathi_owner_dukan_flat_no = fields.Char('Marathi Owner Dukan Flat No')
    
    # Remarks
    comb_prop_remark = fields.Text('Comb Prop Remark')
    
    # Location Information
    latitude = fields.Char('Latitude')
    longitude = fields.Char('Longitude')
    
    # Property Infrastructure Information
    road_width = fields.Char('Road Width')
    no_of_trees = fields.Char('No Of Trees')
    
    # Solar, Bore, Water, and Rainwater Information
    is_solar = fields.Char('Is Solar')
    no_of_solar = fields.Char('No Of Solar')
    is_bore = fields.Char('Is Boar')
    no_of_bore = fields.Char('No Of Boar')
    is_rainwater_harvesting = fields.Char('Is Rain water harvesting')
    no_of_rain_water_harvesting = fields.Char('No Of Rain Water harvesting')
    
    # Water Connection and Hand Pump Information
    is_water_conn_status = fields.Char('Is Warter Conn Status')
    is_hand_pump = fields.Char('Is Hand Pump')
    no_of_hand_pump = fields.Char('No Of Hand Pump')
    is_well = fields.Char('Is Well')
    no_of_well = fields.Char('No Of Well')
    
    # Lift, Drain, and Building Information
    is_lift = fields.Char('Is Lift')
    no_of_lift = fields.Char('No Of Lift')
    drain = fields.Char('Drain')
    building_permissions = fields.Char('Building Permissions')
    building_advertise = fields.Char('Building Advertise')
    building_advertise_type = fields.Char('Building Advertise Type')
    
    # Garbage Information
    garbage_segrigation = fields.Char('Garbage Segrigation')
    garbage_disposal = fields.Char('Garbage Disposal')
    septic_tank_yes_no = fields.Char('Septic Tank Yes/No')
    
    # Water Meter Information
    water_meter_yes_no = fields.Char('Water Meter Yes/No')
    water_connection_year = fields.Char('Water Connection Year')
    
    # License Information
    licence_no = fields.Char('Licence No')
    licence_date = fields.Date('Licence Date')
    
    # Property Construction Information
    year_of_permission = fields.Char('Year Of Permission')
    year_of_construction = fields.Char('Year Of Construction')
    building_age = fields.Char('Building Age')
    building_year = fields.Char('Building Year')
    build_completion_date = fields.Date('Build Completion Date')

    oid = fields.Date('Oid')

    
    # Fire, Water Meter, ETP, and Waste Information
    is_fire = fields.Char('Is Fire')
    no_of_fire = fields.Char('No Of Fire')
    water_meter_condition = fields.Char('Water Meter Condition')
    is_water_motar = fields.Char('Is Water Motar')
    water_connection_no = fields.Char('Water Connection No')
    water_consumer_no = fields.Char('Water Consumer No')
    is_etp = fields.Char('Is ETP')
    
    # Composting and Sewage Information
    is_home_composting = fields.Char('Is Home Composting')
    is_vermicompost = fields.Char('Is Vermi compost')
    is_echarging = fields.Char('Is ECharging')
    is_sewage_water = fields.Char('Is Sewage Water')
    
    # Permission and Certificate Information
    is_const_permission = fields.Char('Is Const Permission')
    const_completion_oc = fields.Char('Const Completion OC')
    gunthewari_certificate = fields.Char('Gunthewari Certificate')
    
    # Bukhand, Construction, and Animal Information
    is_bukhand = fields.Char('Is Bukhand')
    is_construction = fields.Char('Is Construction')
    total_no_of_people = fields.Char('Total No Of People')
    
    # Animal Information
    is_animals = fields.Char('Is Animals')
    dog = fields.Char('Dog')
    cat = fields.Char('Cat')
    cow = fields.Char('Cow')
    buffalo = fields.Char('Buffalo')
    horse = fields.Char('Horse')
    oax = fields.Char('Oax')
    pig = fields.Char('Pig')
    donkey = fields.Char('Donkey')
    other = fields.Char('Other')
    
    # Additional Information
    is_gotha = fields.Char('Is Gotha')
    oc_number = fields.Char('OC Number')

    @api.model
    def get_dashboard_data(self):
        print("\n get_dashboard_data - ", self)
        uploaded = self.env['smkc.property.info'].search_count([('property_status','=','uploaded')])
        print("uploaded - ", uploaded)
        pdf_downloaded = self.search_count([('property_status','=','pdf_downloaded')])
        
        return [{
            'uploaded': uploaded,
            'pdf_downloaded': pdf_downloaded,
            # other fields
        }]