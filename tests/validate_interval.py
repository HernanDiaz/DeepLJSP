"""
Simple validation script for Interval class (doesn't require pytest).
Run this to verify basic functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.models.interval import Interval, ensure_interval


def test_basic_creation():
    """Test basic interval creation."""
    print("Testing interval creation...")
    i = Interval(5, 10)
    assert i.lower == 5
    assert i.upper == 10
    print("✓ Basic creation works")


def test_degenerate():
    """Test degenerate intervals."""
    print("Testing degenerate intervals...")
    i = Interval(7, 7)
    assert i.is_degenerate
    assert i.width == 0
    print("✓ Degenerate intervals work")


def test_addition():
    """Test interval addition."""
    print("Testing addition...")
    i1 = Interval(3, 7)
    i2 = Interval(2, 5)
    result = i1 + i2
    assert result.lower == 5
    assert result.upper == 12
    print("✓ Addition works")


def test_maximum():
    """Test component-wise maximum."""
    print("Testing component-wise maximum...")
    i1 = Interval(5, 10)
    i2 = Interval(3, 12)
    result = Interval.max(i1, i2)
    assert result.lower == 5
    assert result.upper == 12
    print("✓ Component-wise max works")


def test_lexicographic_comparison():
    """Test lexicographic ordering."""
    print("Testing lexicographic comparison...")
    i1 = Interval(5, 8)
    i2 = Interval(3, 10)
    assert i1 < i2  # 8 < 10
    
    i3 = Interval(3, 10)
    i4 = Interval(5, 10)
    assert i3 < i4  # Same upper, 3 < 5
    print("✓ Lexicographic comparison works")


def test_sum_list():
    """Test sum() on list of intervals."""
    print("Testing sum() on intervals...")
    intervals = [Interval(1, 2), Interval(3, 4), Interval(5, 6)]
    result = sum(intervals, Interval(0, 0))
    assert result.lower == 9
    assert result.upper == 12
    print("✓ sum() works on interval lists")


def test_serialization():
    """Test to_dict and from_dict."""
    print("Testing serialization...")
    i1 = Interval(5.5, 10.7)
    d = i1.to_dict()
    i2 = Interval.from_dict(d)
    assert i1 == i2
    print("✓ Serialization works")


def test_ensure_interval():
    """Test ensure_interval utility."""
    print("Testing ensure_interval...")
    i = Interval(5, 10)
    assert ensure_interval(i) is i
    
    scalar = ensure_interval(5)
    assert isinstance(scalar, Interval)
    assert scalar.lower == 5
    assert scalar.upper == 5
    print("✓ ensure_interval works")


def test_invalid_interval():
    """Test that invalid intervals raise error."""
    print("Testing invalid interval detection...")
    try:
        Interval(10, 5)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid interval" in str(e)
    print("✓ Invalid intervals detected")


def test_multiplication():
    """Test interval multiplication."""
    print("Testing multiplication...")
    i = Interval(3, 7)
    result = i * 2
    assert result.lower == 6
    assert result.upper == 14
    
    # Negative scalar
    result2 = i * -2
    assert result2.lower == -14
    assert result2.upper == -6
    print("✓ Multiplication works")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Interval Class Validation")
    print("=" * 60)
    
    tests = [
        test_basic_creation,
        test_degenerate,
        test_addition,
        test_maximum,
        test_lexicographic_comparison,
        test_sum_list,
        test_serialization,
        test_ensure_interval,
        test_invalid_interval,
        test_multiplication,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
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
