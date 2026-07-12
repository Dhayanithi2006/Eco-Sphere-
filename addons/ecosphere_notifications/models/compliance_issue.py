# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EcosphereComplianceIssue(models.Model):
    _inherit = 'ecosphere.compliance.issue'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Interceptors compliance issues creation to notify managers when priority is critical.
        """
        records = super(EcosphereComplianceIssue, self).create(vals_list)
        
        for rec in records:
            if rec.priority == 'critical':
                # Find Compliance group users
                compliance_group = self.env.ref('ecosphere_base.group_ecosphere_compliance', raise_if_not_found=False)
                officers = compliance_group.users if compliance_group else self.env['res.users']
                
                for officer in officers.filtered(lambda u: u.is_esg_active):
                    title = f"CRITICAL Compliance Issue: {rec.title}"
                    message = (
                        f"A critical compliance issue has been registered. "
                        f"Violated Policy: {rec.policy_id.name}. "
                        f"Discovered in Audit: {rec.source_audit_id.name}."
                    )

                    # Trigger alert register
                    self.env['ecosphere.notification'].send_alert(
                        recipient_id=officer.id,
                        title=title,
                        message=message,
                        alert_type='critical'
                    )

                    # Send template email
                    template = self.env.ref('ecosphere_notifications.email_template_compliance_breach', raise_if_not_found=False)
                    if template:
                        template.with_context(recipient_email=officer.email).send_mail(rec.id, force_send=True)
                        
        return records
