# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereCsrActivity(models.Model):
    _name = 'ecosphere.csr.activity'
    _description = 'CSR Activities and Programs'
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Program Name', required=True, index=True)
    
    type = fields.Selection([
        ('environmental', 'Environmental Sustainability'),
        ('community', 'Community Outreach'),
        ('education', 'Education & Development'),
    ], string='Focus Area', required=True, default='environmental')

    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date', required=True)
    
    volunteer_hours_target = fields.Float(string='Target Volunteer Hours', default=10.0)
    
    volunteer_hours_actual = fields.Float(
        string='Approved Logged Hours',
        compute='_compute_volunteer_hours_actual',
        store=True,
        help="Aggregated approved volunteer hours from participation logs."
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active Campaign'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', required=True, default='draft')

    @api.depends('state')
    def _compute_volunteer_hours_actual(self):
        for activity in self:
            participations = self.env['ecosphere.csr.participation'].search([
                ('activity_id', '=', activity.id),
                ('state', '=', 'approved')
            ])
            activity.volunteer_hours_actual = sum(participations.mapped('hours_logged'))

    def action_activate(self):
        self.write({'state': 'active'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
