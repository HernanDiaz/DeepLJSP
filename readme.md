# JobShopRL: Modular RL System for Job Shop Scheduling

JobShopRL is a modular reinforcement learning system designed to solve Job Shop Scheduling problems. The system’s modular architecture facilitates extensibility, maintainability, and component reuse.

## 🚀 Key Features

- 🧩 **Modular Architecture**: Decoupled components with well-defined interfaces  
- 🔀 **Multiple Reward Strategies**: Flexible configuration of reward functions  
- 📊 **Advanced Visualization**: Detailed plots of makespan, schedules, and training metrics  
- 📈 **Comprehensive Logging**: Training metrics recorded in CSV for further analysis  
- 🧠 **PPO Algorithm**: Efficient implementation of Proximal Policy Optimization  
- ⚙️ **Batch Experimentation**: Training and evaluation with multiple problems  
- 🔄 **Knowledge Transfer**: Reuse of models across similar problems  
- 📋 **Comparison with Heuristics**: Evaluation against classical methods and OR-Tools  

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/username/jobshop_rl.git
cd jobshop_rl

# Install dependencies
pip install -r requirements.txt
```

## 📋 Requirements

- Python 3.8+  
- PyTorch 1.9+  
- NumPy  
- Pandas  
- Matplotlib  
- OR-Tools (optional, for comparison with Google solver)  

## 🖥️ Usage Examples

### 1. Training with a Single Problem (FT10)

To train an agent on the FT10 problem with visualization:

```bash
python -m jobshop_rl.main --mode single --episodes 300 --reward adaptive --visualize --save-plots
```

### 2. Training on One Problem and Evaluating on Another (must have the same size)

Train on FT10 and evaluate on ABZ10:

```bash
python -m jobshop_rl.main --mode single --episodes 300 --reward adaptive --visualize --save-plots --train-problem ft10 --eval-problem abz10
```

You can also use the provided scripts:  
- On Windows: `train_ft10_eval_abz10.bat`  
- On Linux/Mac: `./train_ft10_eval_abz10.sh`  

### 3. Evaluating a Trained Model on ABZ10

To evaluate a previously trained model on the ABZ10 problem:

```bash
python -m jobshop_rl.evaluate_abz10 --visualize --save-plot
```

Or use the provided scripts:  
- On Windows: `evaluate_abz10.bat`  
- On Linux/Mac: `./evaluate_abz10.sh`  

### 4. Batch Experimentation with Multiple Problems

To train and evaluate on sets of problems:

```bash
python -m jobshop_rl.main --mode batch     --training-dir data/training_problems     --test-dir data/test_problems     --output-dir results     --episodes-per-problem 100
```

### 5. Generating Random Problems

To generate a set of random problems:

```bash
python -m jobshop_rl.main --mode generate     --num-problems 5     --num-jobs 10     --num-machines 10     --output-format json
```

### 6. Comparison with Google OR-Tools

To compare the agent’s results with OR-Tools:

```bash
python -m jobshop_rl.main --mode single --episodes 300 --reward adaptive --visualize --use-ortools
```

On Windows, you can use: `run_with_ortools.bat`

## 🧰 Project Architecture

```
jobshop_rl/
├── __init__.py
├── models/             # Data models and neural networks
├── environment/        # Job Shop environments
├── agents/             # Reinforcement learning agents
├── rewards/            # Reward strategies
├── heuristics/         # Heuristic strategies
├── utils/              # Utilities (logging, visualization)
├── experiments/        # Experiment configuration and execution
├── data/               # Problem loaders and datasets
└── main.py             # Main entry point
```

## 🔧 Customization

### Reward Strategies

JobShopRL includes several predefined reward strategies that can be selected with the `--reward` parameter:

- `basic`: Simple reward based on the final makespan  
- `advanced`: Reward with intermediate signals (idle times, critical operations, etc.)  
- `adaptive`: Reward that adapts to problem characteristics (recommended)  
- `combined`: Weighted combination of multiple strategies  

Example of implementing a custom strategy:

```python
from jobshop_rl.rewards.base import RewardStrategy

class MyCustomRewardStrategy(RewardStrategy):
    def calculate_reward(self, env, state, next_state, action, done, info):
        # Implement your reward logic here
        return reward
```

### Implemented Heuristics

The system includes several classical heuristics used as baselines:

- SPT (Shortest Processing Time)  
- LPT (Longest Processing Time)  
- MOR (Most Operations Remaining)  
- MWKR (Most Work Remaining)  
- EST (Earliest Start Time)  
- CR (Critical Ratio)  
- OR-Tools (Google constraint programming solver)  

## 📊 Code Examples

### Programmatic Training

```python
from jobshop_rl.experiments.factory import ExperimentFactory

agent, results = ExperimentFactory.run_full_experiment(
    episodes=300,
    reward_strategy="adaptive",
    agent_params={
        "lr": 0.0003,
        "gamma": 0.99,
        "entropy_coef": 0.02,
        "K_epochs": 4,
    },
    reward_params={
        "makespan_weight": 1.0,
        "idle_weight": 0.2,
        "critical_weight": 0.1,
    },
    visualize=True
)
```

### Batch Experimentation

```python
from jobshop_rl.experiments.batch_experimenter import BatchExperimenter

experimenter = BatchExperimenter(
    training_dir="jobshop_rl/data/training_problems",
    test_dir="jobshop_rl/data/test_problems",
    output_dir="results"
)

# Train
best_agent = experimenter.train_agent(episodes_per_problem=100)

# Evaluate
results = experimenter.evaluate_on_test_set(best_agent)
```

## 📋 Command Line Options

### General Options

| Option | Description |
|--------|-------------|
| `--mode` | Execution mode: `single`, `batch`, or `generate` |
| `--episodes` | Number of episodes for training (single mode) |
| `--reward` | Reward strategy: `basic`, `advanced`, `adaptive`, `combined` |
| `--visualize` | Generate visualizations during training |
| `--save-plots` | Save visualizations to files |
| `--seed` | Seed for reproducibility |
| `--log-level` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

### Single Experiment Options

| Option | Description |
|--------|-------------|
| `--train-problem` | Problem ID for training (default: ft10) |
| `--eval-problem` | Problem ID for evaluation (if not specified, no evaluation is performed) |
| `--use-ortools` | Compare with Google OR-Tools solver |
| `--ortools-time-limit` | Time limit for OR-Tools solver (seconds) |

### Batch Options

| Option | Description |
|--------|-------------|
| `--training-dir` | Directory with training problems |
| `--test-dir` | Directory with test problems |
| `--output-dir` | Directory to save results |
| `--episodes-per-problem` | Episodes to train on each problem |

## 🔍 Implementation Details

### Using Google OR-Tools

To enable comparison with OR-Tools:

1. Install OR-Tools: `pip install ortools`  
2. Run experiments with the `--use-ortools` flag  

The OR-Tools solver configuration can be modified in `jobshop_rl/heuristics/ortools_solver.py`.

### Problem Formats

Problems can be loaded in several formats:  
- JSON: System’s native format  
- CSV: Compatible with tabular formats  
- Taillard: Compatible with classical benchmark problems  

## 🧪 Experimentation Scripts

The project includes several scripts to simplify experimentation:

| Script | Description |
|--------|-------------|
| `evaluate_abz10.bat` / `.sh` | Evaluate a model on ABZ10 |
| `train_ft10_eval_abz10.bat` / `.sh` | Train on FT10 and evaluate on ABZ10 |
| `train_abz10_eval_ft10.bat` / `.sh` | Train on ABZ10 and evaluate on FT10 |
| `train_ft20_eval_ft10.bat` / `.sh` | Train on FT20 and evaluate on FT10 |
| `train_and_evaluate_abz10.bat` / `.sh` | Train and evaluate on ABZ10 |
| `run_with_ortools.bat` | Run training with OR-Tools comparison |

## 📚 References

- [PPO Tutorial](https://spinningup.openai.com/en/latest/algorithms/ppo.html)  

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📝 Citation

If you use this code in your research, please cite it:

```
@software{jobshop_rl,
  author = {Hernán Díaz Rodríguez},
  title = {DeepL JSP: A Modular Reinforcement Learning System for Job Shop Scheduling},
  year = {2025},
  url = {https://github.com/HernanDiaz/DeepLJSP}
}
```

python -m jobshop_rl.main --mode batch --train-problem "tai20_15_01, tai20_15_02, tai20_15_03,tai20_15_04" --eval-problem "tai20_15_05,tai20_15_06,tai20_15_07,tai20_15_08,tai20_15_09,tai20_15_10" --episodes 50 --reward adaptive --output-dir outputs/taillard_15x15_experiment --csv-logging --visualize --save-plots --use-ortools --seed 1