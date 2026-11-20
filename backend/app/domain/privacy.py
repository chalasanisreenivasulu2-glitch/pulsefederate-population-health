"""Differential privacy utilities (DP-SGD)."""
import math
import torch


def clip_gradients(model: torch.nn.Module, max_norm: float) -> None:
    total_norm_sq = 0.0
    for p in model.parameters():
        if p.grad is not None:
            total_norm_sq += p.grad.data.norm(2).item() ** 2
    total_norm = math.sqrt(total_norm_sq)
    clip_coef = max_norm / (total_norm + 1e-6)
    if clip_coef < 1.0:
        for p in model.parameters():
            if p.grad is not None:
                p.grad.data.mul_(clip_coef)


def add_gaussian_noise(model: torch.nn.Module, noise_multiplier: float,
                       clip_norm: float, batch_size: int) -> None:
    if noise_multiplier <= 0:
        return
    sigma = noise_multiplier * clip_norm / max(batch_size, 1)
    for p in model.parameters():
        if p.grad is not None:
            p.grad.data.add_(torch.randn_like(p.grad) * sigma)


def compute_privacy_budget(noise_multiplier: float, sample_rate: float,
                           steps: int, delta: float = 1e-5) -> float:
    if noise_multiplier <= 0 or steps <= 0:
        return float("inf")
    rdp = steps * (sample_rate ** 2) / (2 * noise_multiplier ** 2)
    eps = rdp + math.log(1.0 / delta) / max(steps * sample_rate, 1e-12)
    return round(float(eps), 4)