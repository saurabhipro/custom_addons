
# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models,fields,api,_
from odoo.exceptions import UserError
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import uuid
import json

class ShHelpdeskTicketButtonsAndConfig(models.Model):
    _inherit = 'sh.helpdesk.ticket'

    done_stage_boolean = fields.Boolean('Done Stage',
                                        compute='_compute_stage_booleans',
                                        store=True)
    cancel_stage_boolean = fields.Boolean('Cancel Stage',
                                          compute='_compute_stage_booleans',
                                          store=True)
    reopen_stage_boolean = fields.Boolean('Reopened Stage',
                                          compute='_compute_stage_booleans',
                                          store=True)
    closed_stage_boolean = fields.Boolean('Closed Stage',
                                          compute='_compute_stage_booleans',
                                          store=True)
    open_boolean = fields.Boolean('Open Ticket',
                                  compute='_compute_stage_booleans',
                                  store=True)
    
    cancel_button_boolean = fields.Boolean("Cancel Button")
    done_button_boolean = fields.Boolean("Done Button")
    
    form_url = fields.Char('Form Url', compute='_compute_form_url')

    # this onchange method add team head when select team           
    @api.onchange('team_id')
    def onchange_team(self):
        for record in self:
            if record.team_id:
                record.team_head = record.team_id.team_head
            else:
                record.team_head = False
    
    # this compute method return domain for assign users
    @api.depends('team_id')
    def _compute_sh_user_ids_domain(self):
        for rec in self:
            domain = [('id', '<', 0)]
            if rec.team_id:
                domain = [('id', 'in', rec.team_id.team_members.ids)]
            rec.sh_user_ids_domain = json.dumps(domain)
    
    # this compute method return domain for sub category
    @api.depends('category_id')
    def _compute_sub_category_id_domain(self):
        for rec in self:
            domain = [('id', '<', 0)]
            if rec.category_id:
                sub_category_ids = self.env['helpdesk.subcategory'].sudo().search([
                ('parent_category_id', '=', self.category_id.id)]).ids
                domain = [('id', 'in', sub_category_ids)]
            rec.sub_category_id_domain = json.dumps(domain)
            
            
    @api.depends('company_id')
    def _compute_sh_display_multi_user(self):
        if self:
            for rec in self:
                rec.sh_display_multi_user = False
                if rec.company_id and rec.company_id.sh_display_multi_user:
                    rec.sh_display_multi_user = True

    @api.depends('company_id')
    def _compute_sh_display_product(self):
        if self:
            for rec in self:
                rec.sh_display_product = False
                if rec.company_id and rec.company_id.sh_configure_activate:
                    rec.sh_display_product = True

    @api.depends('stage_id')
    def _compute_stage_booleans(self):
        for rec in self:
            rec.cancel_stage_boolean = rec.stage_id.id == rec.company_id.cancel_stage_id.id
            rec.done_stage_boolean = rec.stage_id.id == rec.company_id.done_stage_id.id
            rec.reopen_stage_boolean = rec.stage_id.id == rec.company_id.reopen_stage_id.id
            rec.closed_stage_boolean = rec.stage_id.id == rec.company_id.close_stage_id.id
            rec.open_boolean = rec.done_stage_boolean or rec.cancel_stage_boolean or rec.closed_stage_boolean

            # To Manage Button Visibility Based on Stage (We add a setting in the stage to hide/show the button in a particular stage).
            rec.cancel_button_boolean = rec.stage_id.is_cancel_button_visible
            rec.done_button_boolean = rec.stage_id.is_done_button_visible
    
    def action_approve(self):
        # Ensure only one record is being processed
        self.ensure_one()

        # Check if there is a next stage defined
        if self.stage_id.sh_next_stage:
            # Update the current stage to the next stage
            self.stage_id = self.stage_id.sh_next_stage.id

            # Check if there are mail templates defined for the current stage
            if self.stage_id.mail_template_ids:
                # Loop through the mail templates and send emails
                for template in self.stage_id.mail_template_ids:
                    # Send the email (force_send=True means it will be sent immediately)
                    template.sudo().send_mail(self.id, force_send=True)

    def action_draft(self):
        # Ensure there is only one record (as indicated by self.ensure_one())
        self.ensure_one()

        # Check if the company_id and new_stage_id are set
        if self.company_id and self.company_id.new_stage_id:
            # Set the stage_id to the new_stage_id's ID
            self.stage_id = self.company_id.new_stage_id.id

    def action_done(self):
        # Ensure that there is exactly one record (self.ensure_one())
        self.ensure_one()

        # Check if the company and its done_stage_id are defined and if there are mail templates
        if self.company_id and self.company_id.done_stage_id and self.company_id.done_stage_id.mail_template_ids:
            # Loop through mail templates
            for template in self.company_id.done_stage_id.mail_template_ids:
                # Send mail using sudo to avoid access rights issues
                template.sudo().send_mail(self.id, force_send=True)

            # Update the stage to the 'done_stage_id'
            self.stage_id = self.company_id.done_stage_id.id

    def action_reply(self):
        self.ensure_one()  # Ensure that there's only one record, as this code is not designed to handle multiple records

        ir_model_data = self.env['ir.model.data']
        template_id = self.company_id.reply_mail_template_id.id

        try:
            # Look up the XML ID for the email compose form
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[1]
        except ValueError:
            # If not found, set it to False
            compose_form_id = False

        # Define the context for opening the mail compose window
        ctx = {
            'default_model': 'sh.helpdesk.ticket',
            'default_res_ids': self.ids,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'force_email': True
        }
        # if self.team_id.alias_name:
        #     ctx.update({
        #         'reply_to':self.team_id.alias_name +'@'+ self.team_id.alias_domain_id.name
        #     })
        # else:
        #     replay_mail = self.env['fetchmail.server'].search([], limit=1)
        #     ctx.update({
        #         'reply_to':replay_mail.user
        #     })
            
        # Return an action to open the mail compose window
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',  # Open the window in a new tab
            'context': ctx,  # Pass the context to the compose window
        }

    def action_closed(self):
        # Ensure there is only one record
        self.ensure_one()

        if self.company_id and self.company_id.close_stage_id and self.company_id.close_stage_id.mail_template_ids:
            # Send mail using templates associated with the close stage
            for template in self.company_id.close_stage_id.mail_template_ids:
                template.sudo().send_mail(self.id, force_send=True)

            # Update record fields
            self.write({
                'close_date': fields.Datetime.now(),  # Set the close date to the current date and time
                'close_by': self.env.user.id,  # Set the 'close_by' field to the current user's ID
                'closed_stage_boolean': True,  # Set a boolean indicating the stage is closed
                'stage_id': self.company_id.close_stage_id.id  # Update the 'stage_id' to the close stage
            })

    def action_cancel(self):
        # Ensure there is only one record
        self.ensure_one()

        # Check if company, cancel stage, and mail templates are set
        if self.company_id and self.company_id.cancel_stage_id and self.company_id.cancel_stage_id.mail_template_ids:
            # Loop through mail templates and send emails
            for template in self.company_id.cancel_stage_id.mail_template_ids:
                template.sudo().send_mail(self.id, force_send=True)

            # Set the current stage to the cancel stage
            stage_id = self.company_id.cancel_stage_id
            self.stage_id = stage_id.id

            # Set the cancel date to the current datetime
            self.cancel_date = fields.Datetime.now()

            # Set the cancel_by field to the current user's ID
            self.cancel_by = self.env.user.id

            # Set the cancel_stage_boolean to True
            self.cancel_stage_boolean = True

    def action_open(self):
        # Check if company, reopen stage, and mail templates are set
        if self.company_id and self.company_id.reopen_stage_id and self.company_id.reopen_stage_id.mail_template_ids:
            # Loop through mail templates of the reopen stage
            for template in self.company_id.reopen_stage_id.mail_template_ids:
                # Send the mail using the template
                template.sudo().send_mail(self.id, force_send=True)
            
            # Update the record's stage and open_boolean fields
            self.write({
                'stage_id': self.company_id.reopen_stage_id.id,
                'open_boolean': True,
            })

    def action_send_whatsapp(self):
        # Ensure that there is only one record
        self.ensure_one()
        
        # Check if the partner has a mobile number, otherwise raise an error
        if not self.partner_id.mobile:
            raise UserError(_("Partner Mobile Number Not Exist !"))

        # Get the email template
        template = self.env.ref('sh_helpdesk.sh_send_whatsapp_email_template')

        # Define the context for the mail composition
        ctx = {
            'default_model': 'sh.helpdesk.ticket',
            'default_res_ids': self.ids,
            'default_use_template': bool(template.id),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'default_is_wp': True,
        }

        # Search for attachments related to the current ticket and add them to the context
        attachment_ids = self.env['ir.attachment'].sudo().search([
            ('res_model', '=', 'sh.helpdesk.ticket'),
            ('res_id', '=', str(self.id))
        ])
        if attachment_ids:
            ctx.update({'attachment_ids': [(6, 0, attachment_ids.ids)]})

        # Return the action to open the email composition window
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
    
    def preview_ticket(self):
        # Ensure that there is only one record
        self.ensure_one()
        
        # Define an action to open a URL in the current browser window
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),  # Get the URL for the ticket's portal page
        }

    def action_helpdesk_ticket_merge(self):
        # Retrieve selected tickets
        selected_tickets = self.env['sh.helpdesk.ticket'].browse(self.env.context.get('active_ids'))

        # Ensure at least two tickets are selected for merging
        if len(selected_tickets.ids) < 2:
            raise UserError(_('You should select a minimum of two tickets for merging.'))

        # Check if all selected tickets have the same partner
        are_partners_same = all(rec == selected_tickets.mapped('partner_id').ids[0] for rec in selected_tickets.mapped('partner_id').ids)

        # If partners are not the same, raise an error
        if not are_partners_same:
            raise UserError(_('Partners must be the same.'))

        return {
            'name': 'Merge Ticket',
            'res_model': 'sh.helpdesk.ticket.merge.ticket.wizard',
            'view_mode': 'form',
            'context': {
                'default_sh_helpdesk_ticket_ids': [(6, 0, self.env.context.get('active_ids'))],
                'default_sh_partner_id': selected_tickets.mapped('partner_id').ids[0],
            },
            'view_id': self.env.ref('sh_helpdesk.sh_helpdesk_ticket_merge_ticket_wizard_form_view').id,
            'target': 'new',
            'type': 'ir.actions.act_window'
        }
    
    def _compute_form_url(self):
        # Check if there are any records to process
        if self:
            # Get the base URL from configuration parameters
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            # Initialize an empty URL string
            url_str = ''
            # Get the ID of the helpdesk ticket action
            action = self.env.ref('sh_helpdesk.helpdesk_ticket_action').id
            # If a base URL is available, append it to the URL string
            if base_url:
                url_str += str(base_url) + '/web#'
            for rec in self:
                # Construct the URL with parameters for the specific record
                url_str += 'id=' + str(rec.id) + '&action=' + str(action) + '&model=sh.helpdesk.ticket&view_type=form'
                # Assign the URL to the 'form_url' field of the record
                rec.form_url = url_str

    def _compute_access_url(self):
        super(ShHelpdeskTicketButtonsAndConfig, self)._compute_access_url()
        for ticket in self:
            ticket.access_url = '/my/sh_tickets/%s' % (ticket.id)

    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s %s' % ('Ticket', self.name)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.person_name = self.partner_id.name
            self.email = self.partner_id.email
            self.mobile_no = self.partner_id.mobile
        else:
            self.person_name = False
            self.email = False
            self.mobile_no = False 

     # <-- MULTI ACTION FOR MASS UPDATE ASSIGN-TO,MULTI-USER & STATE // ADD/REMOVE FOLLOWER-->
    def action_mass_update_wizard(self):
        return {
            'name':'Mass Update Ticket',
            'res_model':'sh.helpdesk.ticket.mass.update.wizard',
            'view_mode':'form',
            'context': {'default_helpdesks_ticket_ids':[(6, 0, self.env.context.get('active_ids'))],'default_check_sh_display_multi_user':self.env.user.company_id.sh_display_multi_user},
            'view_id':self.env.ref('sh_helpdesk.sh_helpdesk_ticket_mass_update_wizard_form_view').id,
            'target':'new',
            'type':'ir.actions.act_window'
        }

    def get_merge_tickets(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Merged Tickets",
            "view_mode": "tree,form",
            "res_model": "sh.helpdesk.ticket",
            "domain": [("id", "in", self.sh_merge_ticket_ids.ids)],
        }
    
    def _compute_report_url(self):
        for rec in self:
            # Initialize the field to False
            rec.sh_ticket_report_url = False
            
            # Check if the 'sh_pdf_in_message' flag is set in the company settings
            if rec.company_id.sh_pdf_in_message:
                # Get the base URL
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                
                # Create the download URL for the ticket report
                download_url = base_url + rec.get_download_report_url()
                # Update the 'sh_ticket_report_url' field with the download URL
                self.sudo().write({
                    'sh_ticket_report_url': download_url
                })
    
    def get_download_report_url(self):
        url = ''
        if self.id:
            self.ensure_one()
            url = '/download/ht/' + '%s?access_token=%s' % (self.id,
                                                            self._get_token())
        return url

    def _compute_ticket_portal_url_wp(self):
        for rec in self:
            rec.portal_ticket_url_wp = False
            if rec.company_id.sh_pdf_in_message:
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                ticket_url = base_url + rec.get_portal_url()
                self.sudo().write({'portal_ticket_url_wp': ticket_url})

    def _get_token(self):
        """ Get the current record access token """
        if self.report_token:            
            return self.report_token
        else:
            report_token = str(uuid.uuid4())
            self.write({'report_token': report_token})
            return report_token
