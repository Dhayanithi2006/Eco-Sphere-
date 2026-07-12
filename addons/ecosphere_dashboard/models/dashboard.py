# -*- coding: utf-8 -*-
from odoo import models, fields, api
from ..services.kpi_engine import get_overall_esg_metrics

class EcosphereDashboard(models.TransientModel):
    _name = 'ecosphere.dashboard'
    _description = 'Sustainability Performance Dashboard'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    # Computed Overall metrics
    esg_score = fields.Float(string='ESG Score', compute='_compute_metrics')
    esg_health = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='ESG Health', compute='_compute_metrics')
    esg_trend = fields.Selection([
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('declining', 'Declining')
    ], string='ESG Trend', compute='_compute_metrics')
    esg_risk = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk')
    ], string='ESG Risk Level', compute='_compute_metrics')

    # Sub-scores
    e_score = fields.Float(string='Environmental Score', compute='_compute_metrics')
    s_score = fields.Float(string='Social Score', compute='_compute_metrics')
    g_score = fields.Float(string='Governance Score', compute='_compute_metrics')

    # Environmental breakdowns
    total_carbon_emissions = fields.Float(string='Total Footprint (tCO2e)', compute='_compute_environmental')
    scope_1_emissions = fields.Float(string='Scope 1 (Direct)', compute='_compute_environmental')
    scope_2_emissions = fields.Float(string='Scope 2 (Indirect)', compute='_compute_environmental')
    scope_3_emissions = fields.Float(string='Scope 3 (Commute/Waste)', compute='_compute_environmental')

    # Social breakdowns
    total_volunteer_hours = fields.Float(string='Total CSR Hours', compute='_compute_social')
    csr_activities_count = fields.Integer(string='Active CSR Programs', compute='_compute_social')

    # Governance breakdowns
    mitigated_risk_count = fields.Integer(string='Low/Mitigated Risks', compute='_compute_governance')
    active_issue_count = fields.Integer(string='Unresolved Breaches', compute='_compute_governance')
    policy_compliance_rate = fields.Float(string='Policy Completion (%)', compute='_compute_governance')

    def _compute_metrics(self):
        for rec in self:
            metrics = get_overall_esg_metrics(self.env, rec.company_id.id)
            rec.esg_score = metrics['score']
            rec.esg_health = metrics['health']
            rec.esg_trend = metrics['trend']
            rec.esg_risk = metrics['risk']
            rec.e_score = metrics['e_score']
            rec.s_score = metrics['s_score']
            rec.g_score = metrics['g_score']

    def _compute_environmental(self):
        for rec in self:
            txs = self.env['ecosphere.carbon.transaction'].search([
                ('company_id', '=', rec.company_id.id),
                ('state', '=', 'published')
            ])
            rec.total_carbon_emissions = sum(txs.mapped('co2_eq'))
            rec.scope_1_emissions = sum(txs.filtered(lambda t: t.activity_type in ('stationary_combustion', 'mobile_combustion')).mapped('co2_eq'))
            rec.scope_2_emissions = sum(txs.filtered(lambda t: t.activity_type == 'electricity').mapped('co2_eq'))
            rec.scope_3_emissions = sum(txs.filtered(lambda t: t.activity_type in ('travel', 'waste')).mapped('co2_eq'))

    def _compute_social(self):
        for rec in self:
            logs = self.env['ecosphere.csr.participation'].search([('state', '=', 'approved')])
            rec.total_volunteer_hours = sum(logs.mapped('hours_logged'))
            rec.csr_activities_count = self.env['ecosphere.csr.activity'].search_count([('state', '=', 'active')])

    def _compute_governance(self):
        for rec in self:
            rec.mitigated_risk_count = self.env['ecosphere.risk'].search_count([('risk_level', '=', 'low')])
            rec.active_issue_count = self.env['ecosphere.compliance.issue'].search_count([('status', '!=', 'resolved')])
            
            acks = self.env['ecosphere.policy.acknowledgment'].search([])
            if acks:
                signed = len(acks.filtered(lambda a: a.state == 'acknowledged'))
                rec.policy_compliance_rate = (signed / len(acks)) * 100.0
            else:
                rec.policy_compliance_rate = 100.0
