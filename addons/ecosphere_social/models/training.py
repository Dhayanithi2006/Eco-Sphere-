# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereTraining(models.Model):
    _name = 'ecosphere.training'
    _description = 'Sustainability and Inclusion Training Modules'
    _order = 'date desc, id desc'

    name = fields.Char(string='Course Title', required=True, index=True)
    
    type = fields.Selection([
        ('sustainability', 'Sustainability & Green Operations'),
        ('diversity', 'Diversity, Equity & Inclusion (DEI)'),
        ('health_safety', 'Occupational Health & Safety'),
    ], string='Course Type', required=True, default='sustainability')

    date = fields.Date(string='Training Date', required=True, default=fields.Date.today)
    attendee_ids = fields.Many2many('res.users', string='Attendees')
    completion_rate = fields.Float(string='Completion Rate (%)', default=100.0)
    notes = fields.Text(string='Course Syllabus / Objectives')
