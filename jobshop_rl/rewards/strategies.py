"""
Estrategias de recompensa para el entorno de Job Shop Scheduling.
Implementa el patrón Strategy para diferentes funciones de recompensa.
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any, Optional

from jobshop_rl.utils.problem_analyzer import ProblemAnalyzer, MakespanBoundCalculator

class RewardStrategy(ABC):
    """Estrategia base para el cálculo de recompensas (patrón Strategy)"""

    @abstractmethod
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en el estado, la acción y el resultado"""
        pass

class BasicRewardStrategy(RewardStrategy):
    """Estrategia de recompensa básica: solo recompensa al final basada en makespan"""
    
    def __init__(self, problem_analysis: Optional[Dict] = None):
        self.problem_analysis = problem_analysis
        self.best_seen_makespan = float('inf')
        
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        if done:
            makespan = max(env.job_completion_time)
            
            # Actualizar mejor makespan visto
            if makespan < self.best_seen_makespan:
                self.best_seen_makespan = makespan
                
            # Verificar si tenemos análisis del problema
            if not self.problem_analysis and hasattr(env, 'problem_analysis'):
                self.problem_analysis = env.problem_analysis
                
            # Si no tenemos análisis, calcularlo ahora
            if not self.problem_analysis:
                self.problem_analysis = ProblemAnalyzer.analyze_problem(env.sequences, env.durations)
            
            # Usar límite inferior como referencia en lugar de valor hardcodeado
            lower_bound = self.problem_analysis.get('best_lower_bound', 0)
            makespan_scale = max(100, lower_bound / 10)  # Escalar según el problema
            
            reward = -makespan / makespan_scale  # Escalar la recompensa
            
            # Bonus por acercarse al óptimo o límite inferior
            if lower_bound > 0:
                gap = (makespan - lower_bound) / lower_bound
                if gap <= 0.05:  # Dentro del 5% del límite inferior
                    reward += 10 * (1 - gap * 10)  # Mayor bonus cuanto más cerca
            
            return reward
        return 0
    
    def reset(self):
        """Reinicia el estado interno de la estrategia"""
        pass  # Mantenemos el mejor makespan visto, ya que es útil como referencia

class AdvancedRewardStrategy(RewardStrategy):
    """Estrategia de recompensa avanzada con señales intermedias"""

    def __init__(self, problem_analysis: Optional[Dict] = None, makespan_weight=1.0, idle_weight=0.2, 
                 critical_weight=0.1, balance_weight=0.05, progress_weight=0.2, 
                 local_improvement_weight=0.15):
        self.problem_analysis = problem_analysis
        self.makespan_weight = makespan_weight
        self.idle_weight = idle_weight
        self.critical_weight = critical_weight
        self.balance_weight = balance_weight
        self.progress_weight = progress_weight
        self.local_improvement_weight = local_improvement_weight

        # Estado para seguimiento de mejora relativa
        self.last_projected_makespan = float('inf')
        self.best_seen_makespan = float('inf')
        
        # Calculamos escalas basadas en el análisis del problema
        self.makespan_scale = 100.0
        self.idle_scale = 50.0
        self.critical_scale = 100.0
        self.balance_scale = 50.0
        
        # Si tenemos análisis del problema, ajustar escalas
        if problem_analysis:
            self._adapt_scales_to_problem()
            
    def _adapt_scales_to_problem(self):
        """Adapta las escalas de recompensa según las características del problema"""
        pa = self.problem_analysis
        
        # Ajustar escala de makespan según el límite inferior
        if 'best_lower_bound' in pa and pa['best_lower_bound'] > 0:
            self.makespan_scale = max(100, pa['best_lower_bound'] / 10)
            
        # Ajustar escala de idle basada en duración promedio
        if 'avg_op_duration' in pa and pa['avg_op_duration'] > 0:
            self.idle_scale = max(10, pa['avg_op_duration'] * 2)
            
        # Ajustar escala crítica según el tiempo total de trabajo
        if 'total_work' in pa and pa['total_work'] > 0:
            self.critical_scale = max(50, pa['total_work'] / (pa['num_jobs'] * 2))
            
        # Ajustar balance según el valor máximo esperado de std_dev
        if 'machine_loads' in pa:
            expected_std = np.std(pa['machine_loads']) * 1.5
            self.balance_scale = max(10, expected_std)
            
    def _ensure_problem_analysis(self, env):
        """Asegura que tenemos análisis del problema disponible"""
        if not self.problem_analysis:
            # Intentar obtener del entorno
            if hasattr(env, 'problem_analysis'):
                self.problem_analysis = env.problem_analysis
            # Si no está disponible, calcularlo
            else:
                self.problem_analysis = ProblemAnalyzer.analyze_problem(env.sequences, env.durations)
                
            # Actualizar escalas basadas en el nuevo análisis
            self._adapt_scales_to_problem()

    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        # Asegurar que tenemos análisis del problema
        self._ensure_problem_analysis(env)
        
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
            # Usar límites del análisis del problema en lugar de valor hardcodeado
            lower_bound = self.problem_analysis.get('best_lower_bound', 0)
            makespan_reward = -makespan / self.makespan_scale

            # Bonus por acercarse al límite inferior
            if lower_bound > 0:
                gap = (makespan - lower_bound) / lower_bound
                if gap <= 0.05:  # Dentro del 5% del límite inferior
                    makespan_reward += 10 * (1 - gap * 10)

            reward += self.makespan_weight * makespan_reward

            # Actualizar mejor makespan visto
            if makespan < self.best_seen_makespan:
                self.best_seen_makespan = makespan

        # 2. Penalización por tiempo de inactividad en máquinas
        idle_time = 0
        if start_time > state['machine_completion_time'][machine]:
            idle_time = start_time - state['machine_completion_time'][machine]
        idle_reward = -idle_time / self.idle_scale  # Normalizado usando escala adaptada
        reward += self.idle_weight * idle_reward

        # 3. Recompensa por priorizar operaciones críticas
        remaining_ops = env.num_machines - op_idx - 1
        if remaining_ops > 0:
            remaining_time = sum(env.durations[job_id][op_idx+1:])
            criticality = remaining_time / self.critical_scale  # Normalizado usando escala adaptada
            reward += self.critical_weight * criticality

        # 4. Penalización por desequilibrio de carga
        completion_times = [t for t in next_state['machine_completion_time'] if t > 0]
        if completion_times:
            std_dev = np.std(completion_times)
            balance_reward = -std_dev / self.balance_scale  # Normalizado usando escala adaptada
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
                # Normalizar usando escala adaptada
                local_reward = improvement / (self.makespan_scale / 10)
                reward += self.local_improvement_weight * local_reward

        self.last_projected_makespan = current_projected_makespan

        return reward

    def reset(self):
        """Reinicia el estado interno de la estrategia"""
        self.last_projected_makespan = float('inf')
        # No reiniciamos best_seen_makespan para mantener referencia entre episodios

class AdaptiveRewardStrategy(RewardStrategy):
    """Estrategia de recompensa que se adapta automáticamente a las características del problema"""
    
    def __init__(self, problem_analysis: Optional[Dict] = None):
        self.problem_analysis = problem_analysis
        self.baseline_makespan = None
        self.best_seen_makespan = float('inf')
        self.last_projected_makespan = float('inf')
        
        # Pesos de recompensa adaptados a las características del problema
        self.weights = {
            "makespan_weight": 1.0,
            "idle_weight": 0.2,
            "critical_weight": 0.1,
            "balance_weight": 0.05,
            "progress_weight": 0.2,
            "local_improvement_weight": 0.15,
            "relative_improvement_weight": 0.3
        }
        
        # Escalas para normalización
        self.scales = {
            "makespan": 100.0,
            "idle": 50.0,
            "critical": 100.0,
            "balance": 50.0
        }
        
        if problem_analysis:
            self._adapt_to_problem()
    
    def _adapt_to_problem(self):
        """Adapta los pesos de recompensa a las características del problema"""
        pa = self.problem_analysis
        
        # Adaptar pesos según las características del problema
        # Si hay alta varianza en cargas de máquinas, aumentar balance_weight
        if pa.get("load_variance", 0) > pa.get("avg_op_duration", 1) * 2:
            self.weights["balance_weight"] = 0.1
            
        # Si hay un claro bottleneck, aumentar idle_weight para evitar tiempos muertos
        if pa.get("bottleneck_ratio", 1) > 1.3:
            self.weights["idle_weight"] = 0.3
            
        # Establecer una línea base para comparación (podría ser el mejor límite inferior)
        self.baseline_makespan = pa.get("best_lower_bound")
        
        # Configurar escalas basadas en características del problema
        if 'best_lower_bound' in pa and pa['best_lower_bound'] > 0:
            self.scales["makespan"] = max(100, pa['best_lower_bound'] / 10)
            
        if 'avg_op_duration' in pa and pa['avg_op_duration'] > 0:
            self.scales["idle"] = max(10, pa['avg_op_duration'] * 2)
            
        if 'total_work' in pa and pa['total_work'] > 0:
            self.scales["critical"] = max(50, pa['total_work'] / (pa['num_jobs'] * 2))
            
        if 'machine_loads' in pa:
            expected_std = np.std(pa['machine_loads']) * 1.5
            self.scales["balance"] = max(10, expected_std)
    
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        # Si no tenemos el análisis del problema, hacerlo ahora
        if not self.problem_analysis:
            if hasattr(env, 'problem_analysis'):
                self.problem_analysis = env.problem_analysis
            else:
                self.problem_analysis = ProblemAnalyzer.analyze_problem(
                    env.sequences, env.durations
                )
            self._adapt_to_problem()
        
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
        
        # 1. Recompensa final al terminar
        if done:
            makespan = max(env.job_completion_time)
            self.best_seen_makespan = min(self.best_seen_makespan, makespan)
            
            # Recompensa basada en límite inferior
            if self.baseline_makespan:
                gap = (makespan - self.baseline_makespan) / self.baseline_makespan
                
                # Recompensa por proximidad al límite inferior
                makespan_reward = -gap * 10  # Penalización proporcional a la distancia 
                reward += self.weights["makespan_weight"] * makespan_reward
                
                # Bonus por estar muy cerca del límite
                if gap <= 0.05:  # Dentro del 5% del límite inferior
                    reward += 5 * (1 - gap * 10)  # Bonus proporcional
            else:
                # Si no tenemos límite inferior, usar mejora relativa al mejor visto
                relative_improvement = 1.0
                if self.last_projected_makespan != float('inf'):
                    relative_improvement = (self.last_projected_makespan - makespan) / self.last_projected_makespan
                reward += self.weights["relative_improvement_weight"] * relative_improvement * 10
        
        # 2. Penalización por tiempo de inactividad en máquinas
        idle_time = 0
        if start_time > state['machine_completion_time'][machine]:
            idle_time = start_time - state['machine_completion_time'][machine]
        idle_reward = -idle_time / self.scales["idle"]
        reward += self.weights["idle_weight"] * idle_reward

        # 3. Recompensa por priorizar operaciones críticas
        remaining_ops = env.num_machines - op_idx - 1
        if remaining_ops > 0:
            remaining_time = sum(env.durations[job_id][op_idx+1:])
            criticality = remaining_time / self.scales["critical"]
            reward += self.weights["critical_weight"] * criticality

        # 4. Penalización por desequilibrio de carga
        completion_times = [t for t in next_state['machine_completion_time'] if t > 0]
        if completion_times:
            std_dev = np.std(completion_times)
            balance_reward = -std_dev / self.scales["balance"]
            reward += self.weights["balance_weight"] * balance_reward

        # 5. Recompensa por progreso general
        if not done:
            # Calcular proporción de operaciones completadas
            total_ops = env.num_jobs * env.num_machines
            completed_ops = sum(state['job_status'])
            progress = completed_ops / total_ops

            # Recompensa pequeña por avanzar en el plan
            progress_reward = progress * 0.1
            reward += self.weights["progress_weight"] * progress_reward

        # 6. Recompensa por mejora local (proyección de makespan)
        current_projected_makespan = max(next_state['machine_completion_time'])

        # Mejora relativa desde la última acción
        if self.last_projected_makespan != float('inf'):
            improvement = (self.last_projected_makespan - current_projected_makespan)
            # Normalizar y solo recompensar mejoras
            if improvement > 0:
                local_reward = improvement / (self.scales["makespan"] / 10)
                reward += self.weights["local_improvement_weight"] * local_reward

        self.last_projected_makespan = current_projected_makespan

        return reward
        
    def reset(self):
        """Reinicia el estado interno de la estrategia"""
        self.last_projected_makespan = float('inf')

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
        
    def reset(self):
        """Reinicia el estado interno de todas las estrategias"""
        for strategy, _ in self.strategies_with_weights:
            if hasattr(strategy, 'reset') and callable(getattr(strategy, 'reset')):
                strategy.reset()

class RewardStrategyFactory:
    """Fábrica para crear estrategias de recompensa (patrón Factory)"""

    @staticmethod
    def create_strategy(strategy_type: str, problem_analysis: Optional[Dict] = None, **kwargs) -> RewardStrategy:
        """Crea una estrategia de recompensa basada en el tipo especificado"""
        if strategy_type.lower() == "basic":
            return BasicRewardStrategy(problem_analysis=problem_analysis)
        elif strategy_type.lower() == "advanced":
            return AdvancedRewardStrategy(problem_analysis=problem_analysis, **kwargs)
        elif strategy_type.lower() == "adaptive":
            return AdaptiveRewardStrategy(problem_analysis=problem_analysis)
        elif strategy_type.lower() == "combined":
            # Ejemplo: combined_params = {"strategies": [("basic", 0.3), ("advanced", 0.7, {advanced_params})]}
            strategies_with_weights = []

            for strat_config in kwargs.get("strategies", []):
                if len(strat_config) >= 2:
                    strat_name = strat_config[0]
                    strat_weight = strat_config[1]
                    strat_params = strat_config[2] if len(strat_config) > 2 else {}

                    # Pasar el problema_analysis a cada estrategia
                    if problem_analysis:
                        strat_params['problem_analysis'] = problem_analysis
                        
                    strategy = RewardStrategyFactory.create_strategy(strat_name, problem_analysis=problem_analysis, **strat_params)
                    strategies_with_weights.append((strategy, strat_weight))

            return CombinedRewardStrategy(strategies_with_weights)
        else:
            raise ValueError(f"Estrategia de recompensa desconocida: {strategy_type}")
