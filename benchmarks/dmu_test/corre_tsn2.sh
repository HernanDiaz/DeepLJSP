#!/bin/sh
# Campaña TSN2 sobre las DMU intervalares: 30 runs por instancia,
# setup exacto de la fase B (setup_N2_tuned.txt). NO EDITAR en caliente.
cd /mnt/e/PycharmProjects/DeepLJSP/benchmarks/dmu_test/tsn2
SETUP=/mnt/e/PycharmProjects/DeepLJSP/T2N2/setup/phaseB/setup_N2_tuned.txt
BIN=/mnt/e/PycharmProjects/FuzzyFW
for f in /mnt/e/PycharmProjects/DeepLJSP/benchmarks/dmu_test/instancias_txt/*.txt; do
  echo "=== $(basename $f) $(date +%H:%M:%S)"
  $BIN "$SETUP" "$f" . 2>&1 | tail -1
done
echo "=== CAMPANA COMPLETA $(date +%H:%M:%S)"
