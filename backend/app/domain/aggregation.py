"""Weighted FedAvg aggregation."""
from typing import Dict, List
import numpy as np


def weighted_fedavg(state_dicts: List[Dict[str, np.ndarray]],
                    sample_counts: List[int]) -> Dict[str, np.ndarray]:
    if not state_dicts:
        raise ValueError("state_dicts cannot be empty")
    if len(state_dicts) != len(sample_counts):
        raise ValueError("state_dicts and sample_counts must have equal length")
    total = sum(sample_counts)
    if total <= 0:
        raise ValueError("Total sample count must be positive")
    weights = [c / total for c in sample_counts]
    aggregated = {}
    for key in state_dicts[0].keys():
        acc = state_dicts[0][key] * weights[0]
        for i in range(1, len(state_dicts)):
            acc = acc + state_dicts[i][key] * weights[i]
        aggregated[key] = acc
    return aggregated