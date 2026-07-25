@echo off
REM Piloto fitness robusto (upper + lam*ancho): 5 seeds x 2 brazos
REM (width vs no-width). ~2h. Desacoplado, sobrevive al cierre de consola.
REM Resultado: benchmarks\pilot_robust\VEREDICTO_PILOTO.md
cd /d %~dp0
if not exist logs\pilot_robust mkdir logs\pilot_robust
powershell -NoProfile -Command "Start-Process -WindowStyle Hidden -FilePath '%~dp0venv\Scripts\python.exe' -ArgumentList '%~dp0scripts\pilot_robust_fitness.py','--lam','1.0','--seeds','5' -WorkingDirectory '%~dp0' -RedirectStandardOutput '%~dp0logs\pilot_robust\driver.log' -RedirectStandardError '%~dp0logs\pilot_robust\driver.err.log'"
echo Lanzado en segundo plano (~2h). Progreso: type logs\pilot_robust\driver.log
pause
