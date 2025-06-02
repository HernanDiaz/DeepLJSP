"""
Modelos de redes neuronales para Job Shop RL.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional
from jobshop_rl.models.normalization import (
    StabilizedBatchNorm1d, 
    AdaptiveNormalization,
    create_normalization_layer
)

class FeatureExtractor(nn.Module):
    """Extractor de características para las operaciones"""

    def __init__(self, input_dim: int, hidden_dim: int, depth: int = 2):
        super(FeatureExtractor, self).__init__()
        
        # Crear una lista con capas y activaciones
        layers = []
        layers.append(nn.Linear(input_dim, hidden_dim))
        layers.append(nn.ReLU())
        
        # Añadir capas ocultas adicionales si se requiere más profundidad
        for _ in range(depth-1):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
            layers.append(nn.ReLU())
            
        # Convertir la lista a un módulo secuencial
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

class PolicyNetwork(nn.Module):
    """Red neuronal para la política de selección de acciones"""

    def __init__(self, input_dim: int, hidden_dim: int, depth: int = 2):
        super(PolicyNetwork, self).__init__()
        self.feature_extractor = FeatureExtractor(input_dim, hidden_dim, depth)
        self.output = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor) -> Optional[torch.Tensor]:
        if x.size(0) == 0:
            return None

        features = self.feature_extractor(x)
        logits = self.output(features).squeeze(-1)
        return F.softmax(logits, dim=0)

class ValueNetwork(nn.Module):
    """Red neuronal para la función de valor"""

    def __init__(self, state_dim: int, hidden_dim: int, depth: int = 3):
        super(ValueNetwork, self).__init__()
        
        # Crear una lista con capas y activaciones
        layers = []
        layers.append(nn.Linear(state_dim, hidden_dim))
        layers.append(nn.ReLU())
        
        # Añadir capas ocultas adicionales
        for _ in range(depth-2):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
            layers.append(nn.ReLU())
            
        # Capa de salida
        layers.append(nn.Linear(hidden_dim, 1))
        
        # Convertir la lista a un módulo secuencial
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

# Nuevas clases para la arquitectura avanzada
class EnhancedFeatureExtractor(nn.Module):
    """Extractor de características mejorado con normalización estabilizada"""
    
    def __init__(self, 
                 input_dim: int, 
                 hidden_dim: int, 
                 depth: int = 3, 
                 dropout_rate: float = 0.1,
                 problem_size: int = 100,
                 use_batch_norm: bool = True):
        super(EnhancedFeatureExtractor, self).__init__()
        
        self.use_batch_norm = use_batch_norm
        self.problem_size = problem_size
        
        # Estructura modular: creamos una lista de capas
        layers = []
        
        # Primera capa: entrada -> hidden_dim
        layers.append(nn.Linear(input_dim, hidden_dim))
        if use_batch_norm:
            layers.append(create_normalization_layer(
                hidden_dim, problem_size, "adaptive"
            ))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(dropout_rate))
        
        # Capas intermedias con aumento gradual de dimensionalidad
        current_dim = hidden_dim
        expansion_factor = 1.0
        
        # Para problemas muy grandes (100x20), usar una arquitectura más expresiva
        if hidden_dim >= 512:
            expansion_factor = 1.5  # Aumentar el factor de expansión
            
        for i in range(depth - 1):
            # Para las primeras capas, aumentar dimensionalidad
            if i < depth // 2:
                next_dim = int(current_dim * expansion_factor)
            # Para las últimas, reducir o mantener
            else:
                next_dim = current_dim
                
            layers.append(nn.Linear(current_dim, next_dim))
            if use_batch_norm:
                layers.append(create_normalization_layer(
                    next_dim, problem_size, "adaptive"
                ))
            # Usar LeakyReLU para problemas grandes para evitar neuronas muertas
            if hidden_dim >= 512:
                layers.append(nn.LeakyReLU(0.1))
            else:
                layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            
            current_dim = next_dim
        
        # Registrar las capas como ModuleList para que PyTorch las reconozca
        self.layers = nn.ModuleList(layers)
        self.output_dim = current_dim  # Guardar dimensión de salida
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.size(0)
        
        # Si no hay batch, manejar ese caso especial
        if batch_size == 0:
            return torch.zeros((0, self.output_dim), device=x.device if x.device else torch.device('cpu'))
            
        # Procesar secuencialmente por tipo de capa
        i = 0
        while i < len(self.layers):
            layer = self.layers[i]
            
            # Aplicar la capa lineal
            if isinstance(layer, nn.Linear):
                x = layer(x)
                i += 1
                
                # Si la siguiente capa es de normalización, aplicarla
                if i < len(self.layers) and isinstance(self.layers[i], (AdaptiveNormalization, StabilizedBatchNorm1d, nn.BatchNorm1d, nn.LayerNorm)):
                    x = self.layers[i](x)
                    i += 1
                    
                # Si la siguiente capa es de activación, aplicarla
                if i < len(self.layers) and isinstance(self.layers[i], (nn.ReLU, nn.LeakyReLU)):
                    x = self.layers[i](x)
                    i += 1
                    
                # Si la siguiente capa es dropout, aplicarla solo en training
                if i < len(self.layers) and isinstance(self.layers[i], nn.Dropout):
                    if self.training:
                        x = self.layers[i](x)
                    i += 1
            else:
                # Si no es una capa lineal, simplemente aplicarla
                x = layer(x)
                i += 1
            
        return x

class AdvancedPolicyNetwork(nn.Module):
    """Red de política avanzada para problemas grandes"""
    
    def __init__(self, 
                 input_dim: int, 
                 hidden_dim: int, 
                 depth: int = 3, 
                 dropout_rate: float = 0.1,
                 problem_size: int = 100,
                 use_batch_norm: bool = True):
        super(AdvancedPolicyNetwork, self).__init__()
        self.feature_extractor = EnhancedFeatureExtractor(
            input_dim, hidden_dim, depth, dropout_rate, problem_size, use_batch_norm
        )
        self.output = nn.Linear(self.feature_extractor.output_dim, 1)
        
    def forward(self, x: torch.Tensor) -> Optional[torch.Tensor]:
        if x.size(0) == 0:
            return None
            
        features = self.feature_extractor(x)
        logits = self.output(features).squeeze(-1)
        result = F.softmax(logits, dim=0)
        
        return result

class AdvancedValueNetwork(nn.Module):
    """Red de valor avanzada para problemas grandes"""
    
    def __init__(self, 
                 state_dim: int, 
                 hidden_dim: int, 
                 depth: int = 4, 
                 dropout_rate: float = 0.1,
                 problem_size: int = 100,
                 use_batch_norm: bool = True):
        super(AdvancedValueNetwork, self).__init__()
        
        self.use_batch_norm = use_batch_norm
        self.problem_size = problem_size
        
        # Primera capa con dimensión fija
        layers = []
        layers.append(nn.Linear(state_dim, hidden_dim))
        if use_batch_norm:
            layers.append(create_normalization_layer(
                hidden_dim, problem_size, "adaptive"
            ))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(dropout_rate))
        
        # Capas intermedias con expansión y contracción
        current_dim = hidden_dim
        mid_point = depth // 2
        
        for i in range(1, depth):
            # Fase de expansión
            if i <= mid_point:
                next_dim = int(current_dim * 1.5)
            # Fase de contracción
            else:
                next_dim = int(current_dim / 1.5)
                
            next_dim = max(next_dim, hidden_dim)  # No reducir demasiado
            
            layers.append(nn.Linear(current_dim, next_dim))
            if use_batch_norm:
                layers.append(create_normalization_layer(
                    next_dim, problem_size, "adaptive"
                ))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            
            current_dim = next_dim
        
        # Capa final para salida escalar
        layers.append(nn.Linear(current_dim, 1))
        
        self.layers = nn.ModuleList(layers)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Procesar todas las capas
        i = 0
        while i < len(self.layers):
            layer = self.layers[i]
            
            # Aplicar la capa
            if isinstance(layer, nn.Linear):
                x = layer(x)
                i += 1
                
                # Si la siguiente capa es de normalización, aplicarla
                if i < len(self.layers) and isinstance(self.layers[i], (AdaptiveNormalization, StabilizedBatchNorm1d, nn.BatchNorm1d, nn.LayerNorm)):
                    x = self.layers[i](x)
                    i += 1
                    
                # Si la siguiente capa es de activación, aplicarla
                if i < len(self.layers) and isinstance(self.layers[i], (nn.ReLU, nn.LeakyReLU)):
                    x = self.layers[i](x)
                    i += 1
                    
                # Si la siguiente capa es dropout, aplicarla solo en training
                if i < len(self.layers) and isinstance(self.layers[i], nn.Dropout):
                    if self.training:
                        x = self.layers[i](x)
                    i += 1
            else:
                # Si no es una capa lineal, simplemente aplicarla
                x = layer(x)
                i += 1
            
        return x

def calculate_hidden_dim(num_jobs, num_machines):
    """Calcula el tamaño adecuado de la capa oculta basado en el tamaño del problema"""
    # Para problemas pequeños, dimensión mínima de 128
    # Para problemas grandes, escalar hasta 512
    base_dim = 128
    problem_size = num_jobs * num_machines
    
    if problem_size <= 100:  # 10x10 o menos
        return base_dim
    elif problem_size <= 400:  # hasta 20x20
        return 256
    elif problem_size <= 2000:  # hasta 100x20 (incluido)
        return 384
    else:  # Para problemas extremadamente grandes
        return 512
