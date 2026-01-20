"""
Script para listar todos los problemas disponibles en el sistema.
"""

from jobshop_rl.data import PROBLEM_REGISTRY

print("\n" + "="*60)
print("PROBLEMAS DISPONIBLES EN EL SISTEMA")
print("="*60 + "\n")

# Agrupar por prefijo
problems_by_type = {}

for problem_id in sorted(PROBLEM_REGISTRY.keys()):
    # Determinar el tipo
    if problem_id.startswith('ft'):
        type_key = 'FT (Fisher & Thompson)'
    elif problem_id.startswith('abz'):
        type_key = 'ABZ (Adams, Balas & Zawack)'
    elif problem_id.startswith('ta'):
        type_key = 'Taillard (con intervalos)'
    elif problem_id.startswith('tai'):
        type_key = 'Taillard'
    else:
        type_key = 'Otros'
    
    if type_key not in problems_by_type:
        problems_by_type[type_key] = []
    
    problems_by_type[type_key].append(problem_id)

# Mostrar agrupados
for type_name in sorted(problems_by_type.keys()):
    print(f"\n{type_name}:")
    print("-" * 60)
    
    problems = problems_by_type[type_name]
    
    # Mostrar en columnas
    col_width = 30
    num_cols = 2
    
    for i in range(0, len(problems), num_cols):
        row_problems = problems[i:i+num_cols]
        row_str = "  ".join(f"{p:<{col_width}}" for p in row_problems)
        print(f"  {row_str}")

print("\n" + "="*60)
print(f"TOTAL: {len(PROBLEM_REGISTRY)} problemas disponibles")
print("="*60 + "\n")

print("EJEMPLOS DE USO:")
print("-" * 60)
print("\n# Entrenar con un problema:")
print("python -m jobshop_rl.main --mode batch --train-problem \"ta_01\" --eval-problem \"ta_02\"")

print("\n# Entrenar con múltiples problemas:")
tai_problems = [p for p in PROBLEM_REGISTRY.keys() if p.startswith('ta_')]
if len(tai_problems) >= 10:
    train_example = ",".join(tai_problems[:5])
    test_example = ",".join(tai_problems[5:10])
    print(f"python -m jobshop_rl.main --mode batch \\")
    print(f"  --train-problem \"{train_example}\" \\")
    print(f"  --eval-problem \"{test_example}\" \\")
    print(f"  --episodes 50 --reward adaptive --seed 1")

print("\n")
