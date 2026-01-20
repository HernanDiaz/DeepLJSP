"""
Simple validation script for data loading (no pytest required).
Tests basic interval parsing and problem loading functionality.
"""

import sys
import os
import tempfile
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.data.problem_loader import ProblemLoader
from jobshop_rl.models.interval import Interval
from jobshop_rl.data.test_3x3_interval import get_test_3x3_interval
from jobshop_rl.data.ft10_interval import get_ft10_interval_problem


def test_parse_interval():
    """Test parsing interval from string."""
    print("Testing interval parsing...")
    
    # Scalar
    result = ProblemLoader._parse_duration_value("42")
    assert result == 42, f"Expected 42, got {result}"
    
    # Interval
    result = ProblemLoader._parse_duration_value("(5,10)")
    assert isinstance(result, Interval), "Should be Interval"
    assert result.lower == 5, f"Expected lower=5, got {result.lower}"
    assert result.upper == 10, f"Expected upper=10, got {result.upper}"
    
    print("✓ Interval parsing works")


def test_format_interval():
    """Test formatting interval to string."""
    print("Testing interval formatting...")
    
    # Scalar
    result = ProblemLoader._format_duration_value(42)
    assert result == "42", f"Expected '42', got '{result}'"
    
    # Interval
    interval = Interval(5, 10)
    result = ProblemLoader._format_duration_value(interval)
    assert result == "(5,10)", f"Expected '(5,10)', got '{result}'"
    
    # Degenerate interval
    interval = Interval(7, 7)
    result = ProblemLoader._format_duration_value(interval)
    assert result == "7", f"Expected '7', got '{result}'"
    
    print("✓ Interval formatting works")


def test_load_json_intervals():
    """Test loading JSON with intervals."""
    print("Testing JSON loading with intervals...")
    
    # Create temporary JSON file
    data = {
        'num_jobs': 2,
        'num_machines': 2,
        'sequences': [[0, 1], [1, 0]],
        'durations': [
            [[5, 7], [3, 5]],
            [[6, 8], [4, 6]]
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    
    try:
        problem = ProblemLoader.load_json(temp_path)
        
        assert problem['num_jobs'] == 2
        assert problem['num_machines'] == 2
        assert isinstance(problem['durations'][0][0], Interval)
        assert problem['durations'][0][0].lower == 5
        assert problem['durations'][0][0].upper == 7
        assert problem['has_intervals'] == True
        
        print("✓ JSON loading works")
    finally:
        os.unlink(temp_path)


def test_load_taillard_intervals():
    """Test loading Taillard format with intervals."""
    print("Testing Taillard loading with intervals...")
    
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
        assert problem['has_intervals'] == True
        
        print("✓ Taillard loading works")
    finally:
        os.unlink(temp_path)


def test_save_load_roundtrip():
    """Test save → load roundtrip."""
    print("Testing save/load roundtrip...")
    
    # Get test problem
    original = get_test_3x3_interval()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        # Save
        ProblemLoader.save_problem(original, temp_path, format='json')
        
        # Load
        loaded = ProblemLoader.load_json(temp_path)
        
        # Verify
        assert loaded['num_jobs'] == original['num_jobs']
        assert loaded['num_machines'] == original['num_machines']
        assert isinstance(loaded['durations'][0][0], Interval)
        assert loaded['durations'][0][0].lower == original['durations'][0][0].lower
        assert loaded['durations'][0][0].upper == original['durations'][0][0].upper
        
        print("✓ Save/load roundtrip works")
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_generate_random_intervals():
    """Test random problem generation with intervals."""
    print("Testing random interval problem generation...")
    
    # Deterministic
    problem_det = ProblemLoader.generate_random_problem(
        num_jobs=3,
        num_machines=3,
        uncertainty_ratio=0.0,
        seed=42
    )
    
    assert problem_det['num_jobs'] == 3
    assert not problem_det['has_intervals']
    assert isinstance(problem_det['durations'][0][0], int)
    
    # With intervals
    problem_int = ProblemLoader.generate_random_problem(
        num_jobs=3,
        num_machines=3,
        uncertainty_ratio=0.1,
        seed=42
    )
    
    assert problem_int['num_jobs'] == 3
    assert problem_int['has_intervals']
    assert isinstance(problem_int['durations'][0][0], Interval)
    
    print("✓ Random generation works")


def test_load_test_problems():
    """Test loading predefined test problems."""
    print("Testing predefined test problems...")
    
    # 3x3 interval problem
    problem_3x3 = get_test_3x3_interval()
    assert problem_3x3['num_jobs'] == 3
    assert problem_3x3['has_intervals']
    ProblemLoader._validate_problem_intervals(problem_3x3)
    
    # FT10 interval problem
    problem_ft10 = get_ft10_interval_problem()
    assert problem_ft10['num_jobs'] == 10
    assert problem_ft10['has_intervals']
    ProblemLoader._validate_problem_intervals(problem_ft10)
    
    print("✓ Test problems are valid")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Data Loading Validation")
    print("=" * 60)
    
    tests = [
        test_parse_interval,
        test_format_interval,
        test_load_json_intervals,
        test_load_taillard_intervals,
        test_save_load_roundtrip,
        test_generate_random_intervals,
        test_load_test_problems,
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
