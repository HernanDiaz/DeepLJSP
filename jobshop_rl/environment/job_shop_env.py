"""
Entorno de Job Shop Scheduling para aprendizaje por refuerzo.

Soporta tanto problemas determinísticos (escalares) como problemas con
incertidumbre (intervalos) en los tiempos de procesamiento.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from typing import List, Dict, Tuple, Optional, Any, Union
from copy import deepcopy

from jobshop_rl.models.data_models import SchedulingStep, OperationFeatures
from jobshop_rl.models.interval import Interval, ensure_interval
from jobshop_rl.rewards.base import RewardStrategy
from jobshop_rl.rewards.strategies.basic import BasicRewardStrategy
from jobshop_rl.utils.problem_analyzer import ProblemAnalyzer, MakespanBoundCalculator
from jobshop_rl.utils.seed_utils import set_random_seed


class JobShopEnv:
    """
    Entorno para el problema de Job Shop Scheduling.
    
    Soporta tanto tiempos de procesamiento determinísticos (escalares)
    como inciertos (intervalos).
    """

    def __init__(self, num_jobs: int, num_machines: int,
                 sequences: List[List[int]], 
                 durations: List[List[Union[int, Interval]]],
                 reward_strategy: Optional[RewardStrategy] = None,
                 problem_id: Optional[str] = None,
                 seed: Optional[int] = None):
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.sequences = sequences
        self.durations = durations
        self.problem_id = problem_id
        
        # Detect if problem has intervals
        self.has_intervals = self._check_for_intervals()
        
        # Analizar el problema para obtener límites y características
        self.problem_analysis = ProblemAnalyzer.analyze_problem(sequences, durations)
        
        # Seleccionar la estrategia de recompensa
        if reward_strategy is None:
            # Crear estrategia por defecto con el análisis del problema
            self.reward_strategy = BasicRewardStrategy(problem_analysis=self.problem_analysis)
        else:
            self.reward_strategy = reward_strategy
            # Si la estrategia no tiene el análisis, proporcionarlo
            if hasattr(reward_strategy, 'problem_analysis') and reward_strategy.problem_analysis is None:
                reward_strategy.problem_analysis = self.problem_analysis
                # Si tiene método para adaptar, llamarlo
                if hasattr(reward_strategy, '_adapt_scales_to_problem') and callable(getattr(reward_strategy, '_adapt_scales_to_problem')):
                    reward_strategy._adapt_scales_to_problem()

        # Establecer semilla para reproducibilidad usando la utilidad centralizada
        set_random_seed(seed)

        self.reset()
    
    def _check_for_intervals(self) -> bool:
        """
        Verifica si el problema contiene intervalos.
        
        Returns:
            True si hay al menos un intervalo no degenerado
        """
        for job_durations in self.durations:
            for duration in job_durations:
                if isinstance(duration, Interval) and not duration.is_degenerate:
                    return True
        return False

    def set_reward_strategy(self, strategy: RewardStrategy):
        """Cambia la estrategia de recompensa (patrón Strategy)"""
        self.reward_strategy = strategy
        
        # Si la estrategia no tiene el análisis, proporcionarlo
        if hasattr(strategy, 'problem_analysis') and strategy.problem_analysis is None:
            strategy.problem_analysis = self.problem_analysis
            # Si tiene método para adaptar, llamarlo
            if hasattr(strategy, '_adapt_scales_to_problem') and callable(getattr(strategy, '_adapt_scales_to_problem')):
                strategy._adapt_scales_to_problem()

        # Si la estrategia tiene un método reset, llamarlo
        if hasattr(strategy, 'reset') and callable(getattr(strategy, 'reset')):
            strategy.reset()

    def reset(self) -> Dict:
        """Reinicia el entorno a su estado inicial"""
        # Reiniciar el estado interno de la estrategia de recompensa para que
        # componentes con estado (p.ej. last_projected_makespan) no filtren
        # información del episodio anterior
        if hasattr(self.reward_strategy, 'reset') and callable(getattr(self.reward_strategy, 'reset')):
            self.reward_strategy.reset()

        # Estado de cada trabajo: posición actual en su secuencia
        self.job_status = [0] * self.num_jobs

        # Tiempo de finalización para cada trabajo y máquina
        # Use Interval(0,0) for interval problems, 0 for scalar
        if self.has_intervals:
            self.job_completion_time = [Interval(0, 0) for _ in range(self.num_jobs)]
            self.machine_completion_time = [Interval(0, 0) for _ in range(self.num_machines)]
        else:
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
        """
        Extrae características para todas las operaciones elegibles.
        
        Para problemas con intervalos, retorna 10 características por operación.
        Para problemas escalares, retorna 7 características (backward compatible).
        
        Args:
            state: Estado actual del entorno
            
        Returns:
            Array de características (n_ops, 7) o (n_ops, 10)
        """
        features = []
        
        for job_id in state['eligible_ops']:
            op_idx = state['job_status'][job_id]
            machine = self.sequences[job_id][op_idx]
            duration = self.durations[job_id][op_idx]

            # Calculate earliest start using interval-aware max
            job_completion = state['job_completion_time'][job_id]
            machine_completion = state['machine_completion_time'][machine]
            
            if self.has_intervals:
                # Use Interval.max for interval arithmetic
                earliest_start = Interval.max(job_completion, machine_completion)
            else:
                # Regular max for scalars
                earliest_start = max(job_completion, machine_completion)

            # Calculate remaining time for this job
            remaining_ops = self.num_machines - op_idx - 1
            
            if remaining_ops > 0:
                remaining_durations = self.durations[job_id][op_idx+1:]
                if self.has_intervals:
                    # Sum intervals
                    remaining_time = sum(remaining_durations, Interval(0, 0))
                else:
                    # Sum scalars
                    remaining_time = sum(remaining_durations)
            else:
                if self.has_intervals:
                    remaining_time = Interval(0, 0)
                else:
                    remaining_time = 0

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
            # Return appropriate size based on problem type
            feature_dim = 10 if self.has_intervals else 7
            return np.zeros((0, feature_dim))

        return np.array(features)

    def step(self, action_idx: int) -> Tuple[Dict, float, bool, Dict]:
        """
        Ejecuta un paso en el entorno basado en la acción seleccionada.
        
        Usa aritmética de intervalos cuando el problema tiene incertidumbre.
        
        Args:
            action_idx: Índice de la acción (operación elegible) a ejecutar
            
        Returns:
            next_state: Nuevo estado después de la acción
            reward: Recompensa obtenida
            done: Si el episodio ha terminado
            info: Información adicional
        """
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

        # Calcular tiempos usando aritmética apropiada
        if self.has_intervals:
            # Interval arithmetic
            start_time = Interval.max(
                self.job_completion_time[job_id],
                self.machine_completion_time[machine]
            )
            end_time = start_time + duration  # Interval addition
        else:
            # Scalar arithmetic (backward compatible)
            start_time = max(
                self.job_completion_time[job_id],
                self.machine_completion_time[machine]
            )
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
        if self.has_intervals:
            # Use lexicographic max for intervals
            current_makespan = max(self.job_completion_time)
        else:
            current_makespan = max(self.job_completion_time)
        
        self.makespan_history.append(current_makespan)

        # Verificar si terminó
        done = all(status == self.num_machines for status in self.job_status)

        # Obtener nuevo estado
        next_state = self._get_state()

        # Información adicional (makespan)
        if done:
            if self.has_intervals:
                info = {'makespan': max(self.job_completion_time)}
            else:
                info = {'makespan': max(self.job_completion_time)}
        else:
            info = {'makespan': None}

        # Calcular recompensa usando la estrategia actual
        reward = self.reward_strategy.calculate_reward(
            self, current_state, next_state, action_idx, done, info
        )

        return next_state, reward, done, info

    def render_schedule(self, title="Job Shop Schedule", schedule=None):
        """
        Visualiza la programación actual o una programación proporcionada.
        
        Para problemas con intervalos, usa un gráfico de Gantt con paralelogramos
        que muestran la incertidumbre temporal.
        
        Args:
            title: Título del gráfico
            schedule: Programación a visualizar (None = usar historial actual)
            
        Returns:
            Figura de matplotlib
        """
        if schedule is None:
            schedule = self.schedule_history
            
        if not schedule:
            return None
        
        # Detect if schedule contains intervals
        has_interval_times = any(
            isinstance(op['start'], Interval) or isinstance(op['end'], Interval)
            for op in schedule
        )
        
        if has_interval_times:
            return self._render_interval_schedule(title, schedule)
        else:
            return self._render_scalar_schedule(title, schedule)
    
    def _render_scalar_schedule(self, title: str, schedule: List[Dict]) -> plt.Figure:
        """
        Renderiza programación con tiempos escalares (determinísticos).
        
        Gráfico de Gantt tradicional con barras rectangulares.
        """
        plt.figure(figsize=(20, 10))  # Aumentar tamaño para mejor visibilidad
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
                    f"J{op['job']},O{op['operation']}",
                    va='center',
                    ha='center',
                    color='white',
                    fontweight='bold',
                    fontsize=9)

        plt.yticks(range(self.num_machines), [f'M{i}' for i in range(self.num_machines)])
        plt.xlabel('Tiempo')
        plt.ylabel('Máquina')
        
        makespan = max(op['end'] for op in schedule)
        plt.title(f"{title}\nMakespan: {makespan}")
        plt.grid(axis='x', alpha=0.3)
        plt.xlim(left=0)

        return plt.gcf()
    
    def _render_interval_schedule(self, title: str, schedule: List[Dict]) -> plt.Figure:
        """
        Renderiza programación con tiempos de intervalo (inciertos).
        
        Usa paralelogramos para mostrar la incertidumbre temporal:
        - Borde frontal: diagonal de (start_lower, y_bottom) a (start_upper, y_top)
        - Borde trasero: diagonal de (end_upper, y_top) a (end_lower, y_bottom)
        
        Esto muestra visualmente:
        - Mejor caso: rectángulo en la parte inferior
        - Peor caso: rectángulo en la parte superior
        - Incertidumbre: inclinación del paralelogramo
        """
        plt.figure(figsize=(20, 10))  # Aumentar tamaño para mejor visibilidad
        colors = plt.cm.tab10(np.linspace(0, 1, self.num_jobs))
        
        for op in schedule:
            machine = op['machine']
            job = op['job']
            
            # Extract interval bounds - manejar tanto objetos Interval como dicts
            start = op['start']
            end = op['end']
            
            # Convertir a valores numéricos
            if isinstance(start, dict):
                # Viene del JSON: {"lower": x, "upper": y}
                start_lower = float(start['lower'])
                start_upper = float(start['upper'])
            elif isinstance(start, Interval):
                # Es un objeto Interval
                start_lower = float(start.lower)
                start_upper = float(start.upper)
            else:
                # Es un escalar
                start_lower = float(start)
                start_upper = float(start)
            
            if isinstance(end, dict):
                # Viene del JSON: {"lower": x, "upper": y}
                end_lower = float(end['lower'])
                end_upper = float(end['upper'])
            elif isinstance(end, Interval):
                # Es un objeto Interval
                end_lower = float(end.lower)
                end_upper = float(end.upper)
            else:
                # Es un escalar
                end_lower = float(end)
                end_upper = float(end)
            
            # Machine position (y coordinate)
            y_bottom = machine - 0.4  # Bottom of bar
            y_top = machine + 0.4     # Top of bar
            
            # Define parallelogram vertices (counterclockwise)
            # Start edge: from (start_lower, bottom) to (start_upper, top)
            # End edge: from (end_upper, top) to (end_lower, bottom)
            vertices = [
                (start_lower, y_bottom),  # Bottom-left (best start)
                (start_upper, y_top),     # Top-left (worst start)
                (end_upper, y_top),       # Top-right (worst end)
                (end_lower, y_bottom),    # Bottom-right (best end)
            ]
            
            # Create polygon
            polygon = Polygon(vertices, 
                            facecolor=colors[job],  # Usar facecolor en lugar de color
                            alpha=0.7,
                            edgecolor='black',
                            linewidth=1.5)
            plt.gca().add_patch(polygon)
            
            # Add label at center
            center_x = (start_lower + start_upper + end_lower + end_upper) / 4
            center_y = machine
            
            plt.text(center_x, center_y,
                    f"J{job},O{op['operation']}",
                    va='center', ha='center',
                    color='white', fontweight='bold',
                    fontsize=9)
        
        # Formatting
        plt.yticks(range(self.num_machines), 
                  [f'M{i}' for i in range(self.num_machines)])
        plt.xlabel('Tiempo')
        plt.ylabel('Máquina')
        
        # Get makespan (interval)
        if schedule:
            # Calculate makespan from schedule - manejar diferentes formatos
            end_times = []
            max_time_value = 0
            
            for op in schedule:
                end = op['end']
                if isinstance(end, dict):
                    # Formato JSON
                    end_interval = Interval(end['lower'], end['upper'])
                    end_times.append(end_interval)
                    max_time_value = max(max_time_value, end['upper'])
                elif isinstance(end, Interval):
                    # Objeto Interval
                    end_times.append(end)
                    max_time_value = max(max_time_value, end.upper)
                else:
                    # Escalar
                    end_interval = Interval(float(end), float(end))
                    end_times.append(end_interval)
                    max_time_value = max(max_time_value, float(end))
            
            # Find max using lexicographic ordering
            makespan = max(end_times)
            
            if isinstance(makespan, Interval):
                title_text = f"{title}\nMakespan: [{makespan.lower:.1f}, {makespan.upper:.1f}]"
            else:
                title_text = f"{title}\nMakespan: {makespan}"
        else:
            title_text = title
            max_time_value = 100  # default
            
        plt.title(title_text, fontsize=14, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # Establecer límites del eje X con margen
        plt.xlim(left=-max_time_value * 0.02, right=max_time_value * 1.05)
        plt.ylim(bottom=-0.5, top=self.num_machines - 0.5)
        
        # Add legend explaining visualization with better formatting
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='gray', alpha=0.5, label='Área = Rango de incertidumbre'),
            plt.Line2D([0], [0], color='black', linewidth=2, label='Bordes = Límites temporales')
        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=10)
        
        # Añadir nota explicativa más clara
        textstr = ("Interpretación de paralelogramos:\n"
                   "• Borde inferior → Mejor escenario (mínimo tiempo)\n"
                   "• Borde superior → Peor escenario (máximo tiempo)\n"
                   "• Inclinación → Propagación de incertidumbre")
        plt.text(0.02, 0.02, textstr, transform=plt.gca().transAxes,
                fontsize=9, verticalalignment='bottom',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
        
        plt.tight_layout()
        return plt.gcf()

    def plot_makespan_history(self, makespan_history=None, title="Evolución del Makespan", reference_value=None):
        """
        Visualiza la evolución del makespan durante un episodio.
        
        Para problemas con intervalos, muestra bandas de incertidumbre.
        """
        if makespan_history is None:
            makespan_history = self.makespan_history
        
        if not makespan_history:
            return None
            
        plt.figure(figsize=(12, 6))
        
        # Check if makespans are intervals
        has_interval_makespans = any(isinstance(m, Interval) for m in makespan_history)
        
        if has_interval_makespans:
            # Plot with uncertainty bands
            steps = list(range(len(makespan_history)))
            lower_bounds = []
            upper_bounds = []
            midpoints = []
            
            for m in makespan_history:
                if isinstance(m, Interval):
                    lower_bounds.append(m.lower)
                    upper_bounds.append(m.upper)
                    midpoints.append(m.midpoint)
                else:
                    lower_bounds.append(m)
                    upper_bounds.append(m)
                    midpoints.append(m)
            
            # Plot uncertainty band
            plt.fill_between(steps, lower_bounds, upper_bounds, 
                           alpha=0.3, label='Rango de incertidumbre')
            
            # Plot midpoint
            plt.plot(steps, midpoints, '-o', label='Punto medio', linewidth=2)
            
            # Plot bounds
            plt.plot(steps, lower_bounds, '--', alpha=0.7, label='Mejor caso')
            plt.plot(steps, upper_bounds, '--', alpha=0.7, label='Peor caso')
        else:
            # Plot regular line for scalar makespans
            plt.plot(makespan_history, '-o')
        
        # Si no se proporciona un valor de referencia, usar el límite inferior del problema
        if reference_value is None:
            if 'best_lower_bound' in self.problem_analysis:
                reference_value = self.problem_analysis['best_lower_bound']
                if isinstance(reference_value, Interval):
                    # Use upper bound of lower bound for conservative reference
                    ref_val = reference_value.upper
                    reference_label = f'Límite inferior: [{reference_value.lower:.1f}, {reference_value.upper:.1f}]'
                else:
                    ref_val = reference_value
                    reference_label = f'Límite inferior: {reference_value}'
            elif 'lower_bounds' in self.problem_analysis:
                bounds = self.problem_analysis['lower_bounds'].values()
                best_bound = max(bounds)
                if isinstance(best_bound, Interval):
                    ref_val = best_bound.upper
                    reference_label = f'Límite inferior: [{best_bound.lower:.1f}, {best_bound.upper:.1f}]'
                else:
                    ref_val = best_bound
                    reference_label = f'Límite inferior: {best_bound}'
            else:
                ref_val = None
                reference_label = None
        else:
            if isinstance(reference_value, Interval):
                ref_val = reference_value.upper
                reference_label = f'Referencia: [{reference_value.lower:.1f}, {reference_value.upper:.1f}]'
            else:
                ref_val = reference_value
                reference_label = f'Referencia: {reference_value}'
            
        # Dibujar línea de referencia si está disponible
        if ref_val is not None:
            plt.axhline(y=ref_val, color='r', linestyle='--', label=reference_label)
            
        plt.xlabel('Pasos')
        plt.ylabel('Makespan')
        plt.title(title)
        plt.legend()
        plt.grid(True)

        return plt.gcf()
