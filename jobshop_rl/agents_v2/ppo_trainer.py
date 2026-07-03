"""
Entrenador PPO para agents_v2 — co-diseñado desde cero (batches, normalización
de ventajas, gamma=1 para horizonte finito), sin heredar el régimen por
muestra del v1.
"""

from typing import List

import numpy as np
import torch
import torch.nn.functional as F

from jobshop_rl.agents_v2.state_encoder import OP_FEATURE_DIM


class RolloutBuffer:
    """Almacena transiciones de uno o varios episodios completos."""

    def __init__(self):
        self.op_feats: List[np.ndarray] = []      # (n_i, OP_DIM), tamaño variable
        self.global_feats: List[np.ndarray] = []
        self.actions: List[int] = []
        self.log_probs: List[float] = []
        self.values: List[float] = []
        self.rewards: List[float] = []
        self.dones: List[bool] = []

    def store(self, op_f, glob_f, action, log_prob, value, reward, done):
        self.op_feats.append(op_f)
        self.global_feats.append(glob_f)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.values.append(value)
        self.rewards.append(reward)
        self.dones.append(done)

    def __len__(self):
        return len(self.actions)

    def clear(self):
        self.__init__()


class PPOTrainerV2:

    def __init__(self, network, lr: float = 3e-4, gamma: float = 1.0,
                 gae_lambda: float = 0.95, eps_clip: float = 0.2,
                 k_epochs: int = 4, minibatch_size: int = 256,
                 entropy_coef: float = 0.01, value_coef: float = 0.5,
                 max_grad_norm: float = 0.5):
        self.network = network
        self.optimizer = torch.optim.Adam(network.parameters(), lr=lr, eps=1e-5)
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.eps_clip = eps_clip
        self.k_epochs = k_epochs
        self.minibatch_size = minibatch_size
        self.entropy_coef = entropy_coef
        self.value_coef = value_coef
        self.max_grad_norm = max_grad_norm

    def _compute_gae(self, buffer: RolloutBuffer):
        """GAE sobre trayectorias con episodios terminales (bootstrap 0)."""
        n = len(buffer)
        advantages = np.zeros(n, dtype=np.float32)
        gae = 0.0
        for t in reversed(range(n)):
            if buffer.dones[t]:
                next_value = 0.0
                next_non_terminal = 0.0
            else:
                next_value = buffer.values[t + 1] if t + 1 < n else 0.0
                next_non_terminal = 1.0
            delta = (buffer.rewards[t]
                     + self.gamma * next_value * next_non_terminal
                     - buffer.values[t])
            gae = delta + self.gamma * self.gae_lambda * next_non_terminal * gae
            advantages[t] = gae
        returns = advantages + np.asarray(buffer.values, dtype=np.float32)
        return advantages, returns

    @staticmethod
    def _pad_batch(op_feats_list, device):
        """Apila features de tamaño variable con padding + máscara."""
        max_m = max(f.shape[0] for f in op_feats_list)
        batch = np.zeros((len(op_feats_list), max_m, OP_FEATURE_DIM), dtype=np.float32)
        mask = np.zeros((len(op_feats_list), max_m), dtype=bool)
        for i, f in enumerate(op_feats_list):
            batch[i, :f.shape[0]] = f
            mask[i, :f.shape[0]] = True
        return (torch.from_numpy(batch).to(device),
                torch.from_numpy(mask).to(device))

    def update(self, buffer: RolloutBuffer) -> dict:
        """Actualiza la red con el contenido del buffer y lo vacía."""
        if len(buffer) == 0:
            return {"policy_loss": 0.0, "value_loss": 0.0}

        device = next(self.network.parameters()).device
        advantages, returns = self._compute_gae(buffer)

        adv_t = torch.from_numpy(advantages).to(device)
        adv_t = (adv_t - adv_t.mean()) / (adv_t.std() + 1e-8)
        ret_t = torch.from_numpy(returns).to(device)
        actions_t = torch.tensor(buffer.actions, dtype=torch.int64, device=device)
        old_logp_t = torch.tensor(buffer.log_probs, dtype=torch.float32, device=device)
        glob_t = torch.from_numpy(np.stack(buffer.global_feats)).to(device)

        n = len(buffer)
        indices = np.arange(n)
        policy_losses, value_losses = [], []

        for _ in range(self.k_epochs):
            np.random.shuffle(indices)
            for start in range(0, n, self.minibatch_size):
                mb = indices[start:start + self.minibatch_size]

                op_b, mask_b = self._pad_batch([buffer.op_feats[i] for i in mb], device)
                logits, values = self.network(op_b, glob_t[mb], mask_b)

                dist = torch.distributions.Categorical(logits=logits)
                new_logp = dist.log_prob(actions_t[mb])
                entropy = dist.entropy().mean()

                ratio = torch.exp(new_logp - old_logp_t[mb])
                surr1 = ratio * adv_t[mb]
                surr2 = torch.clamp(ratio, 1 - self.eps_clip, 1 + self.eps_clip) * adv_t[mb]
                policy_loss = -torch.min(surr1, surr2).mean()

                value_loss = F.mse_loss(values, ret_t[mb])

                loss = (policy_loss
                        + self.value_coef * value_loss
                        - self.entropy_coef * entropy)

                self.optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.network.parameters(), self.max_grad_norm)
                self.optimizer.step()

                policy_losses.append(policy_loss.item())
                value_losses.append(value_loss.item())

        buffer.clear()
        return {
            "policy_loss": float(np.mean(policy_losses)),
            "value_loss": float(np.mean(value_losses)),
        }
