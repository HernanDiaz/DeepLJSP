# E6 version 2 (regla compilada y genetico optimizado): los tres
# experimentos parados por tiempo, uno detras de otro, con Start-Process
# y redireccion nativa (nunca *> en PS 5.1). Los tres son reanudables:
# si algo se corta, volver a lanzar este script retoma donde iba.
#   1. las 70 Taillard, 800 s           (e6_tiempo.py,    ~18 h)
#   2. las 12 clasicas, 30 x 900 s      (e6c_clasicas.py, ~46 h)
#   3. 15x15, 30x15 y 50x15, 3 corridas (e6t_clases.py,   ~29 h)
$repo = "E:\PycharmProjects\DeepLJSP"
Set-Location $repo
$env:OMP_NUM_THREADS = "1"
New-Item -ItemType Directory -Force (Join-Path $repo "logs\e6v2") | Out-Null
foreach ($nombre in @("e6_tiempo", "e6c_clasicas", "e6t_clases")) {
    Start-Process -Wait -WindowStyle Hidden `
        -FilePath (Join-Path $repo "venv\Scripts\python.exe") `
        -ArgumentList "scripts\$nombre.py" -WorkingDirectory $repo `
        -RedirectStandardOutput (Join-Path $repo "logs\e6v2\$nombre.out") `
        -RedirectStandardError (Join-Path $repo "logs\e6v2\$nombre.err")
}
