# Metadatos para el formulario de Zenodo

(Este fichero es una guia para rellenar el registro; no forma parte del
deposito publicado. Borrar antes de subir o dejar fuera del zip.)

**Tipo de registro**: Dataset (con software)

**Titulo**:
Deep Reinforcement Learning for the Interval Job Shop:
Checkpoints, Records and Code

**Autor**: Díaz Rodríguez, Hernán — University of Oviedo (añadir ORCID
en el formulario)

**Descripcion** (campo Description):
Companion data and code for the article "Deep Reinforcement Learning
for the Interval Job Shop Scheduling Problem: A Comparison with
Genetic Programming Hyper-Heuristics across Inference Budgets". The
deposit contains the final checkpoints of every training run of the
article's arms (main policy at three training budgets, interval
ablations, self-attention variant and width-penalizing arms); the
primary CSV/JSON result files behind every table and figure, accepted
and rejected records alike; the training and evaluation package
(jobshop_rl) with the interval scheduling environment, the Deep Sets
policy and the PPO trainer; and the verification script that
recomputes every number the article prints from the primary files in
this deposit, together with the benchmark instances themselves. The
article's supplementary material (the automatic configuration
campaigns, the self-attention variant and the per-instance results)
is included as a PDF. The thirty evolved GP rules the article
compares against are published at doi:10.5281/zenodo.21716972 and,
from v3 on, mirrored here under rules/gp_main_arm/ so the shared
evaluation can be rerun from this deposit alone.

**Nota v3** (campo version notes / description al publicar la nueva
version): v3 adds the exported checkpoints (code/models/), the irace
target-runner scripts and the mirrored GP rules of the main arm; the
per-rollout deposits behind the budget curve, the sampled GP arm and
the width-penalizing arms, each storing both interval endpoints so
that any inference budget or retention criterion can be recomputed
without re-evaluating; the forty training runs of the
width-penalizing arms; and a training-reproduction section in the
README.

**Keywords**: interval job shop scheduling; deep reinforcement
learning; neural combinatorial optimization; scheduling under
uncertainty; PPO; size invariance; benchmark results

**Licencias**: código MIT; datos CC BY 4.0 (si Zenodo obliga a elegir
una, CC BY 4.0 y el LICENSE del código dentro del zip).

**Funding**: MCIN/AEI/10.13039/501100011033, grant PID2022-141746OB-I00

**Related identifiers**:
- "is supplement to" → DOI del artículo cuando exista (o dejar pendiente)
- "references" → 10.5281/zenodo.21716972 (las reglas GP)
