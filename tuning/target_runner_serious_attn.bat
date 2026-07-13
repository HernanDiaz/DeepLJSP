@echo off
setlocal enabledelayedexpansion
rem Campana SERIA variante ATENCION: fidelidad de operacion (2 instancias x
rem 1000 episodios, rutas vectorizadas en GPU, eval best-of-64). Fijos por
rem consenso Deep Sets: minibatch 256, update-every 4. attention/heads vienen
rem en !PARAMS! desde irace.
rem irace llama: target_runner_serious_attn.bat <configID> <instanceID> <seed_irace> <instancia> <parametros...>
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
if not exist tuning\runner_logs_attn mkdir tuning\runner_logs_attn
set LAST=999999
for /f "delims=" %%i in ('venv\Scripts\python.exe scripts\train_eval_config.py --seed %TRAINSEED% --train-ids "int__tai20_15_01,int__tai20_15_02" --episodes 1000 --batched --eval-samples 64 --minibatch 256 --update-every 4 !PARAMS! 2^>tuning\runner_logs_attn\run_%CFGID%_%INSTID%_%TRAINSEED%.log') do set LAST=%%i
echo !LAST!
endlocal & exit /b 0
