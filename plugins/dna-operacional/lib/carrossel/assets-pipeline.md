# Pipeline de Ativos Reais do Carrossel

Como nascem os PNGs que vão em `assets/` — o que cada slot do roteiro
(`carrossel.json`) consome e de onde vem. Complementa `screenshot-engine.md`
(que cobre só o herói/screenshot); este guia cobre TODOS os tipos de ativo.

> **Regra-mãe:** **ativo real como referência > gerar do nada.** Toda imagem
> que sai de IA generativa parte de uma foto/logo/print real via `-i` (image-to-image).
> Gerar sem referência só pra elemento decorativo abstrato (textura, voxel mascote)
> — nunca pra pessoa, logo, produto ou tela que exista no mundo.

Verificação = **agente revisor automático + auto-correção** (decisão do user). Cada
PNG gerado é lido de volta (`Read`), o revisor aponta defeito (croma residual, clipping,
logo errado, tela em inglês) e corrige em loop até passar — não pergunta ao user a cada passo.

---

## 1. Tabela de origem por tipo de ativo

Mapeia cada slot do roteiro pro processo de produção. Coluna "Slot" = onde entra no
`carrossel.json` (ver `schema.md`).

| Ativo | Slot no JSON | Origem | Processo |
|---|---|---|---|
| **Pessoa / personagem** (criador, cliente, autor citado) | `compo.left`, `compo.left2` | **Foto real → pixel via gerar-imagem `-i`** | Pega a foto real da pessoa, passa como `-i foto.jpg`, prompt pede recorte pixel-art/cut-out fundo croma. Remove croma via Pillow. |
| **Logo de marca** (do projeto, ou citada: Instagram, GitHub, app do cliente…) | `compo.right_icon`, `meta.icon_top` | **PNG oficial baixado** | Baixar o PNG/SVG oficial da marca (press kit / brand page). NUNCA recriar à mão nem gerar por IA — vira logo errado. O logo de topo é o **da marca do projeto** (vem do `CLAUDE.md` ou perguntado ao user — Passo 0). |
| **Capa de livro / produto físico** | `compo.left`, `compo.left2`, `hero` | **Imagem real recortada** | Capa real do livro/produto (loja/press), recortar fundo (Pillow ou croma). Sobrepor em leque na composição da capa. Não gerar capa fake. |
| **Screenshot de UI** (Claude.ai, terminal, dashboard, app) | `hero` | **Capturar real OU forjar tela PT-BR** | Ordem do `screenshot-engine.md`: captura real > réplica fiel em HTML→PNG > pedir ao user. Tela forjada = HTML em PT-BR renderizado como PNG, `data-replica="true"`. |
| **Background da capa / CTA** | `meta.bg_photo`, `slides[].bg_photo` | **Foto do criador escurecida** | Foto real do criador (setup, rua, ambiente). Escurecer via `.bgphoto`+`.scrim` (já no `base.css` — não queimar a foto no Pillow, o scrim faz isso em CSS). |
| **Ícone de topo** (logo da marca do projeto) | `meta.icon_top` | **PNG oficial baixado** | Mesmo que logo. PNG oficial da marca, fundo transparente. (Ex.: asterisco Claude, logo do GitHub, marca do cliente.) |
| **Mascote / voxel / textura abstrata** | qualquer | **Gerar por IA (sem `-i`)** | Único caso de gerar do nada — não existe no mundo. Cor = `--accent`. PNG transparente. Ver MANIFESTO §6. |

**Por que `-i` quase sempre:** o gpt-image-2 inventa rosto, marca e detalhe quando
gera do zero. Com a foto real como referência ele *transforma* em vez de *fabricar* —
preserva a identidade da pessoa/produto e respeita a regra "não fabrique".

---

## 2. Comando exato — gerar-imagem com referência (`-i`)

Pessoa/personagem a partir de foto real, em pixel-art recortado pra composição de capa:

```bash
python3 ~/.claude/skills/gerar-imagem/scripts/gen.py \
  "pixel-art cut-out of this person, 8-bit style, vibrant, isolated on a solid #00FF00 chroma green background, full body, no shadow, game asset style" \
  -i foto.jpg \
  -o assets/pessoa-raw.png
```

- `-i foto.jpg` — a foto real (jpg/png/webp/gif). Repetível (várias referências).
- Pede **fundo croma `#00FF00`** sólido no prompt → o recorte (próxima seção) fica limpo.
- `-q high` se a composição for grande na capa; default `medium` pro resto.
- Sem `OPENAI_API_KEY` — usa o OAuth do Codex CLI (cobra nos limites do ChatGPT/Codex).

Pra produto/livro a partir da imagem real, mesmo padrão trocando o prompt
("clean cut-out of this book cover, isolated on #00FF00 chroma green, front-facing, sharp edges").

---

## 3. Snippet — remover croma verde via Pillow

Depois de gerar com fundo `#00FF00`, recortar o croma pra transparente e cortar a
moldura vazia (`getbbox`). Resultado: PNG transparente pronto pra `compo.left`/`right_icon`.

```python
from PIL import Image

def remove_chroma(in_path, out_path, key=(0, 255, 0), tol=60):
    """#00FF00 -> transparente. tol = tolerância por canal (anti-aliasing das bordas)."""
    img = Image.open(in_path).convert("RGBA")
    px = img.load()
    w, h = img.size
    kr, kg, kb = key
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            # verde dominante e perto do croma -> apaga
            if abs(r - kr) <= tol and abs(g - kg) <= tol and abs(b - kb) <= tol and g > r and g > b:
                px[x, y] = (r, g, b, 0)
    bbox = img.getbbox()          # caixa do conteúdo não-transparente
    if bbox:
        img = img.crop(bbox)      # remove a moldura vazia ao redor
    img.save(out_path)

remove_chroma("assets/pessoa-raw.png", "assets/pessoa.png")
```

- `tol` controla o quanto da franja verde (anti-alias) some. Subir se sobrar halo verde
  na borda do recorte; descer se estiver comendo verde legítimo do sujeito.
- `getbbox` + `crop` deixa o sujeito colado na borda do PNG → escala previsível na composição.
- **Verificar:** `Read` no PNG final. Se sobrar pixel verde, o revisor sobe `tol` e roda de novo.

---

## 4. Telas forjadas (screenshot UI em PT-BR)

Quando não dá pra capturar a tela real (ou ela está em inglês), forja em HTML→PNG:

1. Recriar o componente real em HTML/CSS com cara de verdade, **texto em PT-BR**.
2. Marcar `data-replica="true"` no root (rastreabilidade — não é print autêntico).
3. Renderizar como PNG (mesmo harness do slide, ver §5) e usar como `hero`.
4. **Honestidade (regra dura):** réplica reproduz a *forma*, não fabrica *fato*. Número/
   citação dentro da tela ou vem da fonte real, ou é claramente ilustrativo. Nunca
   apresentar réplica como print autêntico. (Detalhe em `screenshot-engine.md`.)

---

## 5. Onde os ativos encaixam no render

Fluxo completo (ver `render.md` pro harness determinístico):

1. Ativos vivem em `<workdir>/assets/*.png`. O roteiro referencia `assets/x.png`
   (relativo ao workdir). `templates.asset()` prefixa `../` automático — o HTML vive
   em `slides/` e sobe um nível.
2. Background da capa/CTA: setar `meta.bg_photo` (capa) ou `slides[].bg_photo` (CTA).
   `templates._bg()` injeta `<img class="bgphoto">` + `<div class="scrim">` —
   o escurecimento é **CSS** (`.scrim` no `base.css`), não no Pillow. Foto entra clara.
3. Fontes locais (`Nofex.ttf`, `Crankdat-Bold.ttf`, `Crankdat-Regular.ttf`) de
   `~/Library/Fonts` → copiar pra `<workdir>/fonts/`. (`Nofex-Outline.ttf` não é
   registrada via `@font-face` pelo render — não copiar.)
   `render_carrossel.py` injeta os `@font-face` apontando pra `../fonts/`.
4. Gerar HTML: `python3 render_carrossel.py <carrossel.json> <out_dir>`.
5. QA lint **antes** de renderizar PNG:
   `python3 qa_lint.py <slide.html>` (exit≠0 = corrigir e repetir).
6. Render PNG: `node render.mjs <dir>` (Playwright 1080×1350 @2x, captura por `clip`).
   Precisa `node_modules` com playwright — linkar de
   `/Users/flavioahoy/Documents/projects/propostas/node_modules`.
7. Loop revisor: `Read` cada PNG, auto-corrigir defeito de ativo (croma residual,
   logo errado, tela em inglês, clipping), repetir até passar.

---

## 6. Checklist de fidelidade de ativo

- [ ] Toda pessoa/produto saiu de foto/imagem real via `-i` (nunca gerado do nada).
- [ ] Todo logo é o PNG oficial baixado (não recriado, não gerado por IA).
- [ ] Croma verde 100% removido (sem halo na borda — checar `Read` no PNG).
- [ ] `getbbox`+`crop` aplicado → sujeito colado na borda, escala previsível.
- [ ] Background da capa/CTA = foto do criador, escurecida por `.scrim` (CSS), não queimada no Pillow.
- [ ] Screenshot UI = captura real; se forjado, `data-replica="true"` + PT-BR + fato real ou ilustrativo.
- [ ] Logo de topo = PNG oficial da marca do projeto (baixado, não recriado/gerado por IA — ver MANIFESTO §7).
- [ ] PNG transparente (fundo zerado) pra todo cut-out que entra em `compo`.
- [ ] Revisor automático leu cada PNG e o slide final antes de declarar pronto.
