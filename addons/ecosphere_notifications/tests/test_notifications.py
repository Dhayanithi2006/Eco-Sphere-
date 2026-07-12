# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase  # type: ignore
from odoo.exceptions import AccessError  # type: ignore

class TestNotifications(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestNotifications, cls).setUpClass()
        cls.company = cls.env.company

        # Groups
        cls.group_employee = cls.env.ref('ecosphere_base.group_ecosphere_employee')
        cls.group_compliance = cls.env.ref('ecosphere_base.group_ecosphere_compliance')

        # Test users
        cls.user_employee = cls.env['res.users'].create({
            'name': 'Notif Employee',
            'login': 'test_notif_emp',
            'email': 'emp_notif@test.local',
            'groups_id': [(6, 0, [cls.group_employee.id])]
        })

        cls.user_officer = cls.env['res.users'].create({
            'name': 'Notif Officer',
            'login': 'test_notif_off',
            'email': 'off_notif@test.local',
            'groups_id': [(6, 0, [cls.group_compliance.id])]
        })

        # Department
        cls.dept_ops = cls.env.ref('ecosphere_base.dept_operations', raise_if_not_found=False)
        if not cls.dept_ops:
            cls.dept_ops = cls.env['hr.department'].create({'name': 'Operations'})

        # Link Sustainability Manager
        cls.dept_ops.write({'sustainability_manager_id': cls.user_employee.id})

        # Environmental Target Limit
        cls.goal = cls.env['ecosphere.environmental.goal'].create({
            'name': 'Operations Target Limit',
            'company_id': cls.company.id,
            'department_id': cls.dept_ops.id,
            'target_co2_eq': 10.0,
            'current_co2_eq': 0.0,
            'state': 'active'
        })

        # Base elements for compliance tests
        cls.audit = cls.env['ecosphere.audit'].create({
            'name': 'Operations Check',
            'audit_type': 'internal',
            'auditor_id': cls.user_officer.id
        })
        cls.policy = cls.env['ecosphere.policy'].create({
            'name': 'Carbon Policy',
            'version': '1.0',
            'state': 'published'
        })

    def test_01_carbon_exceeded_notification(self):
        """Verify carbon limits breach triggers automatic warnings."""
        # Create factor
        factor = self.env['ecosphere.emission.factor'].create({
            'name': 'High Coal Factor',
            'co2_multiplier': 5.0
        })

        # Add transaction exceeding limits (quantity = 3 -> 3 * 5 = 15 tCO2e, exceeds target 10 tCO2e)
        tx = self.env['ecosphere.carbon.transaction'].create({
            'name': 'Heavy Combustion Run',
            'activity_type': 'stationary_combustion',
            'quantity': 3.0,
            'factor_id': factor.id,
            'department_id': self.dept_ops.id,
            'state': 'draft'
        })

        # Approve
        tx.action_approve()

        # Alert should have triggered for Sustainability Manager (user_employee)
        alerts = self.env['ecosphere.notification'].search([
            ('recipient_id', '=', self.user_employee.id),
            ('notification_type', '=', 'warning')
        ])
        self.assertTrue(alerts, "Carbon limit breach did not generate automated notifications")
        self.assertIn("Carbon Target Breached", alerts[0].name)

    def test_02_compliance_breach_alert(self):
        """Verify critical compliance issues generate notifications."""
        # Create critical issue
        self.env['ecosphere.compliance.issue'].create({
            'title': 'Critical Boiler Violation',
            'policy_id': self.policy.id,
            'source_audit_id': self.audit.id,
            'priority': 'critical',
            'status': 'draft'
        })

        # Alert should have triggered for the Compliance Officer (user_officer)
        alerts = self.env['ecosphere.notification'].search([
            ('recipient_id', '=', self.user_officer.id),
            ('notification_type', '=', 'critical')
        ])
        self.assertTrue(alerts, "Critical compliance breach did not trigger alerts")
        self.assertIn("CRITICAL Compliance", alerts[0].name)

    def test_03_restrict_employee_notifications(self):
        """Ensure standard employees can only view alerts sent directly to them."""
        # Alert to officer
        self.env['ecosphere.notification'].create({
            'name': 'Officer Alert',
            'recipient_id': self.user_officer.id,
            'message': 'Test message'
        })

        # Read as employee
        employee_alerts = self.env['ecosphere.notification'].with_user(self.user_employee).search([])
        officer_alerts = [a for a in employee_alerts if a.recipient_id == self.user_officer]
        self.assertFalse(officer_alerts, "Employee user should not be able to read officer alert logs")
