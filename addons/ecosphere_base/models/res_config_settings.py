# -*- coding: utf-8 -*-
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_ecosphere_ai = fields.Boolean(
        string='Enable AI Decision Intelligence',
        config_parameter='ecosphere.module_ecosphere_ai',
        default=True,
        help="Activate generative AI features for copilot, report summaries, recommendations, and scenario simulations."
    )

    ai_model_name = fields.Char(
        string='AI Model Name',
        config_parameter='ecosphere.ai_model_name',
        default='gemini-2.5-flash',
        help="LLM model configuration (e.g., gemini-2.5-flash, gpt-4o)."
    )

    ai_confidence_threshold = fields.Float(
        string='AI Confidence Threshold (%)',
        config_parameter='ecosphere.ai_confidence_threshold',
        default=80.0,
        help="Confidence threshold below which AI recommendations are flagged as low confidence."
    )

    default_carbon_unit = fields.Selection([
        ('tons', 'Metric Tons (tCO2e)'),
        ('kg', 'Kilograms (kgCO2e)'),
    ], string='Default Carbon Unit', config_parameter='ecosphere.default_carbon_unit', default='tons')

    enable_audit_logs = fields.Boolean(
        string='Enable Strict ESG Auditing',
        config_parameter='ecosphere.enable_audit_logs',
        default=True,
        help="Enable full transaction logging for all ESG-critical operations."
    )

    enable_auto_emission = fields.Boolean(
        string='Enable Auto Emission Calculation',
        config_parameter='ecosphere.enable_auto_emission',
        default=True,
        help="Automatically calculate carbon emissions from purchase, mfg, expense, and fleet log entries."
    )

    enable_evidence_requirement = fields.Boolean(
        string='Enable CSR Proof File Requirement',
        config_parameter='ecosphere.enable_evidence_requirement',
        default=True,
        help="Employees cannot approve CSR activity hours without an attached proof document."
    )

    enable_badge_auto_award = fields.Boolean(
        string='Enable Badge Auto-Awarding',
        config_parameter='ecosphere.enable_badge_auto_award',
        default=True,
        help="Auto-award employee badges as soon as they satisfy unlock requirements."
    )

    notify_compliance_issue = fields.Boolean(
        string='Notify on New Compliance Issues',
        config_parameter='ecosphere.notify_compliance_issue',
        default=True
    )

    notify_csr_approval = fields.Boolean(
        string='Notify on CSR / Challenge Decisions',
        config_parameter='ecosphere.notify_csr_approval',
        default=True
    )

    notify_badge_unlock = fields.Boolean(
        string='Notify on Badge Unlocks',
        config_parameter='ecosphere.notify_badge_unlock',
        default=True
    )
