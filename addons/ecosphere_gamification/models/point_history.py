# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereEmployeePointHistory(models.Model):
    _name = 'ecosphere.employee.point.history'
    _description = 'Employee Point Allocation Ledger'
    _order = 'date desc, id desc'

    employee_id = fields.Many2one(
        'res.users',
        string='Employee User',
        required=True,
        index=True
    )
    
    points_delta = fields.Integer(string='Points Credit/Debit', required=True)
    reason = fields.Char(string='Transaction Reason', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
