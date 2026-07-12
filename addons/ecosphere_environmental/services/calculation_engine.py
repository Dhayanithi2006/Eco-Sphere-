# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)

def calculate_co2(quantity, factor):
    """
    Computes total CO2 equivalent (tons or kg).
    """
    if not quantity or not factor:
        return 0.0
    return quantity * factor

def recalculate_department_goals(env, department_id, target_date):
    """
    Aggregates all approved/published carbon transactions for a department
    within active goal timeframes, and updates environmental.goal records.
    """
    if not department_id:
        return

    # Find active environmental goals for this department containing the target_date
    goals = env['ecosphere.environmental.goal'].search([
        ('department_id', '=', department_id),
        ('start_date', '<=', target_date),
        ('end_date', '>=', target_date),
        ('state', 'in', ['draft', 'active'])
    ])

    for goal in goals:
        # Search all approved/published transactions in this department and timeframe
        transactions = env['ecosphere.carbon.transaction'].search([
            ('department_id', '=', department_id),
            ('date', '>=', goal.start_date),
            ('date', '<=', goal.end_date),
            ('state', 'in', ['approved', 'published'])
        ])

        total_co2 = sum(transactions.mapped('co2_eq'))
        goal.write({'current_co2_eq': total_co2})
        
        # Auto-update status if end date has passed or limit has been breached
        if goal.end_date < target_date:
            if total_co2 <= goal.target_co2_eq:
                goal.write({'state': 'achieved'})
            else:
                goal.write({'state': 'missed'})
        elif total_co2 > goal.target_co2_eq:
            # Optionally trigger an alert (this can be connected to notifications)
            _logger.warning(
                f"Department {department_id} has exceeded carbon goal target "
                f"{goal.target_co2_eq} with current total of {total_co2}."
            )
            goal.write({'state': 'active'}) # active but flagged
