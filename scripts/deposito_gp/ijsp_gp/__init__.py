"""
ijsp_gp: genetic-programming dispatching rules for the interval job shop.

Self-contained companion package of the paper's data deposit: interval
arithmetic, the semi-active decoder, hand-crafted baselines, evolved-rule
evaluation, the GP evolution itself, the Monte Carlo robustness measure,
and, since version 2.0, a fast simulator shared by all methods of the
budget comparison, the genetic algorithm of that comparison and the
generator of the asymmetric instances.
"""

__version__ = "2.0"

from .env import JobShopEnv, make_env
from .evaluate import evaluate_rule, rollout
from .instances import lb_for_instance_name, load_dir, load_instance
from .interval import Interval, final_makespan
from .robustness import eps_bar_of_rule
from .rules import GPRuleHeuristic, TERMINALS, load_rule

__all__ = [
    "Interval", "final_makespan", "JobShopEnv", "make_env",
    "load_instance", "load_dir", "lb_for_instance_name",
    "GPRuleHeuristic", "TERMINALS", "load_rule",
    "evaluate_rule", "rollout", "eps_bar_of_rule",
]
