"""
Script para convertir instancias de Taillard con formato etiquetado
a archivos Python (.py) como ft10_interval.py

Formato de entrada:
    NUMERO DE TRABAJOS
    15
    NUMERO DE RECURSOS
    15
    SECUENCIA DE MAQUINAS
    6 12 4 7 3 2 10 11 8 14 9 13 5 0 1 
    ...
    DURACIONES
    (93, 95) (66, 66) (9, 11) ...
    ...
"""

import os
import re
from pathlib import Path


def parse_labeled_taillard(filepath: str) -> dict:
    """
    Parsea un archivo Taillard con etiquetas en español.
    
    Args:
        filepath: Ruta al archivo a parsear
        
    Returns:
        Diccionario con los datos del problema
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer número de trabajos
    match = re.search(r'NUMERO DE TRABAJOS\s+(\d+)', content)
    if not match:
        raise ValueError("No se encontró 'NUMERO DE TRABAJOS'")
    num_jobs = int(match.group(1))
    
    # Extraer número de recursos/máquinas
    match = re.search(r'NUMERO DE RECURSOS\s+(\d+)', content)
    if not match:
        raise ValueError("No se encontró 'NUMERO DE RECURSOS'")
    num_machines = int(match.group(1))
    
    # Extraer secuencias de máquinas
    match = re.search(r'SECUENCIA DE MAQUINAS\s+([\s\S]+?)(?=DURACIONES|$)', content)
    if not match:
        raise ValueError("No se encontró 'SECUENCIA DE MAQUINAS'")
    
    sequences_text = match.group(1).strip()
    sequences = []
    for line in sequences_text.split('\n'):
        line = line.strip()
        if line:
            machines = [int(x) for x in line.split()]
            sequences.append(machines)
    
    if len(sequences) != num_jobs:
        raise ValueError(f"Se esperaban {num_jobs} secuencias, se encontraron {len(sequences)}")
    
    # Extraer duraciones
    match = re.search(r'DURACIONES\s+([\s\S]+?)$', content)
    if not match:
        raise ValueError("No se encontró 'DURACIONES'")
    
    durations_text = match.group(1).strip()
    durations = []
    
    # Procesar líneas de duraciones, ignorando líneas vacías y comentarios
    for line in durations_text.split('\n'):
        line = line.strip()
        
        # Ignorar líneas vacías o comentarios
        if not line or line.startswith('#'):
            continue
        
        # Si ya tenemos todas las duraciones necesarias, parar
        if len(durations) >= num_jobs:
            break
        
        # Buscar todos los patrones (min, max) en la línea
        job_durations = []
        intervals = re.findall(r'\((\d+),\s*(\d+)\)', line)
        
        # Si no hay intervalos en esta línea, podría ser contenido extra - ignorar
        if not intervals:
            continue
        
        for min_val, max_val in intervals:
            min_val = int(min_val)
            max_val = int(max_val)
            job_durations.append((min_val, max_val))
        
        # Solo agregar si tenemos el número correcto de duraciones para el job
        if len(job_durations) == num_machines:
            durations.append(job_durations)
        elif len(job_durations) > 0:
            # Si hay duraciones pero no coinciden con num_machines, podría ser un error o formato diferente
            # En ese caso, advertir pero intentar seguir
            print(f"  ⚠️  Advertencia: Línea con {len(job_durations)} duraciones (esperadas: {num_machines})")
    
    if len(durations) != num_jobs:
        raise ValueError(f"Se esperaban {num_jobs} líneas de duraciones, se encontraron {len(durations)}")
    
    return {
        'num_jobs': num_jobs,
        'num_machines': num_machines,
        'sequences': sequences,
        'durations': durations
    }


def generate_python_file(problem: dict, output_path: str, problem_name: str):
    """
    Genera un archivo Python con el formato de ft10_interval.py
    
    Args:
        problem: Diccionario con los datos del problema
        output_path: Ruta donde guardar el archivo .py
        problem_name: Nombre del problema (ej: 'la01_interval')
    """
    
    # Crear el contenido del archivo
    lines = []
    
    # Header
    lines.append('"""')
    lines.append(f'Problema {problem_name.upper()} con incertidumbre en tiempos de procesamiento.')
    lines.append('')
    lines.append('Esta versión utiliza duraciones con intervalos personalizados')
    lines.append('para demostrar el manejo de incertidumbre.')
    lines.append('')
    lines.append('Formato: Cada duración es un intervalo [lower, upper]')
    lines.append('Algunas operaciones tienen incertidumbre (lower < upper)')
    lines.append('Otras son determinísticas (lower = upper)')
    lines.append('"""')
    lines.append('')
    lines.append('from jobshop_rl.models.interval import Interval')
    lines.append('')
    lines.append('')
    
    # Data dictionary
    dict_name = problem_name.upper().replace('-', '_').replace('.', '_') + '_DATA'
    lines.append(f'{dict_name} = {{')
    lines.append(f"    'num_jobs': {problem['num_jobs']},")
    lines.append(f"    'num_machines': {problem['num_machines']},")
    lines.append(f"    'problem_id': '{problem_name}',")
    
    # Sequences
    lines.append("    'sequences': [")
    for seq in problem['sequences']:
        seq_str = ', '.join(map(str, seq))
        lines.append(f"        [{seq_str}],")
    lines.append("    ],")
    
    # Durations
    lines.append("    'durations': [")
    for job_idx, job_durations in enumerate(problem['durations']):
        lines.append(f"        # Job {job_idx}")
        
        # Dividir en líneas de máximo 5 intervalos para legibilidad
        dur_strs = []
        for min_val, max_val in job_durations:
            dur_strs.append(f"Interval({min_val}, {max_val})")
        
        # Dividir en grupos de 5
        for i in range(0, len(dur_strs), 5):
            group = dur_strs[i:i+5]
            if i == 0:
                line = "        [" + ", ".join(group)
            else:
                line = "         " + ", ".join(group)
            
            if i + 5 >= len(dur_strs):
                # Última línea del job
                line += "],"
            else:
                line += ","
            lines.append(line)
    
    lines.append("    ],")
    lines.append(f"    'name': '{problem_name.upper()}',")
    lines.append("    'has_intervals': True,")
    lines.append("    'description': 'Benchmark problem with custom interval processing times'")
    lines.append("}")
    lines.append("")
    lines.append("")
    
    # Getter function
    func_name = f"get_{problem_name.lower().replace('-', '_').replace('.', '_')}_problem"
    lines.append(f"def {func_name}():")
    lines.append("    \"\"\"")
    lines.append(f"    Obtiene los datos del problema {problem_name.upper()} con intervalos.")
    lines.append("    ")
    lines.append("    Returns:")
    lines.append(f"        Diccionario con los datos del problema {problem_name.upper()} con incertidumbre")
    lines.append("    \"\"\"")
    lines.append(f"    return {dict_name}")
    lines.append("")
    
    # Write to file
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Archivo generado: {output_path}")
    
    # Calcular estadísticas
    total_ops = problem['num_jobs'] * problem['num_machines']
    deterministic = sum(1 for job_durs in problem['durations'] 
                       for min_v, max_v in job_durs if min_v == max_v)
    uncertain = total_ops - deterministic
    
    print(f"  - Tamaño: {problem['num_jobs']}x{problem['num_machines']}")
    print(f"  - Operaciones determinísticas: {deterministic} ({deterministic/total_ops*100:.1f}%)")
    print(f"  - Operaciones con incertidumbre: {uncertain} ({uncertain/total_ops*100:.1f}%)")


def convert_directory(input_dir: str, output_dir: str, prefix: str = ""):
    """
    Convierte todos los archivos .txt de un directorio a archivos .py
    
    Args:
        input_dir: Directorio con archivos .txt
        output_dir: Directorio de salida para archivos .py
        prefix: Prefijo opcional para los nombres (ej: 'la' para problemas Lawrence)
    """
    if not os.path.exists(input_dir):
        print(f"❌ Error: Directorio {input_dir} no existe")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    if not txt_files:
        print(f"⚠️  No se encontraron archivos .txt en {input_dir}")
        return
    
    print(f"\n{'='*60}")
    print(f"Convirtiendo {len(txt_files)} archivos de {input_dir}")
    print(f"{'='*60}\n")
    
    for filename in sorted(txt_files):
        input_path = os.path.join(input_dir, filename)
        
        # Generar nombre de salida
        base_name = os.path.splitext(filename)[0]
        if prefix and not base_name.startswith(prefix):
            problem_name = f"{prefix}_{base_name}_interval"
        else:
            problem_name = f"{base_name}_interval"
        
        output_filename = f"{problem_name}.py"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            # Parsear archivo
            problem = parse_labeled_taillard(input_path)
            
            # Generar archivo Python
            generate_python_file(problem, output_path, problem_name)
            
        except Exception as e:
            print(f"❌ Error procesando {filename}:")
            print(f"   {str(e)}")
            print()


def convert_single_file(input_path: str, output_path: str = None, problem_name: str = None):
    """
    Convierte un único archivo .txt a .py
    
    Args:
        input_path: Ruta al archivo .txt
        output_path: Ruta de salida (opcional, se genera automáticamente si no se proporciona)
        problem_name: Nombre del problema (opcional, se extrae del filename si no se proporciona)
    """
    if not os.path.exists(input_path):
        print(f"❌ Error: Archivo {input_path} no existe")
        return
    
    # Generar nombre de salida si no se proporciona
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        problem_name = problem_name or f"{base_name}_interval"
        output_path = f"{problem_name}.py"
    
    if problem_name is None:
        base_name = os.path.splitext(os.path.basename(output_path))[0]
        problem_name = base_name
    
    print(f"\n{'='*60}")
    print(f"Convirtiendo: {input_path}")
    print(f"{'='*60}\n")
    
    try:
        # Parsear archivo
        problem = parse_labeled_taillard(input_path)
        
        # Generar archivo Python
        generate_python_file(problem, output_path, problem_name)
        
        print(f"\n✓ Conversión exitosa!")
        
    except Exception as e:
        print(f"❌ Error:")
        print(f"   {str(e)}")


def main():
    """Función principal con menú interactivo"""
    
    print("\n" + "="*60)
    print("CONVERTIDOR DE INSTANCIAS TAILLARD A PYTHON")
    print("="*60 + "\n")
    
    print("Opciones:")
    print("  1. Convertir un archivo individual")
    print("  2. Convertir un directorio completo")
    print("  3. Ejemplo de uso\n")
    
    choice = input("Selecciona opción (1-3): ").strip()
    
    if choice == "1":
        # Convertir archivo individual
        input_path = input("\nRuta del archivo .txt de entrada: ").strip()
        output_path = input("Ruta del archivo .py de salida (Enter para auto): ").strip()
        problem_name = input("Nombre del problema (Enter para auto): ").strip()
        
        if not output_path:
            output_path = None
        if not problem_name:
            problem_name = None
        
        convert_single_file(input_path, output_path, problem_name)
        
    elif choice == "2":
        # Convertir directorio
        input_dir = input("\nDirectorio de entrada con archivos .txt: ").strip()
        output_dir = input("Directorio de salida para archivos .py: ").strip()
        prefix = input("Prefijo para nombres (Enter para ninguno): ").strip()
        
        if not prefix:
            prefix = ""
        
        convert_directory(input_dir, output_dir, prefix)
        
    elif choice == "3":
        # Mostrar ejemplo
        print("\n" + "="*60)
        print("EJEMPLO DE USO")
        print("="*60 + "\n")
        
        print("# Convertir un archivo individual:")
        print("convert_single_file('la01.txt', 'la01_interval.py', 'la01_interval')")
        print()
        print("# Convertir un directorio completo:")
        print("convert_directory('taillard_instances/', 'jobshop_rl/data/', 'la')")
        print()
        print("# Los archivos .py generados se pueden importar así:")
        print("from jobshop_rl.data.la01_interval import get_la01_interval_problem")
        print("problem = get_la01_interval_problem()")
        
    else:
        print("❌ Opción inválida")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # Ejemplo de uso directo (descomenta para usar):
    
    # Convertir un archivo individual
    # convert_single_file('mi_instancia.txt', 'jobshop_rl/data/mi_instancia_interval.py', 'mi_instancia_interval')
    
    # Convertir un directorio completo
    # convert_directory('taillard_txt/', 'jobshop_rl/data/', 'la')
    
    # O ejecutar el menú interactivo
    main()
