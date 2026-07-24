@echo off
REM Re-evolucion GP con fitness corregido (6 seeds, 3 en paralelo, ~2h).
REM Desacoplado: sobrevive al cierre de esta ventana. Log: logs\reevo\driver.log
REM Resultados: benchmarks\reevo_fixedfit\VEREDICTO.md
cd /d %~dp0
if not exist logs\reevo mkdir logs\reevo
powershell -NoProfile -Command "Start-Process -WindowStyle Hidden -FilePath '%~dp0venv\Scripts\python.exe' -ArgumentList '%~dp0scripts\rerun_evolutions_fixedfit.py' -WorkingDirectory '%~dp0' -RedirectStandardOutput '%~dp0logs\reevo\driver.log' -RedirectStandardError '%~dp0logs\reevo\driver.err.log'"
echo.
echo Lanzado en segundo plano (~2 h; 3 procesos, hilos limitados).
echo Progreso:  type logs\reevo\driver.log
echo Veredicto: benchmarks\reevo_fixedfit\VEREDICTO.md
pause
