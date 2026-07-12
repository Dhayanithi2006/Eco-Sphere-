# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase  # type: ignore
from odoo.exceptions import AccessError  # type: ignore

class TestEnvironmental(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestEnvironmental, cls).setUpClass()

        # Groups & users
        cls.group_employee = cls.env.ref('ecosphere_base.group_ecosphere_employee')
        cls.group_manager = cls.env.ref('ecosphere_base.group_ecosphere_manager')

        cls.user_employee = cls.env['res.users'].create({
            'name': 'Emp Test User',
            'login': 'test_emp_env_login',
            'email': 'emp_env@test.local',
            'groups_id': [(6, 0, [cls.group_employee.id])]
        })

        cls.user_manager = cls.env['res.users'].create({
            'name': 'Mgr Test User',
            'login': 'test_mgr_env_login',
            'email': 'mgr_env@test.local',
            'groups_id': [(6, 0, [cls.group_manager.id])]
        })

        # Department setup
        cls.dept_operations = cls.env['hr.department'].create({
            'name': 'Operations',
            'sustainability_manager_id': cls.user_manager.id
        })

        cls.dept_facilities = cls.env['hr.department'].create({
            'name': 'Facilities'
        })

        # Create emission factor
        cls.factor_electricity = cls.env['ecosphere.emission.factor'].create({
            'name': 'Electricity Factor 2026',
            'version': '2026.1',
            'factor': 0.0008,
            'unit_from': 'kwh',
            'valid_from': '2026-01-01',
            'valid_to': '2026-12-31'
        })

        # Create Goal
        cls.goal_operations = cls.env['ecosphere.environmental.goal'].create({
            'name': 'Ops Q3 Emissions Cap Test',
            'start_date': '2026-07-01',
            'end_date': '2026-09-30',
            'target_co2_eq': 100.0,
            'department_id': cls.dept_operations.id,
            'state': 'active'
        })

    def test_01_co2_calculation(self):
        """Test calculation of CO2 equivalents on transaction creation."""
        tx = self.env['ecosphere.carbon.transaction'].create({
            'name': 'Warehouse Electricity Bill',
            'date': '2026-07-10',
            'activity_type': 'electricity',
            'quantity': 50000.0, # 50000 * 0.0008 = 40.0 tCO2e
            'emission_factor_id': self.factor_electricity.id,
            'department_id': self.dept_operations.id
        })
        self.assertEqual(tx.co2_eq, 40.0, "CO2 equivalent calculation is incorrect")

    def test_02_goal_aggregation_updates(self):
        """Verify dynamic goal aggregation updates on transaction approval."""
        tx = self.env['ecosphere.carbon.transaction'].create({
            'name': 'Logistics fuel refill',
            'date': '2026-07-15',
            'activity_type': 'electricity',
            'quantity': 10000.0, # 10000 * 0.0008 = 8.0 tCO2e
            'emission_factor_id': self.factor_electricity.id,
            'department_id': self.dept_operations.id,
            'state': 'draft'
        })

        # Goal shouldn't aggregate draft transactions
        self.assertEqual(self.goal_operations.current_co2_eq, 0.0, "Draft transaction should not be aggregated")

        # Approve transaction
        tx.action_submit()
        tx.action_approve()

        # Goal must now count it
        self.assertEqual(self.goal_operations.current_co2_eq, 8.0, "Approved transaction should update the goal value")

    def test_03_purchase_invoice_carbon_creation(self):
        """Verify that validating a utility purchase invoice automatically creates a Carbon Transaction."""
        invoice = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'is_utility_bill': True,
            'utility_kwh': 12000.0,
            'invoice_date': '2026-07-10',
        })
        invoice.action_post()
        tx = self.env['ecosphere.carbon.transaction'].search([
            ('activity_type', '=', 'electricity'),
            ('quantity', '=', 12000.0)
        ], limit=1)
        self.assertTrue(tx, "Validation of utility purchase bill failed to automatically register carbon transaction ledger record")
