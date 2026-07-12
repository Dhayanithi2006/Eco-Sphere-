# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    esg_points = fields.Integer(
        string='ESG Points',
        default=0,
        help="Accumulated ESG points from CSR activities and sustainability challenges."
    )
    
    is_esg_active = fields.Boolean(
        string='Participates in ESG',
        default=True,
        help="Indicates whether this employee participates in sustainability incentives."
    )

    volunteer_hours_logged = fields.Float(
        string='Logged Volunteer Hours',
        compute='_compute_volunteer_hours',
        help="Total volunteer hours logged and approved for this user."
    )

    certification_count = fields.Integer(
        string='ESG Certifications',
        compute='_compute_certifications',
        help="Number of ESG and sustainability training modules completed by this user."
    )

    def _compute_volunteer_hours(self):
        # Placeholder computation, will be fully implemented in ecosphere_social
        for user in self:
            user.volunteer_hours_logged = 0.0

    def _compute_certifications(self):
        # Placeholder computation, will be fully implemented in ecosphere_social
        for user in self:
            user.certification_count = 0
