# -*- coding: utf-8 -*-

def get_environmental_score(env, company_id):
    """
    Computes E Score (40% weight) based on carbon goals progress.
    """
    goals = env['ecosphere.environmental.goal'].search([('company_id', '=', company_id), ('state', 'in', ['active', 'achieved', 'missed'])])
    if not goals:
        return 80.0 # Default fallback baseline
    
    total_perf = 0.0
    for goal in goals:
        if goal.target_co2_eq <= 0:
            continue
        if goal.current_co2_eq <= goal.target_co2_eq:
            total_perf += 100.0
        else:
            excess = goal.current_co2_eq - goal.target_co2_eq
            penalty = (excess / goal.target_co2_eq) * 100.0
            total_perf += max(100.0 - penalty, 0.0)
            
    return total_perf / len(goals)

def get_social_score(env, company_id):
    """
    Computes S Score (30% weight) from CSR progress and training rates.
    """
    activities = env['ecosphere.csr.activity'].search([('state', 'in', ['active', 'completed'])])
    csr_perf = 100.0
    if activities:
        total_csr_perf = 0.0
        for act in activities:
            if act.volunteer_hours_target > 0:
                total_csr_perf += min((act.volunteer_hours_actual / act.volunteer_hours_target) * 100.0, 100.0)
            else:
                total_csr_perf += 100.0
        csr_perf = total_csr_perf / len(activities)

    trainings = env['ecosphere.training'].search([])
    training_perf = 100.0
    if trainings:
        training_perf = sum(trainings.mapped('completion_rate')) / len(trainings)

    return (csr_perf * 0.5) + (training_perf * 0.5)

def get_governance_score(env, company_id):
    """
    Computes G Score (30% weight) from policy sign-offs and risk index penalties.
    """
    acks = env['ecosphere.policy.acknowledgment'].search([])
    ack_rate = 100.0
    if acks:
        ack_signed = len(acks.filtered(lambda a: a.state == 'acknowledged'))
        ack_rate = (ack_signed / len(acks)) * 100.0

    risks = env['ecosphere.risk'].search([])
    risk_factor = 100.0
    if risks:
        avg_score = sum(risks.mapped('score')) / len(risks)
        # Scale score 1-25 down to penalty: 25 avg score = 0 risk factor (100 - 25*4)
        risk_factor = max(100.0 - (avg_score * 4.0), 0.0)

    return (ack_rate * 0.6) + (risk_factor * 0.4)

def get_overall_esg_metrics(env, company_id):
    """
    Consolidates scores and outputs general health metadata.
    """
    e_score = get_environmental_score(env, company_id)
    s_score = get_social_score(env, company_id)
    g_score = get_governance_score(env, company_id)

    overall_score = round((e_score * 0.40) + (s_score * 0.30) + (g_score * 0.30), 1)

    # Health
    if overall_score >= 85.0:
        health = 'excellent'
    elif overall_score >= 70.0:
        health = 'good'
    elif overall_score >= 50.0:
        health = 'fair'
    else:
        health = 'poor'

    # Risk level (High if critical issues exist or risks exceed high limits)
    issues = env['ecosphere.compliance.issue'].search_count([('status', '!=', 'resolved'), ('priority', 'in', ['high', 'critical'])])
    if issues > 0:
        risk = 'high'
    else:
        risk = 'medium' if overall_score < 75.0 else 'low'

    # Trend (compare this month's carbon footprint to last month)
    # Default is stable, we simulate based on goal thresholds
    trend = 'stable'
    goals = env['ecosphere.environmental.goal'].search([('company_id', '=', company_id), ('state', '=', 'active')])
    if goals:
        exceeded = any(g.current_co2_eq > g.target_co2_eq for g in goals)
        trend = 'declining' if exceeded else 'improving'

    return {
        'score': overall_score,
        'e_score': round(e_score, 1),
        's_score': round(s_score, 1),
        'g_score': round(g_score, 1),
        'health': health,
        'trend': trend,
        'risk': risk
    }
