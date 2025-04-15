@echo off
echo === JobShopRL: Entrenar con FT20 y evaluar con FT10 ===
cd ..
python -m jobshop_rl.main --mode single --episodes 100 --reward adaptive --visualize --save-plots --train-problem ft20 --eval-problem ft10 --use-ortools
echo === Experimento completado ===
pause
