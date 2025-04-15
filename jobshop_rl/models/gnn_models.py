"""
Módulo que implementa arquitecturas de Graph Neural Networks (GNN) y
mecanismos de atención para problemas de Job Shop Scheduling.

Este módulo proporciona implementaciones modulares de diferentes arquitecturas
que pueden ser utilizadas como base para la red de política y valor en
algoritmos de aprendizaje por refuerzo.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class GNNLayer(nn.Module):
    """
    Capa básica de Graph Neural Network.
    
    Implementa el paso de mensajes y actualización de estados para
    nodos en un grafo, permitiendo que la información fluya a través
    de las conexiones.
    """
    def __init__(self, hidden_dim, aggregation='mean'):
        """
        Inicializa la capa GNN.
        
        Args:
            hidden_dim: Dimensionalidad de los vectores de características
            aggregation: Método de agregación de mensajes ('mean', 'sum', 'max')
        """
        super(GNNLayer, self).__init__()
        self.aggregation = aggregation
        
        # MLP para generar mensajes
        self.message_mlp = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),  # Origen + Destino + Arista
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # GRU para actualizar estados de nodos
        self.update_gru = nn.GRUCell(hidden_dim, hidden_dim)
        
    def forward(self, x, edge_index, edge_features):
        """
        Propaga la información a través del grafo.
        
        Args:
            x: Tensor de características de nodos [num_nodes, hidden_dim]
            edge_index: Índices de aristas [2, num_edges] donde
                        edge_index[0] son nodos origen y
                        edge_index[1] son nodos destino
            edge_features: Características de aristas [num_edges, hidden_dim]
            
        Returns:
            Tensor de características de nodos actualizadas
        """
        # Colectar mensajes
        src, dst = edge_index
        num_nodes = x.size(0)
        
        # Generar mensajes para cada arista
        edge_src = x[src]
        edge_dst = x[dst]
        # Concatenar características de origen, destino y arista
        message_inputs = torch.cat([edge_src, edge_dst, edge_features], dim=1)
        messages = self.message_mlp(message_inputs)
        
        # Agregar mensajes para cada nodo destino
        aggregated_messages = torch.zeros(num_nodes, x.size(1), device=x.device)
        
        # Para cada nodo destino, agregamos sus mensajes entrantes
        for i in range(num_nodes):
            # Encontrar aristas donde el nodo i es el destino
            mask = (dst == i)
            if not mask.any():
                continue
                
            # Obtener mensajes para este nodo
            node_messages = messages[mask]
            
            # Agregar mensajes según el método especificado
            if self.aggregation == 'mean' and node_messages.size(0) > 0:
                aggregated_messages[i] = node_messages.mean(dim=0)
            elif self.aggregation == 'sum':
                aggregated_messages[i] = node_messages.sum(dim=0)
            elif self.aggregation == 'max' and node_messages.size(0) > 0:
                aggregated_messages[i] = node_messages.max(dim=0)[0]
        
        # Actualizar estados de nodos con GRU
        new_x = self.update_gru(aggregated_messages, x)
        
        return new_x


class MultiHeadAttention(nn.Module):
    """
    Implementación personalizada de atención multi-cabeza.
    
    Permite a un nodo atender selectivamente a otros nodos basándose
    en la relevancia para la tarea actual.
    """
    def __init__(self, hidden_dim, num_heads, dropout=0.1):
        """
        Inicializa el módulo de atención.
        
        Args:
            hidden_dim: Dimensionalidad de los vectores de características
            num_heads: Número de cabezas de atención
            dropout: Tasa de dropout
        """
        super(MultiHeadAttention, self).__init__()
        assert hidden_dim % num_heads == 0, "hidden_dim debe ser divisible por num_heads"
        
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads
        
        # Proyecciones lineales para Query, Key, Value
        self.q_linear = nn.Linear(hidden_dim, hidden_dim)
        self.k_linear = nn.Linear(hidden_dim, hidden_dim)
        self.v_linear = nn.Linear(hidden_dim, hidden_dim)
        
        # Proyección final
        self.out_linear = nn.Linear(hidden_dim, hidden_dim)
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, query, key, value, mask=None):
        """
        Calcula la atención multi-cabeza.
        
        Args:
            query: Tensor de consulta [batch_size, seq_len_q, hidden_dim]
            key: Tensor de claves [batch_size, seq_len_k, hidden_dim]
            value: Tensor de valores [batch_size, seq_len_k, hidden_dim]
            mask: Máscara opcional para filtrar ciertas posiciones
            
        Returns:
            Tensor de salida y pesos de atención
        """
        batch_size = query.size(0)
        
        # Proyecciones lineales y reorganización para multi-cabeza
        q = self.q_linear(query).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_linear(key).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_linear(value).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Calcular puntuaciones de atención: (batch, heads, q_len, k_len)
        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        
        # Aplicar máscara si se proporciona
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # Normalización softmax
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        # Aplicar atención a los valores
        context = torch.matmul(attn_weights, v)
        
        # Reorganizar y proyectar a la salida
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, self.hidden_dim)
        output = self.out_linear(context)
        
        return output, attn_weights


class GraphAttentionLayer(nn.Module):
    """
    Capa de atención basada en grafos, combinando conceptos de GAT (Graph Attention Networks).
    
    Permite que cada nodo atienda dinámicamente a sus vecinos, ponderando
    su importancia basándose en el contenido.
    """
    def __init__(self, hidden_dim, num_heads=1, dropout=0.1, residual=True):
        """
        Inicializa la capa de atención basada en grafos.
        
        Args:
            hidden_dim: Dimensionalidad de las características
            num_heads: Número de cabezas de atención
            dropout: Tasa de dropout
            residual: Si se debe usar conexión residual
        """
        super(GraphAttentionLayer, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        self.residual = residual
        
        # Proyección para características de nodos
        self.node_proj = nn.Linear(hidden_dim, hidden_dim)
        
        # Atención para cada cabeza
        self.attention_heads = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_dim * 2, 1),  # Atención basada en pares de nodos
                nn.LeakyReLU(0.2)
            ) for _ in range(num_heads)
        ])
        
        # Transformación de valores para cada cabeza
        self.value_projections = nn.ModuleList([
            nn.Linear(hidden_dim, hidden_dim // num_heads)
            for _ in range(num_heads)
        ])
        
        # Proyección final
        self.output_proj = nn.Linear(hidden_dim, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        
        # Normalización para conexión residual
        self.norm = nn.LayerNorm(hidden_dim)
        
    def forward(self, x, edge_index, return_attention=False):
        """
        Propaga información usando atención basada en grafos.
        
        Args:
            x: Características de nodos [num_nodes, hidden_dim]
            edge_index: Índices de aristas [2, num_edges]
            return_attention: Si se deben devolver pesos de atención
            
        Returns:
            Características de nodos actualizadas y opcionalmente pesos de atención
        """
        num_nodes = x.size(0)
        src, dst = edge_index
        
        # Aplicar proyección a nodos
        h = self.node_proj(x)
        
        # Calcular atención multi-cabeza
        head_outputs = []
        attention_weights = []
        
        for head_idx in range(self.num_heads):
            # Para cada nodo, reunir características de vecinos
            h_src = h[src]
            h_dst = h[dst]
            
            # Calcular puntuaciones de atención para cada arista
            edge_features = torch.cat([h_src, h_dst], dim=1)
            edge_attention = self.attention_heads[head_idx](edge_features)
            
            # Normalizar con softmax por nodo destino
            attention_dst = torch.zeros(num_nodes, src.size(0), device=x.device)
            attention_dst.scatter_add_(0, dst.unsqueeze(0).expand(1, -1), 
                                      edge_attention.t())
            attention_dst = F.softmax(attention_dst, dim=1)
            
            # Aplicar atención a valores
            values = self.value_projections[head_idx](h)
            output = torch.zeros(num_nodes, values.size(1), device=x.device)
            
            # Agregar valores ponderados por atención
            for i in range(num_nodes):
                # Encontrar aristas donde este nodo es destino
                mask = (dst == i)
                if not mask.any():
                    continue
                
                # Obtener nodos origen y aplicar atención
                sources = src[mask]
                attn_weights = attention_dst[i, mask]
                node_values = values[sources]
                
                # Agregar ponderado por atención
                output[i] = (attn_weights.unsqueeze(1) * node_values).sum(dim=0)
            
            head_outputs.append(output)
            attention_weights.append(attention_dst)
        
        # Concatenar salidas de todas las cabezas
        multi_head_output = torch.cat(head_outputs, dim=1)
        
        # Proyección final
        output = self.output_proj(multi_head_output)
        output = self.dropout(output)
        
        # Conexión residual
        if self.residual:
            output = self.norm(output + x)
        
        if return_attention:
            return output, attention_weights
        return output


class BaseModel(nn.Module):
    """
    Clase base para modelos de Job Shop Scheduling.
    
    Define la interfaz común y funcionalidad compartida para
    los diferentes tipos de arquitecturas implementadas.
    """
    def __init__(self):
        super(BaseModel, self).__init__()
    
    def get_action_distribution(self, action_scores, mask=None):
        """
        Convierte puntuaciones brutas a distribución de probabilidad.
        
        Args:
            action_scores: Puntuaciones para cada acción posible
            mask: Máscara de acciones válidas (1 para válidas, 0 para inválidas)
            
        Returns:
            Distribución de probabilidad sobre acciones
        """
        if mask is not None:
            # Asignar -inf a acciones inválidas
            action_scores = action_scores.masked_fill(mask == 0, -1e9)
        
        # Convertir a probabilidades con softmax
        return F.softmax(action_scores, dim=-1)
    
    def forward(self, *args, **kwargs):
        """
        Método a implementar por las subclases.
        """
        raise NotImplementedError("Las subclases deben implementar forward()")


class GNNModel(BaseModel):
    """
    Modelo basado en Graph Neural Networks para Job Shop Scheduling.
    
    Utiliza GNN para capturar las relaciones estructurales entre
    trabajos y máquinas a través del grafo de restricciones.
    """
    def __init__(self, node_feature_dim, edge_feature_dim, hidden_dim, 
                 num_gnn_layers=3, aggregation='mean'):
        """
        Inicializa el modelo GNN.
        
        Args:
            node_feature_dim: Dimensión de las características de los nodos
            edge_feature_dim: Dimensión de las características de las aristas
            hidden_dim: Dimensión de las capas ocultas
            num_gnn_layers: Número de capas GNN
            aggregation: Método de agregación de mensajes ('mean', 'sum', 'max')
        """
        super(GNNModel, self).__init__()
        
        # Codificación de características
        self.node_encoder = nn.Sequential(
            nn.Linear(node_feature_dim, hidden_dim),
            nn.ReLU()
        )
        
        self.edge_encoder = nn.Sequential(
            nn.Linear(edge_feature_dim, hidden_dim),
            nn.ReLU()
        )
        
        # Capas GNN
        self.gnn_layers = nn.ModuleList([
            GNNLayer(hidden_dim, aggregation=aggregation) 
            for _ in range(num_gnn_layers)
        ])
        
        # Cabeza de política: genera puntuaciones para cada nodo
        self.policy_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)  # Un valor por nodo
        )
        
        # Cabeza de valor: estima el valor del estado completo
        self.value_head = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),  # Concat de mean y max pooling
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, node_features, edge_index, edge_features, mask=None):
        """
        Procesa el grafo para obtener puntuaciones de acción y estimación de valor.
        
        Args:
            node_features: Características de nodos [num_nodes, feature_dim]
            edge_index: Índices de aristas [2, num_edges]
            edge_features: Características de aristas [num_edges, edge_feature_dim]
            mask: Máscara de acciones válidas [num_nodes]
            
        Returns:
            action_scores: Puntuaciones para cada nodo/acción
            state_value: Valor estimado del estado actual
        """
        # Codificar características
        x = self.node_encoder(node_features)
        edge_attr = self.edge_encoder(edge_features)
        
        # Aplicar capas GNN
        for gnn_layer in self.gnn_layers:
            x = gnn_layer(x, edge_index, edge_attr)
        
        # Generar puntuaciones de acción
        action_scores = self.policy_head(x).squeeze(-1)
        
        # Generar representación global del estado
        global_avg = torch.mean(x, dim=0)
        global_max, _ = torch.max(x, dim=0)
        global_features = torch.cat([global_avg, global_max])
        
        # Estimar valor del estado
        state_value = self.value_head(global_features)
        
        return action_scores, state_value


class TransformerModel(BaseModel):
    """
    Modelo basado en Transformer para Job Shop Scheduling.
    
    Utiliza mecanismos de atención para capturar relaciones
    entre operaciones independientemente de su posición.
    """
    def __init__(self, feature_dim, hidden_dim, num_heads=4, num_layers=2, dropout=0.1):
        """
        Inicializa el modelo Transformer.
        
        Args:
            feature_dim: Dimensión de las características de entrada
            hidden_dim: Dimensión de las capas ocultas
            num_heads: Número de cabezas de atención
            num_layers: Número de capas de Transformer
            dropout: Tasa de dropout
        """
        super(TransformerModel, self).__init__()
        
        # Codificación de características
        self.feature_encoder = nn.Linear(feature_dim, hidden_dim)
        
        # Codificación posicional
        self.max_seq_len = 1000  # Máximo número de operaciones
        self.pos_encoder = nn.Embedding(self.max_seq_len, hidden_dim)
        
        # Capas de Transformer
        encoder_layers = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=4*hidden_dim,
            dropout=dropout,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layers, 
            num_layers=num_layers
        )
        
        # Cabeza de política: genera puntuaciones para cada operación
        self.policy_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)  # Un valor por operación
        )
        
        # Cabeza de valor: estima el valor del estado completo
        self.value_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, operation_features, mask=None):
        """
        Procesa la secuencia de operaciones para obtener puntuaciones y valor.
        
        Args:
            operation_features: Características de las operaciones [batch_size, seq_len, feature_dim]
                               O [seq_len, feature_dim] para tamaño de batch 1
            mask: Máscara de operaciones válidas [batch_size, seq_len] o [seq_len]
            
        Returns:
            action_scores: Puntuaciones para cada operación
            state_value: Valor estimado del estado actual
        """
        # Asegurar formato correcto de batch
        if operation_features.dim() == 2:
            operation_features = operation_features.unsqueeze(0)
            if mask is not None and mask.dim() == 1:
                mask = mask.unsqueeze(0)
        
        batch_size, seq_len, _ = operation_features.shape
        
        # Codificar características
        x = self.feature_encoder(operation_features)
        
        # Añadir codificación posicional
        positions = torch.arange(seq_len, device=operation_features.device)
        positions = positions.unsqueeze(0).expand(batch_size, -1)
        x = x + self.pos_encoder(positions)
        
        # Preparar máscara de atención
        if mask is not None:
            # Adaptar máscara para el formato que espera el transformer
            # Donde True significa que la posición está enmascarada (ignorada)
            attention_mask = ~mask.bool()
        else:
            attention_mask = None
        
        # Aplicar Transformer
        x = self.dropout(x)
        x = self.transformer_encoder(x, src_key_padding_mask=attention_mask)
        
        # Generar puntuaciones de acción
        action_scores = self.policy_head(x).squeeze(-1)
        
        # Estimar valor del estado usando la representación global
        global_repr = x.mean(dim=1)  # Promedio sobre la secuencia
        state_value = self.value_head(global_repr)
        
        # Para batch_size=1, eliminar esa dimensión
        if batch_size == 1:
            action_scores = action_scores.squeeze(0)
            state_value = state_value.squeeze(0)
        
        return action_scores, state_value


class HybridGNNAttentionModel(BaseModel):
    """
    Modelo híbrido que combina GNN y mecanismos de atención.
    
    Utiliza GNN para capturar la estructura del grafo y luego
    mecanismos de atención para resaltar las partes más relevantes.
    """
    def __init__(self, node_feature_dim, edge_feature_dim, hidden_dim, 
                 num_gnn_layers=2, num_heads=4, num_attn_layers=1, dropout=0.1):
        """
        Inicializa el modelo híbrido.
        
        Args:
            node_feature_dim: Dimensión de las características de los nodos
            edge_feature_dim: Dimensión de las características de las aristas
            hidden_dim: Dimensión de las capas ocultas
            num_gnn_layers: Número de capas GNN
            num_heads: Número de cabezas de atención
            num_attn_layers: Número de capas de atención por grafos
            dropout: Tasa de dropout
        """
        super(HybridGNNAttentionModel, self).__init__()
        
        # Codificación de características
        self.node_encoder = nn.Sequential(
            nn.Linear(node_feature_dim, hidden_dim),
            nn.ReLU()
        )
        
        self.edge_encoder = nn.Sequential(
            nn.Linear(edge_feature_dim, hidden_dim),
            nn.ReLU()
        )
        
        # Capas GNN para procesamiento inicial
        self.gnn_layers = nn.ModuleList([
            GNNLayer(hidden_dim) for _ in range(num_gnn_layers)
        ])
        
        # Capas de atención basada en grafos
        self.attn_layers = nn.ModuleList([
            GraphAttentionLayer(hidden_dim, num_heads, dropout)
            for _ in range(num_attn_layers)
        ])
        
        # Cabeza de política: genera puntuaciones para cada nodo
        self.policy_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)  # Un valor por nodo
        )
        
        # Cabeza de valor: estima el valor del estado completo
        self.value_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, node_features, edge_index, edge_features, mask=None, return_attention=False):
        """
        Procesa el grafo utilizando GNN y atención.
        
        Args:
            node_features: Características de nodos [num_nodes, feature_dim]
            edge_index: Índices de aristas [2, num_edges]
            edge_features: Características de aristas [num_edges, edge_feature_dim]
            mask: Máscara de acciones válidas [num_nodes]
            return_attention: Si se deben devolver pesos de atención
            
        Returns:
            action_scores: Puntuaciones para cada nodo/acción
            state_value: Valor estimado del estado actual
            attention_weights: (opcional) Pesos de atención
        """
        # Codificar características
        x = self.node_encoder(node_features)
        edge_attr = self.edge_encoder(edge_features)
        
        # Aplicar capas GNN
        for gnn_layer in self.gnn_layers:
            x = gnn_layer(x, edge_index, edge_attr)
        
        # Guardar pesos de atención si se solicitan
        attention_weights = []
        
        # Aplicar capas de atención
        for attn_layer in self.attn_layers:
            if return_attention:
                x, attn = attn_layer(x, edge_index, return_attention=True)
                attention_weights.append(attn)
            else:
                x = attn_layer(x, edge_index)
        
        # Aplicar dropout
        x = self.dropout(x)
        
        # Generar puntuaciones de acción
        action_scores = self.policy_head(x).squeeze(-1)
        
        # Generar representación global para el valor
        # Usando media ponderada por atención de la última capa, si está disponible
        if attention_weights and return_attention:
            last_attn = attention_weights[-1]
            # Convertir atención multi-cabeza a un solo valor por nodo
            attn_avg = torch.cat([a.mean(dim=1) for a in last_attn], dim=0)
            attn_avg = F.softmax(attn_avg.mean(dim=0), dim=0)
            global_repr = (x * attn_avg.unsqueeze(1)).sum(dim=0)
        else:
            global_repr = x.mean(dim=0)
        
        # Estimar valor del estado
        state_value = self.value_head(global_repr)
        
        if return_attention:
            return action_scores, state_value, attention_weights
        
        return action_scores, state_value
