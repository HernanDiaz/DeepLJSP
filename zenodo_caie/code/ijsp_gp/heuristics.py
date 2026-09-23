"""
Hand-crafted dispatching heuristics for the interval job shop.

Every heuristic reads the per-operation feature matrix produced by the
environment (see env.py for the column layout). Interval-valued attributes
are compared lexicographically, upper bound first.
"""

import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Union

import numpy as np


class HeuristicStrategy(ABC):
    """Base class for dispatching strategies."""

    @abstractmethod
    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        pass

    @staticmethod
    def _is_interval_features(features: np.ndarray) -> bool:
        if len(features) == 0:
            return False
        return features.shape[1] == 10

    @staticmethod
    def _extract_duration(features: np.ndarray, idx: int) -> Union[float, Tuple[float, float]]:
        if HeuristicStrategy._is_interval_features(features):
            return (features[idx][3], features[idx][4])
        return features[idx][3]

    @staticmethod
    def _extract_earliest_start(features: np.ndarray, idx: int) -> Union[float, Tuple[float, float]]:
        if HeuristicStrategy._is_interval_features(features):
            return (features[idx][5], features[idx][6])
        return features[idx][4]

    @staticmethod
    def _extract_remaining_time(features: np.ndarray, idx: int) -> Union[float, Tuple[float, float]]:
        if HeuristicStrategy._is_interval_features(features):
            return (features[idx][7], features[idx][8])
        return features[idx][5]

    @staticmethod
    def _extract_remaining_ops(features: np.ndarray, idx: int) -> int:
        if HeuristicStrategy._is_interval_features(features):
            return int(features[idx][9])
        return int(features[idx][6])

    @staticmethod
    def _lexicographic_compare(val1: Union[float, Tuple[float, float]],
                               val2: Union[float, Tuple[float, float]],
                               minimize: bool = True) -> int:
        """0 if val1 is preferred, 1 if val2 is preferred."""
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if minimize:
                return 0 if val1 < val2 else 1
            return 0 if val1 > val2 else 1
        if isinstance(val1, tuple) and isinstance(val2, tuple):
            lower1, upper1 = val1
            lower2, upper2 = val2
            if minimize:
                if upper1 < upper2:
                    return 0
                elif upper1 > upper2:
                    return 1
                else:
                    return 0 if lower1 < lower2 else 1
            else:
                if upper1 > upper2:
                    return 0
                elif upper1 < upper2:
                    return 1
                else:
                    return 0 if lower1 > lower2 else 1
        return 0


class SPTHeuristic(HeuristicStrategy):
    """Shortest processing time."""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(features) == 0:
            return 0
        durations = [self._extract_duration(features, i) for i in range(len(features))]
        min_idx = 0
        min_duration = durations[0]
        for i in range(1, len(durations)):
            if self._lexicographic_compare(durations[i], min_duration, minimize=True) == 0:
                min_idx = i
                min_duration = durations[i]
        return min_idx


class LPTHeuristic(HeuristicStrategy):
    """Longest processing time."""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(features) == 0:
            return 0
        durations = [self._extract_duration(features, i) for i in range(len(features))]
        max_idx = 0
        max_duration = durations[0]
        for i in range(1, len(durations)):
            if self._lexicographic_compare(durations[i], max_duration, minimize=False) == 0:
                max_idx = i
                max_duration = durations[i]
        return max_idx


class MORHeuristic(HeuristicStrategy):
    """Most operations remaining."""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(features) == 0:
            return 0
        remaining_ops = [self._extract_remaining_ops(features, i) for i in range(len(features))]
        return np.argmax(remaining_ops)


class MWKRHeuristic(HeuristicStrategy):
    """Most work remaining."""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(features) == 0:
            return 0
        remaining_times = [self._extract_remaining_time(features, i) for i in range(len(features))]
        max_idx = 0
        max_time = remaining_times[0]
        for i in range(1, len(remaining_times)):
            if self._lexicographic_compare(remaining_times[i], max_time, minimize=False) == 0:
                max_idx = i
                max_time = remaining_times[i]
        return max_idx


class ESTHeuristic(HeuristicStrategy):
    """Earliest starting time."""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(features) == 0:
            return 0
        start_times = [self._extract_earliest_start(features, i) for i in range(len(features))]
        min_idx = 0
        min_start = start_times[0]
        for i in range(1, len(start_times)):
            if self._lexicographic_compare(start_times[i], min_start, minimize=True) == 0:
                min_idx = i
                min_start = start_times[i]
        return min_idx


class CRHeuristic(HeuristicStrategy):
    """Critical ratio (worst-case remaining time over remaining operations)."""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(features) == 0:
            return 0
        epsilon = 1e-10
        critical_ratios = []
        for i in range(len(features)):
            remaining_time = self._extract_remaining_time(features, i)
            remaining_ops = self._extract_remaining_ops(features, i)
            if isinstance(remaining_time, tuple):
                time_value = remaining_time[1]
            else:
                time_value = remaining_time
            ratio = time_value / (remaining_ops + epsilon)
            critical_ratios.append(ratio)
        return np.argmin(critical_ratios)


class GTHeuristic(HeuristicStrategy):
    """
    Giffler and Thompson (1960): active schedule generation.

    At each step: (1) find the eligible operation c with the smallest
    completion time (earliest start + duration, interval-aware lexicographic
    comparison); (2) restrict candidates to the conflict set, the eligible
    operations on the SAME machine as c whose start precedes c's completion;
    (3) break ties inside the conflict set with a priority rule (spt or mwkr).
    """

    def __init__(self, tiebreak: str = "spt", epsilon: float = 0.0, rng=None):
        assert tiebreak in ("spt", "mwkr")
        self.tiebreak = tiebreak
        self.epsilon = epsilon
        self.rng = rng if rng is not None else random.Random()

    @staticmethod
    def _add(a, b):
        a = a if isinstance(a, tuple) else (a, a)
        b = b if isinstance(b, tuple) else (b, b)
        return (a[0] + b[0], a[1] + b[1])

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(features) == 0:
            return 0
        n = len(features)
        starts = [self._extract_earliest_start(features, i) for i in range(n)]
        durations = [self._extract_duration(features, i) for i in range(n)]
        completions = [self._add(starts[i], durations[i]) for i in range(n)]
        machines = [int(features[i][2]) for i in range(n)]

        # (1) operation with minimum completion (lexicographic by upper)
        c = 0
        for i in range(1, n):
            if self._lexicographic_compare(completions[i], completions[c], minimize=True) == 0:
                c = i

        # (2) conflict set: same machine as c, start before c's completion
        conflict = [i for i in range(n)
                    if machines[i] == machines[c]
                    and self._lexicographic_compare(starts[i], completions[c], minimize=True) == 0]
        if not conflict:
            conflict = [c]

        # (3) GRASP-style randomization inside the conflict set
        if self.epsilon > 0 and self.rng.random() < self.epsilon:
            return self.rng.choice(conflict)

        # (3b) deterministic tie-break inside the conflict set
        if self.tiebreak == "spt":
            best = conflict[0]
            for i in conflict[1:]:
                if self._lexicographic_compare(durations[i], durations[best], minimize=True) == 0:
                    best = i
        else:  # mwkr
            remaining = [self._extract_remaining_time(features, i) for i in range(n)]
            best = conflict[0]
            for i in conflict[1:]:
                if self._lexicographic_compare(remaining[i], remaining[best], minimize=False) == 0:
                    best = i
        return best


class RandomHeuristic(HeuristicStrategy):
    """Uniformly random dispatcher."""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(eligible_ops) == 0:
            return 0
        return random.randint(0, len(eligible_ops) - 1)
