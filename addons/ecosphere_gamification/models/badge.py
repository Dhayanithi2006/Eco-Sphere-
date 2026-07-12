# -*- coding: utf-8 -*-
from odoo import models, fields

class EcosphereBadge(models.Model):
    _name = 'ecosphere.badge'
    _description = 'Sustainability Achievement Badges'
    _order = 'name asc'

    name = fields.Char(string='Badge Name', required=True, index=True)
    image = fields.Binary(string='Badge Icon', attachment=True)
    description = fields.Text(string='Description / Requirements')
    
    unlock_rule_type = fields.Selection([
        ('xp', 'ESG Points Threshold'),
        ('challenges', 'Completed Challenges Count')
    ], string='Unlock Rule Type', default='xp')
    unlock_rule_value = fields.Integer(string='Unlock Rule Value', default=100)
