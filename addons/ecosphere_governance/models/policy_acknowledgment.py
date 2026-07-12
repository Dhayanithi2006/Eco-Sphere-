# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcospherePolicyAcknowledgment(models.Model):
    _name = 'ecosphere.policy.acknowledgment'
    _description = 'Employee Policy Acknowledgments'
    _order = 'state asc, acknowledged_date desc'

    policy_id = fields.Many2one(
        'ecosphere.policy',
        string='Policy Document',
        required=True,
        ondelete='cascade',
        index=True
    )

    employee_id = fields.Many2one(
        'res.users',
        string='Employee',
        required=True,
        index=True
    )

    acknowledged_date = fields.Date(string='Acknowledge Date', readonly=True)

    state = fields.Selection([
        ('pending', 'Pending Acknowledgment'),
        ('acknowledged', 'Policy Acknowledged')
    ], string='Status', required=True, default='pending')

    def action_acknowledge(self):
        for rec in self:
            rec.write({
                'state': 'acknowledged',
                'acknowledged_date': fields.Date.today()
            })
            
            # Recalculate certifications on user
            rec.employee_id._compute_certifications()
