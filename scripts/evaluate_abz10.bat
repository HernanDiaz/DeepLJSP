@echo off
echo Evaluando el mejor modelo con el problema ABZ10...
cd ..
python -m jobshop_rl.evaluate_abz10 --visualize --save-plot --model-path best_model.pt
pause
