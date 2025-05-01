from odoo import http
from odoo.http import request

class PropertyMapController(http.Controller):
    @http.route('/smkc/property/map_data', type='json', auth='user')
    def property_map_data(self, zone=None, ward=None, status=None):
        print("function is working fine")
        domain = []
        if zone:
            domain.append(('zone', '=', zone))
        if ward:
            domain.append(('new_ward_no', '=', ward))
        if status:
            domain.append(('property_status', '=', status))
        domain.append(('latitude', '!=', False))
        domain.append(('longitude', '!=', False))
        properties = request.env['smkc.property.info'].sudo().search(domain)
        result = []
        for prop in properties:
            result.append({
                'id': prop.id,
                'upic_no': prop.upic_no,
                'address': f"{prop.address_line_1 or ''} {prop.address_line_2 or ''}",
                'zone': prop.zone,
                'ward': prop.new_ward_no.name if prop.new_ward_no else '',
                'status': prop.property_status,
                'latitude': prop.latitude,
                'longitude': prop.longitude,
            })
        return result 