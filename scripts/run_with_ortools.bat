@echo off
echo === JobShopRL con comparación OR-Tools ===
echo Ejecutando experimento con FT10 y comparando con OR-Tools...
cd ..
python -m jobshop_rl.main --mode single --episodes 100 --reward adaptive --visualize --save-plots --train-problem ft10 --use-ortools --ortools-time-limit 60
echo === Experimento completado ===
pause
