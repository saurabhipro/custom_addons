from odoo import models, fields, api

class PropertyInfo(models.Model):
    _name = 'smkc.property.dashboard'
    _description = 'Property Information'



    # Dashboard Statistics
    zone_count = fields.Integer(compute='_compute_dashboard_stats', store=False)
    block_count = fields.Integer(compute='_compute_dashboard_stats', store=False)
    uploaded_count = fields.Integer(compute='_compute_dashboard_stats', store=False)
    pdf_downloaded_count = fields.Integer(compute='_compute_dashboard_stats', store=False)
    plate_installed_count = fields.Integer(compute='_compute_dashboard_stats', store=False)
    surveyed_count = fields.Integer(compute='_compute_dashboard_stats', store=False)
    unlocked_count = fields.Integer(compute='_compute_dashboard_stats', store=False)
    visit_again_count = fields.Integer(compute='_compute_dashboard_stats', store=False)

    qr_code = fields.Binary("QR Code", compute="_compute_qr_code", store=False)



    # @api.depends('property_status')
    def _compute_dashboard_stats(self):
        for record in self:
            # Get zone count
            zones = self.env['smkc.zone'].search_count([])
            record.zone_count = zones

            # Get block count (assuming blocks are stored in a separate model)
            blocks = self.env['smkc.ward'].search_count([])  # Using ward as block for now
            record.block_count = blocks

            # Get counts for different statuses
            properties = self.env['smkc.property.info']
            record.uploaded_count = properties.search_count([('property_status', '=', 'uploaded')])
            record.pdf_downloaded_count = properties.search_count([('property_status', '=', 'pdf_downloaded')])
            record.plate_installed_count = properties.search_count([('property_status', '=', 'plate_installed')])
            record.surveyed_count = properties.search_count([('property_status', '=', 'surveyed')])
            record.unlocked_count = properties.search_count([('property_status', '=', 'unlocked')])
            record.visit_again_count = properties.search_count([('property_status', '=', 'discovered')])