# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereEmissionFactor(models.Model):
    _name = 'ecosphere.emission.factor'
    _description = 'Versioned ESG Emission Factors'
    _order = 'version desc, name asc'

    name = fields.Char(string='Name', required=True, index=True)
    version = fields.Char(string='Version', required=True, default='1.0', index=True)
    valid_from = fields.Date(string='Valid From', required=True, default=fields.Date.today)
    valid_to = fields.Date(string='Valid To', required=True)
    factor = fields.Float(string='Factor Value (tCO2e/Unit)', required=True, digits=(12, 6), default=0.0)
    
    unit_from = fields.Selection([
        ('kwh', 'kWh (Electricity)'),
        ('liters', 'Liters (Liquid Fuel)'),
        ('kg', 'Kilograms (Solid Fuel/Waste)'),
        ('km', 'Kilometers (Logistics/Travel)'),
    ], string='Input Unit Type', required=True, default='kwh')

    source = fields.Char(string='Calculation Source', help="e.g. CEA, IPCC, Defra")
    country = fields.Char(string='Applicable Country/Region', default='Global')
    reference = fields.Text(string='Reference Notes/URLs')

    @api.depends('name', 'version')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} (v{rec.version})"
