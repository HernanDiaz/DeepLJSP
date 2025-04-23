"""
Modelos de redes neuronales para Job Shop RL.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional

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
    """Extractor de características mejorado con dropout y normalización por lotes"""
    
    def __init__(self, input_dim: int, hidden_dim: int, depth: int = 3, dropout_rate: float = 0.1):
        super(EnhancedFeatureExtractor, self).__init__()
        
        # Estructura modular: creamos una lista de capas
        layers = []
        
        # Primera capa: entrada -> hidden_dim
        layers.append(nn.Linear(input_dim, hidden_dim))
        layers.append(nn.BatchNorm1d(hidden_dim))
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
            layers.append(nn.BatchNorm1d(next_dim))
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
            
        # Procesar secuencialmente en grupos de 4 componentes
        # (Linear + BatchNorm + ReLU + Dropout)
        for i in range(0, len(self.layers), 4):
            linear = self.layers[i]
            batch_norm = self.layers[i+1]
            relu = self.layers[i+2]
            dropout = self.layers[i+3]
            
            x = linear(x)
            # BatchNorm requiere más de 1 muestra en modo entrenamiento
            if batch_size > 1:
                x = batch_norm(x)
            x = relu(x)
            x = dropout(x)
            
        return x

class AdvancedPolicyNetwork(nn.Module):
    """Red de política avanzada para problemas grandes"""
    
    def __init__(self, input_dim: int, hidden_dim: int, depth: int = 3, dropout_rate: float = 0.1):
        super(AdvancedPolicyNetwork, self).__init__()
        self.feature_extractor = EnhancedFeatureExtractor(
            input_dim, hidden_dim, depth, dropout_rate
        )
        self.output = nn.Linear(self.feature_extractor.output_dim, 1)
        
    def forward(self, x: torch.Tensor) -> Optional[torch.Tensor]:
        if x.size(0) == 0:
            return None
            
        # Para el caso de batch size 1 en modo entrenamiento
        small_batch = x.size(0) < 2
        if small_batch and self.training:
            # Cambiar temporalmente las BatchNorm a modo evaluación
            original_modes = {}
            for name, module in self.feature_extractor.named_modules():
                if isinstance(module, nn.BatchNorm1d):
                    original_modes[name] = module.training
                    module.eval()
        else:
            original_modes = None
            
        features = self.feature_extractor(x)
        logits = self.output(features).squeeze(-1)
        result = F.softmax(logits, dim=0)
        
        # Restaurar modos originales
        if original_modes:
            for name, module in self.feature_extractor.named_modules():
                if name in original_modes:
                    module.training = original_modes[name]
        
        return result

class AdvancedValueNetwork(nn.Module):
    """Red de valor avanzada para problemas grandes"""
    
    def __init__(self, state_dim: int, hidden_dim: int, depth: int = 4, dropout_rate: float = 0.1):
        super(AdvancedValueNetwork, self).__init__()
        
        # Primera capa con dimensión fija
        layers = []
        layers.append(nn.Linear(state_dim, hidden_dim))
        layers.append(nn.BatchNorm1d(hidden_dim))
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
            layers.append(nn.BatchNorm1d(next_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            
            current_dim = next_dim
        
        # Capa final para salida escalar
        layers.append(nn.Linear(current_dim, 1))
        
        self.layers = nn.ModuleList(layers)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.size(0) if len(x.size()) > 0 else 0
        
        # Si el input es 1D (un solo ejemplo), añadir dimensión de batch para BatchNorm
        is_single_example = len(x.size()) == 1
        if is_single_example:
            x = x.unsqueeze(0)  # Añade dimensión de batch
        
        # Procesar todas las capas excepto la última
        for i in range(0, len(self.layers) - 1, 4):
            linear = self.layers[i]
            batch_norm = self.layers[i+1]
            relu = self.layers[i+2]
            dropout = self.layers[i+3]
            
            x = linear(x)
            
            # BatchNorm solo si hay batch (>1 ejemplo) o si es un solo ejemplo pero en modo evaluación
            if batch_size > 1 or (is_single_example and not self.training):
                x = batch_norm(x)
            
            x = relu(x)
            
            # Dropout solo en modo entrenamiento
            if self.training:
                x = dropout(x)
            
        # Capa final (sin BatchNorm, ReLU ni Dropout)
        x = self.layers[-1](x)
        
        # Si era un solo ejemplo, eliminar la dimensión de batch añadida
        if is_single_example:
            x = x.squeeze(0)
            
        return x

class EnhancedFeatureExtractor(nn.Module):
    """Extractor de características mejorado con dropout y normalización por lotes"""
    
    def __init__(self, input_dim: int, hidden_dim: int, depth: int = 3, dropout_rate: float = 0.1):
        super(EnhancedFeatureExtractor, self).__init__()
        
        # Estructura modular: creamos una lista de capas
        layers = []
        
        # Primera capa: entrada -> hidden_dim
        layers.append(nn.Linear(input_dim, hidden_dim))
        layers.append(nn.BatchNorm1d(hidden_dim))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(dropout_rate))
        
        # Capas intermedias con dimensión fija
        current_dim = hidden_dim
        for i in range(depth - 1):
            layers.append(nn.Linear(current_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
        
        # Registrar las capas como ModuleList para que PyTorch las reconozca
        self.layers = nn.ModuleList(layers)
        self.output_dim = hidden_dim  # Guardar dimensión de salida
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Verificar si es un tensor 1D y convertirlo a 2D para BatchNorm
        is_single_example = x.dim() == 1
        if is_single_example:
            x = x.unsqueeze(0)  # Añade dimensión de batch [1, features]
        
        # Si estamos en modo entrenamiento y solo hay un ejemplo,
        # desactivar batch norm temporalmente
        small_batch = x.size(0) < 2
        running_mode = self.training
        if small_batch and self.training:
            # Cambiar temporalmente a modo evaluación para BatchNorm
            for module in self.modules():
                if isinstance(module, nn.BatchNorm1d):
                    module.eval()
        
        # Procesar todas las capas excepto la última
        for i in range(0, len(self.layers) - 1, 4):
            linear = self.layers[i]
            batch_norm = self.layers[i+1]
            relu = self.layers[i+2]
            dropout = self.layers[i+3]
            
            x = linear(x)
            x = batch_norm(x)  # Ahora seguro porque en modo eval no requiere estadísticas de batch
            x = relu(x)
            
            # Dropout solo en modo entrenamiento original
            if running_mode:
                x = dropout(x)
        
        # Capa final (sin BatchNorm, ReLU ni Dropout)
        x = self.layers[-1](x)
        
        # Restaurar modo original si lo cambiamos
        if small_batch and running_mode:
            for module in self.modules():
                if isinstance(module, nn.BatchNorm1d):
                    module.train()
            
        # Si originalmente era un solo ejemplo, volver al formato original
        if is_single_example:
            x = x.squeeze(0)
            
        return x

class AdvancedPolicyNetwork(nn.Module):
    """Red de política avanzada para problemas grandes"""
    
    def __init__(self, input_dim: int, hidden_dim: int, depth: int = 3, dropout_rate: float = 0.1):
        super(AdvancedPolicyNetwork, self).__init__()
        self.feature_extractor = EnhancedFeatureExtractor(
            input_dim, hidden_dim, depth, dropout_rate
        )
        self.output = nn.Linear(hidden_dim, 1)
        
    def forward(self, x: torch.Tensor) -> Optional[torch.Tensor]:
        if x.size(0) == 0:
            return None
            
        # Para el caso de batch size 1 en modo entrenamiento
        small_batch = x.size(0) < 2
        if small_batch and self.training:
            # Cambiar temporalmente las BatchNorm a modo evaluación
            original_modes = {}
            for name, module in self.feature_extractor.named_modules():
                if isinstance(module, nn.BatchNorm1d):
                    original_modes[name] = module.training
                    module.eval()
        else:
            original_modes = None
            
        features = self.feature_extractor(x)
        logits = self.output(features).squeeze(-1)
        result = F.softmax(logits, dim=0)
        
        # Restaurar modos originales
        if original_modes:
            for name, module in self.feature_extractor.named_modules():
                if name in original_modes:
                    module.training = original_modes[name]
        
        return result

class AdvancedValueNetwork(nn.Module):
    """Red de valor avanzada para problemas grandes"""
    
    def __init__(self, state_dim: int, hidden_dim: int, depth: int = 4, dropout_rate: float = 0.1):
        super(AdvancedValueNetwork, self).__init__()
        
        # Estructura modular: creamos una lista de capas
        layers = []
        
        # Primera capa: estado -> hidden_dim
        layers.append(nn.Linear(state_dim, hidden_dim))
        layers.append(nn.BatchNorm1d(hidden_dim))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(dropout_rate))
        
        # Factor de expansión para problemas grandes
        expansion_factor = 1.5 if hidden_dim >= 512 else 1.2
        
        # Capas intermedias con arquitectura de hora de reloj (aumentar y luego reducir)
        current_dim = hidden_dim
        for i in range(depth - 2):
            # Primero expandimos la red
            if i < (depth - 2) // 2:
                next_dim = int(current_dim * expansion_factor)
            # Luego la contraemos de vuelta
            else:
                next_dim = int(current_dim / expansion_factor)
                next_dim = max(next_dim, hidden_dim // 2)  # No reducir demasiado
                
            layers.append(nn.Linear(current_dim, next_dim))
            layers.append(nn.BatchNorm1d(next_dim))
            
            # Usar activación más avanzada para problemas grandes
            if hidden_dim >= 512:
                layers.append(nn.LeakyReLU(0.1))
            else:
                layers.append(nn.ReLU())
                
            layers.append(nn.Dropout(dropout_rate))
            current_dim = next_dim
        
        # Para problemas muy grandes, añadir una capa final de reducción antes de la salida
        if hidden_dim >= 512:
            layers.append(nn.Linear(current_dim, hidden_dim // 2))
            layers.append(nn.BatchNorm1d(hidden_dim // 2))
            layers.append(nn.LeakyReLU(0.1))
            layers.append(nn.Dropout(dropout_rate))
            current_dim = hidden_dim // 2
        
        # Capa final para salida escalar
        layers.append(nn.Linear(current_dim, 1))
        
        self.layers = nn.ModuleList(layers)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.size(0) if len(x.size()) > 0 else 0
        
        # Si el input es 1D (un solo ejemplo), añadir dimensión de batch para BatchNorm
        is_single_example = len(x.size()) == 1
        if is_single_example:
            x = x.unsqueeze(0)  # Añade dimensión de batch
        
        # Procesar todas las capas excepto la última
        for i in range(0, len(self.layers) - 1, 4):
            linear = self.layers[i]
            batch_norm = self.layers[i+1]
            relu = self.layers[i+2]
            dropout = self.layers[i+3]
            
            x = linear(x)
            
            # BatchNorm solo si hay batch (>1 ejemplo) o si es un solo ejemplo pero en modo evaluación
            if batch_size > 1 or (is_single_example and not self.training):
                x = batch_norm(x)
            
            x = relu(x)
            
            # Dropout solo en modo entrenamiento
            if self.training:
                x = dropout(x)
            
        # Capa final (sin BatchNorm, ReLU ni Dropout)
        x = self.layers[-1](x)
        
        # Si era un solo ejemplo, eliminar la dimensión de batch añadida
        if is_single_example:
            x = x.squeeze(0)
            
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
    elif problem_size <= 1000:  # hasta 50x20
        return 384
    elif problem_size <= 2000:  # hasta 100x20
        return 512
    else:  # Para problemas extremadamente grandes
        return 768
