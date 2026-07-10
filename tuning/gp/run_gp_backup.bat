@echo off
rem Daemon de backup rotado del .Rdata del tuning GP, DESACOPLADO.
cd /d E:\PycharmProjects\DeepLJSP\tuning\gp
if not exist rdata_backups mkdir rdata_backups
:loop
if exist irace_gp.Rdata (
  copy /y irace_gp.Rdata "rdata_backups\bk_%RANDOM%.Rdata" >nul 2>&1
)
for /f "skip=12 delims=" %%f in ('dir /b /o-d rdata_backups\bk_*.Rdata 2^>nul') do del "rdata_backups\%%f" >nul 2>&1
timeout /t 600 /nobreak >nul
goto loop
