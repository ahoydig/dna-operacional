---
description: "Tese Editorial Premium do carrossel-lab: escala modular, contraste WCAG, grid 8pt, motifs persistentes, best-of-N de direção de arte. Cara de revista. Uso: torneio de carrossel."
argument-hint: "[tópico|URL|path-de-briefing?]"
---

Usuário invocou `/carrossel-lab-editorial` com argumento: `$ARGUMENTS`

## Pre-check — DNA Mode (low-cost)

Ler `CLAUDE.md` → `## DNA Mode: <x>` (default: full). O torneio sempre roda em **full** (lowcost não se aplica ao lab). Se lowcost, avisar que o lab ignora e segue full.

## Passo 0: Resolver Handle

Ler `CLAUDE.md` → `## Handle: @<x>`. Fixar em `${USER_HANDLE}`. Sem handle: perguntar uma vez via `AskUserQuestion`.

## Passo 1: Research-first

Antes de qualquer copy: pesquisar o tema/notícia (Playwright/WebSearch) e ler:
- `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/algoritmo-ig.md`
- `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/hooks-frameworks.md`
- `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/design-premium.md`
- `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/design-contract.md`

## Passo 2: Briefing

Coletar: objetivo, template (`references/carrossel-lab/templates.md`), formato (default 4:5), handle (Passo 0).

## Passo 3: Render

Para cada slide, seguir `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/render.md` (inclui gate de QA lint). Screenshots via `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/screenshot-engine.md`.

## Passo 4: Entrega

Salvar PNGs + `roteiro.md` (textos, caption, 5 hashtags, caminhos). Aplicar `/humanizer` na copy (delegação, não cascata).

## Motor — Editorial Premium

Aposta em design top-tier (base: `design-premium.md` + `design-contract.md`).

### Disciplina visual rígida
- Escala modular 1.333, contraste WCAG, grid 8pt — todos validados pelo QA lint (sem exceção).
- Espaço negativo intencional; curva texto→visual ao longo da sequência.

### Motifs persistentes (todos os slides)
- Numeração `01/07`, barra de progresso própria, handle no rodapé, label de seção — mesmos coords/estilo (componentes do `base.css`).

### Best-of-N de direção de arte
- Gerar **3 composições/layouts** distintos para o slide 1 (não de copy — de arte).
- Renderizar preview real das 3 (render harness).
- Juiz interno escolhe a mais "revista premium". User aprova.

### Par tipográfico
- Display + sans dentro do contrato. Default Nofex/Inter; pode propor par editorial (ex: Playfair+DM Sans) **se as fontes estiverem disponíveis** (senão fallback Google Fonts). Nunca 3ª família fora dos papéis.
