# Encadena la v3 EXTENDIDA (asintota: 30 rondas, paciencia 8) detras
# de la v4. Salida en carpeta NUEVA benchmarks\clon_v3_ext.
# NO EDITAR mientras se ejecuta. Python via Start-Process con
# redirecciones nativas (leccion del 2026-08-10: nunca *> en PS 5.1).
$ErrorActionPreference = "Stop"
Set-Location E:\PycharmProjects\DeepLJSP

while (-not (Select-String -Path benchmarks\clon_v4_rr\log.txt `
                           -Pattern "=== RESUMEN ===" -Quiet)) {
    Start-Sleep -Seconds 60
}
Start-Sleep -Seconds 15

Start-Process -Wait -WindowStyle Hidden `
    -FilePath "E:\PycharmProjects\DeepLJSP\venv\Scripts\python.exe" `
    -ArgumentList "scripts\clon_v3.py","--rondas","30","--paciencia","8", `
        "--salida","benchmarks/clon_v3_ext" `
    -WorkingDirectory "E:\PycharmProjects\DeepLJSP" `
    -RedirectStandardOutput "E:\PycharmProjects\DeepLJSP\logs\clon_v3_ext.log" `
    -RedirectStandardError "E:\PycharmProjects\DeepLJSP\logs\clon_v3_ext.err"
