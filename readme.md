# JobShopRL: Sistema Modular de RL para Job Shop Scheduling

JobShopRL es un sistema modular de aprendizaje por refuerzo diseñado para resolver problemas de Job Shop Scheduling. La arquitectura modular del sistema facilita la extensibilidad, mantenibilidad y reutilización de componentes.

## Características

- 🧩 **Arquitectura Modular**: Componentes desacoplados con interfaces bien definidas
- 🔀 **Múltiples Estrategias de Recompensa**: Configuración flexible de funciones de recompensa
- 📊 **Visualización Avanzada**: Gráficos detallados de makespan, programaciones y métricas de entrenamiento
- 📈 **Logging Completo**: Registro de métricas de entrenamiento en CSV para análisis posterior
- 🧠 **Algoritmo PPO**: Implementación eficiente del algoritmo Proximal Policy Optimization
- ⚙️ **Experimentación por Lotes**: Entrenamiento y evaluación con múltiples problemas
- 🔄 **Transferencia de Conocimiento**: Reutilización de modelos entre problemas similares

## Estructura del Proyecto

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

## Requisitos

- Python 3.8+
- PyTorch 1.9+
- NumPy
- Pandas
- Matplotlib
- OR-Tools (opcional, para comparación con solucionador de Google)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/username/jobshop_rl.git
cd jobshop_rl

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Experimento con un único problema (FT10)

```bash
python -m jobshop_rl.main --mode single --episodes 300 --reward advanced --visualize --save-plots  
```

### Experimentación por lotes con múltiples problemas

```bash
python -m jobshop_rl.main --mode batch \
    --training-dir data/training_problems \
    --test-dir data/test_problems \
    --output-dir results \
    --episodes-per-problem 100
```

### Generación de problemas aleatorios

```bash
python -m jobshop_rl.main --mode generate \
    --num-problems 5 \
    --num-jobs 10 \
    --num-machines 10 \
    --output-format json
```

## Uso en Google Colab

JobShopRL se puede ejecutar fácilmente en Google Colab. Para ello:

1. Crea un nuevo notebook en Colab
2. Clona el repositorio o copia los archivos manualmente
3. Instala las dependencias necesarias
4. Importa los módulos y ejecuta los experimentos

Consulta el notebook de ejemplo `jobshop_rl_colab.ipynb` para más detalles.

## Personalización

### Estrategias de Recompensa

JobShopRL incluye varias estrategias de recompensa predefinidas:

- `BasicRewardStrategy`: Recompensa simple basada en el makespan final
- `AdvancedRewardStrategy`: Recompensa con señales intermedias (tiempos de inactividad, operaciones críticas, etc.)
- `CombinedRewardStrategy`: Combinación ponderada de múltiples estrategias

Puedes crear tus propias estrategias implementando la clase base `RewardStrategy`:

```python
from jobshop_rl.rewards.strategies import RewardStrategy

class MyCustomRewardStrategy(RewardStrategy):
    def calculate_reward(self, env, state, next_state, action, done, info):
        # Implementa tu lógica de recompensa aquí
        return reward
```

### Heurísticas

El sistema incluye implementaciones de las heurísticas clásicas para Job Shop:

- SPT (Shortest Processing Time)
- LPT (Longest Processing Time)
- MOR (Most Operations Remaining)
- MWKR (Most Work Remaining)
- EST (Earliest Start Time)
- CR (Critical Ratio)
- OR-Tools (Solucionador de programación de restricciones de Google)

Estas heurísticas se utilizan como baseline para comparar el rendimiento del agente de RL. La heurística de OR-Tools proporciona soluciones de alta calidad utilizando técnicas avanzadas de programación con restricciones y puede servir como referencia para evaluar la calidad de las soluciones obtenidas por el agente de RL.

## Extensión a Múltiples Problemas

El sistema está diseñado para trabajar con múltiples problemas organizados en carpetas:

1. Coloca tus problemas de entrenamiento en `data/training_problems/`
2. Coloca tus problemas de prueba en `data/test_problems/`
3. Ejecuta el modo batch como se muestra arriba

El sistema cargará automáticamente los problemas, entrenará un modelo en los problemas de entrenamiento y lo evaluará en los problemas de prueba.

## Ejemplos

### Entrenamiento con recompensa avanzada

```python
from jobshop_rl.experiments.factory import ExperimentFactory

agent, results = ExperimentFactory.run_full_experiment(
    episodes=300,
    reward_strategy="advanced",
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

### Experimentación por lotes

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

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add amazing feature'`)
4. Haz push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la licencia MIT - ver el archivo LICENSE para más detalles.

## Cita

Si utilizas este código en tu investigación, por favor cítalo:

```
@software{jobshop_rl,
  author = {Your Name},
  title = {JobShopRL: A Modular Reinforcement Learning System for Job Shop Scheduling},
  year = {2023},
  url = {https://github.com/username/jobshop_rl}
}
```
## Evaluación con ABZ10

JobShopRL incluye la capacidad de evaluar modelos entrenados en el problema ABZ10 (10 trabajos × 10 máquinas). Puedes utilizar esta funcionalidad de dos formas:

1. **Durante el entrenamiento**:
   ```bash
   python -m jobshop_rl.main --mode single --episodes 300 --reward advanced --evaluate-abz10 --visualize --save-plots
   ```

2. **Evaluación independiente de un modelo ya entrenado**:
   ```bash
   python -m jobshop_rl.evaluate_abz10 --visualize --save-plot
   ```
   
   También puedes usar los scripts proporcionados:
   - En Windows: `evaluate_abz10.bat`
   - En Linux/Mac: `./evaluate_abz10.sh` (asegúrate de darle permisos de ejecución con `chmod +x evaluate_abz10.sh`)

La evaluación generará:
- Un diagrama de Gantt de la programación obtenida para ABZ10
- El makespan resultante
- El registro detallado del orden de tareas en el archivo de log

## Comparación con Google OR-Tools

El sistema incluye la capacidad de comparar los resultados del agente de RL con los obtenidos por Google OR-Tools, un solucionador de programación de restricciones avanzado.

### Instalación de OR-Tools

Para utilizar esta funcionalidad, primero debes instalar OR-Tools:

```bash
pip install ortools
```

También puedes instalar todas las dependencias, incluida OR-Tools, ejecutando:

```bash
pip install -r requirements.txt
```

### Uso de OR-Tools

La comparación con OR-Tools se realiza automáticamente durante la evaluación de heurísticas. Al ejecutar un experimento, verás una comparación con los resultados de OR-Tools junto con las otras heurísticas:

```bash
python -m jobshop_rl.main --mode single --episodes 300 --reward advanced --visualize
```

### Configuración de OR-Tools

Puedes modificar la configuración de OR-Tools editando el archivo `jobshop_rl/heuristics/ortools_solver.py`. Las principales opciones incluyen:

- **Tiempo límite**: por defecto, OR-Tools busca una solución durante 60 segundos. Puedes ajustar este valor según tus necesidades.
- **Estrategia de búsqueda**: puedes experimentar con diferentes estrategias de búsqueda proporcionadas por OR-Tools.

### Ventajas de la comparación con OR-Tools

- OR-Tools proporciona soluciones de alta calidad (a menudo óptimas) para problemas de Job Shop Scheduling.
- Sirve como una referencia robusta para evaluar el rendimiento del agente de RL.
- Permite entender el gap entre las soluciones del agente y las mejores soluciones conocidas.

## TODO
- reescribir archivo readme
- refactorizar el codigo
- La dimensión de entrada de la red neuronal de valor (ValueNetwork) cambia según el número de trabajos y máquinas.
- Comprobar cómo funciona el entrenamiento por lotes
- Comprobar que se cargan los ejemplos en el formato correcto

Enlaces https://www.youtube.com/watch?v=lbCrQ7iqRuo
https://spinningup.openai.com/en/latest/algorithms/ppo.html#references[readme.md](readme.md)