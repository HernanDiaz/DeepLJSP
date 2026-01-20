"""
Tests for heuristic strategies with interval support.

Tests cover:
- All heuristic types with scalar features
- All heuristic types with interval features
- Lexicographic comparison for intervals
- OR-Tools fallback for interval problems
- Feature extraction (7D vs 10D)
"""

import sys
import os
import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.heuristics.strategies import (
    SPTHeuristic,
    LPTHeuristic,
    MORHeuristic,
    MWKRHeuristic,
    ESTHeuristic,
    CRHeuristic,
    RandomHeuristic,
    ORToolsHeuristic,
    HeuristicFactory
)
from jobshop_rl.models.interval import Interval
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.data.test_3x3_interval import (
    get_test_3x3_interval,
    get_test_3x3_deterministic
)


class TestScalarHeuristics:
    """Test heuristics with scalar (7D) features."""
    
    def test_spt_scalar(self):
        """SPT heuristic with scalar features."""
        # Features: [job_id, op_idx, machine, duration, earliest_start, remaining_time, remaining_ops]
        features = np.array([
            [0, 0, 0, 5.0, 0, 15, 2],
            [1, 0, 1, 3.0, 0, 10, 2],  # Shortest
            [2, 0, 2, 7.0, 0, 20, 2]
        ])
        
        heuristic = SPTHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 1 (shortest duration = 3)
        assert action == 1
    
    def test_lpt_scalar(self):
        """LPT heuristic with scalar features."""
        features = np.array([
            [0, 0, 0, 5.0, 0, 15, 2],
            [1, 0, 1, 3.0, 0, 10, 2],
            [2, 0, 2, 7.0, 0, 20, 2]  # Longest
        ])
        
        heuristic = LPTHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 2 (longest duration = 7)
        assert action == 2
    
    def test_mwkr_scalar(self):
        """MWKR heuristic with scalar features."""
        features = np.array([
            [0, 0, 0, 5.0, 0, 15, 2],
            [1, 0, 1, 3.0, 0, 10, 2],
            [2, 0, 2, 7.0, 0, 20, 2]  # Most work remaining
        ])
        
        heuristic = MWKRHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 2 (most remaining time = 20)
        assert action == 2
    
    def test_est_scalar(self):
        """EST heuristic with scalar features."""
        features = np.array([
            [0, 0, 0, 5.0, 5, 15, 2],
            [1, 0, 1, 3.0, 0, 10, 2],  # Earliest start
            [2, 0, 2, 7.0, 8, 20, 2]
        ])
        
        heuristic = ESTHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 1 (earliest start = 0)
        assert action == 1


class TestIntervalHeuristics:
    """Test heuristics with interval (10D) features."""
    
    def test_spt_interval(self):
        """SPT heuristic with interval features."""
        # Features: [job_id, op_idx, machine, 
        #           dur_lower, dur_upper,
        #           start_lower, start_upper,
        #           remain_lower, remain_upper,
        #           remaining_ops]
        features = np.array([
            [0, 0, 0, 5, 7, 0, 0, 15, 20, 2],   # [5,7]
            [1, 0, 1, 2, 4, 0, 0, 10, 15, 2],   # [2,4] - Shortest (lex)
            [2, 0, 2, 6, 9, 0, 0, 20, 25, 2]    # [6,9]
        ])
        
        heuristic = SPTHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 1 (lexicographically smallest: [2,4])
        # Comparison: (4,2) < (7,5) < (9,6)
        assert action == 1
    
    def test_lpt_interval(self):
        """LPT heuristic with interval features."""
        features = np.array([
            [0, 0, 0, 5, 7, 0, 0, 15, 20, 2],
            [1, 0, 1, 2, 4, 0, 0, 10, 15, 2],
            [2, 0, 2, 6, 9, 0, 0, 20, 25, 2]    # Longest (lex)
        ])
        
        heuristic = LPTHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 2 (lexicographically largest: [6,9])
        assert action == 2
    
    def test_mwkr_interval(self):
        """MWKR heuristic with interval features."""
        features = np.array([
            [0, 0, 0, 5, 7, 0, 0, 15, 20, 2],
            [1, 0, 1, 2, 4, 0, 0, 10, 15, 2],
            [2, 0, 2, 6, 9, 0, 0, 20, 25, 2]    # Most work remaining
        ])
        
        heuristic = MWKRHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 2 (lexicographically largest remaining: [20,25])
        assert action == 2
    
    def test_est_interval(self):
        """EST heuristic with interval features."""
        features = np.array([
            [0, 0, 0, 5, 7, 5, 8, 15, 20, 2],
            [1, 0, 1, 2, 4, 0, 0, 10, 15, 2],   # Earliest start [0,0]
            [2, 0, 2, 6, 9, 8, 10, 20, 25, 2]
        ])
        
        heuristic = ESTHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 1 (lexicographically smallest start: [0,0])
        assert action == 1


class TestLexicographicComparison:
    """Test lexicographic comparison for intervals."""
    
    def test_spt_lexicographic_upper_priority(self):
        """SPT should prioritize upper bound in comparison."""
        features = np.array([
            [0, 0, 0, 5, 10, 0, 0, 15, 20, 2],  # [5,10]
            [1, 0, 1, 4, 8, 0, 0, 10, 15, 2],   # [4,8] - Chosen (smaller upper)
            [2, 0, 2, 6, 8, 0, 0, 20, 25, 2]    # [6,8]
        ])
        
        heuristic = SPTHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # [4,8] and [6,8] both have upper=8
        # Should choose [4,8] because lower=4 < lower=6
        assert action == 1
    
    def test_lpt_lexicographic_upper_priority(self):
        """LPT should prioritize upper bound in comparison."""
        features = np.array([
            [0, 0, 0, 5, 10, 0, 0, 15, 20, 2],  # [5,10] - Chosen (largest upper)
            [1, 0, 1, 7, 10, 0, 0, 10, 15, 2],  # [7,10]
            [2, 0, 2, 6, 8, 0, 0, 20, 25, 2]
        ])
        
        heuristic = LPTHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # [5,10] and [7,10] both have upper=10
        # Should choose [7,10] because lower=7 > lower=5
        assert action == 1


class TestWithEnvironment:
    """Test heuristics integrated with environment."""
    
    def test_spt_with_scalar_env(self):
        """SPT heuristic with scalar environment."""
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
        
        heuristic = SPTHeuristic()
        action = heuristic.select_action(env.eligible_ops, features)
        
        # Should return valid action index
        assert 0 <= action < len(env.eligible_ops)
    
    def test_spt_with_interval_env(self):
        """SPT heuristic with interval environment."""
        problem = get_test_3x3_interval()
        env = JobShopEnv(
            num_jobs=problem['num_jobs'],
            num_machines=problem['num_machines'],
            sequences=problem['sequences'],
            durations=problem['durations']
        )
        
        state = env.reset()
        features = env.get_features(state)
        
        # Should have 10 features per operation
        assert features.shape[1] == 10
        
        heuristic = SPTHeuristic()
        action = heuristic.select_action(env.eligible_ops, features)
        
        # Should return valid action index
        assert 0 <= action < len(env.eligible_ops)
    
    def test_complete_scheduling_with_heuristic(self):
        """Complete scheduling run with heuristic."""
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
        
        # Should complete successfully
        assert done
        assert isinstance(info['makespan'], Interval)


class TestORToolsFallback:
    """Test OR-Tools fallback for interval problems."""
    
    def test_ortools_disabled_for_intervals(self):
        """OR-Tools should fall back to SPT for interval problems."""
        problem = get_test_3x3_interval()
        
        heuristic = ORToolsHeuristic(
            sequences=problem['sequences'],
            durations=problem['durations'],
            has_intervals=True
        )
        
        # Create interval features
        features = np.array([
            [0, 0, 0, 5, 7, 0, 0, 15, 20, 2],
            [1, 0, 1, 2, 4, 0, 0, 10, 15, 2],
            [2, 0, 2, 6, 9, 0, 0, 20, 25, 2]
        ])
        
        # Should use SPT fallback (select shortest)
        action = heuristic.select_action([0, 1, 2], features)
        
        # SPT should select job 1
        assert action == 1


class TestCRHeuristic:
    """Test Critical Ratio heuristic."""
    
    def test_cr_scalar(self):
        """CR heuristic with scalar features."""
        features = np.array([
            [0, 0, 0, 5.0, 0, 20, 4],  # CR = 20/4 = 5.0
            [1, 0, 1, 3.0, 0, 10, 5],  # CR = 10/5 = 2.0 (smallest)
            [2, 0, 2, 7.0, 0, 30, 3]   # CR = 30/3 = 10.0
        ])
        
        heuristic = CRHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 1 (smallest CR)
        assert action == 1
    
    def test_cr_interval(self):
        """CR heuristic with interval features (uses upper bound)."""
        features = np.array([
            [0, 0, 0, 5, 7, 0, 0, 18, 22, 4],   # CR = 22/4 = 5.5
            [1, 0, 1, 2, 4, 0, 0, 8, 12, 5],    # CR = 12/5 = 2.4 (smallest)
            [2, 0, 2, 6, 9, 0, 0, 27, 33, 3]    # CR = 33/3 = 11.0
        ])
        
        heuristic = CRHeuristic()
        action = heuristic.select_action([0, 1, 2], features)
        
        # Should select job 1 (smallest CR using upper bounds)
        assert action == 1


class TestHeuristicFactory:
    """Test heuristic factory."""
    
    def test_create_spt(self):
        """Factory creates SPT heuristic."""
        heuristic = HeuristicFactory.create_heuristic("spt")
        assert isinstance(heuristic, SPTHeuristic)
    
    def test_create_lpt(self):
        """Factory creates LPT heuristic."""
        heuristic = HeuristicFactory.create_heuristic("lpt")
        assert isinstance(heuristic, LPTHeuristic)
    
    def test_create_with_intervals_flag(self):
        """Factory creates OR-Tools with intervals flag."""
        heuristic = HeuristicFactory.create_heuristic(
            "ortools",
            sequences=[[0, 1]],
            durations=[[Interval(5, 7), Interval(3, 5)]],
            has_intervals=True
        )
        assert isinstance(heuristic, ORToolsHeuristic)
        assert heuristic.has_intervals == True


# Simple runner for manual testing
if __name__ == '__main__':
    print("=" * 70)
    print("Heuristics Integration Tests (Intervals)")
    print("=" * 70)
    
    # Run a few quick tests
    test_classes = [
        TestScalarHeuristics(),
        TestIntervalHeuristics(),
        TestLexicographicComparison(),
        TestWithEnvironment(),
        TestORToolsFallback(),
        TestCRHeuristic(),
        TestHeuristicFactory()
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
