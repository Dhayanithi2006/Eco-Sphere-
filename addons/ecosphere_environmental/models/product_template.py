# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    carbon_footprint = fields.Float(
        string='Product Carbon Footprint (kgCO2e)',
        default=0.0,
        help="Lifecycle carbon output generated during manufacturing or logistics for one unit."
    )

    sustainability_grade = fields.Selection([
        ('a', 'Class A (Eco-Friendly / Net-Zero)'),
        ('b', 'Class B (Low Impact)'),
        ('c', 'Class C (Moderate Impact)'),
        ('d', 'Class D (High Impact)'),
        ('e', 'Class E (Critical Impact)'),
    ], string='Sustainability Grade', default='c')

    is_sustainable = fields.Boolean(
        string='Is Certified Sustainable',
        default=False,
        help="Indicates whether this product holds eco-labels or sustainability certifications."
    )
