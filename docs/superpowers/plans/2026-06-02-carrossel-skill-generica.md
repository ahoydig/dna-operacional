# Carrossel Skill Genérica — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reescrever o `/carrossel-instagram` como skill geradora de carrossel viral para QUALQUER tema, consolidando o sistema visual validado (geometria real dos virais, ativos reais, loop de verificação com auto-correção).

**Architecture:** Um gerador Python parametrizado (`render_carrossel.py`) lê um JSON de roteiro (`carrossel.json`) + uma biblioteca de templates (`templates.py`) que clona a geometria do MANIFESTO (eixo 48px, 3 templates capa/conteúdo/CTA), produz HTML por slide, renderiza via Playwright (`render.mjs`), e um agente revisor compara cada PNG com o manifesto e auto-corrige até passar. O command (`carrossel-instagram.md`) orquestra: pesquisa→roteiro→**gate de aprovação**→pipeline de ativos reais→render→loop de verificação→entrega.

**Tech Stack:** Python 3 (gerador + qa_lint, sem deps externas além de Pillow), Node+Playwright (render), HTML/CSS (base.css contrato), skill `gerar-imagem` (assets via IA com `-i` referência), Apify/Playwright MCP (captura), Markdown (command + references).

---

## Convenções deste plano

- **Repo:** `/Users/flavioahoy/Documents/projects/dna-operacional`, branch `ahoydig/carrossel-torneio`. Paths relativos a `plugins/dna-operacional/` salvo indicação.
- **Material de referência (NÃO modificar, é fonte):** `/Users/flavioahoy/orca/workspaces/etc/Nautilus/scrape-virais/MANIFESTO-DIAGRAMACAO.md` e as `RECEITA.md`. Protótipo funcional: `/Users/flavioahoy/orca/workspaces/etc/Nautilus/hormozi-final/` (`gen.py`, `base.css`, `assets/`, `render.mjs`).
- **SAFETY:** nunca `git add -A`/`git add .` — path explícito. Não tocar em `skills/proposta/` (mudanças alheias). Não commitar `node_modules`/`__pycache__`/`slides/*.png`.
- **Commits PT-BR** terminando com `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- **TDD real** onde há código Python testável (gerador, qa_lint). "Verificação visual" onde o artefato é imagem (render → ler PNG).
- **base.css canônico:** a fonte de verdade do CSS é `hormozi-final/base.css` (validado visualmente pelo user). O `lib/carrossel/base.css` do repo será sobrescrito por ele.

---

## File Structure

**Núcleo do gerador (novo, em `lib/carrossel/`):**
- `lib/carrossel/base.css` — contrato CSS (sobrescrito pela versão validada do protótipo). Classes: `.slide`, `.headline`+`.em`, `.sub`, `.kicker`, `.hero`/`.shot`, `.quote`, `.footer`/`.handle`, `.swipe`, `.cta-stack`, `.ghost`, `.snum`, `.bgphoto`/`.scrim`, `.note`, `.compo`.
- `lib/carrossel/templates.py` — funções que geram o HTML de cada tipo de slide a partir de dados: `cover()`, `content()`, `cta()`, `quote()`, `footer()`. Eixo 48px, fontes corretas.
- `lib/carrossel/render_carrossel.py` — lê `carrossel.json`, chama `templates.py`, escreve `slides/NN.html`. CLI: `python3 render_carrossel.py <carrossel.json> <out_dir>`.
- `lib/carrossel/render.mjs` — Playwright: renderiza cada `slides/NN.html` → `NN.png` (1080×1350 @2x).
- `lib/carrossel/qa_lint.py` — lint estrutural (já existe; estender com checagens novas).
- `lib/carrossel/schema.md` — documenta o formato do `carrossel.json` (contrato do roteiro).
- `lib/carrossel/tests/` — testes pytest do gerador + fixtures.

**References (conhecimento, em `references/carrossel-lab/`):**
- `references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md` — copiado do material (blueprint de geometria).
- (demais references já existem do rebuild anterior.)

**Pipeline de ativos (novo):**
- `lib/carrossel/assets-pipeline.md` — guia: como obter cada tipo de ativo (foto real→pixel, logo PNG, telas forjadas, bg do criador).
- `lib/carrossel/forge-screen.md` — como forjar telas de UI (Claude.ai etc) em PT-BR via HTML→PNG.

**Command (orquestrador):**
- `commands/carrossel-instagram.md` — reescrito: pesquisa→roteiro→gate→assets→render→loop verificação→entrega.

**Limpeza:**
- Remover commands do laboratório (`carrossel-lab-*.md`, `carrossel-torneio.md`) — eram do torneio, não vão pra produção.

---

## Task 1: Copiar base.css validado + manifesto pro repo

**Files:**
- Modify: `lib/carrossel/base.css` (sobrescrever com versão validada)
- Create: `references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md`

- [ ] **Step 1: Copiar base.css validado do protótipo**

```bash
cp /Users/flavioahoy/orca/workspaces/etc/Nautilus/hormozi-final/base.css \
   /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional/lib/carrossel/base.css
```

- [ ] **Step 2: Copiar o manifesto como reference**

```bash
cp /Users/flavioahoy/orca/workspaces/etc/Nautilus/scrape-virais/MANIFESTO-DIAGRAMACAO.md \
   /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional/references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md
```

- [ ] **Step 3: Verificar**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -c "s=open('lib/carrossel/base.css').read(); assert s.count('{')==s.count('}'); assert '--pad-x' in s; print('base.css ok', s.count('{'),'blocos')"
grep -c "eixo de coluna\|padding-x\|TEMPLATE" references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md
```
Expected: "base.css ok" + grep ≥1.

- [ ] **Step 4: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/base.css plugins/dna-operacional/references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md
git commit -m "feat(carrossel): base.css validado + manifesto de diagramação como reference

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Definir o schema do carrossel.json

**Files:**
- Create: `lib/carrossel/schema.md`
- Create: `lib/carrossel/tests/exemplo.json` (fixture canônica)

- [ ] **Step 1: Escrever o schema.md**

````markdown
# Schema do carrossel.json (contrato do roteiro)

O gerador (`render_carrossel.py`) lê este JSON. Um objeto com `meta` + lista `slides`.

```json
{
  "meta": {
    "handle": "@flavioahoy",
    "accent": "#C4714A",
    "tema": "claro|escuro",
    "bg_photo": "assets/bg-capa.png",
    "total": 7
  },
  "slides": [
    {
      "tipo": "cover",
      "kicker": "Sem saber programar",
      "headline": "Clone o {Hormozi} dentro do Claude",
      "sub": "6 docs. Um prompt. Ele {destrincha seu negócio}.",
      "compo": {"left": "assets/hormozi-pixel.png", "left2": "assets/livros.png",
                "right_icon": "assets/claude-sun.png", "right_label": "Claude"}
    },
    {
      "tipo": "content",
      "kicker": "Passo 1",
      "headline": "Crie um {projeto}",
      "sub": "Abra um projeto novo e batize de {\"Coach Hormozi\"}.",
      "hero": "assets/tela1.png"
    },
    {
      "tipo": "quote",
      "kicker": "Por que importa",
      "headline": "Um sócio {brutalmente} honesto. De graça.",
      "quote": "A maioria paga R$2 mil/hora por isso.",
      "sub": "Não é sobre o Hormozi."
    },
    {
      "tipo": "cta",
      "headline_top": "Quer o passo a passo?",
      "token": "HORMOZI",
      "sub": "que eu te mando os {6 docs + o prompt}.",
      "bg_photo": "assets/bg-capa.png"
    }
  ]
}
```

## Convenções
- `{texto}` na headline/sub = a palavra/grupo **accent** (vira serif itálico colorido). EXATAMENTE 1 por headline (regra do manifesto).
- `tipo`: `cover` | `content` | `quote` | `cta`.
- `hero`: caminho de imagem (screenshot/réplica) — usado em `content`.
- `compo`: composição da capa (personagem+livros → ícone). Opcional; se ausente, capa é só texto+bg.
- Caminhos de imagem são relativos ao `out_dir` (onde ficam os slides) — convenção: `assets/...`.
- `meta.tema`: `escuro` (default) ou `claro`.
- `meta.total`: número de slides (pra numeração NN/total).
````

- [ ] **Step 2: Criar fixture exemplo.json (carrossel mínimo de 3 slides p/ teste)**

```json
{
  "meta": {"handle": "@teste", "accent": "#C4714A", "tema": "escuro", "total": 3},
  "slides": [
    {"tipo": "cover", "kicker": "Teste", "headline": "Capa de {teste} aqui", "sub": "Subtítulo de {teste}."},
    {"tipo": "content", "kicker": "Passo 1", "headline": "Conteúdo {um}", "sub": "Corpo do slide {dois}.", "hero": "assets/shot.png"},
    {"tipo": "cta", "headline_top": "Quer mais?", "token": "TESTE", "sub": "comenta {TESTE} aí."}
  ]
}
```

- [ ] **Step 3: Verificar JSON válido**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -c "import json; d=json.load(open('lib/carrossel/tests/exemplo.json')); print('slides:', len(d['slides']), '| tipos:', [s['tipo'] for s in d['slides']])"
```
Expected: `slides: 3 | tipos: ['cover', 'content', 'cta']`.

- [ ] **Step 4: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/schema.md plugins/dna-operacional/lib/carrossel/tests/exemplo.json
git commit -m "feat(carrossel): schema do roteiro (carrossel.json) + fixture

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: templates.py — função de accent + footer (TDD)

**Files:**
- Create: `lib/carrossel/templates.py`
- Create: `lib/carrossel/tests/test_templates.py`

- [ ] **Step 1: Escrever testes falhando**

```python
# tests/test_templates.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import templates

def test_accent_converte_chaves_em_span_em():
    # {palavra} vira <span class="em">palavra</span>
    out = templates.accent("Clone o {Hormozi} agora")
    assert '<span class="em">Hormozi</span>' in out
    assert "{" not in out and "}" not in out

def test_accent_sem_chaves_passa_direto():
    assert templates.accent("Sem accent") == "Sem accent"

def test_footer_tem_handle_e_crankdat():
    out = templates.footer("@flavioahoy", swipe=True)
    assert "@flavioahoy" in out
    assert "handle" in out          # classe .handle (Crankdat via CSS)
    assert "swipe" in out           # swipe presente

def test_footer_sem_swipe():
    out = templates.footer("@x", swipe=False)
    assert "swipe" not in out
```

- [ ] **Step 2: Rodar — deve falhar (módulo não existe)**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_templates.py -v
```
Expected: FAIL (ModuleNotFoundError: templates).

- [ ] **Step 3: Implementar templates.py (accent + footer)**

```python
#!/usr/bin/env python3
"""Biblioteca de templates de slide — clona a geometria do MANIFESTO-DIAGRAMACAO.md.
Eixo de coluna 48px (via base.css --pad-x). Headline Nofex + 1 palavra serif itálico accent.
Crankdat só no handle/swipe. 4 tipos: cover, content, quote, cta."""
import re, html

def accent(text):
    """Converte {palavra} -> <span class="em">palavra</span> (a palavra accent da headline).
    Regra do manifesto: exatamente 1 por headline, vira serif itálico colorido."""
    def repl(m):
        return '<span class="em">%s</span>' % m.group(1)
    return re.sub(r"\{([^}]+)\}", repl, text)

def footer(handle, swipe=True):
    s = '<div class="footer"><span class="handle">%s</span></div>' % html.escape(handle)
    if swipe:
        s += '<div class="swipe">arrasta &rarr;</div>'
    return s
```

- [ ] **Step 4: Rodar — deve passar (4 testes)**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_templates.py -v
```
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/templates.py plugins/dna-operacional/lib/carrossel/tests/test_templates.py
git commit -m "feat(carrossel): templates.py com accent + footer (TDD)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: templates.py — slide cover, content, quote, cta (TDD)

**Files:**
- Modify: `lib/carrossel/templates.py`
- Modify: `lib/carrossel/tests/test_templates.py`

- [ ] **Step 1: Adicionar testes falhando**

```python
def test_content_tem_kicker_headline_hero_footer():
    s = {"tipo":"content","kicker":"Passo 1","headline":"Crie um {projeto}",
         "sub":"corpo aqui","hero":"assets/x.png"}
    out = templates.slide(s, idx=2, total=7, meta={"handle":"@f","accent":"#C4714A","tema":"escuro"})
    assert "Passo 1" in out
    assert '<span class="em">projeto</span>' in out
    assert "assets/x.png" in out
    assert "02 / 07" in out          # numeração
    assert "@f" in out               # footer

def test_cover_usa_bg_e_compo():
    s = {"tipo":"cover","kicker":"K","headline":"H {accent}","sub":"s {x}",
         "compo":{"left":"a.png","right_icon":"i.png","right_label":"Claude"}}
    out = templates.slide(s, idx=1, total=7, meta={"handle":"@f","accent":"#C4714A","tema":"escuro","bg_photo":"bg.png"})
    assert "bg.png" in out and "bgphoto" in out
    assert "a.png" in out and "i.png" in out and "Claude" in out

def test_cta_tem_token_e_comenta():
    s = {"tipo":"cta","headline_top":"Quer?","token":"HORMOZI","sub":"manda {x}"}
    out = templates.slide(s, idx=7, total=7, meta={"handle":"@f","accent":"#C4714A","tema":"escuro"})
    assert "HORMOZI" in out
    assert "cta-stack" in out
    assert "swipe" not in out         # CTA não tem swipe

def test_quote_tem_aspas():
    s = {"tipo":"quote","kicker":"K","headline":"H {x}","quote":"frase shareable","sub":"s"}
    out = templates.slide(s, idx=6, total=7, meta={"handle":"@f","accent":"#C4714A","tema":"escuro"})
    assert "frase shareable" in out
    assert "quote" in out
```

- [ ] **Step 2: Rodar — 4 novos falham**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_templates.py -v
```
Expected: 4 passam (accent/footer), 4 falham (slide não existe).

- [ ] **Step 3: Implementar `slide()` dispatcher + os 4 tipos em templates.py**

Adicionar ao fim de `templates.py`:

```python
def _theme_class(meta):
    return "theme-dark" if meta.get("tema","escuro") == "escuro" else "theme-cream"

def _num(idx, total):
    return '<div class="snum">%02d / %02d</div>' % (idx, total)

def slide(s, idx, total, meta):
    t = s["tipo"]
    if t == "cover":   return _cover(s, idx, total, meta)
    if t == "content": return _content(s, idx, total, meta)
    if t == "quote":   return _quote(s, idx, total, meta)
    if t == "cta":     return _cta(s, idx, total, meta)
    raise ValueError("tipo desconhecido: %s" % t)

def _bg(meta_or_slide):
    p = meta_or_slide.get("bg_photo")
    if not p: return ""
    return '<img class="bgphoto" src="%s"><div class="scrim"></div>' % p

def _content(s, idx, total, meta):
    hsize = s.get("hsize", 104)
    hero = '<div class="hero"><img class="shot" src="%s"></div>' % s["hero"] if s.get("hero") else ""
    return f"""
<div class="slide">
  <div class="ghost">{idx-1:02d}</div>
  {_num(idx,total)}
  <div style="margin-top:30px">
    <div class="kicker">{s.get('kicker','')}</div>
    <div class="headline" style="font-size:{hsize}px;">{accent(s['headline'])}</div>
    <div class="sub">{accent(s.get('sub',''))}</div>
  </div>
  <div class="spacer"></div>
  {hero}
  <div class="spacer"></div>
  {footer(meta['handle'], swipe=True)}
</div>"""

def _cover(s, idx, total, meta):
    compo = ""
    c = s.get("compo")
    if c:
        left2 = ('<img src="%s" style="position:absolute;bottom:-6px;left:-160px;width:360px;'
                 'filter:drop-shadow(0 14px 26px rgba(0,0,0,0.6));">' % c["left2"]) if c.get("left2") else ""
        compo = f"""<div style="position:absolute;bottom:118px;left:0;right:0;z-index:2;display:flex;align-items:flex-end;justify-content:center;gap:30px;">
  <div style="position:relative;display:flex;align-items:flex-end;">
    <img src="{c['left']}" style="height:540px;filter:drop-shadow(0 16px 30px rgba(0,0,0,0.65));">{left2}
  </div>
  <div style="font-family:'Nofex',sans-serif;font-size:84px;color:#fff;margin-bottom:230px;filter:drop-shadow(0 4px 10px rgba(0,0,0,0.6));">&rarr;</div>
  <div style="margin-bottom:120px;display:flex;flex-direction:column;align-items:center;gap:16px;">
    <div style="width:300px;height:300px;border-radius:64px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 48px rgba(0,0,0,0.55);">
      <img src="{c['right_icon']}" style="width:210px;height:210px;"></div>
    <div style="font-family:'Inter';font-weight:700;font-size:48px;color:#fff;">{c.get('right_label','')}</div>
  </div></div>"""
    icon_top = '<img src="%s" style="width:84px;height:84px;margin:8px 0 14px;z-index:1;display:block;">' % meta["icon_top"] if meta.get("icon_top") else ""
    return f"""
<div class="slide" style="justify-content:flex-start;text-align:left;align-items:flex-start;">
  {_bg(meta)}
  <div class="snum" style="color:#cfc7bf">{idx:02d} / {total:02d}</div>
  {icon_top}
  <div class="kicker" style="margin:0 0 14px;">{s.get('kicker','')}</div>
  <div class="headline" style="font-size:{s.get('hsize',104)}px;text-align:left;">{accent(s['headline'])}</div>
  <div class="sub" style="margin:22px 0 0;max-width:26ch;text-align:left;color:#e8e0d6;">{accent(s.get('sub',''))}</div>
  {compo}
  {footer(meta['handle'], swipe=True)}
</div>"""

def _quote(s, idx, total, meta):
    return f"""
<div class="slide">
  {_num(idx,total)}
  <div style="margin-top:40px">
    <div class="kicker">{s.get('kicker','')}</div>
    <div class="headline" style="font-size:{s.get('hsize',96)}px;">{accent(s['headline'])}</div>
  </div>
  <div class="spacer"></div>
  <div class="quote">"{s['quote']}"</div>
  <div class="spacer"></div>
  <div class="sub" style="max-width:34ch;">{accent(s.get('sub',''))}</div>
  <div class="spacer"></div>
  {footer(meta['handle'], swipe=True)}
</div>"""

def _cta(s, idx, total, meta):
    icon = '<img src="%s" style="width:104px;height:104px;margin:0 auto 16px;z-index:1;display:block;">' % meta["icon_top"] if meta.get("icon_top") else ""
    return f"""
<div class="slide center" style="justify-content:center;text-align:center;">
  {_bg(s if s.get('bg_photo') else meta)}
  <div class="snum" style="color:#cfc7bf">{idx:02d} / {total:02d}</div>
  {icon}
  <div class="cta-stack" style="text-align:center;">
    <div class="big" style="font-size:64px;color:#e8e0d6;">{s.get('headline_top','')}</div>
    <div class="big" style="font-size:120px;margin-top:8px;">Comenta</div>
    <div class="big tok" style="font-size:120px;">"{s['token']}"</div>
  </div>
  <div class="sub" style="margin:28px auto 0;max-width:30ch;text-align:center;color:#e8e0d6;">{accent(s.get('sub',''))}</div>
  <div style="font-family:'Crankdat',sans-serif;font-weight:700;font-size:48px;color:var(--accent);margin-top:20px;z-index:1;">&darr; comenta aqui embaixo</div>
  {footer(meta['handle'], swipe=False)}
</div>"""
```

- [ ] **Step 4: Rodar — 8 testes passam**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_templates.py -v
```
Expected: 8 passed.

- [ ] **Step 5: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/templates.py plugins/dna-operacional/lib/carrossel/tests/test_templates.py
git commit -m "feat(carrossel): 4 templates de slide (cover/content/quote/cta) TDD

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: render_carrossel.py — JSON → HTML (TDD)

**Files:**
- Create: `lib/carrossel/render_carrossel.py`
- Create: `lib/carrossel/tests/test_render_carrossel.py`

- [ ] **Step 1: Escrever teste falhando**

```python
# tests/test_render_carrossel.py
import subprocess, sys, os, tempfile, shutil, json
HERE = os.path.dirname(__file__)
GEN = os.path.join(HERE, "..", "render_carrossel.py")

def test_gera_html_por_slide():
    tmp = tempfile.mkdtemp()
    try:
        out = subprocess.run([sys.executable, GEN, os.path.join(HERE,"exemplo.json"), tmp],
                             capture_output=True, text=True)
        assert out.returncode == 0, out.stderr
        files = sorted(f for f in os.listdir(tmp) if f.endswith(".html"))
        assert files == ["01.html","02.html","03.html"]
        cover = open(os.path.join(tmp,"01.html")).read()
        assert "<!DOCTYPE html>" in cover
        assert "base.css" in cover            # linka o contrato
        assert "@teste" in cover              # handle do meta
        content = open(os.path.join(tmp,"02.html")).read()
        assert "assets/shot.png" in content   # hero
    finally:
        shutil.rmtree(tmp)
```

- [ ] **Step 2: Rodar — falha (gerador não existe)**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_render_carrossel.py -v
```
Expected: FAIL.

- [ ] **Step 3: Implementar render_carrossel.py**

```python
#!/usr/bin/env python3
"""Lê carrossel.json + templates.py, escreve slides/NN.html.
Uso: python3 render_carrossel.py <carrossel.json> <out_dir>
Cada HTML linka ../base.css e declara @font-face (Nofex, Crankdat)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
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
    cfg_path, out_dir = sys.argv[1], sys.argv[2]
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    meta = cfg["meta"]; slides = cfg["slides"]
    total = meta.get("total", len(slides))
    os.makedirs(out_dir, exist_ok=True)
    for i, s in enumerate(slides, 1):
        body = templates.slide(s, idx=i, total=total, meta=meta)
        open(os.path.join(out_dir, "%02d.html" % i), "w", encoding="utf-8").write(page(body))
    print("gerados %d slides em %s" % (len(slides), out_dir))

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Rodar — passa**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_render_carrossel.py -v
```
Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/render_carrossel.py plugins/dna-operacional/lib/carrossel/tests/test_render_carrossel.py
git commit -m "feat(carrossel): render_carrossel.py — JSON do roteiro para HTML (TDD)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: render.mjs — HTML → PNG (harness Playwright)

**Files:**
- Create: `lib/carrossel/render.mjs`

- [ ] **Step 1: Escrever render.mjs**

```javascript
// HTML → PNG 1080x1350 @2x. Uso: node render.mjs <dir_com_slides>
import { chromium } from 'playwright';
import path from 'path'; import fs from 'fs';
const dir = process.argv[2];
const files = fs.readdirSync(dir).filter(f => /^\d\d\.html$/.test(f)).sort();
const b = await chromium.launch();
for (const f of files) {
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(dir, f), { waitUntil: 'networkidle' });
  try { await p.evaluate(() => document.fonts.ready); } catch {}
  await p.waitForTimeout(2200);
  const s = await p.$('.slide');
  const out = path.join(dir, f.replace('.html', '.png'));
  if (s) await s.screenshot({ path: out });
  else await p.screenshot({ path: out, clip: { x:0,y:0,width:1080,height:1350 } });
  console.log('rendered', f);
  await p.close();
}
await b.close();
console.log('DONE');
```

- [ ] **Step 2: Smoke test (gerar fixture + renderizar)**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional/lib/carrossel
# precisa de playwright + fontes. linkar node_modules de um projeto que tem playwright:
ln -sfn /Users/flavioahoy/Documents/projects/propostas/node_modules ./node_modules
mkdir -p /tmp/carr-smoke/assets /tmp/carr-smoke/fonts
cp /Users/flavioahoy/orca/workspaces/etc/Nautilus/hormozi-final/fonts/* /tmp/carr-smoke/fonts/ 2>/dev/null
# criar um shot.png dummy
python3 -c "from PIL import Image; Image.new('RGB',(900,600),(40,40,40)).save('/tmp/carr-smoke/assets/shot.png')"
python3 render_carrossel.py tests/exemplo.json /tmp/carr-smoke
cp base.css /tmp/carr-smoke/base.css
node render.mjs /tmp/carr-smoke 2>&1 | tail -4
ls /tmp/carr-smoke/*.png
```
Expected: "rendered 01.html...03.html", "DONE", e 3 PNGs listados.

- [ ] **Step 3: Verificar dimensões dos PNG**

```bash
for f in /tmp/carr-smoke/*.png; do sips -g pixelWidth -g pixelHeight "$f" 2>/dev/null | grep pixel; done
```
Expected: cada PNG 2160×2700 (1080×1350 @2x).

- [ ] **Step 4: Commit (.gitignore protege node_modules/png)**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
printf 'node_modules\n__pycache__/\n*.pyc\nslides/\n*.png\n' > plugins/dna-operacional/lib/carrossel/.gitignore
git add plugins/dna-operacional/lib/carrossel/render.mjs plugins/dna-operacional/lib/carrossel/.gitignore
git commit -m "feat(carrossel): render.mjs harness Playwright HTML→PNG

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Estender qa_lint.py com checagens novas (TDD)

**Files:**
- Modify: `lib/carrossel/qa_lint.py`
- Modify: `lib/carrossel/tests/test_qa_lint.py`

> Contexto: o `qa_lint.py` atual valida contraste WCAG, body<24px, font off-scale, object-fit:contain. Adicionar 2 checagens da geometria nova: headline accent presente (1 `.em` por headline) e padding-x consistente não é validável por HTML estático isolado — então adicionamos checagem de **exatamente 1 `<span class="em">` por `.headline`** e **handle presente no footer**.

- [ ] **Step 1: Adicionar testes falhando**

```python
# anexar a tests/test_qa_lint.py
def test_headline_sem_accent_é_flagado():
    p = os.path.join(FIX, "_tmp_noaccent.html")
    open(p,"w").write('<style>:root{--bg:#16213E;--ink:#FFF;--accent:#E94560;}'
      '.slide{background:var(--bg);color:var(--ink);}.body{font-size:24px;}'
      '.headline{font-size:76px;}</style>'
      '<div class="slide"><div class="headline">SEM ACCENT AQUI</div>'
      '<div class="body">x</div><div class="screenshot-frame"><img src="x"></div></div>')
    r = run_lint("_tmp_noaccent.html"); os.remove(p)
    assert "HEADLINE_NO_ACCENT" in [v["code"] for v in r["violations"]]

def test_headline_com_accent_ok():
    p = os.path.join(FIX, "_tmp_accent.html")
    open(p,"w").write('<style>:root{--bg:#16213E;--ink:#FFF;--accent:#E94560;}'
      '.slide{background:var(--bg);color:var(--ink);}.body{font-size:24px;}'
      '.headline{font-size:76px;}</style>'
      '<div class="slide"><div class="headline">COM <span class="em">accent</span></div>'
      '<div class="body">x</div><div class="screenshot-frame"><img src="x"></div></div>')
    r = run_lint("_tmp_accent.html"); os.remove(p)
    assert "HEADLINE_NO_ACCENT" not in [v["code"] for v in r["violations"]]
```

- [ ] **Step 2: Rodar — 2 novos falham**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_qa_lint.py -v
```
Expected: os já existentes passam, 2 novos falham.

- [ ] **Step 3: Adicionar a checagem em qa_lint.py**

Inserir em `lint()`, antes do `return`:

```python
    # headline deve ter >=1 palavra accent (<span class="em">) — regra do manifesto
    for m in re.finditer(r'class="headline[^"]*"[^>]*>(.*?)</div>', html, re.S):
        seg = m.group(1)
        if 'class="em"' not in seg:
            violations.append({"code": "HEADLINE_NO_ACCENT",
                "msg": "headline sem palavra accent (<span class='em'>)"})
```

- [ ] **Step 4: Rodar — todos passam**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_qa_lint.py -v
```
Expected: todos passam (os antigos + 2 novos).

- [ ] **Step 5: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/qa_lint.py plugins/dna-operacional/lib/carrossel/tests/test_qa_lint.py
git commit -m "feat(carrossel): qa_lint valida palavra accent na headline (TDD)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: assets-pipeline.md + forge-screen.md (guias de ativos reais)

**Files:**
- Create: `lib/carrossel/assets-pipeline.md`
- Create: `lib/carrossel/forge-screen.md`

- [ ] **Step 1: Escrever assets-pipeline.md**

````markdown
# Pipeline de Ativos Reais (carrossel)

Regra-mãe: **ativo real como referência > gerar do nada.** Origem deliberada por tipo.

| Ativo | Como obter | Ferramenta |
|---|---|---|
| **Pessoa** (criador, celebridade citada) | Baixar foto real → estilizar (pixel art) usando a foto como REFERÊNCIA | `gerar-imagem -i foto.jpg "...pixel art faithful to this person..."` |
| **Logo de produto/marca** | Baixar PNG oficial transparente (brandfetch, wikimedia, site oficial) | Playwright/curl. NUNCA desenhar. |
| **Capas de livro/produto** | Baixar imagem real (Amazon/site oficial), recortar fundo branco | Playwright/curl + Pillow |
| **Screenshot de UI** | Capturar real; se não der, forjar réplica fiel em PT-BR | Playwright MCP / `forge-screen.md` |
| **Background capa/CTA** | Foto do PRÓPRIO criador, escurecida | foto do user + overlay CSS (`.bgphoto`+`.scrim`) |

## Remoção de croma (imagens geradas com fundo verde #00FF00)
```python
from PIL import Image
im=Image.open(src).convert('RGBA'); px=im.load(); w,h=im.size
for y in range(h):
  for x in range(w):
    r,g,b,a=px[x,y]
    if g>110 and g>r+40 and g>b+40: px[x,y]=(r,g,b,0)
bb=im.getbbox(); im.crop(bb).save(dst)
```

## Pessoa → pixel art (image-to-image)
```bash
python3 ~/.claude/skills/gerar-imagem/scripts/gen.py \
  "Convert this person into a 16-bit pixel art sprite, faithful to appearance: [traços]. Arms crossed, full body, isolated on solid pure green #00FF00 background, no text." \
  -i refs/pessoa-real.jpg -a portrait -q high -o assets/pessoa-pixel-raw.png
```
Depois remover croma → `assets/pessoa-pixel.png`.

## Background do criador
- Usar foto real do user (reference/foto-<handle>.jpg). Aplicar como `.bgphoto` + `.scrim` (overlay rgba 0.55-0.72).
- Se o user não tiver foto pronta, pode gerar uma cena aspiracional, mas o ideal é a foto dele.
````

- [ ] **Step 2: Escrever forge-screen.md**

````markdown
# Forjar Tela de UI (réplica fiel em PT-BR)

Quando não dá pra capturar a UI real (login/idioma), recriar como HTML→PNG.

## Princípio
HTML que imita a UI real (cores/tipografia/layout corretos), renderizado com Playwright capturando só o elemento `.shot`. Resultado parece print real, em português.

## Exemplo — tela do Claude.ai
- Modal branco, cantos 16px, sombra suave. Accent Claude `#D97757`. Texto títulos `#1a1a1a`, secundário `#6b6b6b`. Fonte Inter.
- Campo destacado: borda accent 3px.
- Botão primário: fundo `#D97757`, texto branco.

```html
<div class="shot" style="background:#fff;border-radius:16px;padding:36px 40px;...">
  ... conteúdo em PT-BR ...
</div>
```

## Render
```bash
node -e "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1000,height:1200},deviceScaleFactor:2});
await p.goto('file://ABS/tela.html',{waitUntil:'networkidle'});await p.waitForTimeout(1200);
const el=await p.\$('.shot');await el.screenshot({path:'tela.png'});await b.close();})()"
```

## Honestidade
Réplica reproduz a FORMA da UI, não fabrica fato. Números/dados dentro: reais ou claramente ilustrativos. Nunca apresentar como print autêntico de algo que não aconteceu.
````

- [ ] **Step 3: Verificar**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
grep -c "gerar-imagem -i\|croma\|bgphoto" lib/carrossel/assets-pipeline.md
grep -c "shot\|D97757" lib/carrossel/forge-screen.md
```
Expected: ambos ≥1.

- [ ] **Step 4: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/assets-pipeline.md plugins/dna-operacional/lib/carrossel/forge-screen.md
git commit -m "feat(carrossel): guias de pipeline de ativos reais + forja de telas

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: verify.md — protocolo do loop de verificação com agente revisor

**Files:**
- Create: `lib/carrossel/verify.md`

- [ ] **Step 1: Escrever verify.md**

````markdown
# Loop de Verificação Visual (obrigatório antes de entregar)

Decisão do user: **agente revisor automático + auto-correção.** Nunca entregar sem o loop.

## Ciclo
1. **Render:** `node render.mjs <dir>` → PNGs.
2. **Lint estrutural:** `python3 qa_lint.py <dir>/NN.html` em cada slide (exit 0).
3. **Revisão visual (agente):** despachar 1 agente que faz `Read` de CADA PNG e compara com `references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md`. Reporta defeitos por slide.
4. **Auto-correção:** ajustar o `carrossel.json` ou os assets conforme os defeitos; re-gerar e re-renderizar.
5. **Repetir** até zero defeitos. Só então mostrar ao user.

## Checklist do revisor (o que procurar em cada PNG)
- [ ] Anotação/handwritten SOBRE texto ou borda de screenshot (defeito recorrente).
- [ ] Personagem/imagem sobrepondo o subtítulo ou headline.
- [ ] Palavra accent MENOR que o display (deve ser proporcional/maior).
- [ ] Ícone/logo pequeno demais.
- [ ] Screenshot/livro escondido ou cortado.
- [ ] Headline sem 1 palavra accent.
- [ ] Texto cortado nas bordas (overflow).
- [ ] Eixo de coluna inconsistente (headline/hero/footer desalinhados).
- [ ] Contraste fraco (texto ilegível sobre bg).
- [ ] Footer/handle ausente ou fora de posição.
- [ ] PT-BR correto, acentos certos.

## Prompt do agente revisor (modelo)
> "Você é revisor visual de carrossel. Leia cada PNG em <dir> (01.png..NN.png) com Read. Compare com o MANIFESTO. Para cada slide, liste defeitos do checklist (ou 'OK'). Seja implacável com sobreposição, alinhamento e proporção. Retorne JSON: [{slide, defeitos:[...]}]."

Depois o orquestrador aplica as correções (mexe no carrossel.json/assets), re-renderiza, e re-despacha o revisor até todos os slides virem 'OK'.
````

- [ ] **Step 2: Verificar**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
grep -c "agente revisor\|auto-correção\|checklist\|MANIFESTO" lib/carrossel/verify.md
```
Expected: ≥3.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/verify.md
git commit -m "feat(carrossel): protocolo do loop de verificação com agente revisor

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 10: Reescrever o command carrossel-instagram.md

**Files:**
- Modify: `commands/carrossel-instagram.md` (reescrever inteiro)

- [ ] **Step 1: Reescrever o command com o fluxo novo**

Conteúdo completo (substituir o arquivo):

````markdown
---
description: Gera carrossel viral profissional para Instagram sobre QUALQUER tema. Clona a geometria de carrosséis virais reais (headline gigante, eixo de coluna, screenshot grande), usa ativos reais (foto→pixel, logos oficiais, telas forjadas PT-BR), e roda loop de verificação visual com auto-correção. Use quando digitar "/carrossel-instagram", "criar carrossel", "post instagram", "carrossel viral", "gerar slides".
argument-hint: "[tópico|URL|notícia]"
---

Usuário invocou `/carrossel-instagram` com argumento: `$ARGUMENTS`

# /carrossel-instagram — Gerador de Carrossel Viral

Sistema destilado de 17 carrosséis virais reais (ver `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md`). NÃO improvisar layout — clonar a geometria do manifesto.

## Passo 0: Handle + voz
Ler `CLAUDE.md` → `## Handle: @<x>` (fixar em `${USER_HANDLE}`). Sem handle, perguntar 1 vez. Voz do projeto: `reference/voz-<handle>.md` se existir.

## Passo 1: Pesquisa do tema
Pesquisar `$ARGUMENTS` (WebSearch/Playwright). Levantar fatos REAIS (não inventar números). Ler o MANIFESTO + `references/carrossel-lab/hooks-frameworks.md` + `algoritmo-ig.md`.

## Passo 2: Roteiro (GATE — aprovação obrigatória)
Propor o roteiro completo em texto: para cada slide, `tipo` (cover/content/quote/cta), kicker, headline (com {palavra accent}), sub, e QUAL ativo visual (screenshot real de quê / réplica a forjar / imagem a gerar / foto do criador no bg). 7-8 slides default (ver manifesto). Capa: 1 elemento dominante + composição. CTA: comment "TOKEN".
**APRESENTAR ao user e AGUARDAR aprovação/edição antes de gerar qualquer imagem.**

## Passo 3: Pipeline de ativos reais
Após aprovação, obter cada ativo seguindo `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/assets-pipeline.md`:
- Pessoa citada → foto real → `gerar-imagem -i` pixel art fiel.
- Logos → PNG oficial baixado.
- Telas de UI → capturar real OU forjar PT-BR (`forge-screen.md`).
- Background capa/CTA → **foto do criador** (reference/foto-<handle>.jpg) escurecida.
Montar `carrossel.json` (schema em `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/schema.md`) no diretório de trabalho `./carrossel-<slug>/`, com `assets/` e `fonts/` (copiar de `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/` e fontes locais).

## Passo 4: Render
```
cp ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/base.css ./carrossel-<slug>/base.css
python3 ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/render_carrossel.py ./carrossel-<slug>/carrossel.json ./carrossel-<slug>/slides
node ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/render.mjs ./carrossel-<slug>/slides
```

## Passo 5: Loop de verificação (OBRIGATÓRIO)
Seguir `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/verify.md`: lint estrutural + agente revisor visual compara cada PNG com o MANIFESTO → auto-corrigir (mexer no carrossel.json/assets) → re-render → repetir até zero defeitos. Só então mostrar ao user.

## Passo 6: Entrega
Mostrar os PNGs finais. Criar `roteiro.md` (textos + caption + 5 hashtags). Caption segue voz do projeto.

## Regras invioláveis (do MANIFESTO)
1. Clonar geometria do manifesto — eixo de coluna 48px, headline gigante, herói 35-48% da altura.
2. Headline: Nofex + EXATAMENTE 1 palavra serif itálico accent. Crankdat só em handle/swipe/comentário.
3. Todo slide de conteúdo tem 1 prova visual real (screenshot/réplica/dado).
4. Ativo real > gerado do nada. Foto real como referência no gerar-imagem.
5. Loop de verificação antes de entregar — nunca pular.
6. PT-BR, valores em R$. Não fabricar dado/número.
7. Capa e CTA: bg = foto do criador escurecida.

---
✅ Carrossel gerado, verificado e pronto pra postar
````

- [ ] **Step 2: Verificar estrutura do command**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
head -4 commands/carrossel-instagram.md | grep -c "description:"
grep -c "MANIFESTO\|render_carrossel\|verify.md\|GATE\|carrossel.json" commands/carrossel-instagram.md
```
Expected: description presente; ≥4 referências aos arquivos do sistema.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/commands/carrossel-instagram.md
git commit -m "feat(carrossel): reescrever command como gerador viral genérico

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 11: Limpar commands do laboratório

**Files:**
- Delete: `commands/carrossel-lab-hybrid.md`, `carrossel-lab-viral.md`, `carrossel-lab-editorial.md`, `carrossel-torneio.md`

- [ ] **Step 1: Remover os 4 commands do torneio (eram experimentais)**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional/commands
git rm carrossel-lab-hybrid.md carrossel-lab-viral.md carrossel-lab-editorial.md carrossel-torneio.md
```

- [ ] **Step 2: Verificar que só sobrou o carrossel-instagram**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
ls commands/ | grep carrossel
```
Expected: só `carrossel-instagram.md`.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git commit -m "chore(carrossel): remover commands experimentais do torneio

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 12: Teste end-to-end no tema Hormozi (paridade com protótipo)

**Files:**
- Create: (temporário) `/tmp/carr-hormozi/carrossel.json`

- [ ] **Step 1: Montar carrossel.json do Hormozi a partir do protótipo**

Reusar os assets já validados em `hormozi-final/assets/`. Criar JSON refletindo os 7 slides do protótipo aprovado (cover com compo / 4 content com telas / quote / cta).

```bash
mkdir -p /tmp/carr-hormozi/assets /tmp/carr-hormozi/fonts
cp /Users/flavioahoy/orca/workspaces/etc/Nautilus/hormozi-final/assets/{hormozi-pixel.png,livros.png,claude-sun.png,bg-capa.png,tela1-criar-projeto.png,tela2-documentos.png,tela3-instrucoes.png,tela4-resultado.png} /tmp/carr-hormozi/assets/
cp /Users/flavioahoy/orca/workspaces/etc/Nautilus/hormozi-final/fonts/* /tmp/carr-hormozi/fonts/
cp /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional/lib/carrossel/base.css /tmp/carr-hormozi/base.css
ln -sfn /Users/flavioahoy/Documents/projects/propostas/node_modules /tmp/carr-hormozi/node_modules
```

Criar `/tmp/carr-hormozi/carrossel.json` (conteúdo completo):

```json
{
  "meta": {"handle":"@flavioahoy","accent":"#C4714A","tema":"escuro","total":7,
           "icon_top":"assets/claude-sun.png","bg_photo":"assets/bg-capa.png"},
  "slides": [
    {"tipo":"cover","kicker":"Sem saber programar","headline":"Clone o {Hormozi} dentro do Claude",
     "sub":"6 docs. Um prompt. Ele {destrincha seu negócio}.",
     "compo":{"left":"assets/hormozi-pixel.png","left2":"assets/livros.png","right_icon":"assets/claude-sun.png","right_label":"Claude"}},
    {"tipo":"content","kicker":"Passo 1","headline":"Crie um {projeto}","sub":"Abra um projeto novo e batize de {\"Coach de negócios Hormozi\"}.","hero":"assets/tela1-criar-projeto.png"},
    {"tipo":"content","kicker":"Passo 2","headline":"Suba os {6 docs}","sub":"A voz dele, as perguntas, os 3 livros e {os docs do seu negócio}.","hero":"assets/tela2-documentos.png"},
    {"tipo":"content","kicker":"Passo 3","headline":"Diga {como} agir","sub":"Um prompt curto mandando o Claude te meter o sarrafo igual o Hormozi.","hero":"assets/tela3-instrucoes.png"},
    {"tipo":"content","kicker":"O resultado","headline":"Agora ele {destrincha} tudo","sub":"Te diz exatamente o que arrumar, na ordem, com os frameworks dele.","hero":"assets/tela4-resultado.png"},
    {"tipo":"quote","kicker":"Por que importa","headline":"Um sócio {brutalmente} honesto. De graça.","quote":"A maioria paga R$2 mil/hora por esse tipo de conselho.","sub":"Não é sobre o Hormozi. É sobre {ter a verdade quando você precisar}."},
    {"tipo":"cta","headline_top":"Quer o passo a passo?","token":"HORMOZI","sub":"que eu te mando os {6 docs + o prompt completo}.","bg_photo":"assets/bg-capa.png"}
  ]
}
```

- [ ] **Step 2: Gerar + renderizar**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional/lib/carrossel
python3 render_carrossel.py /tmp/carr-hormozi/carrossel.json /tmp/carr-hormozi/slides
node render.mjs /tmp/carr-hormozi/slides 2>&1 | tail -3
ls /tmp/carr-hormozi/slides/*.png | wc -l
```
Expected: 7 PNGs renderizados.

- [ ] **Step 3: Lint todos**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional/lib/carrossel
for f in /tmp/carr-hormozi/slides/0*.html; do python3 qa_lint.py "$f" >/dev/null 2>&1; echo "$(basename $f) exit=$?"; done
```
Expected: todos exit=0.

- [ ] **Step 4: Verificação visual (ler os PNGs)**

Usar `Read` em `/tmp/carr-hormozi/slides/01.png`..`07.png`. Confirmar paridade com o protótipo aprovado (`hormozi-final/slides/`): capa com Hormozi+livros→Claude, headline accent, telas grandes, footer Crankdat, sem sobreposição. Se houver defeito, corrigir templates.py e re-render.

- [ ] **Step 5: Commit (se ajustes em templates.py)**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/templates.py
git commit -m "fix(carrossel): ajustes de paridade no gerador (teste Hormozi)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>" || echo "sem ajustes"
```

---

## Task 13: Teste GENÉRICO num 2º tema (prova de generalização) — INTERATIVO

> Esta task prova que a skill funciona pra qualquer tema, não só Hormozi. Requer escolha de tema (notícia Anthropic já pesquisada, ou outro). Roda o fluxo completo do command.

- [ ] **Step 1: Escolher 2º tema** (ex: "Anthropic vira IA mais valiosa do mundo" — já pesquisado, assets em `carrossel-anthropic/provas/`). Confirmar com user.

- [ ] **Step 2: Montar carrossel.json do 2º tema** com seus próprios assets (manchete real anthropic, tweet Mosseri PT, etc — já existem em `carrossel-anthropic/`).

- [ ] **Step 3: Gerar + renderizar + loop de verificação** completo via os scripts da skill.

- [ ] **Step 4: Verificação visual** — ler PNGs, confirmar que o MESMO gerador produziu um carrossel coeso de tema totalmente diferente. Isso valida a generalização.

- [ ] **Step 5: Veredito do user** sobre o 2º carrossel.

---

## Self-Review (preenchido)

**Cobertura do spec:**
- Gerador parametrizado (qualquer tema) → Tasks 3,4,5 (templates + render_carrossel) ✓
- Geometria do manifesto → Task 1 (manifesto como reference) + templates clonam o protótipo ✓
- 3 templates (cover/content/cta) + quote → Task 4 ✓
- Pipeline de ativos reais → Task 8 (assets-pipeline + forge-screen) ✓
- Loop de verificação c/ agente revisor + auto-correção → Task 9 (verify.md) + aplicado em 12/13 ✓
- Fonts Nofex+serif accent, Crankdat handle → base.css (Task 1) + templates (Task 4) ✓
- Eixo 48px → base.css `--pad-x` ✓
- Fluxo com gate (roteiro→aprova→render) → Task 10 command Passo 2 GATE ✓
- Provar genérico (2º tema) → Task 13 ✓
- qa_lint estende → Task 7 ✓

**Placeholders:** nenhum TODO/TBD no conteúdo de implementação. Tasks 12/13 dependem de assets já existentes/input do user por design (marcadas interativas).

**Consistência de nomes:** `slide(s, idx, total, meta)`, `accent()`, `footer(handle, swipe)`, `cover/content/quote/cta`, `carrossel.json`, `render_carrossel.py`, `render.mjs`, `qa_lint.py` — usados consistentes entre Tasks 3-12. Classes CSS (`.headline .em`, `.footer .handle`, `.swipe`, `.cta-stack`, `.hero .shot`) batem entre base.css (Task 1) e templates (Task 4).
