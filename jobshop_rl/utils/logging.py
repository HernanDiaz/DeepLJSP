"""
Utilidades para el registro de datos de entrenamiento y experimentos.
"""

import os
import csv
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JobShopRL")

class TrainingLogger:
    """Clase para el registro de datos de entrenamiento en CSV"""
    
    def __init__(self, filename: str = None, include_timestamp: bool = True, base_dir: str = 'outputs'):
        """
        Inicializa el logger para CSV.
        
        Args:
            filename: Nombre del archivo CSV de salida. Si es None, se genera uno automáticamente.
            include_timestamp: Si se debe incluir una marca de tiempo en el nombre del archivo.
            base_dir: Directorio base donde se guardará el archivo (por defecto 'outputs').
        """
        # Asegurar que existe el directorio base
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)
            
        # Crear directorio de logs dentro del directorio base
        logs_dir = os.path.join(base_dir, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Verificar que el directorio se creó correctamente
        if not os.path.exists(logs_dir):
            # Si no se pudo crear, usar el directorio base
            logs_dir = base_dir
            logger.warning(f"No se pudo crear el directorio logs. Usando {base_dir} como alternativa.")
        
        # Generar nombre de archivo si no se proporcionó
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if include_timestamp else ""
            self.filename = os.path.join(logs_dir, f"training_log_{timestamp}.csv")
        else:
            # Si el nombre ya incluye una ruta completa, respetarla
            if os.path.isabs(filename) or '/' in filename:
                self.filename = filename
                # Asegurarse que el directorio existe
                os.makedirs(os.path.dirname(os.path.abspath(self.filename)), exist_ok=True)
            else:
                # De lo contrario, añadir la ruta de logs
                self.filename = os.path.join(logs_dir, filename)
                
            # Añadir extensión CSV si no la tiene
            if not self.filename.endswith('.csv'):
                self.filename = f"{self.filename}.csv"
        
        self.data = []
        # Header expandido para soportar intervalos
        self.header = [
            'episode', 
            'current_makespan_lower', 'current_makespan_upper',
            'best_makespan_lower', 'best_makespan_upper',
            'avg_makespan_lower', 'avg_makespan_upper',
            'training_time'
        ]
        
        logger.info(f"TrainingLogger inicializado. Datos se guardarán en: {self.filename}")
        
        # Crear directorio padre si no existe (por si el filename tiene subdirectorios)
        parent_dir = os.path.dirname(os.path.abspath(self.filename))
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
            
        # Intentar escribir el encabezado del CSV
        try:
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)
            logger.info(f"Archivo CSV creado correctamente en: {self.filename}")
        except Exception as e:
            logger.error(f"Error al crear archivo CSV: {e}")
            # Si no se pudo crear el archivo, intentar en el directorio de trabajo actual
            self.filename = f"training_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            logger.info(f"Intentando crear archivo en ubicación alternativa: {self.filename}")
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)
    
    def log_step(self, episode: int, 
                 current_makespan: float = None,  # Mantener para compatibilidad
                 best_makespan: float = None,     # Mantener para compatibilidad
                 avg_makespan: float = None,      # Mantener para compatibilidad
                 current_makespan_lower: float = None,
                 current_makespan_upper: float = None,
                 best_makespan_lower: float = None,
                 best_makespan_upper: float = None,
                 avg_makespan_lower: float = None,
                 avg_makespan_upper: float = None,
                 training_time: float = 0.0):
        """
        Registra los datos de un paso de entrenamiento.
        Soporta tanto valores escalares (para compatibilidad) como intervalos.
        
        Args:
            episode: Número de episodio
            current_makespan: Makespan del episodio actual (escalar, para compatibilidad)
            best_makespan: Mejor makespan encontrado (escalar, para compatibilidad)
            avg_makespan: Makespan promedio (escalar, para compatibilidad)
            current_makespan_lower: Límite inferior del makespan actual
            current_makespan_upper: Límite superior del makespan actual
            best_makespan_lower: Límite inferior del mejor makespan
            best_makespan_upper: Límite superior del mejor makespan
            avg_makespan_lower: Límite inferior del makespan promedio
            avg_makespan_upper: Límite superior del makespan promedio
            training_time: Tiempo de entrenamiento transcurrido en segundos
        """
        # Compatibilidad hacia atrás: si se pasan valores escalares, usarlos para ambos límites
        if current_makespan_lower is None and current_makespan is not None:
            current_makespan_lower = current_makespan
            current_makespan_upper = current_makespan
        if best_makespan_lower is None and best_makespan is not None:
            best_makespan_lower = best_makespan
            best_makespan_upper = best_makespan
        if avg_makespan_lower is None and avg_makespan is not None:
            avg_makespan_lower = avg_makespan
            avg_makespan_upper = avg_makespan
        
        # Valores por defecto si no se proporciona nada
        current_makespan_lower = current_makespan_lower or 0.0
        current_makespan_upper = current_makespan_upper or 0.0
        best_makespan_lower = best_makespan_lower or 0.0
        best_makespan_upper = best_makespan_upper or 0.0
        avg_makespan_lower = avg_makespan_lower or 0.0
        avg_makespan_upper = avg_makespan_upper or 0.0
        
        row = [
            episode, 
            current_makespan_lower, current_makespan_upper,
            best_makespan_lower, best_makespan_upper,
            avg_makespan_lower, avg_makespan_upper,
            training_time
        ]
        self.data.append(row)
        
        # Cada 10 registros o múltiplo de 10, guardar a disco
        if len(self.data) % 10 == 0:
            self._write_to_disk()
    
    def _write_to_disk(self):
        """Escribe los datos acumulados en el archivo CSV"""
        try:
            with open(self.filename, 'a', newline='') as f:
                writer = csv.writer(f)
                for row in self.data:
                    writer.writerow(row)
                    
            # Vaciar buffer después de escribir
            self.data = []
            
        except Exception as e:
            logger.error(f"Error al escribir en el archivo CSV: {e}")
            # No vaciamos el buffer para intentar escribirlo en la próxima ocasión
    
    def save(self):
        """Guarda cualquier dato pendiente y finaliza el logger"""
        if self.data:
            self._write_to_disk()
            
        # Comprobar si el archivo existe y tiene datos
        try:
            if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
                logger.info(f"Datos de entrenamiento guardados en {self.filename}")
            else:
                logger.warning(f"El archivo {self.filename} no existe o está vacío.")
        except:
            # Si no podemos verificar el archivo o no estamos en un entorno interactivo
            logger.info(f"Operación de guardado completada para {self.filename}")
