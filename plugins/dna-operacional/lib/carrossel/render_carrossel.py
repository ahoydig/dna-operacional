#!/usr/bin/env python3
"""Lê carrossel.json + templates.py, escreve slides/NN.html.
Uso: python3 render_carrossel.py <carrossel.json> <out_dir>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import templates

GOOGLE = ("@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900"
          "&family=Caveat:wght@600;700&family=Instrument+Serif:ital@0;1&display=swap');")

LOCAL_FONTS = (GOOGLE + "\n"
    "@font-face{font-family:'Nofex';src:url('../fonts/Nofex.ttf') format('truetype');}\n"
    "@font-face{font-family:'Crankdat';src:url('../fonts/Crankdat-Bold.ttf') format('truetype');font-weight:700;}\n"
    "@font-face{font-family:'Crankdat';src:url('../fonts/Crankdat-Regular.ttf') format('truetype');font-weight:400;}")

# Fallback quando NÃO há Nofex/Crankdat local: Bebas Neue (display) + Space Grotesk (handle) via Google.
# Sem isso, headline cairia no genérico sans-serif e o visual viral sumia silenciosamente.
FALLBACK_FONTS = (GOOGLE + "\n"
    "@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@500;700&display=swap');\n"
    ".headline,.cta-stack .big,.ghost{font-family:'Bebas Neue',sans-serif !important;}\n"
    ".footer .handle,.swipe{font-family:'Space Grotesk',sans-serif !important;}")

REQUIRED = {"cover": ["headline"], "content": ["headline"], "quote": ["headline", "quote"], "cta": ["token"]}


def fonts_block(workdir):
    if os.path.exists(os.path.join(workdir, "fonts", "Nofex.ttf")):
        return LOCAL_FONTS
    sys.stderr.write("[render] AVISO: sem fontes locais (Nofex/Crankdat) — usando fallback Google "
                     "(Bebas Neue/Space Grotesk). Copie as .ttf pra <workdir>/fonts/ pro visual original.\n")
    return FALLBACK_FONTS


def validate(meta, slides):
    """Erro legível por slide/campo em vez de KeyError cru. Lista TODOS os problemas de uma vez."""
    errs = []
    if not meta.get("handle"):
        errs.append("meta.handle ausente (handle do Instagram, ex: @fulano)")
    if not slides:
        errs.append("nenhum slide em 'slides'")
    for i, s in enumerate(slides, 1):
        t = s.get("tipo")
        if t not in REQUIRED:
            errs.append(f"slide #{i}: tipo '{t}' desconhecido (use cover|content|quote|cta)")
            continue
        for f in REQUIRED[t]:
            if not s.get(f):
                errs.append(f"slide #{i} ({t}): campo '{f}' obrigatório ausente")
    if errs:
        sys.stderr.write("[render] JSON inválido — corrija e rode de novo:\n  - " + "\n  - ".join(errs) + "\n")
        sys.exit(2)


def page(body, fonts):
    return ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<link rel="stylesheet" href="../base.css">'
            '<style>%s</style></head><body>%s</body></html>' % (fonts, body))


def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    meta = cfg.get("meta") or {}
    slides = cfg.get("slides") or []
    validate(meta, slides)
    total = meta.get("total", len(slides))
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    fonts = fonts_block(os.path.dirname(os.path.abspath(out_dir)))
    for i, s in enumerate(slides, 1):
        open(os.path.join(out_dir, "%02d.html" % i), "w", encoding="utf-8").write(
            page(templates.slide(s, idx=i, total=total, meta=meta), fonts))
    print("gerados %d slides em %s" % (len(slides), out_dir))


if __name__ == "__main__":
    main()
