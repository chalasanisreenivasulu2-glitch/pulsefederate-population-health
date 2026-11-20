"""Dataset loading and scaling."""
from typing import Tuple
import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset


def load_csv(path: str, target_col: str = "risk_label",
             test_size: float = 0.2, seed: int = 42):
    df = pd.read_csv(path)
    if target_col not in df.columns:
        raise ValueError(f"Missing target column {target_col} in {path}")
    feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols].values.astype(np.float32)
    y = df[target_col].values.astype(np.int64)
    X_tr, X_val, y_tr, y_val = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y)
    scaler = StandardScaler()
    X_tr = scaler.fit_transform(X_tr).astype(np.float32)
    X_val = scaler.transform(X_val).astype(np.float32)
    return (X_tr, y_tr), (X_val, y_val), scaler


def make_loader(X, y, batch_size: int = 32, shuffle: bool = True) -> DataLoader:
    ds = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    return DataLoader(ds, batch_size=batch_size, shuffle=shuffle)