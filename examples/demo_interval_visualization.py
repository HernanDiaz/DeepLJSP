"""
Demonstration of interval-based scheduling visualization.

This script shows:
1. Scalar scheduling with traditional Gantt chart
2. Interval scheduling with parallelogram Gantt chart
3. Makespan evolution with uncertainty bands
"""

import sys
import os
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.data.test_3x3_interval import (
    get_test_3x3_interval,
    get_test_3x3_deterministic
)


def demo_scalar_scheduling():
    """Demonstrate scalar scheduling with traditional Gantt chart."""
    print("\n" + "=" * 60)
    print("Demo 1: Scalar Scheduling (Deterministic)")
    print("=" * 60)
    
    problem = get_test_3x3_deterministic()
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    env.reset()
    
    # Run to completion using simple greedy policy
    done = False
    while not done:
        if len(env.eligible_ops) > 0:
            state, reward, done, info = env.step(0)
        else:
            break
    
    print(f"✓ Completed {len(env.schedule_history)} operations")
    print(f"✓ Makespan: {info['makespan']}")
    
    # Visualize
    fig = env.render_schedule(title="Scalar Schedule - Traditional Gantt Chart")
    plt.savefig('scalar_schedule.png', dpi=150, bbox_inches='tight')
    print(f"✓ Saved visualization to scalar_schedule.png")
    
    # Makespan evolution
    fig_makespan = env.plot_makespan_history(title="Makespan Evolution - Scalar")
    plt.savefig('scalar_makespan.png', dpi=150, bbox_inches='tight')
    print(f"✓ Saved makespan plot to scalar_makespan.png")


def demo_interval_scheduling():
    """Demonstrate interval scheduling with parallelogram Gantt chart."""
    print("\n" + "=" * 60)
    print("Demo 2: Interval Scheduling (Uncertainty)")
    print("=" * 60)
    
    problem = get_test_3x3_interval()
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    env.reset()
    
    # Run to completion
    done = False
    while not done:
        if len(env.eligible_ops) > 0:
            state, reward, done, info = env.step(0)
        else:
            break
    
    print(f"✓ Completed {len(env.schedule_history)} operations")
    
    makespan = info['makespan']
    print(f"✓ Makespan: [{makespan.lower:.1f}, {makespan.upper:.1f}]")
    print(f"  - Best case: {makespan.lower:.1f}")
    print(f"  - Worst case: {makespan.upper:.1f}")
    print(f"  - Uncertainty range: {makespan.width:.1f}")
    
    # Visualize with parallelograms
    fig = env.render_schedule(title="Interval Schedule - Parallelogram Gantt Chart")
    plt.savefig('interval_schedule.png', dpi=150, bbox_inches='tight')
    print(f"✓ Saved visualization to interval_schedule.png")
    
    # Makespan evolution with uncertainty bands
    fig_makespan = env.plot_makespan_history(title="Makespan Evolution - Interval")
    plt.savefig('interval_makespan.png', dpi=150, bbox_inches='tight')
    print(f"✓ Saved makespan plot to interval_makespan.png")


def demo_feature_extraction():
    """Demonstrate feature extraction for both problem types."""
    print("\n" + "=" * 60)
    print("Demo 3: Feature Extraction")
    print("=" * 60)
    
    # Scalar features
    problem_scalar = get_test_3x3_deterministic()
    env_scalar = JobShopEnv(
        num_jobs=problem_scalar['num_jobs'],
        num_machines=problem_scalar['num_machines'],
        sequences=problem_scalar['sequences'],
        durations=problem_scalar['durations']
    )
    
    state_scalar = env_scalar.reset()
    features_scalar = env_scalar.get_features(state_scalar)
    
    print(f"\nScalar Problem:")
    print(f"  Feature dimensions: {features_scalar.shape}")
    print(f"  Number of eligible operations: {len(state_scalar['eligible_ops'])}")
    print(f"  Features per operation: {features_scalar.shape[1]}")
    print(f"  First operation features: {features_scalar[0]}")
    
    # Interval features
    problem_interval = get_test_3x3_interval()
    env_interval = JobShopEnv(
        num_jobs=problem_interval['num_jobs'],
        num_machines=problem_interval['num_machines'],
        sequences=problem_interval['sequences'],
        durations=problem_interval['durations']
    )
    
    state_interval = env_interval.reset()
    features_interval = env_interval.get_features(state_interval)
    
    print(f"\nInterval Problem:")
    print(f"  Feature dimensions: {features_interval.shape}")
    print(f"  Number of eligible operations: {len(state_interval['eligible_ops'])}")
    print(f"  Features per operation: {features_interval.shape[1]}")
    print(f"  First operation features: {features_interval[0]}")
    
    print(f"\nFeature Explanation (Interval):")
    print(f"  [0] job_id: {features_interval[0][0]}")
    print(f"  [1] op_idx: {features_interval[0][1]}")
    print(f"  [2] machine: {features_interval[0][2]}")
    print(f"  [3] duration_lower: {features_interval[0][3]}")
    print(f"  [4] duration_upper: {features_interval[0][4]}")
    print(f"  [5] earliest_start_lower: {features_interval[0][5]}")
    print(f"  [6] earliest_start_upper: {features_interval[0][6]}")
    print(f"  [7] remaining_time_lower: {features_interval[0][7]}")
    print(f"  [8] remaining_time_upper: {features_interval[0][8]}")
    print(f"  [9] remaining_ops: {features_interval[0][9]}")


def demo_comparison():
    """Compare scalar vs interval scheduling on same problem structure."""
    print("\n" + "=" * 60)
    print("Demo 4: Scalar vs Interval Comparison")
    print("=" * 60)
    
    # Use same sequences
    sequences = [[0, 1, 2], [1, 0, 2], [2, 1, 0]]
    
    # Scalar version (midpoints)
    durations_scalar = [[6, 4, 9], [5, 7, 2], [6, 6, 8]]
    
    # Interval version (±1 uncertainty)
    from jobshop_rl.models.interval import Interval
    durations_interval = [
        [Interval(5, 7), Interval(3, 5), Interval(8, 10)],
        [Interval(4, 6), Interval(6, 8), Interval(1, 3)],
        [Interval(5, 7), Interval(5, 7), Interval(7, 9)]
    ]
    
    # Scalar scheduling
    env_scalar = JobShopEnv(
        num_jobs=3,
        num_machines=3,
        sequences=sequences,
        durations=durations_scalar
    )
    
    env_scalar.reset()
    done = False
    while not done:
        if len(env_scalar.eligible_ops) > 0:
            state, reward, done, info = env_scalar.step(0)
        else:
            break
    
    makespan_scalar = info['makespan']
    
    # Interval scheduling
    env_interval = JobShopEnv(
        num_jobs=3,
        num_machines=3,
        sequences=sequences,
        durations=durations_interval
    )
    
    env_interval.reset()
    done = False
    while not done:
        if len(env_interval.eligible_ops) > 0:
            state, reward, done, info = env_interval.step(0)
        else:
            break
    
    makespan_interval = info['makespan']
    
    print(f"\nResults:")
    print(f"  Scalar makespan: {makespan_scalar}")
    print(f"  Interval makespan: [{makespan_interval.lower:.1f}, {makespan_interval.upper:.1f}]")
    print(f"  Interval contains scalar: {makespan_interval.contains(makespan_scalar)}")
    print(f"\nInterpretation:")
    print(f"  The scalar solution ({makespan_scalar}) represents one possible")
    print(f"  realization within the uncertainty bounds [{makespan_interval.lower:.1f}, {makespan_interval.upper:.1f}]")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print(" INTERVAL-BASED JOB SHOP SCHEDULING - VISUALIZATION DEMO")
    print("=" * 70)
    
    # Run demos
    demo_scalar_scheduling()
    demo_interval_scheduling()
    demo_feature_extraction()
    demo_comparison()
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - scalar_schedule.png: Traditional Gantt chart")
    print("  - scalar_makespan.png: Makespan evolution")
    print("  - interval_schedule.png: Parallelogram Gantt chart")
    print("  - interval_makespan.png: Makespan with uncertainty bands")
    print("\nKey takeaways:")
    print("  1. Scalar problems use traditional rectangular Gantt charts")
    print("  2. Interval problems use parallelogram Gantt charts")
    print("  3. Parallelograms show temporal uncertainty visually")
    print("  4. Bottom edge = best case, top edge = worst case")
    print("  5. Feature extraction expands to 10D for intervals")


if __name__ == '__main__':
    main()
