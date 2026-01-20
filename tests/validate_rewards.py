"""
Simple validation script for interval-aware reward components (no pytest required).
Tests basic reward functionality with intervals.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.rewards.components.makespan import MakespanRewardComponent
from jobshop_rl.rewards.components.idle_time import IdleTimeRewardComponent
from jobshop_rl.rewards.components.progress import ProgressRewardComponent
from jobshop_rl.rewards.components.local_improvement import LocalImprovementRewardComponent
from jobshop_rl.rewards.components.balance import BalanceRewardComponent
from jobshop_rl.rewards.components.criticality import CriticalityRewardComponent
from jobshop_rl.models.interval import Interval
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.data.test_3x3_interval import (
    get_test_3x3_interval,
    get_test_3x3_deterministic
)
from jobshop_rl.utils.problem_analyzer import ProblemAnalyzer


def test_makespan_scalar():
    """Test makespan reward with scalar values."""
    print("Testing makespan reward with scalar values...")
    
    component = MakespanRewardComponent(weight=1.0)
    
    class MockEnv:
        job_completion_time = [10, 15, 20]
    
    env = MockEnv()
    
    # Should only reward when done
    reward_not_done = component.calculate(env, {}, {}, 0, done=False, info={})
    assert reward_not_done == 0
    
    reward_done = component.calculate(env, {}, {}, 0, done=True, info={})
    assert reward_done < 0  # Negative (minimize makespan)
    
    print("✓ Makespan reward with scalar values works")


def test_makespan_interval():
    """Test makespan reward with interval values."""
    print("Testing makespan reward with interval values...")
    
    component = MakespanRewardComponent(weight=1.0)
    
    class MockEnv:
        job_completion_time = [
            Interval(10, 12),
            Interval(15, 18),
            Interval(20, 25)
        ]
    
    env = MockEnv()
    
    reward = component.calculate(env, {}, {}, 0, done=True, info={})
    assert reward < 0
    
    print("✓ Makespan reward with interval values works")


def test_idle_time_interval():
    """Test idle time reward with intervals."""
    print("Testing idle time reward with intervals...")
    
    component = IdleTimeRewardComponent(weight=0.2)
    
    state = {
        'eligible_ops': [0],
        'job_status': [0],
        'job_completion_time': [Interval(5, 7)],
        'machine_completion_time': [Interval(0, 0), Interval(0, 0), Interval(0, 0)]
    }
    
    class MockEnv:
        sequences = [[0, 1, 2]]
    
    env = MockEnv()
    
    reward = component.calculate(env, state, {}, 0, done=False, info={})
    assert reward < 0  # Penalty for idle time
    
    print("✓ Idle time reward with intervals works")


def test_progress_reward():
    """Test progress reward (interval-independent)."""
    print("Testing progress reward...")
    
    component = ProgressRewardComponent(weight=0.2)
    
    state = {
        'eligible_ops': [0],
        'job_status': [1, 2, 3]
    }
    
    class MockEnv:
        num_jobs = 3
        num_machines = 3
    
    env = MockEnv()
    
    reward = component.calculate(env, state, {}, 0, done=False, info={})
    assert reward > 0
    
    print("✓ Progress reward works")


def test_local_improvement_interval():
    """Test local improvement with intervals."""
    print("Testing local improvement with intervals...")
    
    component = LocalImprovementRewardComponent(weight=0.15)
    
    state = {'eligible_ops': [0]}
    next_state1 = {
        'machine_completion_time': [
            Interval(10, 12),
            Interval(15, 18),
            Interval(20, 25)
        ]
    }
    
    # First call
    reward1 = component.calculate(None, state, next_state1, 0, done=False, info={})
    assert reward1 == 0
    
    # Improvement
    next_state2 = {
        'machine_completion_time': [
            Interval(10, 12),
            Interval(15, 18),
            Interval(18, 22)
        ]
    }
    reward2 = component.calculate(None, state, next_state2, 0, done=False, info={})
    assert reward2 > 0
    
    print("✓ Local improvement with intervals works")


def test_balance_interval():
    """Test balance reward with intervals."""
    print("Testing balance reward with intervals...")
    
    component = BalanceRewardComponent(weight=0.05)
    
    state = {'eligible_ops': [0]}
    next_state = {
        'machine_completion_time': [
            Interval(10, 12),
            Interval(10, 13),
            Interval(10, 11)
        ]
    }
    
    reward = component.calculate(None, state, next_state, 0, done=False, info={})
    assert reward < 0
    
    print("✓ Balance reward with intervals works")


def test_criticality_interval():
    """Test criticality reward with intervals."""
    print("Testing criticality reward with intervals...")
    
    component = CriticalityRewardComponent(weight=0.1)
    
    state = {
        'eligible_ops': [0],
        'job_status': [0]
    }
    
    class MockEnv:
        num_machines = 3
        durations = [[Interval(5, 7), Interval(3, 5), Interval(7, 9)]]
    
    env = MockEnv()
    
    reward = component.calculate(env, state, {}, 0, done=False, info={})
    assert reward > 0
    
    print("✓ Criticality reward with intervals works")


def test_with_scalar_environment():
    """Test reward components with scalar environment."""
    print("Testing rewards with scalar environment...")
    
    problem = get_test_3x3_deterministic()
    analysis = ProblemAnalyzer.analyze_problem(
        problem['sequences'],
        problem['durations']
    )
    
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    component = MakespanRewardComponent(weight=1.0, problem_analysis=analysis)
    
    # Complete schedule
    env.reset()
    done = False
    while not done:
        if len(env.eligible_ops) > 0:
            state, reward, done, info = env.step(0)
    
    final_reward = component.calculate(env, {}, {}, 0, done=True, info=info)
    assert final_reward < 0
    
    print("✓ Rewards work with scalar environment")


def test_with_interval_environment():
    """Test reward components with interval environment."""
    print("Testing rewards with interval environment...")
    
    problem = get_test_3x3_interval()
    analysis = ProblemAnalyzer.analyze_problem(
        problem['sequences'],
        problem['durations']
    )
    
    env = JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations']
    )
    
    component = MakespanRewardComponent(weight=1.0, problem_analysis=analysis)
    
    # Complete schedule
    env.reset()
    done = False
    while not done:
        if len(env.eligible_ops) > 0:
            state, reward, done, info = env.step(0)
    
    final_reward = component.calculate(env, {}, {}, 0, done=True, info=info)
    assert final_reward < 0
    assert isinstance(info['makespan'], Interval)
    
    print(f"✓ Rewards work with interval environment (makespan: {info['makespan']})")


def test_scalar_extraction():
    """Test scalar extraction from intervals."""
    print("Testing scalar extraction from intervals...")
    
    component = MakespanRewardComponent()
    
    # Scalar
    assert component._get_scalar_value(10.0) == 10.0
    
    # Interval (uses upper)
    assert component._get_scalar_value(Interval(10, 15)) == 15
    
    print("✓ Scalar extraction works")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Reward Components Interval Support Validation")
    print("=" * 60)
    
    tests = [
        test_makespan_scalar,
        test_makespan_interval,
        test_idle_time_interval,
        test_progress_reward,
        test_local_improvement_interval,
        test_balance_interval,
        test_criticality_interval,
        test_with_scalar_environment,
        test_with_interval_environment,
        test_scalar_extraction,
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
