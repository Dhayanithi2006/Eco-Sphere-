# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class EcosphereCsrParticipation(models.Model):
    _name = 'ecosphere.csr.participation'
    _description = 'CSR Volunteer Log Participation'
    _order = 'create_date desc'

    activity_id = fields.Many2one(
        'ecosphere.csr.activity',
        string='CSR Activity Program',
        required=True,
        domain="[('state', '=', 'active')]"
    )

    employee_id = fields.Many2one(
        'res.users',
        string='Employee',
        required=True,
        default=lambda self: self.env.user
    )

    hours_logged = fields.Float(string='Volunteer Hours', required=True, default=0.0)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', required=True, default='draft', copy=False)

    notes = fields.Text(string='Activity Logs / Summary')
    proof_attachment = fields.Binary(string='Attached Proof Document', attachment=True)

    @api.constrains('hours_logged')
    def _check_hours_logged(self):
        for rec in self:
            if rec.hours_logged <= 0:
                raise UserError("Logged volunteer hours must be positive.")

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        # Admin / Manager only controls (permissions handled via ACL)
        evidence_required = self.env['ir.config_parameter'].sudo().get_param('ecosphere.enable_evidence_requirement', default='True') == 'True'
        for rec in self:
            if rec.state != 'submitted':
                raise UserError("Only submitted logs can be approved.")
            
            if evidence_required and not rec.proof_attachment:
                raise UserError("Cannot approve CSR volunteer participation log: An attached proof document is required under current settings.")
            
            # Award points: 10 points per volunteer hour
            points_to_award = int(rec.hours_logged * 10)
            rec.employee_id.sudo().write({
                'esg_points': rec.employee_id.esg_points + points_to_award
            })
            rec.write({'state': 'approved'})
            # Update the related activity hours
            rec.activity_id._compute_volunteer_hours_actual()

    def action_reject(self):
        for rec in self:
            if rec.state != 'submitted':
                raise UserError("Only submitted logs can be rejected.")
            rec.write({'state': 'rejected'})

    def action_draft(self):
        for rec in self:
            if rec.state == 'approved':
                # Deduct points if already awarded
                points_to_deduct = int(rec.hours_logged * 10)
                rec.employee_id.sudo().write({
                    'esg_points': max(rec.employee_id.esg_points - points_to_deduct, 0)
                })
            rec.write({'state': 'draft'})
            rec.activity_id._compute_volunteer_hours_actual()
            
    @api.model_create_multi
    def create(self, vals_list):
        records = super(EcosphereCsrParticipation, self).create(vals_list)
        return records

    def write(self, vals):
        res = super(EcosphereCsrParticipation, self).write(vals)
        if 'state' in vals or 'hours_logged' in vals:
            for rec in self:
                rec.activity_id._compute_volunteer_hours_actual()
        return res
