"""
Entrenamiento con recolección de rollouts vectorizada para AgentV2.

Semántica PPO preservada: con update_every_episodes=B, el camino secuencial
recolecta B episodios con los MISMOS pesos y luego actualiza — recolectar
esos B episodios en lockstep (un forward de batch por paso) es el mismo
algoritmo on-policy, solo cambia el orden de consumo del RNG. El buffer se
rellena episodio a episodio (contiguo), como exige el GAE del trainer.

La evaluación greedy periódica (selección de mejor modelo) se ejecuta como
fila extra greedy dentro del lockstep de la ronda que cruza el múltiplo de
greedy_eval_every.

Módulo NUEVO: no modifica agent.py; train_batched(agent, ...) es un drop-in
de agent.train(...) con la misma superficie de tracking.

La equivalencia estadística con el camino secuencial se verifica en
scripts/test_batched_train.py.
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


def _track_best(agent, makespan: float, env):
    if makespan < agent.best_makespan:
        agent.best_makespan = makespan
        agent.best_schedule = env.schedule_history
        agent.best_makespan_history = env.makespan_history
        agent.best_model_state = {
            "policy": deepcopy(agent.network.state_dict()),
            "value": {},
        }


def _collect_lockstep(agent, device, n_stochastic: int, add_greedy: bool):
    """
    Ejecuta n_stochastic episodios muestreados (+ 1 greedy opcional) en
    lockstep con forwards batcheados. Devuelve lista de episodios
    [(transiciones, makespan, total_reward, env, es_greedy)], donde
    transiciones = [(op_f, glob_f, action, log_prob, value, reward, done)].
    """
    n_total = n_stochastic + (1 if add_greedy else 0)
    envs = [deepcopy(agent.env) for _ in range(n_total)]
    encoders = [StateEncoder(e) for e in envs]
    states = [e.reset() for e in envs]
    alive = [bool(s["eligible_ops"]) for s in states]
    transitions = [[] for _ in range(n_total)]
    total_rewards = [0.0] * n_total
    greedy_idx = n_total - 1 if add_greedy else -1

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
            logits, values = agent.network(
                torch.from_numpy(op_batch).to(device),
                torch.from_numpy(glob_batch).to(device),
                torch.from_numpy(mask).to(device),
            )
        logits = logits.cpu()
        values = values.cpu()

        dist = torch.distributions.Categorical(logits=logits)
        actions = dist.sample()
        log_probs = dist.log_prob(actions)
        greedy_actions = torch.argmax(logits, dim=-1)

        for r, i in enumerate(idxs):
            a = int(greedy_actions[r].item()) if i == greedy_idx \
                else int(actions[r].item())
            states[i], reward, done, _ = envs[i].step(a)
            total_rewards[i] += reward
            if i != greedy_idx:
                transitions[i].append((
                    feats[r][0], feats[r][1], a,
                    float(log_probs[r].item()), float(values[r].item()),
                    reward, done,
                ))
            if done or not states[i]["eligible_ops"]:
                alive[i] = False

    return [(transitions[i], _makespan_upper(envs[i]), total_rewards[i],
             envs[i], i == greedy_idx) for i in range(n_total)]


def train_batched(agent, episodes: int = 100,
                  device: Optional[str] = None, verbose: bool = False):
    """
    Drop-in de agent.train(episodes): mismo tracking (best_makespan,
    training_makespan_history, losses), recolección vectorizada. El tamaño
    del lockstep es update_every_episodes (mismos pesos por construcción).
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)
    agent.network.to(device)

    b = max(1, agent.update_every_episodes)
    done_eps = 0
    t0 = time.time()

    while done_eps < episodes:
        n_round = min(b, episodes - done_eps)
        # ¿esta ronda cruza un múltiplo de greedy_eval_every?
        g = agent.greedy_eval_every
        add_greedy = (done_eps // g) != ((done_eps + n_round) // g)

        results = _collect_lockstep(agent, device, n_round, add_greedy)

        for trans, makespan, total_reward, env, is_greedy in results:
            if is_greedy:
                _track_best(agent, makespan, env)
                continue
            for op_f, glob_f, a, logp, v, r, d in trans:
                agent.buffer.store(op_f, glob_f, a, logp, v, r, d)
            agent.total_episodes += 1
            done_eps += 1
            agent.training_makespan_history.append(makespan)
            agent.episode_rewards.append(total_reward)
            _track_best(agent, makespan, env)

        losses = agent.trainer.update(agent.buffer)
        agent.training_losses["policy"].append(losses["policy_loss"])
        agent.training_losses["value"].append(losses["value_loss"])

        if verbose and done_eps % 20 == 0:
            print(f"  ep {done_eps}/{episodes} best={agent.best_makespan:.0f} "
                  f"({time.time()-t0:.0f}s)", flush=True)

    agent.network.to("cpu")
    # el estado de Adam (momentos) vive en el device donde se hizo step():
    # devolverlo a CPU para que updates posteriores fuera de esta ruta no
    # mezclen devices
    for state in agent.trainer.optimizer.state.values():
        for k, v in state.items():
            if torch.is_tensor(v):
                state[k] = v.to("cpu")
    return agent, {"best_makespan": agent.best_makespan}
