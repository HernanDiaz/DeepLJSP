# Tercer paper: siembra de metaheurísticas con generadores aprendidos

Carpeta del futuro paper 3 (decidido 2026-07-24): la comparación GP-vs-DRL
se saca del paper del GP (que queda autocontenido, sin dependencia del
companion) y se integra AQUÍ, junto con los resultados de siembra del TS en
el cluster cuando lleguen.

## Contenido previsto
- Comparación controlada GP vs DRL con presupuestos emparejados
  (`PARKED_gp_vs_rl.tex` — ojo: números pre-fix, ver nota en el archivo y
  `paper_gp/AUDIT_MAKESPAN_FIX.md`).
- Framing del hueco señalado por el survey de Xu et al. (AI Review 58:160,
  2025): faltan comparaciones GP-vs-RL bajo protocolo común, y piden
  hibridación — este paper hace ambas.
- Los 4 generadores de semillas (v2, GP-ε, MOR-ε, GT-ε): calidad,
  diversidad, robustez (benchmarks/generators_comparison.csv y análisis de
  pools ya hechos).
- Resultados del piloto TS con 5 brazos (cluster, pendiente).
- Transferencia entre modelos de incertidumbre (crisp/fuzzy/estocástico,
  RESULTADOS_TRANSFERENCIA.md) como evidencia de robustez de las semillas.

## Orden de publicación acordado
1. paper_gp -> revista, directo, sin arXiv (autocontenido).
2. paper (RL) -> después, citando el GP.
3. Este -> con los resultados del cluster; hereda la comparación GP-vs-DRL.
