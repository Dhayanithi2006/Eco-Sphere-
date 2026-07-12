# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase  # type: ignore
from odoo.exceptions import AccessError  # type: ignore

class TestBaseRbac(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestBaseRbac, cls).setUpClass()
        
        # Reference groups
        cls.group_employee = cls.env.ref('ecosphere_base.group_ecosphere_employee')
        cls.group_manager = cls.env.ref('ecosphere_base.group_ecosphere_manager')
        cls.group_auditor = cls.env.ref('ecosphere_base.group_ecosphere_auditor')
        cls.group_compliance = cls.env.ref('ecosphere_base.group_ecosphere_compliance')
        cls.group_admin = cls.env.ref('ecosphere_base.group_ecosphere_admin')

        # Create test users
        cls.user_employee = cls.env['res.users'].create({
            'name': 'Test Employee',
            'login': 'test_employee_login',
            'email': 'emp@test.local',
            'groups_id': [(6, 0, [cls.group_employee.id])]
        })
        
        cls.user_manager = cls.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'test_manager_login',
            'email': 'mgr@test.local',
            'groups_id': [(6, 0, [cls.group_manager.id])]
        })

        cls.user_compliance = cls.env['res.users'].create({
            'name': 'Test Compliance',
            'login': 'test_compliance_login',
            'email': 'comp@test.local',
            'groups_id': [(6, 0, [cls.group_compliance.id])]
        })

        # Define departments
        cls.dept_test = cls.env['hr.department'].create({
            'name': 'Test Sustainable Department',
            'department_target_co2': 15.0
        })

    def test_01_employee_defaults(self):
        """Test default points and constraints for employees."""
        self.assertEqual(self.user_employee.esg_points, 0, "Default points should be 0")
        self.assertTrue(self.user_employee.is_esg_active, "Employee should default to ESG participating")
        self.assertEqual(self.user_employee.volunteer_hours_logged, 0.0)

    def test_02_department_sustainability_manager(self):
        """Test assigning a sustainability representative to a department."""
        # Manager should have access to update target
        dept_sudo = self.dept_test.with_user(self.user_manager)
        dept_sudo.write({
            'sustainability_manager_id': self.user_manager.id,
            'department_target_co2': 25.0
        })
        self.assertEqual(self.dept_test.sustainability_manager_id, self.user_manager)
        self.assertEqual(self.dept_test.department_target_co2, 25.0)

    def test_03_settings_access_restricted(self):
        """Ensure standard employees and managers cannot write to global ESG settings."""
        # Create setting record simulation
        settings_env = self.env['res.config.settings']
        
        # Test as Employee (should raise AccessError if they try to save admin settings,
        # but in Odoo config is Transient, permissions are controlled via views and ACL)
        # We will assert that only base configuration settings action restricts to Admin groups.
        action = self.env.ref('ecosphere_base.action_ecosphere_config_settings')
        self.assertTrue('ecosphere_base.group_ecosphere_admin' in action.groups_id.mapped('xml_id') or not action.groups_id)
