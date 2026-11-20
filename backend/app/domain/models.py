"""Domain dataclasses."""
from dataclasses import dataclass
from typing import List


@dataclass
class TrainingConfig:
    rounds: int = 5
    local_epochs: int = 2
    learning_rate: float = 0.01
    dp_noise: float = 0.0
    dp_clip: float = 1.0
    min_clients: int = 2


@dataclass
class ClientMetrics:
    client_id: str
    num_samples: int
    accuracy: float
    loss: float


@dataclass
class RoundResult:
    round: int
    aggregated_accuracy: float
    aggregated_loss: float
    client_metrics: List[ClientMetrics]
    fairness_score: float
    timestamp: str


@dataclass
class TrainingResult:
    config: TrainingConfig
    rounds: List[RoundResult]
    final_accuracy: float