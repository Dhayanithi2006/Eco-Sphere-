# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class EcosphereChallenge(models.Model):
    _name = 'ecosphere.challenge'
    _description = 'Sustainability Engagement Challenges'
    _order = 'end_date desc, id desc'

    name = fields.Char(string='Challenge Title', required=True)
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date', required=True)
    
    target_points = fields.Integer(
        string='Points Target',
        required=True,
        default=50,
        help="The amount of ESG points an employee must accumulate during the campaign to earn the badge."
    )

    reward_badge_id = fields.Many2one(
        'ecosphere.badge',
        string='Reward Badge',
        required=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active Campaign'),
        ('completed', 'Completed')
    ], string='Status', required=True, default='draft', copy=False)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_complete(self):
        """
        Closes challenge and distributes badges to employees who completed targets.
        """
        for rec in self:
            if rec.state != 'active':
                raise UserError("Only active challenges can be completed.")
            
            # Find point histories in timeframe to see who met targets
            histories = self.env['ecosphere.employee.point.history'].search([
                ('date', '>=', rec.start_date),
                ('date', '<=', rec.end_date),
                ('points_delta', '>', 0)
            ])
            
            # Sum points per employee
            user_points = {}
            for history in histories:
                user_points[history.employee_id.id] = user_points.get(history.employee_id.id, 0) + history.points_delta
            
            # Award badge to all users who hit the threshold
            for user_id, points in user_points.items():
                if points >= rec.target_points:
                    user = self.env['res.users'].browse(user_id)
                    if rec.reward_badge_id not in user.earned_badge_ids:
                        user.write({
                            'earned_badge_ids': [(4, rec.reward_badge_id.id)]
                        })
            
            rec.write({'state': 'completed'})
