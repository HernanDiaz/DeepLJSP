"""
Integration tests for JobShopEnv with interval support.

Tests cover:
- Environment initialization with intervals
- Schedule construction using interval arithmetic
- Feature extraction (7D vs 10D)
- Makespan calculation
- Backward compatibility with scalar problems
- Visualization for both scalar and interval schedules
"""

import sys
import os
import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.models.interval import Interval
from jobshop_rl.data.test_3x3_interval import (
    get_test_3x3_interval,
    get_test_3x3_deterministic,
    get_test_3x3_partial_interval
)
from jobshop_rl.data.ft10_interval import (
    get_ft10_interval_problem,
    get_ft10_deterministic_as_intervals
)


class TestEnvironmentInitialization:
    """Test environment initialization with different problem types."""
    
    def test_init_with_scalar_problem(self):
        """Initialize environment with scalar durations."""
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
    
    def test_init_with_interval_problem(self):
        """Initialize environment with interval durations."""
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
    
    def test_init_with_degenerate_intervals(self):
        """Initialize with degenerate intervals (should behave like scalars)."""
        problem = get_ft10_deterministic_as_intervals()
        
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        # All intervals are degenerate
        assert not env.has_intervals


class TestEnvironmentReset:
    """Test environment reset behavior."""
    
    def test_reset_scalar_problem(self):
        """Reset should initialize scalar completion times to 0."""
        problem = get_test_3x3_deterministic()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        state = env.reset()
        
        # All completion times should be 0
        assert all(t == 0 for t in env.job_completion_time)
        assert all(t == 0 for t in env.machine_completion_time)
        
        # State should contain completion times
        assert 'job_completion_time' in state
        assert 'machine_completion_time' in state
    
    def test_reset_interval_problem(self):
        """Reset should initialize interval completion times to Interval(0,0)."""
        problem = get_test_3x3_interval()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        state = env.reset()
        
        # All completion times should be Interval(0,0)
        assert all(isinstance(t, Interval) and t.lower == 0 and t.upper == 0 
                  for t in env.job_completion_time)
        assert all(isinstance(t, Interval) and t.lower == 0 and t.upper == 0 
                  for t in env.machine_completion_time)


class TestFeatureExtraction:
    """Test feature extraction for scalar vs interval problems."""
    
    def test_scalar_features_dimension(self):
        """Scalar problems should produce 7D features."""
        problem = get_test_3x3_deterministic()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        state = env.reset()
        features = env.get_features(state)
        
        # Should have 7 features per operation
        assert features.shape[1] == 7
        
        # Should have 3 eligible operations (one per job initially)
        assert features.shape[0] == 3
    
    def test_interval_features_dimension(self):
        """Interval problems should produce 10D features."""
        problem = get_test_3x3_interval()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        state = env.reset()
        features = env.get_features(state)
        
        # Should have 10 features per operation (intervals expanded)
        assert features.shape[1] == 10
        
        # Should have 3 eligible operations
        assert features.shape[0] == 3
    
    def test_interval_features_content(self):
        """Verify interval features are correctly expanded."""
        problem = get_test_3x3_interval()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        state = env.reset()
        features = env.get_features(state)
        
        # First operation features
        first_op = features[0]
        
        # Features should be: [job_id, op_idx, machine, 
        #                      dur_lower, dur_upper,
        #                      start_lower, start_upper,
        #                      remain_lower, remain_upper,
        #                      remaining_ops]
        assert len(first_op) == 10
        
        # job_id should be first job
        assert first_op[0] == 0
        
        # Duration bounds should be from interval
        duration = problem['durations'][0][0]
        assert first_op[3] == duration.lower
        assert first_op[4] == duration.upper


class TestScheduleConstruction:
    """Test schedule construction with interval arithmetic."""
    
    def test_scalar_schedule_construction(self):
        """Construct schedule with scalar durations."""
        problem = get_test_3x3_deterministic()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        env.reset()
        
        # Take a few steps
        for _ in range(3):
            if len(env.eligible_ops) > 0:
                state, reward, done, info = env.step(0)
        
        # Check that schedule history exists
        assert len(env.schedule_history) == 3
        
        # All times should be scalars
        for op in env.schedule_history:
            assert isinstance(op['start'], (int, float))
            assert isinstance(op['end'], (int, float))
    
    def test_interval_schedule_construction(self):
        """Construct schedule with interval durations."""
        problem = get_test_3x3_interval()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        env.reset()
        
        # Take a few steps
        for _ in range(3):
            if len(env.eligible_ops) > 0:
                state, reward, done, info = env.step(0)
        
        # Check that schedule history exists
        assert len(env.schedule_history) == 3
        
        # All times should be intervals
        for op in env.schedule_history:
            assert isinstance(op['start'], Interval)
            assert isinstance(op['end'], Interval)
    
    def test_interval_arithmetic_correctness(self):
        """Verify interval arithmetic is correctly applied."""
        # Create simple 2x2 problem
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
        
        # Schedule Job 0, Op 0 (M0, duration [5,7])
        state, reward, done, info = env.step(0)
        
        # Job 0 should complete at [5,7]
        assert env.job_completion_time[0].lower == 5
        assert env.job_completion_time[0].upper == 7
        
        # Machine 0 should be busy until [5,7]
        assert env.machine_completion_time[0].lower == 5
        assert env.machine_completion_time[0].upper == 7
        
        # Schedule Job 1, Op 0 (M1, duration [4,6])
        state, reward, done, info = env.step(0)  # Now Job 1 is eligible
        
        # Job 1 completes at [4,6]
        assert env.job_completion_time[1].lower == 4
        assert env.job_completion_time[1].upper == 6
    
    def test_precedence_constraints_with_intervals(self):
        """Verify precedence constraints are respected with intervals."""
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
        env.step(0)
        
        # Schedule Job 1, Op 0 (M1, [4,6])
        env.step(0)
        
        # Now schedule Job 0, Op 1 (M1, [3,5])
        # Should start after Job 0 Op 0 ends ([5,7]) AND after M1 is free ([4,6])
        # Max([5,7], [4,6]) = [5,7]
        env.step(0)  # Job 0 Op 1
        
        last_op = env.schedule_history[-1]
        
        # Start should be at least [5,7] (precedence)
        assert last_op['start'].lower >= 5
        assert last_op['start'].upper >= 7


class TestMakespanCalculation:
    """Test makespan calculation for scalar and interval problems."""
    
    def test_scalar_makespan(self):
        """Scalar makespan should be maximum completion time."""
        problem = get_test_3x3_deterministic()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        env.reset()
        
        # Run until completion
        done = False
        while not done:
            if len(env.eligible_ops) > 0:
                state, reward, done, info = env.step(0)
            else:
                break
        
        # Makespan should be scalar
        if done:
            makespan = info['makespan']
            assert isinstance(makespan, (int, float))
            assert makespan > 0
    
    def test_interval_makespan(self):
        """Interval makespan should be maximum interval (lexicographic)."""
        problem = get_test_3x3_interval()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        env.reset()
        
        # Run until completion
        done = False
        while not done:
            if len(env.eligible_ops) > 0:
                state, reward, done, info = env.step(0)
            else:
                break
        
        # Makespan should be interval
        if done:
            makespan = info['makespan']
            assert isinstance(makespan, Interval)
            assert makespan.lower > 0
            assert makespan.upper >= makespan.lower


class TestBackwardCompatibility:
    """Test that degenerate intervals behave like scalars."""
    
    def test_degenerate_intervals_as_scalars(self):
        """Degenerate intervals should produce same results as scalars."""
        # Create two versions: one with scalars, one with degenerate intervals
        sequences = [[0, 1], [1, 0]]
        scalar_durations = [[5, 3], [4, 2]]
        interval_durations = [
            [Interval(5, 5), Interval(3, 3)],
            [Interval(4, 4), Interval(2, 2)]
        ]
        
        # Scalar environment
        env_scalar = JobShopEnv(
            num_jobs=2,
            num_machines=2,
            sequences=sequences,
            durations=scalar_durations
        )
        
        # Interval environment (degenerate)
        env_interval = JobShopEnv(
            num_jobs=2,
            num_machines=2,
            sequences=sequences,
            durations=interval_durations
        )
        
        env_scalar.reset()
        env_interval.reset()
        
        # Take same actions in both
        actions = [0, 0, 0, 0]  # Complete schedule
        
        for action in actions:
            if len(env_scalar.eligible_ops) > 0:
                env_scalar.step(action)
            if len(env_interval.eligible_ops) > 0:
                env_interval.step(action)
        
        # Makespans should be equivalent
        makespan_scalar = max(env_scalar.job_completion_time)
        makespan_interval = max(env_interval.job_completion_time)
        
        # Degenerate interval makespan should equal scalar makespan
        if isinstance(makespan_interval, Interval):
            assert makespan_interval.lower == makespan_scalar
            assert makespan_interval.upper == makespan_scalar


class TestVisualization:
    """Test visualization for scalar and interval schedules."""
    
    def test_render_scalar_schedule(self):
        """Render scalar schedule (traditional Gantt chart)."""
        problem = get_test_3x3_deterministic()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        env.reset()
        
        # Create a simple schedule
        for _ in range(3):
            if len(env.eligible_ops) > 0:
                env.step(0)
        
        # Render should work
        fig = env.render_schedule(title="Test Scalar Schedule")
        assert fig is not None
    
    def test_render_interval_schedule(self):
        """Render interval schedule (parallelogram Gantt chart)."""
        problem = get_test_3x3_interval()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        env.reset()
        
        # Create a simple schedule
        for _ in range(3):
            if len(env.eligible_ops) > 0:
                env.step(0)
        
        # Render should work
        fig = env.render_schedule(title="Test Interval Schedule")
        assert fig is not None
    
    def test_plot_makespan_history_scalar(self):
        """Plot makespan history for scalar problem."""
        problem = get_test_3x3_deterministic()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        env.reset()
        
        # Build makespan history
        for _ in range(3):
            if len(env.eligible_ops) > 0:
                env.step(0)
        
        # Plot should work
        if env.makespan_history:
            fig = env.plot_makespan_history()
            assert fig is not None
    
    def test_plot_makespan_history_interval(self):
        """Plot makespan history for interval problem (with uncertainty bands)."""
        problem = get_test_3x3_interval()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        env.reset()
        
        # Build makespan history
        for _ in range(3):
            if len(env.eligible_ops) > 0:
                env.step(0)
        
        # Plot should work
        if env.makespan_history:
            fig = env.plot_makespan_history()
            assert fig is not None


class TestCompleteScheduling:
    """Test complete scheduling runs."""
    
    def test_complete_3x3_scalar(self):
        """Complete scheduling of 3x3 scalar problem."""
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
        max_steps = 100  # Safety limit
        
        while not done and steps < max_steps:
            if len(env.eligible_ops) > 0:
                state, reward, done, info = env.step(0)
                steps += 1
            else:
                break
        
        # Should complete successfully
        assert done
        assert len(env.schedule_history) == 9  # 3 jobs × 3 machines
        
        # All jobs should be fully scheduled
        assert all(status == 3 for status in env.job_status)
    
    def test_complete_3x3_interval(self):
        """Complete scheduling of 3x3 interval problem."""
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
        max_steps = 100
        
        while not done and steps < max_steps:
            if len(env.eligible_ops) > 0:
                state, reward, done, info = env.step(0)
                steps += 1
            else:
                break
        
        # Should complete successfully
        assert done
        assert len(env.schedule_history) == 9
        
        # Makespan should be interval
        assert isinstance(info['makespan'], Interval)
        
        # All times should be valid intervals
        for op in env.schedule_history:
            assert isinstance(op['start'], Interval)
            assert isinstance(op['end'], Interval)
            assert op['start'].lower <= op['start'].upper
            assert op['end'].lower <= op['end'].upper


# Simple runner for manual testing
if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    
    print("=" * 70)
    print("Environment Integration Tests (Intervals)")
    print("=" * 70)
    
    # Run a few quick tests
    test_classes = [
        TestEnvironmentInitialization(),
        TestEnvironmentReset(),
        TestFeatureExtraction(),
        TestScheduleConstruction(),
        TestMakespanCalculation(),
        TestBackwardCompatibility(),
        TestVisualization(),
        TestCompleteScheduling()
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
