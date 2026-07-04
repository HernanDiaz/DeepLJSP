@echo off
setlocal enabledelayedexpansion
rem irace llama: target_runner.bat <configID> <instanceID> <seed_irace> <instancia> <parametros...>
rem La "instancia" (%4) es la semilla de entrenamiento (instances.txt)
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
set LAST=999999
for /f "delims=" %%i in ('venv\Scripts\python.exe scripts\train_eval_config.py --seed %TRAINSEED% --train-ids int__tai20_15_01 !PARAMS! 2^>nul') do set LAST=%%i
echo !LAST!
endlocal & exit /b 0
