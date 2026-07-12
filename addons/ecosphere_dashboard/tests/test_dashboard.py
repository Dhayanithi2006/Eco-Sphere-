# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase  # type: ignore
from ..services.kpi_engine import (
    get_environmental_score,
    get_social_score,
    get_governance_score,
    get_overall_esg_metrics
)

class TestDashboard(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestDashboard, cls).setUpClass()
        cls.company = cls.env.company

        # Setup standard baseline indicators to compute scores
        cls.goal = cls.env['ecosphere.environmental.goal'].create({
            'name': 'Reduce Warehouse Footprint',
            'company_id': cls.company.id,
            'target_co2_eq': 100.0,
            'current_co2_eq': 80.0,
            'state': 'active'
        })

        cls.training = cls.env['ecosphere.training'].create({
            'name': 'Diversity & Ethics 101',
            'completion_rate': 90.0
        })

        cls.badge = cls.env['ecosphere.badge'].create({
            'name': 'Base Badge'
        })
        cls.policy = cls.env['ecosphere.policy'].create({
            'name': 'Company Handbook',
            'version': '1.0',
            'state': 'published'
        })

        # Generate some acknowledgments to count rates
        cls.user_1 = cls.env['res.users'].create({
            'name': 'Test G1',
            'login': 'test_g1_login',
            'email': 'g1@test.local'
        })
        cls.user_2 = cls.env['res.users'].create({
            'name': 'Test G2',
            'login': 'test_g2_login',
            'email': 'g2@test.local'
        })

        cls.ack_1 = cls.env['ecosphere.policy.acknowledgment'].create({
            'policy_id': cls.policy.id,
            'employee_id': cls.user_1.id,
            'state': 'acknowledged'
        })
        cls.ack_2 = cls.env['ecosphere.policy.acknowledgment'].create({
            'policy_id': cls.policy.id,
            'employee_id': cls.user_2.id,
            'state': 'pending'
        })

    def test_01_environmental_score(self):
        """Verify carbon target completion outputs 100% since current is less than target."""
        score = get_environmental_score(self.env, self.company.id)
        self.assertEqual(score, 100.0, "E Score should be 100.0 since goal is not exceeded")

        # Exceed target
        self.goal.write({'current_co2_eq': 120.0}) # 20% excess -> 80% performance
        score = get_environmental_score(self.env, self.company.id)
        self.assertEqual(score, 80.0, "E Score should evaluate to 80.0")

    def test_02_social_score(self):
        """Verify training rate aggregates correctly."""
        score = get_social_score(self.env, self.company.id)
        # No CSR activities, so CSR defaults to 100. Training completion is 90. Average = 95.
        self.assertEqual(score, 95.0, "S Score should be 95.0")

    def test_03_governance_score(self):
        """Verify policy sign-offs and risk penalties apply."""
        score = get_governance_score(self.env, self.company.id)
        # Sign-off: 1/2 = 50%. Risks: 0 risks -> factor is 100%. G Score = 50 * 0.6 + 100 * 0.4 = 70.
        self.assertEqual(score, 70.0, "G Score should be 70.0")

    def test_04_overall_weighted_esg(self):
        """Verify consolidation math using 40/30/30 weighting."""
        # E Score: 100
        # S Score: 95
        # G Score: 70
        # Weighted = 100 * 0.4 + 95 * 0.3 + 70 * 0.3 = 40 + 28.5 + 21 = 89.5
        metrics = get_overall_esg_metrics(self.env, self.company.id)
        self.assertEqual(metrics['score'], 89.5, "Overall ESG Score consolidation is incorrect")
        self.assertEqual(metrics['health'], 'excellent', "Score 89.5 should map to excellent health rating")

    def test_05_transient_dashboard_model(self):
        """Verify transient model queries match KPI outputs."""
        dashboard = self.env['ecosphere.dashboard'].create({
            'company_id': self.company.id
        })
        self.assertEqual(dashboard.esg_score, 89.5)
        self.assertEqual(dashboard.e_score, 100.0)
        self.assertEqual(dashboard.s_score, 95.0)
        self.assertEqual(dashboard.g_score, 70.0)
        self.assertEqual(dashboard.policy_compliance_rate, 50.0)
