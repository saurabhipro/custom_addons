# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import logging
from odoo import models, fields, api, _
import random
from odoo.exceptions import UserError
from odoo.tools import email_re
_logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _name = 'sh.helpdesk.ticket'
    _inherit = ['portal.mixin','mail.activity.mixin']
    _description = "Helpdesk Ticket"
    _order = 'id DESC'
    _rec_name = 'name'
    _primary_email = 'email'

    def unlink(self):
        for record in self:
            find_analysis_record = self.env['sh.helpdesk.sla.analysis'].sudo().search([('sh_helpdesk_ticket_id','=',record.id)])
            find_analysis_record.unlink()
        super(HelpdeskTicket, self).unlink()

    def get_deafult_company(self):
        company_id = self.env.company
        return company_id

    @api.model
    def get_default_stage(self):
        company_id = self.env.company
        stage_id = self.env['helpdesk.stages'].sudo().search(
            [('id', '=', company_id.new_stage_id.id)], limit=1)
        return stage_id.id

    @api.model
    def default_due_date(self):
        return fields.Datetime.now()

    name = fields.Char("Name", tracking=True)
    company_id = fields.Many2one('res.company',
                                 string="Company",
                                 default=get_deafult_company)
    state = fields.Selection([('customer_replied', 'Customer Replied'),
                              ('staff_replied', 'Staff Replied')],
                             string="Replied Status",
                             default='customer_replied',
                             required=True,
                             tracking=True)
    active = fields.Boolean(
        'Active',
        default=True,
        help=
        "If unchecked, it will allow you to hide the product without removing it."
    )
    ticket_from_website = fields.Boolean('Ticket From Website')
    ticket_from_portal = fields.Boolean('Ticket From Portal')
    cancel_reason = fields.Char("Cancel Reason", tracking=True, translate=True)
    tag_ids = fields.Many2many('helpdesk.tags', string="Tags")
    priority = fields.Many2one('helpdesk.priority',
                               string='Priority',
                               tracking=True)
    stage_id = fields.Many2one('helpdesk.stages',
                               string="Stage",
                               default=get_default_stage,
                               tracking=True,
                               index=True,)
    ticket_type = fields.Many2one('sh.helpdesk.ticket.type',
                                  string='Ticket Type',
                                  tracking=True)
    team_id = fields.Many2one('sh.helpdesk.team', string='Team')
    team_head = fields.Many2one('res.users', "Team Head", tracking=True)
    user_id = fields.Many2one('res.users',
                              string="Assigned User",
                              tracking=True)
    subject_id = fields.Many2one('helpdesk.sub.type',
                                 string='Ticket Subject Type',
                                 tracking=True)
    category_id = fields.Many2one('helpdesk.category',
                                  string="Category",
                                  tracking=True)
    sub_category_id = fields.Many2one('helpdesk.subcategory',
                                      string="Sub Category")
    sub_category_id_domain = fields.Char("Sub category domain",compute="_compute_sub_category_id_domain", store=True)
    partner_id = fields.Many2one('res.partner', string='Partner',tracking=True,required=True)
    person_name = fields.Char(string='Person Name', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    close_date = fields.Datetime(string='Close Date', tracking=True)
    close_by = fields.Many2one('res.users', string='Closed By', tracking=True)
    cancel_date = fields.Datetime(string='Cancelled Date', tracking=True)
    cancel_by = fields.Many2one('res.users',
                                string='Cancelled By',
                                tracking=True)
    replied_date = fields.Datetime('Replied Date', tracking=True)
    product_ids = fields.Many2many('product.product', string='Products')

    comment = fields.Text(string="Comment", tracking=True, translate=True)
    description = fields.Html('Description')
    color = fields.Integer(string='Color Index')
    priority_new = fields.Selection([('1', 'Very Low'), ('2', 'Low'),
                                     ('3', 'Normal'), ('4', 'High'),
                                     ('5', 'Very High'), ('6', 'Excellent')],
                                    string="Customer Rating",
                                    tracking=True)
    customer_comment = fields.Text("Customer Comment", tracking=True)

    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
    
    category_bool = fields.Boolean(string='Category Setting',
                                   related='company_id.category',
                                   store=True)
    sub_category_bool = fields.Boolean(string='Sub Category Setting',
                                       related='company_id.sub_category',
                                       store=True)
    rating_bool = fields.Boolean(string='Rating Setting',
                                 related='company_id.customer_rating',
                                 store=True)
    ticket_allocated = fields.Boolean("Allocated")
    sh_user_ids = fields.Many2many('res.users', string="Assign Multi Users")
    sh_user_ids_domain = fields.Char("users domain",compute="_compute_sh_user_ids_domain", store=True)
    # sh_display_multi_user = fields.Boolean()
    sh_display_multi_user = fields.Boolean(compute="_compute_sh_display_multi_user")
    sh_status = fields.Selection([('sla_failed', 'Failed'),
                                  ('sla_passed', 'Passed'),
                                  ('sh_partially_passed', 'Partially Passed')],
                                 string="Status")
    
    sh_status_boolean = fields.Boolean(compute="_compute_state_boolean") 
    sh_days_to_reach = fields.Float(string='SLA reached duration')
    sh_days_to_late = fields.Float(string='SLA late duration')
    sh_due_date = fields.Datetime('Reminder Due Date',
                                  default=default_due_date)
    sh_ticket_alarm_ids = fields.Many2many('sh.ticket.alarm',
                                           string='Ticket Reminders')
    sh_ticket_report_url = fields.Char(compute='_compute_report_url')
    report_token = fields.Char("Access Token")
    portal_ticket_url_wp = fields.Char(compute='_compute_ticket_portal_url_wp')
    mobile_no = fields.Char('Mobile')
    email_subject = fields.Char('Subject')

    sh_display_product = fields.Boolean(compute='_compute_sh_display_product')

    sh_merge_ticket_ids = fields.Many2many('sh.helpdesk.ticket',relation='model_merge_helpdesk_ticket',column1="helpdesk", column2="ticket", string='Merge Tickets')

    sh_merge_ticket_count = fields.Integer(compute="_compute_count_merge_ticket")

    def _compute_count_merge_ticket(self):
        for record in self:
            record.sh_merge_ticket_count = len(record.sh_merge_ticket_ids) if record.sh_merge_ticket_ids else 0

    def _compute_state_boolean(self):
        if self:
            for rec in self:
                rec.sh_status_boolean = False
                sla_passed = rec.sh_sla_status_ids.filtered(
                    lambda x: x.sh_status == 'sla_passed')
                sla_failed = rec.sh_sla_status_ids.filtered(
                    lambda x: x.sh_status == 'sla_failed')
                if sla_passed:
                    rec.sh_status = 'sla_passed'
                elif sla_failed:
                    rec.sh_status = 'sla_failed'
                elif rec.sh_sla_status_ids:
                    rec.sh_status = 'sh_partially_passed'
                else:
                    rec.sh_status = ""
                    
    # This onchange method add team head when select team
    # @api.onchange('team_id')
    # def onchange_team(self):
    #     for record in self:
    #         if record.sh_user_ids or record.user_id:
    #             record.sh_user_ids = False
    #             record.user_id = False
    #         if record.team_id:
    #             record.team_head = record.team_id.team_head
    #         else:
    #             record.team_head = False
               
# this compute method return domain for assign users
    # @api.depends('team_id')F
    # def _compute_sh_user_ids_domain(self):
    #     for rec in self:
    #         domain = [('id', '<', 0)]
    #         if rec.team_id:
    #             domain = [('id', 'in', rec.team_id.team_members.ids)]
    #         rec.sh_user_ids_domain = json.dumps(domain)
                
# this compute method return domain for sub category
    # @api.depends('category_id')
    # def _compute_sub_category_id_domain(self):
    #     for rec in self:
    #         domain = [('id', '<', 0)]
    #         if rec.category_id:
    #             sub_category_ids = self.env['helpdesk.subcategory'].sudo().search([
    #             ('parent_category_id', '=', self.category_id.id)]).ids
    #             domain = [('id', 'in', sub_category_ids)]
    #         rec.sub_category_id_domain = json.dumps(domain)
            
            
#====THIS METHOD CALLED IN Create METHOD=====#
    def _create_partner(self, vals):
        # this code for create new partner 
        if not vals.get('partner_id') and vals.get('email', False):
            emails = email_re.findall(vals.get('email') or '')
            email = emails and emails[0] or ''
            name = str(vals.get('email').split('"')[1])
            partner_id = self.env['res.partner'].create({'name': name,'email': email,'company_type': 'person'})
            vals.update({'partner_id': partner_id.id,'email': email,'person_name': partner_id.name})

    def _allocate_team(self, vals):
        # this code when ticket create by support user default value add
        if self.env.user.has_group('sh_helpdesk.helpdesk_group_user') and not self.env.user.has_group('sh_helpdesk.helpdesk_group_team_leader'):
            find_team = self.env['sh.helpdesk.team'].search(['|', ('team_members', 'in', [self.env.user.id]), ('team_head', '=', self.env.user.id)], limit=1)
            if find_team:
                vals.update({
                    'team_id': find_team.id,
                    'team_head': find_team.team_head.id,
                    'user_id': self.env.user.id,
                })

    def _set_defaults(self, vals):
        # this code if in setting default team and assign user added than add that in ticket
        if self.env.company.sh_default_team_id and not vals.get('team_id') and not vals.get('user_id'):
            vals.update({
                'team_id': self.env.company.sh_default_team_id.id,
                'team_head': self.env.company.sh_default_team_id.sudo().team_head.id,
                'user_id': self.env.company.sh_default_user_id.id,
            })

    def _customize_ticket(self, vals):
        vals['color'] = random.randrange(1, 10)
        vals['name'] = self.env['ir.sequence'].next_by_code('sh.helpdesk.ticket') or _('New')
        company_id = self.env.company
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if company_id.new_stage_id:
            vals['stage_id'] = company_id.new_stage_id.id
    
    def _send_mail(self, res):
        #send mail when create ticket
        if res.ticket_from_website and res.company_id.new_stage_id.mail_template_ids and res.partner_id:
            for template in res.company_id.new_stage_id.mail_template_ids:
                template.sudo().send_mail(res.id, force_send=True)
        elif not res.ticket_from_website and res.company_id.new_stage_id.mail_template_ids and res.partner_id:
            for template in res.company_id.new_stage_id.mail_template_ids:
                template.sudo().send_mail(res.id, force_send=True)

    def _allocate_mail(self, res):
        allocation_template = res.company_id.allocation_mail_template_id
        email_formatted = []
        if res.team_id and res.team_head and res.user_id and res.sh_user_ids: 
            if res.team_head.partner_id.email_formatted not in email_formatted:
                email_formatted.append(res.team_head.partner_id.email_formatted)
            if res.user_id.partner_id.email and res.user_id.partner_id.email_formatted not in email_formatted:
                email_formatted.append(res.user_id.partner_id.email_formatted)
            for user in res.sh_user_ids:
                if user.id != res.user_id.id:
                    if user.partner_id.email_formatted not in email_formatted:
                        email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(res.team_head.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                allocation_template.sudo().send_mail(res.id,force_send=True,email_values=email_values)
                res.ticket_allocated = True

        elif res.team_id and res.team_head and res.user_id and not res.sh_user_ids:
            if res.team_head.partner_id.email_formatted not in email_formatted:
                email_formatted.append(res.team_head.partner_id.email_formatted)
            if res.user_id.partner_id.email and res.user_id.partner_id.email_formatted not in email_formatted:
                email_formatted.append(res.user_id.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(res.team_head.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                allocation_template.sudo().send_mail(res.id,force_send=True,email_values=email_values)
                res.ticket_allocated = True

        elif res.team_id and res.team_head and not res.user_id and res.sh_user_ids:
            for user in res.sh_user_ids:
                if user.partner_id.email and user.partner_id.email_formatted not in email_formatted:
                    email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(res.team_head.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                allocation_template.sudo().send_mail(res.id,force_send=True,email_values=email_values)
                res.ticket_allocated = True

        elif not res.team_id and not res.team_head and res.user_id and res.sh_user_ids:
            if res.user_id.partner_id.email_formatted not in email_formatted:
                email_formatted.append(res.user_id.partner_id.email_formatted)
            for user in res.sh_user_ids:
                if user.id != res.user_id.id:
                    if user.partner_id.email and user.partner_id.email_formatted not in email_formatted:
                        email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(res.company_id.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                allocation_template.sudo().send_mail(res.id,force_send=True,email_values=email_values)
                res.ticket_allocated = True

        elif not res.team_id and not res.team_head and res.user_id and not res.sh_user_ids:
            allocation_template.sudo().write({
                'email_from':
                str(res.company_id.partner_id.email_formatted),
                'email_to':
                str(res.user_id.partner_id.email_formatted),
                'partner_to':
                str(res.user_id.partner_id.id)
            })
            email_values = {
                        'email_from': str(res.company_id.partner_id.email_formatted),
                        'email_to': str(res.user_id.partner_id.email_formatted)
                    }
            if allocation_template:
                allocation_template.sudo().send_mail(res.id,force_send=True,email_values=email_values)
                res.ticket_allocated = True
            
        elif not res.team_id and not res.team_head and not res.user_id and res.sh_user_ids:
            for user in res.sh_user_ids:
                if user.partner_id.email and user.partner_id.email_formatted not in email_formatted:
                    email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(res.company_id.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                allocation_template.sudo().send_mail(res.id,force_send=True,email_values=email_values)
                res.ticket_allocated = True

    def _subscribe_partner(self,res):
        if self.env.company.sh_auto_add_customer_as_follower and res.partner_id:
                        res.message_subscribe(partner_ids=res.partner_id.ids)
        if res.sh_user_ids:
            if res.sh_user_ids.mapped('partner_id'):
                res.message_subscribe(partner_ids=res.sh_user_ids.mapped('partner_id').ids)
    
    def update_ir_attachment(self,result):
        if result.attachment_ids:
            result.attachment_ids.sudo().write({
                'res_id' : result.id,
                'res_model' : 'sh.helpdesk.ticket'
            })

    @api.model_create_multi
    def create(self, values):
        for value in values:
            try:
                self._create_partner(value)
                self._allocate_team(value)
                self._customize_ticket(value)                
            except Exception as e:                                 
                _logger.exception("Error during ticket creation: %s", e)
                continue
            self._set_defaults(value)

        result = super(HelpdeskTicket, self).create(values)
        self.update_ir_attachment(result)
        self._subscribe_partner(result)
        result.sh_apply_sla()
        for each_result in result:
            self._send_mail(each_result)
            self._allocate_mail(each_result)

        return result
    
#====THIS METHOD CALLED IN Write METHOD=====#
    def set_stage_id(self, vals):
        if vals.get('state'):
            if vals.get('state') == 'customer_replied':
                if self.env.user.company_id.sh_customer_replied:
                    for rec in self:
                        if rec.stage_id.id != self.env.user.company_id.new_stage_id.id:
                            vals.update({
                                'stage_id': self.env.user.company_id.sh_customer_replied_stage_id.id
                            })
            elif vals.get('state') == 'staff_replied':
                if self.env.user.company_id.sh_staff_replied:
                    for rec in self:
                        if rec.stage_id.id != self.env.user.company_id.new_stage_id.id:
                            vals.update({
                                'stage_id': self.env.user.company_id.sh_staff_replied_stage_id.id
                            })

    def check_access(self, vals):
        user_groups = self.env.user.groups_id.ids
        if vals.get('stage_id'):
            stage_id = self.env['helpdesk.stages'].sudo().search([('id', '=', vals.get('stage_id'))], limit=1)
            if stage_id and stage_id.sh_group_ids:
                is_group_exist = False
                list_user_groups = user_groups
                list_stage_groups = stage_id.sh_group_ids.ids
                
                for item in list_stage_groups:
                    if item in list_user_groups:
                        is_group_exist = True
                        break
                if not is_group_exist:
                    raise UserError(_('You do not have access to edit this support request.'))
                    # raise UserError(_('You do not have access to edit this support request.'))

    def send_mail_on_partner_change(self, vals):
        if vals.get('partner_id') and self.env.company.new_stage_id.mail_template_ids:
            for rec in self:
                for template in rec.company_id.new_stage_id.mail_template_ids:
                    template.sudo().send_mail(rec.id, force_send=True)
    
    def allocate_ticket(self, vals):
        allocation_template = self.env.company.allocation_mail_template_id
        email_formatted = []
        if vals.get('team_id') and vals.get('team_head') and vals.get('user_id') and vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            team_head = self.env['res.users'].sudo().browse(vals.get('team_head'))
            user_id = self.env['res.users'].sudo().browse(vals.get('user_id'))
            if team_head.partner_id.email_formatted not in email_formatted:
                email_formatted.append(team_head.partner_id.email_formatted)
            if user_id.partner_id.email_formatted not in email_formatted:
                email_formatted.append(user_id.partner_id.email_formatted)
            users = vals.get('sh_user_ids')[0][2]
            user_ids = self.env['res.users'].sudo().browse(users)
            for user in user_ids:
                if user.id != user_id.id:
                    if user.partner_id.email and user.partner_id.email_formatted not in email_formatted:
                        email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(team_head.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                for rec in self:
                    allocation_template.sudo().send_mail(
                        rec.id, force_send=True, email_values=email_values)
                    rec.ticket_allocated = True

        elif vals.get('team_id') and vals.get('team_head') and vals.get('user_id') and not vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            team_head = self.env['res.users'].sudo().browse(vals.get('team_head'))
            user_id = self.env['res.users'].sudo().browse(vals.get('user_id'))
            if team_head.partner_id.email_formatted not in email_formatted:
                email_formatted.append(team_head.partner_id.email_formatted)
            if user_id.partner_id.email_formatted not in email_formatted:
                email_formatted.append(user_id.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(team_head.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                for rec in self:
                    allocation_template.sudo().send_mail(
                        rec.id, force_send=True, email_values=email_values)
                    rec.ticket_allocated = True

        elif vals.get('team_id') and vals.get('team_head') and not vals.get('user_id') and vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            users = vals.get('sh_user_ids')[0][2]
            user_ids = self.env['res.users'].sudo().browse(users)
            team_head = self.env['res.users'].sudo().browse(vals.get('team_head'))
            for user in user_ids:
                if user.partner_id.email_formatted not in email_formatted:
                    email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(team_head.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                for rec in self:
                    allocation_template.sudo().send_mail(
                        rec.id, force_send=True, email_values=email_values)
                    rec.ticket_allocated = True

        elif not vals.get('team_id') and not vals.get('team_head') and vals.get('user_id') and vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            user_id = self.env['res.users'].sudo().browse(vals.get('user_id'))
            users = vals.get('sh_user_ids')[0][2]
            user_ids = self.env['res.users'].sudo().browse(users)
            if user_id.partner_id.email_formatted not in email_formatted:
                email_formatted.append(user_id.partner_id.email_formatted)
            for user in user_ids:
                if user.id != user_id.id:
                    if user.partner_id.email_formatted not in email_formatted:
                        email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(team_head.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                for rec in self:
                    allocation_template.sudo().send_mail(
                        rec.id, force_send=True, email_values=email_values)
                    rec.ticket_allocated = True
        elif not vals.get('team_id') and not vals.get('team_head') and vals.get('user_id') and not vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            user_id = self.env['res.users'].sudo().browse(vals.get('user_id'))
            email_values = {
                'email_from': str(self.env.company.partner_id.email_formatted),
                'email_to': str(user_id.partner_id.email_formatted)
            }
            if allocation_template:
                for rec in self:
                    allocation_template.sudo().send_mail(
                        rec.id, force_send=True, email_values=email_values)
                    rec.ticket_allocated = True
        elif not vals.get('team_id') and not vals.get('team_head') and not vals.get('user_id') and vals.get('sh_user_ids') and not vals.get('ticket_allocated'):
            users = vals.get('sh_user_ids')[0][2]
            user_ids = self.env['res.users'].sudo().browse(users)
            for user in user_ids:
                if user.partner_id.email and user.partner_id.email_formatted not in email_formatted:
                    email_formatted.append(user.partner_id.email_formatted)
            email_formatted_str = ','.join(email_formatted)
            email_values = {
                'email_from': str(self.env.company.partner_id.email_formatted),
                'email_to': email_formatted_str
            }
            if allocation_template:
                for rec in self:
                    allocation_template.sudo().send_mail(
                        rec.id, force_send=True, email_values=email_values)
                    rec.ticket_allocated = True
        
            
    def write(self, vals):
        for rec in self:
            try:
                rec.set_stage_id(vals)
            except Exception as e:
                _logger.exception("Error when stage id not set: %s", e)
            rec.check_access(vals)
            try:
                rec.send_mail_on_partner_change(vals)
            except Exception as e:
                _logger.exception("Error when partner not have email: %s", e)

        res = super(HelpdeskTicket, self).write(vals)
        self.update_ir_attachment(self)
        for rec in self:
            try:
                rec.allocate_ticket(vals)
            except Exception as e:
                _logger.exception("Error when partner not have email: %s", e)

        if vals.get('sh_user_ids'):
            if self.sh_user_ids:
                if self.sh_user_ids.mapped('partner_id'):
                    self.message_subscribe(partner_ids=self.sh_user_ids.mapped('partner_id').ids)
        # ***************************************************
        # SLA APPLY
        # ***************************************************
        if vals.get('ticket_type') or vals.get('team_id'):
            for each_record in self:                                    
                    each_record.sh_apply_sla()
        if vals.get('stage_id'):
            for each_record in self:
                each_record.sh_conclude_sla()
            if vals.get('sh_user_ids'):
                if rec.sh_user_ids:
                    if rec.sh_user_ids.mapped('partner_id'):
                        rec.message_subscribe(partner_ids=rec.sh_user_ids.mapped('partner_id').ids)
        return res
    
        # ***************************************************
        # SLA APPLY
        # ***************************************************
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        res = super(HelpdeskTicket, self).copy(default=default)
        res.state = 'customer_replied'
        return res
