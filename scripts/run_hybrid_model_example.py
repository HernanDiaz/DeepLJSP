"""
Script para ejecutar un ejemplo de entrenamiento con el modelo híbrido GNN + Atención
"""

import os
import sys
import logging
import matplotlib.pyplot as plt

# Añadir el directorio raíz del proyecto al path para poder importar jobshop_rl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jobshop_rl.experiments.factory_integration import ExtendedAgentFactory
from jobshop_rl.experiments.factory import EnvironmentFactory

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("JSP-HybridModel")

def run_hybrid_model_example(problem_id="ft10", episodes=100):
    """
    Entrena y evalúa un modelo híbrido GNN + Atención en el problema especificado.
    
    Args:
        problem_id: Identificador del problema JSP a resolver
        episodes: Número de episodios de entrenamiento
        
    Returns:
        agent: Agente entrenado
        best_makespan: Mejor makespan alcanzado durante el entrenamiento
        final_makespan: Makespan de la evaluación final
    """
    logger.info(f"Ejecutando ejemplo de modelo híbrido en problema {problem_id}...")
    
    # Crear entorno
    env = EnvironmentFactory.create_from_problem_id(
        problem_id=problem_id,
        reward_strategy="adaptive"
    )
    
    # Configurar parámetros del modelo híbrido
    agent_params = {
        "hidden_dim": 160,              # Dimensión de características ocultas
        "num_gnn_layers": 2,            # Número de capas GNN
        "num_heads": 4,                 # Número de cabezas de atención
        "num_attn_layers": 1,           # Número de capas de atención
        "node_feature_dim": 14,         # Dimensión de características de nodos 
        "edge_feature_dim": 3,          # Dimensión de características de aristas
        "lr": 0.0003                    # Tasa de aprendizaje
    }
    
    # Crear agente con modelo híbrido
    agent = ExtendedAgentFactory.create_agent(
        env=env,
        agent_type='advanced',
        model_type='hybrid',
        **agent_params
    )
    
    # Entrenar el agente
    logger.info(f"Iniciando entrenamiento por {episodes} episodios...")
    agent.train(
        episodes=episodes,
        dynamic_entropy=True,
        early_stopping=True,
        patience=20
    )
    
    # Evaluar el rendimiento final
    logger.info("Evaluando política entrenada...")
    final_makespan, final_schedule, _, _ = agent.evaluate_policy()
    
    # Guardar modelo y visualizaciones
    os.makedirs('outputs/hybrid_example', exist_ok=True)
    os.makedirs('outputs/models', exist_ok=True)
    
    # Guardar el modelo entrenado
    model_path = f'outputs/models/hybrid_{problem_id}.pt'
    agent.save_checkpoint(model_path)
    logger.info(f"Modelo guardado en: {model_path}")
    
    # Generar y guardar visualización del plan
    env.render_schedule(
        title=f"Planificación Modelo Híbrido (Makespan: {final_makespan})", 
        schedule=final_schedule
    )
    plt.savefig('outputs/hybrid_example/final_schedule.png')
    plt.close()
    
    # Visualizar progreso de entrenamiento
    training_fig = agent.plot_training_history()
    plt.savefig('outputs/hybrid_example/training_progress.png')
    plt.close()
    
    # Visualizar pérdidas durante el entrenamiento
    losses_fig = agent.plot_losses()
    if losses_fig:
        plt.savefig('outputs/hybrid_example/training_losses.png')
        plt.close()
        
    logger.info(f"Ejemplo completado. Mejor makespan: {agent.best_makespan}, Final: {final_makespan}")
    
    return agent, agent.best_makespan, final_makespan

if __name__ == "__main__":
    # Si se pasan argumentos por línea de comandos, usarlos como problem_id y episodes
    if len(sys.argv) > 1:
        problem_id = sys.argv[1]
        episodes = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        agent, best_makespan, final_makespan = run_hybrid_model_example(problem_id, episodes)
    else:
        # Usar valores por defecto
        agent, best_makespan, final_makespan = run_hybrid_model_example()
    
    print(f"Ejemplo completado. Mejor makespan: {best_makespan}, Makespan final: {final_makespan}")
