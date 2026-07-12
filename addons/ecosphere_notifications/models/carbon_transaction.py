# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereCarbonTransaction(models.Model):
    _inherit = 'ecosphere.carbon.transaction'

    def action_approve(self):
        """
        Extend approval workflow to verify carbon limits and trigger alerts if breached.
        """
        super(EcosphereCarbonTransaction, self).action_approve()

        for rec in self:
            if not rec.department_id:
                continue

            # Query active goal for this department
            goals = self.env['ecosphere.environmental.goal'].search([
                ('department_id', '=', rec.department_id.id),
                ('state', '=', 'active')
            ])

            for goal in goals:
                if goal.current_co2_eq > goal.target_co2_eq:
                    # Target breached! Log alert
                    manager = rec.department_id.sustainability_manager_id
                    recipient = manager if manager else self.env.user

                    title = f"Carbon Target Breached: {rec.department_id.name}"
                    message = (
                        f"Department '{rec.department_id.name}' has exceeded its carbon target limit. "
                        f"Cumulative CO2: {goal.current_co2_eq} tCO2e, Target Cap: {goal.target_co2_eq} tCO2e."
                    )

                    # Trigger alert register
                    self.env['ecosphere.notification'].send_alert(
                        recipient_id=recipient.id,
                        title=title,
                        message=message,
                        alert_type='warning'
                    )

                    # Trigger Odoo Mail template
                    template = self.env.ref('ecosphere_notifications.email_template_carbon_breach', raise_if_not_found=False)
                    if template:
                        # Contextual override to force correct email
                        template.with_context(recipient_email=recipient.email).send_mail(rec.id, force_send=True)
