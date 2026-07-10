@echo off
setlocal enabledelayedexpansion
rem Target runner del tuning del GP (irace). Presupuesto de evolucion FIJO
rem (pop 100 x gens 50, ~wall-clock comparable al entrenamiento del RL);
rem entrena en TA11-14, evalua la mejor regla en TA15-17 (validacion) e
rem imprime el RE medio como coste. stderr por-invocacion (evita el lock del
rem archivo compartido que serializaba los workers en la campana del RL).
rem irace llama: target_runner_gp.bat <configID> <instanceID> <seed_irace> <instancia> <parametros...>
set CFGID=%1
set INSTID=%2
set TRAINSEED=%4
shift & shift & shift & shift
set PARAMS=
:collect
if "%~1"=="" goto run
set PARAMS=!PARAMS! %~1
shift
goto collect
:run
cd /d E:\PycharmProjects\DeepLJSP
if not exist tuning\gp\runner_logs mkdir tuning\gp\runner_logs
set LAST=999999
for /f "delims=" %%i in ('venv\Scripts\python.exe scripts\evolve_gp_rule.py --seed %TRAINSEED% --pop 100 --gens 50 --train-ids "int__tai20_15_01,int__tai20_15_02,int__tai20_15_03,int__tai20_15_04" --eval-ids "int__tai20_15_05,int__tai20_15_06,int__tai20_15_07" !PARAMS! 2^>tuning\gp\runner_logs\run_%CFGID%_%INSTID%_%TRAINSEED%.log') do set LAST=%%i
echo !LAST!
endlocal & exit /b 0
