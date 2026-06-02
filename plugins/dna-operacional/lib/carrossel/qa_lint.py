#!/usr/bin/env python3
"""QA lint do carrossel-lab. Valida HTML de slide contra o contrato de design.
Uso: python3 qa_lint.py <slide.html> [--json]
Sem dependências externas (regex + cálculo WCAG)."""
import re, sys, json

MODULAR = {24, 32, 43, 57, 76, 101, 135}

def _hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _luminance(rgb):
    def chan(c):
        c = c / 255.0
        return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    r, g, b = (chan(x) for x in rgb)
    return 0.2126*r + 0.7152*g + 0.0722*b

def contrast_ratio(hex1, hex2):
    l1, l2 = _luminance(_hex_to_rgb(hex1)), _luminance(_hex_to_rgb(hex2))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

def _find_var(css, name):
    m = re.search(rf'{re.escape(name)}\s*:\s*([^;]+);', css)
    return m.group(1).strip() if m else None

def _first_hex(value):
    if value is None:
        return None
    m = re.search(r'#[0-9A-Fa-f]{3,6}', value)
    return m.group(0) if m else None

def lint(html):
    violations = []
    css = " ".join(re.findall(r'<style>(.*?)</style>', html, re.S))

    bg = _first_hex(_find_var(css, '--bg'))
    ink = _first_hex(_find_var(css, '--ink'))
    accent = _first_hex(_find_var(css, '--accent'))

    if bg and ink:
        if contrast_ratio(ink, bg) < 4.5:
            violations.append({"code": "CONTRAST_INK_BG",
                "msg": f"contraste ink/bg {contrast_ratio(ink, bg):.2f} < 4.5"})
    if bg and accent:
        if contrast_ratio(accent, bg) < 3.0:
            violations.append({"code": "CONTRAST_ACCENT_BG",
                "msg": f"contraste accent/bg {contrast_ratio(accent, bg):.2f} < 3.0"})

    # body font-size mínimo 24px e dentro da escala modular
    for m in re.finditer(r'\.body\s*\{[^}]*font-size\s*:\s*(\d+)px', css):
        size = int(m.group(1))
        if size < 24:
            violations.append({"code": "BODY_TOO_SMALL",
                "msg": f"body {size}px < 24px"})

    # qualquer font-size declarado deve estar na escala modular
    for m in re.finditer(r'font-size\s*:\s*(\d+)px', css):
        size = int(m.group(1))
        if size not in MODULAR:
            violations.append({"code": "FONT_OFF_SCALE",
                "msg": f"font-size {size}px fora da escala modular {sorted(MODULAR)}"})

    # object-fit: contain combinado com background no mesmo bloco de screenshot
    for block in re.findall(r'\{[^}]*\}', css):
        if 'object-fit' in block and 'contain' in block and 'background' in block:
            violations.append({"code": "OBJECTFIT_CONTAIN_BG",
                "msg": "object-fit:contain + background cria bordas escuras"})

    # headline deve ter >=1 palavra accent (<span class="em">) — regra do MANIFESTO (exatamente 1)
    for m in re.finditer(r'class="headline[^"]*"[^>]*>(.*?)</div>', html, re.S):
        if 'class="em"' not in m.group(1):
            violations.append({"code": "HEADLINE_NO_ACCENT",
                "msg": "headline sem palavra accent (<span class='em'>)"})

    return {"violations": violations}

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    html = open(args[0], encoding="utf-8").read()
    result = lint(html)
    if as_json:
        print(json.dumps(result))
    else:
        if not result["violations"]:
            print("OK — sem violações")
        else:
            for v in result["violations"]:
                print(f"[{v['code']}] {v['msg']}")
    sys.exit(1 if result["violations"] else 0)

if __name__ == "__main__":
    main()
