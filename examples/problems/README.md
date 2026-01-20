# Example Problem Files

This directory contains example problem files demonstrating the interval format support.

## File Formats

### Taillard Format (`.txt`)

The Taillard format is extended to support intervals using `(min,max)` notation:

```
# num_jobs num_machines [optimal]
machine1 duration1 machine2 duration2 ...
...
```

**Scalar durations**:
```
3 3
0 5 1 7 2 9
1 6 0 4 2 8
2 3 1 5 0 10
```

**Interval durations**:
```
3 3
0 (5,7) 1 (3,5) 2 (8,10)
1 (4,5) 0 (7,8) 2 (2,3)
2 (3,9) 1 (5,7) 0 (6,10)
```

**Mixed** (scalars and intervals):
```
3 3
0 (5,7) 1 4 2 (8,10)
1 6 0 (7,8) 2 3
2 (3,9) 1 5 0 10
```

### JSON Format (`.json`)

**Interval format** (array notation):
```json
{
  "num_jobs": 3,
  "num_machines": 3,
  "sequences": [[0, 1, 2], [1, 0, 2], [2, 1, 0]],
  "durations": [
    [[5, 7], [3, 5], [8, 10]],
    [[4, 5], [7, 8], [2, 3]],
    [[3, 9], [5, 7], [6, 10]]
  ]
}
```

**Interval format** (dict notation):
```json
{
  "durations": [
    [
      {"lower": 5, "upper": 7},
      {"lower": 3, "upper": 5}
    ]
  ]
}
```

**Scalar format** (backward compatible):
```json
{
  "durations": [[5, 7, 9], [6, 4, 8], [3, 5, 10]]
}
```

### CSV Format (`.csv`)

**Min/Max column format** (for intervals):
```csv
machine_0,duration_0_min,duration_0_max,machine_1,duration_1_min,duration_1_max
0,5,7,1,3,5
1,4,5,0,7,8
```

**Standard format** (for scalars):
```csv
machine_0,duration_0,machine_1,duration_1
0,5,1,7
1,6,0,4
```

## Loading Examples

### Python Code

```python
from jobshop_rl.data.problem_loader import ProblemLoader

# Load from any format
problem = ProblemLoader.load_json('test_3x3_interval.json')
# or
problem = ProblemLoader.load_taillard('test_3x3_interval.txt')
# or
problem = ProblemLoader.load_csv('test_3x3_interval.csv')

# Check if problem has intervals
if problem['has_intervals']:
    print("Problem contains interval processing times")
    print(f"First duration: {problem['durations'][0][0]}")
else:
    print("Problem has deterministic processing times")
```

### Generating Random Problems

```python
# Deterministic problem
det_problem = ProblemLoader.generate_random_problem(
    num_jobs=5,
    num_machines=5,
    uncertainty_ratio=0.0,  # No uncertainty
    seed=42
)

# Problem with ±10% uncertainty
interval_problem = ProblemLoader.generate_random_problem(
    num_jobs=5,
    num_machines=5,
    uncertainty_ratio=0.1,  # ±10%
    seed=42
)

# Save to file
ProblemLoader.save_problem(interval_problem, 'my_problem.json', format='json')
```

## Test Problems

### Small Test Problems (3x3)
- `test_3x3_interval.json` - Full interval problem
- `test_3x3_interval.txt` - Taillard format
- `test_3x3_interval.csv` - CSV format

### Benchmark Problems (10x10)
Available in Python modules:
- `jobshop_rl.data.ft10_interval.get_ft10_interval_problem()` - FT10 with ±10% uncertainty
- `jobshop_rl.data.ft10_interval.get_ft10_deterministic_as_intervals()` - FT10 as degenerate intervals

## File Format Specification

### Interval Notation

Intervals can be specified using:
- Parentheses: `(5,10)` or `(5, 10)`
- Brackets: `[5,10]` or `[5, 10]`

Both formats are equivalent. Whitespace around commas is optional.

### Validation Rules

All loaded intervals are validated to ensure:
1. Lower bound ≤ Upper bound
2. No negative durations (unless explicitly allowed)
3. Consistent structure across all jobs

### Backward Compatibility

Scalar (deterministic) problems are fully supported:
- No code changes needed for existing problem files
- Scalars are automatically converted when needed
- Degenerate intervals `[x,x]` are treated as scalars

## Usage Tips

1. **Start small**: Test with 3x3 problems before scaling up
2. **Validate**: Always check `has_intervals` flag after loading
3. **Roundtrip testing**: Save and reload to verify format preservation
4. **Mixed problems**: You can mix scalars and intervals in the same problem

## See Also

- `docs/INTERVAL_QUICK_START.md` - Interval class usage guide
- `INTERVAL_IMPLEMENTATION_STATUS.md` - Implementation progress
- `tests/test_data_loading.py` - Comprehensive test suite
