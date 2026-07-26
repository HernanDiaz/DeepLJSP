@echo off
REM Dos trabajos encadenados (~8h en total), desacoplados:
REM  1) ablation_interval_width.py  (~1.5h) — ancho de intervalo 30v30 bajo
REM     objetivo MIDPOINT, para completar tab:ablation con media+-sd.
REM  2) lambda_sweep.py (~7h) — barrido lambda={0.5,2,4} x 10 seeds, brazo con
REM     anchura, para la frontera calidad-predictibilidad + fig_lambda.pdf.
cd /d %~dp0
if not exist logs\lambda_sweep mkdir logs\lambda_sweep
powershell -NoProfile -Command "Start-Process -WindowStyle Hidden -FilePath 'cmd.exe' -ArgumentList '/c','%~dp0venv\Scripts\python.exe %~dp0scripts\ablation_interval_width.py > %~dp0logs\lambda_sweep\anchos30.log 2>&1 & %~dp0venv\Scripts\python.exe %~dp0scripts\lambda_sweep.py --seeds 10 > %~dp0logs\lambda_sweep\driver.log 2>&1' -WorkingDirectory '%~dp0'"
echo Lanzado en segundo plano (~8h).
echo   anchos 30v30: type logs\lambda_sweep\anchos30.log
echo   barrido:      type logs\lambda_sweep\driver.log
pause
