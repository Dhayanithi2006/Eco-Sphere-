# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase  # type: ignore
from odoo.exceptions import ValidationError, UserError  # type: ignore

class TestSocial(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestSocial, cls).setUpClass()

        # Groups
        cls.group_employee = cls.env.ref('ecosphere_base.group_ecosphere_employee')
        cls.group_manager = cls.env.ref('ecosphere_base.group_ecosphere_manager')

        # Test user
        cls.user_employee = cls.env['res.users'].create({
            'name': 'Social Employee',
            'login': 'test_soc_emp_login',
            'email': 'emp_soc@test.local',
            'groups_id': [(6, 0, [cls.group_employee.id])]
        })

        # CSR Campaign
        cls.activity_test = cls.env['ecosphere.csr.activity'].create({
            'name': 'Beach Clean-up 2026',
            'type': 'environmental',
            'start_date': '2026-07-01',
            'end_date': '2026-07-31',
            'volunteer_hours_target': 50.0,
            'state': 'active'
        })

    def test_01_volunteer_hours_constraints(self):
        """Verify that negative volunteer hours are rejected by ORM constraints."""
        with self.assertRaises(ValidationError):
            self.env['ecosphere.csr.participation'].create({
                'activity_id': self.activity_test.id,
                'employee_id': self.user_employee.id,
                'hours_logged': -5.0
            })

    def test_02_points_accrual_workflow(self):
        """Verify state transitions and point allocation on hours approval."""
        participation = self.env['ecosphere.csr.participation'].create({
            'activity_id': self.activity_test.id,
            'employee_id': self.user_employee.id,
            'hours_logged': 6.0
        })

        self.assertEqual(participation.state, 'draft', "Should default to draft state")
        self.assertEqual(self.user_employee.esg_points, 0, "No points should be awarded yet")

        # Submit
        participation.action_submit()
        self.assertEqual(participation.state, 'submitted')

        # Approve
        participation.action_approve()
        self.assertEqual(participation.state, 'approved')
        
        # Verify points: 6 hours * 10 = 60 points
        self.assertEqual(self.user_employee.esg_points, 60, "ESG points not correctly allocated on approval")
        self.assertEqual(self.activity_test.volunteer_hours_actual, 6.0, "Activity total approved hours not aggregated")

    def test_03_user_computed_metrics(self):
        """Verify user volunteer hours and certification metrics recalculations."""
        # Check current volunteer hours
        self.user_employee._compute_volunteer_hours()
        self.assertEqual(self.user_employee.volunteer_hours_logged, 0.0)

        # Create approved volunteer hours
        participation = self.env['ecosphere.csr.participation'].create({
            'activity_id': self.activity_test.id,
            'employee_id': self.user_employee.id,
            'hours_logged': 10.0,
            'state': 'approved'
        })
        # Force compute
        self.user_employee._compute_volunteer_hours()
        self.assertEqual(self.user_employee.volunteer_hours_logged, 10.0)

        # Create training completion
        training = self.env['ecosphere.training'].create({
            'name': 'Green Building Standard',
            'type': 'sustainability',
            'date': '2026-07-12',
            'attendee_ids': [(4, self.user_employee.id)]
        })
        self.user_employee._compute_certifications()
        self.assertEqual(self.user_employee.certification_count, 1)
