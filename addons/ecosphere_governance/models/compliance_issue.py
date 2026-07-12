# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereComplianceIssue(models.Model):
    _name = 'ecosphere.compliance.issue'
    _description = 'ESG Compliance Gaps & Breaches'
    _order = 'priority desc, id desc'

    title = fields.Char(string='Issue Title', required=True, index=True)
    
    policy_id = fields.Many2one(
        'ecosphere.policy',
        string='Violated ESG Policy',
        required=True
    )

    source_audit_id = fields.Many2one(
        'ecosphere.audit',
        string='Discovered in Audit',
        required=True
    )

    priority = fields.Selection([
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('critical', 'Critical / Legal risk')
    ], string='Priority Level', required=True, default='medium')

    status = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Investigation'),
        ('resolved', 'Resolved & Mitigated')
    ], string='Status', required=True, default='draft')

    description = fields.Text(string='Incident Details & Corrective Actions')
    
    owner_id = fields.Many2one('res.users', string='Owner', required=True)
    due_date = fields.Date(string='Due Date', required=True, default=fields.Date.today)
    is_overdue = fields.Boolean(string='Is Overdue', compute='_compute_is_overdue', store=True)

    @api.depends('due_date', 'status')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_overdue = rec.status != 'resolved' and rec.due_date and rec.due_date < today

    def action_investigate(self):
        self.write({'status': 'review'})

    def action_resolve(self):
        self.write({'status': 'resolved'})

    @api.model_create_multi
    def create(self, vals_list):
        records = super(EcosphereComplianceIssue, self).create(vals_list)
        for record in records:
            notify = self.env['ir.config_parameter'].sudo().get_param('ecosphere.notify_compliance_issue', default='True') == 'True'
            if notify and record.owner_id:
                self.env['ecosphere.notification'].sudo().send_alert(
                    record.owner_id.id,
                    f"Compliance Issue Assigned: {record.title}",
                    f"You have been assigned as the owner of the compliance issue '{record.title}' due on {record.due_date}.",
                    'critical' if record.priority in ['high', 'critical'] else 'warning'
                )
        return records
