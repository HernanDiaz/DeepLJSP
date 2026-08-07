@echo off
rem Espera a que la campana de pesos termine y lanza la confirmacion
rem pre-registrada del ganador. Desacoplado: sobrevive al cierre de la
rem sesion. NO adopta nada: solo mide y escribe el veredicto.
cd /d E:\PycharmProjects\DeepLJSP
:espera
if not exist logs\irace_reward_done.txt (
  timeout /t 300 /nobreak >nul
  goto espera
)
call tuning\run_confirm_reward.bat
