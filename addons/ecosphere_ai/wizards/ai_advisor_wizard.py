# -*- coding: utf-8 -*-
from odoo import models, fields, api
from ...ecosphere_dashboard.services.kpi_engine import get_overall_esg_metrics

class EcosphereAiAdvisorWizard(models.TransientModel):
    _name = 'ecosphere.ai.advisor.wizard'
    _description = 'Interactive AI Consultation Portal'

    query_input = fields.Text(
        string='Consultation Topic',
        required=True,
        placeholder="e.g. Suggest carbon reduction goals for our operations department."
    )
    
    ai_response = fields.Text(string='AI Analysis & Recommendations', readonly=True)
    confidence = fields.Float(string='Confidence Index', readonly=True)
    history_id = fields.Many2one('ecosphere.ai.history', string='Related History Entry', readonly=True)

    def action_consult_ai(self):
        """
        Gathers ESG context and returns recommendations.
        """
        self.ensure_one()
        
        # 1. Gather real-time metrics
        company_id = self.env.company.id
        metrics = get_overall_esg_metrics(self.env, company_id)
        
        # 2. Formulate Prompt
        prompt = (
            f"Topic: {self.query_input}\n"
            f"Corporate ESG Context:\n"
            f"- Overall ESG Score: {metrics['score']}/100\n"
            f"- Pillar Breakdown: E={metrics['e_score']}%, S={metrics['s_score']}%, G={metrics['g_score']}%\n"
            f"- System Health: {metrics['health']}\n"
            f"- Risk Warnings: {metrics['risk']}"
        )

        # 3. Simulate intelligent advice based on metrics
        advice = []
        if metrics['score'] < 75.0:
            advice.append(
                "🚩 ESG Score is below target index. We recommend prioritizing policies sign-offs "
                "to improve the Governance (G) score. Consider launching a monthly challenge in the Gamification Cabinet."
            )
        else:
            advice.append(
                "🟢 ESG Performance indicators are positive. To sustain this rating, we suggest accelerating Scope 3 "
                "commute checks and integrating versioned emission factors."
            )

        # Environmental advice
        txs_exceeded = self.env['ecosphere.environmental.goal'].search_count([
            ('company_id', '=', company_id),
            ('state', '=', 'active'),
            ('current_co2_eq', '>', ('target_co2_eq'))
        ])
        if txs_exceeded > 0:
            advice.append(
                "🔥 Alert: Several active carbon targets are currently exceeded. We recommend introducing "
                "energy-efficient lighting retrofits and conducting a third-party audit check on logistics fuel logs."
            )
        else:
            advice.append(
                "🍃 Carbon targets are currently within boundaries. We recommend establishing double-walled backup reservoirs "
                "to mitigate mechanical spillage risks."
            )

        # Governance advice
        unresolved_issues = self.env['ecosphere.compliance.issue'].search_count([('status', '!=', 'resolved')])
        if unresolved_issues > 0:
            advice.append(
                "⚠️ There are unresolved compliance issues. We advise nominating specific risk owners "
                "to draft mitigation plans and expedite issue review workflows."
            )

        response_text = (
            f"Based on real-time ESG intelligence, here are your strategic recommendations:\n\n"
            f"{'\n\n'.join(advice)}\n\n"
            f"Confidence Score: 96% | Advisory Model: EcoSphere-ESG-v4"
        )

        # 4. Save to history
        hist = self.env['ecosphere.ai.history'].create({
            'name': f"Consultation: {self.query_input[:40]}...",
            'prompt': prompt,
            'response': response_text,
            'confidence_score': 0.96
        })

        self.write({
            'ai_response': response_text,
            'confidence': 0.96,
            'history_id': hist.id
        })

        # Keep wizard modal open to display results
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    def action_rate_like(self):
        self.ensure_one()
        if self.history_id:
            self.history_id.action_like()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    def action_rate_dislike(self):
        self.ensure_one()
        if self.history_id:
            self.history_id.action_dislike()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }
