"""
Componente de recompensa basado en el progreso general del plan.
"""

from typing import Dict, Optional

from jobshop_rl.rewards.base import RewardComponent

class ProgressRewardComponent(RewardComponent):
    """Calcula la recompensa basada en el progreso general del plan"""
    
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
