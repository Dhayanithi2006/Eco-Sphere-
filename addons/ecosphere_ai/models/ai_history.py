# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereAiHistory(models.Model):
    _name = 'ecosphere.ai.history'
    _description = 'AI Advisor History Logs'
    _order = 'date desc, id desc'

    name = fields.Char(string='Consultation Title', required=True)
    prompt = fields.Text(string='Prompt Sent', required=True)
    response = fields.Text(string='AI Advice', required=True)
    confidence_score = fields.Float(string='Confidence Score', default=0.95, group_operator="avg")

    user_rating = fields.Selection([
        ('none', 'No Rating'),
        ('like', 'Thumbs Up 👍'),
        ('dislike', 'Thumbs Down 👎')
    ], string='User Feedback', required=True, default='none')

    date = fields.Datetime(string='Date Consulted', default=fields.Datetime.now, readonly=True)

    def action_like(self):
        self.write({'user_rating': 'like'})

    def action_dislike(self):
        self.write({'user_rating': 'dislike'})
