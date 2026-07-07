@echo off
setlocal enabledelayedexpansion
rem Campana SERIA: fidelidad de operacion (2 instancias x 1000 episodios,
rem rutas vectorizadas batched_train/batched_eval en GPU, eval best-of-64).
rem Fijos por consenso elites+default de la campana previa: minibatch 256,
rem update-every 4.
rem irace llama: target_runner_serious.bat <configID> <instanceID> <seed_irace> <instancia> <parametros...>
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
if not exist tuning\runner_logs mkdir tuning\runner_logs
set LAST=999999
rem stderr a archivo POR INVOCACION: un archivo compartido con 2>> queda
rem bloqueado por el primer worker y los demas fallan la redireccion al
rem instante (devolviendo 999999 como coste y envenenando la campana)
for /f "delims=" %%i in ('venv\Scripts\python.exe scripts\train_eval_config.py --seed %TRAINSEED% --train-ids "int__tai20_15_01,int__tai20_15_02" --episodes 1000 --batched --eval-samples 64 --minibatch 256 --update-every 4 !PARAMS! 2^>tuning\runner_logs\run_%CFGID%_%INSTID%_%TRAINSEED%.log') do set LAST=%%i
echo !LAST!
endlocal & exit /b 0
