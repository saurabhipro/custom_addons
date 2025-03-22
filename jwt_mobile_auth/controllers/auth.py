from .main import *

SECRET_KEY = 'secret'

class JWTAuthController(http.Controller):


    """ OTP SENT AND SIGN UP """
    @http.route('/api/auth/request_otp', type='http', auth='public', methods=['POST'], csrf=False)
    def request_otp(self, **kwargs):
        data = json.loads(request.httprequest.data or "{}")
        mobile = data.get('mobile')
        if not mobile:
            return Response(json.dumps({'error': 'Mobile number is missing'}), status=400, content_type='application/json' )

        user = request.env['res.users'].sudo().search([('mobile', '=', mobile)], limit=1)
        if not user:           
            # user_vals = {
            #     'name': f"demo{user.id+1}",
            #     'mobile': mobile,
            #     'login': f"demo{user.id+1}",
            #     'active': True,
            #     'company_id': 1,
            #     'company_ids': [(4, 1)],
            #     'groups_id': [(6, 0, [request.env.ref('base.group_user').id, request.env.ref('jwt_mobile_auth.surveyor_group_ddn').id])],  # Assigning the user to the basic user group
            # }
            return Response(json.dumps({'error': 'Surveyor Not Register'}), status=400, content_type='application/json')
        

        existing_otp = request.env['mobile.otp'].sudo().search([('mobile', '=', mobile)])
        if existing_otp:
            existing_otp.unlink()

        otp_code = str(random.randint(1000, 9999))
        expire_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

        print("user.id - ", user.id)
        request.env['mobile.otp'].sudo().create({
            'mobile': mobile,
            'user_id': user.id,
            'otp': otp_code,
            'expire_date': expire_time.strftime('%Y-%m-%d %H:%M:%S'),
        })

        try:
            api_url = f"https://webmsg.smsbharti.com/app/smsapi/index.php?key=5640415B1D6730&campaign=0&routeid=9&type=text&contacts={mobile}&senderid=SPTSMS&msg=Your%20otp%20is%20{otp_code}%20SELECTIAL&template_id=1707166619134631839"
            response = requests.get(api_url)
            if response.status_code == 200:
                if 'ERR' in response.text:
                    return Response(json.dumps({'message': 'Invalid Mobile','details': response.text}), status=400, content_type='application/json')
                return Response(json.dumps({'message': 'OTP sent successfully','details': response.text}), status=200, content_type='application/json')
            else:
                return Response(
                    json.dumps({'error': 'Failed to send OTP via SMS API', 'details': response.text}), status=400, content_type='application/json')
        except Exception as e:
            return Response( json.dumps({'error': 'Error sending SMS', 'details': str(e)}), status=400, content_type='application/json' )
               
    """ LOGIN """
    @http.route('/api/auth/login', type='http', auth='none', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        data = json.loads(request.httprequest.data or "{}")
        mobile = data.get('mobile')
        otp_input = data.get('otp_input')

        if not mobile or not otp_input:
            return Response(json.dumps({'error': 'Mobile number or OTP is missing'}), status=400, content_type='application/json')

        otp_record = request.env['mobile.otp'].sudo().search([
            ('mobile', '=', mobile),
            ('otp', '=', otp_input)
        ], limit=1)
        print("otp_record - ", otp_record)
        if not otp_record:
            return Response( json.dumps({'error': 'Invalid OTP'}), status=400, content_type='application/json' )

        expire_date = otp_record.expire_date
        print("expire_date - ", expire_date)
        if datetime.datetime.utcnow() > expire_date:
            otp_record.unlink()
            return Response(json.dumps({'error': 'OTP expired'}),status=400, content_type='application/json')

        user = otp_record.user_id.id
        otp_record.unlink()

        payload = {
            'user_id': user,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        request.env['jwt.token'].sudo().create({'user_id': user, 'token': token})

        return Response( json.dumps({'user_id': user, 'token': token}), status=200, content_type='application/json' )

    """ API CRUD """
    @http.route('/api/get_contacts', type='json', auth='none', methods=['POST'], csrf=False)
    def get_contacts(self, **kwargs):
        print("\n self - ", self)
        try:
            user_id = check_permission(request.httprequest.headers.get('Authorization'))
            print("user_id - ", user_id)
            if user_id :
                contacts = request.env['res.partner'].sudo().search([])
                print("contacts - ", contacts)
                contact_data = []
                for contact in contacts:
                    contact_data.append({
                        'name': contact.name,
                        'phone': contact.phone,
                        'email': contact.email,
                        'company': contact.company_id.name if contact.company_id else ''
                    })

                return {'contacts': contact_data}

        except jwt.ExpiredSignatureError:
            raise AccessError('JWT token has expired')
        except jwt.InvalidTokenError:
            raise AccessError('Invalid JWT token')
        
        
    