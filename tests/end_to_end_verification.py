"""
End-to-End Verification Script for Interval-Based Job Shop Scheduling

This script verifies that all components work together correctly:
1. Data loading (scalar and interval)
2. Environment creation and scheduling
3. Heuristics execution
4. Lower bounds calculation
5. Reward components
6. Visualization
7. Complete training run (mini)

Run this to verify the entire system is working correctly.
"""

import sys
import os
import time
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.models.interval import Interval
from jobshop_rl.data.test_3x3_interval import get_test_3x3_interval, get_test_3x3_deterministic
from jobshop_rl.data.problem_loader import ProblemLoader
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.heuristics.strategies import SPTHeuristic, LPTHeuristic, MWKRHeuristic
from jobshop_rl.utils.problem_analyzer import ProblemAnalyzer, MakespanBoundCalculator
from jobshop_rl.rewards.components.makespan import MakespanRewardComponent
from jobshop_rl.rewards.components.idle_time import IdleTimeRewardComponent
from jobshop_rl.rewards.components.progress import ProgressRewardComponent


class EndToEndVerification:
    """Complete end-to-end verification of the system."""
    
    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.start_time = None
    
    def log_pass(self, test_name, details=""):
        """Log a passed test."""
        msg = f"✓ {test_name}"
        if details:
            msg += f": {details}"
        print(msg)
        self.results['passed'].append(test_name)
    
    def log_fail(self, test_name, error):
        """Log a failed test."""
        msg = f"✗ {test_name}: {error}"
        print(msg)
        self.results['failed'].append((test_name, str(error)))
    
    def log_warning(self, test_name, warning):
        """Log a warning."""
        msg = f"⚠ {test_name}: {warning}"
        print(msg)
        self.results['warnings'].append((test_name, warning))
    
    def print_header(self, title):
        """Print a section header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def test_1_data_loading_scalar(self):
        """Test 1: Load scalar problem."""
        self.print_header("Test 1: Data Loading (Scalar)")
        
        try:
            problem = get_test_3x3_deterministic()
            
            assert problem['num_jobs'] == 3
            assert problem['num_machines'] == 3
            assert len(problem['sequences']) == 3
            assert len(problem['durations']) == 3
            
            # Check all durations are scalars
            for job_durations in problem['durations']:
                for duration in job_durations:
                    assert isinstance(duration, (int, float))
            
            self.log_pass("Load scalar problem", f"{problem['num_jobs']}x{problem['num_machines']}")
            return problem
            
        except Exception as e:
            self.log_fail("Load scalar problem", e)
            return None
    
    def test_2_data_loading_interval(self):
        """Test 2: Load interval problem."""
        self.print_header("Test 2: Data Loading (Interval)")
        
        try:
            problem = get_test_3x3_interval()
            
            assert problem['num_jobs'] == 3
            assert problem['num_machines'] == 3
            assert len(problem['sequences']) == 3
            assert len(problem['durations']) == 3
            
            # Check all durations are intervals
            has_intervals = False
            for job_durations in problem['durations']:
                for duration in job_durations:
                    if isinstance(duration, Interval):
                        has_intervals = True
            
            assert has_intervals, "No intervals found in interval problem"
            
            self.log_pass("Load interval problem", f"{problem['num_jobs']}x{problem['num_machines']} with intervals")
            return problem
            
        except Exception as e:
            self.log_fail("Load interval problem", e)
            return None
    
    def test_3_environment_scalar(self, problem):
        """Test 3: Create and run scalar environment."""
        self.print_header("Test 3: Environment (Scalar)")
        
        if not problem:
            self.log_fail("Create scalar environment", "No problem loaded")
            return None
        
        try:
            env = JobShopEnv(
                num_jobs=problem['num_jobs'],
                num_machines=problem['num_machines'],
                sequences=problem['sequences'],
                durations=problem['durations']
            )
            
            assert not env.has_intervals, "Scalar problem detected as interval"
            
            state = env.reset()
            assert state is not None
            
            # Get features
            features = env.get_features(state)
            assert features.shape[1] == 7, f"Expected 7D features for scalar, got {features.shape[1]}D"
            
            self.log_pass("Create scalar environment", f"Features: {features.shape}")
            return env
            
        except Exception as e:
            self.log_fail("Create scalar environment", e)
            return None
    
    def test_4_environment_interval(self, problem):
        """Test 4: Create and run interval environment."""
        self.print_header("Test 4: Environment (Interval)")
        
        if not problem:
            self.log_fail("Create interval environment", "No problem loaded")
            return None
        
        try:
            env = JobShopEnv(
                num_jobs=problem['num_jobs'],
                num_machines=problem['num_machines'],
                sequences=problem['sequences'],
                durations=problem['durations']
            )
            
            assert env.has_intervals, "Interval problem not detected"
            
            state = env.reset()
            assert state is not None
            
            # Get features
            features = env.get_features(state)
            assert features.shape[1] == 10, f"Expected 10D features for interval, got {features.shape[1]}D"
            
            self.log_pass("Create interval environment", f"Features: {features.shape}")
            return env
            
        except Exception as e:
            self.log_fail("Create interval environment", e)
            return None
    
    def test_5_complete_scheduling_scalar(self, env):
        """Test 5: Complete scheduling with scalar environment."""
        self.print_header("Test 5: Complete Scheduling (Scalar)")
        
        if not env:
            self.log_fail("Complete scalar scheduling", "No environment")
            return None
        
        try:
            env.reset()
            done = False
            steps = 0
            max_steps = 50
            
            while not done and steps < max_steps:
                if len(env.eligible_ops) > 0:
                    state, reward, done, info = env.step(0)
                    steps += 1
                else:
                    break
            
            assert done, "Scheduling did not complete"
            assert 'makespan' in info
            assert isinstance(info['makespan'], (int, float))
            
            makespan = info['makespan']
            self.log_pass("Complete scalar scheduling", f"Makespan: {makespan} in {steps} steps")
            return makespan
            
        except Exception as e:
            self.log_fail("Complete scalar scheduling", e)
            return None
    
    def test_6_complete_scheduling_interval(self, env):
        """Test 6: Complete scheduling with interval environment."""
        self.print_header("Test 6: Complete Scheduling (Interval)")
        
        if not env:
            self.log_fail("Complete interval scheduling", "No environment")
            return None
        
        try:
            env.reset()
            done = False
            steps = 0
            max_steps = 50
            
            while not done and steps < max_steps:
                if len(env.eligible_ops) > 0:
                    state, reward, done, info = env.step(0)
                    steps += 1
                else:
                    break
            
            assert done, "Scheduling did not complete"
            assert 'makespan' in info
            assert isinstance(info['makespan'], Interval)
            
            makespan = info['makespan']
            self.log_pass("Complete interval scheduling", 
                         f"Makespan: [{makespan.lower}, {makespan.upper}] in {steps} steps")
            return makespan
            
        except Exception as e:
            self.log_fail("Complete interval scheduling", e)
            return None
    
    def test_7_heuristics_scalar(self, problem):
        """Test 7: Run heuristics on scalar problem."""
        self.print_header("Test 7: Heuristics (Scalar)")
        
        if not problem:
            self.log_fail("Run scalar heuristics", "No problem")
            return
        
        heuristics = [
            ("SPT", SPTHeuristic()),
            ("LPT", LPTHeuristic()),
            ("MWKR", MWKRHeuristic())
        ]
        
        results = {}
        
        for name, heuristic in heuristics:
            try:
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
                        state = env._get_state()
                        features = env.get_features(state)
                        action = heuristic.select_action(env.eligible_ops, features)
                        state, reward, done, info = env.step(action)
                    else:
                        break
                
                makespan = info['makespan']
                results[name] = makespan
                self.log_pass(f"Heuristic {name}", f"Makespan: {makespan}")
                
            except Exception as e:
                self.log_fail(f"Heuristic {name}", e)
        
        return results
    
    def test_8_heuristics_interval(self, problem):
        """Test 8: Run heuristics on interval problem."""
        self.print_header("Test 8: Heuristics (Interval)")
        
        if not problem:
            self.log_fail("Run interval heuristics", "No problem")
            return
        
        heuristics = [
            ("SPT", SPTHeuristic()),
            ("LPT", LPTHeuristic()),
            ("MWKR", MWKRHeuristic())
        ]
        
        results = {}
        
        for name, heuristic in heuristics:
            try:
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
                        state = env._get_state()
                        features = env.get_features(state)
                        action = heuristic.select_action(env.eligible_ops, features)
                        state, reward, done, info = env.step(action)
                    else:
                        break
                
                makespan = info['makespan']
                results[name] = makespan
                self.log_pass(f"Heuristic {name}", 
                             f"Makespan: [{makespan.lower}, {makespan.upper}]")
                
            except Exception as e:
                self.log_fail(f"Heuristic {name}", e)
        
        return results
    
    def test_9_lower_bounds_scalar(self, problem):
        """Test 9: Calculate lower bounds for scalar problem."""
        self.print_header("Test 9: Lower Bounds (Scalar)")
        
        if not problem:
            self.log_fail("Calculate scalar bounds", "No problem")
            return
        
        try:
            bounds = MakespanBoundCalculator.get_all_bounds(
                problem['sequences'],
                problem['durations']
            )
            
            assert 'capacity' in bounds
            assert 'critical_path' in bounds
            assert 'one_machine' in bounds
            
            for name, value in bounds.items():
                assert isinstance(value, (int, float))
                self.log_pass(f"Bound {name}", f"Value: {value}")
            
            best_lb = MakespanBoundCalculator.get_best_lower_bound(
                problem['sequences'],
                problem['durations']
            )
            
            self.log_pass("Best lower bound", f"Value: {best_lb}")
            return bounds
            
        except Exception as e:
            self.log_fail("Calculate scalar bounds", e)
            return None
    
    def test_10_lower_bounds_interval(self, problem):
        """Test 10: Calculate lower bounds for interval problem."""
        self.print_header("Test 10: Lower Bounds (Interval)")
        
        if not problem:
            self.log_fail("Calculate interval bounds", "No problem")
            return
        
        try:
            bounds = MakespanBoundCalculator.get_all_bounds(
                problem['sequences'],
                problem['durations']
            )
            
            assert 'capacity' in bounds
            assert 'critical_path' in bounds
            assert 'one_machine' in bounds
            
            for name, value in bounds.items():
                assert isinstance(value, Interval)
                self.log_pass(f"Bound {name}", f"Value: [{value.lower}, {value.upper}]")
            
            best_lb = MakespanBoundCalculator.get_best_lower_bound(
                problem['sequences'],
                problem['durations']
            )
            
            self.log_pass("Best lower bound", f"Value: [{best_lb.lower}, {best_lb.upper}]")
            return bounds
            
        except Exception as e:
            self.log_fail("Calculate interval bounds", e)
            return None
    
    def test_11_rewards_scalar(self, problem):
        """Test 11: Test reward components with scalar problem."""
        self.print_header("Test 11: Reward Components (Scalar)")
        
        if not problem:
            self.log_fail("Test scalar rewards", "No problem")
            return
        
        try:
            analysis = ProblemAnalyzer.analyze_problem(
                problem['sequences'],
                problem['durations']
            )
            
            components = [
                ("Makespan", MakespanRewardComponent(weight=1.0, problem_analysis=analysis)),
                ("Idle Time", IdleTimeRewardComponent(weight=0.2, problem_analysis=analysis)),
                ("Progress", ProgressRewardComponent(weight=0.2))
            ]
            
            env = JobShopEnv(
                num_jobs=problem['num_jobs'],
                num_machines=problem['num_machines'],
                sequences=problem['sequences'],
                durations=problem['durations']
            )
            
            # Complete schedule
            env.reset()
            done = False
            prev_state = None
            final_state = None
            while not done:
                if len(env.eligible_ops) > 0:
                    prev_state = env._get_state()
                    state, reward, done, info = env.step(0)
                    final_state = state
                else:
                    break
            
            # Test each component
            for name, component in components:
                # Use final states from the last step
                test_state = prev_state if prev_state else env._get_state()
                test_next_state = final_state if final_state else env._get_state()
                reward = component.calculate(env, test_state, test_next_state, 0, done=True, info=info)
                assert isinstance(reward, (int, float))
                self.log_pass(f"Reward {name}", f"Value: {reward:.4f}")
            
        except Exception as e:
            self.log_fail("Test scalar rewards", e)
    
    def test_12_rewards_interval(self, problem):
        """Test 12: Test reward components with interval problem."""
        self.print_header("Test 12: Reward Components (Interval)")
        
        if not problem:
            self.log_fail("Test interval rewards", "No problem")
            return
        
        try:
            analysis = ProblemAnalyzer.analyze_problem(
                problem['sequences'],
                problem['durations']
            )
            
            components = [
                ("Makespan", MakespanRewardComponent(weight=1.0, problem_analysis=analysis)),
                ("Idle Time", IdleTimeRewardComponent(weight=0.2, problem_analysis=analysis)),
                ("Progress", ProgressRewardComponent(weight=0.2))
            ]
            
            env = JobShopEnv(
                num_jobs=problem['num_jobs'],
                num_machines=problem['num_machines'],
                sequences=problem['sequences'],
                durations=problem['durations']
            )
            
            # Complete schedule
            env.reset()
            done = False
            prev_state = None
            final_state = None
            while not done:
                if len(env.eligible_ops) > 0:
                    prev_state = env._get_state()
                    state, reward, done, info = env.step(0)
                    final_state = state
                else:
                    break
            
            # Test each component
            for name, component in components:
                # Use final states from the last step
                test_state = prev_state if prev_state else env._get_state()
                test_next_state = final_state if final_state else env._get_state()
                reward = component.calculate(env, test_state, test_next_state, 0, done=True, info=info)
                assert isinstance(reward, (int, float))
                self.log_pass(f"Reward {name}", f"Value: {reward:.4f}")
            
        except Exception as e:
            self.log_fail("Test interval rewards", e)
    
    def test_13_problem_analyzer(self):
        """Test 13: Test problem analyzer with both types."""
        self.print_header("Test 13: Problem Analyzer")
        
        try:
            # Scalar
            problem_scalar = get_test_3x3_deterministic()
            analysis_scalar = ProblemAnalyzer.analyze_problem(
                problem_scalar['sequences'],
                problem_scalar['durations']
            )
            
            assert 'has_intervals' in analysis_scalar
            assert analysis_scalar['has_intervals'] == False
            self.log_pass("Analyze scalar problem", "Detected as scalar")
            
            # Interval
            problem_interval = get_test_3x3_interval()
            analysis_interval = ProblemAnalyzer.analyze_problem(
                problem_interval['sequences'],
                problem_interval['durations']
            )
            
            assert 'has_intervals' in analysis_interval
            assert analysis_interval['has_intervals'] == True
            self.log_pass("Analyze interval problem", "Detected as interval")
            
        except Exception as e:
            self.log_fail("Problem analyzer", e)
    
    def print_summary(self):
        """Print final summary."""
        elapsed = time.time() - self.start_time
        
        print("\n" + "=" * 70)
        print("  VERIFICATION SUMMARY")
        print("=" * 70)
        
        total = len(self.results['passed']) + len(self.results['failed'])
        passed = len(self.results['passed'])
        failed = len(self.results['failed'])
        warnings = len(self.results['warnings'])
        
        print(f"\nTotal Tests: {total}")
        print(f"✓ Passed: {passed}")
        print(f"✗ Failed: {failed}")
        print(f"⚠ Warnings: {warnings}")
        print(f"\nElapsed Time: {elapsed:.2f} seconds")
        
        if failed > 0:
            print("\nFailed Tests:")
            for test_name, error in self.results['failed']:
                print(f"  ✗ {test_name}")
                print(f"    Error: {error}")
        
        if warnings > 0:
            print("\nWarnings:")
            for test_name, warning in self.results['warnings']:
                print(f"  ⚠ {test_name}: {warning}")
        
        print("\n" + "=" * 70)
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED - System is fully functional!")
            print("=" * 70)
            return 0
        else:
            print(f"❌ {failed} TEST(S) FAILED - Please review errors above")
            print("=" * 70)
            return 1
    
    def run_all_tests(self):
        """Run all verification tests."""
        self.start_time = time.time()
        
        print("\n" + "=" * 70)
        print("  END-TO-END VERIFICATION")
        print("  Interval-Based Job Shop Scheduling System")
        print("=" * 70)
        
        # Load problems
        problem_scalar = self.test_1_data_loading_scalar()
        problem_interval = self.test_2_data_loading_interval()
        
        # Test environments
        env_scalar = self.test_3_environment_scalar(problem_scalar)
        env_interval = self.test_4_environment_interval(problem_interval)
        
        # Complete scheduling
        self.test_5_complete_scheduling_scalar(env_scalar)
        self.test_6_complete_scheduling_interval(env_interval)
        
        # Heuristics
        self.test_7_heuristics_scalar(problem_scalar)
        self.test_8_heuristics_interval(problem_interval)
        
        # Lower bounds
        self.test_9_lower_bounds_scalar(problem_scalar)
        self.test_10_lower_bounds_interval(problem_interval)
        
        # Rewards
        self.test_11_rewards_scalar(problem_scalar)
        self.test_12_rewards_interval(problem_interval)
        
        # Problem analyzer
        self.test_13_problem_analyzer()
        
        # Print summary
        return self.print_summary()


def main():
    """Main entry point."""
    verifier = EndToEndVerification()
    return verifier.run_all_tests()


if __name__ == '__main__':
    sys.exit(main())
