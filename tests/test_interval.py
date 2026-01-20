"""
Unit tests for the Interval class.

Tests cover:
- Basic interval creation and validation
- Arithmetic operations (addition, subtraction)
- Component-wise operations (max, min)
- Lexicographic comparison
- Serialization/deserialization
- Edge cases and error handling
"""

import pytest
from jobshop_rl.models.interval import Interval, ensure_interval


class TestIntervalCreation:
    """Test interval creation and validation."""
    
    def test_valid_interval(self):
        """Valid intervals should be created successfully."""
        i = Interval(5, 10)
        assert i.lower == 5
        assert i.upper == 10
    
    def test_degenerate_interval(self):
        """Degenerate intervals (point intervals) are valid."""
        i = Interval(7, 7)
        assert i.lower == 7
        assert i.upper == 7
        assert i.is_degenerate
    
    def test_invalid_interval(self):
        """Intervals with lower > upper should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid interval"):
            Interval(10, 5)
    
    def test_float_conversion(self):
        """Integer inputs should be converted to float."""
        i = Interval(5, 10)
        assert isinstance(i.lower, float)
        assert isinstance(i.upper, float)


class TestIntervalProperties:
    """Test interval properties."""
    
    def test_width(self):
        """Width should be upper - lower."""
        i = Interval(5, 10)
        assert i.width == 5
    
    def test_width_degenerate(self):
        """Degenerate intervals have zero width."""
        i = Interval(7, 7)
        assert i.width == 0
    
    def test_midpoint(self):
        """Midpoint should be average of bounds."""
        i = Interval(4, 10)
        assert i.midpoint == 7
    
    def test_is_degenerate(self):
        """is_degenerate should correctly identify point intervals."""
        assert Interval(5, 5).is_degenerate
        assert not Interval(5, 10).is_degenerate


class TestIntervalAddition:
    """Test interval addition operation."""
    
    def test_add_two_intervals(self):
        """Adding two intervals should use component-wise addition."""
        i1 = Interval(3, 7)
        i2 = Interval(2, 5)
        result = i1 + i2
        assert result.lower == 5  # 3 + 2
        assert result.upper == 12  # 7 + 5
    
    def test_add_interval_scalar(self):
        """Adding interval and scalar."""
        i = Interval(3, 7)
        result = i + 5
        assert result.lower == 8  # 3 + 5
        assert result.upper == 12  # 7 + 5
    
    def test_add_scalar_interval(self):
        """Scalar + interval should work (right addition)."""
        i = Interval(3, 7)
        result = 5 + i
        assert result.lower == 8
        assert result.upper == 12
    
    def test_add_associativity(self):
        """Addition should be associative."""
        i1 = Interval(1, 2)
        i2 = Interval(3, 4)
        i3 = Interval(5, 6)
        
        result1 = (i1 + i2) + i3
        result2 = i1 + (i2 + i3)
        
        assert result1 == result2
    
    def test_sum_intervals(self):
        """Should support sum() on list of intervals."""
        intervals = [Interval(1, 2), Interval(3, 4), Interval(5, 6)]
        result = sum(intervals, Interval(0, 0))
        assert result.lower == 9  # 1 + 3 + 5
        assert result.upper == 12  # 2 + 4 + 6


class TestIntervalSubtraction:
    """Test interval subtraction operation."""
    
    def test_subtract_intervals(self):
        """Subtracting intervals should handle worst-case bounds."""
        i1 = Interval(10, 15)
        i2 = Interval(3, 5)
        result = i1 - i2
        # Lower: 10 - 5 = 5 (subtract upper for worst case)
        # Upper: 15 - 3 = 12 (subtract lower for best case)
        assert result.lower == 5
        assert result.upper == 12
    
    def test_subtract_scalar(self):
        """Subtracting scalar from interval."""
        i = Interval(10, 15)
        result = i - 3
        assert result.lower == 7
        assert result.upper == 12


class TestIntervalMaximum:
    """Test interval component-wise maximum operation."""
    
    def test_max_two_intervals(self):
        """Component-wise max of two intervals."""
        i1 = Interval(5, 10)
        i2 = Interval(3, 12)
        result = Interval.max(i1, i2)
        assert result.lower == 5  # max(5, 3)
        assert result.upper == 12  # max(10, 12)
    
    def test_max_interval_scalar(self):
        """Max of interval and scalar."""
        i = Interval(3, 7)
        result = Interval.max(i, 5)
        assert result.lower == 5  # max(3, 5)
        assert result.upper == 7  # max(7, 5)
    
    def test_max_multiple_intervals(self):
        """Max of multiple intervals."""
        i1 = Interval(1, 5)
        i2 = Interval(3, 4)
        i3 = Interval(2, 10)
        result = Interval.max(i1, i2, i3)
        assert result.lower == 3  # max(1, 3, 2)
        assert result.upper == 10  # max(5, 4, 10)
    
    def test_max_degenerate_returns_scalar(self):
        """Max of degenerate interval should return scalar."""
        i1 = Interval(5, 5)
        i2 = Interval(3, 3)
        result = Interval.max(i1, i2)
        assert result == 5
        assert isinstance(result, (int, float))


class TestIntervalMinimum:
    """Test interval component-wise minimum operation."""
    
    def test_min_two_intervals(self):
        """Component-wise min of two intervals."""
        i1 = Interval(5, 10)
        i2 = Interval(3, 12)
        result = Interval.min(i1, i2)
        assert result.lower == 3  # min(5, 3)
        assert result.upper == 10  # min(10, 12)
    
    def test_min_degenerate_returns_scalar(self):
        """Min of degenerate interval should return scalar."""
        i1 = Interval(5, 5)
        i2 = Interval(7, 7)
        result = Interval.min(i1, i2)
        assert result == 5


class TestLexicographicComparison:
    """Test lexicographic ordering for optimization."""
    
    def test_less_than_upper_bound(self):
        """Primary comparison: upper bounds."""
        i1 = Interval(5, 8)
        i2 = Interval(3, 10)
        assert i1 < i2  # 8 < 10
    
    def test_less_than_lower_bound(self):
        """Secondary comparison: lower bounds when uppers equal."""
        i1 = Interval(3, 10)
        i2 = Interval(5, 10)
        assert i1 < i2  # Uppers equal, 3 < 5
    
    def test_equal_intervals(self):
        """Equal intervals should not be less than."""
        i1 = Interval(5, 10)
        i2 = Interval(5, 10)
        assert not (i1 < i2)
        assert i1 == i2
    
    def test_greater_than(self):
        """Greater than comparison."""
        i1 = Interval(5, 12)
        i2 = Interval(3, 10)
        assert i1 > i2  # 12 > 10
    
    def test_less_equal(self):
        """Less than or equal comparison."""
        i1 = Interval(5, 10)
        i2 = Interval(5, 10)
        assert i1 <= i2
        
        i3 = Interval(3, 8)
        assert i3 <= i1
    
    def test_greater_equal(self):
        """Greater than or equal comparison."""
        i1 = Interval(5, 10)
        i2 = Interval(5, 10)
        assert i1 >= i2
        
        i3 = Interval(7, 12)
        assert i3 >= i1
    
    def test_comparison_with_scalar(self):
        """Comparing interval with scalar."""
        i = Interval(5, 10)
        assert i > 9  # (10, 5) > (9, 9)
        assert not (i < 9)
        assert i < 11  # (10, 5) < (11, 11)


class TestIntervalEquality:
    """Test equality and hashing."""
    
    def test_equality(self):
        """Equal intervals should be equal."""
        i1 = Interval(5, 10)
        i2 = Interval(5, 10)
        assert i1 == i2
    
    def test_inequality_lower(self):
        """Intervals with different lower bounds are not equal."""
        i1 = Interval(5, 10)
        i2 = Interval(6, 10)
        assert i1 != i2
    
    def test_inequality_upper(self):
        """Intervals with different upper bounds are not equal."""
        i1 = Interval(5, 10)
        i2 = Interval(5, 11)
        assert i1 != i2
    
    def test_equality_with_scalar(self):
        """Degenerate interval equals its value."""
        i = Interval(5, 5)
        assert i == 5
    
    def test_hash_consistency(self):
        """Equal intervals should have same hash."""
        i1 = Interval(5, 10)
        i2 = Interval(5, 10)
        assert hash(i1) == hash(i2)
    
    def test_use_in_set(self):
        """Intervals should be usable in sets."""
        i1 = Interval(5, 10)
        i2 = Interval(5, 10)
        i3 = Interval(3, 7)
        
        s = {i1, i2, i3}
        assert len(s) == 2  # i1 and i2 are equal


class TestIntervalString:
    """Test string representations."""
    
    def test_repr(self):
        """repr should show constructor form."""
        i = Interval(5, 10)
        assert repr(i) == "Interval(5.0, 10.0)"
    
    def test_str_interval(self):
        """str should show bracket notation for intervals."""
        i = Interval(5, 10)
        assert str(i) == "[5.0, 10.0]"
    
    def test_str_degenerate(self):
        """str should show single value for degenerate intervals."""
        i = Interval(7, 7)
        assert str(i) == "7.0"


class TestIntervalSerialization:
    """Test serialization and deserialization."""
    
    def test_to_dict(self):
        """Convert to dictionary."""
        i = Interval(5, 10)
        d = i.to_dict()
        assert d == {'lower': 5.0, 'upper': 10.0}
    
    def test_from_dict(self):
        """Create from dictionary."""
        d = {'lower': 5, 'upper': 10}
        i = Interval.from_dict(d)
        assert i.lower == 5
        assert i.upper == 10
    
    def test_to_tuple(self):
        """Convert to tuple."""
        i = Interval(5, 10)
        t = i.to_tuple()
        assert t == (5.0, 10.0)
    
    def test_from_tuple(self):
        """Create from tuple."""
        t = (5, 10)
        i = Interval.from_tuple(t)
        assert i.lower == 5
        assert i.upper == 10
    
    def test_roundtrip_dict(self):
        """Roundtrip through dictionary."""
        i1 = Interval(5.5, 10.7)
        i2 = Interval.from_dict(i1.to_dict())
        assert i1 == i2
    
    def test_roundtrip_tuple(self):
        """Roundtrip through tuple."""
        i1 = Interval(5.5, 10.7)
        i2 = Interval.from_tuple(i1.to_tuple())
        assert i1 == i2


class TestIntervalUtilities:
    """Test utility methods."""
    
    def test_contains(self):
        """Test if value is in interval."""
        i = Interval(5, 10)
        assert i.contains(7)
        assert i.contains(5)
        assert i.contains(10)
        assert not i.contains(3)
        assert not i.contains(12)
    
    def test_overlaps(self):
        """Test if two intervals overlap."""
        i1 = Interval(5, 10)
        i2 = Interval(7, 12)
        assert i1.overlaps(i2)
        
        i3 = Interval(11, 15)
        assert not i1.overlaps(i3)
        
        i4 = Interval(10, 15)
        assert i1.overlaps(i4)  # Touch at boundary
    
    def test_intersection(self):
        """Test interval intersection."""
        i1 = Interval(5, 10)
        i2 = Interval(7, 12)
        result = i1.intersection(i2)
        assert result.lower == 7
        assert result.upper == 10
    
    def test_intersection_no_overlap(self):
        """Intersection of non-overlapping intervals should raise error."""
        i1 = Interval(5, 10)
        i2 = Interval(11, 15)
        with pytest.raises(ValueError, match="do not overlap"):
            i1.intersection(i2)


class TestIntervalMultiplication:
    """Test interval multiplication by scalar."""
    
    def test_multiply_positive(self):
        """Multiply by positive scalar."""
        i = Interval(3, 7)
        result = i * 2
        assert result.lower == 6
        assert result.upper == 14
    
    def test_multiply_negative(self):
        """Multiply by negative scalar reverses bounds."""
        i = Interval(3, 7)
        result = i * -2
        assert result.lower == -14  # -2 * 7
        assert result.upper == -6   # -2 * 3
    
    def test_multiply_zero(self):
        """Multiply by zero."""
        i = Interval(3, 7)
        result = i * 0
        assert result.lower == 0
        assert result.upper == 0
    
    def test_right_multiply(self):
        """Right multiplication (scalar * interval)."""
        i = Interval(3, 7)
        result = 2 * i
        assert result.lower == 6
        assert result.upper == 14


class TestEnsureInterval:
    """Test the ensure_interval utility function."""
    
    def test_interval_passthrough(self):
        """Interval should pass through unchanged."""
        i = Interval(5, 10)
        result = ensure_interval(i)
        assert result is i
    
    def test_scalar_conversion(self):
        """Scalar should convert to degenerate interval."""
        result = ensure_interval(5)
        assert isinstance(result, Interval)
        assert result.lower == 5
        assert result.upper == 5
        assert result.is_degenerate
    
    def test_float_conversion(self):
        """Float should convert to degenerate interval."""
        result = ensure_interval(5.5)
        assert result.lower == 5.5
        assert result.upper == 5.5
    
    def test_invalid_type(self):
        """Invalid type should raise TypeError."""
        with pytest.raises(TypeError):
            ensure_interval("invalid")


class TestIntervalMonotonicity:
    """Test monotonicity properties required for correctness."""
    
    def test_addition_monotonicity(self):
        """If A ≤ B, then A + C ≤ B + C (lexicographically)."""
        a = Interval(3, 8)
        b = Interval(4, 10)
        c = Interval(2, 5)
        
        assert a < b
        assert (a + c) < (b + c)
    
    def test_max_monotonicity(self):
        """Max should preserve ordering in some sense."""
        i1 = Interval(3, 8)
        i2 = Interval(5, 7)
        
        # Component-wise max
        result = Interval.max(i1, i2)
        
        # Result should be at least as large as both inputs
        assert result.lower >= i1.lower or result.lower >= i2.lower
        assert result.upper >= i1.upper or result.upper >= i2.upper


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_zero_width_interval(self):
        """Zero-width intervals should work correctly."""
        i = Interval(5, 5)
        assert i.width == 0
        assert i.is_degenerate
    
    def test_very_large_values(self):
        """Large values should work."""
        i = Interval(1e10, 1e11)
        assert i.lower == 1e10
        assert i.upper == 1e11
    
    def test_very_small_values(self):
        """Small positive values should work."""
        i = Interval(1e-10, 1e-9)
        assert i.lower == 1e-10
        assert i.upper == 1e-9
    
    def test_negative_intervals(self):
        """Negative values should work."""
        i = Interval(-10, -5)
        assert i.lower == -10
        assert i.upper == -5
    
    def test_mixed_sign_intervals(self):
        """Intervals spanning zero should work."""
        i = Interval(-5, 5)
        assert i.lower == -5
        assert i.upper == 5
        assert i.width == 10


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
