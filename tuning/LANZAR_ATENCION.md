# Campaña seria de ATENCIÓN — lista para lanzar

Infraestructura montada y probada (smoke test del target runner OK,
2026-07-13). **No lanzada** — arrancar cuando se decida.

## Qué es
Tuning irace de la variante de atención a fidelidad de operación (1000 eps),
para cerrar la comparativa arquitectónica tuned-vs-tuned del paper. Espacio
de 8 parámetros (los 6 de la serie Deep Sets + capas de atención {1,2,3} y
cabezas {2,4,8}), default L=2/H=4 sembrada + 2 élites Deep Sets adaptadas.
maxExperiments=400, parallel=3. Estimado: ~2.5-3.5 días de máquina dedicada
+ ~3h de confirmación.

Recordatorio: la ablación previa ya favorece Deep Sets (+1.2% @300, +1.6%
@1000). Esto es por completitud, no se espera que cambie el modelo final.

## Cómo lanzar (desde PowerShell)
```powershell
cd E:\PycharmProjects\DeepLJSP\tuning
Start-Process -FilePath "cmd.exe" -ArgumentList "/c","E:\PycharmProjects\DeepLJSP\tuning\run_serious_attn.bat" -WorkingDirectory "E:\PycharmProjects\DeepLJSP\tuning" -WindowStyle Hidden
Start-Process -FilePath "cmd.exe" -ArgumentList "/c","E:\PycharmProjects\DeepLJSP\tuning\run_serious_attn_backup.bat" -WorkingDirectory "E:\PycharmProjects\DeepLJSP\tuning" -WindowStyle Hidden
```
(desacoplado: sobrevive a reinicios de sesión de Claude Code)

## Seguimiento
- Log: `tuning/irace_serious_attn.log`
- stderr por experimento: `tuning/runner_logs_attn/`
- Backups del checkpoint: `tuning/rdata_backups_attn/` (cada 10 min)

## Recuperación tras un corte
Copiar el `.Rdata` estable (frontera de iteración o backup bk_) a
`irace_serious_attn_recovery.Rdata` y añadir `--recovery-file
irace_serious_attn_recovery.Rdata` a la llamada en `run_serious_attn.bat`.

## Al terminar
Confirmación pre-registrada: élite atención vs default atención a presupuesto
completo (TA11-14 × 1000 eps × 3 semillas, eval TA15-20) — adaptar
`scripts/confirm_elite22.py` con la config y `attention_layers`.

## Archivos
- `parameters_serious_attn.txt`, `configurations_serious_attn.txt`,
  `scenario_serious_attn.txt`, `target_runner_serious_attn.bat`
- `run_serious_attn.bat` (lanzador), `run_serious_attn_backup.bat` (daemon)
