from src.policy import fixed_policy, greedy_policy, rule_policy
from src.sim import N_CABLES, T_MAX, T_MIN, step_damage


def test_fixed_keeps_tensions():
    t = (1200.0,) * N_CABLES
    assert fixed_policy(t) == t


def test_damage_grows_with_load():
    d = (0.0,) * N_CABLES
    low, _, _ = step_damage(d, (1200.0,) * N_CABLES, 0.6)
    high, _, _ = step_damage(d, (1200.0,) * N_CABLES, 1.4)
    assert sum(high) > sum(low)


def test_policies_respect_limits():
    t = (T_MIN,) * N_CABLES
    d = (0.0,) * N_CABLES
    for cand in (rule_policy(t, d), greedy_policy(t, d, 1.0)):
        assert len(cand) == N_CABLES
        assert min(cand) >= T_MIN
        assert max(cand) <= T_MAX
