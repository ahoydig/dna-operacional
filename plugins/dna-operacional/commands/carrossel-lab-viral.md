---
description: "Tese Viral Engineer do carrossel-lab: capa dupla (second-chance), engenharia de send/save, open loops obrigatórios, best-of-N agressivo de hook. Uso: torneio de carrossel."
argument-hint: "[tópico|URL|path-de-briefing?]"
---

Usuário invocou `/carrossel-lab-viral` com argumento: `$ARGUMENTS`

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

## Motor — Viral Engineer

Aposta em alcance/retenção (base: `algoritmo-ig.md`).

### Capa dupla autônoma
- **Slide 1 E slide 2** são ambos capa completa e independente (o IG re-entra pelo slide 2). Cada um para o scroll sozinho.

### Best-of-N agressivo de hook
- Gerar **8–12 hooks** (todos os padrões de `hooks-frameworks.md`).
- Lint de retenção: reprovar hook genérico, body >30 palavras, jargão, frase cortada, slide sem função.
- Forçar especificidade numérica nos hooks de resultado.

### Engenharia de send/save
- Slide final pede **save com motivo** ("salva pra usar depois") **e** dá **razão de DM** ("manda pra quem precisa") — sends movem alcance unconnected.
- Sugerir música (elegibilidade aba Reels).

### Open loop obrigatório
- Cada slide termina abrindo loop pro próximo (slippery slide). Slide que se fecha sozinho é **reprovado e reescrito**.
- Uma ideia por slide + mini-headline "road sign" 4–7 palavras.

### Arco explícito
- Escolher 1 (PAS/AIDA/BAB/listicle-escalada/story) antes de redigir; reprovar carrossel sem progressão.
