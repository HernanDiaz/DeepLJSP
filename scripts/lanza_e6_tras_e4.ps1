# Encadena E6 detras de E4: las dos campañas saturan la maquina, asi que
# E6 espera a que los sesenta artefactos de E4 esten en disco y entonces
# lanza sus seis carriles.
#
# Redirecciones nativas de Start-Process: con `*>` en PowerShell 5.1 el
# proceso desatendido se muere al cerrar la sesion.
#
# NO EDITAR mientras se ejecuta.
$ErrorActionPreference = "Stop"
Set-Location E:\PycharmProjects\DeepLJSP

$objetivo = 60
while ($true) {
    $n = @(Get-ChildItem -Path benchmarks\e4_asimetrico -Filter seed*.json `
                         -Recurse -ErrorAction SilentlyContinue).Count
    if ($n -ge $objetivo) { break }
    Start-Sleep -Seconds 120
}

# margen para que el ultimo carril cierre su fichero
Start-Sleep -Seconds 60

0..5 | ForEach-Object {
    Start-Process -FilePath ".\venv\Scripts\python.exe" `
      -ArgumentList "-X","utf8","scripts\e6_presupuesto.py", `
                    "--carril","$_","--de","6" `
      -RedirectStandardOutput "logs\e6_carril$_.out" `
      -RedirectStandardError  "logs\e6_carril$_.err" `
      -WindowStyle Hidden
}
"E6 lanzado a las $(Get-Date -Format 'HH:mm:ss')" |
    Out-File -FilePath logs\e6_encadenado.log -Encoding utf8
