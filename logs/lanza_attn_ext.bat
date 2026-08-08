@echo off
rem Extiende el brazo de atencion de 3 a 10 semillas (tarea #11).
rem Mismo tier, mismos episodios y mismo mecanismo que las semillas 2-4
rem (registro v2-attn-1000ep, tier full con --episodes 1000,
rem DEEPLJSP_AGENT=v2 y DEEPLJSP_V2_ATTENTION=2). Etiqueta NUEVA: no
rem sobrescribe nada.
rem
rem El marcador SOLO se escribe si el script termina bien: la primera
rem version lo escribia siempre y una aborto por la guarda de
rem DEEPLJSP_AGENT dejando una terminacion falsa.
cd /d E:\PycharmProjects\DeepLJSP
set DEEPLJSP_AGENT=v2
set DEEPLJSP_V2_ATTENTION=2
venv\Scripts\python.exe -X utf8 scripts\run_benchmark.py ^
  --tier full --episodes 1000 --tag v2-attn-1000ep-ext ^
  --seeds 5,6,7,8,9,10,11 > logs\attn_ext.log 2>&1
if errorlevel 1 (
  echo ATTN EXT FALLO errorlevel %errorlevel% > logs\attn_ext_fallo.txt
) else (
  echo ATTN EXT LISTO > logs\attn_ext_done.txt
)
