# Descripción del Proyecto DeepLJSP (JobShopRL)

## Información General
- **Nombre**: DeepLJSP (Deep Learning Job Shop Scheduling)
- **Tipo**: Sistema de aprendizaje por refuerzo para problemas de Job Shop Scheduling 
- **Lenguaje**: Python
- **Framework principal**: PyTorch
- **Algoritmo de RL**: PPO (Proximal Policy Optimization)

## Arquitectura del Proyecto

El proyecto sigue una arquitectura modular y está organizado de la siguiente manera:

```
DeepLJSP/
├── jobshop_rl/                    # Módulo principal
│   ├── agents/                    # Agentes de RL (PPO)
│   ├── data/                      # Datos de problemas de benchmark
│   ├── environment/               # Entorno de Job Shop Scheduling
│   ├── experiments/               # Configuración y ejecución de experimentos
│   ├── heuristics/                # Heurísticas clásicas (SPT, LPT, MOR, etc.)
│   ├── models/                    # Modelos de datos y redes neuronales
│   ├── rewards/                   # Estrategias de recompensa modulares
│   ├── utils/                     # Utilidades (logging, visualización, etc.)
│   └── main.py                    # Punto de entrada principal
├── outputs/                       # Resultados de experimentos
├── venv/                         # Entorno virtual de Python
├── requirements.txt              # Dependencias del proyecto
└── readme.md                     # Documentación principal
```

## Componentes Principales

### 1. Entorno (jobshop_rl/environment/)
- **job_shop_env.py**: Entorno principal que simula el problema de Job Shop Scheduling
- Implementa la interfaz estándar de RL (reset, step, render)
- Maneja estados, acciones y transiciones
- Integra análisis de problemas para límites inferiores

### 2. Agentes (jobshop_rl/agents/)
- **ppo_agent.py**: Implementación del algoritmo PPO
- **ppo_memory.py**: Buffer de experiencia para PPO
- **base_agent.py**: Clase base para agentes
- Características avanzadas: GAE, clipping de gradientes, decaimiento de LR

### 3. Modelos (jobshop_rl/models/)
- **neural_models.py**: Redes neuronales (PolicyNetwork, ValueNetwork, FeatureExtractor)
- **data_models.py**: Estructuras de datos (Operation, SchedulingStep, OperationFeatures)

### 4. Sistema de Recompensas (jobshop_rl/rewards/)
- **base.py**: Interfaz base para estrategias de recompensa
- **strategies.py**: Implementaciones de estrategias (Basic, Advanced, Adaptive, Combined)
- **factory.py**: Fábrica para crear estrategias de recompensa
- Patrón Strategy para flexibilidad en diseño de recompensas

### 5. Datos (jobshop_rl/data/)
- Problemas de benchmark: FT10, FT20, ABZ7-10, TAI (15x15, 20x20, 30x20, 50x20, 100x20)
- **problem_loader.py**: Cargador de problemas con soporte para múltiples formatos
- Registro centralizado de problemas (PROBLEM_REGISTRY)

### 6. Heurísticas (jobshop_rl/heuristics/)
- **strategies.py**: Heurísticas clásicas (SPT, LPT, MOR, MWKR, Random)
- **ortools_solver.py**: Integración con Google OR-Tools como baseline

### 7. Utilidades (jobshop_rl/utils/)
- **logging.py**: Sistema de logging para métricas de entrenamiento
- **visualization.py**: Funciones de visualización (Gantt charts, curvas de aprendizaje)
- **checkpoint_manager.py**: Gestión de checkpoints de modelos
- **problem_analyzer.py**: Análisis de problemas y cálculo de límites inferiores
- **experiment_config.py**: Configuraciones de experimentos
- **seed_utils.py**: Utilidades para reproducibilidad
- **path_utils.py**: Gestión de rutas y directorios

### 8. Experimentación (jobshop_rl/experiments/)
- **factory.py**: Fábrica para crear y ejecutar experimentos
- **batch_experimenter.py**: Experimentación por lotes con múltiples problemas
- **evaluator.py**: Evaluación de agentes entrenados

## Características Técnicas

### Algoritmo PPO
- **Parámetros configurables**: learning rate, gamma, epsilon clipping, epochs
- **Características avanzadas**: 
  - GAE (Generalized Advantage Estimation)
  - Clipping de gradientes
  - Normalización de ventajas
  - Decaimiento de learning rate
  - Early stopping

### Estrategias de Recompensa
1. **Basic**: Recompensa solo al final basada en makespan
2. **Advanced**: Recompensas intermedias (tiempo de inactividad, operaciones críticas, balance de carga)
3. **Adaptive**: Se adapta automáticamente a las características del problema
4. **Combined**: Combinación ponderada de múltiples estrategias

### Características del Entorno
- **Estado**: Operaciones elegibles, estado de trabajos, tiempos de completion
- **Acciones**: Selección de la siguiente operación a programar
- **Recompensas**: Configurables según estrategia elegida
- **Observaciones**: Características de operaciones (duración, máquina, tiempo restante, etc.)

## Datos y Problemas

### Problemas de Benchmark Incluidos
- **FT10**: 10 trabajos × 10 máquinas (óptimo conocido: 930)
- **FT20**: 20 trabajos × 5 máquinas
- **ABZ7-10**: Problemas de Adams, Balas y Zawack
- **TAI**: Problemas de Taillard en varias dimensiones

### Formato de Datos
Los problemas se definen con:
- `sequences`: Secuencia de máquinas para cada trabajo
- `durations`: Duración de cada operación
- `num_jobs`, `num_machines`: Dimensiones del problema

## Modos de Ejecución

### 1. Modo Single
Entrena/evalúa en un solo problema:
```bash
python -m jobshop_rl.main --mode single --episodes 300 --reward adaptive --visualize
```

### 2. Modo Batch
Entrena en múltiples problemas:
```bash
python -m jobshop_rl.main --mode batch --training-dir data/problems --episodes-per-problem 100
```

### 3. Modo Generate
Genera problemas aleatorios:
```bash
python -m jobshop_rl.main --mode generate --num-problems 5 --num-jobs 10 --num-machines 10
```

## Scripts Auxiliares

### Entrenamiento y Evaluación
- `train_and_evaluate_abz10.bat`: Entrena y evalúa en ABZ10
- `evaluate_abz10.bat/.sh`: Solo evaluación en ABZ10
- `train_ft10_eval_abz10.bat/.sh`: Entrena en FT10, evalúa en ABZ10

### Configuración
- `directory-structure.sh`: Script para mostrar estructura del proyecto

## Archivos de Configuración

### requirements.txt
Dependencias principales:
- torch>=2.0.0
- numpy>=1.22.0
- matplotlib>=3.5.0
- ortools>=9.4.0 (para comparación)
- pandas, tqdm, networkx, etc.

### Archivos de Estado Inicial
- `DeepLearningFt10Inicial.txt`: Implementación inicial completa en un solo archivo
- `DeepLearningFT10V2.txt`: Versión mejorada

## Outputs y Resultados

### Estructura de outputs/
- `checkpoints/`: Modelos guardados
- `logs/`: Logs de entrenamiento en CSV
- `taillard_30x20_experiment/`: Resultados de experimentos específicos
- `plots/`: Gráficos generados

### Tipos de Visualizaciones
1. **Gantt Charts**: Programación de trabajos en máquinas
2. **Curvas de Aprendizaje**: Evolución del makespan durante entrenamiento
3. **Métricas de Entrenamiento**: Pérdidas, recompensas, exploración
4. **Comparaciones**: RL vs heurísticas vs OR-Tools

## Características Avanzadas

### Análisis de Problemas
- Cálculo automático de límites inferiores
- Análisis de características del problema para adaptación automática
- Múltiples métodos de cálculo de bounds (máquina crítica, trabajo crítico, etc.)

### Reproducibilidad
- Sistema centralizado de semillas
- Logging completo de parámetros y resultados
- Checkpoints automáticos

### Flexibilidad
- Patrón Strategy para recompensas y heurísticas
- Factory pattern para experimentos
- Configuración modular de parámetros

## Ejemplos de Uso Programático

### Experimento Básico
```python
from jobshop_rl.experiments.factory import ExperimentFactory

agent, results = ExperimentFactory.run_full_experiment(
    episodes=300,
    reward_strategy="adaptive",
    visualize=True
)
```

### Experimento por Lotes
```python
from jobshop_rl.experiments.batch_experimenter import BatchExperimenter

experimenter = BatchExperimenter(output_dir="results")
best_agent = experimenter.train_agent(episodes_per_problem=100)
results = experimenter.evaluate_on_test_set(best_agent)
```

## Estado del Proyecto

### Implementado
- ✅ Algoritmo PPO completo con características avanzadas
- ✅ Sistema modular de recompensas
- ✅ Múltiples problemas de benchmark
- ✅ Visualizaciones y logging completos
- ✅ Comparación con heurísticas y OR-Tools
- ✅ Experimentación por lotes
- ✅ Sistema de checkpoints

### Posibles Mejoras Futuras
- Integración con más algoritmos de RL (SAC, A3C)
- Soporte para problemas con máquinas paralelas
- Interfaz web para visualización
- Optimización de hiperparámetros automática
- Paralelización de entrenamiento

## Archivos Importantes para Revisión

### Configuración Principal
- `jobshop_rl/main.py`: Punto de entrada
- `requirements.txt`: Dependencias
- `readme.md`: Documentación completa

### Implementación Core
- `jobshop_rl/environment/job_shop_env.py`: Entorno principal
- `jobshop_rl/agents/ppo_agent.py`: Agente PPO
- `jobshop_rl/rewards/strategies.py`: Estrategias de recompensa

### Datos y Experimentos
- `jobshop_rl/data/problem_loader.py`: Carga de problemas
- `jobshop_rl/experiments/factory.py`: Fábrica de experimentos
- `jobshop_rl/utils/`: Utilidades diversas

Este proyecto implementa un sistema completo y modular de aprendizaje por refuerzo para Job Shop Scheduling, con arquitectura profesional, documentación extensa y múltiples características avanzadas.

## Problema con BatchNorm en Instancias Grandes (50x20 y 100x20)

### Descripción del Problema
Al entrenar en problemas grandes (50x20 y 100x20), se observó alta variabilidad en los resultados:
- Con algunas semillas: Excelentes resultados tanto en entrenamiento como en test
- Con otras semillas: Resultados mucho peores en test que en entrenamiento
- La variabilidad era excesiva e impredecible

### Posible causa
Las capas BatchNorm (Batch Normalization) causaban inestabilidad debido a:
1. **Estadísticas de batch pequeño**: Durante el entrenamiento con PPO, a veces se procesan pocos ejemplos
2. **Cambio de distribución**: Las estadísticas aprendidas en un problema no se generalizan bien a otros
3. **Modo train vs eval**: Diferencias significativas entre las estadísticas del entrenamiento y evaluación

### Solución Temporal Implementada
Se reemplazó BatchNorm con LayerNorm, lo cual:
- ✅ Eliminó la variabilidad extrema
- ❌ Redujo el rendimiento máximo posible
- ❌ Los resultados son más estables pero no tan buenos como los mejores con BatchNorm

### Solución Propuesta para Reimplementar BatchNorm

#### 1. **BatchNorm Estabilizado**
```python
class StabilizedBatchNorm1d(nn.Module):
    def __init__(self, num_features, momentum=0.01, eps=1e-3):
        # Usar momentum muy bajo (0.01) para estadísticas más estables
        # Aumentar eps para evitar divisiones problemáticas
```

#### 2. **Tamaño de Batch Mínimo Garantizado**
- Problemas pequeños (≤20x20): min_batch_size = 8
- Problemas medianos (≤50x20): min_batch_size = 16-32  
- Problemas grandes (100x20): min_batch_size = 64
- Acumular experiencias si es necesario antes de actualizar

#### 3. **Manejo Especial para Batch Size = 1**
```python
if batch_size == 1 and self.training:
    # Usar Instance Normalization o modo eval temporalmente
    # No actualizar running stats con un solo ejemplo
```

#### 4. **Reset de Estadísticas Entre Problemas**
```python
def reset_batch_norm_stats(self):
    for module in self.modules():
        if isinstance(module, nn.BatchNorm1d):
            module.reset_running_stats()
            module.momentum = 0.01  # Momentum bajo
```

#### 5. **Gradient Accumulation**
Para problemas grandes, acumular gradientes sobre múltiples mini-batches:
- 50x20: accumulation_steps = 4
- 100x20: accumulation_steps = 8

#### 6. **Warmup del Learning Rate**
Implementar warmup para estabilizar el inicio del entrenamiento:
```python
if episode < warmup_episodes:
    lr = base_lr * (episode / warmup_episodes) ** 2
```

### Implementación Recomendada

1. **Crear una versión mejorada de BatchNorm** que maneje automáticamente casos edge
2. **Modificar el PPOAgent** para garantizar tamaños de batch mínimos
3. **Añadir configuración adaptativa** según el tamaño del problema
4. **Implementar warmup y gradient accumulation** para estabilidad
5. **Mantener LayerNorm como opción** para problemas donde BatchNorm falle

### Resultados Esperados
- Mantener los buenos resultados que BatchNorm puede dar
- Eliminar la variabilidad entre semillas
- Mejorar la estabilidad sin sacrificar rendimiento
- Resultados consistentes en problemas grandes
