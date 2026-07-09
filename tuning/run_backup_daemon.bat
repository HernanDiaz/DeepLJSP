@echo off
rem Daemon de backup rotado del .Rdata, DESACOPLADO de la sesion.
cd /d E:\PycharmProjects\DeepLJSP\tuning
if not exist rdata_backups mkdir rdata_backups
:loop
if exist irace_serious.Rdata (
  for /f "tokens=1-4 delims=/: " %%a in ("%date% %time%") do set STAMP=%%d%%c%%b_%%a
  copy /y irace_serious.Rdata "rdata_backups\bk_%RANDOM%.Rdata" >nul 2>&1
)
rem conservar solo las 12 mas recientes
for /f "skip=12 delims=" %%f in ('dir /b /o-d rdata_backups\bk_*.Rdata 2^>nul') do del "rdata_backups\%%f" >nul 2>&1
timeout /t 600 /nobreak >nul
goto loop
