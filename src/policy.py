# Policies compared on the same seed.
from .sim import T_MAX, T_MIN, cable_stresses, clamp_tension, damage_rates


def clamp_all(tensions):
    return tuple(clamp_tension(t) for t in tensions)


def fixed_policy(tensions):
    return tuple(tensions)


def rule_policy(tensions, damage):
    """Shed load from the most damaged cable onto its neighbors."""
    worst = max(range(len(tensions)), key=lambda i: damage[i])
    out = list(tensions)
    shed = 24.0
    out[worst] = clamp_tension(out[worst] + shed)
    for nb in (worst - 1, worst + 1):
        if 0 <= nb < len(out):
            out[nb] = clamp_tension(out[nb] - shed / 2.0)
    return tuple(out)


def greedy_policy(tensions, damage, load, temp_c=20.0, step=24.0):
    """One-step damage-rate search over single-cable moves."""
    base = damage_rates(cable_stresses(tensions, load, temp_c))
    base_cost = sum(base)
    best = tuple(tensions)
    for i in range(len(tensions)):
        for delta in (step, -step):
            cand = list(tensions)
            cand[i] = clamp_tension(cand[i] + delta)
            cost = sum(damage_rates(cable_stresses(cand, load, temp_c)))
            # Actuation penalty keeps the optimizer from jittering.
            cost += 1e-6 * abs(delta) / T_MAX
            if cost < base_cost:
                base_cost = cost
                best = tuple(cand)
    # Keep tensions inside hard limits even when the search stalls.
    low = min(best)
    high = max(best)
    if low < T_MIN or high > T_MAX:
        best = clamp_all(best)
    return best
