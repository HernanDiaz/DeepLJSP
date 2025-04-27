
"""
Implementación de la estrategia de recompensa adaptativa.
"""

from typing import Dict, Optional, Any

from jobshop_rl.rewards.base import RewardStrategy
from jobshop_rl.rewards.components.makespan import MakespanRewardComponent
from jobshop_rl.rewards.components.idle_time import IdleTimeRewardComponent
from jobshop_rl.rewards.components.criticality import CriticalityRewardComponent
from jobshop_rl.rewards.components.balance import BalanceRewardComponent
from jobshop_rl.rewards.components.progress import ProgressRewardComponent
from jobshop_rl.rewards.components.local_improvement import LocalImprovementRewardComponent

class AdaptiveRewardStrategy(RewardStrategy):
    """Estrategia de recompensa que se adapta automáticamente a las características del problema"""
    
    def __init__(self, problem_analysis: Optional[Dict] = None, **kwargs):
        super().__init__(problem_analysis)
        
        # Pesos iniciales
        self.weights = {
            "makespan_weight": 1.0,
            "idle_weight": 0.2,
            "critical_weight": 0.1,
            "balance_weight": 0.05,
            "progress_weight": 0.2,
            "local_improvement_weight": 0.15
        }
        
        # Sobrescribir pesos con parámetros proporcionados
        for key, value in kwargs.items():
            if key in self.weights:
                self.weights[key] = value
        
        # Adaptar pesos si hay análisis del problema
        if problem_analysis:
            self._adapt_weights()
        
        # Inicializar componentes con pesos adaptados
        self.components = [
            MakespanRewardComponent(self.weights["makespan_weight"], problem_analysis),
            IdleTimeRewardComponent(self.weights["idle_weight"], problem_analysis),
            CriticalityRewardComponent(self.weights["critical_weight"], problem_analysis),
            BalanceRewardComponent(self.weights["balance_weight"], problem_analysis),
            ProgressRewardComponent(self.weights["progress_weight"]),
            LocalImprovementRewardComponent(self.weights["local_improvement_weight"], problem_analysis)
        ]
    
    def _adapt_weights(self) -> None:
        """Adapta los pesos según las características del problema"""
        pa = self.problem_analysis
        
        # Ajustar peso de balance si hay alta varianza en cargas de máquinas
        if pa.get("load_variance", 0) > pa.get("avg_op_duration", 1) * 2:
            self.weights["balance_weight"] = 0.1
            
        # Ajustar peso de idle si hay un claro bottleneck
        if pa.get("bottleneck_ratio", 1) > 1.3:
            self.weights["idle_weight"] = 0.3
            
        # Si la estructura de la red crítica es densa, enfatizar más la criticidad
        if pa.get("avg_critical_path_length", 0) > pa.get("num_machines", 10) * 0.7:
            self.weights["critical_weight"] = 0.15
    
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa combinando todos los componentes"""
        if action is None or not state['eligible_ops']:
            return 0
            
        total_reward = 0
        for component in self.components:
            total_reward += component.calculate(env, state, next_state, action, done, info)
            
        return total_reward
    
    def reset(self) -> None:
        """Reinicia el estado interno de todos los componentes"""
        for component in self.components:
            component.reset()
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Actualiza el análisis del problema y readapta los pesos"""
        super().set_problem_analysis(problem_analysis)
        
        # Readaptar pesos
        self._adapt_weights()
        
        # Actualizar componentes
        self.components[0].weight = self.weights["makespan_weight"]
        self.components[1].weight = self.weights["idle_weight"]
        self.components[2].weight = self.weights["critical_weight"]
        self.components[3].weight = self.weights["balance_weight"]
        self.components[4].weight = self.weights["progress_weight"]
        self.components[5].weight = self.weights["local_improvement_weight"]
        
        # Propagar análisis a componentes
        for component in self.components:
            component.set_problem_analysis(problem_analysis)
