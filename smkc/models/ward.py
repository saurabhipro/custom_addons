from odoo import models, fields, api

class Ward(models.Model):
    _name = 'smkc.ward'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Ward'

    name = fields.Char(string='Ward Name', required=True, tracking=True)
    code = fields.Char(string='Ward Code', tracking=True)
    zone_id = fields.Many2one('smkc.zone', string='Zone', tracking=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True, tracking=True)
    pdf_url = fields.Char(string='PDF URL', tracking=True)
    company_id = fields.Many2one('res.company', string="Company")


    def update_ward(self):
        """ This function will update the pdf_url field and return a dynamic URL. """
        config_parameter = self.env['ir.config_parameter'].sudo()
        base_url = config_parameter.get_param('web.base.url', default=False)

        new_pdf_url = f"{base_url}/download/ward_properties_pdf?ward_id={(self.id)}" 
        self.write({'pdf_url': new_pdf_url})
        property = self.env['smkc.property.info'].search([('ward_no','=',self.id)])
        property.write({'property_status' : 'pdf_downloaded'})

        return {
                'type': 'ir.actions.act_url',
                'url': '/download/ward_properties_pdf?ward_id=%s' % (self.id),
                'target': 'new',
            } 