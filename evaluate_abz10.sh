#!/bin/bash
echo "Evaluando el mejor modelo con el problema ABZ10..."
python -m jobshop_rl.evaluate_abz10 --visualize --save-plot --model-path best_model.pt
