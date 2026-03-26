import math

def electric_time_budget(remaining_ms, depth, node_visits) -> float:
    reserve_ms = 0.12 * remaining_ms
    available_ms = max(0, remaining_ms - reserve_ms)
    root_factor = 1 / (1 + 0.35 * depth)
    visit_factor = 1 / (1 + 0.1 * node_visits)
    raw_budget = available_ms * 0.06 * root_factor * visit_factor
    min_budget = 1
    max_budget = min(120, available_ms * 0.2)
    budget_ms = max(min_budget, min(raw_budget, max_budget))
    if remaining_ms < 250:
        budget_ms = min(budget_ms, max(1, 0.08 * remaining_ms))
    return budget_ms