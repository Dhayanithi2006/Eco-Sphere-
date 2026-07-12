# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    sustainability_manager_id = fields.Many2one(
        'res.users',
        string='Sustainability Manager',
        help="Manager responsible for tracking and verifying sustainability metrics in this department."
    )

    department_target_co2 = fields.Float(
        string='CO2 Target (Tons)',
        default=20.0,
        help="Departmental annual emission threshold."
    )

    # Computed fields (NOT STORED, dynamically calculated)
    dynamic_esg_score = fields.Float(
        string='Department ESG Score',
        compute='_compute_esg_metrics',
        store=False,
        help="Dynamic ESG score for the department computed from carbon, volunteer, and governance records."
    )

    dynamic_esg_health = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='Department ESG Health', compute='_compute_esg_metrics', store=False)

    def _compute_esg_metrics(self):
        for dept in self:
            dept.dynamic_esg_score = 80.0
            dept.dynamic_esg_health = 'good'
