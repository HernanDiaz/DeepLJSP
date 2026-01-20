"""
Componente de recompensa basado en el progreso general del plan.

Este componente es independiente de los tiempos de procesamiento,
por lo que funciona igual para problemas determinísticos e intervalos.
"""

from typing import Dict, Optional

from jobshop_rl.rewards.base import RewardComponent


class ProgressRewardComponent(RewardComponent):
    """
    Calcula la recompensa basada en el progreso general del plan.
    
    No depende de valores de tiempo, solo del número de operaciones completadas.
    Compatible con problemas escalares e intervalos sin cambios.
    """
    
    def __init__(self, weight: float = 0.2):
        self.weight = weight
    
    def calculate(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en el progreso"""
        if action is None or not state['eligible_ops'] or done:
            return 0
        
        # Calcular proporción de operaciones completadas
        total_ops = env.num_jobs * env.num_machines
        completed_ops = sum(state['job_status'])
        progress = completed_ops / total_ops
        
        # Recompensa pequeña por avanzar en el plan
        progress_reward = progress * 0.1
        
        return self.weight * progress_reward
