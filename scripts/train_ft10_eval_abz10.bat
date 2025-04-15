@echo off
echo === JobShopRL: Entrenar con FT10 y evaluar con ABZ10 ===
cd ..
python -m jobshop_rl.main --mode single --episodes 100 --reward adaptive --visualize --save-plots --train-problem ft10 --eval-problem abz10 --use-ortools
echo === Experimento completado ===
pause
