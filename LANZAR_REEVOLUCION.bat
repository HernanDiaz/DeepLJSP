@echo off
REM Campana GP con fitness corregido: 30 default + 30 tuned + 30 no-width
REM (ablacion de interval-awareness). 3 procesos en paralelo.
REM Desacoplado: sobrevive al cierre de esta ventana. Log: logs\reevo\driver.log
REM Resultados: benchmarks\reevo_fixedfit\VEREDICTO.md (media+-std, Wilcoxon)
cd /d %~dp0
if not exist logs\reevo mkdir logs\reevo
powershell -NoProfile -Command "Start-Process -WindowStyle Hidden -FilePath '%~dp0venv\Scripts\python.exe' -ArgumentList '%~dp0scripts\rerun_evolutions_fixedfit.py' -WorkingDirectory '%~dp0' -RedirectStandardOutput '%~dp0logs\reevo\driver.log' -RedirectStandardError '%~dp0logs\reevo\driver.err.log'"
echo.
echo Lanzado en segundo plano (~28 h en total; 3 procesos, hilos limitados).
echo Progreso:  type logs\reevo\driver.log
echo Veredicto: benchmarks\reevo_fixedfit\VEREDICTO.md
pause
