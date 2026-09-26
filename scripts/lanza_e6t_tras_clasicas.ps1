# Espera a que termine el experimento de las clasicas (e6c_clasicas.py) y
# lanza el de las tres clases de Taillard (e6t_clases.py), con
# Start-Process y redireccion nativa (nunca *> en PS 5.1).
$repo = "E:\PycharmProjects\DeepLJSP"
Set-Location $repo
$marca = Join-Path $repo "logs\e6c\clasicas.out"
while (-not (Select-String -Path $marca -Pattern "experimento hecho" -Quiet)) {
    Start-Sleep -Seconds 120
}
New-Item -ItemType Directory -Force (Join-Path $repo "logs\e6t") | Out-Null
Start-Process -WindowStyle Hidden -FilePath (Join-Path $repo "venv\Scripts\python.exe") `
    -ArgumentList "scripts\e6t_clases.py" -WorkingDirectory $repo `
    -RedirectStandardOutput (Join-Path $repo "logs\e6t\clases.out") `
    -RedirectStandardError (Join-Path $repo "logs\e6t\clases.err")
