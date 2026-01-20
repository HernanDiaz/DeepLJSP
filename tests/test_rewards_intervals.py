"""
Tests for reward components with interval support.

Tests cover:
- All reward components with scalar values
- All reward components with interval values
- Proper scalar extraction from intervals
- Lexicographic comparison in rewards
- Problem analysis with intervals
"""

import sys
import os
import numpy as np
import pytest

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


class TestMakespanRewardComponent:
    """Test makespan reward component with intervals."""
    
    def test_makespan_reward_scalar(self):
        """Makespan reward with scalar problem."""
        problem = get_test_3x3_deterministic()
        analysis = ProblemAnalyzer.analyze_problem(
            problem['sequences'],
            problem['durations']
        )
        
        component = MakespanRewardComponent(weight=1.0, problem_analysis=analysis)
        
        # Create mock environment
        class MockEnv:
            job_completion_time = [10, 15, 20]
        
        env = MockEnv()
        state = {}
        next_state = {}
        info = {}
        
        # Should only reward when done=True
        reward_not_done = component.calculate(env, state, next_state, 0, done=False, info=info)
        assert reward_not_done == 0
        
        # When done, should give negative reward (we want to minimize makespan)
        reward_done = component.calculate(env, state, next_state, 0, done=True, info=info)
        assert reward_done < 0
    
    def test_makespan_reward_interval(self):
        """Makespan reward with interval problem."""
        problem = get_test_3x3_interval()
        analysis = ProblemAnalyzer.analyze_problem(
            problem['sequences'],
            problem['durations']
        )
        
        component = MakespanRewardComponent(weight=1.0, problem_analysis=analysis)
        
        # Create mock environment with interval completion times
        class MockEnv:
            job_completion_time = [
                Interval(10, 12),
                Interval(15, 18),
                Interval(20, 25)  # Max (lexicographically)
            ]
        
        env = MockEnv()
        state = {}
        next_state = {}
        info = {}
        
        # When done, should give negative reward based on upper bound
        reward_done = component.calculate(env, state, next_state, 0, done=True, info=info)
        assert reward_done < 0
    
    def test_makespan_improvement_tracking(self):
        """Makespan component tracks best seen makespan."""
        component = MakespanRewardComponent(weight=1.0)
        
        class MockEnv:
            job_completion_time = [Interval(20, 25)]
        
        env = MockEnv()
        
        # First completion
        component.calculate(env, {}, {}, 0, done=True, info={})
        assert component.best_seen_makespan == Interval(20, 25)
        
        # Better makespan (lexicographically)
        env.job_completion_time = [Interval(18, 22)]
        component.calculate(env, {}, {}, 0, done=True, info={})
        assert component.best_seen_makespan == Interval(18, 22)


class TestIdleTimeRewardComponent:
    """Test idle time reward component with intervals."""
    
    def test_idle_time_scalar(self):
        """Idle time reward with scalar values."""
        component = IdleTimeRewardComponent(weight=0.2)
        
        state = {
            'eligible_ops': [0],
            'job_status': [0],
            'job_completion_time': [5],
            'machine_completion_time': [0, 0, 0]
        }
        
        next_state = {}
        
        class MockEnv:
            sequences = [[0, 1, 2]]
        
        env = MockEnv()
        
        # No idle time (job ready at 5, machine at 0, so start at 5)
        # Idle time = 5 - 0 = 5
        reward = component.calculate(env, state, next_state, 0, done=False, info={})
        assert reward < 0  # Penalize idle time
    
    def test_idle_time_interval(self):
        """Idle time reward with interval values."""
        component = IdleTimeRewardComponent(weight=0.2)
        
        state = {
            'eligible_ops': [0],
            'job_status': [0],
            'job_completion_time': [Interval(5, 7)],
            'machine_completion_time': [Interval(0, 0), Interval(0, 0), Interval(0, 0)]
        }
        
        next_state = {}
        
        class MockEnv:
            sequences = [[0, 1, 2]]
        
        env = MockEnv()
        
        # Idle time will be an interval
        reward = component.calculate(env, state, next_state, 0, done=False, info={})
        assert reward < 0  # Penalize idle time
    
    def test_no_idle_time(self):
        """No idle time when machine ready after job."""
        component = IdleTimeRewardComponent(weight=0.2)
        
        state = {
            'eligible_ops': [0],
            'job_status': [0],
            'job_completion_time': [Interval(0, 0)],
            'machine_completion_time': [Interval(5, 7), Interval(0, 0), Interval(0, 0)]
        }
        
        next_state = {}
        
        class MockEnv:
            sequences = [[0, 1, 2]]
        
        env = MockEnv()
        
        # No idle time (machine already ahead)
        reward = component.calculate(env, state, next_state, 0, done=False, info={})
        assert reward == 0  # No penalty when no idle time


class TestProgressRewardComponent:
    """Test progress reward component (independent of intervals)."""
    
    def test_progress_reward(self):
        """Progress reward is independent of interval/scalar."""
        component = ProgressRewardComponent(weight=0.2)
        
        state = {
            'eligible_ops': [0],
            'job_status': [1, 2, 3]  # 6 operations completed
        }
        
        next_state = {}
        
        class MockEnv:
            num_jobs = 3
            num_machines = 3  # Total: 9 operations
        
        env = MockEnv()
        
        # Progress = 6/9 = 0.667
        reward = component.calculate(env, state, next_state, 0, done=False, info={})
        assert reward > 0  # Positive reward for progress


class TestLocalImprovementRewardComponent:
    """Test local improvement reward component with intervals."""
    
    def test_local_improvement_scalar(self):
        """Local improvement with scalar values."""
        component = LocalImprovementRewardComponent(weight=0.15)
        
        state = {'eligible_ops': [0]}
        next_state = {'machine_completion_time': [10, 15, 20]}
        
        # First call - no previous makespan
        reward1 = component.calculate(None, state, next_state, 0, done=False, info={})
        assert reward1 == 0
        
        # Second call - improvement
        next_state2 = {'machine_completion_time': [10, 15, 18]}
        reward2 = component.calculate(None, state, next_state2, 0, done=False, info={})
        assert reward2 > 0  # Reward for improvement
        
        # Third call - no improvement
        next_state3 = {'machine_completion_time': [10, 15, 19]}
        reward3 = component.calculate(None, state, next_state3, 0, done=False, info={})
        assert reward3 == 0  # No reward when worse
    
    def test_local_improvement_interval(self):
        """Local improvement with interval values."""
        component = LocalImprovementRewardComponent(weight=0.15)
        
        state = {'eligible_ops': [0]}
        next_state = {
            'machine_completion_time': [
                Interval(10, 12),
                Interval(15, 18),
                Interval(20, 25)
            ]
        }
        
        # First call
        reward1 = component.calculate(None, state, next_state, 0, done=False, info={})
        assert reward1 == 0
        
        # Second call - improvement (lexicographically)
        next_state2 = {
            'machine_completion_time': [
                Interval(10, 12),
                Interval(15, 18),
                Interval(18, 22)  # Better upper bound
            ]
        }
        reward2 = component.calculate(None, state, next_state2, 0, done=False, info={})
        assert reward2 > 0


class TestBalanceRewardComponent:
    """Test balance reward component with intervals."""
    
    def test_balance_scalar(self):
        """Balance reward with scalar values."""
        component = BalanceRewardComponent(weight=0.05)
        
        state = {'eligible_ops': [0]}
        
        # Balanced completion times
        next_state_balanced = {'machine_completion_time': [10, 10, 10]}
        reward_balanced = component.calculate(None, state, next_state_balanced, 0, done=False, info={})
        
        # Unbalanced completion times
        next_state_unbalanced = {'machine_completion_time': [5, 15, 25]}
        reward_unbalanced = component.calculate(None, state, next_state_unbalanced, 0, done=False, info={})
        
        # Balanced should be better (less negative)
        assert reward_balanced > reward_unbalanced
    
    def test_balance_interval(self):
        """Balance reward with interval values."""
        component = BalanceRewardComponent(weight=0.05)
        
        state = {'eligible_ops': [0]}
        
        # Balanced (uses upper bounds for std calculation)
        next_state = {
            'machine_completion_time': [
                Interval(10, 12),
                Interval(10, 13),
                Interval(10, 11)
            ]
        }
        
        reward = component.calculate(None, state, next_state, 0, done=False, info={})
        assert reward < 0  # Penalty for imbalance (even small)


class TestCriticalityRewardComponent:
    """Test criticality reward component with intervals."""
    
    def test_criticality_scalar(self):
        """Criticality reward with scalar durations."""
        component = CriticalityRewardComponent(weight=0.1)
        
        state = {
            'eligible_ops': [0],
            'job_status': [0]  # First operation
        }
        
        class MockEnv:
            num_machines = 3
            durations = [[5, 3, 7]]  # Remaining: [3, 7]
        
        env = MockEnv()
        
        reward = component.calculate(env, state, {}, 0, done=False, info={})
        assert reward > 0  # Positive reward for criticality
    
    def test_criticality_interval(self):
        """Criticality reward with interval durations."""
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
        assert reward > 0  # Uses upper bounds of remaining time


class TestWithEnvironment:
    """Test reward components integrated with environment."""
    
    def test_makespan_with_scalar_env(self):
        """Makespan reward with scalar environment."""
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
        
        # Complete a schedule
        env.reset()
        done = False
        while not done:
            if len(env.eligible_ops) > 0:
                state = env._get_state()
                next_state, reward, done, info = env.step(0)
        
        # Calculate reward at completion
        final_reward = component.calculate(
            env,
            state={},
            next_state={},
            action=0,
            done=True,
            info=info
        )
        
        assert final_reward < 0  # Negative reward for makespan
    
    def test_makespan_with_interval_env(self):
        """Makespan reward with interval environment."""
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
        
        # Complete a schedule
        env.reset()
        done = False
        while not done:
            if len(env.eligible_ops) > 0:
                state = env._get_state()
                next_state, reward, done, info = env.step(0)
        
        # Calculate reward at completion
        final_reward = component.calculate(
            env,
            state={},
            next_state={},
            action=0,
            done=True,
            info=info
        )
        
        assert final_reward < 0  # Negative reward
        assert isinstance(info['makespan'], Interval)


# Simple runner for manual testing
if __name__ == '__main__':
    print("=" * 70)
    print("Reward Components Integration Tests (Intervals)")
    print("=" * 70)
    
    # Run a few quick tests
    test_classes = [
        TestMakespanRewardComponent(),
        TestIdleTimeRewardComponent(),
        TestProgressRewardComponent(),
        TestLocalImprovementRewardComponent(),
        TestBalanceRewardComponent(),
        TestCriticalityRewardComponent(),
        TestWithEnvironment()
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"\n{class_name}:")
        
        # Get all test methods
        test_methods = [m for m in dir(test_class) if m.startswith('test_')]
        
        for method_name in test_methods:
            try:
                method = getattr(test_class, method_name)
                method()
                print(f"  ✓ {method_name}")
                passed += 1
            except Exception as e:
                print(f"  ✗ {method_name}: {e}")
                import traceback
                traceback.print_exc()
                failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    sys.exit(0 if failed == 0 else 1)
