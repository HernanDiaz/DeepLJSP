"""
Ejemplos de uso de arquitecturas GNN y mecanismos de atención
para Job Shop Scheduling.

Este módulo proporciona ejemplos prácticos para utilizar las
nuevas arquitecturas de redes neuronales y el entrenamiento
con múltiples instancias.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("JSP-Examples")

# Ejemplo 1: Entrenamiento con modelo GNN en un problema específico
def example_single_problem_gnn():
    """
    Ejemplo de entrenamiento con modelo GNN en un problema.
    """
    from jobshop_rl.experiments.factory_integration import extend_experiment_factory
    from jobshop_rl.experiments.factory import ExperimentFactory
    
    # Extender el ExperimentFactory para soportar modelos avanzados
    extend_experiment_factory()
    
    # Crear experimento con modelo GNN
    problem_id = "ft10"  # Problema 10x10
    episodes = 30
    
    # Parámetros del modelo GNN
    agent_params = {
        "hidden_dim": 128,
        "num_gnn_layers": 2,
        "node_feature_dim": 14,  # Cambiado de 7 a 14 para coincidir con las características generadas
        "edge_feature_dim": 3
    }
    
    env, agent, runner = ExperimentFactory.create_experiment(
        problem_id=problem_id,
        agent_type='advanced',
        model_type='gnn',
        agent_params=agent_params,
        reward_strategy="adaptive",
        output_dir='outputs/gnn_example',
        experiment_name=f"gnn_{problem_id}"
    )
    
    # Entrenar
    best_makespan, results = runner.train(episodes=episodes, dynamic_entropy=True)
    
    # Evaluación final
    final_makespan, final_schedule, _, _ = agent.evaluate_policy()
    
    # Guardar modelo
    os.makedirs('outputs/models', exist_ok=True)
    agent.save_checkpoint('outputs/models/gnn_ft10.pt')  # Usando save_checkpoint en lugar de save_model
    
    # Visualizar planificación final
    env.render_schedule(title=f"Planificación final GNN (Makespan: {final_makespan})", 
                       schedule=final_schedule)
    plt.savefig('outputs/gnn_example/final_schedule.png')
    
    # Visualizar progreso de entrenamiento
    training_fig = agent.plot_training_history()
    plt.savefig('outputs/gnn_example/training_progress.png')
    
    return agent, best_makespan, final_makespan

# Ejemplo 2: Modelo Transformer para un problema más grande
def example_transformer_large_problem():
    """
    Ejemplo de modelo Transformer para un problema más grande.
    """
    from jobshop_rl.experiments.factory_integration import ExtendedAgentFactory
    from jobshop_rl.experiments.factory import EnvironmentFactory
    
    # Problema más grande (20x20)
    problem_id = "tai20_20_01"
    
    # Crear entorno
    env = EnvironmentFactory.create_from_problem_id(
        problem_id=problem_id,
        reward_strategy="adaptive"
    )
    
    # Crear agente Transformer
    agent_params = {
        "hidden_dim": 192,  # Más capacidad para problema grande
        "num_heads": 6,
        "num_attn_layers": 2,
        "sequence_feature_dim": 16,  # Actualizado de 9 a 16 para coincidir con las dimensiones reales
        "lr": 0.0002  # Tasa de aprendizaje más baja para estabilidad
    }
    
    agent = ExtendedAgentFactory.create_agent(
        env=env,
        agent_type='advanced',
        model_type='transformer',
        **agent_params
    )
    
    # Entrenar por menos episodios (los Transformer pueden converger más rápido)
    agent.train(
        episodes=50,
        dynamic_entropy=True,
        early_stopping=True,
        patience=20  # Cambiado early_stopping_patience a patience para que coincida con la definición
    )
    
    # Evaluar
    final_makespan, final_schedule, _, _ = agent.evaluate_policy()
    
    # Guardar modelo y visualizaciones
    os.makedirs('outputs/transformer_example', exist_ok=True)
    os.makedirs('outputs/models', exist_ok=True)
    
    agent.save_checkpoint('outputs/models/transformer_tai20_20_01.pt')  # Usando save_checkpoint en lugar de save_model
    
    env.render_schedule(title=f"Planificación Transformer (Makespan: {final_makespan})", 
                       schedule=final_schedule)
    plt.savefig('outputs/transformer_example/final_schedule.png')
    
    # Si el problema es suficientemente pequeño, visualizar atención
    if env.num_jobs * env.num_machines <= 100:
        state = env.reset()
        attn_fig = agent.plot_attention_weights(state)
        if attn_fig:
            plt.savefig('outputs/transformer_example/attention_weights.png')
    
    return agent, agent.best_makespan, final_makespan

# Ejemplo 3: Entrenamiento con múltiples instancias
def example_multi_instance_training():
    """
    Ejemplo de entrenamiento con múltiples instancias para mejorar generalización.
    """
    from jobshop_rl.training.multi_instance_trainer import MultiInstanceTrainer
    
    # Lista de problemas para entrenamiento
    # Incluir diversos tamaños ayuda a la generalización
    problems = [
        "ft10",       # 10x10
        "ft20",       # 20x5
        "abz10",      # 10x10 diferente
        "tai20_20_01", # 20x20
        "tai20_20_02"  # 20x20 diferente
    ]
    
    # Crear entrenador multi-instancia con GNN híbrido
    trainer = MultiInstanceTrainer(
        problem_ids=problems,
        agent_type='advanced',
        model_type='hybrid',  # Modelo híbrido GNN + Atención
        reward_strategy='adaptive',
        agent_params={
            "hidden_dim": 160,
            "num_gnn_layers": 2,
            "num_heads": 4,
            "num_attn_layers": 1
        },
        use_curriculum=True,   # Empezar con problemas más simples
        curriculum_strategy='size',
        batch_size=2,          # Entrenar en 2 problemas por lote
        epochs_per_instance=15,
        total_episodes=500,
        output_dir='outputs/multi_instance'
    )
    
    # Entrenar modelo
    agent, results = trainer.train()
    
    # Evaluar en todos los problemas usados para entrenamiento
    eval_results = trainer.evaluate(problems)
    
    # También evaluar en un problema no visto durante entrenamiento
    if "tai50_15_01" not in problems:
        new_problem_results = trainer.evaluate(["tai50_15_01"])
        # Combinar resultados
        eval_results.update(new_problem_results)
    
    # Imprimir resumen de resultados
    logger.info("Resultados de evaluación:")
    for problem_id, result in eval_results.items():
        logger.info(f"  {problem_id}: Makespan = {result['makespan']}")
    
    # Guardar gráfico de progreso
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extraer datos de historial
    episodes = [entry['episode'] for entry in results['training_history']]
    performances = [entry['avg_performance'] for entry in results['training_history']]
    
    ax.plot(episodes, performances, label='Rendimiento promedio')
    ax.set_xlabel('Episodios')
    ax.set_ylabel('Makespan promedio')
    ax.set_title('Progreso de entrenamiento multi-instancia')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.savefig('outputs/multi_instance/training_progress.png')
    
    return agent, eval_results, results

# Ejemplo 4: Comparación entre diferentes arquitecturas
def example_architecture_comparison():
    """
    Compara diferentes arquitecturas en el mismo problema.
    """
    from jobshop_rl.experiments.factory_integration import ExtendedAgentFactory
    from jobshop_rl.experiments.factory import EnvironmentFactory
    import pandas as pd
    
    # Problema de prueba (tamaño mediano)
    problem_id = "abz10"  # 10x10
    
    # Arquitecturas a comparar
    architectures = [
        {"name": "GNN", "type": "gnn", "params": {
            "hidden_dim": 128, "num_gnn_layers": 2
        }},
        {"name": "Transformer", "type": "transformer", "params": {
            "hidden_dim": 128, "num_heads": 4, "num_attn_layers": 2
        }},
        {"name": "Híbrido", "type": "hybrid", "params": {
            "hidden_dim": 128, "num_gnn_layers": 2, "num_heads": 4,
            "num_attn_layers": 1
        }}
    ]
    
    # Configuración de entrenamiento
    episodes = 200
    num_runs = 3  # Repeticiones para robustez
    
    # Crear entorno
    env = EnvironmentFactory.create_from_problem_id(
        problem_id=problem_id,
        reward_strategy="adaptive"
    )
    
    # Preparar resultados
    comparison_results = {
        "Architecture": [],
        "Run": [],
        "Best Makespan": [],
        "Avg Makespan": [],
        "Training Time": [],
        "Evaluation Makespan": []
    }
    
    # Hacer comparación
    for architecture in architectures:
        logger.info(f"Evaluando arquitectura: {architecture['name']}")
        
        for run in range(1, num_runs + 1):
            logger.info(f"Ejecución {run}/{num_runs}")
            
            # Crear agente con la arquitectura específica
            agent = ExtendedAgentFactory.create_agent(
                env=env,
                agent_type='advanced',
                model_type=architecture['type'],
                **architecture['params']
            )
            
            # Medir tiempo de entrenamiento
            start_time = time.time()
            
            # Entrenar agente
            agent.train(
                episodes=episodes,
                early_stopping=True,
                patience=20  # Cambiado early_stopping_patience a patience para que coincida con la definición
            )
            
            training_time = time.time() - start_time
            
            # Evaluar rendimiento
            eval_makespan, eval_schedule, _, eval_time = agent.evaluate_policy()
            
            # Guardar resultados
            comparison_results["Architecture"].append(architecture['name'])
            comparison_results["Run"].append(run)
            comparison_results["Best Makespan"].append(agent.best_makespan)
            comparison_results["Avg Makespan"].append(np.mean(agent.training_makespan_history[-20:] if len(agent.training_makespan_history) >= 20 else agent.training_makespan_history))
            comparison_results["Training Time"].append(training_time)
            comparison_results["Evaluation Makespan"].append(eval_makespan)
            
            logger.info(f"Resultados: Mejor={agent.best_makespan}, Eval={eval_makespan:.2f}, Tiempo={training_time:.2f}s")
    
    # Crear DataFrame con resultados
    results_df = pd.DataFrame(comparison_results)
    
    # Guardar resultados
    os.makedirs('outputs/architecture_comparison', exist_ok=True)
    results_df.to_csv('outputs/architecture_comparison/results.csv', index=False)
    
    # Visualizar comparación
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    
    # Gráfico 1: Comparar makespan promedio
    average_by_arch = results_df.groupby('Architecture')[['Best Makespan', 'Evaluation Makespan']].mean()
    average_by_arch.plot(kind='bar', ax=axs[0], rot=0)
    axs[0].set_title('Comparación de Makespan')
    axs[0].set_ylabel('Makespan')
    axs[0].grid(axis='y', alpha=0.3)
    
    # Gráfico 2: Comparar tiempo de entrenamiento
    average_time = results_df.groupby('Architecture')['Training Time'].mean()
    average_time.plot(kind='bar', ax=axs[1], rot=0, color='orange')
    axs[1].set_title('Tiempo de Entrenamiento')
    axs[1].set_ylabel('Segundos')
    axs[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('outputs/architecture_comparison/comparison_chart.png')
    
    return results_df