# Encadena la tirada real del clon v3 detras del humo.
# NO EDITAR mientras se ejecuta.
$ErrorActionPreference = "Stop"
Set-Location E:\PycharmProjects\DeepLJSP

# 1) esperar a que el humo cierre (RESUMEN es lo ultimo que escribe)
while (-not (Select-String -Path benchmarks\clon_v3\log.txt `
                           -Pattern "=== RESUMEN ===" -Quiet)) {
    Start-Sleep -Seconds 20
}
Start-Sleep -Seconds 15

# 2) archivar el humo aparte; no se borra nada
New-Item -ItemType Directory -Force benchmarks\clon_v3\humo | Out-Null
foreach ($f in @("log.txt", "resultados.csv", "clon_v3_seed1.pt")) {
    if (Test-Path "benchmarks\clon_v3\$f") {
        Move-Item "benchmarks\clon_v3\$f" "benchmarks\clon_v3\humo\$f" -Force
    }
}

# 3) tirada real: 3 semillas x 10 rondas, n=64, top=4, 3 epocas
& .\venv\Scripts\python.exe scripts\clon_v3.py --seeds 3 --rondas 10 `
    --n 64 --top 4 --epocas 3 *> logs\clon_v3_real.log
