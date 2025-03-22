from odoo import http
from .main import *

_logger = logging.getLogger(__name__)
class PropertyDetailsAPI(http.Controller):


    """ API CRUD """
        
    @http.route('/api/get_property', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def get_property_details(self, **kwargs):
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
                                        "address_line_1": survey.address_line_1, 
                                        "address_line_2": survey.address_line_2, 
                                        "colony_name": survey.colony_name, 
                                        "street": survey.street, 
                                        "house_number": survey.house_number, 
                                        "unit": survey.unit, 
                                        "total_floors": survey.total_floors,
                                        "floor_number": survey.floor_number,
                                        "owner_name": survey.owner_name, 
                                        "father_name": survey.father_name, 
                                        "area": survey.area, 
                                        "area_code": survey.area_code, 
                                        "longitude": survey.longitude, 
                                        "latitude": survey.latitude, 
                                        "surveyer_id": survey.surveyer_id.id,
                                        "installer_id": survey.installer_id.id,
                                        "property_image": survey.property_image,
                                        "property_image1": survey.property_image1, 
                                    } for survey in property.survey_line_ids if property.survey_line_ids]
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

    @http.route('/api/property/create_survey', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def create_survey(self, **kwargs):
        _logger.info("create_survey API endpoint hit")

        try:
            data = json.loads(request.httprequest.data or "{}")
            upic_no = data.get('upic_no', '')
            if not upic_no:
                return Response(json.dumps({'error': 'upic_no is required'}), status=400, content_type='application/json')
            
            property_record = request.env['smkc.property.info'].sudo().search([('upic_no', '=', upic_no)])

            if not property_record:
                return Response(json.dumps({'error': 'Property not found for the provided upic_no'}), status=404, content_type='application/json')
            
            address_line_1 = data.get("address_line_1", '')
            address_line_2 = data.get("address_line_2", '')
            colony_name = data.get("colony_name", '')
            street = data.get("street", '')
            house_number = data.get("house_number", '')
            unit = data.get("unit", '')
            total_floors = data.get("total_floors", '')
            floor_number = data.get("floor_number", '')
            owner_name = data.get("owner_name", '')
            father_name = data.get("father_name", '')
            area = data.get("area", '')
            area_code = data.get("area_code", '')
            longitude = data.get("longitude", '')
            latitude = data.get("latitude", '')
            surveyer_id = data.get("surveyer_id", False)
            installer_id = data.get("installer_id", False)
            property_image = data.get("property_image", False)
            property_image1 = data.get("property_image1", False)

            if surveyer_id:
                surveyer_user = request.env['res.users'].sudo().browse(surveyer_id)
                if not surveyer_user.exists():
                    return Response(json.dumps({'error': f"Surveyor with ID {surveyer_id} does not exist"}), status=400, content_type='application/json')

            # Prepare the survey line values
            survey_line_vals = {
                'address_line_1': address_line_1,
                'address_line_2': address_line_2,
                'colony_name': colony_name,
                'street': street,
                'house_number': house_number,
                'unit': unit,
                'total_floors': total_floors,
                'floor_number': floor_number,
                'owner_name': owner_name,
                'father_name': father_name,
                'area': area,
                'area_code': area_code,
                'longitude': longitude,
                'latitude': latitude,
                'surveyer_id': surveyer_id if surveyer_id else False,
                'installer_id': installer_id if installer_id else False,
                'property_image': property_image if property_image else False,
                'property_image1': property_image1 if property_image1 else False,
            }

            property_record.write({
                'survey_line_ids': [(0, 0, survey_line_vals)]
            })

            _logger.info(f"Successfully created a new survey for property {upic_no}")
            return Response(json.dumps({'message': 'Survey created successfully'}), status=200, content_type='application/json')

        except jwt.ExpiredSignatureError:
            _logger.error("JWT token has expired")
            raise AccessError('JWT token has expired')
        except jwt.InvalidTokenError:
            _logger.error("Invalid JWT token")
            raise AccessError('Invalid JWT token')
        except Exception as e:
            _logger.error(f"Error occurred: {str(e)}")
            return Response(json.dumps({'error': str(e)}), status=500, content_type='application/json')
