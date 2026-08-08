@echo off
rem Espera a que termine la extension del brazo de atencion y extiende
rem el brazo sin anchuras de 3 a 10 semillas (tarea #11). Mismo
rem mecanismo que las semillas 2-4 (DEEPLJSP_V2_WORSTCASE_ONLY=1).
rem Etiqueta NUEVA: no sobrescribe nada. El marcador solo se escribe
rem si el proceso termina bien.
cd /d E:\PycharmProjects\DeepLJSP
:espera
if not exist logs\attn_ext_done.txt (
  timeout /t 300 /nobreak >nul
  goto espera
)
set DEEPLJSP_AGENT=v2
set DEEPLJSP_V2_WORSTCASE_ONLY=1
venv\Scripts\python.exe -X utf8 scripts\run_benchmark.py ^
  --tier full --episodes 1000 --tag v2-nowidth-1000ep-ext ^
  --seeds 5,6,7,8,9,10,11 > logs\nowidth_ext.log 2>&1
if errorlevel 1 (
  echo NOWIDTH EXT FALLO > logs\nowidth_ext_fallo.txt
) else (
  echo NOWIDTH EXT LISTO > logs\nowidth_ext_done.txt
)
