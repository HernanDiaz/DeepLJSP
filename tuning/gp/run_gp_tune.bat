@echo off
rem Lanzador DESACOPLADO del tuning del GP (sobrevive al teardown de sesion).
rem Uso: arrancar via  Start-Process cmd /c run_gp_tune.bat  con -WorkingDirectory
rem apuntando a tuning\gp. Para recuperar: anadir --recovery-file irace_gp_recovery.Rdata.
cd /d E:\PycharmProjects\DeepLJSP\tuning\gp
"C:\Users\herdi\AppData\Local\Programs\R\R-4.6.1\bin\Rscript.exe" -e "library(irace); irace.cmdline(c('--scenario','scenario_gp.txt'))" > irace_gp.log 2>&1
