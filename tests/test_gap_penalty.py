"""
Test del nuevo componente GapPenaltyComponent
"""

import sys
sys.path.insert(0, 'E:/PycharmProjects/DeepLJSP')

from jobshop_rl.rewards.components.gap_penalty import GapPenaltyComponent
from jobshop_rl.models.interval import Interval


def test_gap_penalty_scalar():
    """Prueba con valores escalares"""
    print("\n=== Test Gap Penalty con Valores Escalares ===")
    
    # Configurar problema de prueba
    problem_analysis = {
        'avg_op_duration': 50.0,
        'num_machines': 5,
        'num_jobs': 5
    }
    
    component = GapPenaltyComponent(weight=0.3, problem_analysis=problem_analysis)
    
    print(f"Gap scale: {component.gap_scale}")
    print(f"Gap threshold: {component.gap_threshold}")
    
    # Simular diferentes escenarios
    scenarios = [
        ("Sin gap", 100, 100, 50),
        ("Gap pequeño (3)", 100, 97, 50),
        ("Gap medio (10)", 100, 90, 50),
        ("Gap grande (30)", 100, 70, 50),
        ("Gap muy grande (50)", 100, 50, 50),
    ]
    
    # Mock env and state
    class MockEnv:
        sequences = [[0, 1, 2, 3, 4]]
        durations = [[50] * 5]
    
    env = MockEnv()
    
    for name, job_time, machine_time, duration in scenarios:
        state = {
            'eligible_ops': [0],
            'job_status': [2],
            'job_completion_time': [job_time],
            'machine_completion_time': [0, 0, machine_time, 0, 0]
        }
        
        next_state = state.copy()
        action = 0
        
        reward = component.calculate(env, state, next_state, action, False, {})
        gap = job_time - machine_time if job_time > machine_time else 0
        
        print(f"\n{name}:")
        print(f"  Gap: {gap}")
        print(f"  Reward: {reward:.4f}")


def test_gap_penalty_intervals():
    """Prueba con intervalos"""
    print("\n\n=== Test Gap Penalty con Intervalos ===")
    
    # Configurar problema de prueba
    problem_analysis = {
        'avg_op_duration': Interval(40, 60),
        'num_machines': 5,
        'num_jobs': 5
    }
    
    component = GapPenaltyComponent(weight=0.3, problem_analysis=problem_analysis)
    
    print(f"Gap scale: {component.gap_scale}")
    print(f"Gap threshold: {component.gap_threshold}")
    
    # Simular diferentes escenarios con intervalos
    scenarios = [
        ("Sin gap", Interval(100, 110), Interval(100, 110)),
        ("Gap pequeño", Interval(100, 110), Interval(95, 105)),
        ("Gap medio", Interval(100, 110), Interval(85, 95)),
        ("Gap grande", Interval(100, 110), Interval(60, 80)),
    ]
    
    # Mock env and state
    class MockEnv:
        sequences = [[0, 1, 2, 3, 4]]
        durations = [[Interval(40, 60)] * 5]
    
    env = MockEnv()
    
    for name, job_time, machine_time in scenarios:
        state = {
            'eligible_ops': [0],
            'job_status': [2],
            'job_completion_time': [job_time],
            'machine_completion_time': [Interval(0, 0), Interval(0, 0), machine_time, Interval(0, 0), Interval(0, 0)]
        }
        
        next_state = state.copy()
        action = 0
        
        reward = component.calculate(env, state, next_state, action, False, {})
        
        if job_time > machine_time:
            gap = job_time - machine_time
        else:
            gap = Interval(0, 0)
        
        print(f"\n{name}:")
        print(f"  Gap: {gap}")
        print(f"  Reward: {reward:.4f}")


def test_comparison_weights():
    """Compara el impacto de diferentes pesos"""
    print("\n\n=== Comparación de Pesos ===")
    
    problem_analysis = {'avg_op_duration': 50.0}
    
    weights = [0.1, 0.2, 0.3, 0.4, 0.5]
    gap = 30  # Gap grande
    
    class MockEnv:
        sequences = [[0, 1, 2]]
        durations = [[50] * 3]
    
    env = MockEnv()
    
    state = {
        'eligible_ops': [0],
        'job_status': [1],
        'job_completion_time': [100],
        'machine_completion_time': [0, 70, 0]
    }
    
    print(f"\nGap fijo de {gap} unidades:")
    for w in weights:
        component = GapPenaltyComponent(weight=w, problem_analysis=problem_analysis)
        reward = component.calculate(env, state, state.copy(), 0, False, {})
        print(f"  Weight {w}: Reward = {reward:.4f}")


if __name__ == "__main__":
    test_gap_penalty_scalar()
    test_gap_penalty_intervals()
    test_comparison_weights()
    
    print("\n\n✓ Todos los tests completados")
