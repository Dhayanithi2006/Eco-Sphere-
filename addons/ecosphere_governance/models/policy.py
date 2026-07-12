# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcospherePolicy(models.Model):
    _name = 'ecosphere.policy'
    _description = 'Corporate ESG Compliance Policies'
    _order = 'version desc, name asc'

    name = fields.Char(string='Policy Name', required=True, index=True)
    file_attachment = fields.Binary(string='Policy Document (PDF)', attachment=True)
    version = fields.Char(string='Version', required=True, default='1.0')
    active = fields.Boolean(string='Active', default=True)
    
    target_department_ids = fields.Many2many(
        'hr.department',
        string='Target Departments',
        help="Specify which departments need to acknowledge this policy. Leave empty for all employees."
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string='Status', required=True, default='draft', copy=False)

    def action_submit(self):
        self.write({'state': 'review'})

    def action_publish(self):
        for rec in self:
            rec.write({'state': 'published'})
            rec._generate_acknowledgments()

    def action_archive(self):
        self.write({'state': 'archived'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def _generate_acknowledgments(self):
        """
        Generates pending acknowledgment records for all applicable employees.
        """
        for rec in self:
            # Determine target users based on departments
            domain = [('is_esg_active', '=', True)]
            if rec.target_department_ids:
                # Find users where user.employee_id.department_id is in target departments
                domain.append(('employee_id.department_id', 'in', rec.target_department_ids.ids))
            
            target_users = self.env['res.users'].search(domain)
            
            for user in target_users:
                # Avoid duplicate acknowledgments
                existing = self.env['ecosphere.policy.acknowledgment'].search([
                    ('policy_id', '=', rec.id),
                    ('employee_id', '=', user.id)
                ])
                if not existing:
                    self.env['ecosphere.policy.acknowledgment'].create({
                        'policy_id': rec.id,
                        'employee_id': user.id,
                        'state': 'pending'
                    })
