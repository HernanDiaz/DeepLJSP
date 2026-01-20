"""
Simple validation script for interval-aware environment (no pytest required).
Tests basic interval scheduling functionality.
"""

import sys
import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.models.interval import Interval
from jobshop_rl.data.test_3x3_interval import (
    get_test_3x3_interval,
    get_test_3x3_deterministic
)


def test_init_scalar():
    """Test environment initialization with scalar problem."""
    print("Testing scalar environment initialization...")
    
    problem = get_test_3x3_deterministic()
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    assert env.num_jobs == 3
    assert env.num_machines == 3
    assert not env.has_intervals
    
    print("✓ Scalar environment initialization works")


def test_init_interval():
    """Test environment initialization with interval problem."""
    print("Testing interval environment initialization...")
    
    problem = get_test_3x3_interval()
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    assert env.num_jobs == 3
    assert env.num_machines == 3
    assert env.has_intervals
    
    print("✓ Interval environment initialization works")


def test_scalar_features():
    """Test feature extraction for scalar problem (7D)."""
    print("Testing scalar feature extraction...")
    
    problem = get_test_3x3_deterministic()
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    state = env.reset()
    features = env.get_features(state)
    
    assert features.shape[1] == 7, f"Expected 7 features, got {features.shape[1]}"
    assert features.shape[0] == 3, f"Expected 3 eligible ops, got {features.shape[0]}"
    
    print("✓ Scalar features (7D) work correctly")


def test_interval_features():
    """Test feature extraction for interval problem (10D)."""
    print("Testing interval feature extraction...")
    
    problem = get_test_3x3_interval()
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    state = env.reset()
    features = env.get_features(state)
    
    assert features.shape[1] == 10, f"Expected 10 features, got {features.shape[1]}"
    assert features.shape[0] == 3, f"Expected 3 eligible ops, got {features.shape[0]}"
    
    print("✓ Interval features (10D) work correctly")


def test_scalar_scheduling():
    """Test complete scheduling with scalar durations."""
    print("Testing scalar scheduling...")
    
    problem = get_test_3x3_deterministic()
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    env.reset()
    
    # Run to completion
    done = False
    steps = 0
    
    while not done and steps < 20:
        if len(env.eligible_ops) > 0:
            state, reward, done, info = env.step(0)
            steps += 1
        else:
            break
    
    assert done, "Scheduling did not complete"
    assert len(env.schedule_history) == 9, f"Expected 9 operations, got {len(env.schedule_history)}"
    
    # All times should be scalars
    for op in env.schedule_history:
        assert isinstance(op['start'], (int, float)), "Start time should be scalar"
        assert isinstance(op['end'], (int, float)), "End time should be scalar"
    
    # Makespan should be scalar
    assert isinstance(info['makespan'], (int, float)), "Makespan should be scalar"
    assert info['makespan'] > 0
    
    print(f"✓ Scalar scheduling works (makespan: {info['makespan']})")


def test_interval_scheduling():
    """Test complete scheduling with interval durations."""
    print("Testing interval scheduling...")
    
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
    steps = 0
    
    while not done and steps < 20:
        if len(env.eligible_ops) > 0:
            state, reward, done, info = env.step(0)
            steps += 1
        else:
            break
    
    assert done, "Scheduling did not complete"
    assert len(env.schedule_history) == 9, f"Expected 9 operations, got {len(env.schedule_history)}"
    
    # All times should be intervals
    for op in env.schedule_history:
        assert isinstance(op['start'], Interval), "Start time should be Interval"
        assert isinstance(op['end'], Interval), "End time should be Interval"
    
    # Makespan should be interval
    assert isinstance(info['makespan'], Interval), "Makespan should be Interval"
    assert info['makespan'].lower > 0
    assert info['makespan'].upper >= info['makespan'].lower
    
    print(f"✓ Interval scheduling works (makespan: [{info['makespan'].lower:.1f}, {info['makespan'].upper:.1f}])")


def test_interval_arithmetic():
    """Test interval arithmetic in schedule construction."""
    print("Testing interval arithmetic...")
    
    # Simple 2x2 problem
    sequences = [[0, 1], [1, 0]]
    durations = [
        [Interval(5, 7), Interval(3, 5)],
        [Interval(4, 6), Interval(2, 3)]
    ]
    
    env = JobShopEnv(
        num_jobs=2,
        num_machines=2,
        sequences=sequences,
        durations=durations
    )
    
    env.reset()
    
    # Schedule Job 0, Op 0 (M0, [5,7])
    state, reward, done, info = env.step(0)
    
    # Verify interval addition
    assert env.job_completion_time[0].lower == 5
    assert env.job_completion_time[0].upper == 7
    assert env.machine_completion_time[0].lower == 5
    assert env.machine_completion_time[0].upper == 7
    
    print("✓ Interval arithmetic works correctly")


def test_visualization():
    """Test visualization for both scalar and interval schedules."""
    print("Testing visualization...")
    
    # Scalar visualization
    problem_scalar = get_test_3x3_deterministic()
    env_scalar = JobShopEnv(
        num_jobs=problem_scalar['num_jobs'],
        num_machines=problem_scalar['num_machines'],
        sequences=problem_scalar['sequences'],
        durations=problem_scalar['durations']
    )
    
    env_scalar.reset()
    for _ in range(3):
        if len(env_scalar.eligible_ops) > 0:
            env_scalar.step(0)
    
    fig_scalar = env_scalar.render_schedule(title="Test Scalar")
    assert fig_scalar is not None
    
    # Interval visualization
    problem_interval = get_test_3x3_interval()
    env_interval = JobShopEnv(
        num_jobs=problem_interval['num_jobs'],
        num_machines=problem_interval['num_machines'],
        sequences=problem_interval['sequences'],
        durations=problem_interval['durations']
    )
    
    env_interval.reset()
    for _ in range(3):
        if len(env_interval.eligible_ops) > 0:
            env_interval.step(0)
    
    fig_interval = env_interval.render_schedule(title="Test Interval")
    assert fig_interval is not None
    
    print("✓ Visualization works for both scalar and interval schedules")


def test_backward_compatibility():
    """Test that degenerate intervals behave like scalars."""
    print("Testing backward compatibility...")
    
    # Same problem, different representations
    sequences = [[0, 1], [1, 0]]
    scalar_durations = [[5, 3], [4, 2]]
    interval_durations = [
        [Interval(5, 5), Interval(3, 3)],
        [Interval(4, 4), Interval(2, 2)]
    ]
    
    env_scalar = JobShopEnv(2, 2, sequences, scalar_durations)
    env_interval = JobShopEnv(2, 2, sequences, interval_durations)
    
    env_scalar.reset()
    env_interval.reset()
    
    # Same actions
    for _ in range(4):
        if len(env_scalar.eligible_ops) > 0:
            env_scalar.step(0)
        if len(env_interval.eligible_ops) > 0:
            env_interval.step(0)
    
    # Should produce equivalent results
    makespan_scalar = max(env_scalar.job_completion_time)
    makespan_interval = max(env_interval.job_completion_time)
    
    if isinstance(makespan_interval, Interval):
        assert makespan_interval.lower == makespan_scalar
        assert makespan_interval.upper == makespan_scalar
    
    print("✓ Backward compatibility maintained")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Environment Interval Support Validation")
    print("=" * 60)
    
    tests = [
        test_init_scalar,
        test_init_interval,
        test_scalar_features,
        test_interval_features,
        test_scalar_scheduling,
        test_interval_scheduling,
        test_interval_arithmetic,
        test_visualization,
        test_backward_compatibility,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {failed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
