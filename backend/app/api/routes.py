"""REST API surface."""
import glob, os
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..domain.models import TrainingConfig
from ..ml.datasets import load_csv
from ..services.simulation import FederatedSimulator

router = APIRouter()


class TrainRequest(BaseModel):
    rounds: int = Field(5, ge=1, le=50)
    local_epochs: int = Field(2, ge=1, le=20)
    learning_rate: float = Field(0.01, gt=0)
    dp_noise: float = Field(0.0, ge=0)
    dp_clip: float = Field(1.0, gt=0)
    min_clients: int = Field(2, ge=1)


class ClientOut(BaseModel):
    client_id: str
    num_samples: int
    accuracy: float
    loss: float


class RoundOut(BaseModel):
    round: int
    accuracy: float
    loss: float
    fairness: float
    clients: List[ClientOut]
    timestamp: str


class TrainResponse(BaseModel):
    final_accuracy: float
    rounds: List[RoundOut]


@router.get("/health")
def health():
    return {"status": "ok", "service": "federated-population-health"}


@router.get("/api/sites")
def list_sites():
    data_dir = os.getenv("DATA_DIR", "../data/partitions")
    paths = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    return {"data_dir": data_dir, "sites": [os.path.basename(p) for p in paths]}


@router.post("/api/train", response_model=TrainResponse)
def train(req: TrainRequest):
    data_dir = os.getenv("DATA_DIR", "../data/partitions")
    paths = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    if len(paths) < req.min_clients:
        raise HTTPException(400, f"Need at least {req.min_clients} site files; found {len(paths)}")
    sites = {}
    for p in paths:
        sid = os.path.splitext(os.path.basename(p))[0]
        (Xtr, ytr), (Xval, yval), _ = load_csv(p, target_col="risk_label")
        sites[sid] = {"X_train": Xtr, "y_train": ytr, "X_val": Xval, "y_val": yval}
    cfg = TrainingConfig(**req.model_dump())
    result = FederatedSimulator(sites, cfg).run()
    return TrainResponse(
        final_accuracy=result.final_accuracy,
        rounds=[RoundOut(round=r.round, accuracy=r.aggregated_accuracy,
                         loss=r.aggregated_loss, fairness=r.fairness_score,
                         clients=[ClientOut(**c.__dict__) for c in r.client_metrics],
                         timestamp=r.timestamp) for r in result.rounds])


@router.get("/api/audit")
def audit():
    return {"events": [
        {"event": "system_initialized", "time": "2026-11-12T00:00:00Z"},
        {"event": "privacy_policy_loaded", "time": "2026-11-12T00:00:01Z", "policy": "DP-SGD"},
    ]}