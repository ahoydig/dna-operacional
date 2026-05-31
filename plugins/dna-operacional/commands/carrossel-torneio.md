---
description: Roda um torneio de carrosséis — controle atual + 3 teses do lab — sobre a mesma notícia, julga cego por 5 dimensões e deixa o user escolher o vencedor. Uso: avaliação, não produção.
argument-hint: "<URL ou tema da notícia>"
---

Usuário invocou `/carrossel-torneio` com argumento: `$ARGUMENTS`

## Passo 0: Brief normalizado

1. Resolver handle (`CLAUDE.md` → `## Handle:`).
2. A partir de `$ARGUMENTS` (URL/tema), pesquisar e montar **um brief único**: objetivo, público, fatos-chave, formato (default 4:5). Este brief é entregue **idêntico** aos 4 motores.
3. Criar diretório do torneio: `./torneio-<slug>/` com subpastas `motor-controle/`, `motor-hybrid/`, `motor-viral/`, `motor-editorial/`.

## Passo 1: Rodar os 4 motores

Para cada motor, gerar o carrossel completo no seu diretório, com o MESMO brief:
- **Controle:** seguir `${CLAUDE_PLUGIN_ROOT}/commands/carrossel-instagram.md` (sem modificação).
- **Hybrid:** seguir `${CLAUDE_PLUGIN_ROOT}/commands/carrossel-lab-hybrid.md`.
- **Viral:** seguir `${CLAUDE_PLUGIN_ROOT}/commands/carrossel-lab-viral.md`.
- **Editorial:** seguir `${CLAUDE_PLUGIN_ROOT}/commands/carrossel-lab-editorial.md`.

Mesmo formato, mesma config de fonte, mesmo piso. Controle usa suas próprias references; teses usam `carrossel-lab/`.

## Passo 2: Anonimizar (juiz cego)

1. Gerar um embaralhamento dos 4 motores → rótulos neutros `competidor-1..4`. **Não usar a ordem do Passo 1.**
2. Copiar os PNGs de cada `motor-*/` para `./torneio-<slug>/competidor-N/` conforme o embaralhamento.
3. Salvar o mapping motor→competidor em `./torneio-<slug>/.mapping.json` (NÃO mostrar ainda).

## Passo 3: Juiz cego

Avaliar APENAS os `competidor-N/` (sem saber qual motor é qual). Para cada competidor, pontuar **0–10 em cada uma das 5 dimensões**, com justificativa, **slide-a-slide E carrossel inteiro**:
1. Força viral / retenção (usar critérios de `algoritmo-ig.md`).
2. Copy / hook / narrativa (`hooks-frameworks.md`).
3. Design / impacto visual (`design-premium.md`).
4. Consistência / menos retrabalho (quantas violações o QA lint pegou; quão coeso).
5. Screenshots reais ou réplica fiel (qualidade/credibilidade do visual de prova).

Pesos default iguais (ajustáveis pelo user antes do julgamento). Produzir ranking.

## Passo 4: Montagem e revelação

1. Montar comparação lado-a-lado (capa de cada competidor + grade completa).
2. Apresentar a tabela de notas + justificativas + ranking.
3. **Só então** revelar o `.mapping.json` (qual competidor era qual motor).
4. Pedir o **veredito final do user** (juiz dá nota; decisão é humana).

## Passo 5: Aprendizado

Registrar o que ganhou e por quê em `learnings/` do projeto. **Não** promover nada a `carrossel-instagram` v2 sem aceite explícito do user (fora do escopo desta rodada).

---

✅ Torneio rodado — 4 carrosséis, juiz cego, veredito do user.
