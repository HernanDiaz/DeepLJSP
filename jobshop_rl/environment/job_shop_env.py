"""
Entorno de Job Shop Scheduling para aprendizaje por refuerzo.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional, Any
from copy import deepcopy

from jobshop_rl.models.data_models import SchedulingStep, OperationFeatures
from jobshop_rl.rewards.strategies import RewardStrategy, BasicRewardStrategy

class JobShopEnv:
    """Entorno para el problema de Job Shop Scheduling"""

    def __init__(self, num_jobs: int, num_machines: int,
                 sequences: List[List[int]], durations: List[List[int]],
                 reward_strategy: Optional[RewardStrategy] = None,
                 seed: Optional[int] = None):
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.sequences = sequences
        self.durations = durations
        self.reward_strategy = reward_strategy or BasicRewardStrategy()

        # Establecer semilla para reproducibilidad
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.reset()

    def set_reward_strategy(self, strategy: RewardStrategy):
        """Cambia la estrategia de recompensa (patrón Strategy)"""
        self.reward_strategy = strategy

        # Si la estrategia tiene un método reset, llamarlo
        if hasattr(self.reward_strategy, 'reset') and callable(getattr(self.reward_strategy, 'reset')):
            self.reward_strategy.reset()

    def reset(self) -> Dict:
        """Reinicia el entorno a su estado inicial"""
        # Estado de cada trabajo: posición actual en su secuencia
        self.job_status = [0] * self.num_jobs

        # Tiempo de finalización para cada trabajo y máquina
        self.job_completion_time = [0] * self.num_jobs
        self.machine_completion_time = [0] * self.num_machines

        # Operaciones ya programadas
        self.scheduled_ops = []

        # Operaciones elegibles
        self.eligible_ops = self._get_eligible_ops()

        # Historia para visualización
        self.schedule_history = []
        self.makespan_history = []

        return self._get_state()

    def _get_eligible_ops(self) -> List[int]:
        """Determina qué operaciones son elegibles para programar en el estado actual"""
        eligible = []
        for job_id in range(self.num_jobs):
            if self.job_status[job_id] < self.num_machines:
                # Si es la primera operación o la anterior ya está programada
                if self.job_status[job_id] == 0 or (job_id, self.job_status[job_id] - 1) in self.scheduled_ops:
                    eligible.append(job_id)
        return eligible

    def _get_state(self) -> Dict:
        """Obtiene el estado actual del entorno"""
        state = {
            'eligible_ops': self.eligible_ops,
            'job_status': self.job_status.copy(),
            'job_completion_time': self.job_completion_time.copy(),
            'machine_completion_time': self.machine_completion_time.copy(),
        }
        return state

    def get_features(self, state: Dict) -> np.ndarray:
        """Extrae características para todas las operaciones elegibles"""
        features = []
        for job_id in state['eligible_ops']:
            op_idx = state['job_status'][job_id]
            machine = self.sequences[job_id][op_idx]
            duration = self.durations[job_id][op_idx]

            earliest_start = max(state['job_completion_time'][job_id],
                                state['machine_completion_time'][machine])

            # Tiempo restante para este trabajo
            remaining_ops = self.num_machines - op_idx - 1
            remaining_time = sum(self.durations[job_id][op_idx+1:]) if remaining_ops > 0 else 0

            # Crear objeto de características
            op_features = OperationFeatures(
                job_id=job_id,
                op_idx=op_idx,
                machine=machine,
                duration=duration,
                earliest_start=earliest_start,
                remaining_time=remaining_time,
                remaining_ops=remaining_ops
            )

            features.append(op_features.to_array())

        if not features:
            return np.zeros((0, 7))

        return np.array(features)

    def step(self, action_idx: int) -> Tuple[Dict, float, bool, Dict]:
        """Ejecuta un paso en el entorno basado en la acción seleccionada"""
        if len(self.eligible_ops) == 0:
            return self._get_state(), 0, True, {}

        # Guardar el estado actual para el cálculo de recompensa
        current_state = self._get_state()

        # Seleccionar un trabajo
        job_id = self.eligible_ops[action_idx]

        # Obtener operación
        op_idx = self.job_status[job_id]
        machine = self.sequences[job_id][op_idx]
        duration = self.durations[job_id][op_idx]

        # Calcular tiempos
        start_time = max(self.job_completion_time[job_id],
                         self.machine_completion_time[machine])
        end_time = start_time + duration

        # Actualizar estado
        self.job_completion_time[job_id] = end_time
        self.machine_completion_time[machine] = end_time
        self.scheduled_ops.append((job_id, op_idx))
        self.job_status[job_id] += 1
        self.eligible_ops = self._get_eligible_ops()

        # Guardar historial
        scheduling_step = SchedulingStep(
            job=job_id,
            operation=op_idx,
            machine=machine,
            start=start_time,
            end=end_time
        )
        self.schedule_history.append(vars(scheduling_step))

        # Actualizar makespan history
        current_makespan = max(self.job_completion_time)
        self.makespan_history.append(current_makespan)

        # Verificar si terminó
        done = all(status == self.num_machines for status in self.job_status)

        # Obtener nuevo estado
        next_state = self._get_state()

        # Información adicional
        info = {'makespan': max(self.job_completion_time) if done else None}

        # Calcular recompensa usando la estrategia actual
        reward = self.reward_strategy.calculate_reward(
            self, current_state, next_state, action_idx, done, info
        )

        return next_state, reward, done, info

    def render_schedule(self, title="Job Shop Schedule", schedule=None):
        """Visualiza la programación actual o una programación proporcionada"""
        if schedule is None:
            schedule = self.schedule_history
            
        if not schedule:
            return None

        plt.figure(figsize=(15, 8))
        colors = plt.cm.tab10(np.linspace(0, 1, self.num_jobs))

        for op in schedule:
            plt.barh(op['machine'],
                    op['end'] - op['start'],
                    left=op['start'],
                    color=colors[op['job']],
                    edgecolor='black',
                    alpha=0.8)

            plt.text(op['start'] + (op['end'] - op['start'])/2,
                    op['machine'],
                    f"J{op['job']},{op['operation']}",
                    va='center',
                    ha='center',
                    color='white',
                    fontweight='bold')

        plt.yticks(range(self.num_machines), [f'M{i}' for i in range(self.num_machines)])
        plt.xlabel('Tiempo')
        plt.ylabel('Máquina')
        plt.title(f"{title}\nMakespan: {max(max(op['end'] for op in schedule), 0)}")
        plt.grid(axis='x')

        return plt.gcf()

    def plot_makespan_history(self, makespan_history=None, title="Evolución del Makespan"):
        """Visualiza la evolución del makespan durante un episodio"""
        if makespan_history is None:
            makespan_history = self.makespan_history
            
        plt.figure(figsize=(12, 6))
        plt.plot(makespan_history, '-o')
        plt.axhline(y=930, color='r', linestyle='--', label='Óptimo: 930')
        plt.xlabel('Pasos')
        plt.ylabel('Makespan')
        plt.title(title)
        plt.legend()
        plt.grid(True)

        return plt.gcf()
