"""
Interval arithmetic for job shop scheduling with uncertain processing times.

This module provides a lightweight Interval class that supports:
- Component-wise arithmetic operations (addition, maximum)
- Lexicographic comparison for optimization
- No probabilistic interpretation - intervals represent hard bounds

Interval Semantics:
- An interval [p⁻, p⁺] represents a processing time that can be anywhere from p⁻ to p⁺
- All operations preserve the interval property (no probabilistic sampling)
- Comparisons use lexicographic ordering: minimize (upper, lower) in that priority
"""

from typing import Union, Tuple, Dict, Any


class Interval:
    """
    Represents an interval [lower, upper] with deterministic arithmetic.
    
    Intervals satisfy the invariant: lower ≤ upper
    
    Operations:
    - Addition: [a⁻, a⁺] + [b⁻, b⁺] = [a⁻ + b⁻, a⁺ + b⁺]
    - Maximum: max([a⁻, a⁺], [b⁻, b⁺]) = [max(a⁻, b⁻), max(a⁺, b⁺)]
    - Comparison: Lexicographic on (upper, lower) tuple
    
    Examples:
        >>> i1 = Interval(5, 10)
        >>> i2 = Interval(3, 7)
        >>> i1 + i2
        Interval(8, 17)
        >>> Interval.max(i1, i2)
        Interval(5, 10)
        >>> i2 < i1  # Lexicographic: (7, 3) < (10, 5)
        True
    """
    
    __slots__ = ['_lower', '_upper']  # Memory optimization
    
    def __init__(self, lower: float, upper: float):
        """
        Initialize an interval.
        
        Args:
            lower: Lower bound of the interval
            upper: Upper bound of the interval
            
        Raises:
            ValueError: If lower > upper (invalid interval)
        """
        if lower > upper:
            raise ValueError(
                f"Invalid interval: lower bound ({lower}) cannot exceed "
                f"upper bound ({upper})"
            )
        self._lower = float(lower)
        self._upper = float(upper)
    
    @property
    def lower(self) -> float:
        """Get the lower bound of the interval."""
        return self._lower
    
    @property
    def upper(self) -> float:
        """Get the upper bound of the interval."""
        return self._upper
    
    @property
    def width(self) -> float:
        """Get the width (uncertainty) of the interval."""
        return self._upper - self._lower
    
    @property
    def midpoint(self) -> float:
        """Get the midpoint of the interval."""
        return (self._lower + self._upper) / 2
    
    @property
    def is_degenerate(self) -> bool:
        """Check if this is a degenerate interval (point interval, no uncertainty)."""
        return self._lower == self._upper
    
    def __add__(self, other: Union['Interval', float, int]) -> 'Interval':
        """
        Add two intervals or an interval and a scalar.
        
        Component-wise addition: [a⁻, a⁺] + [b⁻, b⁺] = [a⁻ + b⁻, a⁺ + b⁺]
        
        Args:
            other: Another interval or a scalar
            
        Returns:
            New interval representing the sum
        """
        if isinstance(other, Interval):
            return Interval(self.lower + other.lower, self.upper + other.upper)
        elif isinstance(other, (int, float)):
            return Interval(self.lower + other, self.upper + other)
        return NotImplemented
    
    def __radd__(self, other: Union['Interval', float, int]) -> 'Interval':
        """
        Right addition (supports sum() on lists of intervals).
        
        This allows: sum([Interval(1,2), Interval(3,4)], Interval(0,0))
        """
        if other == 0:
            # sum() starts with 0, so we return self
            return self
        return self.__add__(other)
    
    def __sub__(self, other: Union['Interval', float, int]) -> 'Interval':
        """
        Subtract two intervals or an interval and a scalar.
        
        [a⁻, a⁺] - [b⁻, b⁺] = [a⁻ - b⁺, a⁺ - b⁻]
        Note: Lower bound subtracts the upper bound of other (worst case)
        """
        if isinstance(other, Interval):
            return Interval(self.lower - other.upper, self.upper - other.lower)
        elif isinstance(other, (int, float)):
            return Interval(self.lower - other, self.upper - other)
        return NotImplemented
    
    @staticmethod
    def max(*intervals: Union['Interval', float, int]) -> Union['Interval', float]:
        """
        Component-wise maximum of intervals.
        
        max([a⁻, a⁺], [b⁻, b⁺]) = [max(a⁻, b⁻), max(a⁺, b⁺)]
        
        This is NOT lexicographic - it's component-wise for propagation.
        
        Args:
            *intervals: Variable number of intervals or scalars
            
        Returns:
            Interval representing the component-wise maximum
            
        Examples:
            >>> Interval.max(Interval(5, 10), Interval(3, 12))
            Interval(5, 12)
            >>> Interval.max(Interval(5, 10), 7)
            Interval(7, 10)
        """
        if not intervals:
            raise ValueError("max() requires at least one argument")
        
        # Convert all to intervals for uniform processing
        interval_list = []
        for item in intervals:
            if isinstance(item, Interval):
                interval_list.append(item)
            elif isinstance(item, (int, float)):
                interval_list.append(Interval(item, item))
            else:
                raise TypeError(f"Cannot compute max with type {type(item)}")
        
        # Component-wise maximum
        max_lower = max(i.lower for i in interval_list)
        max_upper = max(i.upper for i in interval_list)
        
        result = Interval(max_lower, max_upper)
        
        # If result is degenerate, return scalar for backward compatibility
        if result.is_degenerate:
            return result.lower
        return result
    
    @staticmethod
    def min(*intervals: Union['Interval', float, int]) -> Union['Interval', float]:
        """
        Component-wise minimum of intervals.
        
        min([a⁻, a⁺], [b⁻, b⁺]) = [min(a⁻, b⁻), min(a⁺, b⁺)]
        
        Args:
            *intervals: Variable number of intervals or scalars
            
        Returns:
            Interval representing the component-wise minimum
        """
        if not intervals:
            raise ValueError("min() requires at least one argument")
        
        interval_list = []
        for item in intervals:
            if isinstance(item, Interval):
                interval_list.append(item)
            elif isinstance(item, (int, float)):
                interval_list.append(Interval(item, item))
            else:
                raise TypeError(f"Cannot compute min with type {type(item)}")
        
        min_lower = min(i.lower for i in interval_list)
        min_upper = min(i.upper for i in interval_list)
        
        result = Interval(min_lower, min_upper)
        
        if result.is_degenerate:
            return result.lower
        return result
    
    def __lt__(self, other: Union['Interval', float, int]) -> bool:
        """
        Lexicographic less-than comparison.
        
        [a⁻, a⁺] < [b⁻, b⁺] iff:
        - a⁺ < b⁺, OR
        - a⁺ = b⁺ AND a⁻ < b⁻
        
        Priority: minimize upper bound first, then lower bound.
        This implements robust optimization (worst-case first).
        """
        if isinstance(other, Interval):
            return (self.upper, self.lower) < (other.upper, other.lower)
        elif isinstance(other, (int, float)):
            return (self.upper, self.lower) < (other, other)
        return NotImplemented
    
    def __le__(self, other: Union['Interval', float, int]) -> bool:
        """Lexicographic less-than-or-equal comparison."""
        if isinstance(other, Interval):
            return (self.upper, self.lower) <= (other.upper, other.lower)
        elif isinstance(other, (int, float)):
            return (self.upper, self.lower) <= (other, other)
        return NotImplemented
    
    def __gt__(self, other: Union['Interval', float, int]) -> bool:
        """Lexicographic greater-than comparison."""
        if isinstance(other, Interval):
            return (self.upper, self.lower) > (other.upper, other.lower)
        elif isinstance(other, (int, float)):
            return (self.upper, self.lower) > (other, other)
        return NotImplemented
    
    def __ge__(self, other: Union['Interval', float, int]) -> bool:
        """Lexicographic greater-than-or-equal comparison."""
        if isinstance(other, Interval):
            return (self.upper, self.lower) >= (other.upper, other.lower)
        elif isinstance(other, (int, float)):
            return (self.upper, self.lower) >= (other, other)
        return NotImplemented
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison (both bounds must match)."""
        if isinstance(other, Interval):
            return self.lower == other.lower and self.upper == other.upper
        elif isinstance(other, (int, float)):
            return self.is_degenerate and self.lower == other
        return False
    
    def __ne__(self, other: object) -> bool:
        """Inequality comparison."""
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        """Hash function for use in sets/dicts."""
        return hash((self.lower, self.upper))
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Interval({self.lower}, {self.upper})"
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        if self.is_degenerate:
            return f"{self.lower}"
        return f"[{self.lower}, {self.upper}]"
    
    def to_dict(self) -> Dict[str, float]:
        """
        Convert to dictionary for serialization.
        
        Returns:
            Dictionary with 'lower' and 'upper' keys
        """
        return {'lower': self.lower, 'upper': self.upper}
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'Interval':
        """
        Create interval from dictionary.
        
        Args:
            data: Dictionary with 'lower' and 'upper' keys
            
        Returns:
            New Interval instance
        """
        return cls(data['lower'], data['upper'])
    
    def to_tuple(self) -> Tuple[float, float]:
        """
        Convert to tuple for compact representation.
        
        Returns:
            Tuple (lower, upper)
        """
        return (self.lower, self.upper)
    
    @classmethod
    def from_tuple(cls, data: Tuple[float, float]) -> 'Interval':
        """
        Create interval from tuple.
        
        Args:
            data: Tuple (lower, upper)
            
        Returns:
            New Interval instance
        """
        return cls(data[0], data[1])
    
    def contains(self, value: float) -> bool:
        """
        Check if a value is within the interval.
        
        Args:
            value: Value to check
            
        Returns:
            True if lower ≤ value ≤ upper
        """
        return self.lower <= value <= self.upper
    
    def overlaps(self, other: 'Interval') -> bool:
        """
        Check if this interval overlaps with another.
        
        Args:
            other: Another interval
            
        Returns:
            True if intervals have non-empty intersection
        """
        return self.lower <= other.upper and other.lower <= self.upper
    
    def intersection(self, other: 'Interval') -> 'Interval':
        """
        Compute the intersection of two intervals.
        
        Args:
            other: Another interval
            
        Returns:
            Intersection interval
            
        Raises:
            ValueError: If intervals don't overlap
        """
        if not self.overlaps(other):
            raise ValueError(f"Intervals {self} and {other} do not overlap")
        
        return Interval(
            max(self.lower, other.lower),
            min(self.upper, other.upper)
        )
    
    def __mul__(self, scalar: Union[int, float]) -> 'Interval':
        """
        Multiply interval by a scalar.
        
        Args:
            scalar: Multiplication factor
            
        Returns:
            Scaled interval
        """
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        
        if scalar >= 0:
            return Interval(self.lower * scalar, self.upper * scalar)
        else:
            # Negative scalar reverses the order
            return Interval(self.upper * scalar, self.lower * scalar)
    
    def __rmul__(self, scalar: Union[int, float]) -> 'Interval':
        """Right multiplication (scalar * interval)."""
        return self.__mul__(scalar)


def ensure_interval(value: Union[Interval, float, int]) -> Interval:
    """
    Convert a value to an Interval if it isn't already.
    
    Utility function for backward compatibility with scalar values.
    
    Args:
        value: An interval or scalar
        
    Returns:
        Interval representation of the value
    """
    if isinstance(value, Interval):
        return value
    elif isinstance(value, (int, float)):
        return Interval(value, value)
    else:
        raise TypeError(f"Cannot convert {type(value)} to Interval")


def final_makespan(completions):
    """Agregacion CORRECTA del makespan final sobre las terminaciones de trabajo.

    Componente a componente para intervalos ([max lowers, max uppers]),
    max normal para escalares. Devuelve Interval (o float si es degenerado).

    USAR SIEMPRE ESTO en vez de `max(completions)` cuando las terminaciones
    puedan ser Intervalos. `max()` sobre Intervalos usa Interval.__lt__ (orden
    lexicografico por upper) y devuelve el intervalo del trabajo de mayor upper
    -> su lower es demasiado bajo (no es la cota real). Por monotonia del
    makespan en las duraciones, las cotas reales son las esquinas todo-lower
    y todo-upper, es decir [max_j lower_j, max_j upper_j] = Interval.max.

    Debe coincidir con EvaluationIJSP_Makespan (M_COMPONENT) del repositorio.
    """
    return Interval.max(*completions)
