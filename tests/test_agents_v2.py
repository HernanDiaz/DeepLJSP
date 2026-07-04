"""
Tests de agents_v2: invarianza al tamaño, dimensiones del encoder,
validez de acciones y ciclo de entrenamiento mínimo.
"""

import sys
import os

import numpy as np
import pytest
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.agents_v2 import AgentV2
from jobshop_rl.agents_v2.networks import PolicyValueNetV2
from jobshop_rl.agents_v2.state_encoder import (
    StateEncoder, OP_FEATURE_DIM, GLOBAL_FEATURE_DIM,
)
from jobshop_rl.data.test_3x3_interval import (
    get_test_3x3_interval, get_test_3x3_deterministic,
)
from jobshop_rl.data.ft10_interval import get_ft10_interval_problem


def _make_env(problem):
    return JobShopEnv(
        num_jobs=problem["num_jobs"],
        num_machines=problem["num_machines"],
        sequences=problem["sequences"],
        durations=problem["durations"],
    )


class TestStateEncoder:

    def test_dimensions_fixed_across_sizes(self):
        """Las dimensiones no dependen del tamaño del problema."""
        for problem in (get_test_3x3_interval(), get_ft10_interval_problem()):
            env = _make_env(problem)
            state = env.reset()
            op_f, glob_f = StateEncoder(env).encode(state)
            assert op_f.shape == (len(state["eligible_ops"]), OP_FEATURE_DIM)
            assert glob_f.shape == (GLOBAL_FEATURE_DIM,)

    def test_scalar_problem_supported(self):
        """Los problemas deterministas producen anchuras de incertidumbre 0."""
        env = _make_env(get_test_3x3_deterministic())
        state = env.reset()
        op_f, _ = StateEncoder(env).encode(state)
        # columnas 2 y 5 = anchuras relativas de duración y earliest start
        assert np.allclose(op_f[:, 2], 0.0)
        assert np.allclose(op_f[:, 5], 0.0)

    def test_features_are_finite_along_episode(self):
        env = _make_env(get_test_3x3_interval())
        encoder = StateEncoder(env)
        state = env.reset()
        done = False
        while not done and state["eligible_ops"]:
            op_f, glob_f = encoder.encode(state)
            assert np.isfinite(op_f).all()
            assert np.isfinite(glob_f).all()
            state, _, done, _ = env.step(0)


class TestNetworkSizeInvariance:

    def test_same_network_any_problem_size(self):
        """Una misma instancia de red procesa estados de 3x3 y 10x10."""
        net = PolicyValueNetV2()
        for problem in (get_test_3x3_interval(), get_ft10_interval_problem()):
            env = _make_env(problem)
            state = env.reset()
            op_f, glob_f = StateEncoder(env).encode(state)
            logits, value = net(torch.from_numpy(op_f).unsqueeze(0),
                                torch.from_numpy(glob_f).unsqueeze(0))
            assert logits.shape == (1, len(state["eligible_ops"]))
            assert torch.isfinite(logits).all()
            assert value.shape == (1,)

    def test_padding_mask_matches_unpadded(self):
        """El forward con padding+máscara equivale al forward sin padding."""
        net = PolicyValueNetV2()
        net.eval()
        env = _make_env(get_test_3x3_interval())
        state = env.reset()
        op_f, glob_f = StateEncoder(env).encode(state)
        n = op_f.shape[0]

        with torch.no_grad():
            logits_plain, value_plain = net(
                torch.from_numpy(op_f).unsqueeze(0),
                torch.from_numpy(glob_f).unsqueeze(0))

            padded = np.zeros((1, n + 4, OP_FEATURE_DIM), dtype=np.float32)
            padded[0, :n] = op_f
            mask = np.zeros((1, n + 4), dtype=bool)
            mask[0, :n] = True
            logits_pad, value_pad = net(
                torch.from_numpy(padded),
                torch.from_numpy(glob_f).unsqueeze(0),
                torch.from_numpy(mask))

        assert torch.allclose(logits_plain[0], logits_pad[0, :n], atol=1e-5)
        assert torch.isinf(logits_pad[0, n:]).all()
        assert torch.allclose(value_plain, value_pad, atol=1e-5)


class TestAttentionPhase2:

    def test_zero_layers_matches_base_architecture(self):
        """Con 0 capas de atención, la red es la arquitectura base exacta."""
        base = PolicyValueNetV2()
        attn0 = PolicyValueNetV2(num_attention_layers=0)
        assert (sum(p.numel() for p in base.parameters())
                == sum(p.numel() for p in attn0.parameters()))

    def test_attention_size_invariance(self):
        """La misma red con atención procesa cualquier tamaño de problema."""
        net = PolicyValueNetV2(num_attention_layers=2)
        for problem in (get_test_3x3_interval(), get_ft10_interval_problem()):
            env = _make_env(problem)
            state = env.reset()
            op_f, glob_f = StateEncoder(env).encode(state)
            logits, value = net(torch.from_numpy(op_f).unsqueeze(0),
                                torch.from_numpy(glob_f).unsqueeze(0))
            assert logits.shape == (1, len(state["eligible_ops"]))
            assert torch.isfinite(logits).all()

    def test_attention_padding_mask_equivalence(self):
        """El padding enmascarado no altera los logits de las ops reales."""
        net = PolicyValueNetV2(num_attention_layers=2)
        net.eval()
        env = _make_env(get_test_3x3_interval())
        state = env.reset()
        op_f, glob_f = StateEncoder(env).encode(state)
        n = op_f.shape[0]

        with torch.no_grad():
            logits_plain, value_plain = net(
                torch.from_numpy(op_f).unsqueeze(0),
                torch.from_numpy(glob_f).unsqueeze(0))

            padded = np.zeros((1, n + 5, OP_FEATURE_DIM), dtype=np.float32)
            padded[0, :n] = op_f
            mask = np.zeros((1, n + 5), dtype=bool)
            mask[0, :n] = True
            logits_pad, value_pad = net(
                torch.from_numpy(padded),
                torch.from_numpy(glob_f).unsqueeze(0),
                torch.from_numpy(mask))

        assert torch.allclose(logits_plain[0], logits_pad[0, :n], atol=1e-5)
        assert torch.allclose(value_plain, value_pad, atol=1e-5)

    def test_attention_training_cycle(self):
        env = _make_env(get_test_3x3_interval())
        agent = AgentV2(env, seed=1, attention_layers=2,
                        update_every_episodes=2, greedy_eval_every=4)
        agent.train(episodes=4)
        assert agent.best_makespan < float("inf")
        assert len(agent.buffer) == 0


class TestAgentV2:

    def test_actions_valid_and_episode_completes(self):
        env = _make_env(get_test_3x3_interval())
        agent = AgentV2(env, seed=1)
        state = env.reset()
        done = False
        steps = 0
        while not done:
            action, log_prob, aux = agent.select_action(state, training=True)
            assert action is not None
            assert 0 <= action < len(state["eligible_ops"])
            state, _, done, _ = env.step(action)
            steps += 1
        assert steps == env.num_jobs * env.num_machines

    def test_training_cycle_runs_and_learns_signal(self):
        """Un ciclo corto de entrenamiento corre sin errores y trackea el mejor."""
        env = _make_env(get_test_3x3_interval())
        agent = AgentV2(env, seed=1, update_every_episodes=2, greedy_eval_every=4)
        agent.train(episodes=6)
        assert agent.total_episodes == 6
        assert len(agent.training_makespan_history) == 6
        assert agent.best_makespan < float("inf")
        assert agent.best_model_state is not None
        assert len(agent.buffer) == 0  # sin gradientes parciales pendientes
        assert len(agent.training_losses["policy"]) >= 3

    def test_weight_transfer_between_problem_sizes(self):
        """La transferencia de pesos entre tamaños distintos funciona (v1 no podía)."""
        env_small = _make_env(get_test_3x3_interval())
        env_big = _make_env(get_ft10_interval_problem())
        a = AgentV2(env_small, seed=1)
        b = AgentV2(env_big, seed=2)
        b.policy.load_state_dict(a.policy.state_dict())  # misma vía que el pipeline
        mk, schedule, history, _ = b.evaluate_policy(n_samples=2)
        assert mk < float("inf")
        assert len(schedule) == env_big.num_jobs * env_big.num_machines

    def test_checkpoint_roundtrip(self, tmp_path):
        env = _make_env(get_test_3x3_interval())
        agent = AgentV2(env, seed=1)
        agent.train(episodes=2)
        path = str(tmp_path / "v2.pt")
        agent.save_checkpoint(path)

        fresh = AgentV2(_make_env(get_test_3x3_interval()), seed=3)
        fresh.load_checkpoint(path)
        for p1, p2 in zip(agent.network.parameters(), fresh.network.parameters()):
            assert torch.equal(p1, p2)
