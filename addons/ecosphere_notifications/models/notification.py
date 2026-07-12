# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereNotification(models.Model):
    _name = 'ecosphere.notification'
    _description = 'Sustainability Alerts Log'
    _order = 'date desc, id desc'

    name = fields.Char(string='Subject', required=True, index=True)
    recipient_id = fields.Many2one('res.users', string='Recipient', required=True, index=True)
    message = fields.Text(string='Message Details', required=True)
    
    notification_type = fields.Selection([
        ('info', 'Information'),
        ('warning', 'Goal Warning'),
        ('critical', 'Critical Breach')
    ], string='Alert Level', required=True, default='info')

    is_read = fields.Boolean(string='Read', default=False)
    date = fields.Datetime(string='Triggered Date', default=fields.Datetime.now, readonly=True)

    def action_mark_read(self):
        self.write({'is_read': True})

    @api.model
    def send_alert(self, recipient_id, title, message, alert_type='info'):
        """
        Static helper to create alert registers.
        """
        notification = self.create({
            'name': title,
            'recipient_id': recipient_id,
            'message': message,
            'notification_type': alert_type
        })
        return notification
