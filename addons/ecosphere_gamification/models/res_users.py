# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    earned_badge_ids = fields.Many2many(
        'ecosphere.badge',
        'res_users_ecosphere_badge_rel',
        'user_id',
        'badge_id',
        string='Sustainability Badges',
        help="Earned sustainability badges cabinet."
    )

    point_history_ids = fields.One2many(
        'ecosphere.employee.point.history',
        'employee_id',
        string='ESG Point Transactions'
    )

    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if 'esg_points' in vals:
            self.check_and_award_badges()
        return res

    def check_and_award_badges(self):
        """
        Calculates user point balance and completed challenges to auto-award badges.
        """
        auto_award = self.env['ir.config_parameter'].sudo().get_param('ecosphere.enable_badge_auto_award', default='True') == 'True'
        if not auto_award:
            return

        for user in self:
            badges = self.env['ecosphere.badge'].search([])
            for badge in badges:
                if badge in user.earned_badge_ids:
                    continue
                
                # Check points threshold
                if badge.unlock_rule_type == 'xp' and user.esg_points >= badge.unlock_rule_value:
                    user.write({'earned_badge_ids': [(4, badge.id)]})
                    
                    # Send alert if notifications are enabled
                    notify = self.env['ir.config_parameter'].sudo().get_param('ecosphere.notify_badge_unlock', default='True') == 'True'
                    if notify:
                        self.env['ecosphere.notification'].sudo().send_alert(
                            user.id,
                            f"Badge Unlocked: {badge.name}",
                            f"Congratulations! You have unlocked the '{badge.name}' badge by satisfying the unlock threshold requirement ({badge.unlock_rule_value} points).",
                            'info'
                        )
