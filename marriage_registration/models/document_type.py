from odoo import models, fields, api

class MarriageDocumentType(models.Model):
    _name = 'marriage.document.type'
    _description = 'Marriage Document Types'
    _order = 'sequence'
    
    name = fields.Char('Document Type Name', required=True)
    name_marathi = fields.Char('Document Type Name (Marathi)')
    code = fields.Char('Document Code')
    sequence = fields.Integer('Sequence', default=10)
    is_mandatory = fields.Boolean('Is Mandatory')
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Document code must be unique!')
    ]


class MarriageDocument(models.Model):
    _name = 'marriage.document'
    _description = 'Marriage Registration Documents'
    
    marriage_id = fields.Many2one('marriage.registration', string='Marriage Registration')
    sr_no = fields.Integer('Sr No')
    document_type_id = fields.Many2one('marriage.document.type', string='Document Type')
    document_type = fields.Char(related='document_type_id.name', string='Document Type Name')
    document_type_marathi = fields.Char(related='document_type_id.name_marathi', string='Document Type Name (Marathi)')
    document_file = fields.Binary('Document File')
    file_name = fields.Char('File Name')
    is_selected = fields.Boolean('Selected')
    is_mandatory = fields.Boolean(related='document_type_id.is_mandatory', string='Is Mandatory')
    file_type = fields.Selection([
        ('image', 'Image'),
        ('pdf', 'PDF'),
        ('doc', 'DOC'),
        ('other', 'Other')
    ], string='File Type', default='image') 