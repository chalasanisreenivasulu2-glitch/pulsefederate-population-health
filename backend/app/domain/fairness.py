"""Fairness scoring."""
from typing import List
import numpy as np


def fairness_score(accuracies: List[float]) -> float:
    if len(accuracies) < 2:
        return 1.0
    mean = float(np.mean(accuracies))
    if mean <= 0:
        return 0.0
    std = float(np.std(accuracies))
    return round(max(0.0, min(1.0, 1.0 - (std / mean))), 4)