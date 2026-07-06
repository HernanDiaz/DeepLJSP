"""
Evaluador de estrategias heurísticas y agentes de RL para Job Shop Scheduling.
"""

import logging
import time
from typing import Dict, List, Tuple, Any, Optional
from copy import deepcopy

from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.heuristics.strategies import (
    HeuristicStrategy, SPTHeuristic, LPTHeuristic,
    MORHeuristic, MWKRHeuristic, RandomHeuristic, ORToolsHeuristic,
    GTHeuristic,
)
from jobshop_rl.agents.ppo_agent import PPOAgent

logger = logging.getLogger("JobShopRL.Evaluator")

class HeuristicEvaluator:
    """Evaluador para comparar diferentes heurísticas"""

    def __init__(self, env: JobShopEnv):
        """
        Inicializa el evaluador.
        
        Args:
            env: Entorno de Job Shop Scheduling
        """
        self.env = env
        self.results = {}
        self.execution_times = {}

    @staticmethod
    def _run_episode(env_copy: JobShopEnv, heuristic: HeuristicStrategy) -> float:
        """
        Ejecuta un episodio completo con la heurística dada sobre el entorno
        (ya copiado) y devuelve el makespan escalar (peor caso para intervalos).
        """
        from jobshop_rl.models.interval import Interval

        state = env_copy.reset()
        done = False

        while not done:
            eligible_ops = state['eligible_ops']
            if not eligible_ops:
                break

            features = env_copy.get_features(state)

            action_idx = heuristic.select_action(eligible_ops, features)
            action_idx = min(action_idx, len(eligible_ops)-1)  # Asegurar índice válido
            next_state, _, done, _ = env_copy.step(action_idx)
            state = next_state

        if done:
            max_time = max(env_copy.job_completion_time)
            # Manejar tanto valores escalares como intervalos
            if isinstance(max_time, Interval):
                return float(max_time.upper)  # Usar límite superior
            return float(max_time)
        return float('inf')

    def evaluate_heuristic(self, heuristic: HeuristicStrategy, name: str) -> Tuple[float, float]:
        """
        Evalúa una heurística específica.

        Args:
            heuristic: Estrategia heurística a evaluar
            name: Nombre identificativo de la heurística

        Returns:
            Tupla con (makespan resultante, tiempo de ejecución en segundos)
        """
        # Crear una copia del entorno para no afectar a otros experimentos
        env_copy = deepcopy(self.env)

        start_time = time.time()
        makespan = self._run_episode(env_copy, heuristic)
        execution_time = time.time() - start_time

        self.results[name] = makespan
        self.execution_times[name] = execution_time

        logger.info(f"{name}: Makespan = {makespan}, Tiempo = {execution_time:.4f} segundos")
        return makespan, execution_time

    def evaluate_random(self, n_runs: int = 250) -> Tuple[float, float]:
        """
        Evalúa la heurística aleatoria con múltiples ejecuciones para obtener
        una estimación representativa (una sola ejecución aleatoria es puro azar).

        Args:
            n_runs: Número de soluciones aleatorias a generar

        Returns:
            Tupla con (makespan medio, mejor makespan)
        """
        heuristic = RandomHeuristic()
        env_copy = deepcopy(self.env)

        start_time = time.time()
        makespans = [self._run_episode(env_copy, heuristic) for _ in range(n_runs)]
        execution_time = time.time() - start_time

        mean_makespan = sum(makespans) / len(makespans)
        best_makespan = min(makespans)

        self.results["Random (media)"] = mean_makespan
        self.results["Random (mejor)"] = best_makespan
        self.execution_times["Random (media)"] = execution_time
        self.execution_times["Random (mejor)"] = execution_time

        logger.info(f"Random ({n_runs} soluciones): media = {mean_makespan:.1f}, "
                    f"mejor = {best_makespan:.1f}, Tiempo total = {execution_time:.4f} segundos")
        return mean_makespan, best_makespan

    def evaluate_all(self, return_times: bool = False, use_ortools: bool = True) -> Dict[str, float]:
        """
        Evalúa todas las heurísticas comunes.
        
        Args:
            return_times: Si es True, devuelve también los tiempos de ejecución
            use_ortools: Si es True, intenta evaluar OR-Tools (se salta automáticamente si hay intervalos)
            
        Returns:
            Si return_times es False: diccionario de makespan
            Si return_times es True: tupla (diccionario de makespan, diccionario de tiempos)
        """
        self.evaluate_heuristic(SPTHeuristic(), "SPT")
        self.evaluate_heuristic(LPTHeuristic(), "LPT")
        self.evaluate_heuristic(MORHeuristic(), "MOR")
        self.evaluate_heuristic(MWKRHeuristic(), "MWKR")
        # G&T (schedules activos) con desempate MWKR: el baseline
        # determinista más fuerte conocido en este benchmark
        self.evaluate_heuristic(GTHeuristic("mwkr"), "GT-MWKR")
        # Random se evalúa con múltiples soluciones (media y mejor)
        self.evaluate_random(n_runs=250)
        
        # Evaluar con OR-Tools solo si no hay intervalos
        if use_ortools:
            # Detectar si el problema tiene intervalos
            from jobshop_rl.models.interval import Interval
            has_intervals = False
            
            try:
                # Verificar si las duraciones contienen intervalos
                if hasattr(self.env, 'durations') and self.env.durations is not None:
                    for job_durations in self.env.durations:
                        for duration in job_durations:
                            if isinstance(duration, Interval) and not duration.is_degenerate:
                                has_intervals = True
                                break
                        if has_intervals:
                            break
            except Exception as e:
                logger.warning(f"Error al detectar intervalos: {str(e)}")
            
            if has_intervals:
                logger.info("Problema con intervalos detectado. OR-Tools no puede resolver problemas con incertidumbre en duraciones. Saltando evaluación de OR-Tools.")
            else:
                try:
                    # Obtener datos del problema del entorno
                    sequences = self.env.sequences
                    durations = self.env.durations
                    
                    # Verificar si las características están disponibles
                    if not hasattr(self.env, 'sequences') or not hasattr(self.env, 'durations'):
                        logger.warning("El entorno no proporciona secuencias o duraciones. No se puede evaluar OR-Tools.")
                        return self.results
                        
                    if sequences is None or durations is None:
                        logger.warning("Secuencias o duraciones son None. No se puede evaluar OR-Tools.")
                        return self.results
                    
                    # Crear instancia de OR-Tools con tiempo límite de 60 segundos
                    ortools_heuristic = ORToolsHeuristic(sequences, durations, time_limit_seconds=60)
                    
                    # Si OR-Tools está disponible, evaluar esta heurística
                    if hasattr(ortools_heuristic, 'ortools_available') and ortools_heuristic.ortools_available:
                        logger.info("Evaluando heurística OR-Tools (tiempo límite: 60 segundos)...")
                        self.evaluate_heuristic(ortools_heuristic, "OR-Tools")
                        logger.info(f"Evaluación de OR-Tools completada. Makespan: {self.results.get('OR-Tools', 'N/A')}")
                    else:
                        logger.warning("OR-Tools no disponible. Saltando la evaluación de OR-Tools.")
                        logger.warning("Para instalar OR-Tools: pip install ortools")
                except ImportError as e:
                    logger.error(f"Error al importar OR-Tools: {str(e)}")
                    logger.warning("Para instalar OR-Tools: pip install ortools")
                except Exception as e:
                    logger.error(f"Error al evaluar OR-Tools: {str(e)}")
                    import traceback
                    logger.error(traceback.format_exc())
        
        if return_times:
            return self.results, self.execution_times
        else:
            return self.results

    def compare_with_agent(self, agent_makespan: float) -> Dict[str, float]:
        """
        Compara el rendimiento del agente con las heurísticas.
        
        Args:
            agent_makespan: Mejor makespan obtenido por el agente
            
        Returns:
            Diccionario con el porcentaje de mejora respecto a cada heurística
        """
        comparison = {}
        for name, makespan in self.results.items():
            improvement = (makespan - agent_makespan) / makespan * 100
            comparison[name] = improvement
            logger.info(f"vs {name}: {improvement:.2f}% de mejora")
        return comparison

class AgentEvaluator:
    """Evaluador para experimentos con agentes de RL"""
    
    def __init__(self, env: JobShopEnv, agent: PPOAgent):
        """
        Inicializa el evaluador.
        
        Args:
            env: Entorno de Job Shop Scheduling
            agent: Agente de RL a evaluar
        """
        self.env = env
        self.agent = agent
        self.results = {}
        
    def evaluate_on_problem(self, problem_data: Dict[str, Any], problem_name: str) -> Dict[str, Any]:
        """
        Evalúa el agente en un problema específico.
        
        Args:
            problem_data: Datos del problema (secuencias, duraciones, etc.)
            problem_name: Nombre identificativo del problema
            
        Returns:
            Diccionario con los resultados de la evaluación
        """
        from jobshop_rl.experiments.factory import EnvironmentFactory

        # Configurar entorno para este problema
        test_env = EnvironmentFactory.create_from_problem(problem_data)
        
        # Crear un agente para evaluación que comparta el modelo con el agente original
        test_agent = PPOAgent(test_env)
        test_agent.policy.load_state_dict(self.agent.policy.state_dict())
        test_agent.value.load_state_dict(self.agent.value.state_dict())
        
        # Evaluar
        makespan, schedule, makespan_history, _ = test_agent.evaluate_policy()
        
        # Calcular desviación del óptimo si está disponible
        optimal = problem_data.get('optimal_makespan', None)
        if optimal:
            gap = (makespan - optimal) / optimal * 100
        else:
            gap = None
            
        # Guardar resultados
        result = {
            'problem': problem_name,
            'makespan': makespan,
            'schedule': schedule,
            'makespan_history': makespan_history,
            'optimal': optimal,
            'gap': gap
        }
        
        self.results[problem_name] = result
        
        return result
    
    def evaluate_on_problems(self, problems: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Evalúa el agente en múltiples problemas.
        
        Args:
            problems: Lista de diccionarios con datos de problemas
            
        Returns:
            Diccionario con los resultados para cada problema
        """
        for i, problem in enumerate(problems):
            problem_name = problem.get('name', f"problem_{i}")
            logger.info(f"Evaluando agente en problema: {problem_name}")
            self.evaluate_on_problem(problem, problem_name)
            
        # Calcular estadísticas globales
        if self.results:
            avg_makespan = sum(r['makespan'] for r in self.results.values()) / len(self.results)
            logger.info(f"Makespan promedio en {len(self.results)} problemas: {avg_makespan:.2f}")
            
            # Calcular gap promedio si hay valores óptimos
            gaps = [r['gap'] for r in self.results.values() if r['gap'] is not None]
            if gaps:
                avg_gap = sum(gaps) / len(gaps)
                logger.info(f"Desviación promedio del óptimo: {avg_gap:.2f}%")
        
        return self.results
    
    def compare_with_heuristics(self, problems: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """
        Compara el agente con heurísticas clásicas en múltiples problemas.
        
        Args:
            problems: Lista de diccionarios con datos de problemas
            
        Returns:
            Diccionario con comparativas para cada problema
        """
        from jobshop_rl.experiments.factory import EnvironmentFactory

        comparisons = {}
        
        for i, problem in enumerate(problems):
            problem_name = problem.get('name', f"problem_{i}")
            logger.info(f"Comparando en problema: {problem_name}")
            
            # Evaluar el agente si aún no se ha hecho
            if problem_name not in self.results:
                self.evaluate_on_problem(problem, problem_name)
                
            agent_makespan = self.results[problem_name]['makespan']
            
            # Evaluar heurísticas
            test_env = EnvironmentFactory.create_from_problem(problem)
            evaluator = HeuristicEvaluator(test_env)
            heuristic_results = evaluator.evaluate_all()
            
            # Comparar
            comparison = evaluator.compare_with_agent(agent_makespan)
            comparisons[problem_name] = comparison
            
        return comparisons
