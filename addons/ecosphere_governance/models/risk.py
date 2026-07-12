# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereRisk(models.Model):
    _name = 'ecosphere.risk'
    _description = 'Sustainability Risk Register'
    _order = 'score desc, id desc'

    title = fields.Char(string='Risk Description', required=True, index=True)
    
    category = fields.Selection([
        ('environmental', 'Environmental Risk'),
        ('social', 'Social & Corporate Risk'),
        ('governance', 'Governance & Regulatory Risk'),
    ], string='Risk Category', required=True, default='environmental')

    likelihood = fields.Selection([
        ('1', '1 - Rare'),
        ('2', '2 - Unlikely'),
        ('3', '3 - Possible'),
        ('4', '4 - Likely'),
        ('5', '5 - Almost Certain')
    ], string='Likelihood Scale', required=True, default='3')

    impact = fields.Selection([
        ('1', '1 - Negligible'),
        ('2', '2 - Minor'),
        ('3', '3 - Moderate'),
        ('4', '4 - Major'),
        ('5', '5 - Critical')
    ], string='Impact Scale', required=True, default='3')

    score = fields.Integer(
        string='Risk Score (L × I)',
        compute='_compute_risk_score',
        store=True,
        readonly=True,
        help="Risk Score calculation = Likelihood × Impact (Scale 1 to 25)."
    )

    risk_level = fields.Selection([
        ('low', 'Low Risk (1-4)'),
        ('medium', 'Medium Risk (5-12)'),
        ('high', 'High Risk (15-25)')
    ], string='Priority Level', compute='_compute_risk_score', store=True, readonly=True)

    mitigation_plan = fields.Text(string='Mitigation / Action Plan')
    
    owner_id = fields.Many2one(
        'res.users',
        string='Risk Owner',
        required=True,
        default=lambda self: self.env.user
    )

    @api.depends('likelihood', 'impact')
    def _compute_risk_score(self):
        for rec in self:
            l_val = int(rec.likelihood) if rec.likelihood else 3
            i_val = int(rec.impact) if rec.impact else 3
            rec.score = l_val * i_val
            
            # Map score to levels
            if rec.score <= 4:
                rec.risk_level = 'low'
            elif rec.score <= 12:
                rec.risk_level = 'medium'
            else:
                rec.risk_level = 'high'
