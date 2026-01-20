"""
Simple validation script for interval-aware heuristics (no pytest required).
Tests basic heuristic functionality with intervals.
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.heuristics.strategies import (
    SPTHeuristic,
    LPTHeuristic,
    MWKRHeuristic,
    ESTHeuristic,
    CRHeuristic
)
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.data.test_3x3_interval import (
    get_test_3x3_interval,
    get_test_3x3_deterministic
)


def test_spt_scalar():
    """Test SPT with scalar features."""
    print("Testing SPT with scalar features...")
    
    # Scalar features: [job_id, op_idx, machine, duration, earliest_start, remaining_time, remaining_ops]
    features = np.array([
        [0, 0, 0, 5.0, 0, 15, 2],
        [1, 0, 1, 3.0, 0, 10, 2],  # Shortest
        [2, 0, 2, 7.0, 0, 20, 2]
    ])
    
    heuristic = SPTHeuristic()
    action = heuristic.select_action([0, 1, 2], features)
    
    assert action == 1, f"Expected action 1, got {action}"
    
    print("✓ SPT with scalar features works")


def test_spt_interval():
    """Test SPT with interval features."""
    print("Testing SPT with interval features...")
    
    # Interval features: [job_id, op_idx, machine, dur_lower, dur_upper, 
    #                     start_lower, start_upper, remain_lower, remain_upper, remaining_ops]
    features = np.array([
        [0, 0, 0, 5, 7, 0, 0, 15, 20, 2],
        [1, 0, 1, 2, 4, 0, 0, 10, 15, 2],   # Shortest (lex)
        [2, 0, 2, 6, 9, 0, 0, 20, 25, 2]
    ])
    
    heuristic = SPTHeuristic()
    action = heuristic.select_action([0, 1, 2], features)
    
    assert action == 1, f"Expected action 1, got {action}"
    
    print("✓ SPT with interval features works")


def test_lpt_interval():
    """Test LPT with interval features."""
    print("Testing LPT with interval features...")
    
    features = np.array([
        [0, 0, 0, 5, 7, 0, 0, 15, 20, 2],
        [1, 0, 1, 2, 4, 0, 0, 10, 15, 2],
        [2, 0, 2, 6, 9, 0, 0, 20, 25, 2]    # Longest (lex)
    ])
    
    heuristic = LPTHeuristic()
    action = heuristic.select_action([0, 1, 2], features)
    
    assert action == 2, f"Expected action 2, got {action}"
    
    print("✓ LPT with interval features works")


def test_with_scalar_environment():
    """Test heuristic with scalar environment."""
    print("Testing heuristic with scalar environment...")
    
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
    
    heuristic = SPTHeuristic()
    action = heuristic.select_action(env.eligible_ops, features)
    
    assert 0 <= action < len(env.eligible_ops), f"Invalid action {action}"
    
    print("✓ Heuristic with scalar environment works")


def test_with_interval_environment():
    """Test heuristic with interval environment."""
    print("Testing heuristic with interval environment...")
    
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
    
    heuristic = SPTHeuristic()
    action = heuristic.select_action(env.eligible_ops, features)
    
    assert 0 <= action < len(env.eligible_ops), f"Invalid action {action}"
    
    print("✓ Heuristic with interval environment works")


def test_complete_scheduling():
    """Test complete scheduling with heuristic."""
    print("Testing complete scheduling with heuristic...")
    
    problem = get_test_3x3_interval()
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    heuristic = SPTHeuristic()
    
    env.reset()
    done = False
    steps = 0
    max_steps = 20
    
    while not done and steps < max_steps:
        if len(env.eligible_ops) > 0:
            state = env._get_state()
            features = env.get_features(state)
            action = heuristic.select_action(env.eligible_ops, features)
            state, reward, done, info = env.step(action)
            steps += 1
        else:
            break
    
    assert done, "Scheduling did not complete"
    
    from jobshop_rl.models.interval import Interval
    assert isinstance(info['makespan'], Interval), "Makespan should be Interval"
    
    print(f"✓ Complete scheduling works (makespan: {info['makespan']})")


def test_lexicographic_comparison():
    """Test lexicographic comparison for intervals."""
    print("Testing lexicographic comparison...")
    
    # [4,8] should be chosen over [6,8] because lower bound is smaller
    features = np.array([
        [0, 0, 0, 5, 10, 0, 0, 15, 20, 2],
        [1, 0, 1, 4, 8, 0, 0, 10, 15, 2],   # Chosen (smaller upper, then lower)
        [2, 0, 2, 6, 8, 0, 0, 20, 25, 2]
    ])
    
    heuristic = SPTHeuristic()
    action = heuristic.select_action([0, 1, 2], features)
    
    assert action == 1, f"Expected action 1 (lexicographic), got {action}"
    
    print("✓ Lexicographic comparison works")


def test_all_heuristics_scalar():
    """Test all heuristics with scalar features."""
    print("Testing all heuristics with scalar features...")
    
    features = np.array([
        [0, 0, 0, 5.0, 0, 15, 2],
        [1, 0, 1, 3.0, 0, 10, 2],
        [2, 0, 2, 7.0, 0, 20, 2]
    ])
    
    heuristics = [
        SPTHeuristic(),
        LPTHeuristic(),
        MWKRHeuristic(),
        ESTHeuristic(),
        CRHeuristic()
    ]
    
    for heuristic in heuristics:
        action = heuristic.select_action([0, 1, 2], features)
        assert 0 <= action <= 2, f"{heuristic.__class__.__name__} returned invalid action"
    
    print("✓ All heuristics work with scalar features")


def test_all_heuristics_interval():
    """Test all heuristics with interval features."""
    print("Testing all heuristics with interval features...")
    
    features = np.array([
        [0, 0, 0, 5, 7, 0, 0, 15, 20, 2],
        [1, 0, 1, 2, 4, 0, 0, 10, 15, 2],
        [2, 0, 2, 6, 9, 0, 0, 20, 25, 2]
    ])
    
    heuristics = [
        SPTHeuristic(),
        LPTHeuristic(),
        MWKRHeuristic(),
        ESTHeuristic(),
        CRHeuristic()
    ]
    
    for heuristic in heuristics:
        action = heuristic.select_action([0, 1, 2], features)
        assert 0 <= action <= 2, f"{heuristic.__class__.__name__} returned invalid action"
    
    print("✓ All heuristics work with interval features")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Heuristics Interval Support Validation")
    print("=" * 60)
    
    tests = [
        test_spt_scalar,
        test_spt_interval,
        test_lpt_interval,
        test_with_scalar_environment,
        test_with_interval_environment,
        test_complete_scheduling,
        test_lexicographic_comparison,
        test_all_heuristics_scalar,
        test_all_heuristics_interval,
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
