from odoo import models, fields, api
from datetime import datetime

class MarriageRegistration(models.Model):
    _name = 'marriage.registration'
    _description = 'Marriage Registration'
    _rec_name = 'registration_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    registration_number = fields.Char('Registration Number', readonly=True, default='New')
    
    # Application Entry Tab
    zone = fields.Selection([
        ('sangali', 'सांगली'),
        ('miraj', 'मिरज'),
        ('kupwad', 'कुपवाड'),
        # Add other zones as needed
    ], string='Zone', required=True, tracking=True)
    
    appli_name = fields.Char('Applicant Name', required=True, tracking=True)
    husband_first_name = fields.Char('Husband First Name')
    husband_middle_name = fields.Char('Husband Middle Name')
    husband_last_name = fields.Char('Husband Last Name')
    
    address = fields.Text('Address', required=True)
    mobile_no = fields.Char('Mobile No', required=True)
    mrg_date = fields.Date('Marriage Date', required=True)
    
    marriage_place_english = fields.Text('Marriage Place English', required=True)
    marriage_place_marathi = fields.Text('Marriage Place Marathi', required=True)
    
    # Document Management
    document_ids = fields.One2many('marriage.document', 'marriage_id', string='Documents')
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    # Husband Details Tab
    husband_full_name = fields.Char('Husband Full Name')
    husband_religion = fields.Char('Husband Religion')
    husband_dob = fields.Date('Husband Date of Birth')
    husband_age = fields.Integer('Husband Age', compute='_compute_age')
    husband_status_before_marriage = fields.Selection([
        ('unmarried', 'Unmarried'),
        ('divorced', 'Divorced'),
        ('widower', 'Widower')
    ], string='Status Before Marriage')
    husband_address = fields.Text('Husband Address')
    husband_photo = fields.Binary('Husband Photo')
    
    # Wife Details Tab
    wife_full_name = fields.Char('Wife Full Name')
    wife_religion = fields.Char('Wife Religion')
    wife_dob = fields.Date('Wife Date of Birth')
    wife_age = fields.Integer('Wife Age', compute='_compute_age')
    wife_status_before_marriage = fields.Selection([
        ('unmarried', 'Unmarried'),
        ('divorced', 'Divorced'),
        ('widow', 'Widow')
    ], string='Status Before Marriage')
    wife_address = fields.Text('Wife Address')
    wife_photo = fields.Binary('Wife Photo')
    
    # Witness Details Tabs
    witness1_name = fields.Char('Witness 1 Name')
    witness1_address = fields.Text('Witness 1 Address')
    witness1_age = fields.Integer('Witness 1 Age')
    witness1_photo = fields.Binary('Witness 1 Photo')
    
    witness2_name = fields.Char('Witness 2 Name')
    witness2_address = fields.Text('Witness 2 Address')
    witness2_age = fields.Integer('Witness 2 Age')
    witness2_photo = fields.Binary('Witness 2 Photo')
    
    witness3_name = fields.Char('Witness 3 Name')
    witness3_address = fields.Text('Witness 3 Address')
    witness3_age = fields.Integer('Witness 3 Age')
    witness3_photo = fields.Binary('Witness 3 Photo')
    
    # Priest Details Tab
    priest_name = fields.Char('Priest Name')
    priest_address = fields.Text('Priest Address')
    priest_religion = fields.Char('Priest Religion')
    priest_age = fields.Integer('Priest Age')
    priest_photo = fields.Binary('Priest Photo')

    # Payment and Certificate Status
    payment_ids = fields.One2many('marriage.payment', 'marriage_id', string='Payments')
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ], string='Payment Status', compute='_compute_payment_status', store=True)

    certificate_status = fields.Selection([
        ('pending', 'Pending'),
        ('generated', 'Generated'),
        ('delivered', 'Delivered')
    ], string='Certificate Status', compute='_compute_certificate_status', store=True)

    @api.depends('husband_dob', 'wife_dob')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.husband_dob:
                record.husband_age = today.year - record.husband_dob.year - ((today.month, today.day) < (record.husband_dob.month, record.husband_dob.day))
            else:
                record.husband_age = 0
                
            if record.wife_dob:
                record.wife_age = today.year - record.wife_dob.year - ((today.month, today.day) < (record.wife_dob.month, record.wife_dob.day))
            else:
                record.wife_age = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('registration_number', 'New') == 'New':
                vals['registration_number'] = self.env['ir.sequence'].next_by_code('marriage.registration') or 'New'
        return super(MarriageRegistration, self).create(vals_list)

    def action_submit(self):
        self.state = 'submitted'

    def action_verify(self):
        self.state = 'verified'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'

    def action_cancel(self):
        self.state = 'cancelled'

    @api.depends('payment_ids', 'payment_ids.payment_status')
    def _compute_payment_status(self):
        for record in self:
            if record.payment_ids:
                latest_payment = record.payment_ids.sorted('create_date', reverse=True)[0]
                record.payment_status = latest_payment.payment_status
            else:
                record.payment_status = 'pending'

    @api.depends('payment_ids', 'payment_ids.certificate_status')
    def _compute_certificate_status(self):
        for record in self:
            if record.payment_ids:
                latest_payment = record.payment_ids.sorted('create_date', reverse=True)[0]
                record.certificate_status = latest_payment.certificate_status
            else:
                record.certificate_status = 'pending'

    def action_create_payment(self):
        """Create payment record for certificate"""
        return {
            'name': 'Certificate Payment',
            'type': 'ir.actions.act_window',
            'res_model': 'marriage.payment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_marriage_id': self.id,
            }
        }


class MarriageDocument(models.Model):
    _name = 'marriage.document'
    _description = 'Marriage Registration Documents'
    
    marriage_id = fields.Many2one('marriage.registration', string='Marriage Registration')
    sr_no = fields.Integer('Sr No')
    document_type = fields.Char('Document Type')
    document_file = fields.Binary('Document File')
    file_name = fields.Char('File Name')
    is_selected = fields.Boolean('Selected') 