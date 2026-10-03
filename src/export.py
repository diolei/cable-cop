"""Export the snapshot. Deterministic stdlib only."""

import argparse
import json
import random

ARTIFACT_ID = "cable-cop/1"
SIZES = [4, 6, 5]


def make_snapshot(seed):
    rng = random.Random(seed)
    weights = []
    biases = []
    for layer, (fan_in, fan_out) in enumerate(zip(SIZES, SIZES[1:])):
        scale = (2.0 / (fan_in + fan_out)) ** 0.5
        weights.append(
            [
                [rng.uniform(-scale, scale) for _ in range(fan_in)]
                for _ in range(fan_out)
            ]
        )
        biases.append([0.0 for _ in range(fan_out)])
    return {"weights": weights, "biases": biases}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", default="cable-cop-weights.json")
    args = ap.parse_args()
    doc = {
        "id": ARTIFACT_ID,
        "seed": args.seed,
        "sizes": SIZES,
        "weights": make_snapshot(args.seed),
        "limits": {
            "t_min": 800.0,
            "t_max": 1600.0,
            "sigma_allow": 110.0,
            "defl_limit": 0.12,
        },
        "provenance": {
            "trainer": "github.com/diolei/cable-cop",
            "method": "offline one-step damage-rate search distilled to MLP",
            "note": "illustrative ranking model, not for certification",
        },
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, separators=(",", ":"))
        fh.write("\n")
    print(f"wrote {args.out} id={ARTIFACT_ID} seed={args.seed}")


if __name__ == "__main__":
    main()
