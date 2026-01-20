"""
Tests for lower bound calculations with interval support.

Tests cover:
- Lower bound calculations for scalar problems
- Lower bound calculations for interval problems  
- Validation that LB ⪯ makespan (lexicographically)
- Problem analysis with intervals
- All three bound types (capacity, critical path, one-machine)
"""

import sys
import os
import pytest

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
from jobshop_rl.data.ft10_interval import get_ft10_interval_problem


class TestScalarLowerBounds:
    """Test lower bounds for scalar (deterministic) problems."""
    
    def test_capacity_bound_scalar(self):
        """Capacity bound for scalar problem."""
        sequences = [[0, 1], [1, 0]]
        durations = [[5, 3], [4, 2]]
        
        bound = MakespanBoundCalculator.capacity_bound(sequences, durations)
        
        # Machine 0: 5 + 2 = 7
        # Machine 1: 3 + 4 = 7
        assert bound == 7
        assert isinstance(bound, (int, float))
    
    def test_critical_path_bound_scalar(self):
        """Critical path bound for scalar problem."""
        sequences = [[0, 1], [1, 0]]
        durations = [[5, 3], [4, 2]]
        
        bound = MakespanBoundCalculator.critical_path_bound(sequences, durations)
        
        # Job 0: 5 + 3 = 8
        # Job 1: 4 + 2 = 6
        assert bound == 8
        assert isinstance(bound, (int, float))
    
    def test_one_machine_relaxation_scalar(self):
        """One-machine relaxation bound for scalar problem."""
        sequences = [[0, 1], [1, 0]]
        durations = [[5, 3], [4, 2]]
        
        bound = MakespanBoundCalculator.one_machine_relaxation(sequences, durations)
        
        assert bound >= 0
        assert isinstance(bound, (int, float))
    
    def test_get_all_bounds_scalar(self):
        """Get all bounds for scalar problem."""
        sequences = [[0, 1], [1, 0]]
        durations = [[5, 3], [4, 2]]
        
        bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
        
        assert "capacity" in bounds
        assert "critical_path" in bounds
        assert "one_machine" in bounds
        
        # All should be scalars
        for bound_name, bound_value in bounds.items():
            assert isinstance(bound_value, (int, float))
    
    def test_best_lower_bound_scalar(self):
        """Best lower bound for scalar problem."""
        sequences = [[0, 1], [1, 0]]
        durations = [[5, 3], [4, 2]]
        
        best_bound = MakespanBoundCalculator.get_best_lower_bound(sequences, durations)
        
        # Should be max of all bounds
        all_bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
        assert best_bound == max(all_bounds.values())


class TestIntervalLowerBounds:
    """Test lower bounds for interval problems."""
    
    def test_capacity_bound_interval(self):
        """Capacity bound for interval problem."""
        sequences = [[0, 1], [1, 0]]
        durations = [
            [Interval(5, 7), Interval(3, 5)],
            [Interval(4, 6), Interval(2, 3)]
        ]
        
        bound = MakespanBoundCalculator.capacity_bound(sequences, durations)
        
        # Should return an Interval
        assert isinstance(bound, Interval)
        
        # Machine 0: [5,7] + [2,3] = [7,10]
        # Machine 1: [3,5] + [4,6] = [7,11]
        # Max is [7,11]
        assert bound.lower == 7
        assert bound.upper == 11
    
    def test_critical_path_bound_interval(self):
        """Critical path bound for interval problem."""
        sequences = [[0, 1], [1, 0]]
        durations = [
            [Interval(5, 7), Interval(3, 5)],
            [Interval(4, 6), Interval(2, 3)]
        ]
        
        bound = MakespanBoundCalculator.critical_path_bound(sequences, durations)
        
        # Should return an Interval
        assert isinstance(bound, Interval)
        
        # Job 0: [5,7] + [3,5] = [8,12]
        # Job 1: [4,6] + [2,3] = [6,9]
        # Max is [8,12] (lexicographic)
        assert bound.lower == 8
        assert bound.upper == 12
    
    def test_one_machine_relaxation_interval(self):
        """One-machine relaxation bound for interval problem."""
        sequences = [[0, 1], [1, 0]]
        durations = [
            [Interval(5, 7), Interval(3, 5)],
            [Interval(4, 6), Interval(2, 3)]
        ]
        
        bound = MakespanBoundCalculator.one_machine_relaxation(sequences, durations)
        
        # Should return an Interval
        assert isinstance(bound, Interval)
        assert bound.lower >= 0
        assert bound.upper >= bound.lower
    
    def test_get_all_bounds_interval(self):
        """Get all bounds for interval problem."""
        sequences = [[0, 1], [1, 0]]
        durations = [
            [Interval(5, 7), Interval(3, 5)],
            [Interval(4, 6), Interval(2, 3)]
        ]
        
        bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
        
        assert "capacity" in bounds
        assert "critical_path" in bounds
        assert "one_machine" in bounds
        
        # All should be Intervals
        for bound_name, bound_value in bounds.items():
            assert isinstance(bound_value, Interval)
            assert bound_value.lower <= bound_value.upper
    
    def test_best_lower_bound_interval(self):
        """Best lower bound for interval problem uses lexicographic comparison."""
        sequences = [[0, 1], [1, 0]]
        durations = [
            [Interval(5, 7), Interval(3, 5)],
            [Interval(4, 6), Interval(2, 3)]
        ]
        
        best_bound = MakespanBoundCalculator.get_best_lower_bound(sequences, durations)
        
        # Should be an Interval
        assert isinstance(best_bound, Interval)
        
        # Should be lexicographically maximum of all bounds
        all_bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
        assert best_bound == max(all_bounds.values())


class TestLowerBoundValidity:
    """Test that lower bounds are valid (LB ⪯ makespan)."""
    
    def test_scalar_bound_validity(self):
        """Scalar lower bound should be ≤ actual makespan."""
        problem = get_test_3x3_deterministic()
        
        # Calculate lower bound
        lb = MakespanBoundCalculator.get_best_lower_bound(
            problem['sequences'],
            problem['durations']
        )
        
        # Create environment and get actual makespan
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
        
        # Lower bound should be ≤ makespan
        assert lb <= makespan
    
    def test_interval_bound_validity(self):
        """Interval lower bound should satisfy LB ⪯ makespan (lexicographically)."""
        problem = get_test_3x3_interval()
        
        # Calculate lower bound
        lb = MakespanBoundCalculator.get_best_lower_bound(
            problem['sequences'],
            problem['durations']
        )
        
        # Create environment and get actual makespan
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
        
        # Both should be Intervals
        assert isinstance(lb, Interval)
        assert isinstance(makespan, Interval)
        
        # Lower bound should be ⪯ makespan (lexicographically)
        # This means: (lb.upper, lb.lower) <= (makespan.upper, makespan.lower)
        assert lb <= makespan or lb == makespan
        
        # Also check component-wise
        assert lb.lower <= makespan.lower
        assert lb.upper <= makespan.upper
    
    def test_capacity_bound_validity(self):
        """Capacity bound should be valid."""
        problem = get_test_3x3_interval()
        
        # Calculate capacity bound
        capacity_lb = MakespanBoundCalculator.capacity_bound(
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
                env.step(0)
                done = all(s == problem['num_machines'] for s in env.job_status)
        
        makespan = max(env.job_completion_time)
        
        # Capacity bound should be ≤ makespan
        assert capacity_lb <= makespan


class TestProblemAnalyzer:
    """Test ProblemAnalyzer with intervals."""
    
    def test_analyze_scalar_problem(self):
        """Analyze scalar problem."""
        problem = get_test_3x3_deterministic()
        
        analysis = ProblemAnalyzer.analyze_problem(
            problem['sequences'],
            problem['durations']
        )
        
        assert analysis['num_jobs'] == 3
        assert analysis['num_machines'] == 3
        assert analysis['has_intervals'] == False
        
        # All metrics should be scalars
        assert isinstance(analysis['total_work'], (int, float))
        assert isinstance(analysis['avg_op_duration'], (int, float))
        assert isinstance(analysis['best_lower_bound'], (int, float))
        
        # Lower bounds dict
        assert 'lower_bounds' in analysis
        for bound_name, bound_value in analysis['lower_bounds'].items():
            assert isinstance(bound_value, (int, float))
    
    def test_analyze_interval_problem(self):
        """Analyze interval problem."""
        problem = get_test_3x3_interval()
        
        analysis = ProblemAnalyzer.analyze_problem(
            problem['sequences'],
            problem['durations']
        )
        
        assert analysis['num_jobs'] == 3
        assert analysis['num_machines'] == 3
        assert analysis['has_intervals'] == True
        
        # Total work should be Interval
        assert isinstance(analysis['total_work'], Interval)
        
        # Best lower bound should be Interval
        assert isinstance(analysis['best_lower_bound'], Interval)
        
        # Max/min op durations should be Intervals
        assert isinstance(analysis['max_op_duration'], Interval)
        assert isinstance(analysis['min_op_duration'], Interval)
        
        # Lower bounds dict should contain Intervals
        for bound_name, bound_value in analysis['lower_bounds'].items():
            assert isinstance(bound_value, Interval)
    
    def test_machine_loads_interval(self):
        """Machine loads should be intervals for interval problems."""
        problem = get_test_3x3_interval()
        
        analysis = ProblemAnalyzer.analyze_problem(
            problem['sequences'],
            problem['durations']
        )
        
        machine_loads = analysis['machine_loads']
        
        # All machine loads should be Intervals
        assert all(isinstance(load, Interval) for load in machine_loads)
        
        # Should have one load per machine
        assert len(machine_loads) == 3
    
    def test_bottleneck_identification(self):
        """Bottleneck machine should be correctly identified."""
        # Create problem with clear bottleneck
        sequences = [[0, 1], [0, 1]]
        durations = [
            [Interval(10, 12), Interval(2, 3)],
            [Interval(8, 10), Interval(1, 2)]
        ]
        
        analysis = ProblemAnalyzer.analyze_problem(sequences, durations)
        
        # Machine 0 should be bottleneck ([10,12] + [8,10] = [18,22])
        # Machine 1 should have less load ([2,3] + [1,2] = [3,5])
        assert analysis['bottleneck_machine'] == 0


class TestBoundComparison:
    """Test comparison of different bound types."""
    
    def test_bounds_ordering_scalar(self):
        """Different bounds may have different values."""
        sequences = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
        durations = [[5, 3, 7], [4, 6, 2], [8, 4, 6]]
        
        bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
        
        capacity = bounds['capacity']
        critical_path = bounds['critical_path']
        one_machine = bounds['one_machine']
        
        # All should be valid
        assert capacity >= 0
        assert critical_path >= 0
        assert one_machine >= 0
        
        # Best should be max of all
        best = max([capacity, critical_path, one_machine])
        assert best == MakespanBoundCalculator.get_best_lower_bound(sequences, durations)
    
    def test_bounds_ordering_interval(self):
        """Different interval bounds may have different values."""
        sequences = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
        durations = [
            [Interval(5, 7), Interval(3, 5), Interval(7, 9)],
            [Interval(4, 6), Interval(6, 8), Interval(2, 4)],
            [Interval(8, 10), Interval(4, 6), Interval(6, 8)]
        ]
        
        bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
        
        capacity = bounds['capacity']
        critical_path = bounds['critical_path']
        one_machine = bounds['one_machine']
        
        # All should be Intervals
        assert isinstance(capacity, Interval)
        assert isinstance(critical_path, Interval)
        assert isinstance(one_machine, Interval)
        
        # All should be valid
        assert capacity.lower >= 0
        assert critical_path.lower >= 0
        assert one_machine.lower >= 0
        
        # Best should be lexicographically maximum
        best = max([capacity, critical_path, one_machine])
        assert best == MakespanBoundCalculator.get_best_lower_bound(sequences, durations)


class TestAdaptiveConfig:
    """Test adaptive configuration generation."""
    
    def test_agent_config_scalar(self):
        """Generate agent config for scalar problem."""
        problem = get_test_3x3_deterministic()
        analysis = ProblemAnalyzer.analyze_problem(
            problem['sequences'],
            problem['durations']
        )
        
        from jobshop_rl.utils.problem_analyzer import AdaptiveConfigGenerator
        config = AdaptiveConfigGenerator.generate_agent_config(analysis)
        
        assert 'lr' in config
        assert 'gamma' in config
        assert 'entropy_coef' in config
        assert config['lr'] > 0
    
    def test_agent_config_interval(self):
        """Generate agent config for interval problem."""
        problem = get_test_3x3_interval()
        analysis = ProblemAnalyzer.analyze_problem(
            problem['sequences'],
            problem['durations']
        )
        
        from jobshop_rl.utils.problem_analyzer import AdaptiveConfigGenerator
        config = AdaptiveConfigGenerator.generate_agent_config(analysis)
        
        assert 'lr' in config
        assert 'entropy_coef' in config
        
        # Interval problems should have higher exploration
        # (This is a design choice in the implementation)
        assert config['entropy_coef'] > 0


# Simple runner for manual testing
if __name__ == '__main__':
    print("=" * 70)
    print("Lower Bounds Integration Tests (Intervals)")
    print("=" * 70)
    
    # Run a few quick tests
    test_classes = [
        TestScalarLowerBounds(),
        TestIntervalLowerBounds(),
        TestLowerBoundValidity(),
        TestProblemAnalyzer(),
        TestBoundComparison(),
        TestAdaptiveConfig()
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
