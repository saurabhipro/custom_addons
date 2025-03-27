from odoo import http
from odoo.http import request
import json
from datetime import datetime
from odoo.exceptions import ValidationError

class TaxTrackerAPI(http.Controller):
    @http.route('/api/v1/tax/transaction', type='json', auth='api_key', methods=['POST'], csrf=False)
    def create_tax_transaction(self, **kwargs):
        """
        Create a tax transaction via API
        Payload example:
        {
            "upic_id": "UPIC123456",
            "tax_type_code": "PROPERTY",  # or "WATER" or "COMMERCIAL"
            "amount": 1000.00,
            "payment_reference": "PAY123",
            "payment_date": "2025-03-27"
        }
        """
        try:
            # Validate required fields
            required_fields = ['upic_id', 'tax_type_code', 'amount']
            for field in required_fields:
                if field not in kwargs:
                    return {'success': False, 'error': f'Missing required field: {field}'}

            # Validate tax type code
            valid_tax_codes = ['PROPERTY', 'WATER', 'COMMERCIAL']
            if kwargs['tax_type_code'] not in valid_tax_codes:
                return {'success': False, 'error': f'Invalid tax type code. Must be one of: {", ".join(valid_tax_codes)}'}

            # Find tax type by code
            tax_type = request.env['tax.type'].sudo().search([('code', '=', kwargs['tax_type_code'])], limit=1)
            if not tax_type:
                return {'success': False, 'error': f'Tax type not found: {kwargs["tax_type_code"]}'}

            # Find or create partner based on UPIC ID
            partner = request.env['res.partner'].sudo().search([('upic_id', '=', kwargs['upic_id'])], limit=1)
            if not partner:
                partner = request.env['res.partner'].sudo().create({
                    'name': f'UPIC: {kwargs["upic_id"]}',
                    'upic_id': kwargs['upic_id'],
                })

            # Check for existing transaction with same UPIC, tax type and date
            existing_transaction = request.env['tax.transaction'].sudo().search([
                ('upic_id', '=', kwargs['upic_id']),
                ('tax_type_id', '=', tax_type.id),
                ('date', '=', kwargs.get('payment_date', fields.Date.today())),
            ], limit=1)

            if existing_transaction:
                return {
                    'success': False, 
                    'error': 'Transaction already exists for this UPIC ID, tax type and date'
                }

            # Prepare transaction values
            transaction_vals = {
                'partner_id': partner.id,
                'upic_id': kwargs['upic_id'],
                'tax_type_id': tax_type.id,
                'amount': float(kwargs['amount']),
                'date': kwargs.get('payment_date', fields.Date.today()),
                'payment_reference': kwargs.get('payment_reference', ''),
                'state': 'paid',
                'payment_date': kwargs.get('payment_date', fields.Date.today()),
            }

            # Create transaction
            transaction = request.env['tax.transaction'].sudo().create(transaction_vals)

            return {
                'success': True,
                'data': {
                    'transaction_id': transaction.id,
                    'name': transaction.name,
                    'amount': transaction.amount,
                    'tax_amount': transaction.tax_amount,
                    'date': transaction.date.strftime('%Y-%m-%d'),
                }
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    @http.route('/api/v1/tax/transactions/<string:upic_id>', type='http', auth='api_key', methods=['GET'], csrf=False)
    def get_tax_transactions(self, upic_id, **kwargs):
        """Get all tax transactions for a given UPIC ID"""
        try:
            domain = [('upic_id', '=', upic_id)]
            
            # Filter by tax category if specified
            if kwargs.get('tax_category'):
                tax_types = request.env['tax.type'].sudo().search([('category', '=', kwargs['tax_category'])])
                if tax_types:
                    domain.append(('tax_type_id', 'in', tax_types.ids))
                else:
                    return request.make_response(
                        json.dumps({'success': False, 'error': 'Invalid tax category'}),
                        headers=[('Content-Type', 'application/json')]
                    )
            
            transactions = request.env['tax.transaction'].sudo().search(domain)
            
            result = []
            for trans in transactions:
                result.append({
                    'transaction_id': trans.id,
                    'name': trans.name,
                    'amount': trans.amount,
                    'tax_amount': trans.tax_amount,
                    'tax_type': trans.tax_type_id.name,
                    'tax_category': trans.tax_type_id.category,
                    'date': trans.date.strftime('%Y-%m-%d'),
                    'state': trans.state,
                    'payment_reference': trans.payment_reference or '',
                })

            return request.make_response(
                json.dumps({'success': True, 'data': result}),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'success': False, 'error': str(e)}),
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api/v1/tax/summary/<string:upic_id>', type='http', auth='api_key', methods=['GET'], csrf=False)
    def get_tax_summary(self, upic_id, **kwargs):
        """Get tax payment summary for a given UPIC ID"""
        try:
            domain = [('upic_id', '=', upic_id)]
            
            # Optional date range filter
            if kwargs.get('from_date'):
                domain.append(('date', '>=', kwargs['from_date']))
            if kwargs.get('to_date'):
                domain.append(('date', '<=', kwargs['to_date']))

            transactions = request.env['tax.transaction'].sudo().search(domain)
            
            # Group by tax category and type
            summary = {
                'property': {'total_amount': 0, 'total_tax': 0, 'transaction_count': 0},
                'water': {'total_amount': 0, 'total_tax': 0, 'transaction_count': 0},
                'commercial': {'total_amount': 0, 'total_tax': 0, 'transaction_count': 0}
            }
            
            for trans in transactions:
                category = trans.tax_type_id.category
                summary[category]['total_amount'] += trans.amount
                summary[category]['total_tax'] += trans.tax_amount
                summary[category]['transaction_count'] += 1

            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': {
                        'upic_id': upic_id,
                        'summary': summary,
                        'total_transactions': len(transactions)
                    }
                }),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'success': False, 'error': str(e)}),
                headers=[('Content-Type', 'application/json')]
            )
