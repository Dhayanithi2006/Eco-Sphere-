# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EcosphereDiversityDashboard(models.Model):
    _name = 'ecosphere.diversity.dashboard'
    _description = 'Departmental Diversity KPIs'
    _rec_name = 'department_id'

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
        ondelete='cascade',
        index=True
    )

    female_ratio = fields.Float(string='Female Ratio (%)', default=50.0)
    male_ratio = fields.Float(string='Male Ratio (%)', default=50.0)
    other_ratio = fields.Float(string='Other Ratio (%)', default=0.0)
    
    avg_age = fields.Float(string='Average Employee Age', default=35.0)
    ethnic_diversity_index = fields.Float(
        string='Ethnic Diversity Index',
        default=1.0,
        help="Diversity index coefficient (e.g. 1.0 - 5.0 scale)."
    )

    _sql_constraints = [
        ('uniq_department', 'unique(department_id)', 'A diversity scorecard already exists for this department!')
    ]

    @api.constrains('female_ratio', 'male_ratio', 'other_ratio')
    def _check_ratios_total(self):
        for rec in self:
            total = rec.female_ratio + rec.male_ratio + rec.other_ratio
            # Allow minor floating point rounding deviation
            if not (99.0 <= total <= 101.0):
                raise ValidationError("The sum of employee ratios (Female + Male + Other) must equal 100%.")
