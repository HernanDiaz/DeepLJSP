"""
fig_arch_svg.py — Deep Sets policy/value network, publication-ready.

Same conventions as the compact-architecture template: all layout constants
in typographic points (1 pt = 1/72 in), so font sizes print at their stated
size when the figure is placed at its physical width; compact blocks (title
bar + two content lines); inline <polygon> arrowheads (svglib does not
support SVG <marker>, so marker-end would vanish in the PDF conversion).

Three columns, serpentine flow, input entering from above; the context MLP
sits vertically BETWEEN the two heads, so its two feeds are symmetric
elbows and the global state joins it with a straight arrow:

    eligible ops
        |
    encoder phi  ->  embeddings      [self-attn, dashed detour]
                          |               :
    policy head                        pooling
              <-  context MLP  <----'
    value head                       global state

Topology carries the semantics. SOLID edges are the base model's data
path: embeddings drop straight into pooling. The self-attention variant is
a DASHED DETOUR off that path (not a stage of it): its box and both its
arrows are dashed, because B = 0 removes it entirely and that is the model
every headline number uses. The grey dashed lane is the per-candidate path
that carries each phi_i past the pooling into the policy head: pooling by
design discards candidate identity, so the head must receive the embedding
itself alongside the context.

Run standalone:
    python paper/fig_arch_svg.py
Output:
    paper/figures/fig_arch.svg  (+ fig_arch.pdf via svglib/reportlab, with
    Times New Roman registered from the Windows font directory so the Greek
    letters survive as embedded vector text — and the core Times-Roman
    re-registered as TrueType, because reportlab otherwise leaves an
    unembedded Type 1 in the resources that publisher preflight flags)
"""

from pathlib import Path

# ── Layout constants (all in typographic points) ─────────────────────────────
BW      = 70     # block width (pt)
TITLE_H = 13     # title bar height inside block
LINE_H  = 12     # one content-line height
IO_H    = 20     # I/O box height (two text lines)
HGAP    = 16     # horizontal gap between slots
LM      = 44     # left margin: room for the pi(i|s) / V(s) labels
MX      = 2      # right canvas margin
BH      = TITLE_H + 2 * LINE_H          # block height (= 37 pt)
STEP    = BW + HGAP                     # 86 pt per slot

IN_TOP  = 6                              # eligible-ops box, above the encoder
ENC_TOP = 44                             # encoder row, lowered
MID1    = ENC_TOP + BH / 2               # row-1 arrow level (= 62.5)
Y_BASE  = 94                             # elbow lane of the base path
Y_SKIP  = 100                            # elbow lane of the phi_i path
R2      = 116                            # policy-head / pooling band top
VAL_TOP = R2 + BH + 8                    # value head below policy (= 161)

FONT  = "Times New Roman"
FS_T  = 6.8    # title bar font size
FS_B  = 6.2    # body (ops / out lines)
FS_IO = 6.4    # I/O box text
FS_N  = 5.4    # dim annotations
FS_L  = 5.4    # legend labels

# ── Colour palette ───────────────────────────────────────────────────────────
C_MLP  = "#D6EAF8"; C_MLPT = "#C5D9E8"    # learned blocks + their title bar
C_HEAD = "#FADBD8"; C_HEADT = "#E8C5C5"   # heads
C_POOL = "#EAECEE"; C_POOLT = "#D5D8DC"   # parameter-free pooling
C_ATT  = "#FDF3E3"; C_ATTT = "#F0DDBE"    # attention variant (dashed)
C_ATTA = "#8B6F3D"                        # its detour arrows
C_IO   = "#F2F3F4"                        # tensors / inputs
C_EDGE = "#2C3E50"; C_ARR = "#2C3E50"
C_SKIP = "#7F8C8D"; C_DIM = "#555555"

# ── Arrowhead dimensions (pt) ────────────────────────────────────────────────
AH_LEN, AH_HW     = 4.8, 2.0
AH_LEN_S, AH_HW_S = 3.5, 1.5


# ── SVG primitives ───────────────────────────────────────────────────────────

def _r(x, y, w, h, fill, stroke=C_EDGE, sw=0.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def _t(x, y, s, size=FS_B, weight="normal", fill="#111111", anchor="middle"):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'dominant-baseline="middle" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" '
            f'font-family="{FONT}">{s}</text>')


def _arrowhead(x, y, direction, color=C_ARR, ln=AH_LEN, hw=AH_HW):
    if direction == 'r':
        pts = f"{x-ln:.1f},{y-hw:.1f} {x:.1f},{y:.1f} {x-ln:.1f},{y+hw:.1f}"
    elif direction == 'l':
        pts = f"{x+ln:.1f},{y-hw:.1f} {x:.1f},{y:.1f} {x+ln:.1f},{y+hw:.1f}"
    elif direction == 'd':
        pts = f"{x-hw:.1f},{y-ln:.1f} {x:.1f},{y:.1f} {x+hw:.1f},{y-ln:.1f}"
    else:  # 'u'
        pts = f"{x-hw:.1f},{y+ln:.1f} {x:.1f},{y:.1f} {x+hw:.1f},{y+ln:.1f}"
    return f'<polygon points="{pts}" fill="{color}"/>'


def _ah(x1, y, x2, color=C_ARR, lw=0.8, dash=None):
    """Horizontal arrow with inline arrowhead."""
    xe = x2 - AH_LEN if x2 >= x1 else x2 + AH_LEN
    d = 'r' if x2 >= x1 else 'l'
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{xe:.1f}" y2="{y:.1f}" '
            f'stroke="{color}" stroke-width="{lw}"{dd}/>\n'
            + _arrowhead(x2, y, d, color))


def _av(x, y1, y2, color=C_ARR, lw=0.8, dash=None):
    """Vertical arrow with inline arrowhead."""
    ye = y2 - AH_LEN if y2 >= y1 else y2 + AH_LEN
    d = 'd' if y2 >= y1 else 'u'
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{ye:.1f}" '
            f'stroke="{color}" stroke-width="{lw}"{dd}/>\n'
            + _arrowhead(x, y2, d, color))


def _poly(points, color=C_ARR, lw=0.8, dash=None, ln=AH_LEN, hw=AH_HW):
    """Polyline through points with arrowhead at the last point.

    The final segment must be axis-aligned; the shaft stops short of the
    tip and the inline polygon draws the head.
    """
    (x3, y3), (x4, y4) = points[-2], points[-1]
    dy = 1 if y4 > y3 else (-1 if y4 < y3 else 0)
    dx = 1 if x4 > x3 else (-1 if x4 < x3 else 0)
    direction = {(1, 0): 'r', (-1, 0): 'l', (0, 1): 'd', (0, -1): 'u'}[(dx, dy)]
    xe, ye = x4 - dx * ln, y4 - dy * ln
    body = " ".join(f"{px:.1f},{py:.1f}" for px, py in points[:-1])
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline points="{body} {xe:.1f},{ye:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{lw}"{d}/>\n'
            + _arrowhead(x4, y4, direction, color, ln=ln, hw=hw))


# ── Block builders ───────────────────────────────────────────────────────────

def _block(x, y, title, ops, out, fill, tc, dashed=False):
    dash = "3,2" if dashed else None
    ps, cy = [], y
    ps += [_r(x, cy, BW, TITLE_H, tc, dash=dash),
           _t(x + BW / 2, cy + TITLE_H / 2, title, size=FS_T, weight="bold")]
    cy += TITLE_H
    ps += [_r(x, cy, BW, LINE_H, fill, dash=dash),
           _t(x + BW / 2, cy + LINE_H / 2, ops, size=FS_B)]
    cy += LINE_H
    ps += [_r(x, cy, BW, LINE_H, fill, dash=dash),
           _t(x + BW / 2, cy + LINE_H / 2, out, size=FS_B)]
    return ps, cy + LINE_H


def _io(x, y, l1, l2):
    return [_r(x, y, BW, IO_H, C_IO),
            _t(x + BW / 2, y + IO_H / 2 - 4.4, l1, size=FS_IO),
            _t(x + BW / 2, y + IO_H / 2 + 4.6, l2, size=FS_IO)]


# ── Main SVG builder ─────────────────────────────────────────────────────────

def build_svg() -> str:
    parts = []
    x = [LM + i * STEP for i in range(3)]          # 3 slots per row
    emb_top = MID1 - IO_H / 2

    enc_c = x[0] + BW / 2                          # encoder / input centre x
    emb_c = x[1] + BW / 2                          # embeddings centre x
    pol_c = x[0] + BW / 2                          # policy-head centre x
    pol_cy = R2 + BH / 2                           # policy centre y (134.5)
    val_cy = VAL_TOP + BH / 2                      # value centre y (179.5)
    ctx_cy = (pol_cy + val_cy) / 2                 # context centred between
    CTX_TOP = ctx_cy - BH / 2                      # the two heads
    xm = x[0] + BW + HGAP / 2                      # elbow lane, heads column
    G_TOP = VAL_TOP                                # global state, under pooling
    g_cy = G_TOP + IO_H / 2

    CW = x[2] + BW + MX
    sep_y = max(VAL_TOP + BH, G_TOP + IO_H) + 8
    leg_y = sep_y + 11
    CH = leg_y + 9

    parts.append(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{CW / 72:.3f}in" height="{CH / 72:.3f}in" '
        f'viewBox="0 0 {CW:.1f} {CH:.1f}">\n'
        f'<rect width="{CW:.1f}" height="{CH:.1f}" fill="white"/>')

    # ── input above the encoder, entering from the top ─────────────────────
    parts += _io(x[0], IN_TOP, "eligible ops", "|E| × 16")
    parts.append(_av(enc_c, IN_TOP + IO_H, ENC_TOP))

    ps, _ = _block(x[0], ENC_TOP, "encoder φ", "shared 2-layer MLP",
                   "→ |E| × h", C_MLP, C_MLPT)
    parts += ps
    parts.append(_t(x[0] + BW / 2, ENC_TOP + BH + 5.5,
                    "(weights indep. of n, m)", size=FS_N, fill=C_DIM))
    parts.append(_ah(x[0] + BW, MID1, x[1]))

    parts += _io(x[1], emb_top, "embeddings", "|E| × h")

    ps, _ = _block(x[2], ENC_TOP, "self-attn × B", "pre-LN, 4 heads",
                   "not in base (B=0)", C_ATT, C_ATTT, dashed=True)
    parts += ps

    # ── base path (SOLID): embeddings drop straight into the pooling ──────
    parts.append(_poly([(emb_c + 12, emb_top + IO_H),
                        (emb_c + 12, Y_BASE),
                        (x[2] + BW * 0.33, Y_BASE),
                        (x[2] + BW * 0.33, R2)]))

    # ── variant detour (DASHED): embeddings -> attention -> pooling ────────
    parts.append(_ah(x[1] + BW, MID1, x[2], color=C_ATTA, dash="3,2"))
    parts.append(_av(x[2] + BW * 0.67, ENC_TOP + BH, R2, color=C_ATTA,
                     dash="3,2"))

    # ── pooling (right), context between the heads (middle) ────────────────
    ps, _ = _block(x[2], R2, "pooling", "mean + max", "→ 2h summary",
                   C_POOL, C_POOLT)
    parts += ps

    ps, _ = _block(x[1], CTX_TOP, "context MLP", "2-layer MLP",
                   "→ context g", C_MLP, C_MLPT)
    parts += ps

    # pooling → context: straight where the two bands overlap
    y_pc = (R2 + BH + CTX_TOP) / 2
    parts.append(_ah(x[2], y_pc, x[1] + BW))

    # ── heads, fed by symmetric elbows from the context ────────────────────
    ps, _ = _block(x[0], R2, "policy head", "scores [φi ; g]",
                   "masked softmax", C_HEAD, C_HEADT)
    parts += ps
    ps, _ = _block(x[0], VAL_TOP, "value head", "reads g alone",
                   "return estimate", C_HEAD, C_HEADT)
    parts += ps

    parts.append(_poly([(x[1], ctx_cy), (xm, ctx_cy), (xm, pol_cy),
                        (x[0] + BW, pol_cy)]))
    parts.append(_poly([(x[1], ctx_cy), (xm, ctx_cy), (xm, val_cy),
                        (x[0] + BW, val_cy)]))

    parts.append(_ah(x[0], pol_cy, x[0] - 16))
    parts.append(_t(x[0] - 19, pol_cy, "π(i | s)", size=FS_IO, anchor="end"))
    parts.append(_ah(x[0], val_cy, x[0] - 16))
    parts.append(_t(x[0] - 19, val_cy, "V(s)", size=FS_IO, anchor="end"))

    # ── global state joining the context straight from the right ───────────
    parts += _io(x[2], G_TOP, "global state", "12 aggregates")
    parts.append(_ah(x[2], g_cy, x[1] + BW))

    # ── per-candidate path: each phi_i carried past the pooling ────────────
    parts.append(_poly([(emb_c - 12, emb_top + IO_H),
                        (emb_c - 12, Y_SKIP),
                        (pol_c, Y_SKIP),
                        (pol_c, R2)],
                       color=C_SKIP, dash="3.5,2",
                       ln=AH_LEN_S, hw=AH_HW_S))
    parts.append(_t((pol_c + emb_c - 12) / 2, Y_SKIP + 6,
                    "each φi, past the pooling", size=FS_N, fill=C_DIM))

    # ── separator + legend ─────────────────────────────────────────────────
    parts.append(f'<line x1="{MX}" y1="{sep_y:.1f}" x2="{CW - MX:.1f}" '
                 f'y2="{sep_y:.1f}" stroke="#BBBBBB" stroke-width="0.5"/>')

    legend = [(C_MLP, "learned MLP"),
              (C_POOL, "parameter-free"),
              (C_IO, "tensor / input"),
              ("dash", "attn. variant"),
              ("skip", "per-candidate φi")]
    slot_w = (CW - 2 * MX) / len(legend)
    sw_sz = 8
    for k, (c, lbl) in enumerate(legend):
        sx = MX + k * slot_w + slot_w * 0.04
        if c == "skip":
            parts.append(f'<line x1="{sx:.1f}" y1="{leg_y:.1f}" '
                         f'x2="{sx + sw_sz:.1f}" y2="{leg_y:.1f}" '
                         f'stroke="{C_SKIP}" stroke-width="0.9" '
                         f'stroke-dasharray="3,2"/>')
        elif c == "dash":
            parts.append(_r(sx, leg_y - sw_sz / 2, sw_sz, sw_sz, C_ATT,
                            stroke=C_ATTA, sw=0.5, dash="2,1.5"))
        else:
            parts.append(_r(sx, leg_y - sw_sz / 2, sw_sz, sw_sz, c,
                            stroke="#888888", sw=0.4))
        parts.append(_t(sx + sw_sz + 3, leg_y, lbl, size=FS_L,
                        anchor="start", fill="#333333"))

    parts.append("</svg>")
    return "\n".join(parts)


# ── PDF conversion (vector text: register the real Times New Roman) ─────────

def to_pdf(svg_path: Path, pdf_path: Path):
    from svglib.fonts import register_font
    register_font("Times New Roman", r"C:\Windows\Fonts\times.ttf")
    register_font("Times New Roman", r"C:\Windows\Fonts\timesbd.ttf",
                  weight="bold")
    # reportlab arranca el lienzo con el Times-Roman Type 1 del nucleo,
    # que queda en los recursos SIN EMBEBER aunque ningun glifo lo use, y
    # el preflight de la editorial lo marcaria. Registrar la TTF bajo ese
    # mismo nombre hace que cualquier referencia resuelva a fuente
    # embebida.
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont("Times-Roman",
                                   r"C:\Windows\Fonts\times.ttf"))
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    renderPDF.drawToFile(svg2rlg(str(svg_path)), str(pdf_path))


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_dir = Path(__file__).parent / "figures"
    out_dir.mkdir(exist_ok=True)
    svg_path = out_dir / "fig_arch.svg"
    svg = build_svg()
    svg_path.write_text(svg, encoding="utf-8")
    print(f"[saved] {svg_path}")

    import re
    m_w = re.search(r'width="([\d.]+in)"', svg)
    m_h = re.search(r'height="([\d.]+in)"', svg)
    print(f"  boxes={len(re.findall(r'<rect ', svg))}  "
          f"arrowheads={len(re.findall(r'<polygon ', svg))}  "
          f"physical size: {m_w.group(1)} × {m_h.group(1)}")

    pdf_path = out_dir / "fig_arch.pdf"
    to_pdf(svg_path, pdf_path)
    print(f"[saved] {pdf_path}")
