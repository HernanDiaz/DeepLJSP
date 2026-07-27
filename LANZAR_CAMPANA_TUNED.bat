@echo off
REM Campana completa con la configuracion ganadora de irace (tournament 7,
REM crossover 0.7695, maxtree 30, elitism 2): 120 evoluciones nuevas
REM (30 ablacion no-width + 60 objetivo robusto + 30 barrido lambda) y su
REM evaluacion sobre las 70 instancias. ~24h.
REM
REM NO sobreescribe nada: todo va a benchmarks\tuned\. Reejecutable: los JSON
REM ya existentes se saltan, asi que puede relanzarse si se interrumpe.
REM Desacoplado: sobrevive al cierre de esta ventana y de Claude Code.
cd /d %~dp0
if not exist logs\tuned_campaign mkdir logs\tuned_campaign
powershell -NoProfile -Command "Start-Process -WindowStyle Hidden -FilePath '%~dp0venv\Scripts\python.exe' -ArgumentList '%~dp0scripts\tuned_campaign.py' -WorkingDirectory '%~dp0' -RedirectStandardOutput '%~dp0logs\tuned_campaign\driver.log' -RedirectStandardError '%~dp0logs\tuned_campaign\driver.err.log'"
echo.
echo Lanzada en segundo plano (~24h).
echo   Progreso:   type logs\tuned_campaign\driver.log
echo   Resultados: benchmarks\tuned\RESULTADOS.md
pause
