---
description: Gera carrossel viral pra Instagram sobre QUALQUER tema. Clona a geometria de virais reais (eixo de coluna, headline gigante, herói grande), usa ativos reais (não inventa) e fecha com loop de verificação automático (lint + agente revisor + auto-correção). Use quando digitar "/carrossel-instagram", "criar carrossel", "post instagram", "carrossel viral", "gerar slides".
argument-hint: "[tópico|URL|notícia]"
---

Usuário invocou `/carrossel-instagram` com argumento: `$ARGUMENTS`

# /carrossel-instagram — Gerador de Carrossel Viral (genérico)

> Gera um carrossel pronto pra postar (PNG por slide + roteiro.md com caption e hashtags), clonando a geometria de carrosséis virais reais. Tema é livre — vem de `$ARGUMENTS` (ideia, URL, notícia). Os ativos são **reais** (fotos, logos oficiais, telas capturadas/forjadas), nunca inventados. A verificação não é opcional: é um loop automático de lint + agente revisor + auto-correção até zero defeitos.

**Pipeline canônico** (lib em `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/`):
- Geometria: `base.css` (classes `.slide .headline .em .sub .kicker .hero .shot .quote .footer .handle .swipe .cta-stack .ghost .snum .bgphoto .scrim .note .center .spacer`; vars `--pad-x:64px`, `--accent:#C4714A`).
- Roteiro: `carrossel.json` (formato em `schema.md`).
- Render: `render_carrossel.py` (json → HTML) + `render.mjs` (HTML → PNG via Playwright).
- QA: `qa_lint.py`.

---

## Passo 0 — Handle e voz

1. Ler `CLAUDE.md` do projeto atual procurando `## Handle: @<x>`. Fixar em `${HANDLE}` pra toda a sessão.
   - Sem handle → perguntar **uma vez** ("Qual handle do Instagram assina este carrossel?"), usar a resposta e sugerir gravar em `CLAUDE.md` depois.
2. Se existir `reference/voz-${HANDLE}.md`, ler o frontmatter (tom, formalidade, energia, vícios a evitar). Calibra a copy do roteiro e a caption. Sem arquivo de voz → tom "amigo que descobriu algo bom" (não guru, não professor).
3. **Ativos da marca — PERGUNTAR, nunca assumir nem salvar.** Esta skill é genérica e multi-pessoa. Quando chegar a hora dos ativos (Passo 3), pedir ao user:
   - uma **foto dele** (vira o `bg_photo` escurecido da capa/CTA — de lado, lifestyle, não encarando a câmera fica melhor);
   - se a marca tiver um **mascote/personagem recorrente**, a imagem de **referência** dele (vira herói da capa, gerado fiel via `gerar-imagem -i ref` — mesmo estilo, não infantilizar).
   Não guardar foto/mascote de ninguém no repo — usar só na sessão. (Se o projeto já tiver um asset de marca documentado no `CLAUDE.md`, usar esse.)

---

## Passo 1 — Pesquisa do tema (fatos REAIS)

1. Interpretar `$ARGUMENTS`:
   - URL / notícia / post → abrir via Playwright (ou WebFetch) e extrair os pontos-chave reais.
   - Ideia/tema solto → `WebSearch` pra reunir fatos, números, exemplos reais e ângulos.
2. Ler os mapas de viralização:
   - `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md` — blueprint de geometria (3 escolas, grid, zonas verticais, tipografia, elemento herói, templates A/B/C). **É o contrato visual desta skill.**
   - `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/hooks-frameworks.md` — fórmulas de hook e arco narrativo.
   - `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/algoritmo-ig.md` — alavancas de alcance (save/comment, retenção, swipe).

**Nunca fabricar** dado, número, métrica, citação, link ou nome. Se não achar a fonte, dizer que não achou — não inventar.

---

## Passo 2 — GATE: roteiro completo em texto (aguardar aprovação)

Propor o **roteiro completo em texto** — sem gerar uma única imagem ainda. **7-8 slides.** Cada slide descrito assim:

- **tipo:** `cover` | `content` | `quote` | `cta`
- **kicker:** label curto (ex: "Passo 1", "O problema")
- **headline:** com `{palavra accent}` (exatamente 1 trecho entre chaves — vira serif itálico colorido)
- **sub:** subtítulo / linha de impacto
- **ativo visual:** QUAL prova visual real vai entrar (foto tratada, logo oficial, tela capturada/forjada, gráfico)

Arco recomendado (do MANIFESTO, templates A/B/C):
- **Slide 1 (cover):** hook mais agressivo, promessa quantificada. bg = **foto do criador** escurecida. **Herói visual:** escolher do **repertório** (`forge-screen.md` §8) — perfil viralizando, pasta secreta/censurada, telas do produto, gráfico de crescimento, mascote da marca. **Apresentar 3-5 opções concretas de herói ao user e deixar ele escolher — nunca estreitar num device só** (ex: só mascote). A capa pode ter **até 2 imagens** (herói `figure` + 2ª prova `aux`) pra não ficar vazia. **Background da capa/CTA:** ofereça **opções/sugestões** de cenário e tratamento (ângulo, troca de roupa, mais/menos escuro via `scrim_top`/`scrim_bot`) e **pergunte como o user quer** — nunca reutilizar a foto no automático. Se ele quiser variar, gerar a partir da foto dele (`gerar-imagem -i`).
- **Slides 2-6/7 (content/quote):** um passo/ideia por slide, 1 prova visual real cada.
- **Último (cta):** headline maior do carrossel + `Comenta "TOKEN"`. bg = **foto do criador** (bookend, fecha o loop).

**Apresentar o roteiro e AGUARDAR aprovação explícita do user antes de avançar.** Não gerar imagem, não montar `carrossel.json`, não renderizar nada antes do "ok".

---

## Passo 3 — Pipeline de ativos + montar carrossel.json

> Só depois do roteiro aprovado.

1. **Ativos** — seguir `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/assets-pipeline.md` (foto real → pixel via `gerar-imagem`, remoção de croma, logos oficiais) e `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/forge-screen.md` (telas forjadas em PT-BR via HTML→PNG). Regra-mãe: **ativo real > gerado do nada**. bg da capa/CTA = **foto do criador**.
   - **Herói da capa:** PNG transparente no campo `figure` (recortar croma se gerado). Se cobrir texto, deslocar com `figure_x`; o vazio que sobrar do outro lado vira a 2ª imagem `aux` (ver `schema.md`).
   - **Forjar tela de SO/app:** sempre na **versão ATUAL** (`forge-screen.md` §6 — ex: pasta macOS Big Sur flat, não o emoji velho); pedir um print de referência se estiver em dúvida do design atual.
   - **Censura "secreto":** mosaico **pixelado**, não tarja preta chapada (`forge-screen.md` §7).
2. **Estrutura de trabalho** — criar `./carrossel-<slug>/` com:
   - `assets/` — todos os ativos (fotos, logos, telas, gráficos)
   - `fonts/` — copiar `Nofex.ttf`, `Crankdat-Bold.ttf`, `Crankdat-Regular.ttf` (de `~/Library/Fonts/`, fallback workdir/fonts) — `Nofex-Outline.ttf` não é registrada pelo render, não copiar
   - `carrossel.json` — o roteiro (formato em `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/schema.md`)
3. **Montar `carrossel.json`** seguindo o schema:
   - `meta`: `handle` (= `${HANDLE}`), `accent` (default `#C4714A`), `tema` (`escuro`), `total`, `bg_photo` (foto do criador), `icon_top` opcional.
   - `slides[]`: tipos `cover`/`content`/`quote`/`cta`. `{x}` = palavra accent (exatamente 1 por headline). `hero` (content) = caminho da tela/prova. `compo` (cover) = composição. Paths relativos `assets/...` (o gerador prefixa `../` sozinho).

---

## Passo 4 — Render

No diretório `./carrossel-<slug>/`:

```bash
cp ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/base.css ./base.css
# render.mjs precisa rodar DE DENTRO do workdir (ESM resolve playwright a partir da pasta do script,
# não do cwd) — por isso copiamos ele pra cá, junto do node_modules linkado:
cp ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/render.mjs ./render.mjs
ln -sfn /Users/flavioahoy/Documents/projects/propostas/node_modules ./node_modules   # se não houver playwright local
python3 ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/render_carrossel.py carrossel.json slides
node ./render.mjs slides
```

- `render_carrossel.py` injeta `@import` Google Fonts + `@font-face` Nofex/Crankdat e linka `../base.css`; escreve `slides/NN.html`.
- `render.mjs` usa Playwright (viewport 1080×1350 @2x, captura `clip` fixo) e escreve `slides/NN.png`.
- **Importante:** o `render.mjs` e o `node_modules` (com Playwright) precisam estar NO workdir — rodar o script direto de `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/` falha com `ERR_MODULE_NOT_FOUND: playwright`.

---

## Passo 4.5 — Playground de ajuste fino (recomendado)

Antes do loop final, oferecer o playground pro user calibrar tamanho/posição de cada elemento ao vivo (ver `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/render.md` § Playground):

```bash
cp ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/playground.html ./playground.html
python3 -m http.server 8777 &   # no workdir
open http://localhost:8777/playground.html
```

O user mexe nos sliders (headline/sub/quote/hero, figure/aux da capa, scrim, cor do accent), clica **Copiar carrossel.json**, cola de volta → re-render. Usar pra validar **distribuição e tamanho** (respiro headline↔sub, heróis enchendo o slide).

---

## Passo 5 — Loop de verificação (OBRIGATÓRIO, nunca pular)

Seguir `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/verify.md`. Em resumo, o loop:

1. **Lint determinístico** — `python3 ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/qa_lint.py slides/NN.html` em cada slide. Lê CSS de `<style>` inline, `base.css` linkado e atributos `style=`. Valida contraste WCAG (`--text`/`--bg`, `--accent`/`--bg`), `BODY_TOO_SMALL`, `HEADLINE_TOO_SMALL` (< 76px), `OBJECTFIT_CONTAIN_BG`, `HEADLINE_NO_ACCENT`. Exit ≠ 0 = violação.
2. **Agente revisor automático** — `Read` cada PNG e checar o subjetivo que o lint não pega: hierarquia, respiro, palavra órfã, acentos PT-BR corretos, prova visual presente em todo slide de conteúdo, headline com exatamente 1 palavra accent, Crankdat só no handle/swipe, bg foto do criador na capa/CTA.
3. **Auto-correção** — corrigir HTML/json/ativo e **re-renderizar**. Repetir lint + revisor **até zero defeitos**. Não mostrar ao user antes de zerar.

---

## Passo 6 — Entrega

1. Mostrar os PNGs finais (`slides/NN.png`).
2. Criar `roteiro.md` em `./carrossel-<slug>/` com: textos de cada slide, **caption** e **5 hashtags** — tudo na voz do projeto (`reference/voz-${HANDLE}.md` se existir).

---

## Regras invioláveis (do MANIFESTO)

1. **Clonar geometria** — eixo de coluna (`--pad-x:64px`), headline gigante, elemento herói grande. Não reinventar layout; usar `base.css` + `templates.py`.
2. **Headline:** Nofex + **exatamente 1 palavra** serif itálico accent (`{x}` → `.em`). **Crankdat só no handle e no swipe.**
3. **Todo slide de conteúdo com ≥1 prova visual real.** Slide só-texto é proibido.
4. **Ativo real > gerado do nada.** Foto, logo oficial, tela capturada/forjada antes de qualquer coisa inventada.
5. **Loop de verificação nunca pula** (Passo 5).
6. **PT-BR e R$** — público brasileiro, valores em reais, nunca dólar no texto. **Não fabricar dado.**
7. **Capa e CTA: bg = foto do criador** (escurecida via `.bgphoto` + `.scrim`).
8. **GATE do Passo 2** — nenhuma imagem antes da aprovação do roteiro.
9. **Capa com herói do repertório (e até 2ª imagem).** Escolher o herói do repertório (`forge-screen.md` §8) e **apresentar opções ao user — nunca estreitar num device só**. Se o herói sair do centro pra largar o texto (`figure_x`), preencher o vazio com `aux` (perguntando qual 2ª imagem). **Capa sem buraco.**
10. **Forjar SO/app sempre na versão ATUAL** — nunca emoji/asset de sistema velho; "secreto" = censura em **mosaico pixelado**.
11. **Distribuição e tamanho — encher o slide.** Slides bem distribuídos, com **respiro entre headline e sub** (não amontoar). Headlines de conteúdo costumam ir **grandes** (100-140px), quote **grande** (80-100px), e o **hero enche o slide** — imagem pequena perdida no meio é defeito. Ajustar tamanho de cada elemento (`hsize`/`sub_size`/`quote_size`/`hero_w`) e a escuridão do bg (`scrim_top`/`scrim_bot`) por slide. Telas forjadas devem nascer **altas o suficiente** pra encher (mais conteúdo na tela), não curtas.
12. **Playground antes do loop final.** Depois de renderizar, oferecer o **playground** (`lib/carrossel/playground.html`, ver `render.md`) pro user **ajustar cada elemento ao vivo** e copiar o JSON de volta. É a forma de validar distribuição/tamanho sem ping-pong.

---

## Reference / lib

| Arquivo | Quando |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md` | Passo 1 — geometria |
| `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/hooks-frameworks.md` | Passo 1 — hooks |
| `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/algoritmo-ig.md` | Passo 1 — alcance |
| `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/schema.md` | Passo 3 — carrossel.json |
| `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/assets-pipeline.md` | Passo 3 — ativos |
| `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/forge-screen.md` | Passo 3 — telas PT-BR |
| `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/render_carrossel.py` · `render.mjs` · `base.css` | Passo 4 — render |
| `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/verify.md` · `qa_lint.py` | Passo 5 — verificação |

---

✅ Carrossel viral renderizado, verificado e pronto pra postar

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /ideias-conteudo  — próximo carrossel da série
  2. /roteiro-viral    — virar isso em Reel

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
