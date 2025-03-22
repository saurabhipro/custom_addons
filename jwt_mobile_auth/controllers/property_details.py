from odoo import http
from .main import *

class PropertyDetailsAPI(http.Controller):


    """ API CRUD """
        
    @http.route('/api/get_property', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def get_property_details(self, **kwargs):
        print("\n self - ", self)
        try:
            data = json.loads(request.httprequest.data or "{}")

            upic_no = data.get('upic_no', '')
            mobile = data.get('mobile', '')
            owner = data.get('owner', '')
            page = int(data.get('page', 1))
            limit = int(data.get('limit', 50))

            domain = []

            if upic_no:
                domain.append(('upic_no', '=', upic_no))
            if mobile:
                domain.append(('mobile_no', '=', mobile))
            if owner:
                domain.append(('marathi_owner_name', 'like', owner))

            if domain:
                property_details = request.env['smkc.property.info'].sudo().search(domain, limit=limit, offset=(page - 1) * limit)
            else:
                property_details = request.env['smkc.property.info'].sudo().search([], limit=limit, offset=(page - 1) * limit)

            property_data = []
            for property in property_details:
                property_data.append({
                    "status" : property.property_status,
                    "owner_id": property.owner_id,
                    "upic_no": property.upic_no,
                    "zone": property.zone,
                    "new_zone_no": property.new_zone_no,
                    "new_ward_no": property.new_ward_no,
                    "latitude": property.latitude,
                    "longitude": property.longitude,
                    "mobile_no": property.mobile_no,
                    "marathi_owner_name": property.marathi_owner_name,
                    "marathi_occupier_name": property.marathi_occupier_name,
                    "marathi_owner_dukan_imarate_nav": property.marathi_owner_dukan_imarate_nav,
                    "plot_area": property.plot_area,
                    "marathi_renter_name": property.marathi_renter_name,
                    "survey_line_ids": [{
                                        "address_line_1": "123 Street",
                                        "address_line_2": "Near Park",
                                        "colony_name": "Colony 1",
                                        "street": "Main Street",
                                        "house_number": "12A",
                                        "unit": "Unit 101",
                                        "total_floors": "5",
                                        "floor_number": "1",
                                        "owner_name": "Owner 1",
                                        "father_name": "Father Name 1",
                                        "area": 200,
                                        "area_code": "AreaCode1",
                                        "longitude": "73.8567",
                                        "latitude": "18.5204",
                                        "surveyer_id": 2,
                                        "installer_id": 3,
                                        "property_image": "base64encodedimage",
                                        "property_image1": "base64encodedimage1"
                                    }]
                })

            # Return the paginated response
            return Response(json.dumps({
                'property_details': property_data,
                'page': page,
                'limit': limit
            }), status=200, content_type='application/json')

        except jwt.ExpiredSignatureError:
            raise AccessError('JWT token has expired')
        except jwt.InvalidTokenError:
            raise AccessError('Invalid JWT token')
