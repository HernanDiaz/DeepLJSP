"""
Test de equivalencia y velocidad de la evaluación batcheada (batched_eval).

1. EQUIVALENCIA (bloqueante): el greedy batcheado (n=1) debe reproducir
   EXACTAMENTE el makespan del greedy secuencial en cada instancia probada,
   en CPU. En GPU se admite discrepancia solo si hay empates de argmax
   (se reporta).
2. CALIDAD: best-of-64 batcheado vs secuencial (misma política, distinta
   secuencia RNG) deben dar makespans similares (no bit-idénticos).
3. VELOCIDAD: speedup del batcheado (CPU y GPU) vs secuencial.

Uso: python scripts/test_batched_eval.py [checkpoint]
"""

import sys
import time

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch

from jobshop_rl.agents_v2 import AgentV2
from jobshop_rl.agents_v2.batched_eval import evaluate_policy_batched
from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.experiments.factory import EnvironmentFactory

CHECKPOINT = sys.argv[1] if len(sys.argv) > 1 else \
    "models/v2_final_deepsets_1000ep_seed2.pt"
INSTANCES = ["int__tai15_15_01", "int__tai20_15_05", "int__tai30_20_04",
             "int__tai50_20_01"]
N = 64


def make_agent(pid):
    env = EnvironmentFactory.create_from_problem(
        PROBLEM_REGISTRY[pid](), "adaptive", seed=1)
    agent = AgentV2(env, seed=1)
    agent.load_checkpoint(CHECKPOINT)
    return agent


def main():
    torch.set_num_threads(2)
    has_cuda = torch.cuda.is_available()
    print(f"CUDA: {has_cuda} | checkpoint: {CHECKPOINT}\n")

    print("== 1. EQUIVALENCIA greedy (bloqueante) ==")
    all_ok = True
    for pid in INSTANCES:
        agent = make_agent(pid)
        mk_seq, _, _, _ = agent.evaluate_policy(n_samples=1)
        mk_cpu, _, _, _ = evaluate_policy_batched(agent, 1, device="cpu")
        ok = mk_seq == mk_cpu
        line = f"  {pid}: seq={mk_seq:.0f} batch_cpu={mk_cpu:.0f} {'OK' if ok else 'FALLO'}"
        if has_cuda:
            mk_gpu, _, _, _ = evaluate_policy_batched(agent, 1, device="cuda")
            line += f" batch_gpu={mk_gpu:.0f} {'OK' if mk_seq == mk_gpu else 'DIF(gpu)'}"
        print(line, flush=True)
        all_ok = all_ok and ok
    if not all_ok:
        print("\nEQUIVALENCIA GREEDY ROTA - no usar la ruta batcheada.")
        sys.exit(1)

    print("\n== 2/3. CALIDAD Y VELOCIDAD best-of-%d ==" % N)
    print(f"  {'instancia':<18} {'seq':>14} {'batch CPU':>14} "
          f"{'batch GPU':>14} {'spdup CPU':>10} {'spdup GPU':>10}")
    for pid in INSTANCES:
        agent = make_agent(pid)
        t0 = time.time()
        mk_seq, _, _, _ = agent.evaluate_policy(n_samples=N)
        t_seq = time.time() - t0

        mk_cpu, _, _, t_cpu = evaluate_policy_batched(
            agent, N, device="cpu", seed=1)
        if has_cuda:
            mk_gpu, _, _, t_gpu = evaluate_policy_batched(
                agent, N, device="cuda", seed=1)
            gpu_txt = f"{mk_gpu:>6.0f} {t_gpu:>6.1f}s"
            gpu_spd = f"{t_seq/t_gpu:>9.1f}x"
        else:
            gpu_txt, gpu_spd = " " * 14, " " * 10
        print(f"  {pid:<18} {mk_seq:>6.0f} {t_seq:>6.1f}s "
              f"{mk_cpu:>6.0f} {t_cpu:>6.1f}s {gpu_txt} "
              f"{t_seq/t_cpu:>9.1f}x {gpu_spd}", flush=True)

    print("\nHecho. Criterio: equivalencia greedy OK + makespans best-of-N "
          "comparables (+-ruido de muestreo) + speedup > 1.")


if __name__ == "__main__":
    main()
