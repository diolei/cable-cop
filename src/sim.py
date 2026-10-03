# Illustrative five-cable stayed span. Ranks policies only.
# No certification use. Deterministic stdlib only.

T_MIN = 800.0
T_MAX = 1600.0
SIGMA_ALLOW = 110.0
DEFL_LIMIT = 0.12
S0 = 90.0
M_EXP = 3.0
N_CABLES = 5

# Load share per cable at uniform tension. Center cable carries most.
SHARE = (0.16, 0.19, 0.30, 0.19, 0.16)


def clamp_tension(t):
    if t < T_MIN:
        return T_MIN
    if t > T_MAX:
        return T_MAX
    return t


def cable_stresses(tensions, load, temp_c):
    """Stress per cable in MPa for a quasi-static block."""
    tensions = tuple(clamp_tension(t) for t in tensions)
    mean_t = sum(tensions) / len(tensions)
    temp_factor = 1.0 + 0.004 * (temp_c - 20.0)
    out = []
    for i, share in enumerate(SHARE):
        # Tighter cable sheds load; looser cable picks it up.
        redistribution = mean_t / max(1.0, tensions[i])
        stress = 62.0 * share * 5.0 * load * temp_factor * redistribution
        out.append(stress)
    return tuple(out)


def deflection(tensions, load):
    mean_t = sum(tensions) / len(tensions)
    return 0.06 * load * (1200.0 / mean_t)


def damage_rates(stresses, corrosion=1.0):
    """Miner-style rate per block. Higher range shortens life cubically."""
    rates = []
    for s in stresses:
        ratio = max(0.0, s) / S0
        rates.append(corrosion * ratio**M_EXP * 1e-4)
    return tuple(rates)


def step_damage(damage, tensions, load, temp_c=20.0, corrosion=1.0):
    stresses = cable_stresses(tensions, load, temp_c)
    rates = damage_rates(stresses, corrosion)
    nxt = tuple(d + r for d, r in zip(damage, rates))
    return nxt, stresses, sum(rates)
