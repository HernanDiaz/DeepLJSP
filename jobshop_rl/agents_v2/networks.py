"""
Red de política y valor invariante al tamaño (Deep Sets + heads por operación).

Una única red con dos cabezas:
- policy: puntúa cada operación elegible (embedding propio ⊕ contexto global
  agregado por pooling) → softmax sobre las elegibles.
- value: MLP sobre el contexto agregado — sin dependencia de num_jobs ni
  num_machines, a diferencia del v1.
"""

import torch
import torch.nn as nn

from jobshop_rl.agents_v2.state_encoder import OP_FEATURE_DIM, GLOBAL_FEATURE_DIM


def _mlp(dims, out_gain=None):
    layers = []
    for i in range(len(dims) - 1):
        layers.append(nn.Linear(dims[i], dims[i + 1]))
        if i < len(dims) - 2:
            layers.append(nn.LayerNorm(dims[i + 1]))
            layers.append(nn.ReLU())
    net = nn.Sequential(*layers)
    # Inicialización ortogonal (estándar PPO)
    linear_layers = [m for m in net.modules() if isinstance(m, nn.Linear)]
    for i, m in enumerate(linear_layers):
        gain = 2 ** 0.5
        if out_gain is not None and i == len(linear_layers) - 1:
            gain = out_gain
        nn.init.orthogonal_(m.weight, gain)
        nn.init.zeros_(m.bias)
    return net


class PolicyValueNetV2(nn.Module):

    def __init__(self, op_dim: int = OP_FEATURE_DIM, global_dim: int = GLOBAL_FEATURE_DIM,
                 hidden: int = 128):
        super().__init__()
        self.hidden = hidden
        self.op_encoder = _mlp([op_dim, hidden, hidden])
        self.context = _mlp([2 * hidden + global_dim, hidden, hidden])
        # gain pequeño en la última capa de la política → logits iniciales ~0
        self.policy_head = _mlp([2 * hidden, hidden, 1], out_gain=0.01)
        self.value_head = _mlp([hidden, hidden, 1], out_gain=1.0)

    def forward(self, op_feats: torch.Tensor, global_feats: torch.Tensor,
                mask: torch.Tensor = None):
        """
        Args:
            op_feats: (B, M, op_dim) — M = máximo de elegibles del batch (padding)
            global_feats: (B, global_dim)
            mask: (B, M) bool, True donde hay operación real. None = todo real.

        Returns:
            logits (B, M) con -inf en el padding, values (B,)
        """
        if mask is None:
            mask = torch.ones(op_feats.shape[:2], dtype=torch.bool,
                              device=op_feats.device)

        phi = self.op_encoder(op_feats)                       # (B, M, H)

        mask_f = mask.unsqueeze(-1).float()
        counts = mask_f.sum(dim=1).clamp(min=1.0)
        mean_pool = (phi * mask_f).sum(dim=1) / counts        # (B, H)
        max_pool = phi.masked_fill(~mask.unsqueeze(-1), float("-inf")).max(dim=1).values
        max_pool = torch.where(torch.isfinite(max_pool), max_pool,
                               torch.zeros_like(max_pool))    # filas sin válidos

        ctx = self.context(torch.cat([mean_pool, max_pool, global_feats], dim=-1))  # (B, H)

        ctx_exp = ctx.unsqueeze(1).expand(-1, phi.shape[1], -1)
        logits = self.policy_head(torch.cat([phi, ctx_exp], dim=-1)).squeeze(-1)    # (B, M)
        logits = logits.masked_fill(~mask, float("-inf"))

        values = self.value_head(ctx).squeeze(-1)             # (B,)
        return logits, values
