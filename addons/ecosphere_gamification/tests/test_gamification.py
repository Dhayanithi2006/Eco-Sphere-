# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase  # type: ignore
from odoo.exceptions import UserError  # type: ignore

class TestGamification(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestGamification, cls).setUpClass()

        # Groups
        cls.group_employee = cls.env.ref('ecosphere_base.group_ecosphere_employee')

        # Test users
        cls.user_employee = cls.env['res.users'].create({
            'name': 'Gami User',
            'login': 'test_gami_login',
            'email': 'gami@test.local',
            'groups_id': [(6, 0, [cls.group_employee.id])],
            'esg_points': 100
        })

        # Badge
        cls.badge = cls.env['ecosphere.badge'].create({
            'name': 'Recycling Specialist',
            'description': 'Recycled over 10kg e-waste.'
        })

        # Challenge
        cls.challenge = cls.env['ecosphere.challenge'].create({
            'name': 'August Zero Waste',
            'start_date': '2026-08-01',
            'end_date': '2026-08-31',
            'target_points': 50,
            'reward_badge_id': cls.badge.id,
            'state': 'active'
        })

        # Reward item
        cls.reward = cls.env['ecosphere.reward'].create({
            'name': 'Eco Cup',
            'point_cost': 40,
            'stock': 3
        })

    def test_01_rewards_redemption_flow(self):
        """Test redemption of store items and point/inventory decreases."""
        # Execute redemption as Gami User
        reward_sudo = self.reward.with_user(self.user_employee)
        reward_sudo.action_redeem()

        # Points should decrease: 100 - 40 = 60
        self.assertEqual(self.user_employee.esg_points, 60, "ESG points not correctly deducted on redemption")
        
        # Stock should decrease: 3 - 1 = 2
        self.assertEqual(self.reward.stock, 2, "Reward stock inventory not decremented")

        # Confirm point history logs have been written
        history = self.env['ecosphere.employee.point.history'].search([
            ('employee_id', '=', self.user_employee.id)
        ])
        self.assertTrue(history, "Points transaction log not generated")
        self.assertEqual(history[0].points_delta, -40, "Points delta value in history is incorrect")

    def test_02_rewards_constraints(self):
        """Verify errors are thrown when user points or item stock are depleted."""
        # Test low points: user now has 100 points in setup, let's deduct points
        self.user_employee.write({'esg_points': 10})
        
        with self.assertRaises(UserError):
            self.reward.with_user(self.user_employee).action_redeem()

        # Reset points, deplete stock
        self.user_employee.write({'esg_points': 100})
        self.reward.write({'stock': 0})
        
        with self.assertRaises(UserError):
            self.reward.with_user(self.user_employee).action_redeem()

    def test_03_challenge_completion_badges(self):
        """Assert badges are awarded to eligible employees when challenge completes."""
        # Create credit history in challenge timeframe
        self.env['ecosphere.employee.point.history'].create({
            'employee_id': self.user_employee.id,
            'points_delta': 60,
            'reason': 'Clean campaign',
            'date': '2026-08-10'
        })

        # Complete campaign
        self.challenge.action_complete()

        # Employee should have received the badge
        self.assertIn(self.badge, self.user_employee.earned_badge_ids, "Reward badge not successfully distributed to employee")
