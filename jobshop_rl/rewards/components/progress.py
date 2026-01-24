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
        """
        Calcula la recompensa por completar una operación.
        
        Da una recompensa fija normalizada por operación completada,
        en lugar de basarse en el progreso total acumulado.
        """
        if action is None or not state['eligible_ops'] or done:
            return 0
        
        # Recompensa fija por completar una operación
        # Normalizada para que completar todas las operaciones sume a 1.0
        total_ops = env.num_jobs * env.num_machines
        reward_per_op = 1.0 / total_ops if total_ops > 0 else 0
        
        return self.weight * reward_per_op
