"""
Semi-active schedule generation for the interval job shop.

The environment dispatches one eligible operation per step, propagating
starting and completion times with component-wise interval arithmetic
(scalar arithmetic for crisp instances). The per-operation feature layout
consumed by dispatching rules is:

  interval instances (10 columns):
    [job_id, op_idx, machine, dur_lo, dur_up, est_lo, est_up,
     rem_lo, rem_up, remaining_ops]
  crisp instances (7 columns):
    [job_id, op_idx, machine, duration, earliest_start,
     remaining_time, remaining_ops]
"""

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from .interval import Interval


@dataclass
class SchedulingStep:
    job: int
    operation: int
    machine: int
    start: Union[int, Interval]
    end: Union[int, Interval]


@dataclass
class OperationFeatures:
    job_id: int
    op_idx: int
    machine: int
    duration: Union[int, Interval]
    earliest_start: Union[int, Interval]
    remaining_time: Union[int, Interval]
    remaining_ops: int

    def to_array(self) -> List[float]:
        has_intervals = (isinstance(self.duration, Interval) or
                         isinstance(self.earliest_start, Interval) or
                         isinstance(self.remaining_time, Interval))
        if has_intervals:
            duration_lower = self.duration.lower if isinstance(self.duration, Interval) else float(self.duration)
            duration_upper = self.duration.upper if isinstance(self.duration, Interval) else float(self.duration)
            earliest_start_lower = (self.earliest_start.lower if isinstance(self.earliest_start, Interval)
                                    else float(self.earliest_start))
            earliest_start_upper = (self.earliest_start.upper if isinstance(self.earliest_start, Interval)
                                    else float(self.earliest_start))
            remaining_time_lower = (self.remaining_time.lower if isinstance(self.remaining_time, Interval)
                                    else float(self.remaining_time))
            remaining_time_upper = (self.remaining_time.upper if isinstance(self.remaining_time, Interval)
                                    else float(self.remaining_time))
            return [
                float(self.job_id),
                float(self.op_idx),
                float(self.machine),
                duration_lower,
                duration_upper,
                earliest_start_lower,
                earliest_start_upper,
                remaining_time_lower,
                remaining_time_upper,
                float(self.remaining_ops),
            ]
        return [
            float(self.job_id),
            float(self.op_idx),
            float(self.machine),
            float(self.duration),
            float(self.earliest_start),
            float(self.remaining_time),
            float(self.remaining_ops),
        ]


class JobShopEnv:
    """Semi-active decoder for interval and crisp job shop instances."""

    def __init__(self, num_jobs: int, num_machines: int,
                 sequences: List[List[int]],
                 durations: List[List[Union[int, Interval]]],
                 problem_id: Optional[str] = None,
                 seed: Optional[int] = None):
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.sequences = sequences
        self.durations = durations
        self.problem_id = problem_id
        self.has_intervals = self._check_for_intervals()
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.reset()

    def _check_for_intervals(self) -> bool:
        for job_durations in self.durations:
            for duration in job_durations:
                if isinstance(duration, Interval) and not duration.is_degenerate:
                    return True
        return False

    def reset(self) -> Dict:
        self.job_status = [0] * self.num_jobs
        if self.has_intervals:
            self.job_completion_time = [Interval(0, 0) for _ in range(self.num_jobs)]
            self.machine_completion_time = [Interval(0, 0) for _ in range(self.num_machines)]
        else:
            self.job_completion_time = [0] * self.num_jobs
            self.machine_completion_time = [0] * self.num_machines
        self.scheduled_ops = []
        self.eligible_ops = self._get_eligible_ops()
        self.schedule_history = []
        self.makespan_history = []
        return self._get_state()

    def _get_eligible_ops(self) -> List[int]:
        eligible = []
        for job_id in range(self.num_jobs):
            if self.job_status[job_id] < self.num_machines:
                if self.job_status[job_id] == 0 or (job_id, self.job_status[job_id] - 1) in self.scheduled_ops:
                    eligible.append(job_id)
        return eligible

    def _get_state(self) -> Dict:
        return {
            'eligible_ops': self.eligible_ops,
            'job_status': self.job_status.copy(),
            'job_completion_time': self.job_completion_time.copy(),
            'machine_completion_time': self.machine_completion_time.copy(),
        }

    def get_features(self, state: Dict) -> np.ndarray:
        features = []
        for job_id in state['eligible_ops']:
            op_idx = state['job_status'][job_id]
            machine = self.sequences[job_id][op_idx]
            duration = self.durations[job_id][op_idx]
            job_completion = state['job_completion_time'][job_id]
            machine_completion = state['machine_completion_time'][machine]
            if self.has_intervals:
                earliest_start = Interval.max(job_completion, machine_completion)
            else:
                earliest_start = max(job_completion, machine_completion)
            remaining_ops = self.num_machines - op_idx - 1
            if remaining_ops > 0:
                remaining_durations = self.durations[job_id][op_idx + 1:]
                if self.has_intervals:
                    remaining_time = sum(remaining_durations, Interval(0, 0))
                else:
                    remaining_time = sum(remaining_durations)
            else:
                remaining_time = Interval(0, 0) if self.has_intervals else 0
            op_features = OperationFeatures(
                job_id=job_id,
                op_idx=op_idx,
                machine=machine,
                duration=duration,
                earliest_start=earliest_start,
                remaining_time=remaining_time,
                remaining_ops=remaining_ops,
            )
            features.append(op_features.to_array())
        if not features:
            feature_dim = 10 if self.has_intervals else 7
            return np.zeros((0, feature_dim))
        return np.array(features)

    def step(self, action_idx: int) -> Tuple[Dict, float, bool, Dict]:
        if len(self.eligible_ops) == 0:
            return self._get_state(), 0.0, True, {}
        job_id = self.eligible_ops[action_idx]
        op_idx = self.job_status[job_id]
        machine = self.sequences[job_id][op_idx]
        duration = self.durations[job_id][op_idx]
        if self.has_intervals:
            start_time = Interval.max(
                self.job_completion_time[job_id],
                self.machine_completion_time[machine],
            )
            end_time = start_time + duration
        else:
            start_time = max(
                self.job_completion_time[job_id],
                self.machine_completion_time[machine],
            )
            end_time = start_time + duration
        self.job_completion_time[job_id] = end_time
        self.machine_completion_time[machine] = end_time
        self.scheduled_ops.append((job_id, op_idx))
        self.job_status[job_id] += 1
        self.eligible_ops = self._get_eligible_ops()
        self.schedule_history.append(vars(SchedulingStep(
            job=job_id, operation=op_idx, machine=machine,
            start=start_time, end=end_time)))
        # component-wise interval makespan: [max lowers, max uppers]
        if self.has_intervals:
            current_makespan = Interval.max(*self.job_completion_time)
        else:
            current_makespan = max(self.job_completion_time)
        self.makespan_history.append(current_makespan)
        done = all(status == self.num_machines for status in self.job_status)
        next_state = self._get_state()
        if done:
            info = {'makespan': current_makespan}
        else:
            info = {'makespan': None}
        return next_state, 0.0, done, info


def make_env(problem: Dict, seed: Optional[int] = 0) -> JobShopEnv:
    """Build a decoder environment from an instance dictionary."""
    return JobShopEnv(
        num_jobs=problem['num_jobs'],
        num_machines=problem['num_machines'],
        sequences=problem['sequences'],
        durations=problem['durations'],
        problem_id=problem.get('problem_id'),
        seed=seed,
    )
