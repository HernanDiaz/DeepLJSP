# v4b (clones v3 reconstruyendo) y despues v4c (d hasta T).
# NO EDITAR mientras se ejecuta. Start-Process con redirecciones
# nativas (leccion 2026-08-10).
$ErrorActionPreference = "Stop"
Set-Location E:\PycharmProjects\DeepLJSP

Start-Process -Wait -WindowStyle Hidden `
    -FilePath "E:\PycharmProjects\DeepLJSP\venv\Scripts\python.exe" `
    -ArgumentList "scripts\clon_v4_rr.py","--salida","benchmarks/clon_v4b_clones", `
        "--modelos","benchmarks/clon_v3/clon_v3_seed1.pt,benchmarks/clon_v3/clon_v3_seed2.pt,benchmarks/clon_v3/clon_v3_seed3.pt" `
    -WorkingDirectory "E:\PycharmProjects\DeepLJSP" `
    -RedirectStandardOutput "E:\PycharmProjects\DeepLJSP\logs\clon_v4b.log" `
    -RedirectStandardError "E:\PycharmProjects\DeepLJSP\logs\clon_v4b.err"

Start-Process -Wait -WindowStyle Hidden `
    -FilePath "E:\PycharmProjects\DeepLJSP\venv\Scripts\python.exe" `
    -ArgumentList "scripts\clon_v4_rr.py","--salida","benchmarks/clon_v4c_dfull", `
        "--dmax","299" `
    -WorkingDirectory "E:\PycharmProjects\DeepLJSP" `
    -RedirectStandardOutput "E:\PycharmProjects\DeepLJSP\logs\clon_v4c.log" `
    -RedirectStandardError "E:\PycharmProjects\DeepLJSP\logs\clon_v4c.err"
