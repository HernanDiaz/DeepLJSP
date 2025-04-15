@echo off
echo Entrenando con FT10 y evaluando con ABZ10...
cd ..
python -m jobshop_rl.main --mode single --episodes 300 --reward advanced --visualize --save-plots --evaluate-abz10
pause
