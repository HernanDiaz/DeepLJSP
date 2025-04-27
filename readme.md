# JobShopRL: Sistema Modular de RL para Job Shop Scheduling

JobShopRL es un sistema modular de aprendizaje por refuerzo diseñado para resolver problemas de Job Shop Scheduling. La arquitectura modular del sistema facilita la extensibilidad, mantenibilidad y reutilización de componentes.

## 🚀 Características Principales

- 🧩 **Arquitectura Modular**: Componentes desacoplados con interfaces bien definidas
- 🔀 **Múltiples Estrategias de Recompensa**: Configuración flexible de funciones de recompensa
- 📊 **Visualización Avanzada**: Gráficos detallados de makespan, programaciones y métricas de entrenamiento
- 📈 **Logging Completo**: Registro de métricas de entrenamiento en CSV para análisis posterior
- 🧠 **Algoritmo PPO**: Implementación eficiente del algoritmo Proximal Policy Optimization
- ⚙️ **Experimentación por Lotes**: Entrenamiento y evaluación con múltiples problemas
- 🔄 **Transferencia de Conocimiento**: Reutilización de modelos entre problemas similares
- 📋 **Comparación con Heurísticas**: Evaluación contra métodos clásicos y OR-Tools

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/username/jobshop_rl.git
cd jobshop_rl

# Instalar dependencias
pip install -r requirements.txt
```

## 📋 Requisitos

- Python 3.8+
- PyTorch 1.9+
- NumPy
- Pandas
- Matplotlib
- OR-Tools (opcional, para comparación con solucionador de Google)

## 🖥️ Ejemplos de Uso

### 1. Entrenamiento con un Único Problema (FT10)

Para entrenar un agente en el problema FT10 con visualización:

```bash
python -m jobshop_rl.main --mode single --episodes 300 --reward adaptive --visualize --save-plots
```

### 2. Entrenamiento en un Problema y Evaluación en Otro (deben tener el mismo tamaño)

Entrenar en FT10 y evaluar en ABZ10:

```bash
python -m jobshop_rl.main --mode single --episodes 300 --reward adaptive --visualize --save-plots --train-problem ft10 --eval-problem abz10
```

También puede usar los scripts proporcionados:
- En Windows: `train_ft10_eval_abz10.bat`
- En Linux/Mac: `./train_ft10_eval_abz10.sh`

### 3. Evaluación de un Modelo Entrenado en ABZ10

Para evaluar un modelo previamente entrenado en el problema ABZ10:

```bash
python -m jobshop_rl.evaluate_abz10 --visualize --save-plot
```

O use los scripts proporcionados:
- En Windows: `evaluate_abz10.bat`
- En Linux/Mac: `./evaluate_abz10.sh`

### 4. Experimentación por Lotes con Múltiples Problemas

Para entrenar y evaluar con conjuntos de problemas:

```bash
python -m jobshop_rl.main --mode batch \
    --training-dir data/training_problems \
    --test-dir data/test_problems \
    --output-dir results \
    --episodes-per-problem 100
```

### 5. Generación de Problemas Aleatorios

Para generar un conjunto de problemas aleatorios:

```bash
python -m jobshop_rl.main --mode generate \
    --num-problems 5 \
    --num-jobs 10 \
    --num-machines 10 \
    --output-format json
```

### 6. Comparación con Google OR-Tools

Para comparar los resultados del agente con OR-Tools:

```bash
python -m jobshop_rl.main --mode single --episodes 300 --reward adaptive --visualize --use-ortools
```

En Windows, puede usar: `run_with_ortools.bat`

## 🧰 Arquitectura del Proyecto

```
jobshop_rl/
├── __init__.py
├── models/             # Modelos de datos y redes neuronales
├── environment/        # Entornos de Job Shop
├── agents/             # Agentes de aprendizaje por refuerzo
├── rewards/            # Estrategias de recompensa
├── heuristics/         # Estrategias heurísticas
├── utils/              # Utilidades (logging, visualización)
├── experiments/        # Configuración y ejecución de experimentos
├── data/               # Cargadores de problemas y conjuntos de datos
└── main.py             # Punto de entrada principal
```

## 🔧 Personalización

### Estrategias de Recompensa

JobShopRL incluye varias estrategias de recompensa predefinidas que pueden seleccionarse con el parámetro `--reward`:

- `basic`: Recompensa simple basada en el makespan final
- `advanced`: Recompensa con señales intermedias (tiempos de inactividad, operaciones críticas, etc.)
- `adaptive`: Recompensa que se adapta a las características del problema (recomendada)
- `combined`: Combinación ponderada de múltiples estrategias

Ejemplo de implementación de una estrategia personalizada:

```python
from jobshop_rl.rewards.base import RewardStrategy

class MyCustomRewardStrategy(RewardStrategy):
    def calculate_reward(self, env, state, next_state, action, done, info):
        # Implementa tu lógica de recompensa aquí
        return reward
```

### Heurísticas Implementadas

El sistema incluye varias heurísticas clásicas que se utilizan como baseline:

- SPT (Shortest Processing Time)
- LPT (Longest Processing Time)
- MOR (Most Operations Remaining)
- MWKR (Most Work Remaining)
- EST (Earliest Start Time)
- CR (Critical Ratio)
- OR-Tools (Solucionador de programación de restricciones de Google)

## 📊 Ejemplos de Código

### Entrenamiento Programático

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

### Experimentación por Lotes

```python
from jobshop_rl.experiments.batch_experimenter import BatchExperimenter

experimenter = BatchExperimenter(
    training_dir="jobshop_rl/data/training_problems",
    test_dir="jobshop_rl/data/test_problems",
    output_dir="results"
)

# Entrenar
best_agent = experimenter.train_agent(episodes_per_problem=100)

# Evaluar
results = experimenter.evaluate_on_test_set(best_agent)
```

## 📋 Opciones de Línea de Comandos

### Opciones Generales

| Opción | Descripción |
|--------|-------------|
| `--mode` | Modo de ejecución: `single`, `batch` o `generate` |
| `--episodes` | Número de episodios para entrenar (modo single) |
| `--reward` | Estrategia de recompensa: `basic`, `advanced`, `adaptive`, `combined` |
| `--visualize` | Generar visualizaciones durante el entrenamiento |
| `--save-plots` | Guardar visualizaciones en archivos |
| `--seed` | Semilla para reproducibilidad |
| `--log-level` | Nivel de logging: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

### Opciones de Experimento Individual

| Opción | Descripción |
|--------|-------------|
| `--train-problem` | ID del problema para entrenamiento (default: ft10) |
| `--eval-problem` | ID del problema para evaluación (si no se especifica, no se realiza evaluación) |
| `--use-ortools` | Comparar con solucionador de Google OR-Tools |
| `--ortools-time-limit` | Límite de tiempo para el solucionador OR-Tools (segundos) |

### Opciones de Lotes

| Opción | Descripción |
|--------|-------------|
| `--training-dir` | Directorio con problemas de entrenamiento |
| `--test-dir` | Directorio con problemas de prueba |
| `--output-dir` | Directorio para guardar resultados |
| `--episodes-per-problem` | Episodios para entrenar en cada problema |

## 🔍 Detalles de Implementación

### Uso de Google OR-Tools

Para utilizar la comparación con OR-Tools:

1. Instale OR-Tools: `pip install ortools`
2. Ejecute experimentos con la bandera `--use-ortools`

La configuración del solucionador OR-Tools puede modificarse en `jobshop_rl/heuristics/ortools_solver.py`.

### Formato de los Problemas

Los problemas pueden cargarse en varios formatos:
- JSON: Formato nativo del sistema
- CSV: Compatible con formatos tabulares
- Taillard: Compatible con problemas clásicos de literatura

## 🧪 Scripts de Experimentación

El proyecto incluye varios scripts para facilitar la experimentación:

| Script | Descripción |
|--------|-------------|
| `evaluate_abz10.bat` / `.sh` | Evalúa un modelo en ABZ10 |
| `train_ft10_eval_abz10.bat` / `.sh` | Entrena con FT10 y evalúa con ABZ10 |
| `train_abz10_eval_ft10.bat` / `.sh` | Entrena con ABZ10 y evalúa con FT10 |
| `train_ft20_eval_ft10.bat` / `.sh` | Entrena con FT20 y evalúa con FT10 |
| `train_and_evaluate_abz10.bat` / `.sh` | Entrena y evalúa con ABZ10 |
| `run_with_ortools.bat` | Ejecuta entrenamiento con comparación OR-Tools |

## 📚 Referencias

- [Tutorial sobre PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html)
- [Visualización de Job Shop Scheduling](https://www.youtube.com/watch?v=lbCrQ7iqRuo)

## 📄 Licencia

Este proyecto está licenciado bajo la licencia MIT - ver el archivo LICENSE para más detalles.

## 📝 Cita

Si utilizas este código en tu investigación, por favor cítalo:

```
@software{jobshop_rl,
  author = {Your Name},
  title = {JobShopRL: A Modular Reinforcement Learning System for Job Shop Scheduling},
  year = {2023},
  url = {https://github.com/username/jobshop_rl}
}
```