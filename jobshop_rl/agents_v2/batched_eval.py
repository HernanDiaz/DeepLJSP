"""
Evaluación best-of-N vectorizada para AgentV2.

Los N rollouts del best-of-N son independientes: se avanzan N entornos en
lockstep y se hace UN forward de batch (N, M_max, op_dim) por paso de
despacho, en CPU o GPU. El perfil del rollout secuencial muestra que el
forward de la red es el 64-77% del tiempo (batch de 1), así que batchearlo
es donde está la ganancia; encode y env.step siguen siendo Python por
entorno.

Módulo NUEVO: no modifica el camino secuencial de agent.py. La semántica es
la de evaluate_policy (idea-16): muestra 0 greedy (argmax), resto muestreadas
de la distribución de la política; se devuelve la mejor por makespan (peor
caso, upper).

La equivalencia con el camino secuencial se verifica en
scripts/test_batched_eval.py (greedy batcheado == greedy secuencial).
"""

import time
from copy import deepcopy
from typing import Optional

import numpy as np
import torch

from jobshop_rl.agents_v2.state_encoder import StateEncoder
from jobshop_rl.models.interval import Interval


def _makespan_upper(env) -> float:
    m = max(env.job_completion_time)
    return float(m.upper) if isinstance(m, Interval) else float(m)


def evaluate_policy_batched(agent, n_samples: int = 1,
                            device: Optional[str] = None,
                            chunk_size: int = 256,
                            seed: Optional[int] = None):
    """
    Best-of-N con rollouts en lockstep. Devuelve la misma tupla que
    AgentV2.evaluate_policy: (best_makespan, best_schedule, best_history, t).

    Args:
        agent: AgentV2 con la red ya cargada.
        n_samples: N del best-of-N (muestra 0 greedy, resto estocásticas).
        device: "cuda", "cpu" o None (auto: cuda si está disponible).
        chunk_size: entornos simultáneos máximos (memoria/deepcopy).
        seed: semilla del generador de muestreo (reproducibilidad); None =
            RNG global de torch (comportamiento del camino secuencial).
    """
    start_time = time.time()
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)

    network = agent.network.to(device)
    network.eval()

    generator = None
    if seed is not None:
        generator = torch.Generator(device="cpu")
        generator.manual_seed(seed)

    best_makespan = float("inf")
    best_schedule = []
    best_history = []

    n_samples = max(1, n_samples)
    first_of_run = True
    remaining = n_samples
    while remaining > 0:
        batch = min(chunk_size, remaining)
        # la muestra 0 global es greedy; el resto estocásticas
        greedy_rows = {0} if first_of_run else set()

        envs = [deepcopy(agent.env) for _ in range(batch)]
        encoders = [StateEncoder(e) for e in envs]
        states = [e.reset() for e in envs]
        alive = [bool(s["eligible_ops"]) for s in states]

        while any(alive):
            idxs = [i for i, a in enumerate(alive) if a]
            feats = [encoders[i].encode(states[i]) for i in idxs]
            sizes = [f[0].shape[0] for f in feats]
            m_max = max(sizes)

            op_batch = np.zeros((len(idxs), m_max, feats[0][0].shape[1]),
                                dtype=np.float32)
            glob_batch = np.stack([f[1] for f in feats])
            mask = np.zeros((len(idxs), m_max), dtype=bool)
            for r, (f, n) in enumerate(zip(feats, sizes)):
                op_batch[r, :n] = f[0]
                mask[r, :n] = True

            with torch.no_grad():
                logits, _ = network(
                    torch.from_numpy(op_batch).to(device),
                    torch.from_numpy(glob_batch).to(device),
                    torch.from_numpy(mask).to(device),
                )
            logits = logits.cpu()

            greedy_actions = torch.argmax(logits, dim=-1)
            probs = torch.softmax(logits, dim=-1)
            sampled_actions = torch.multinomial(
                probs, 1, generator=generator).squeeze(-1)

            for r, i in enumerate(idxs):
                a = greedy_actions[r] if i in greedy_rows else sampled_actions[r]
                states[i], _, done, _ = envs[i].step(int(a.item()))
                if done or not states[i]["eligible_ops"]:
                    alive[i] = False

        for i, env in enumerate(envs):
            makespan = _makespan_upper(env)
            if makespan < best_makespan or (first_of_run and i == 0):
                best_makespan = makespan
                best_schedule = env.schedule_history
                best_history = env.makespan_history

        first_of_run = False
        remaining -= batch

    agent.network.to("cpu")
    return best_makespan, best_schedule, best_history, time.time() - start_time
