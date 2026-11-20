#!/usr/bin/env python3
"""PulseFederate scaffold generator. Run: python scaffold.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "federated-population-health"
ROOT.mkdir(exist_ok=True)


def write(rel: str, content: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")
    print(f"  + {rel}")


# ---------- Directories ----------
for d in [
    "backend/app/api", "backend/app/domain", "backend/app/ml", "backend/app/services",
    "backend/tests",
    "frontend/src/app/admin", "frontend/src/app/hospital",
    "frontend/src/components", "frontend/src/lib",
    "clients",
    "data/synthetic", "data/partitions",
    "docker", "k8s", "monitoring", "docs", "tests", "scripts",
]:
    (ROOT / d).mkdir(parents=True, exist_ok=True)

print("=== ROOT ===")
write("README.md", """# Federated Population Health Platform
...
""")
Privacy-preserving community risk stratification using Flower + PyTorch + FastAPI + Next.js.

## Quick Start
bash
python scripts/generate_synthetic_data.py
docker compose -f docker/docker-compose.yml up --build