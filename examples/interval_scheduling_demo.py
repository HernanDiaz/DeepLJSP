"""
Demonstration of interval-based scheduling in JobShopRL.

This script shows how to:
1. Load interval-valued problems
2. Schedule with interval arithmetic
3. Visualize uncertainty in schedules
4. Compare deterministic vs uncertain schedules
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
from jobshop_rl.heuristics.strategies import SPTHeuristic


def demo_basic_interval_scheduling():
    """Demonstrate basic interval scheduling."""
    print("=" * 70)
    print("Demo 1: Basic Interval Scheduling")
    print("=" * 70)
    
    # Load interval problem
    problem = get_test_3x3_interval()
    
    print(f"\nProblem: {problem['num_jobs']} jobs × {problem['num_machines']} machines")
    print(f"Has intervals: {problem['has_intervals']}")
    
    # Show sample durations
    print("\nSample durations (Job 0):")
    for i, dur in enumerate(problem['durations'][0]):
        print(f"  Operation {i}: {dur}")
    
    # Create environment
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    env.reset()
    
    # Use SPT heuristic for scheduling
    heuristic = SPTHeuristic()
    
    done = False
    step = 0
    
    print("\nScheduling progress:")
    while not done:
        if len(env.eligible_ops) == 0:
            break
        
        # Get features
        state = env._get_state()
        features = env.get_features(state)
        
        # Select action using heuristic
        action_idx = heuristic.select_action(env.eligible_ops, features)
        
        # Execute action
        next_state, reward, done, info = env.step(action_idx)
        
        step += 1
        
        if step % 3 == 0 or done:
            current_makespan = max(env.job_completion_time)
            print(f"  Step {step}: Makespan = {current_makespan}")
    
    # Final results
    makespan = info['makespan']
    print(f"\n✓ Scheduling complete!")
    print(f"  Total steps: {step}")
    print(f"  Final makespan: {makespan}")
    print(f"  Best case: {makespan.lower:.1f}")
    print(f"  Worst case: {makespan.upper:.1f}")
    print(f"  Uncertainty: ±{makespan.width/2:.1f}")
    
    # Visualize
    print("\nGenerating visualization...")
    fig = env.render_schedule(title="3x3 Interval Schedule (SPT)")
    plt.savefig('interval_schedule_demo.png', dpi=150, bbox_inches='tight')
    print("  Saved: interval_schedule_demo.png")
    plt.close()
    
    # Makespan history
    fig = env.plot_makespan_history(title="Makespan Evolution (Interval)")
    plt.savefig('makespan_history_interval.png', dpi=150, bbox_inches='tight')
    print("  Saved: makespan_history_interval.png")
    plt.close()


def demo_comparison():
    """Compare deterministic vs interval scheduling."""
    print("\n" + "=" * 70)
    print("Demo 2: Deterministic vs Interval Comparison")
    print("=" * 70)
    
    # Load both versions
    problem_det = get_test_3x3_deterministic()
    problem_int = get_test_3x3_interval()
    
    # Create environments
    env_det = JobShopEnv(
        num_jobs=problem_det['num_jobs'],
        num_machines=problem_det['num_machines'],
        sequences=problem_det['sequences'],
        durations=problem_det['durations']
    )
    
    env_int = JobShopEnv(
        num_jobs=problem_int['num_jobs'],
        num_machines=problem_int['num_machines'],
        sequences=problem_int['sequences'],
        durations=problem_int['durations']
    )
    
    env_det.reset()
    env_int.reset()
    
    # Use same heuristic
    heuristic = SPTHeuristic()
    
    # Schedule both
    print("\nScheduling deterministic problem...")
    done = False
    while not done:
        if len(env_det.eligible_ops) == 0:
            break
        state = env_det._get_state()
        features = env_det.get_features(state)
        action_idx = heuristic.select_action(env_det.eligible_ops, features)
        _, _, done, info_det = env_det.step(action_idx)
    
    print("Scheduling interval problem...")
    done = False
    while not done:
        if len(env_int.eligible_ops) == 0:
            break
        state = env_int._get_state()
        features = env_int.get_features(state)
        action_idx = heuristic.select_action(env_int.eligible_ops, features)
        _, _, done, info_int = env_int.step(action_idx)
    
    # Compare results
    makespan_det = info_det['makespan']
    makespan_int = info_int['makespan']
    
    print("\nResults:")
    print(f"  Deterministic makespan: {makespan_det}")
    print(f"  Interval makespan: [{makespan_int.lower:.1f}, {makespan_int.upper:.1f}]")
    print(f"  Deterministic is close to midpoint: {makespan_int.midpoint:.1f}")
    
    # Side-by-side visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Deterministic schedule
    plt.sca(ax1)
    env_det.render_schedule(title="Deterministic Schedule")
    
    # Interval schedule
    plt.sca(ax2)
    env_int.render_schedule(title="Interval Schedule")
    
    plt.tight_layout()
    plt.savefig('comparison_det_vs_interval.png', dpi=150, bbox_inches='tight')
    print("\n  Saved: comparison_det_vs_interval.png")
    plt.close()


def demo_feature_dimensions():
    """Show feature dimension differences."""
    print("\n" + "=" * 70)
    print("Demo 3: Feature Dimension Comparison")
    print("=" * 70)
    
    problem_det = get_test_3x3_deterministic()
    problem_int = get_test_3x3_interval()
    
    env_det = JobShopEnv(
        num_jobs=problem_det['num_jobs'],
        num_machines=problem_det['num_machines'],
        sequences=problem_det['sequences'],
        durations=problem_det['durations']
    )
    
    env_int = JobShopEnv(
        num_jobs=problem_int['num_jobs'],
        num_machines=problem_int['num_machines'],
        sequences=problem_int['sequences'],
        durations=problem_int['durations']
    )
    
    state_det = env_det.reset()
    state_int = env_int.reset()
    
    features_det = env_det.get_features(state_det)
    features_int = env_int.get_features(state_int)
    
    print("\nFeature comparison:")
    print(f"  Deterministic: {features_det.shape} (7 features per operation)")
    print(f"  Interval: {features_int.shape} (10 features per operation)")
    
    print("\nDeterministic features (Job 0, Op 0):")
    print(f"  {features_det[0]}")
    print("  [job_id, op_idx, machine, duration, earliest_start, remaining_time, remaining_ops]")
    
    print("\nInterval features (Job 0, Op 0):")
    print(f"  {features_int[0]}")
    print("  [job_id, op_idx, machine,")
    print("   duration_lower, duration_upper,")
    print("   earliest_start_lower, earliest_start_upper,")
    print("   remaining_time_lower, remaining_time_upper,")
    print("   remaining_ops]")


def demo_uncertainty_propagation():
    """Demonstrate how uncertainty propagates through schedule."""
    print("\n" + "=" * 70)
    print("Demo 4: Uncertainty Propagation")
    print("=" * 70)
    
    from jobshop_rl.models.interval import Interval
    
    # Create simple problem with clear uncertainty
    sequences = [[0, 1], [1, 0]]
    durations = [
        [Interval(10, 20), Interval(5, 10)],  # High uncertainty
        [Interval(8, 12), Interval(3, 5)]     # Low uncertainty
    ]
    
    env = JobShopEnv(
        num_jobs=2,
        num_machines=2,
        sequences=sequences,
        durations=durations
    )
    
    env.reset()
    
    print("\nInput durations:")
    print("  Job 0: [10,20] → [5,10]")
    print("  Job 1: [8,12] → [3,5]")
    
    # Schedule step by step
    print("\nSchedule construction:")
    
    # Job 0, Op 0
    env.step(0)
    print(f"\n  After J0-O0 on M0:")
    print(f"    Job 0 completion: {env.job_completion_time[0]}")
    print(f"    Machine 0 busy: {env.machine_completion_time[0]}")
    
    # Job 1, Op 0
    env.step(0)
    print(f"\n  After J1-O0 on M1:")
    print(f"    Job 1 completion: {env.job_completion_time[1]}")
    print(f"    Machine 1 busy: {env.machine_completion_time[1]}")
    
    # Job 0, Op 1
    env.step(0)
    print(f"\n  After J0-O1 on M1:")
    print(f"    Job 0 completion: {env.job_completion_time[0]}")
    print(f"    Machine 1 busy: {env.machine_completion_time[1]}")
    
    # Job 1, Op 1
    env.step(0)
    print(f"\n  After J1-O1 on M0:")
    print(f"    Job 1 completion: {env.job_completion_time[1]}")
    print(f"    Machine 0 busy: {env.machine_completion_time[0]}")
    
    # Final makespan
    makespan = max(env.job_completion_time)
    print(f"\n✓ Final makespan: {makespan}")
    print(f"  Uncertainty width: {makespan.width:.1f} time units")
    print(f"  Relative uncertainty: {makespan.width/makespan.midpoint*100:.1f}%")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("INTERVAL-BASED SCHEDULING DEMONSTRATION")
    print("=" * 70)
    
    try:
        # Demo 1: Basic usage
        demo_basic_interval_scheduling()
        
        # Demo 2: Comparison
        demo_comparison()
        
        # Demo 3: Feature dimensions
        demo_feature_dimensions()
        
        # Demo 4: Uncertainty propagation
        demo_uncertainty_propagation()
        
        print("\n" + "=" * 70)
        print("All demonstrations completed successfully!")
        print("=" * 70)
        print("\nGenerated visualizations:")
        print("  - interval_schedule_demo.png")
        print("  - makespan_history_interval.png")
        print("  - comparison_det_vs_interval.png")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
