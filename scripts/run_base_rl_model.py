"""
Script para ejecutar el modelo base de aprendizaje por refuerzo en problemas de Job Shop Scheduling.
"""

import os
import sys
import logging
import matplotlib.pyplot as plt

# Añadir el directorio raíz del proyecto al path para poder importar jobshop_rl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jobshop_rl.experiments.factory import ExperimentFactory

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("JSP-BaseRL")

def run_base_rl_model(problem_id="ft10", episodes=200):
    """
    Entrena y evalúa el modelo base de aprendizaje por refuerzo en el problema especificado.
    
    Args:
        problem_id: Identificador del problema JSP a resolver
        episodes: Número de episodios de entrenamiento
        
    Returns:
        agent: Agente entrenado
        best_makespan: Mejor makespan alcanzado durante el entrenamiento
        final_makespan: Makespan de la evaluación final
    """
    logger.info(f"Ejecutando modelo base de RL en problema {problem_id}...")
    
    # Crear experimento con modelo base de PPO
    env, agent, runner = ExperimentFactory.create_experiment(
        problem_id=problem_id,
        agent_type='ppo',  # Usar el agente PPO básico
        reward_strategy="adaptive",
        output_dir='outputs/base_rl_example',
        experiment_name=f"base_rl_{problem_id}"
    )
    
    # Entrenar el agente
    logger.info(f"Iniciando entrenamiento por {episodes} episodios...")
    best_makespan, results = runner.train(episodes=episodes)
    
    # Evaluar el rendimiento final
    logger.info("Evaluando política entrenada...")
    final_makespan, final_schedule, _, _ = agent.evaluate_policy()
    
    # Guardar modelo y visualizaciones
    os.makedirs('outputs/base_rl_example', exist_ok=True)
    os.makedirs('outputs/models', exist_ok=True)
    
    # Guardar el modelo entrenado
    model_path = f'outputs/models/base_rl_{problem_id}.pt'
    agent.save_model(model_path)
    logger.info(f"Modelo guardado en: {model_path}")
    
    # Generar y guardar visualización del plan
    env.render_schedule(
        title=f"Planificación RL Base (Makespan: {final_makespan})", 
        schedule=final_schedule
    )
    plt.savefig('outputs/base_rl_example/final_schedule.png')
    plt.close()
    
    # Visualizar progreso de entrenamiento
    plt.figure(figsize=(10, 6))
    plt.plot(results['makespan_history'])
    plt.title('Evolución del Makespan durante entrenamiento')
    plt.xlabel('Episodios')
    plt.ylabel('Makespan')
    plt.grid(True, alpha=0.3)
    plt.savefig('outputs/base_rl_example/training_progress.png')
    plt.close()
    
    logger.info(f"Ejemplo completado. Mejor makespan: {best_makespan}, Final: {final_makespan}")
    
    return agent, best_makespan, final_makespan

if __name__ == "__main__":
    # Si se pasan argumentos por línea de comandos, usarlos como problem_id y episodes
    if len(sys.argv) > 1:
        problem_id = sys.argv[1]
        episodes = int(sys.argv[2]) if len(sys.argv) > 2 else 200
        agent, best_makespan, final_makespan = run_base_rl_model(problem_id, episodes)
    else:
        # Usar valores por defecto
        agent, best_makespan, final_makespan = run_base_rl_model()
    
    print(f"Ejemplo completado. Mejor makespan: {best_makespan}, Makespan final: {final_makespan}")
