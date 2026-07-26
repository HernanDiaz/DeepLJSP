@echo off
REM Campana fitness robusto (upper + lam*ancho), 30 seeds x 2 brazos
REM (width vs no-width). Salta los 10 JSON del piloto ya hechos -> 50 nuevas.
REM ~12-13h. Desacoplado, sobrevive al cierre de consola.
REM Resultado: benchmarks\pilot_robust\VEREDICTO_PILOTO.md (con Wilcoxon)
cd /d %~dp0
if not exist logs\pilot_robust mkdir logs\pilot_robust
powershell -NoProfile -Command "Start-Process -WindowStyle Hidden -FilePath '%~dp0venv\Scripts\python.exe' -ArgumentList '%~dp0scripts\pilot_robust_fitness.py','--lam','1.0','--seeds','30' -WorkingDirectory '%~dp0' -RedirectStandardOutput '%~dp0logs\pilot_robust\driver30.log' -RedirectStandardError '%~dp0logs\pilot_robust\driver30.err.log'"
echo Lanzado en segundo plano (~12-13h). Progreso: type logs\pilot_robust\driver30.log
pause
