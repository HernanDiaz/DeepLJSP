@echo off
setlocal enabledelayedexpansion
rem Campana de PESOS DEL REWARD: fidelidad de operacion (2 instancias x
rem 1000 episodios, rutas batched, eval best-of-64). El optimizador va
rem congelado en los defaults de tab:hyper (sin flags = defaults del
rem script). Los --rw-* exportan DEEPLJSP_REWARD_WEIGHTS dentro del
rem script, que fija los seis pesos y anula el reajuste por instancia.
rem irace llama: target_runner_reward.bat <configID> <instanceID> <seed_irace> <instancia> <parametros...>
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
rem blindaje: ninguna variable de otros brazos debe tocar esta campana
set DEEPLJSP_V2_LAMBDA=
set DEEPLJSP_V2_ATTENTION=
set DEEPLJSP_V2_WORSTCASE_ONLY=
if not exist tuning\runner_logs_reward mkdir tuning\runner_logs_reward
set LAST=999999
rem stderr a archivo POR INVOCACION (ver target_runner_serious.bat)
for /f "delims=" %%i in ('venv\Scripts\python.exe scripts\train_eval_config.py --seed %TRAINSEED% --train-ids "int__tai20_15_01,int__tai20_15_02" --episodes 1000 --batched --eval-samples 64 !PARAMS! 2^>tuning\runner_logs_reward\run_%CFGID%_%INSTID%_%TRAINSEED%.log') do set LAST=%%i
echo !LAST!
endlocal & exit /b 0
