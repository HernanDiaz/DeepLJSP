"""
Script para debuguear los bugs específicos en el manejo de intervalos.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.models.interval import Interval
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.rewards.components.idle_time import IdleTimeRewardComponent
from jobshop_rl.data import PROBLEM_REGISTRY


def test_interval_subtraction():
    """Test que demuestra el problema con la resta de intervalos."""
    print("\n" + "="*60)
    print("TEST 1: RESTA DE INTERVALOS")
    print("="*60)
    
    # Caso problemático
    a = Interval(10, 20)
    b = Interval(5, 25)
    
    print(f"a = {a}")
    print(f"b = {b}")
    
    try:
        result = a - b
        print(f"a - b = {result}")
    except ValueError as e:
        print(f"ERROR: La resta falla porque: {e}")
        print("  Explicación: a.lower - b.upper = 10 - 25 = -15")
        print("              a.upper - b.lower = 20 - 5 = 15")
        print("              Resultado: [-15, 15] viola lower <= upper")


def test_max_inconsistency():
    """Test que demuestra la inconsistencia entre max() y Interval.max()."""
    print("\n" + "="*60)
    print("TEST 2: INCONSISTENCIA max() vs Interval.max()")
    print("="*60)
    
    a = Interval(10, 30)
    b = Interval(15, 25)
    
    print(f"a = {a}  (upper=30, lower=10)")
    print(f"b = {b}  (upper=25, lower=15)")
    
    # max() de Python usa comparación lexicográfica (upper, lower)
    python_max = max(a, b)
    print(f"\nmax(a, b) [Python - lexicográfico] = {python_max}")
    print(f"  Compara (30,10) vs (25,15) → (30,10) > (25,15) → a gana")
    
    # Interval.max() es component-wise
    interval_max = Interval.max(a, b)
    print(f"\nInterval.max(a, b) [component-wise] = {interval_max}")
    print(f"  max(10,15)=15, max(30,25)=30 → [15, 30]")
    
    print(f"\n¡DIFERENTES RESULTADOS!")


def test_idle_time_calculation():
    """Test que demuestra el problema en el cálculo de idle_time."""
    print("\n" + "="*60)
    print("TEST 3: CÁLCULO DE IDLE_TIME CON INTERVALOS")
    print("="*60)
    
    job_time = Interval(10, 20)
    machine_time = Interval(5, 25)
    
    print(f"job_completion_time = {job_time}")
    print(f"machine_completion_time = {machine_time}")
    
    # Cómo lo calcula el ENTORNO (correcto - component-wise)
    start_time_env = Interval.max(job_time, machine_time)
    print(f"\nEntorno calcula start_time = Interval.max(...) = {start_time_env}")
    
    # Cómo lo calcula el COMPONENTE DE RECOMPENSA (incorrecto - lexicográfico)
    start_time_reward = max(job_time, machine_time)
    print(f"Componente recompensa calcula start_time = max(...) = {start_time_reward}")
    
    print(f"\n¡VALORES DIFERENTES!")
    
    # Intento de calcular idle_time
    print(f"\nIntentando calcular idle_time = start_time - machine_time:")
    try:
        # Usando el start_time del entorno
        idle_time = start_time_env - machine_time
        print(f"  Con Interval.max: {idle_time}")
    except ValueError as e:
        print(f"  Con Interval.max: ERROR - {e}")
    
    # Verificar la condición del if
    print(f"\nCondición 'start_time > machine_time':")
    print(f"  Con start_time del entorno ({start_time_env}): {start_time_env} > {machine_time} = {start_time_env > machine_time}")
    print(f"  Con start_time del reward ({start_time_reward}): {start_time_reward} > {machine_time} = {start_time_reward > machine_time}")


def test_feature_extraction():
    """Test que verifica la extracción de características con intervalos."""
    print("\n" + "="*60)
    print("TEST 4: EXTRACCIÓN DE CARACTERÍSTICAS")
    print("="*60)
    
    try:
        # Cargar problema con intervalos
        interval_data = PROBLEM_REGISTRY['ft10_interval']()
        env = JobShopEnv(
            num_jobs=interval_data['num_jobs'],
            num_machines=interval_data['num_machines'],
            sequences=interval_data['sequences'],
            durations=interval_data['durations'],
            problem_id='ft10_interval'
        )
        
        state = env.reset()
        
        print(f"Problema: {interval_data['num_jobs']} jobs x {interval_data['num_machines']} máquinas")
        print(f"has_intervals: {env.has_intervals}")
        
        # Obtener características
        features = env.get_features(state)
        print(f"\nDimensión de características: {features.shape}")
        print(f"Esperado para intervalos: (n_ops, 10)")
        
        # Mostrar algunas características
        print(f"\nPrimeras 3 operaciones elegibles:")
        print(f"{'Job':<5} {'Op':<5} {'Maq':<5} {'Dur_L':<8} {'Dur_U':<8} {'Start_L':<8} {'Start_U':<8}")
        for i in range(min(3, len(features))):
            f = features[i]
            print(f"{f[0]:<5.0f} {f[1]:<5.0f} {f[2]:<5.0f} {f[3]:<8.2f} {f[4]:<8.2f} {f[5]:<8.2f} {f[6]:<8.2f}")
        
        # Verificar normalización
        print(f"\nFactores de normalización usados:")
        print(f"  time_norm: {env.problem_analysis.get('best_lower_bound', 'N/A')}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


def test_reward_with_intervals():
    """Test que simula el cálculo de recompensas paso a paso."""
    print("\n" + "="*60)
    print("TEST 5: SIMULACIÓN DE RECOMPENSAS")
    print("="*60)
    
    try:
        interval_data = PROBLEM_REGISTRY['ft10_interval']()
        env = JobShopEnv(
            num_jobs=interval_data['num_jobs'],
            num_machines=interval_data['num_machines'],
            sequences=interval_data['sequences'],
            durations=interval_data['durations'],
            problem_id='ft10_interval'
        )
        
        state = env.reset()
        total_reward = 0
        rewards_by_step = []
        
        print("Ejecutando 10 pasos y registrando recompensas...")
        
        for step in range(10):
            eligible = state['eligible_ops']
            if not eligible:
                break
            
            # Siempre tomar la primera acción (simula política degenerada)
            action_idx = 0
            selected_job = eligible[action_idx]
            
            state, reward, done, info = env.step(action_idx)
            total_reward += reward
            rewards_by_step.append((selected_job, reward))
            
            if done:
                print(f"  Episodio terminó en paso {step+1}")
                print(f"  Makespan final: {info.get('makespan', 'N/A')}")
                break
        
        print(f"\nRecompensas por paso (acción 0 = primer trabajo elegible):")
        for i, (job, reward) in enumerate(rewards_by_step):
            print(f"  Paso {i+1}: Job {job}, Recompensa = {reward:.4f}")
        
        print(f"\nRecompensa total: {total_reward:.4f}")
        
        # Verificar si hay problema de colapso a política degenerada
        jobs_selected = [j for j, r in rewards_by_step]
        unique_jobs = len(set(jobs_selected))
        print(f"\nJobs únicos seleccionados: {unique_jobs}/{len(jobs_selected)}")
        if unique_jobs < len(jobs_selected) / 2:
            print("⚠️  POSIBLE PROBLEMA: Muy poca diversidad en selección de jobs")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


def test_comparison_crisp_vs_interval():
    """Compara el comportamiento con problema CRISP vs Interval."""
    print("\n" + "="*60)
    print("TEST 6: COMPARACIÓN CRISP vs INTERVAL")
    print("="*60)
    
    try:
        # CRISP
        crisp_data = PROBLEM_REGISTRY['ft10']()
        crisp_env = JobShopEnv(
            num_jobs=crisp_data['num_jobs'],
            num_machines=crisp_data['num_machines'],
            sequences=crisp_data['sequences'],
            durations=crisp_data['durations'],
            problem_id='ft10'
        )
        
        # Interval
        interval_data = PROBLEM_REGISTRY['ft10_interval']()
        interval_env = JobShopEnv(
            num_jobs=interval_data['num_jobs'],
            num_machines=interval_data['num_machines'],
            sequences=interval_data['sequences'],
            durations=interval_data['durations'],
            problem_id='ft10_interval'
        )
        
        print("Ejecutando mismo conjunto de acciones en ambos entornos...")
        
        # Generar secuencia aleatoria de acciones
        import random
        random.seed(42)
        
        crisp_state = crisp_env.reset()
        interval_state = interval_env.reset()
        
        crisp_rewards = []
        interval_rewards = []
        
        for step in range(20):
            crisp_eligible = crisp_state['eligible_ops']
            interval_eligible = interval_state['eligible_ops']
            
            if not crisp_eligible or not interval_eligible:
                break
            
            # Usar misma acción en ambos
            action_idx = 0  # Siempre primera acción
            
            crisp_state, crisp_r, crisp_done, _ = crisp_env.step(action_idx)
            interval_state, interval_r, interval_done, _ = interval_env.step(action_idx)
            
            crisp_rewards.append(crisp_r)
            interval_rewards.append(interval_r)
            
            if crisp_done or interval_done:
                break
        
        print(f"\n{'Paso':<6} {'CRISP':<12} {'Interval':<12} {'Diferencia':<12}")
        print("-"*45)
        for i, (c, iv) in enumerate(zip(crisp_rewards, interval_rewards)):
            diff = iv - c
            print(f"{i+1:<6} {c:<12.4f} {iv:<12.4f} {diff:<12.4f}")
        
        print(f"\nSuma CRISP:    {sum(crisp_rewards):.4f}")
        print(f"Suma Interval: {sum(interval_rewards):.4f}")
        
        if abs(sum(interval_rewards)) < 0.001 and abs(sum(crisp_rewards)) > 0.1:
            print("\n⚠️  PROBLEMA DETECTADO: Las recompensas con intervalos son casi 0")
            print("    mientras que con CRISP son significativas.")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_interval_subtraction()
    test_max_inconsistency()
    test_idle_time_calculation()
    test_feature_extraction()
    test_reward_with_intervals()
    test_comparison_crisp_vs_interval()
    
    print("\n" + "="*60)
    print("RESUMEN DE DIAGNÓSTICO")
    print("="*60)
    print("""
Los tests anteriores demuestran varios problemas:

1. La resta de intervalos puede violar la invariante lower <= upper
2. max() de Python y Interval.max() dan resultados diferentes
3. El componente de idle_time usa max() incorrecto
4. Las características podrían no estar normalizadas correctamente
5. Las recompensas con intervalos podrían ser cercanas a 0

Revisa los resultados para confirmar qué problemas están presentes
en tu configuración específica.
""")
