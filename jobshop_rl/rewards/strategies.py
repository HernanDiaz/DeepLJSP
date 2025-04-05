"""
Estrategias de recompensa para el entorno de Job Shop Scheduling.
Implementa el patrón Strategy para diferentes funciones de recompensa.
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any, Optional

class RewardStrategy(ABC):
    """Estrategia base para el cálculo de recompensas (patrón Strategy)"""

    @abstractmethod
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en el estado, la acción y el resultado"""
        pass

class BasicRewardStrategy(RewardStrategy):
    """Estrategia de recompensa básica: solo recompensa al final basada en makespan"""

    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        if done:
            makespan = max(env.job_completion_time)
            optimal_makespan = 930  # Óptimo para FT10
            reward = -makespan / 100  # Escalar la recompensa

            # Bonus por acercarse al óptimo
            if makespan <= optimal_makespan:
                reward += 10
            return reward
        return 0

class AdvancedRewardStrategy(RewardStrategy):
    """Estrategia de recompensa avanzada con señales intermedias"""

    def __init__(self, makespan_weight=1.0, idle_weight=0.2, critical_weight=0.1, balance_weight=0.05,
                 progress_weight=0.2, local_improvement_weight=0.15):
        self.makespan_weight = makespan_weight
        self.idle_weight = idle_weight
        self.critical_weight = critical_weight
        self.balance_weight = balance_weight
        self.progress_weight = progress_weight
        self.local_improvement_weight = local_improvement_weight

        # Estado para seguimiento de mejora relativa
        self.last_projected_makespan = float('inf')
        self.best_seen_makespan = float('inf')

    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        reward = 0

        # Si la acción fue None o no hay operaciones elegibles
        if action is None or not state['eligible_ops']:
            return 0

        # Obtener información de la operación programada
        job_id = state['eligible_ops'][action]
        op_idx = state['job_status'][job_id]
        machine = env.sequences[job_id][op_idx]

        # Calcular tiempos
        start_time = max(state['job_completion_time'][job_id],
                         state['machine_completion_time'][machine])
        duration = env.durations[job_id][op_idx]
        end_time = start_time + duration

        # 1. Recompensa final basada en makespan
        if done:
            makespan = max(env.job_completion_time)
            optimal_makespan = 930  # Óptimo para FT10
            makespan_reward = -makespan / 100

            # Bonus por acercarse al óptimo
            if makespan <= optimal_makespan:
                makespan_reward += 10

            reward += self.makespan_weight * makespan_reward

            # Actualizar mejor makespan visto
            if makespan < self.best_seen_makespan:
                self.best_seen_makespan = makespan

        # 2. Penalización por tiempo de inactividad en máquinas
        idle_time = 0
        if start_time > state['machine_completion_time'][machine]:
            idle_time = start_time - state['machine_completion_time'][machine]
        idle_reward = -idle_time / 50  # Normalizado
        reward += self.idle_weight * idle_reward

        # 3. Recompensa por priorizar operaciones críticas
        remaining_ops = env.num_machines - op_idx - 1
        if remaining_ops > 0:
            remaining_time = sum(env.durations[job_id][op_idx+1:])
            criticality = remaining_time / 100  # Normalizado
            reward += self.critical_weight * criticality

        # 4. Penalización por desequilibrio de carga
        completion_times = [t for t in next_state['machine_completion_time'] if t > 0]
        if completion_times:
            std_dev = np.std(completion_times)
            balance_reward = -std_dev / 50
            reward += self.balance_weight * balance_reward

        # 5. Recompensa por progreso general
        if not done:
            # Calcular proporción de operaciones completadas
            total_ops = env.num_jobs * env.num_machines
            completed_ops = sum(state['job_status'])
            progress = completed_ops / total_ops

            # Recompensa pequeña por avanzar en el plan
            progress_reward = progress * 0.1
            reward += self.progress_weight * progress_reward

        # 6. Recompensa por mejora local (proyección de makespan)
        current_projected_makespan = max(next_state['machine_completion_time'])

        # Mejora relativa desde la última acción
        if self.last_projected_makespan != float('inf'):
            improvement = (self.last_projected_makespan - current_projected_makespan)
            # Normalizar y solo recompensar mejoras
            if improvement > 0:
                local_reward = improvement / 100
                reward += self.local_improvement_weight * local_reward

        self.last_projected_makespan = current_projected_makespan

        return reward

    def reset(self):
        """Reinicia el estado interno de la estrategia"""
        self.last_projected_makespan = float('inf')
        # No reiniciamos best_seen_makespan para mantener referencia entre episodios

# Fábrica de estrategias de recompensa
class CombinedRewardStrategy(RewardStrategy):
    """Estrategia de recompensa que combina múltiples estrategias con pesos"""

    def __init__(self, strategies_with_weights: List[Tuple[RewardStrategy, float]]):
        self.strategies_with_weights = strategies_with_weights

    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        total_reward = 0
        for strategy, weight in self.strategies_with_weights:
            reward = strategy.calculate_reward(env, state, next_state, action, done, info)
            total_reward += weight * reward
        return total_reward

class RewardStrategyFactory:
    """Fábrica para crear estrategias de recompensa (patrón Factory)"""

    @staticmethod
    def create_strategy(strategy_type: str, **kwargs) -> RewardStrategy:
        """Crea una estrategia de recompensa basada en el tipo especificado"""
        if strategy_type.lower() == "basic":
            return BasicRewardStrategy()
        elif strategy_type.lower() == "advanced":
            return AdvancedRewardStrategy(**kwargs)
        elif strategy_type.lower() == "combined":
            # Ejemplo: combined_params = {"strategies": [("basic", 0.3), ("advanced", 0.7, {advanced_params})]}
            strategies_with_weights = []

            for strat_config in kwargs.get("strategies", []):
                if len(strat_config) >= 2:
                    strat_name = strat_config[0]
                    strat_weight = strat_config[1]
                    strat_params = strat_config[2] if len(strat_config) > 2 else {}

                    strategy = RewardStrategyFactory.create_strategy(strat_name, **strat_params)
                    strategies_with_weights.append((strategy, strat_weight))

            return CombinedRewardStrategy(strategies_with_weights)
        else:
            raise ValueError(f"Estrategia de recompensa desconocida: {strategy_type}")
