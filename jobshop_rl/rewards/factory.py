"""
Fábrica y registro para estrategias de recompensa.
"""

import inspect
from typing import Dict, Optional, Any, List, Tuple, Type

from jobshop_rl.rewards.base import RewardStrategy
from jobshop_rl.rewards.strategies.basic import BasicRewardStrategy
from jobshop_rl.rewards.strategies.advanced import AdvancedRewardStrategy
from jobshop_rl.rewards.strategies.adaptive import AdaptiveRewardStrategy
from jobshop_rl.rewards.strategies.combined import CombinedRewardStrategy
from jobshop_rl.rewards.strategies.sparse import SparseRewardStrategy

class RewardStrategyRegistry:
    """Registro de estrategias de recompensa disponibles"""
    
    # Diccionario que mapea nombres de estrategias a sus clases
    _strategies = {
        "basic": BasicRewardStrategy,
        "advanced": AdvancedRewardStrategy,
        "adaptive": AdaptiveRewardStrategy,
        "combined": CombinedRewardStrategy,
        "sparse": SparseRewardStrategy
    }
    
    @classmethod
    def register(cls, name: str, strategy_class: Type[RewardStrategy]) -> None:
        """Registra una nueva estrategia de recompensa"""
        cls._strategies[name.lower()] = strategy_class
    
    @classmethod
    def get_strategy_class(cls, name: str) -> Type[RewardStrategy]:
        """Obtiene la clase de estrategia por nombre"""
        if name.lower() not in cls._strategies:
            raise ValueError(f"Estrategia de recompensa desconocida: {name}")
        return cls._strategies[name.lower()]
    
    @classmethod
    def list_strategies(cls) -> List[str]:
        """Lista todas las estrategias registradas"""
        return list(cls._strategies.keys())

class RewardStrategyFactory:
    """Fábrica para crear estrategias de recompensa (patrón Factory)"""
    
    @staticmethod
    def create_strategy(strategy_type: str, problem_analysis: Optional[Dict] = None, **kwargs) -> RewardStrategy:
        """Crea una estrategia de recompensa basada en el tipo especificado"""
        strategy_class = RewardStrategyRegistry.get_strategy_class(strategy_type)
        
        # Caso especial para estrategia combinada
        if strategy_type.lower() == "combined":
            # Crear las sub-estrategias
            strategies_with_weights = []
            
            for strat_config in kwargs.get("strategies", []):
                if len(strat_config) >= 2:
                    strat_name = strat_config[0]
                    strat_weight = strat_config[1]
                    strat_params = strat_config[2] if len(strat_config) > 2 else {}
                    # problem_analysis se pasa como keyword explícito; no debe
                    # duplicarse dentro de strat_params
                    strat_params.pop('problem_analysis', None)

                    strategy = RewardStrategyFactory.create_strategy(
                        strat_name,
                        problem_analysis=problem_analysis,
                        **strat_params
                    )
                    strategies_with_weights.append((strategy, strat_weight))
            
            return CombinedRewardStrategy(strategies_with_weights, problem_analysis)
        elif strategy_type.lower() == "adaptive":
            # Para la estrategia adaptativa, filtramos los parámetros que realmente usa
            valid_params = {
                "makespan_weight", "idle_weight", "critical_weight", 
                "balance_weight", "progress_weight", "local_improvement_weight"
            }
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_params}
            return strategy_class(problem_analysis=problem_analysis, **filtered_kwargs)
        else:
            # Filtrar los kwargs a los parámetros que el constructor de la
            # estrategia realmente acepta (main.py siempre envía los pesos,
            # pero no todas las estrategias los usan)
            signature = inspect.signature(strategy_class.__init__)
            accepts_var_keyword = any(
                p.kind == inspect.Parameter.VAR_KEYWORD
                for p in signature.parameters.values()
            )
            if not accepts_var_keyword:
                kwargs = {k: v for k, v in kwargs.items() if k in signature.parameters}
            return strategy_class(problem_analysis=problem_analysis, **kwargs)
