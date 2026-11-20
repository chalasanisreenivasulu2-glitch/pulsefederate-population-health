"""Local training routine."""
from typing import Optional, Tuple
import torch
import torch.nn as nn
from ..domain import privacy as dp
from .models import TabularClassifier


def train_local(X_train, y_train, X_val, y_val, config,
                model: Optional[TabularClassifier] = None) -> Tuple[dict, float, float]:
    if model is None:
        model = TabularClassifier(input_dim=X_train.shape[1])
    optimizer = torch.optim.SGD(model.parameters(), lr=config.learning_rate)
    criterion = nn.CrossEntropyLoss()
    X_t = torch.from_numpy(X_train)
    y_t = torch.from_numpy(y_train)
    model.train()
    for _ in range(config.local_epochs):
        optimizer.zero_grad()
        loss = criterion(model(X_t), y_t)
        loss.backward()
        if config.dp_noise > 0:
            dp.clip_gradients(model, config.dp_clip)
            dp.add_gaussian_noise(model, config.dp_noise, config.dp_clip, X_t.shape[0])
        optimizer.step()
    model.eval()
    with torch.no_grad():
        val_logits = model(torch.from_numpy(X_val))
        val_loss = float(criterion(val_logits, torch.from_numpy(y_val)).item())
        preds = val_logits.argmax(dim=1).numpy()
        acc = float((preds == y_val).mean())
    return model.state_dict(), acc, val_loss