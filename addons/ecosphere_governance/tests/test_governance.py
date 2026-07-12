# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase  # type: ignore
from odoo.exceptions import AccessError  # type: ignore

class TestGovernance(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestGovernance, cls).setUpClass()
        # Safe constructor setup
        cls.group_employee = cls.env.ref('ecosphere_base.group_ecosphere_employee')
        cls.group_manager = cls.env.ref('ecosphere_base.group_ecosphere_manager')
        cls.group_compliance = cls.env.ref('ecosphere_base.group_ecosphere_compliance')

        # Test users
        cls.user_employee = cls.env['res.users'].create({
            'name': 'Gov Employee',
            'login': 'test_gov_emp_login',
            'email': 'emp_gov@test.local',
            'groups_id': [(6, 0, [cls.group_employee.id])]
        })

        cls.user_compliance = cls.env['res.users'].create({
            'name': 'Gov Compliance Officer',
            'login': 'test_gov_comp_login',
            'email': 'comp_gov@test.local',
            'groups_id': [(6, 0, [cls.group_compliance.id])]
        })

        # Base departments
        cls.dept_ops = cls.env.ref('ecosphere_base.dept_operations', raise_if_not_found=False)
        if not cls.dept_ops:
            cls.dept_ops = cls.env['hr.department'].create({'name': 'Operations'})

    def test_01_risk_calculation(self):
        """Verify dynamic likelihood/impact matrix calculation."""
        risk = self.env['ecosphere.risk'].create({
            'title': 'Chemical Leak Risk',
            'category': 'environmental',
            'likelihood': '4', # Likely
            'impact': '3',     # Moderate
            'owner_id': self.user_compliance.id
        })
        self.assertEqual(risk.score, 12, "Risk Score should be 4 x 3 = 12")
        self.assertEqual(risk.risk_level, 'medium', "Score 12 should map to medium risk")

        # Increase impact
        risk.write({'impact': '5'}) # Critical (4 * 5 = 20)
        self.assertEqual(risk.score, 20, "Risk Score should be 20")
        self.assertEqual(risk.risk_level, 'high', "Score 20 should map to high risk")

    def test_02_policy_publication_propagation(self):
        """Verify policy publication automatically generates sign-off requirements."""
        policy = self.env['ecosphere.policy'].create({
            'name': 'Zero Single Use Plastic Policy',
            'version': '1.0',
            'state': 'draft'
        })

        # Draft policy should not have sign-offs
        acks = self.env['ecosphere.policy.acknowledgment'].search([('policy_id', '=', policy.id)])
        self.assertFalse(acks, "Draft policy should not have acknowledgements")

        # Link our test user to the department to guarantee targeting
        employee = self.env['hr.employee'].create({
            'name': 'Test Employee Profile',
            'user_id': self.user_employee.id,
            'department_id': self.dept_ops.id
        })

        policy.write({'target_department_ids': [(4, self.dept_ops.id)]})

        # Submit and Publish
        policy.action_submit()
        policy.action_publish()

        # Check acks
        acks = self.env['ecosphere.policy.acknowledgment'].search([('policy_id', '=', policy.id)])
        self.assertTrue(acks, "Published policy must generate acknowledgements")
        self.assertEqual(acks[0].employee_id, self.user_employee, "Sign-off not mapped to targeted employee user")
        self.assertEqual(acks[0].state, 'pending')

        # Employee signs off
        acks[0].with_user(self.user_employee).action_acknowledge()
        self.assertEqual(acks[0].state, 'acknowledged')

    def test_03_restrict_employee_governance_access(self):
        """Ensure standard employees cannot view compliance audits or risks."""
        # Create an audit
        audit = self.env['ecosphere.audit'].create({
            'name': 'Q2 Plant Audit',
            'audit_type': 'internal',
            'auditor_id': self.user_compliance.id,
            'compliance_status': 'compliant'
        })

        # Read as employee user (should raise AccessError)
        with self.assertRaises(AccessError):
            self.env['ecosphere.audit'].with_user(self.user_employee).search([])
            
        with self.assertRaises(AccessError):
            self.env['ecosphere.risk'].with_user(self.user_employee).search([])
