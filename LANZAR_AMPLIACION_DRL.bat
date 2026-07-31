@echo off
REM Ampliacion experimental del paper DRL (bloques B y C), secuencial.
REM Coste aproximado: 5h (no-width) + 5h (punto medio) + 12h (7 semillas
REM extra) de CPU. Cada brazo escribe su propio benchmark JSON y sus
REM directorios en outputs\ -- nada se sobreescribe.
REM
REM Requisito: repo limpio (run_benchmark avisa si hay cambios sin commit).

cd /d E:\PycharmProjects\DeepLJSP

echo === [1/3] Ablacion no-width (encoder solo-peor-caso) ===
set DEEPLJSP_V2_WORSTCASE_ONLY=1
venv\Scripts\python.exe scripts\run_benchmark.py --tier full --tag v2-nowidth-1000ep --episodes 1000
set DEEPLJSP_V2_WORSTCASE_ONLY=

echo === [2/3] Control del punto medio (entrena crisp, evalua intervalo) ===
venv\Scripts\python.exe scripts\run_benchmark.py --tier midpoint --tag v2-midpoint-1000ep

echo === [3/3] Ampliacion de semillas: 5-11 del brazo principal ===
venv\Scripts\python.exe scripts\run_benchmark.py --tier full --tag v2-full-1000ep-ext --episodes 1000 --seeds 5,6,7,8,9,10,11

echo === AMPLIACION COMPLETA ===
pause
