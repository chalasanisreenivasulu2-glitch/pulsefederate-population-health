# PulseFederate - Federated Population Health Platform

Privacy-preserving community risk stratification using Flower + PyTorch + FastAPI + Next.js.

## Architecture

Hospital nodes -> Local training (DP-SGD) -> Secure FedAvg -> Global model -> Dashboard.

Raw patient data never leaves a hospital node. Only model weights are aggregated.

## Quick Start

### 1. Generate synthetic data

```powershell
python scripts\generate_synthetic_data.py
```

### 2. Install backend dependencies

```powershell
pip install fastapi "uvicorn[standard]" pydantic flwr torch scikit-learn pandas numpy pyyaml pytest httpx prometheus-client
```

### 3. Start the backend API

```powershell
$env:DATA_DIR = (Resolve-Path .\data\partitions).Path
uvicorn backend.app.main:app --reload --port 8000
```

### 4. Run federated training via CLI

```powershell
python launcher.py simulate --rounds 5
```

Expected output: accuracy improves across rounds (e.g. 0.64 -> 0.76), fairness stays above 0.95.

### 5. Start the frontend dashboard

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:3000/admin and click "Run Federated Training".

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /health | Service health check |
| GET | /api/sites | List hospital site CSVs |
| POST | /api/train | Run federated training rounds |
| GET | /api/audit | Immutable-style audit event log |

Interactive docs: http://localhost:8000/docs

## Project Structure

```
federated-population-health/
backend/                # FastAPI + PyTorch + Flower
  app/
    api/routes.py       # REST endpoints
    domain/
      aggregation.py    # Weighted FedAvg
      privacy.py        # DP-SGD (gradient clipping + noise)
      fairness.py       # Per-site fairness scoring
    ml/
      models.py         # TabularClassifier (DNN)
      datasets.py       # CSV loading + scaling
      trainer.py        # Local training routine
    services/
      simulation.py     # In-process FL simulator
      fl_server.py      # Flower aggregator
frontend/               # Next.js + Tailwind + Recharts
  src/app/admin/        # Training dashboard
  src/app/hospital/     # Hospital node view
clients/                # Flower hospital-node client
data/partitions/        # Synthetic site data (gitignored)
scripts/
  generate_synthetic_data.py
launcher.py             # CLI: simulate / serve / fl-server / client
```

## Responsible AI

- **Data minimization**: raw records never leave the node
- **Differential privacy**: DP-SGD with per-sample gradient clipping and calibrated Gaussian noise
- **Fairness monitoring**: per-client accuracy disparity tracked every round
- **Auditability**: every aggregation round is timestamped and logged

## License

MIT
