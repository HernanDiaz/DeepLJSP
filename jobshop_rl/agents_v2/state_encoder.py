"""
Representación de estado invariante al tamaño para agents_v2.

Todas las features son adimensionales: los tiempos se dividen por el límite
inferior (LB) del problema y las anchuras de incertidumbre se expresan como
ratios. Las dimensiones (OP_FEATURE_DIM por operación elegible y
GLOBAL_FEATURE_DIM del contexto) son FIJAS, independientes de num_jobs y
num_machines — la misma red sirve para cualquier tamaño de problema.
"""

import numpy as np

from jobshop_rl.models.interval import Interval

OP_FEATURE_DIM = 16
GLOBAL_FEATURE_DIM = 12
_EPS = 1e-8


def _lo(x) -> float:
    return float(x.lower) if isinstance(x, Interval) else float(x)


def _up(x) -> float:
    return float(x.upper) if isinstance(x, Interval) else float(x)


class StateEncoder:
    """Convierte el estado del entorno en (features_por_op, features_globales)."""

    def __init__(self, env):
        self.env = env

        # Factor de normalización temporal: LB del problema (peor caso si es
        # intervalo). Toda feature temporal se divide por él.
        analysis = getattr(env, "problem_analysis", None) or {}
        lb = analysis.get("best_lower_bound")
        lb = _up(lb) if lb is not None else 0.0
        self.lb = lb if lb > 0 else 1.0

    def encode(self, state):
        """
        Args:
            state: dict del entorno (eligible_ops, job_status,
                job_completion_time, machine_completion_time)

        Returns:
            (op_feats (n_elegibles, OP_FEATURE_DIM) float32,
             global_feats (GLOBAL_FEATURE_DIM,) float32)
        """
        env, lb = self.env, self.lb
        eligible = state["eligible_ops"]
        job_status = state["job_status"]
        jc = state["job_completion_time"]
        mc = state["machine_completion_time"]
        nj, nm = env.num_jobs, env.num_machines

        # Agregados sobre lo NO programado: carga restante por máquina y por
        # job (peor caso) e incertidumbre pendiente
        machine_load = [0.0] * nm
        job_rem_total = [0.0] * nj
        pending_width = 0.0
        pending_mid = 0.0
        scheduled = 0
        for j in range(nj):
            k0 = job_status[j]
            scheduled += k0
            for k in range(k0, nm):
                d = env.durations[j][k]
                lo, up = _lo(d), _up(d)
                machine_load[env.sequences[j][k]] += up
                job_rem_total[j] += up
                pending_width += up - lo
                pending_mid += (up + lo) / 2.0

        total_ops = nj * nm
        mean_load = sum(machine_load) / nm

        # earliest start (peor caso) de cada elegible, para la holgura relativa
        est_up_by_job = {}
        for j in eligible:
            k = job_status[j]
            m = env.sequences[j][k]
            est_up_by_job[j] = max(_up(jc[j]), _up(mc[m]))
        min_est_up = min(est_up_by_job.values()) if est_up_by_job else 0.0

        rows = []
        for j in eligible:
            k = job_status[j]
            m = env.sequences[j][k]
            d = env.durations[j][k]

            d_lo, d_up = _lo(d), _up(d)
            d_mid = (d_lo + d_up) / 2.0

            est_lo = max(_lo(jc[j]), _lo(mc[m]))
            est_up = est_up_by_job[j]
            est_mid = (est_lo + est_up) / 2.0

            rem_lo = sum(_lo(env.durations[j][q]) for q in range(k + 1, nm))
            rem_up = sum(_up(env.durations[j][q]) for q in range(k + 1, nm))

            rows.append([
                # duración (2) + incertidumbre relativa (1)
                d_lo / lb,
                d_up / lb,
                (d_up - d_lo) / max(d_mid, _EPS),
                # earliest start (2) + incertidumbre relativa (1)
                est_lo / lb,
                est_up / lb,
                (est_up - est_lo) / max(est_mid, _EPS) if est_up > 0 else 0.0,
                # trabajo restante del job tras esta op (2)
                rem_lo / lb,
                rem_up / lb,
                # posición en el job (2)
                (nm - k - 1) / nm,
                k / nm,
                # contexto de la máquina (3)
                machine_load[m] / lb,
                max(0.0, _up(jc[j]) - _up(mc[m])) / lb,  # hueco que dejaría en la máquina
                machine_load[m] / max(mean_load, _EPS),   # congestión relativa
                # holgura frente a la elegible más temprana (1)
                (est_up - min_est_up) / lb,
                # estado absoluto normalizado (2)
                _up(mc[m]) / lb,
                _up(jc[j]) / lb,
            ])

        if rows:
            op_feats = np.asarray(rows, dtype=np.float32)
        else:
            op_feats = np.zeros((0, OP_FEATURE_DIM), dtype=np.float32)

        mc_up = [_up(x) for x in mc]
        global_feats = np.asarray([
            scheduled / total_ops,
            (max(mc_up) if mc_up else 0.0) / lb,          # makespan parcial
            float(np.mean(mc_up)) / lb,
            float(np.std(mc_up)) / lb,
            mean_load / lb,
            max(machine_load) / lb,
            float(np.std(machine_load)) / lb,
            float(np.mean(job_rem_total)) / lb,
            max(job_rem_total) / lb,
            len(eligible) / nj,
            pending_width / max(pending_mid, _EPS),        # incertidumbre pendiente
            sum(machine_load) / (lb * nm),                 # carga total restante
        ], dtype=np.float32)

        return op_feats, global_feats
