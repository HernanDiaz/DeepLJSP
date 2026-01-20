"""
Simple validation script for interval-aware lower bounds (no pytest required).
Tests basic lower bound calculation functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.utils.problem_analyzer import (
    MakespanBoundCalculator,
    ProblemAnalyzer
)
from jobshop_rl.models.interval import Interval
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.data.test_3x3_interval import (
    get_test_3x3_interval,
    get_test_3x3_deterministic
)


def test_scalar_capacity_bound():
    """Test capacity bound for scalar problem."""
    print("Testing scalar capacity bound...")
    
    sequences = [[0, 1], [1, 0]]
    durations = [[5, 3], [4, 2]]
    
    bound = MakespanBoundCalculator.capacity_bound(sequences, durations)
    
    # Machine 0: 5 + 2 = 7, Machine 1: 3 + 4 = 7
    assert bound == 7, f"Expected 7, got {bound}"
    assert isinstance(bound, (int, float))
    
    print("✓ Scalar capacity bound works")


def test_scalar_critical_path():
    """Test critical path bound for scalar problem."""
    print("Testing scalar critical path bound...")
    
    sequences = [[0, 1], [1, 0]]
    durations = [[5, 3], [4, 2]]
    
    bound = MakespanBoundCalculator.critical_path_bound(sequences, durations)
    
    # Job 0: 5 + 3 = 8, Job 1: 4 + 2 = 6
    assert bound == 8, f"Expected 8, got {bound}"
    
    print("✓ Scalar critical path bound works")


def test_interval_capacity_bound():
    """Test capacity bound for interval problem."""
    print("Testing interval capacity bound...")
    
    sequences = [[0, 1], [1, 0]]
    durations = [
        [Interval(5, 7), Interval(3, 5)],
        [Interval(4, 6), Interval(2, 3)]
    ]
    
    bound = MakespanBoundCalculator.capacity_bound(sequences, durations)
    
    assert isinstance(bound, Interval), f"Expected Interval, got {type(bound)}"
    assert bound.lower == 7, f"Expected lower=7, got {bound.lower}"
    assert bound.upper == 11, f"Expected upper=11, got {bound.upper}"
    
    print("✓ Interval capacity bound works")


def test_interval_critical_path():
    """Test critical path bound for interval problem."""
    print("Testing interval critical path bound...")
    
    sequences = [[0, 1], [1, 0]]
    durations = [
        [Interval(5, 7), Interval(3, 5)],
        [Interval(4, 6), Interval(2, 3)]
    ]
    
    bound = MakespanBoundCalculator.critical_path_bound(sequences, durations)
    
    assert isinstance(bound, Interval)
    # Job 0: [5,7] + [3,5] = [8,12], Job 1: [4,6] + [2,3] = [6,9]
    assert bound.lower == 8, f"Expected lower=8, got {bound.lower}"
    assert bound.upper == 12, f"Expected upper=12, got {bound.upper}"
    
    print("✓ Interval critical path bound works")


def test_all_bounds_scalar():
    """Test all bounds for scalar problem."""
    print("Testing all bounds (scalar)...")
    
    sequences = [[0, 1], [1, 0]]
    durations = [[5, 3], [4, 2]]
    
    bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
    
    assert 'capacity' in bounds
    assert 'critical_path' in bounds
    assert 'one_machine' in bounds
    
    for name, value in bounds.items():
        assert isinstance(value, (int, float)), f"{name} should be scalar"
    
    print("✓ All scalar bounds work")


def test_all_bounds_interval():
    """Test all bounds for interval problem."""
    print("Testing all bounds (interval)...")
    
    sequences = [[0, 1], [1, 0]]
    durations = [
        [Interval(5, 7), Interval(3, 5)],
        [Interval(4, 6), Interval(2, 3)]
    ]
    
    bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
    
    assert 'capacity' in bounds
    assert 'critical_path' in bounds
    assert 'one_machine' in bounds
    
    for name, value in bounds.items():
        assert isinstance(value, Interval), f"{name} should be Interval"
        assert value.lower <= value.upper
    
    print("✓ All interval bounds work")


def test_bound_validity_scalar():
    """Test that scalar bound is valid (≤ makespan)."""
    print("Testing scalar bound validity...")
    
    problem = get_test_3x3_deterministic()
    
    # Get lower bound
    lb = MakespanBoundCalculator.get_best_lower_bound(
        problem['sequences'],
        problem['durations']
    )
    
    # Get actual makespan
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    env.reset()
    done = False
    while not done:
        if len(env.eligible_ops) > 0:
            state, reward, done, info = env.step(0)
        else:
            break
    
    makespan = info['makespan']
    
    assert lb <= makespan, f"Lower bound {lb} > makespan {makespan}"
    
    print(f"✓ Scalar bound validity: LB={lb} ≤ makespan={makespan}")


def test_bound_validity_interval():
    """Test that interval bound is valid (⪯ makespan lexicographically)."""
    print("Testing interval bound validity...")
    
    problem = get_test_3x3_interval()
    
    # Get lower bound
    lb = MakespanBoundCalculator.get_best_lower_bound(
        problem['sequences'],
        problem['durations']
    )
    
    # Get actual makespan
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    env.reset()
    done = False
    while not done:
        if len(env.eligible_ops) > 0:
            state, reward, done, info = env.step(0)
        else:
            break
    
    makespan = info['makespan']
    
    assert isinstance(lb, Interval), "Lower bound should be Interval"
    assert isinstance(makespan, Interval), "Makespan should be Interval"
    
    # Lexicographic comparison
    assert lb <= makespan, f"Lower bound {lb} > makespan {makespan} (lexicographic)"
    
    # Also check component-wise
    assert lb.lower <= makespan.lower, f"LB.lower={lb.lower} > makespan.lower={makespan.lower}"
    assert lb.upper <= makespan.upper, f"LB.upper={lb.upper} > makespan.upper={makespan.upper}"
    
    print(f"✓ Interval bound validity: LB={lb} ⪯ makespan={makespan}")


def test_problem_analyzer_scalar():
    """Test problem analyzer with scalar problem."""
    print("Testing problem analyzer (scalar)...")
    
    problem = get_test_3x3_deterministic()
    
    analysis = ProblemAnalyzer.analyze_problem(
        problem['sequences'],
        problem['durations']
    )
    
    assert analysis['num_jobs'] == 3
    assert analysis['num_machines'] == 3
    assert analysis['has_intervals'] == False
    assert isinstance(analysis['total_work'], (int, float))
    assert isinstance(analysis['best_lower_bound'], (int, float))
    
    print("✓ Problem analyzer works for scalar problems")


def test_problem_analyzer_interval():
    """Test problem analyzer with interval problem."""
    print("Testing problem analyzer (interval)...")
    
    problem = get_test_3x3_interval()
    
    analysis = ProblemAnalyzer.analyze_problem(
        problem['sequences'],
        problem['durations']
    )
    
    assert analysis['num_jobs'] == 3
    assert analysis['num_machines'] == 3
    assert analysis['has_intervals'] == True
    assert isinstance(analysis['total_work'], Interval)
    assert isinstance(analysis['best_lower_bound'], Interval)
    
    print("✓ Problem analyzer works for interval problems")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Lower Bounds Interval Support Validation")
    print("=" * 60)
    
    tests = [
        test_scalar_capacity_bound,
        test_scalar_critical_path,
        test_interval_capacity_bound,
        test_interval_critical_path,
        test_all_bounds_scalar,
        test_all_bounds_interval,
        test_bound_validity_scalar,
        test_bound_validity_interval,
        test_problem_analyzer_scalar,
        test_problem_analyzer_interval,
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
