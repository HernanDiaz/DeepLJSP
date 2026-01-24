"""
Script de diagnóstico para identificar por qué el agente 
planifica primero las operaciones de un trabajo entero con intervalos.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from typing import Dict, List, Tuple

from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.models.interval import Interval
from jobshop_rl.data import PROBLEM_REGISTRY


def print_features_comparison(env: JobShopEnv, state: Dict) -> None:
    """
    Imprime las características de todas las operaciones elegibles
    para analizar por qué el agente podría preferir ciertas acciones.
    """
    features = env.get_features(state)
    eligible_ops = state['eligible_ops']
    
    print("\n" + "="*80)
    print("ANÁLISIS DE CARACTERÍSTICAS DE OPERACIONES ELEGIBLES")
    print("="*80)
    
    if env.has_intervals:
        headers = ['Job', 'Op', 'Maq', 'Dur_L', 'Dur_U', 'Start_L', 'Start_U', 
                   'Rem_L', 'Rem_U', 'RemOps']
    else:
        headers = ['Job', 'Op', 'Maq', 'Duration', 'EarliestStart', 'RemTime', 'RemOps']
    
    print("\t".join(headers))
    print("-"*80)
    
    for i, job_id in enumerate(eligible_ops):
        feat = features[i]
        if env.has_intervals:
            print(f"{int(feat[0])}\t{int(feat[1])}\t{int(feat[2])}\t"
                  f"{feat[3]:.1f}\t{feat[4]:.1f}\t{feat[5]:.1f}\t{feat[6]:.1f}\t"
                  f"{feat[7]:.1f}\t{feat[8]:.1f}\t{int(feat[9])}")
        else:
            print(f"{int(feat[0])}\t{int(feat[1])}\t{int(feat[2])}\t"
                  f"{feat[3]:.1f}\t{feat[4]:.1f}\t{feat[5]:.1f}\t{int(feat[6])}")


def analyze_feature_statistics(env: JobShopEnv, state: Dict) -> Dict:
    """
    Analiza las estadísticas de las características para detectar problemas de escala.
    """
    features = env.get_features(state)
    
    if len(features) == 0:
        return {}
    
    stats = {}
    if env.has_intervals:
        feature_names = ['job_id', 'op_idx', 'machine', 
                        'duration_lower', 'duration_upper',
                        'earliest_start_lower', 'earliest_start_upper',
                        'remaining_time_lower', 'remaining_time_upper',
                        'remaining_ops']
    else:
        feature_names = ['job_id', 'op_idx', 'machine', 
                        'duration', 'earliest_start', 'remaining_time', 'remaining_ops']
    
    for i, name in enumerate(feature_names):
        col = features[:, i]
        stats[name] = {
            'min': col.min(),
            'max': col.max(),
            'mean': col.mean(),
            'std': col.std(),
            'range': col.max() - col.min()
        }
    
    return stats


def simulate_first_few_steps(env: JobShopEnv, strategy: str = 'sequential_job') -> None:
    """
    Simula los primeros pasos de planificación para ver cómo evolucionan
    las características.
    
    strategy: 
        'sequential_job' - planifica todas las ops de un trabajo primero
        'round_robin' - alterna entre trabajos
    """
    state = env.reset()
    
    print(f"\n{'='*80}")
    print(f"SIMULACIÓN CON ESTRATEGIA: {strategy}")
    print(f"{'='*80}")
    
    steps = min(10, env.num_jobs * env.num_machines)
    
    for step in range(steps):
        print(f"\n--- PASO {step + 1} ---")
        print_features_comparison(env, state)
        
        # Seleccionar acción según estrategia
        eligible = state['eligible_ops']
        if not eligible:
            break
            
        if strategy == 'sequential_job':
            # Siempre selecciona la primera operación elegible (mismo trabajo si es posible)
            action_idx = 0
        else:  # round_robin
            # Selecciona una operación de un trabajo diferente al anterior si es posible
            if step > 0 and len(eligible) > 1:
                action_idx = step % len(eligible)
            else:
                action_idx = 0
        
        selected_job = eligible[action_idx]
        print(f"\n>>> Acción seleccionada: Trabajo {selected_job}, "
              f"Operación {state['job_status'][selected_job]}")
        
        state, reward, done, info = env.step(action_idx)
        print(f">>> Recompensa: {reward:.4f}")
        
        if done:
            print(f"\n*** EPISODIO TERMINADO ***")
            print(f"Makespan final: {info.get('makespan', 'N/A')}")
            break


def compare_interval_widths(env: JobShopEnv) -> None:
    """
    Compara cómo evoluciona el ancho de los intervalos bajo diferentes estrategias.
    """
    if not env.has_intervals:
        print("Este análisis solo es relevante para problemas con intervalos.")
        return
    
    print("\n" + "="*80)
    print("COMPARACIÓN DE ANCHOS DE INTERVALOS")
    print("="*80)
    
    results = {}
    
    for strategy in ['sequential_job', 'round_robin']:
        state = env.reset()
        widths = []
        
        steps = env.num_jobs * env.num_machines
        for step in range(steps):
            eligible = state['eligible_ops']
            if not eligible:
                break
            
            features = env.get_features(state)
            
            # Calcular anchos de intervalos para cada característica
            # earliest_start_width = upper - lower
            start_widths = features[:, 6] - features[:, 5]  # indices 5,6 son earliest_start_lower/upper
            widths.append({
                'step': step,
                'avg_start_width': start_widths.mean(),
                'max_start_width': start_widths.max(),
            })
            
            if strategy == 'sequential_job':
                action_idx = 0
            else:
                action_idx = step % len(eligible) if len(eligible) > 1 else 0
            
            state, _, done, _ = env.step(action_idx)
            if done:
                break
        
        results[strategy] = widths
    
    # Mostrar comparación
    print("\nEvolución del ancho promedio de earliest_start:")
    print(f"{'Paso':<6} {'Sequential':<15} {'Round-Robin':<15}")
    print("-"*40)
    
    max_steps = min(len(results['sequential_job']), len(results['round_robin']))
    for i in range(min(15, max_steps)):
        seq_width = results['sequential_job'][i]['avg_start_width']
        rr_width = results['round_robin'][i]['avg_start_width']
        print(f"{i:<6} {seq_width:<15.2f} {rr_width:<15.2f}")


def check_feature_scale_problem(env: JobShopEnv) -> None:
    """
    Verifica si hay problemas de escala en las características.
    """
    state = env.reset()
    stats = analyze_feature_statistics(env, state)
    
    print("\n" + "="*80)
    print("ANÁLISIS DE ESCALA DE CARACTERÍSTICAS (Estado Inicial)")
    print("="*80)
    
    print(f"\n{'Característica':<25} {'Min':<10} {'Max':<10} {'Mean':<10} {'Std':<10} {'Range':<10}")
    print("-"*75)
    
    for name, s in stats.items():
        print(f"{name:<25} {s['min']:<10.2f} {s['max']:<10.2f} "
              f"{s['mean']:<10.2f} {s['std']:<10.2f} {s['range']:<10.2f}")
    
    # Detectar problemas
    print("\n>>> PROBLEMAS DETECTADOS:")
    issues = []
    
    for name, s in stats.items():
        if 'job_id' in name or 'op_idx' in name or 'machine' in name or 'remaining_ops' in name:
            continue  # Estos son índices, no valores continuos
            
        if s['range'] > 100:
            issues.append(f"  - {name}: rango muy grande ({s['range']:.2f})")
        if s['std'] > 50:
            issues.append(f"  - {name}: alta varianza ({s['std']:.2f})")
    
    if env.has_intervals:
        # Verificar si los upper bounds son mucho mayores que los lower
        if 'earliest_start_upper' in stats and 'earliest_start_lower' in stats:
            ratio = stats['earliest_start_upper']['max'] / max(stats['earliest_start_lower']['max'], 1)
            if ratio > 2:
                issues.append(f"  - Ratio upper/lower de earliest_start alto: {ratio:.2f}")
    
    if issues:
        for issue in issues:
            print(issue)
    else:
        print("  No se detectaron problemas obvios de escala.")


def main():
    # Cargar un problema CRISP para comparación
    print("\n" + "#"*80)
    print("# ANÁLISIS DE PROBLEMA CRISP (FT10)")
    print("#"*80)
    
    try:
        crisp_data = PROBLEM_REGISTRY['ft10']()
        crisp_env = JobShopEnv(
            num_jobs=crisp_data['num_jobs'],
            num_machines=crisp_data['num_machines'],
            sequences=crisp_data['sequences'],
            durations=crisp_data['durations'],
            problem_id='ft10'
        )
        
        check_feature_scale_problem(crisp_env)
        simulate_first_few_steps(crisp_env, 'sequential_job')
        
    except Exception as e:
        print(f"Error cargando problema CRISP: {e}")
    
    # Cargar un problema con intervalos
    print("\n" + "#"*80)
    print("# ANÁLISIS DE PROBLEMA CON INTERVALOS (FT10_INTERVAL)")
    print("#"*80)
    
    try:
        interval_data = PROBLEM_REGISTRY['ft10_interval']()
        interval_env = JobShopEnv(
            num_jobs=interval_data['num_jobs'],
            num_machines=interval_data['num_machines'],
            sequences=interval_data['sequences'],
            durations=interval_data['durations'],
            problem_id='ft10_interval'
        )
        
        check_feature_scale_problem(interval_env)
        simulate_first_few_steps(interval_env, 'sequential_job')
        compare_interval_widths(interval_env)
        
    except Exception as e:
        print(f"Error cargando problema con intervalos: {e}")
        import traceback
        traceback.print_exc()
    
    # Probar con una instancia Taillard con intervalos si existe
    print("\n" + "#"*80)
    print("# ANÁLISIS DE PROBLEMA TAILLARD CON INTERVALOS")
    print("#"*80)
    
    try:
        # Buscar una instancia de intervalos tipo Taillard
        interval_problems = [k for k in PROBLEM_REGISTRY.keys() if 'interval' in k.lower() and 'tai' in k.lower()]
        
        if interval_problems:
            problem_id = interval_problems[0]
            print(f"Usando problema: {problem_id}")
            
            tai_data = PROBLEM_REGISTRY[problem_id]()
            tai_env = JobShopEnv(
                num_jobs=tai_data['num_jobs'],
                num_machines=tai_data['num_machines'],
                sequences=tai_data['sequences'],
                durations=tai_data['durations'],
                problem_id=problem_id
            )
            
            check_feature_scale_problem(tai_env)
            compare_interval_widths(tai_env)
        else:
            print("No se encontraron problemas Taillard con intervalos.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
