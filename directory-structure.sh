jobshop_rl/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── data_models.py        # Clases de datos (Operation, SchedulingStep, etc.)
│   └── neural_models.py      # Modelos de redes neuronales
├── environment/
│   ├── __init__.py
│   └── job_shop_env.py       # Entorno de Job Shop
├── agents/
│   ├── __init__.py
│   ├── base_agent.py         # Clase base para agentes
│   ├── ppo_agent.py          # Implementación de PPO
│   └── ppo_memory.py         # Memoria para el agente PPO
├── rewards/
│   ├── __init__.py
│   └── strategies.py         # Estrategias de recompensa
├── heuristics/
│   ├── __init__.py
│   └── strategies.py         # Estrategias heurísticas
├── utils/
│   ├── __init__.py
│   ├── visualization.py      # Funciones de visualización
│   ├── logging.py            # TrainingLogger
│   ├── checkpoint_manager.py # Gestión de checkpoints
│   ├── experiment_config.py  # Configuración de experimentos
│   └── path_utils.py         # Utilidades para manejo de rutas
├── experiments/
│   ├── __init__.py
│   ├── factory.py            # ExperimentFactory
│   ├── evaluator.py          # HeuristicEvaluator
│   └── batch_experimenter.py # Para entrenamiento por lotes
├── data/
│   ├── __init__.py
│   ├── problem_loader.py     # Cargador de problemas
│   ├── training_problems/    # Directorio para problemas de entrenamiento
│   └── test_problems/        # Directorio para problemas de prueba
└── main.py                   # Punto de entrada principal
