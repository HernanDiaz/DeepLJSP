"""
Integration tests for data loading with interval support.

Tests cover:
- Loading interval problems from different formats
- Saving interval problems to different formats
- Roundtrip testing (save → load → verify)
- Backward compatibility with deterministic problems
- Validation of invalid intervals
"""

import os
import json
import tempfile
import pytest
from typing import Dict, Any

# Import problem loader and interval class
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.data.problem_loader import ProblemLoader
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


class TestIntervalParsing:
    """Test parsing of interval values from strings."""
    
    def test_parse_scalar(self):
        """Parse scalar duration."""
        result = ProblemLoader._parse_duration_value("42")
        assert result == 42
        assert isinstance(result, int)
    
    def test_parse_interval_parentheses(self):
        """Parse interval with parentheses (5,10)."""
        result = ProblemLoader._parse_duration_value("(5,10)")
        assert isinstance(result, Interval)
        assert result.lower == 5
        assert result.upper == 10
    
    def test_parse_interval_brackets(self):
        """Parse interval with brackets [5,10]."""
        result = ProblemLoader._parse_duration_value("[5,10]")
        assert isinstance(result, Interval)
        assert result.lower == 5
        assert result.upper == 10
    
    def test_parse_interval_with_spaces(self):
        """Parse interval with spaces ( 5 , 10 )."""
        result = ProblemLoader._parse_duration_value("( 5 , 10 )")
        assert isinstance(result, Interval)
        assert result.lower == 5
        assert result.upper == 10
    
    def test_parse_float_interval(self):
        """Parse interval with float values."""
        result = ProblemLoader._parse_duration_value("(5.5,10.7)")
        assert isinstance(result, Interval)
        assert result.lower == 5.5
        assert result.upper == 10.7
    
    def test_parse_invalid_interval(self):
        """Invalid interval (lower > upper) should raise error."""
        with pytest.raises(ValueError, match="Intervalo inválido"):
            ProblemLoader._parse_duration_value("(10,5)")
    
    def test_parse_degenerate_interval(self):
        """Parse degenerate interval (point)."""
        result = ProblemLoader._parse_duration_value("(7,7)")
        assert isinstance(result, Interval)
        assert result.is_degenerate
        assert result.lower == 7
        assert result.upper == 7


class TestIntervalFormatting:
    """Test formatting of interval values to strings."""
    
    def test_format_scalar(self):
        """Format scalar to string."""
        result = ProblemLoader._format_duration_value(42)
        assert result == "42"
    
    def test_format_interval(self):
        """Format non-degenerate interval to string."""
        interval = Interval(5, 10)
        result = ProblemLoader._format_duration_value(interval)
        assert result == "(5,10)"
    
    def test_format_degenerate_interval(self):
        """Format degenerate interval as scalar."""
        interval = Interval(7, 7)
        result = ProblemLoader._format_duration_value(interval)
        assert result == "7"
    
    def test_format_float_interval(self):
        """Format interval with float values."""
        interval = Interval(5.5, 10.7)
        result = ProblemLoader._format_duration_value(interval)
        assert result == "(5.5,10.7)"


class TestJSONLoading:
    """Test loading problems from JSON format."""
    
    def test_load_json_scalar_durations(self):
        """Load JSON with scalar durations."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                'num_jobs': 2,
                'num_machines': 2,
                'sequences': [[0, 1], [1, 0]],
                'durations': [[5, 7], [6, 4]]
            }, f)
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_json(temp_path)
            assert problem['num_jobs'] == 2
            assert problem['num_machines'] == 2
            assert problem['durations'][0][0] == 5
            assert not problem['has_intervals']
        finally:
            os.unlink(temp_path)
    
    def test_load_json_interval_array_format(self):
        """Load JSON with intervals as arrays [[lower, upper], ...]."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                'num_jobs': 2,
                'num_machines': 2,
                'sequences': [[0, 1], [1, 0]],
                'durations': [
                    [[5, 7], [3, 5]],
                    [[6, 8], [4, 6]]
                ]
            }, f)
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_json(temp_path)
            assert isinstance(problem['durations'][0][0], Interval)
            assert problem['durations'][0][0].lower == 5
            assert problem['durations'][0][0].upper == 7
            assert problem['has_intervals']
        finally:
            os.unlink(temp_path)
    
    def test_load_json_interval_dict_format(self):
        """Load JSON with intervals as dicts {"lower": x, "upper": y}."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                'num_jobs': 2,
                'num_machines': 2,
                'sequences': [[0, 1], [1, 0]],
                'durations': [
                    [{"lower": 5, "upper": 7}, {"lower": 3, "upper": 5}],
                    [{"lower": 6, "upper": 8}, {"lower": 4, "upper": 6}]
                ]
            }, f)
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_json(temp_path)
            assert isinstance(problem['durations'][0][0], Interval)
            assert problem['durations'][0][0].lower == 5
            assert problem['durations'][0][0].upper == 7
        finally:
            os.unlink(temp_path)
    
    def test_load_json_mixed_durations(self):
        """Load JSON with mix of scalars and intervals."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                'num_jobs': 2,
                'num_machines': 2,
                'sequences': [[0, 1], [1, 0]],
                'durations': [
                    [[5, 7], 4],  # Interval and scalar
                    [6, [4, 6]]   # Scalar and interval
                ]
            }, f)
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_json(temp_path)
            assert isinstance(problem['durations'][0][0], Interval)
            assert isinstance(problem['durations'][0][1], int)
            assert isinstance(problem['durations'][1][0], int)
            assert isinstance(problem['durations'][1][1], Interval)
            assert problem['has_intervals']  # Has at least one interval
        finally:
            os.unlink(temp_path)


class TestTaillardLoading:
    """Test loading problems from Taillard format."""
    
    def test_load_taillard_scalar(self):
        """Load Taillard format with scalar durations."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("2 2\n")
            f.write("0 5 1 7\n")
            f.write("1 6 0 4\n")
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_taillard(temp_path)
            assert problem['num_jobs'] == 2
            assert problem['num_machines'] == 2
            assert problem['durations'][0][0] == 5
            assert not problem['has_intervals']
        finally:
            os.unlink(temp_path)
    
    def test_load_taillard_intervals(self):
        """Load Taillard format with interval durations."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("2 2\n")
            f.write("0 (5,7) 1 (3,5)\n")
            f.write("1 (6,8) 0 (4,6)\n")
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_taillard(temp_path)
            assert problem['num_jobs'] == 2
            assert isinstance(problem['durations'][0][0], Interval)
            assert problem['durations'][0][0].lower == 5
            assert problem['durations'][0][0].upper == 7
            assert problem['has_intervals']
        finally:
            os.unlink(temp_path)
    
    def test_load_taillard_mixed(self):
        """Load Taillard with mix of scalars and intervals."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("2 2\n")
            f.write("0 (5,7) 1 4\n")
            f.write("1 6 0 (4,6)\n")
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_taillard(temp_path)
            assert isinstance(problem['durations'][0][0], Interval)
            assert isinstance(problem['durations'][0][1], int)
            assert problem['durations'][0][1] == 4
            assert problem['has_intervals']
        finally:
            os.unlink(temp_path)
    
    def test_load_taillard_with_optimal(self):
        """Load Taillard with optimal makespan."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("2 2 15\n")
            f.write("0 5 1 7\n")
            f.write("1 6 0 4\n")
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_taillard(temp_path)
            assert problem['optimal_makespan'] == 15
        finally:
            os.unlink(temp_path)


class TestCSVLoading:
    """Test loading problems from CSV format."""
    
    def test_load_csv_scalar(self):
        """Load CSV with scalar durations."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("machine_0,duration_0,machine_1,duration_1\n")
            f.write("0,5,1,7\n")
            f.write("1,6,0,4\n")
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_csv(temp_path)
            assert problem['num_jobs'] == 2
            assert problem['num_machines'] == 2
            assert problem['durations'][0][0] == 5
            assert not problem['has_intervals']
        finally:
            os.unlink(temp_path)
    
    def test_load_csv_min_max_format(self):
        """Load CSV with min/max columns for intervals."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("machine_0,duration_0_min,duration_0_max,machine_1,duration_1_min,duration_1_max\n")
            f.write("0,5,7,1,3,5\n")
            f.write("1,6,8,0,4,6\n")
            temp_path = f.name
        
        try:
            problem = ProblemLoader.load_csv(temp_path)
            assert isinstance(problem['durations'][0][0], Interval)
            assert problem['durations'][0][0].lower == 5
            assert problem['durations'][0][0].upper == 7
            assert problem['has_intervals']
        finally:
            os.unlink(temp_path)


class TestSavingProblems:
    """Test saving problems to different formats."""
    
    def test_save_json_with_intervals(self):
        """Save problem with intervals to JSON."""
        problem = get_test_3x3_interval()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            ProblemLoader.save_problem(problem, temp_path, format='json')
            
            # Load it back
            loaded = ProblemLoader.load_json(temp_path)
            
            assert loaded['num_jobs'] == problem['num_jobs']
            assert loaded['num_machines'] == problem['num_machines']
            assert isinstance(loaded['durations'][0][0], Interval)
            assert loaded['durations'][0][0].lower == problem['durations'][0][0].lower
            assert loaded['durations'][0][0].upper == problem['durations'][0][0].upper
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_save_taillard_with_intervals(self):
        """Save problem with intervals to Taillard format."""
        problem = get_test_3x3_interval()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            ProblemLoader.save_problem(problem, temp_path, format='taillard')
            
            # Load it back
            loaded = ProblemLoader.load_taillard(temp_path)
            
            assert loaded['num_jobs'] == problem['num_jobs']
            assert isinstance(loaded['durations'][0][0], Interval)
            assert loaded['durations'][0][0].lower == problem['durations'][0][0].lower
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_save_csv_with_intervals(self):
        """Save problem with intervals to CSV."""
        problem = get_test_3x3_interval()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            ProblemLoader.save_problem(problem, temp_path, format='csv')
            
            # Load it back
            loaded = ProblemLoader.load_csv(temp_path)
            
            assert loaded['num_jobs'] == problem['num_jobs']
            assert isinstance(loaded['durations'][0][0], Interval)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestRoundtrip:
    """Test save → load roundtrips for all formats."""
    
    def test_roundtrip_json(self):
        """JSON roundtrip test."""
        original = get_test_3x3_interval()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            ProblemLoader.save_problem(original, temp_path, format='json')
            loaded = ProblemLoader.load_json(temp_path)
            
            # Verify structure
            assert loaded['num_jobs'] == original['num_jobs']
            assert loaded['num_machines'] == original['num_machines']
            assert loaded['sequences'] == original['sequences']
            
            # Verify durations
            for j in range(original['num_jobs']):
                for m in range(original['num_machines']):
                    orig_dur = original['durations'][j][m]
                    load_dur = loaded['durations'][j][m]
                    
                    if isinstance(orig_dur, Interval):
                        assert isinstance(load_dur, Interval)
                        assert load_dur.lower == orig_dur.lower
                        assert load_dur.upper == orig_dur.upper
                    else:
                        assert load_dur == orig_dur
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_roundtrip_taillard(self):
        """Taillard roundtrip test."""
        original = get_test_3x3_interval()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            ProblemLoader.save_problem(original, temp_path, format='taillard')
            loaded = ProblemLoader.load_taillard(temp_path)
            
            assert loaded['num_jobs'] == original['num_jobs']
            assert loaded['sequences'] == original['sequences']
            
            # Check first duration
            assert isinstance(loaded['durations'][0][0], Interval)
            assert loaded['durations'][0][0].lower == original['durations'][0][0].lower
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestBackwardCompatibility:
    """Test that deterministic problems still work."""
    
    def test_deterministic_as_intervals(self):
        """Degenerate intervals should work like scalars."""
        problem = get_ft10_deterministic_as_intervals()
        
        # All durations are Interval objects
        assert all(
            isinstance(dur, Interval) 
            for job_durs in problem['durations'] 
            for dur in job_durs
        )
        
        # But all are degenerate
        assert all(
            dur.is_degenerate 
            for job_durs in problem['durations'] 
            for dur in job_durs
        )
        
        # has_intervals should be False for all-degenerate
        assert not problem['has_intervals']
    
    def test_scalar_problem_loading(self):
        """Pure scalar problems should still load correctly."""
        problem = get_test_3x3_deterministic()
        
        # All durations are int
        assert all(
            isinstance(dur, int) 
            for job_durs in problem['durations'] 
            for dur in job_durs
        )
        
        assert not problem['has_intervals']


class TestValidation:
    """Test validation of interval problems."""
    
    def test_invalid_interval_detection(self):
        """Invalid intervals should be detected during loading."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("2 2\n")
            f.write("0 (10,5) 1 7\n")  # Invalid: lower > upper
            f.write("1 6 0 4\n")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="inválido"):
                ProblemLoader.load_taillard(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_interval_validation(self):
        """Test _validate_problem_intervals method."""
        problem = {
            'num_jobs': 2,
            'num_machines': 2,
            'sequences': [[0, 1], [1, 0]],
            'durations': [
                [Interval(5, 7), Interval(3, 5)],
                [Interval(6, 8), Interval(10, 5)]  # Invalid!
            ]
        }
        
        with pytest.raises(ValueError, match="Intervalo inválido"):
            ProblemLoader._validate_problem_intervals(problem)


class TestRandomGeneration:
    """Test random problem generation with intervals."""
    
    def test_generate_deterministic_problem(self):
        """Generate deterministic problem (uncertainty_ratio=0)."""
        problem = ProblemLoader.generate_random_problem(
            num_jobs=3,
            num_machines=3,
            uncertainty_ratio=0.0,
            seed=42
        )
        
        assert problem['num_jobs'] == 3
        assert problem['num_machines'] == 3
        assert not problem['has_intervals']
        
        # All durations should be int
        assert all(
            isinstance(dur, int)
            for job_durs in problem['durations']
            for dur in job_durs
        )
    
    def test_generate_interval_problem(self):
        """Generate problem with intervals (uncertainty_ratio>0)."""
        problem = ProblemLoader.generate_random_problem(
            num_jobs=3,
            num_machines=3,
            uncertainty_ratio=0.1,  # ±10%
            seed=42
        )
        
        assert problem['num_jobs'] == 3
        assert problem['has_intervals']
        
        # All durations should be Interval
        assert all(
            isinstance(dur, Interval)
            for job_durs in problem['durations']
            for dur in job_durs
        )
    
    def test_generate_reproducibility(self):
        """Same seed should produce same problem."""
        problem1 = ProblemLoader.generate_random_problem(
            num_jobs=3,
            num_machines=3,
            uncertainty_ratio=0.1,
            seed=42
        )
        
        problem2 = ProblemLoader.generate_random_problem(
            num_jobs=3,
            num_machines=3,
            uncertainty_ratio=0.1,
            seed=42
        )
        
        # Should be identical
        assert problem1['sequences'] == problem2['sequences']
        
        for j in range(3):
            for m in range(3):
                dur1 = problem1['durations'][j][m]
                dur2 = problem2['durations'][j][m]
                assert dur1 == dur2


class TestTestProblems:
    """Test that test problem files are valid."""
    
    def test_ft10_interval_valid(self):
        """FT10 interval problem should be valid."""
        problem = get_ft10_interval_problem()
        
        assert problem['num_jobs'] == 10
        assert problem['num_machines'] == 10
        assert problem['has_intervals']
        
        # Validate all intervals
        ProblemLoader._validate_problem_intervals(problem)
    
    def test_3x3_problems_valid(self):
        """All 3x3 test problems should be valid."""
        problems = [
            get_test_3x3_interval(),
            get_test_3x3_deterministic(),
            get_test_3x3_partial_interval()
        ]
        
        for problem in problems:
            assert problem['num_jobs'] == 3
            assert problem['num_machines'] == 3
            
            # Validate structure
            ProblemLoader._validate_problem_intervals(problem)


# Simple runner for manual testing
if __name__ == '__main__':
    import sys
    
    print("=" * 70)
    print("Data Loading Integration Tests")
    print("=" * 70)
    
    # Run a few quick tests
    test_classes = [
        TestIntervalParsing(),
        TestJSONLoading(),
        TestTaillardLoading(),
        TestBackwardCompatibility(),
        TestRandomGeneration(),
        TestTestProblems()
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
                failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    sys.exit(0 if failed == 0 else 1)
