# -*- coding: utf-8 -*-
import csv
import io
import base64
from odoo import models, fields, api

class EcosphereReportExportWizard(models.TransientModel):
    _name = 'ecosphere.report.export.wizard'
    _description = 'ESG Raw Data Export Wizard'

    report_type = fields.Selection([
        ('carbon', 'Carbon Transactions Ledger'),
        ('volunteer', 'CSR Volunteer Logs')
    ], string='Report Type', required=True, default='carbon')

    department_id = fields.Many2one('hr.department', string='Department Filter')
    date_from = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', required=True, default=fields.Date.context_today)

    export_file = fields.Binary(string='Download File', readonly=True)
    export_filename = fields.Char(string='File Name', readonly=True)

    def action_export_csv(self):
        """
        Processes query filters and returns a downloadable CSV attachment action.
        """
        self.ensure_one()
        
        # Buffer setup
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if self.report_type == 'carbon':
            # Write Header
            writer.writerow(['Date', 'Reference', 'Activity Type', 'Quantity', 'Unit', 'CO2 Equivalent (tCO2e)', 'Department'])
            
            # Query transactions
            domain = [
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
                ('state', 'in', ['approved', 'published'])
            ]
            if self.department_id:
                domain.append(('department_id', '=', self.department_id.id))
            
            records = self.env['ecosphere.carbon.transaction'].search(domain)
            for rec in records:
                writer.writerow([
                    rec.date,
                    rec.name,
                    rec.activity_type,
                    rec.quantity,
                    rec.unit or '',
                    rec.co2_eq,
                    rec.department_id.name or 'Unknown'
                ])
            
            filename = f"carbon_ledger_{fields.Date.today()}.csv"

        else:
            # Write Header
            writer.writerow(['Date Logged', 'Employee', 'CSR Program', 'Volunteer Hours', 'Status'])
            
            # Query volunteer logs
            domain = [
                ('create_date', '>=', fields.Datetime.to_string(self.date_from)),
                ('create_date', '<=', fields.Datetime.to_string(self.date_to)),
                ('state', '=', 'approved')
            ]
            
            records = self.env['ecosphere.csr.participation'].search(domain)
            for rec in records:
                # Optional filtering
                if self.department_id and rec.employee_id.employee_id.department_id != self.department_id:
                    continue
                writer.writerow([
                    rec.create_date.date(),
                    rec.employee_id.name,
                    rec.activity_id.name,
                    rec.hours_logged,
                    rec.state
                ])
            
            filename = f"volunteer_logs_{fields.Date.today()}.csv"

        # Encode and attach
        csv_data = output.getvalue()
        self.write({
            'export_file': base64.b64encode(csv_data.encode('utf-8')),
            'export_filename': filename
        })
        output.close()

        # Return action to download file
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model={self._name}&id={self.id}&field=export_file&filename={self.export_filename}&download=true',
            'target': 'self',
        }
