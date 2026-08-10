# Encadena la v4 (ruin & recreate) detras de la tirada real del v3.
# NO EDITAR mientras se ejecuta.
$ErrorActionPreference = "Stop"
Set-Location E:\PycharmProjects\DeepLJSP

# 1) esperar el cierre del v3 real (su log es nuevo, del 10/08 13:37;
#    el del humo esta archivado en benchmarks\clon_v3\humo\)
while (-not (Select-String -Path benchmarks\clon_v3\log.txt `
                           -Pattern "=== RESUMEN ===" -Quiet)) {
    Start-Sleep -Seconds 60
}
Start-Sleep -Seconds 15

# 2) v4 real: 3 politicas x 6 instancias dev, presupuesto 64xT, bo64
& .\venv\Scripts\python.exe scripts\clon_v4_rr.py *> logs\clon_v4_rr_real.log
