from odoo import models, fields, api

class MarriagePayment(models.Model):
    _name = 'marriage.payment'
    _description = 'Marriage Certificate Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'payment_reference'
    
    payment_reference = fields.Char('Payment Reference', readonly=True, default='New')
    marriage_id = fields.Many2one('marriage.registration', 'Marriage Registration', required=True)
    application_no = fields.Char(related='marriage_id.registration_number', string='Application No.', readonly=True)
    
    # Certificate Details
    no_of_copies = fields.Integer('No. of Certificate Copies', default=1, required=True)
    certificate_charges = fields.Float('Certificate Charges', compute='_compute_charges', store=True)
    postal_charges = fields.Float('Postal Charges', compute='_compute_charges', store=True)
    total_amount = fields.Float('Total Amount', compute='_compute_charges', store=True)
    
    # Delivery Method
    delivery_method = fields.Selection([
        ('online', 'Online'),
        ('post', 'By Post'),
        ('visit', 'By Visiting Department')
    ], string='Delivery Method', default='online', required=True, tracking=True)
    
    post_type = fields.Selection([
        ('regular', 'Regular Post'),
        ('speed', 'Speed Post'),
        ('registered', 'Registered Post')
    ], string='Post Type')
    
    # Payment Details
    payment_method = fields.Selection([
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI')
    ], string='Payment Method')
    
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ], string='Payment Status', default='pending', tracking=True)
    
    transaction_id = fields.Char('Transaction ID')
    payment_date = fields.Datetime('Payment Date')
    
    # Certificate Status
    certificate_status = fields.Selection([
        ('pending', 'Pending'),
        ('generated', 'Generated'),
        ('delivered', 'Delivered')
    ], string='Certificate Status', default='pending', tracking=True)
    
    certificate_delivery_date = fields.Datetime('Certificate Delivery Date')
    certificate_download_link = fields.Char('Certificate Download Link')
    
    # Tracking Information
    tracking_number = fields.Char('Tracking Number')
    tracking_link = fields.Char('Tracking Link')
    
    @api.depends('no_of_copies', 'delivery_method', 'post_type')
    def _compute_charges(self):
        for record in self:
            # Certificate charges
            certificate_charge_per_copy = 65.0  # Base charge per certificate
            record.certificate_charges = certificate_charge_per_copy * record.no_of_copies
            
            # Postal charges
            if record.delivery_method == 'post':
                if record.post_type == 'regular':
                    record.postal_charges = 20.0
                elif record.post_type == 'speed':
                    record.postal_charges = 50.0
                elif record.post_type == 'registered':
                    record.postal_charges = 70.0
                else:
                    record.postal_charges = 0.0
            else:
                record.postal_charges = 0.0
                
            # Total amount
            record.total_amount = record.certificate_charges + record.postal_charges
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('payment_reference', 'New') == 'New':
                vals['payment_reference'] = self.env['ir.sequence'].next_by_code('marriage.payment') or 'New'
        return super(MarriagePayment, self).create(vals_list)
    
    def action_make_payment(self):
        """Redirect to payment gateway"""
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/marriage/payment/{self.id}',
            'target': 'self',
        }
    
    def action_mark_as_paid(self):
        """Mark payment as paid (for demo/testing)"""
        self.write({
            'payment_status': 'paid',
            'payment_date': fields.Datetime.now(),
            'transaction_id': f'DEMO-{fields.Datetime.now().strftime("%Y%m%d%H%M%S")}'
        })
        
        # Generate certificate
        self.generate_certificate()
        
        return True
    
    def generate_certificate(self):
        """Generate marriage certificate"""
        self.write({
            'certificate_status': 'generated',
            'certificate_download_link': f'/web/marriage/certificate/{self.id}'
        })
        
        # If delivery method is online, mark as delivered
        if self.delivery_method == 'online':
            self.write({
                'certificate_status': 'delivered',
                'certificate_delivery_date': fields.Datetime.now()
            })
        
        # If delivery method is post, generate tracking
        if self.delivery_method == 'post':
            self.write({
                'tracking_number': f'TRK-{fields.Datetime.now().strftime("%Y%m%d%H%M%S")}',
                'tracking_link': f'/web/marriage/tracking/{self.id}'
            })
        
        return True 