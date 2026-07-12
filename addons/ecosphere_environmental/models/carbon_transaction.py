# -*- coding: utf-8 -*-
from odoo import models, fields, api
from ..services.calculation_engine import calculate_co2, recalculate_department_goals

class EcosphereCarbonTransaction(models.Model):
    _name = 'ecosphere.carbon.transaction'
    _description = 'Environmental Carbon Transactions Ledger'
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference/Title', required=True, index=True)
    date = fields.Date(string='Transaction Date', required=True, default=fields.Date.today, index=True)
    
    activity_type = fields.Selection([
        ('stationary_combustion', 'Stationary Combustion (Scope 1 - e.g. Generators)'),
        ('mobile_combustion', 'Mobile Combustion (Scope 1 - e.g. Fleet vehicles)'),
        ('electricity', 'Purchased Electricity (Scope 2)'),
        ('travel', 'Business Travel & Commute (Scope 3)'),
        ('waste', 'Waste Disposal (Scope 3)'),
    ], string='Activity Type', required=True, default='electricity')

    quantity = fields.Float(string='Raw Quantity Used', required=True, default=0.0)
    
    unit = fields.Selection([
        ('kwh', 'kWh'),
        ('liters', 'Liters'),
        ('kg', 'kg'),
        ('km', 'km'),
    ], string='Measurement Unit', related='emission_factor_id.unit_from', readonly=True)

    emission_factor_id = fields.Many2one(
        'ecosphere.emission.factor',
        string='Emission Factor Reference',
        required=True,
        domain="[('valid_from', '<=', date), ('valid_to', '>=', date)]"
    )

    co2_eq = fields.Float(
        string='CO2 Equivalent (tCO2e)',
        compute='_compute_co2_eq',
        store=True,
        readonly=True,
        help="Calculated carbon footprint in metric tons of carbon dioxide equivalent (tCO2e)."
    )

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
        default=lambda self: self.env.user.employee_id.department_id or False
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('published', 'Published')
    ], string='Status', required=True, default='draft', copy=False, tracking=True)

    @api.depends('quantity', 'emission_factor_id')
    def _compute_co2_eq(self):
        for rec in self:
            factor_val = rec.emission_factor_id.factor if rec.emission_factor_id else 0.0
            rec.co2_eq = calculate_co2(rec.quantity, factor_val)

    # Workflow Actions
    def action_submit(self):
        self.write({'state': 'under_review'})

    def action_approve(self):
        self.write({'state': 'approved'})
        self._trigger_goal_recalculation()

    def action_publish(self):
        self.write({'state': 'published'})
        self._trigger_goal_recalculation()

    def action_draft(self):
        self.write({'state': 'draft'})
        self._trigger_goal_recalculation()

    def _trigger_goal_recalculation(self):
        for rec in self:
            if rec.department_id:
                recalculate_department_goals(self.env, rec.department_id.id, rec.date)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(EcosphereCarbonTransaction, self).create(vals_list)
        for record in records:
            if record.state in ['approved', 'published']:
                record._trigger_goal_recalculation()
        return records

    def write(self, vals):
        res = super(EcosphereCarbonTransaction, self).write(vals)
        if any(f in vals for f in ['quantity', 'emission_factor_id', 'department_id', 'date', 'state']):
            for record in self:
                record._trigger_goal_recalculation()
        return res
