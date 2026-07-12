# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereEnvironmentalGoal(models.Model):
    _name = 'ecosphere.environmental.goal'
    _description = 'Departmental Carbon Target Goals'
    _order = 'end_date desc, id desc'

    name = fields.Char(string='Goal Description', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    
    target_co2_eq = fields.Float(
        string='Target CO2 Cap (tCO2e)',
        required=True,
        help="Target maximum carbon emissions allowance (in tCO2e) during this timeframe."
    )
    
    current_co2_eq = fields.Float(
        string='Current Cumulative Emissions',
        default=0.0,
        readonly=True,
        help="Aggregated carbon footprints from approved and published transactions during this period."
    )

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active Goal'),
        ('achieved', 'Goal Achieved'),
        ('missed', 'Goal Exceeded/Missed')
    ], string='Status', required=True, default='draft', copy=False)

    progress_bar = fields.Float(string='Goal Progress (%)', compute='_compute_progress_bar')

    @api.depends('target_co2_eq', 'current_co2_eq')
    def _compute_progress_bar(self):
        for goal in self:
            if goal.target_co2_eq > 0:
                goal.progress_bar = min((goal.current_co2_eq / goal.target_co2_eq) * 100.0, 100.0)
            else:
                goal.progress_bar = 0.0

    def action_activate(self):
        self.write({'state': 'active'})

    def action_evaluate(self):
        # Force evaluation based on end date comparison
        today = fields.Date.today()
        for goal in self:
            if goal.current_co2_eq <= goal.target_co2_eq:
                goal.write({'state': 'achieved'})
            else:
                goal.write({'state': 'missed'})
