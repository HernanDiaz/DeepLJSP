# E6 version 2 (regla compilada y genetico optimizado): los dos
# experimentos parados por tiempo, uno detras de otro, con Start-Process
# y redireccion nativa (nunca *> en PS 5.1). Los dos son reanudables:
# si algo se corta, volver a lanzar este script retoma donde iba.
#   1. 15x15, 30x15 y 50x15, 3 corridas (e6t_clases.py,   ~29 h)
#   2. las 12 clasicas, 30 x 900 s      (e6c_clasicas.py, ~46 h)
# Las 70 Taillard (e6_tiempo.py) no se corren: su figura sale del
# articulo y la sustituyen las de las tres clases.
$repo = "E:\PycharmProjects\DeepLJSP"
Set-Location $repo
$env:OMP_NUM_THREADS = "1"
New-Item -ItemType Directory -Force (Join-Path $repo "logs\e6v2") | Out-Null
foreach ($nombre in @("e6t_clases", "e6c_clasicas")) {
    Start-Process -Wait -WindowStyle Hidden `
        -FilePath (Join-Path $repo "venv\Scripts\python.exe") `
        -ArgumentList "scripts\$nombre.py" -WorkingDirectory $repo `
        -RedirectStandardOutput (Join-Path $repo "logs\e6v2\$nombre.out") `
        -RedirectStandardError (Join-Path $repo "logs\e6v2\$nombre.err")
}
