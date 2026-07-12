# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase  # type: ignore

class TestAi(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestAi, cls).setUpClass()
        cls.company = cls.env.company

        # Setup base indicators for KPI Engine to read
        cls.goal = cls.env['ecosphere.environmental.goal'].create({
            'name': 'Operations Target Limit',
            'company_id': cls.company.id,
            'target_co2_eq': 100.0,
            'current_co2_eq': 90.0,
            'state': 'active'
        })

    def test_01_ai_advisor_generation(self):
        """Test AI advisor simulation and query logging."""
        wizard = self.env['ecosphere.ai.advisor.wizard'].create({
            'query_input': 'Check carbon targets.'
        })

        action = wizard.action_consult_ai()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertTrue(wizard.ai_response, "AI Response was not generated")
        self.assertTrue(wizard.history_id, "AI History log relation not established")

        # Verify history log contains information
        history = wizard.history_id
        self.assertIn("ESG Score", history.prompt)
        self.assertIn("recommendations", history.response)
        self.assertEqual(history.user_rating, 'none')

        # Gami like rating trigger
        wizard.action_rate_like()
        self.assertEqual(history.user_rating, 'like', "Helpful button did not toggle like state in history log")
