# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    is_utility_bill = fields.Boolean(string="Is Utility Bill?", default=False)
    utility_kwh = fields.Float(string="Utility Quantity (kWh)", default=0.0)

    def action_post(self):
        res = super(AccountMove, self).action_post()
        auto_calc = self.env['ir.config_parameter'].sudo().get_param('ecosphere.enable_auto_emission', default='True') == 'True'
        if not auto_calc:
            return res
        for move in self:
            if move.move_type == 'in_invoice' and move.is_utility_bill and move.utility_kwh > 0:
                factor = self.env['ecosphere.emission.factor'].search([
                    ('activity_type', '=', 'electricity'),
                    ('valid_from', '<=', move.invoice_date or fields.Date.today()),
                    ('valid_to', '>=', move.invoice_date or fields.Date.today())
                ], limit=1)
                if factor:
                    self.env['ecosphere.carbon.transaction'].create({
                        'name': f"Electricity Utility Invoice: {move.name or move.ref or 'Inv'}",
                        'date': move.invoice_date or fields.Date.today(),
                        'activity_type': 'electricity',
                        'quantity': move.utility_kwh,
                        'emission_factor_id': factor.id,
                        'state': 'approved'
                    })
        return res

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    machine_kwh = fields.Float(string="Machine Power Usage (kWh)", default=0.0)

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        auto_calc = self.env['ir.config_parameter'].sudo().get_param('ecosphere.enable_auto_emission', default='True') == 'True'
        if not auto_calc:
            return res
        for production in self:
            if production.machine_kwh > 0:
                factor = self.env['ecosphere.emission.factor'].search([
                    ('activity_type', '=', 'electricity'),
                    ('valid_from', '<=', fields.Date.today()),
                    ('valid_to', '>=', fields.Date.today())
                ], limit=1)
                if factor:
                    self.env['ecosphere.carbon.transaction'].create({
                        'name': f"Manufacturing Order: {production.name}",
                        'date': fields.Date.today(),
                        'activity_type': 'electricity',
                        'quantity': production.machine_kwh,
                        'emission_factor_id': factor.id,
                        'state': 'approved'
                    })
        return res

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    is_aviation_travel = fields.Boolean(string="Is Aviation Travel?", default=False)
    travel_distance_km = fields.Float(string="Travel Distance (km)", default=0.0)

    def action_submit_expenses(self):
        res = super(HrExpense, self).action_submit_expenses()
        auto_calc = self.env['ir.config_parameter'].sudo().get_param('ecosphere.enable_auto_emission', default='True') == 'True'
        if not auto_calc:
            return res
        for expense in self:
            if expense.is_aviation_travel and expense.travel_distance_km > 0:
                factor = self.env['ecosphere.emission.factor'].search([
                    ('activity_type', '=', 'travel'),
                    ('valid_from', '<=', fields.Date.today()),
                    ('valid_to', '>=', fields.Date.today())
                ], limit=1)
                if factor:
                    self.env['ecosphere.carbon.transaction'].create({
                        'name': f"Travel Expense Claim: {expense.name}",
                        'date': fields.Date.today(),
                        'activity_type': 'travel',
                        'quantity': expense.travel_distance_km,
                        'emission_factor_id': factor.id,
                        'state': 'approved'
                    })
        return res

class FleetVehicleLogFuel(models.Model):
    _inherit = 'fleet.vehicle.log.fuel'

    liters_diesel = fields.Float(string="Diesel Consumed (Liters)", default=0.0)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(FleetVehicleLogFuel, self).create(vals_list)
        auto_calc = self.env['ir.config_parameter'].sudo().get_param('ecosphere.enable_auto_emission', default='True') == 'True'
        if not auto_calc:
            return records
        for record in records:
            if record.liters_diesel > 0:
                factor = self.env['ecosphere.emission.factor'].search([
                    ('activity_type', '=', 'stationary_combustion'),
                    ('valid_from', '<=', fields.Date.today()),
                    ('valid_to', '>=', fields.Date.today())
                ], limit=1)
                if factor:
                    self.env['ecosphere.carbon.transaction'].create({
                        'name': f"Fleet Fuel Refill: {record.vehicle_id.name if record.vehicle_id else 'Vehicle'}",
                        'date': fields.Date.today(),
                        'activity_type': 'stationary_combustion',
                        'quantity': record.liters_diesel,
                        'emission_factor_id': factor.id,
                        'state': 'approved'
                    })
        return records
