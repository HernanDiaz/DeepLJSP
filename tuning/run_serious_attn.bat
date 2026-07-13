@echo off
rem Lanzador DESACOPLADO de la campana seria ATENCION (sobrevive al teardown
rem de sesion). Arrancar via:
rem   Start-Process cmd /c tuning\run_serious_attn.bat -WorkingDirectory tuning
rem Para recuperar tras un corte: anadir --recovery-file irace_serious_attn_recovery.Rdata
cd /d E:\PycharmProjects\DeepLJSP\tuning
"C:\Users\herdi\AppData\Local\Programs\R\R-4.6.1\bin\Rscript.exe" -e "library(irace); irace.cmdline(c('--scenario','scenario_serious_attn.txt'))" > irace_serious_attn.log 2>&1
