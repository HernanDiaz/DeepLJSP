@echo off
rem Lanzador DESACOPLADO de la confirmacion del ganador de la campana de
rem pesos del reward. Requiere que la campana haya terminado
rem (logs\irace_reward_done.txt). Sobrevive al teardown de sesion.
cd /d E:\PycharmProjects\DeepLJSP
if not exist logs\irace_reward_done.txt (
  echo La campana de irace aun no ha terminado. Abortando.
  exit /b 1
)
venv\Scripts\python.exe scripts\confirma_ganador_reward.py > tuning\confirm_reward.log 2>&1
echo CONFIRMACION LISTA > logs\confirm_reward_done.txt
