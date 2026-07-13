@echo off
rem Daemon de backup rotado del .Rdata de la campana seria ATENCION.
cd /d E:\PycharmProjects\DeepLJSP\tuning
if not exist rdata_backups_attn mkdir rdata_backups_attn
:loop
if exist irace_serious_attn.Rdata (
  copy /y irace_serious_attn.Rdata "rdata_backups_attn\bk_%RANDOM%.Rdata" >nul 2>&1
)
for /f "skip=12 delims=" %%f in ('dir /b /o-d rdata_backups_attn\bk_*.Rdata 2^>nul') do del "rdata_backups_attn\%%f" >nul 2>&1
timeout /t 600 /nobreak >nul
goto loop
