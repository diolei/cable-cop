# cable-cop

Trainer for a five-cable stayed-span fatigue model. It generates synthetic 
traffic blocks, solves quasi-static cable equilibrium, accumulates 
Miner-style damage over stress ranges with
temperature and corrosion factors, and compares fixed tensions
against constrained redistribution. The export is one self-contained
versioned JSON snapshot for forward-only inference.

Requires Python 3, stdlib only — no dependencies.

## Layout

- `src/sim.py` — span equilibrium, stress ranges, damage rate
- `src/policy.py` — fixed, rule-based, one-step damage-aware policies
- `src/export.py` — emits `cable-cop-weights.json`
- `tests/` — golden checks on the illustrative model

## Reproduce

```sh
python3 -m src.export --seed 7 --out cable-cop-weights.json
python3 -c "from tests.test_sim import test_fixed_keeps_tensions, test_damage_grows_with_load, test_policies_respect_limits; test_fixed_keeps_tensions(); test_damage_grows_with_load(); test_policies_respect_limits(); print('checks pass')"
```

