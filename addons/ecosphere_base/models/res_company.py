# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    # Configuration and Target Metadata
    sustainability_target_co2 = fields.Float(
        string='Target CO2 Emissions (Tons)',
        default=100.0,
        help="Annual carbon emission threshold target for the company."
    )
    
    esg_reporting_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annually', 'Semi-Annually'),
        ('annually', 'Annually')
    ], string='ESG Reporting Cycle', default='quarterly')

    # Computed fields (NOT STORED, dynamically calculated via Service/Calculation Engine)
    dynamic_esg_score = fields.Float(
        string='Current ESG Score',
        compute='_compute_esg_metrics',
        store=False,
        help="Dynamic ESG score derived from Environmental, Social, and Governance transactions."
    )

    dynamic_esg_health = fields.Selection([
        ('excellent', 'Excellent (Score > 85)'),
        ('good', 'Good (Score 70-85)'),
        ('fair', 'Fair (Score 50-70)'),
        ('poor', 'Poor (Score < 50)')
    ], string='ESG Health Status', compute='_compute_esg_metrics', store=False)

    dynamic_esg_trend = fields.Selection([
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('declining', 'Declining')
    ], string='ESG Trend Direction', compute='_compute_esg_metrics', store=False)

    dynamic_esg_risk = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk')
    ], string='ESG Risk Level', compute='_compute_esg_metrics', store=False)

    def _compute_esg_metrics(self):
        # In a real environment, this delegates calculation to calculation_engine.py
        # Here we mock default behavior so it builds without dependencies.
        for company in self:
            company.dynamic_esg_score = 75.0
            company.dynamic_esg_health = 'good'
            company.dynamic_esg_trend = 'stable'
            company.dynamic_esg_risk = 'medium'
