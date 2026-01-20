"""
Paquete de datos para problemas de Job Shop Scheduling.
"""

# Problemas estándar
from jobshop_rl.data.ft10 import get_ft10_problem
from jobshop_rl.data.ft10_interval import get_ft10_interval_problem
from jobshop_rl.data.ft20 import get_ft20_problem

# Problemas ABZ
from jobshop_rl.data.abz7 import get_abz7_problem
from jobshop_rl.data.abz8 import get_abz8_problem
from jobshop_rl.data.abz9 import get_abz9_problem
from jobshop_rl.data.abz10 import get_abz10_problem

# Problemas Taillard con tamaño 20x20
from jobshop_rl.data.tai20_20_01 import get_tai20_20_01_problem
from jobshop_rl.data.tai20_20_02 import get_tai20_20_02_problem

# Problemas Taillard con tamaño 50x15
from jobshop_rl.data.tai50_15_01 import get_tai50_15_01_problem
from jobshop_rl.data.tai50_15_02 import get_tai50_15_02_problem

# Problemas Taillard con tamaño 100x20
from jobshop_rl.data.tai100_20_01 import get_tai100_20_01_problem
from jobshop_rl.data.tai100_20_02 import get_tai100_20_02_problem

# Importar el cargador de problemas
from jobshop_rl.data.problem_loader import ProblemLoader

# Diccionario para registrar todos los problemas
PROBLEM_REGISTRY = {
    'ft10': get_ft10_problem,
    'ft10_interval': get_ft10_interval_problem,
    'ft20': get_ft20_problem,
    'abz7': get_abz7_problem,
    'abz8': get_abz8_problem,
    'abz9': get_abz9_problem,
    'abz10': get_abz10_problem,
    'tai20_20_01': get_tai20_20_01_problem,
    'tai20_20_02': get_tai20_20_02_problem,
    'tai50_15_01': get_tai50_15_01_problem,
    'tai50_15_02': get_tai50_15_02_problem,
    'tai100_20_01': get_tai100_20_01_problem,
    'tai100_20_02': get_tai100_20_02_problem,
}

# Función para cargar problemas con F.15_01 manualmente (sin importación)
def register_special_problem(filename):
    """
    Registra manualmente un problema que tiene un nombre de archivo con punto.
    
    Args:
        filename: Nombre del archivo .py
    """
    import os
    import re
    
    # Crear ID del problema sin la extensión F.15_01
    base_name = filename.replace('.py', '')
    problem_id = base_name.split('.')[0]
    
    # Generar un nombre de función basado en el nombre del archivo
    func_name = f"get_{base_name.replace('.', '_').lower()}_problem"
    
    # Ruta completa al archivo
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        print(f"Archivo no encontrado: {file_path}")
        return
    
    try:
        # Leer el contenido del archivo
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        # Buscar la estructura de diccionario DATA y el nombre de la variable
        data_var_pattern = r'(\w+)\s*=\s*{[^}]*\'num_jobs\'[^}]*\'num_machines\'[^}]*\'sequences\'[^}]*\'durations\'[^}]*}'
        data_var_match = re.search(data_var_pattern, file_content, re.DOTALL)
        
        if data_var_match:
            data_var_name = data_var_match.group(1)
            
            # Crear una función getter para este problema
            def problem_getter():
                # Cargar el módulo en tiempo de ejecución
                import importlib.util
                spec = importlib.util.spec_from_file_location(problem_id, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Devolver los datos del problema
                return getattr(module, data_var_name)
            
            # Registrar la función getter
            PROBLEM_REGISTRY[problem_id] = problem_getter
            
            # Agregar la función al espacio global
            globals()[func_name] = problem_getter
            
            return func_name
        else:
            print(f"No se pudo encontrar la estructura de datos del problema en {filename}")
            
    except Exception as e:
        print(f"Error al procesar {filename}: {str(e)}")

# Cargar problemas especiales (.F.15_01)
import os
data_dir = os.path.dirname(__file__)

# Registrar archivos con .F.15_01
for filename in os.listdir(data_dir):
    if filename.endswith('.py') and '.F.15_01' in filename:
        register_special_problem(filename)

# AUTO-REGISTRO: Cargar todos los archivos *_interval.py automáticamente
print("Registrando problemas con intervalos...")
for filename in os.listdir(data_dir):
    if filename.endswith('_interval.py') and not filename.startswith('__'):
        try:
            # Extraer el nombre del módulo (sin .py)
            module_name = filename[:-3]
            
            # Crear el ID del problema (sin el sufijo _interval)
            problem_id = module_name.replace('_interval', '')
            
            # Si ya está registrado, usar el nombre con _interval
            if problem_id in PROBLEM_REGISTRY:
                problem_id = module_name  # Usar nombre completo con _interval
            
            # Nombre de la función getter
            func_name = f"get_{module_name}_problem"
            
            # Importar dinámicamente el módulo
            import importlib
            module = importlib.import_module(f'jobshop_rl.data.{module_name}')
            
            # Obtener la función getter
            if hasattr(module, func_name):
                getter_func = getattr(module, func_name)
                PROBLEM_REGISTRY[problem_id] = getter_func
                print(f"  ✓ Registrado: {problem_id}")
            else:
                print(f"  ⚠️  No se encontró {func_name} en {filename}")
                
        except Exception as e:
            print(f"  ❌ Error registrando {filename}: {str(e)}")

print(f"Total de problemas registrados: {len(PROBLEM_REGISTRY)}")

# Lista de exportación
__all__ = ['ProblemLoader', 'PROBLEM_REGISTRY'] + list(filter(lambda x: x.startswith('get_') and x.endswith('_problem'), globals().keys()))
