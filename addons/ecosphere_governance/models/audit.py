# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereAudit(models.Model):
    _name = 'ecosphere.audit'
    _description = 'ESG Compliance Audits'
    _order = 'audit_date desc, id desc'

    name = fields.Char(string='Audit Name/Ref', required=True, index=True)
    
    audit_type = fields.Selection([
        ('internal', 'Internal Audit'),
        ('external', 'Third-Party External Audit'),
    ], string='Audit Type', required=True, default='internal')

    auditor_id = fields.Many2one(
        'res.users',
        string='Lead Auditor',
        required=True
    )

    audit_date = fields.Date(string='Audit Date', required=True, default=fields.Date.today)
    score = fields.Float(string='Compliance Score (0-100)', default=100.0)

    compliance_status = fields.Selection([
        ('compliant', 'Fully Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('critical_non_compliant', 'Critical Non-Compliance')
    ], string='Oversight Rating', required=True, default='compliant')

    notes = fields.Text(string='Auditor Comments & Findings')
