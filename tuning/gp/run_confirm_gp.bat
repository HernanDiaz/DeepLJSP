@echo off
rem Confirmacion GP tuneado vs default, DESACOPLADA de la sesion.
cd /d E:\PycharmProjects\DeepLJSP
venv\Scripts\python.exe scripts\confirm_gp_tuned.py > tuning\gp\confirm_gp.log 2>&1
