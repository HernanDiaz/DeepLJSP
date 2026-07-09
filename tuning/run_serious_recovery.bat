@echo off
rem Lanzador DESACOPLADO de la campana seria (recuperacion desde checkpoint
rem limpio). Se ejecuta via Start-Process para sobrevivir al teardown de la
rem sesion de Claude Code. logFile = irace_serious.Rdata (distinto del
rem archivo de recuperacion, para no pisarlo).
cd /d E:\PycharmProjects\DeepLJSP\tuning
"C:\Users\herdi\AppData\Local\Programs\R\R-4.6.1\bin\Rscript.exe" -e "library(irace); irace.cmdline(c('--scenario','scenario_serious.txt','--recovery-file','irace_serious_recovery.Rdata'))" > irace_serious.log 2>&1
