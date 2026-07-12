# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class EcosphereReward(models.Model):
    _name = 'ecosphere.reward'
    _description = 'ESG Points Redemption Catalog'
    _order = 'point_cost asc'

    name = fields.Char(string='Reward Item', required=True, index=True)
    point_cost = fields.Integer(string='Point Cost', required=True, default=100)
    stock = fields.Integer(string='Stock Count', required=True, default=10)
    description = fields.Text(string='Item Description')
    image = fields.Binary(string='Item Image', attachment=True)

    def action_redeem(self):
        """
        Deducts points from the current user and decrements stock count.
        """
        for rec in self:
            if rec.stock <= 0:
                raise UserError(f"Sorry, '{rec.name}' is currently out of stock.")
            
            user = self.env.user
            if user.esg_points < rec.point_cost:
                raise UserError(
                    f"Insufficient ESG Points! "
                    f"'{rec.name}' costs {rec.point_cost} points, but you only have {user.esg_points}."
                )

            # Deduct points
            user.write({'esg_points': user.esg_points - rec.point_cost})
            
            # Decrement stock
            rec.write({'stock': rec.stock - 1})

            # Create points history record
            self.env['ecosphere.employee.point.history'].create({
                'employee_id': user.id,
                'points_delta': -rec.point_cost,
                'reason': f"Redeemed item: {rec.name}",
                'date': fields.Date.today()
            })
