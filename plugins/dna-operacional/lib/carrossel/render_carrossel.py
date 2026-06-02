#!/usr/bin/env python3
"""Lê carrossel.json + templates.py, escreve slides/NN.html.
Uso: python3 render_carrossel.py <carrossel.json> <out_dir>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import templates

FONTS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&family=Caveat:wght@600;700&family=Instrument+Serif:ital@0;1&display=swap');
@font-face{font-family:'Nofex';src:url('../fonts/Nofex.ttf') format('truetype');}
@font-face{font-family:'Crankdat';src:url('../fonts/Crankdat-Bold.ttf') format('truetype');font-weight:700;}
@font-face{font-family:'Crankdat';src:url('../fonts/Crankdat-Regular.ttf') format('truetype');font-weight:400;}
"""

def page(body):
    return ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<link rel="stylesheet" href="../base.css">'
            '<style>%s</style></head><body>%s</body></html>' % (FONTS, body))

def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    meta = cfg["meta"]; slides = cfg["slides"]
    total = meta.get("total", len(slides))
    out_dir = sys.argv[2]; os.makedirs(out_dir, exist_ok=True)
    for i, s in enumerate(slides, 1):
        open(os.path.join(out_dir, "%02d.html" % i), "w", encoding="utf-8").write(
            page(templates.slide(s, idx=i, total=total, meta=meta)))
    print("gerados %d slides em %s" % (len(slides), out_dir))

if __name__ == "__main__":
    main()
