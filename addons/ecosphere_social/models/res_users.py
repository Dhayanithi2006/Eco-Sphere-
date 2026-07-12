# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    def _compute_volunteer_hours(self):
        for user in self:
            participations = self.env['ecosphere.csr.participation'].search([
                ('employee_id', '=', user.id),
                ('state', '=', 'approved')
            ])
            user.volunteer_hours_logged = sum(participations.mapped('hours_logged'))

    def _compute_certifications(self):
        for user in self:
            trainings = self.env['ecosphere.training'].search([
                ('attendee_ids', 'in', [user.id])
            ])
            user.certification_count = len(trainings)
