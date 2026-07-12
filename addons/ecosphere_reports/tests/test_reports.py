# -*- coding: utf-8 -*-
import base64
from odoo.tests.common import TransactionCase  # type: ignore

class TestReports(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestReports, cls).setUpClass()

        # Groups
        cls.group_employee = cls.env.ref('ecosphere_base.group_ecosphere_employee')

        # Test user
        cls.user_employee = cls.env['res.users'].create({
            'name': 'Report User',
            'login': 'test_report_login',
            'email': 'rep@test.local',
            'groups_id': [(6, 0, [cls.group_employee.id])]
        })

        # Department
        cls.dept_ops = cls.env['hr.department'].create({'name': 'Operations'})

    def test_01_export_wizard_execution(self):
        """Test wizard CSV creation logic."""
        wizard = self.env['ecosphere.report.export.wizard'].with_user(self.user_employee).create({
            'report_type': 'carbon',
            'department_id': self.dept_ops.id,
            'date_from': '2026-07-01',
            'date_to': '2026-07-31'
        })

        action = wizard.action_export_csv()
        
        # Verify result
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertTrue(wizard.export_file, "Export file binary was not generated")
        self.assertTrue(wizard.export_filename.endswith('.csv'), "Incorrect file name extension")

        # Decode CSV to verify format
        csv_data = base64.b64decode(wizard.export_file).decode('utf-8')
        lines = csv_data.split('\r\n')
        self.assertTrue(len(lines) >= 1, "CSV data is empty")
        self.assertIn('Date', lines[0], "Header row is incorrect")
