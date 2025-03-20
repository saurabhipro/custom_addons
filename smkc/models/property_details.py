from odoo import models, fields

class PropertyInfo(models.Model):
    _name = 'smkc.property.info'
    _description = 'Property Information'
    _inherit = ['mail.thread']


    # Owner Information
    property_status = fields.Selection([
        ('uploaded','Uploaded'),
        ('pdf_downloaded','PDF Downloaded'),
        ('plate_installed', 'Plate Installed'),
        ('surveyed', 'Surveyed'),
        ('unlocked','Unlocked'),
        ('discovered', 'Discovered')
         ], string="Property Status", default="uploaded")
    property_image = fields.Binary() 
    property_image1 = fields.Binary() 

    owner_id = fields.Char('OwnerID')
    upic_no = fields.Char('UPICNO')

    _sql_constraints = [
        ('unique_upic_no', 'UNIQUE(upic_no)', 'The UPICNO must be unique.')
    ]

    survey_line_ids = fields.One2many('smkc.property.survey', 'property_id', string="Survey Line")
    
    # Zone and Ward Information
    zone = fields.Char('Zone')
    new_zone_no = fields.Char('NewZoneNo')
    new_ward_no = fields.Char('NewWardNo')
    new_property_no = fields.Char('NewPropertyNo')
    new_partition_no = fields.Char('NewPartitionNo')
    new_city_survey_no = fields.Char('NewCityServeyNo')
    new_plot_no = fields.Char('NewPlotNo')
    old_zone_no = fields.Char('OldZoneNo')
    old_ward_no = fields.Char('OldWardNo')
    old_property_no = fields.Char('OldPropertyNo')
    
    # Billing Information
    bill_no = fields.Char('BillNo')
    property_description = fields.Text('PropertyDescription')
    
    # Plot Information
    plot_area = fields.Char('PlotArea')  # In Sq. Ft. or desired unit
    mobile_no = fields.Char('MobileNo')
    
    # Old Rent Information
    old_rental_value = fields.Char('OldRentalValue')
    old_rv = fields.Char('OldRV')
    old_property_tax = fields.Char('OldPropertyTax')
    old_total_tax = fields.Char('OldTotalTax')
    
    # New Property Information
    new_toilet_no = fields.Char('NewToiletNo')
    plot_taxable_area_sqft = fields.Char('PlotTaxableAreaSqFt')
    
    # Marathi Names
    marathi_owner_name = fields.Char('MarathiOwnerName')
    marathi_renter_name = fields.Char('MarathiRenterName')
    marathi_occupier_name = fields.Char('MarathiOccupierName')
    marathi_owner_patta = fields.Char('MarathiOwnerPatta')
    marathi_owner_dukan_imarate_nav = fields.Char('MarathiOwnerDukanImarateNav')
    marathi_owner_dukan_flat_no = fields.Char('MarathiOwnerDukanFlatNo')
    
    # Remarks
    comb_prop_remark = fields.Text('CombPropRemark')
    
    # Location Information
    latitude = fields.Char('Latitude')
    longitude = fields.Char('Longitude')
    
    # Property Infrastructure Information
    road_width = fields.Char('RoadWidth')
    no_of_trees = fields.Char('NoOfTrees')
    
    # Solar, Bore, Water, and Rainwater Information
    is_solar = fields.Char('IsSolar')
    no_of_solar = fields.Char('NoOfSolar')
    is_bore = fields.Char('IsBoar')
    no_of_bore = fields.Char('NoOfBoar')
    is_rainwater_harvesting = fields.Char('IsRainwaterharvesting')
    no_of_rain_water_harvesting = fields.Char('NoOfRainWaterharvesting')
    
    # Water Connection and Hand Pump Information
    is_water_conn_status = fields.Char('IsWarterConnStatus')
    is_hand_pump = fields.Char('IsHandPump')
    no_of_hand_pump = fields.Char('NoOfHandPump')
    is_well = fields.Char('IsWell')
    no_of_well = fields.Char('NoOfWell')
    
    # Lift, Drain, and Building Information
    is_lift = fields.Char('IsLift')
    no_of_lift = fields.Char('NoOfLift')
    drain = fields.Char('Drain')
    building_permissions = fields.Char('BuildingPermissions')
    building_advertise = fields.Char('BuildingAdvertise')
    building_advertise_type = fields.Char('BuildingAdvertiseType')
    
    # Garbage Information
    garbage_segrigation = fields.Char('GarbageSegrigation')
    garbage_disposal = fields.Char('GarbageDisposal')
    septic_tank_yes_no = fields.Char('SepticTankYesNo')
    
    # Water Meter Information
    water_meter_yes_no = fields.Char('WaterMeterYesNo')
    water_connection_year = fields.Char('WaterConnectionYear')
    
    # License Information
    licence_no = fields.Char('LicenceNo')
    licence_date = fields.Date('LicenceDate')
    
    # Property Construction Information
    year_of_permission = fields.Char('YearOfPermission')
    year_of_construction = fields.Char('YearOfConstruction')
    building_age = fields.Char('BuildingAge')
    building_year = fields.Char('BuildingYear')
    build_completion_date = fields.Date('BuildCompletionDate')

    oid = fields.Date('Oid')

    
    # Fire, Water Meter, ETP, and Waste Information
    is_fire = fields.Char('IsFire')
    no_of_fire = fields.Char('NoOfFire')
    water_meter_condition = fields.Char('WaterMeterCondition')
    is_water_motar = fields.Char('IsWaterMotar')
    water_connection_no = fields.Char('WaterConnectionNo')
    water_consumer_no = fields.Char('WaterConsumerNo')
    is_etp = fields.Char('IsETP')
    
    # Composting and Sewage Information
    is_home_composting = fields.Char('IsHomeComposting')
    is_vermicompost = fields.Char('IsVermicompost')
    is_echarging = fields.Char('IsECharging')
    is_sewage_water = fields.Char('IsSewageWater')
    
    # Permission and Certificate Information
    is_const_permission = fields.Char('IsConstPermission')
    const_completion_oc = fields.Char('ConstCompletionOC')
    gunthewari_certificate = fields.Char('GunthewariCertificate')
    
    # Bukhand, Construction, and Animal Information
    is_bukhand = fields.Char('IsBukhand')
    is_construction = fields.Char('IsConstruction')
    total_no_of_people = fields.Char('TotalNoOfPeople')
    
    # Animal Information
    is_animals = fields.Char('IsAnimals')
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
    is_gotha = fields.Char('IsGotha')
    oc_number = fields.Char('OCNumber')




