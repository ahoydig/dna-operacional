#!/usr/bin/env python3
"""QA lint do carrossel-lab. Valida HTML de slide contra o contrato de design.
Uso: python3 qa_lint.py <slide.html> [--json]
Sem dependências externas (regex + cálculo WCAG).

Lê o CSS de 3 fontes (senão os checks ficariam inertes — o HTML gerado linka base.css
externo e usa font-size em style= inline):
  1. blocos <style> do próprio HTML
  2. o base.css linkado via <link href="...base.css"> (resolvido relativo ao HTML)
  3. atributos style="..." inline dos elementos
"""
import re, sys, json, os

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

def _collect_css(html, base_dir):
    """Junta CSS de: <style> inline + base.css linkado + atributos style= inline."""
    parts = re.findall(r'<style>(.*?)</style>', html, re.S)
    # base.css linkado
    for href in re.findall(r'<link[^>]+href="([^"]+\.css)"', html):
        p = href
        if not os.path.isabs(p):
            p = os.path.normpath(os.path.join(base_dir, href))
        if os.path.exists(p):
            parts.append(open(p, encoding="utf-8").read())
    # atributos style="..." inline (font-sizes/cores aplicados direto nos elementos)
    parts += re.findall(r'style="([^"]*)"', html)
    return " ".join(parts)

def lint(html, base_dir="."):
    violations = []
    css = _collect_css(html, base_dir)

    bg = _first_hex(_find_var(css, '--bg'))
    # var de texto: o contrato usa --text (não --ink). aceitar ambos por robustez.
    ink = _first_hex(_find_var(css, '--text')) or _first_hex(_find_var(css, '--ink'))
    accent = _first_hex(_find_var(css, '--accent'))

    if bg and ink:
        if contrast_ratio(ink, bg) < 4.5:
            violations.append({"code": "CONTRAST_INK_BG",
                "msg": f"contraste text/bg {contrast_ratio(ink, bg):.2f} < 4.5"})
    if bg and accent:
        if contrast_ratio(accent, bg) < 3.0:
            violations.append({"code": "CONTRAST_ACCENT_BG",
                "msg": f"contraste accent/bg {contrast_ratio(accent, bg):.2f} < 3.0"})

    # sub (body text) com tamanho mínimo. A classe .body do contrato antigo nunca é emitida;
    # o body real é a .sub (com font-size inline = sub_size). Floor 20px (mínimo legível no mobile).
    for size in [int(s) for s in re.findall(r'class="sub[^"]*"[^>]*font-size\s*:\s*(\d+)px', html)]:
        if size < 20:
            violations.append({"code": "BODY_TOO_SMALL",
                "msg": f"sub {size}px < 20px (texto pequeno demais)"})

    # headline tem que ser GRANDE (regra dos virais: headline domina). Mínimo 76px.
    # Nota: NÃO travamos numa escala modular rígida — o design aprovado pelo user (96/104/112px)
    # é a régua real; forçar a escala teórica reprovaria design validado. Só pegamos headline pequena.
    hl_sizes = [int(s) for s in re.findall(r'class="headline[^"]*"[^>]*style="[^"]*font-size\s*:\s*(\d+)px', html)]
    for size in hl_sizes:
        if size < 76:
            violations.append({"code": "HEADLINE_TOO_SMALL",
                "msg": f"headline {size}px < 76px (headline tem que dominar)"})

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

    # asset faltando: <img src> apontando pra arquivo inexistente (figure/hero/bg/aux/preview)
    for src in re.findall(r'<img[^>]+src="([^"]+)"', html):
        if src.startswith(("http", "data:")):
            continue
        p = src if os.path.isabs(src) else os.path.normpath(os.path.join(base_dir, src))
        if not os.path.exists(p):
            violations.append({"code": "ASSET_MISSING", "msg": f"asset não encontrado: {src}"})

    # slide de conteúdo (tem .ghost, exclusivo do _content) precisa de prova visual (.shot) — regra #3
    if 'class="ghost"' in html and 'class="shot"' not in html:
        violations.append({"code": "NO_VISUAL",
            "msg": "slide de conteúdo sem hero/prova visual (.shot) — regra #3 (sem slide só-texto)"})

    return {"violations": violations}

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    html = open(args[0], encoding="utf-8").read()
    result = lint(html, base_dir=os.path.dirname(os.path.abspath(args[0])))
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
