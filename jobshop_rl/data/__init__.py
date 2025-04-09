"""
Paquete de datos para problemas de Job Shop Scheduling.
"""

from jobshop_rl.data.ft10 import get_ft10_problem
from jobshop_rl.data.ft20 import get_ft20_problem
from jobshop_rl.data.abz10 import get_abz10_problem
from jobshop_rl.data.tai20_20_01 import get_tai20_20_01_problem
from jobshop_rl.data.tai20_20_02 import get_tai20_20_02_problem
from jobshop_rl.data.tai50_15_01 import get_tai50_15_01_problem
from jobshop_rl.data.tai50_15_02 import get_tai50_15_02_problem
from jobshop_rl.data.tai100_20_01 import get_tai100_20_01_problem
from jobshop_rl.data.tai100_20_02 import get_tai100_20_02_problem
from jobshop_rl.data.problem_loader import ProblemLoader

__all__ = [
    'get_ft10_problem', 
    'get_ft20_problem', 
    'get_abz10_problem',
    'get_tai20_20_01_problem',
    'get_tai20_20_02_problem',
    'get_tai50_15_01_problem',
    'get_tai50_15_02_problem',
    'get_tai100_20_01_problem',
    'get_tai100_20_02_problem',
    'ProblemLoader'
]
