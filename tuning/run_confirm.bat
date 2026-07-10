@echo off
rem Lanzador DESACOPLADO de la confirmacion elite #22 vs default.
rem Hilos limitados (via el propio script). Sobrevive al teardown de sesion.
cd /d E:\PycharmProjects\DeepLJSP
venv\Scripts\python.exe scripts\confirm_elite22.py > tuning\confirm_elite22.log 2>&1
