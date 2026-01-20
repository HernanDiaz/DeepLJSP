# Interval Quick Start Guide

## Basic Usage

### Creating Intervals

```python
from jobshop_rl.models import Interval

# Create an interval
processing_time = Interval(5, 10)  # [5, 10]

# Degenerate interval (deterministic)
deterministic = Interval(7, 7)  # Represents exactly 7

# From scalar (convenience)
from jobshop_rl.models import ensure_interval
interval = ensure_interval(5)  # Creates Interval(5, 5)
```

### Basic Operations

```python
# Addition (component-wise)
i1 = Interval(3, 7)
i2 = Interval(2, 5)
total = i1 + i2  # Interval(5, 12)

# Maximum (component-wise, for schedule constraints)
start1 = Interval(10, 15)
start2 = Interval(12, 14)
actual_start = Interval.max(start1, start2)  # Interval(12, 15)

# Subtraction
i3 = Interval(20, 30)
i4 = Interval(5, 8)
difference = i3 - i4  # Interval(12, 25)
```

### Comparison (Lexicographic)

```python
# Lexicographic comparison for optimization
makespan1 = Interval(45, 50)
makespan2 = Interval(40, 52)

# Compare: prioritize upper bound, then lower
if makespan2 < makespan1:
    print("makespan2 is better")  # This will print
    # Because: (40, 52) < (45, 50)
    # Upper: 52 > 50, so NO
    # Wait, actually (52, 40) vs (50, 45)
    # 52 > 50, so makespan2 > makespan1

# Let me correct this
makespan1 = Interval(40, 50)
makespan2 = Interval(45, 52)
if makespan1 < makespan2:
    print("makespan1 is better")  # This prints
    # (50, 40) < (52, 45) lexicographically
```

**Lexicographic Rule**: `(upper₁, lower₁) < (upper₂, lower₂)`
- Primary: minimize upper bound (worst case)
- Secondary: minimize lower bound (best case)

### Properties

```python
interval = Interval(5, 10)

# Access bounds
print(interval.lower)  # 5.0
print(interval.upper)  # 10.0

# Computed properties
print(interval.width)     # 5.0 (uncertainty)
print(interval.midpoint)  # 7.5 (center)
print(interval.is_degenerate)  # False

# Check containment
print(interval.contains(7))   # True
print(interval.contains(12))  # False
```

## Common Patterns

### Summing Processing Times

```python
# Calculate total job processing time
operations = [
    Interval(5, 7),
    Interval(3, 4),
    Interval(8, 10)
]

total_time = sum(operations, Interval(0, 0))
print(total_time)  # Interval(16, 21)
```

### Computing Schedule Constraints

```python
# Job precedence constraint
job_completion = Interval(20, 25)

# Machine availability constraint
machine_ready = Interval(18, 22)

# Earliest start is maximum of both
earliest_start = Interval.max(job_completion, machine_ready)
print(earliest_start)  # Interval(20, 25)

# Add processing time
duration = Interval(5, 8)
completion_time = earliest_start + duration
print(completion_time)  # Interval(25, 33)
```

### Finding Best Solution

```python
# Compare multiple makespans lexicographically
solutions = [
    Interval(45, 50),
    Interval(42, 55),
    Interval(48, 52),
]

best = min(solutions)  # Uses lexicographic comparison
print(f"Best makespan: {best}")
```

## Serialization

### To/From Dictionary

```python
interval = Interval(5, 10)

# Serialize
data = interval.to_dict()
print(data)  # {'lower': 5.0, 'upper': 10.0}

# Deserialize
restored = Interval.from_dict(data)
assert restored == interval
```

### To/From Tuple

```python
# Compact representation
interval = Interval(5, 10)
tuple_form = interval.to_tuple()  # (5.0, 10.0)

# Restore
restored = Interval.from_tuple(tuple_form)
```

## Working with Problem Instances

### Creating Interval Problem Data

```python
# Problem with interval durations
problem_data = {
    'num_jobs': 3,
    'num_machines': 3,
    'sequences': [
        [0, 1, 2],
        [1, 0, 2],
        [2, 1, 0]
    ],
    'durations': [
        [Interval(5, 7), Interval(3, 4), Interval(8, 10)],
        [Interval(4, 6), Interval(7, 9), Interval(2, 3)],
        [Interval(6, 8), Interval(5, 6), Interval(9, 11)]
    ]
}
```

### Backward Compatibility

```python
# Deterministic problem (all intervals are points)
deterministic_problem = {
    'num_jobs': 2,
    'num_machines': 2,
    'sequences': [[0, 1], [1, 0]],
    'durations': [
        [Interval(5, 5), Interval(7, 7)],  # Same as [5, 7]
        [Interval(6, 6), Interval(4, 4)]   # Same as [6, 4]
    ]
}

# Or use scalars directly (auto-converted in environment)
scalar_problem = {
    'durations': [[5, 7], [6, 4]]  # Will work with updated loaders
}
```

## Error Handling

### Invalid Intervals

```python
try:
    invalid = Interval(10, 5)  # lower > upper
except ValueError as e:
    print(f"Error: {e}")  # "Invalid interval: lower > upper"
```

### Type Checking

```python
from jobshop_rl.models import ensure_interval

# Safe conversion
def process_duration(value):
    interval = ensure_interval(value)
    # Now guaranteed to be an Interval
    return interval.upper * 1.2  # Add 20% buffer

# Works with both
process_duration(10)  # Converts to Interval(10, 10)
process_duration(Interval(8, 12))  # Uses as-is
```

## Advanced Usage

### Interval Arithmetic

```python
# Multiple operations
i1 = Interval(5, 10)
i2 = Interval(3, 7)
i3 = Interval(2, 4)

# Chain operations
result = (i1 + i2) - i3
# Step 1: i1 + i2 = Interval(8, 17)
# Step 2: Interval(8, 17) - Interval(2, 4) = Interval(4, 15)
```

### Scalar Multiplication

```python
duration = Interval(5, 10)

# Scale up (e.g., parallel machines)
scaled = duration * 2  # Interval(10, 20)

# Negative scaling
reversed = duration * -1  # Interval(-10, -5)
```

### Intersection of Constraints

```python
# Two constraints on same operation
constraint1 = Interval(10, 20)
constraint2 = Interval(15, 25)

# Find overlapping region
feasible = constraint1.intersection(constraint2)
print(feasible)  # Interval(15, 20)
```

## Performance Tips

1. **Reuse Intervals**: Intervals are immutable, safe to reuse
2. **Batch Operations**: Use list comprehensions for multiple operations
3. **Avoid Unnecessary Conversions**: Keep as Interval when possible

```python
# Good: Direct operations
intervals = [Interval(i, i+2) for i in range(10)]
total = sum(intervals, Interval(0, 0))

# Avoid: Converting back and forth
# (Not necessary in most cases)
```

## Common Pitfalls

### ❌ Wrong: Using upper for deterministic value
```python
duration = Interval(5, 10)
# Don't use just upper bound for calculations
wait_time = duration.upper * 2  # Loses information!
```

### ✓ Correct: Keep as interval
```python
duration = Interval(5, 10)
wait_time = duration * 2  # Interval(10, 20) - preserves bounds
```

### ❌ Wrong: Comparing with scalar equality
```python
interval = Interval(5, 10)
if interval == 5:  # False - interval is not scalar
    pass
```

### ✓ Correct: Check if degenerate
```python
interval = Interval(5, 5)
if interval.is_degenerate and interval.lower == 5:
    pass
```

## Examples

### Example 1: Schedule Construction

```python
from jobshop_rl.models import Interval

# Job has three operations with uncertain durations
operations = [
    Interval(5, 7),   # Operation 0
    Interval(3, 5),   # Operation 1
    Interval(8, 10)   # Operation 2
]

# Compute job completion time
job_start = Interval(0, 0)
completion = job_start

for op_duration in operations:
    completion = completion + op_duration

print(f"Job completes in {completion}")
# Output: Job completes in [16.0, 22.0]
```

### Example 2: Machine Scheduling

```python
# Two operations need the same machine
op1_end = Interval(10, 15)
op2_duration = Interval(5, 8)

# Op2 can't start until op1 finishes
op2_start = op1_end  # Earliest start
op2_end = op2_start + op2_duration

print(f"Op2 completes in {op2_end}")
# Output: Op2 completes in [15.0, 23.0]
```

### Example 3: Lower Bound Calculation

```python
# Calculate lower bound on makespan
# Based on critical path (longest job)

job_durations = [
    [Interval(5, 7), Interval(3, 5), Interval(8, 10)],
    [Interval(4, 6), Interval(7, 9), Interval(2, 4)],
]

job_lengths = [
    sum(ops, Interval(0, 0)) for ops in job_durations
]

lower_bound = max(job_lengths)  # Lexicographic max
print(f"Makespan lower bound: {lower_bound}")
```

## Integration with Existing Code

### Gradual Migration

```python
# Old code (scalars)
def old_calculate_makespan(durations):
    return sum(durations)

# New code (intervals or scalars)
from jobshop_rl.models import ensure_interval

def new_calculate_makespan(durations):
    intervals = [ensure_interval(d) for d in durations]
    return sum(intervals, Interval(0, 0))

# Works with both!
print(new_calculate_makespan([5, 7, 3]))  # Interval(15, 15)
print(new_calculate_makespan([Interval(5, 7), Interval(3, 5)]))  # Interval(8, 12)
```

---

## Next Steps

- Read `INTERVAL_IMPLEMENTATION_STATUS.md` for project progress
- Check `tests/test_interval.py` for more examples
- See Phase 2 documentation for data loading with intervals

---

*Quick Start Guide - v1.0*
*Part of the Interval-Based Scheduling Refactoring*
