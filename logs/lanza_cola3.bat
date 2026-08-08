@echo off
rem Cola tras la extension sin-anchuras (que a su vez espera a la de
rem atencion): (1) la semilla 11 del brazo robusto lambda=1, la unica
rem que falta para dejarlo en diez; (2) la robustez ejecucional de 7.5
rem sobre las 70 instancias. Marcadores solo con exit 0.
cd /d E:\PycharmProjects\DeepLJSP
:espera
if not exist logs\nowidth_ext_done.txt (
  timeout /t 300 /nobreak >nul
  goto espera
)

set DEEPLJSP_AGENT=v2
set DEEPLJSP_V2_ATTENTION=
set DEEPLJSP_V2_WORSTCASE_ONLY=
set DEEPLJSP_V2_LAMBDA=1
venv\Scripts\python.exe -X utf8 scripts\run_benchmark.py ^
  --tier full --episodes 1000 --tag v2-robust-lam1-ext-b ^
  --seeds 11 > logs\lam1_s11.log 2>&1
if errorlevel 1 (
  echo LAM1 S11 FALLO > logs\lam1_s11_fallo.txt
) else (
  echo LAM1 S11 LISTO > logs\lam1_s11_done.txt
)

set DEEPLJSP_V2_LAMBDA=
venv\Scripts\python.exe -X utf8 scripts\eval_eps_all70.py ^
  > logs\eps70.log 2>&1
if errorlevel 1 (
  echo EPS70 FALLO > logs\eps70_fallo.txt
) else (
  echo EPS70 LISTO > logs\eps70_done.txt
)
