"""
Modelos de redes neuronales para Job Shop RL.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional

class FeatureExtractor(nn.Module):
    """Extractor de características para las operaciones"""

    def __init__(self, input_dim: int, hidden_dim: int):
        super(FeatureExtractor, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x

class PolicyNetwork(nn.Module):
    """Red neuronal para la política de selección de acciones"""

    def __init__(self, input_dim: int, hidden_dim: int):
        super(PolicyNetwork, self).__init__()
        self.feature_extractor = FeatureExtractor(input_dim, hidden_dim)
        self.output = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor) -> Optional[torch.Tensor]:
        if x.size(0) == 0:
            return None

        features = self.feature_extractor(x)
        logits = self.output(features).squeeze(-1)
        return F.softmax(logits, dim=0)

class ValueNetwork(nn.Module):
    """Red neuronal para la función de valor"""

    def __init__(self, state_dim: int, hidden_dim: int):
        super(ValueNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)