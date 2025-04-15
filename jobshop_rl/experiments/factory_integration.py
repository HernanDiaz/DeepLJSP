"""
Módulo para la integración de los modelos GNN y Transformer
con el patrón Factory existente.

Extiende las clases de fábrica para permitir la creación
y configuración de agentes con arquitecturas avanzadas.
"""

import logging
import torch
from typing import Dict, Any, Optional

from jobshop_rl.agents.ppo_agent_gnn import AdvancedPPOAgent
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.utils.logging import TrainingLogger
from jobshop_rl.utils.problem_analyzer import AdaptiveConfigGenerator

# Configurar logger
logger = logging.getLogger("JobShopRL.AgentFactory")


class AdvancedAgentFactory:
    """
    Fábrica para crear agentes de RL con arquitecturas avanzadas.
    
    Esta clase extiende la funcionalidad de creación de agentes para
    incluir soporte para modelos GNN y Transformer.
    """
    
    @staticmethod
    def create_agent(env: JobShopEnv, model_type: str = 'gnn', 
                     csv_logger: Optional[TrainingLogger] = None, 
                     **agent_params) -> AdvancedPPOAgent:
        """
        Crea un agente avanzado con el tipo de modelo especificado.
        
        Args:
            env: Entorno de JobShop
            model_type: Tipo de modelo ('gnn', 'transformer', 'hybrid')
            csv_logger: Logger para datos de entrenamiento (opcional)
            **agent_params: Parámetros específicos del agente
            
        Returns:
            Agente PPO avanzado configurado
        """
        # Parámetros por defecto
        default_params = {
            "hidden_dim": 128,
            "lr": 0.0003,
            "gamma": 0.99,
            "eps_clip": 0.2,
            "K_epochs": 4,
            "entropy_coef": 0.01,
            "use_lr_decay": True,
            "use_grad_clip": True,
            "advantage_normalization": True,
            "gae_lambda": 0.95,
            "node_feature_dim": 7,
            "edge_feature_dim": 3,
            "sequence_feature_dim": 9,
            "num_gnn_layers": 2,
            "num_heads": 4,
            "num_attn_layers": 1
        }
        
        # Si el entorno tiene análisis del problema, adaptar parámetros
        if hasattr(env, 'problem_analysis') and not agent_params:
            adapted_params = AdaptiveConfigGenerator.generate_agent_config(env.problem_analysis)
            logger.info("Adaptando parámetros del agente según características del problema")
            
            # Adaptar parámetros específicos del modelo según tamaño del problema
            num_ops = env.num_jobs * env.num_machines
            
            # Para problemas más grandes, aumentar capacidad del modelo
            if num_ops > 200:  # Para problemas como 20x15 o más grandes
                adapted_params['hidden_dim'] = 256
                adapted_params['num_gnn_layers'] = 3
                adapted_params['num_heads'] = 8
                adapted_params['num_attn_layers'] = 2
            elif num_ops > 100:  # Para problemas medianos (10x10, 15x15)
                adapted_params['hidden_dim'] = 192
                adapted_params['num_gnn_layers'] = 2
                adapted_params['num_heads'] = 6
            
            # Combinar con parámetros por defecto
            adapted_params = {**default_params, **adapted_params}
            # Combinar con parámetros proporcionados
            adapted_params.update(agent_params)
            agent_params = adapted_params
        else:
            # Combinar con parámetros por defecto
            default_params.update(agent_params)
            agent_params = default_params
        
        # Añadir logger CSV si se proporciona
        if csv_logger:
            agent_params['csv_logger'] = csv_logger
        
        # Crear y devolver agente avanzado
        agent = AdvancedPPOAgent(
            env=env,
            model_type=model_type,
            **agent_params
        )
        
        return agent


class ExtendedAgentFactory:
    """
    Extensión del patrón Factory original para soportar tanto
    agentes tradicionales como avanzados con GNN y Transformer.
    
    Esta clase actúa como un puente entre el sistema existente y 
    las nuevas capacidades.
    """
    
    @staticmethod
    def create_agent(env: JobShopEnv, agent_type: str = 'ppo', 
                     model_type: Optional[str] = None,
                     csv_logger: Optional[TrainingLogger] = None, 
                     **agent_params) -> Any:
        """
        Crea un agente del tipo especificado.
        
        Args:
            env: Entorno de JobShop
            agent_type: Tipo de agente ('ppo', 'advanced')
            model_type: Tipo de modelo para agentes avanzados
            csv_logger: Logger para datos de entrenamiento
            **agent_params: Parámetros específicos del agente
            
        Returns:
            Agente configurado del tipo especificado
        """
        if agent_type.lower() == 'advanced':
            # Verificar tipo de modelo
            if model_type not in ['gnn', 'transformer', 'hybrid']:
                logger.warning(f"Tipo de modelo {model_type} no reconocido. Usando 'gnn' por defecto.")
                model_type = 'gnn'
            
            logger.info(f"Creando agente avanzado con modelo {model_type}")
            return AdvancedAgentFactory.create_agent(
                env=env,
                model_type=model_type,
                csv_logger=csv_logger,
                **agent_params
            )
        else:
            # Usar la factory original para otros tipos de agente
            # Importar aquí para evitar dependencia circular
            from jobshop_rl.experiments.factory import AgentFactory
            
            return AgentFactory.create_agent(
                env=env,
                csv_logger=csv_logger,
                **agent_params
            )


# Extensión del ExperimentFactory para usar agentes avanzados
def extend_experiment_factory():
    """
    Extiende la clase ExperimentFactory existente para soportar
    agentes avanzados con GNN y Transformer.
    
    Esta función debe ser llamada antes de usar ExperimentFactory
    si se desea utilizar los agentes avanzados.
    """
    # Importar ExperimentFactory
    from jobshop_rl.experiments.factory import ExperimentFactory
    
    # Guardar método create_experiment original
    original_create_experiment = ExperimentFactory.create_experiment
    
    @staticmethod
    def extended_create_experiment(
        problem_id: str, 
        reward_strategy: str = "adaptive",
        agent_type: str = 'ppo',
        model_type: Optional[str] = None,
        agent_params: Dict = None, 
        reward_params: Dict = None,
        seed: Optional[int] = None,
        visualize: bool = True,
        save_plots: bool = True,
        output_dir: str = 'outputs',
        experiment_name: Optional[str] = None,
        csv_logger: Optional[TrainingLogger] = None
    ):
        """
        Versión extendida de create_experiment que soporta agentes avanzados.
        """
        # Si se solicita un agente avanzado
        if agent_type.lower() == 'advanced':
            # Usar el flujo original para crear entorno
            env, _, runner = original_create_experiment(
                problem_id=problem_id,
                reward_strategy=reward_strategy,
                agent_params={},  # Parámetros vacíos para no crear agente
                reward_params=reward_params,
                seed=seed,
                visualize=visualize,
                save_plots=save_plots,
                output_dir=output_dir,
                experiment_name=experiment_name,
                csv_logger=csv_logger
            )
            
            # Crear agente avanzado
            agent = ExtendedAgentFactory.create_agent(
                env=env,
                agent_type='advanced',
                model_type=model_type or 'gnn',
                csv_logger=csv_logger,
                **(agent_params or {})
            )
            
            # Actualizar runner con el nuevo agente
            runner.agent = agent
            
            return env, agent, runner
        else:
            # Usar flujo original para agentes estándar
            return original_create_experiment(
                problem_id=problem_id,
                reward_strategy=reward_strategy,
                agent_params=agent_params,
                reward_params=reward_params,
                seed=seed,
                visualize=visualize,
                save_plots=save_plots,
                output_dir=output_dir,
                experiment_name=experiment_name,
                csv_logger=csv_logger
            )
    
    # Reemplazar método en la clase
    ExperimentFactory.create_experiment = extended_create_experiment
    
    # También extender el método run_full_experiment
    original_run_full_experiment = ExperimentFactory.run_full_experiment
    
    @staticmethod
    def extended_run_full_experiment(
        episodes: int = 100, 
        reward_strategy: str = "adaptive",
        agent_type: str = 'ppo',
        model_type: Optional[str] = None,
        agent_params: Dict = None, 
        reward_params: Dict = None,
        problem_id: str = "ft10", 
        seed: Optional[int] = None, 
        visualize: bool = True, 
        save_plots: bool = True, 
        csv_logging: bool = True, 
        csv_filename: Optional[str] = None, 
        csv_base_dir: str = 'outputs', 
        output_dir: str = 'outputs', 
        experiment_name: Optional[str] = None,
        evaluate_other_problem: bool = False,
        evaluation_problem_id: Optional[str] = None,
        use_ortools: bool = False,
        ortools_time_limit: int = 60
    ):
        """
        Versión extendida de run_full_experiment que soporta agentes avanzados.
        """
        # Actualizar parámetros para incluir tipo de agente y modelo
        config = {
            'agent_type': agent_type,
            'model_type': model_type
        }
        
        # Llamar al método original con los parámetros actualizados
        return original_run_full_experiment(
            episodes=episodes,
            reward_strategy=reward_strategy,
            agent_params=agent_params,
            reward_params=reward_params,
            problem_id=problem_id,
            seed=seed,
            visualize=visualize,
            save_plots=save_plots,
            csv_logging=csv_logging,
            csv_filename=csv_filename,
            csv_base_dir=csv_base_dir,
            output_dir=output_dir,
            experiment_name=experiment_name,
            evaluate_other_problem=evaluate_other_problem,
            evaluation_problem_id=evaluation_problem_id,
            use_ortools=use_ortools,
            ortools_time_limit=ortools_time_limit,
            **config
        )
    
    # Reemplazar método en la clase
    ExperimentFactory.run_full_experiment = extended_run_full_experiment
    
    logger.info("ExperimentFactory extendido para soportar agentes avanzados GNN/Transformer")
