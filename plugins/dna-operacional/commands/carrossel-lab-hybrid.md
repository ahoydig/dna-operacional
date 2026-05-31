---
description: "Tese Hybrid Director do carrossel-lab: research-first + best-of-N só na capa e na direção visual + pipeline de especialistas. Uso: torneio de carrossel, não produção diária."
argument-hint: "[tópico|URL|path-de-briefing?]"
---

Usuário invocou `/carrossel-lab-hybrid` com argumento: `$ARGUMENTS`

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

## Motor — Hybrid Director

Pareto: capa/hook e direção visual decidem o carrossel. Best-of-N só neles.

### Gate A — Best-of-N de capa
1. Gerar **5 hooks** cobrindo padrões distintos de `hooks-frameworks.md`.
2. Juiz interno escolhe por *information gap delimitado* (Loewenstein). Justificar.
3. Slide 2 = confirmador de swipe (restate + 1º loop).

### Gate B — Best-of-N de direção visual
1. Propor **3 direções** (paleta de `palettes.md` + efeito de `headline-effects.md` + composição), ancoradas no moodboard (`visual-research.md`).
2. Renderizar **preview real do slide 1** das 3 (via render harness).
3. Juiz interno escolhe por impacto. Apresentar ao user pra aprovação.

### Pipeline de especialistas (resto)
- Arquiteto de narrativa: arco explícito (1 de PAS/AIDA/BAB/listicle/story), open loop entre slides.
- Diretor de arte: aplica direção aprovada a todos os slides (motifs persistentes).
- Render + QA: harness + lint por slide.
