"""In-process federated simulation."""
from datetime import datetime, timezone
from typing import Dict, List
from ..domain.aggregation import weighted_fedavg
from ..domain.fairness import fairness_score
from ..domain.models import ClientMetrics, RoundResult, TrainingConfig, TrainingResult
from ..ml.models import TabularClassifier
from ..ml.trainer import train_local


class FederatedSimulator:
    def __init__(self, sites: Dict[str, dict], config: TrainingConfig):
        self.sites = sites
        self.config = config
        self.global_model = None
        self.rounds: List[RoundResult] = []

    def run(self) -> TrainingResult:
        if len(self.sites) < self.config.min_clients:
            raise ValueError(f"Need at least {self.config.min_clients} sites")
        first = next(iter(self.sites.values()))
        self.global_model = TabularClassifier(input_dim=first["X_train"].shape[1])
        for r in range(1, self.config.rounds + 1):
            self.rounds.append(self._run_round(r))
        return TrainingResult(config=self.config, rounds=self.rounds,
                              final_accuracy=self.rounds[-1].aggregated_accuracy)

    def _run_round(self, round_idx: int) -> RoundResult:
        state_dicts, counts, metrics = [], [], []
        for sid, data in self.sites.items():
            model = TabularClassifier(input_dim=data["X_train"].shape[1])
            model.load_state_dict(self.global_model.state_dict())
            sd, acc, loss = train_local(
                data["X_train"], data["y_train"], data["X_val"], data["y_val"],
                self.config, model=model)
            state_dicts.append(sd)
            counts.append(len(data["y_train"]))
            metrics.append(ClientMetrics(client_id=sid,
                                         num_samples=len(data["y_train"]),
                                         accuracy=acc, loss=loss))
        agg_sd = weighted_fedavg(state_dicts, counts)
        self.global_model.load_state_dict(agg_sd)
        total = sum(c.num_samples for c in metrics)
        agg_acc = sum(c.accuracy * c.num_samples for c in metrics) / total
        agg_loss = sum(c.loss * c.num_samples for c in metrics) / total
        return RoundResult(round=round_idx,
                           aggregated_accuracy=round(agg_acc, 4),
                           aggregated_loss=round(agg_loss, 4),
                           client_metrics=metrics,
                           fairness_score=fairness_score([c.accuracy for c in metrics]),
                           timestamp=datetime.now(timezone.utc).isoformat())