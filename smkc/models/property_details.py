from odoo import models, fields

class PropertyInfo(models.Model):
    _name = 'smkc.property.info'
    _description = 'Property Information'

    # Owner Information
    owner_id = fields.Char('OwnerID')
    upic_no = fields.Char('UPICNO')
    
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
    plot_area = fields.Float('PlotArea')  # In Sq. Ft. or desired unit
    mobile_no = fields.Char('MobileNo')
    
    # Old Rent Information
    old_rental_value = fields.Float('OldRentalValue')
    old_rv = fields.Float('OldRV')
    old_property_tax = fields.Float('OldPropertyTax')
    old_total_tax = fields.Float('OldTotalTax')
    
    # New Property Information
    new_toilet_no = fields.Integer('NewToiletNo')
    plot_taxable_area_sqft = fields.Float('PlotTaxableAreaSqFt')
    
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
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')
    
    # Property Infrastructure Information
    road_width = fields.Float('RoadWidth')
    no_of_trees = fields.Integer('NoOfTrees')
    
    # Solar, Bore, Water, and Rainwater Information
    is_solar = fields.Boolean('IsSolar')
    no_of_solar = fields.Integer('NoOfSolar')
    is_bore = fields.Boolean('IsBoar')
    no_of_bore = fields.Integer('NoOfBoar')
    is_rainwater_harvesting = fields.Boolean('IsRainwaterharvesting')
    no_of_rain_water_harvesting = fields.Integer('NoOfRainWaterharvesting')
    
    # Water Connection and Hand Pump Information
    is_water_conn_status = fields.Boolean('IsWarterConnStatus')
    is_hand_pump = fields.Boolean('IsHandPump')
    no_of_hand_pump = fields.Integer('NoOfHandPump')
    is_well = fields.Boolean('IsWell')
    no_of_well = fields.Integer('NoOfWell')
    
    # Lift, Drain, and Building Information
    is_lift = fields.Boolean('IsLift')
    no_of_lift = fields.Integer('NoOfLift')
    drain = fields.Boolean('Drain')
    building_permissions = fields.Boolean('BuildingPermissions')
    building_advertise = fields.Boolean('BuildingAdvertise')
    building_advertise_type = fields.Char('BuildingAdvertiseType')
    
    # Garbage Information
    garbage_segrigation = fields.Boolean('GarbageSegrigation')
    garbage_disposal = fields.Boolean('GarbageDisposal')
    septic_tank_yes_no = fields.Boolean('SepticTankYesNo')
    
    # Water Meter Information
    water_meter_yes_no = fields.Boolean('WaterMeterYesNo')
    water_connection_year = fields.Integer('WaterConnectionYear')
    
    # License Information
    licence_no = fields.Char('LicenceNo')
    licence_date = fields.Date('LicenceDate')
    
    # Property Construction Information
    year_of_permission = fields.Integer('YearOfPermission')
    year_of_construction = fields.Integer('YearOfConstruction')
    building_age = fields.Integer('BuildingAge')
    building_year = fields.Integer('BuildingYear')
    build_completion_date = fields.Date('BuildCompletionDate')
    
    # Fire, Water Meter, ETP, and Waste Information
    is_fire = fields.Boolean('IsFire')
    no_of_fire = fields.Integer('NoOfFire')
    water_meter_condition = fields.Char('WaterMeterCondition')
    is_water_motar = fields.Boolean('IsWaterMotar')
    water_connection_no = fields.Char('WaterConnectionNo')
    water_consumer_no = fields.Char('WaterConsumerNo')
    is_etp = fields.Boolean('IsETP')
    
    # Composting and Sewage Information
    is_home_composting = fields.Boolean('IsHomeComposting')
    is_vermicompost = fields.Boolean('IsVermicompost')
    is_echarging = fields.Boolean('IsECharging')
    is_sewage_water = fields.Boolean('IsSewageWater')
    
    # Permission and Certificate Information
    is_const_permission = fields.Boolean('IsConstPermission')
    const_completion_oc = fields.Boolean('ConstCompletionOC')
    gunthewari_certificate = fields.Boolean('GunthewariCertificate')
    
    # Bukhand, Construction, and Animal Information
    is_bukhand = fields.Boolean('IsBukhand')
    is_construction = fields.Boolean('IsConstruction')
    total_no_of_people = fields.Integer('TotalNoOfPeople')
    
    # Animal Information
    is_animals = fields.Boolean('IsAnimals')
    dog = fields.Integer('Dog')
    cat = fields.Integer('Cat')
    cow = fields.Integer('Cow')
    buffalo = fields.Integer('Buffalo')
    horse = fields.Integer('Horse')
    oax = fields.Integer('Oax')
    pig = fields.Integer('Pig')
    donkey = fields.Integer('Donkey')
    other = fields.Char('Other')
    
    # Additional Information
    is_gotha = fields.Boolean('IsGotha')
    oc_number = fields.Char('OCNumber')

