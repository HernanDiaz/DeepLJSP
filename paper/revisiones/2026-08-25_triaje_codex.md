# Triaje de la revisión Codex/EAAI (2026-08-25)

Informe crudo: `2026-08-25_revision_codex_eaai_raw.md` (gpt-5.6-sol,
esfuerzo alto, workspace aislado `review_ws/`, árbol real intacto y
auditado). Recomendación del revisor: **reject** con invitación a
reenvío. Cada acusación mayor se ha verificado de forma independiente
contra el código y los datos ANTES de este triaje.

## Mayores — veredicto propio

**M1. El currículo TA11→TA14 no es el implementado. CONFIRMADA.**
`batch_experimenter.py` transfiere pesos desde el "mejor agente
global", actualizado comparando makespans BRUTOS entre instancias
distintas. Auditadas las 30 tiradas: en 26, TA14 arranca de TA12 (el
bloque TA13 se descarta). El texto de §5.4 ("weights carried over
from each block to the next") es falso en general.

**M2. best_model.pt no es el checkpoint descrito. CONFIRMADA.**
`_track_best` guarda `best_model_state`, pero `save_checkpoint`
serializa la red ACTUAL. El artefacto desplegado es la red final del
bloque ganador, no los pesos del mejor episodio (§5.4 dice lo
contrario).

**M3. El idle lee el extremo inferior. CONFIRMADA.**
`idle_time.py` hace `start - machine_time` con la resta intervalar
[a,b]−[c,d]=[a−d,b−c] y toma el upper ⇒ contiene c^L_μ. Además el
start usa el max lexicográfico de Python, no el join componentwise.
Tumba la afirmación estructural "ninguna componente lee un extremo
inferior" (§7.3, contribución 3, conclusiones). El verificador no lo
vio porque la dependencia está encapsulada en `Interval.__sub__`.

**M4. f_λ del tracking usa la anchura equivocada. CONFIRMADA, PERO
CON IMPACTO ~NULO.** `_episode_makespan` toma el intervalo del max
lexicográfico (un solo job), no el componentwise. Solo afecta al
tracking interno de mejor episodio — y por M2 ese tracking ni
siquiera decide el artefacto guardado. La recompensa terminal sí usa
el componentwise (verificado), y todos los análisis de la frontera
son sobre depósitos con extremos componentwise del evaluador.

**M5. La regla GP destacada se seleccionó sobre las 70. CONFIRMADA
COMO HECHO, DESACTIVADA EMPÍRICAMENTE.** Recomputado: la selección
sobre TA15–TA20 elige LA MISMA regla (gp_tuned_seed1, 17.45 vs 18.13
de la segunda). Además: el contraste de medias-de-30 a una pasada es
libre de selección, y en las clásicas la Tabla 8 ya empareja 30v30 a
los tres presupuestos. Se resuelve con una frase y un check, sin
experimentos.

**M6. "Exact Wilcoxon" no es exacto en n≥60. CONFIRMADA.** Los
scripts usan el método por defecto de scipy (asintótico a esos n).
Ejemplo del revisor reproducible: p=0.0288 asintótica vs 0.0284
exacta. Ninguna conclusión cambia; el método exacto es computable a
n=70 ⇒ regenerar p-valores y corregir la convención de §5.1.

**M7. Reproducibilidad del paquete. PARCIALMENTE CONFIRMADA.** Parte
de los hallazgos son artefactos de MI ensamblaje del workspace de
revisión (README/licencias no copiados; main.log ausente). Huecos
reales del depósito: models/ referenciado por scripts, target_runner
de irace, árboles GP (por diseño están en el depósito GP — hay que
decirlo más fuerte), configs efectivas por tirada, y el verificador
exige main.log ⇒ hacerlo opcional.

**Figura 2. CONFIRMADA.** El logger escribe el peor caso en ambas
columnas; la curva pinta gap de peor caso, no la RE de la Eq. (4).
Etiquetar el eje correctamente o loguear el midpoint.

## Menores: todas razonables; destacan
- §4.1 dice pesos fijos, pero `problem_analyzer` adapta idle/balance
  por instancia (¡el ≈ de w_id era esto!). Divulgar.
- Balance omite máquinas con completion cero (difiere de la fórmula).
- "prove inert" → formulación con efecto e incertidumbre.
- "at no budget do they tie" → "at each evaluated budget".

## Las dos rutas

**Ruta A — describir el sistema real (sin reentrenar), ~2-3 días.**
Los resultados son hechos medidos sobre los artefactos que existen;
lo falso es la DESCRIPCIÓN. Reescribir §5.4 (régimen de transferencia
real y artefacto real), §4.1 (idle implementado, pesos adaptativos,
floors), reformular §7.3/contribución 3/conclusiones: el canal del
extremo inferior EXISTE (idle, peso ~0.24) y aun así las anchuras
como entrada son inertes — el hallazgo empírico se vuelve más
informativo, no menos. + M5 frase, M6 p-valores exactos, M7 paquete,
Fig. 2. Los 813 checks se amplían con checks de código-vs-texto.

**Ruta B — arreglar el pipeline y reentrenar, semanas de máquina.**
Currículo encadenado de verdad, checkpoint serializado correcto,
idle según fórmula, tracking componentwise; recampaña de 30 semillas
+ ablaciones + brazos robustos + reevaluaciones. Da la historia
limpia que el revisor exige para sus M1–M3.

Decisión del autor pendiente.
