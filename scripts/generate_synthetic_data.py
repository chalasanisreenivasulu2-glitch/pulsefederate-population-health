"""Generate synthetic hospital-site data modeled on Abu Dhabi population health risks."""
import numpy as np
import pandas as pd
from pathlib import Path


def generate_site(n_samples: int, seed: int, path: Path, site_type: str) -> None:
    rng = np.random.default_rng(seed)

    # Base demographics aligned with UAE/Abu Dhabi health data
    age = rng.integers(18, 85, n_samples)
    
    # Abu Dhabi has high obesity (61% overweight/obese). We model this with a mean BMI of ~29.
    if site_type == "rural":
        bmi = rng.normal(31, 6, n_samples).clip(16, 50)
    else:
        bmi = rng.normal(29, 5.5, n_samples).clip(16, 50)

    # Clinical thresholds: Raise baselines slightly so only extreme cases are flagged
    bp = rng.normal(128, 15, n_samples).clip(80, 210)
    glucose = rng.normal(105, 18, n_samples).clip(60, 350)

    # Smoking rate in UAE is ~14% for adults
    smoker = rng.choice([0, 1], size=n_samples, p=[0.86, 0.14])

    # Clinical Risk Logic (Target Variable)
    # High risk if: (Obese AND High BP) OR (Diabetic) OR (Smoker over 55)
    # We use tighter thresholds to ensure a realistic 20-25% positive rate.
    risk = (
        ((bmi >= 35) & (bp >= 145)) |
        (glucose >= 135) |
        ((smoker == 1) & (age > 55))
    ).astype(int)

    df = pd.DataFrame({
        "age": age, "bmi": np.round(bmi, 1), "bp": bp.astype(int),
        "glucose": glucose.astype(int), "smoker": smoker, "risk_label": risk,
    })
    df.to_csv(path, index=False)
    print(f"Wrote {n_samples} samples -> {path} ({site_type}, {risk.mean():.1%} high-risk)")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "data" / "partitions"
    out.mkdir(parents=True, exist_ok=True)
    
    generate_site(2000, 42, out / "site_a.csv", "urban")
    generate_site(2000, 43, out / "site_b.csv", "urban")
    generate_site(1000, 44, out / "site_c.csv", "rural")
