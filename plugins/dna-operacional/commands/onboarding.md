---
description: Onboarding completo de cliente novo — cria grupo WhatsApp (cliente + Bruna + equipe), Shared Drive com pastas padrão, Google Form de briefing, NotebookLM nomeado, e dispara mensagem de boas-vindas pela Bruna com links. Use quando digitar "/onboarding", "novo cliente", "iniciar cliente <nome>", "kickoff cliente".
argument-hint: "[nome do cliente]"
---

Usuário invocou `/onboarding $ARGUMENTS`.

Wrapper fino pra skill `onboarding-cliente` bundled em `${CLAUDE_PLUGIN_ROOT}/skills/onboarding-cliente/SKILL.md`.

## Resolução da skill

1. Bundled (preferencial): `${CLAUDE_PLUGIN_ROOT}/skills/onboarding-cliente/SKILL.md`
2. Sem fallback global (skill é nova, exclusiva do plugin).

Se ausente: abortar com `⚠ Skill onboarding-cliente não encontrada. Reinstale o plugin DNA Operacional.`

## Passo 1 — Pré-checks

Antes de invocar a skill, validar config no CLAUDE.md do projeto. Ver Etapa 0 do SKILL.md.

Se config faltando, imprimir instrução amigável e abortar.

## Passo 2 — Invocar skill

Usar **Skill tool** com `skill: "onboarding-cliente"` passando `$ARGUMENTS` (nome do cliente, se veio).

Se vazio, skill faz a coleta conversacional completa.

## Passo 3 — Output

Skill retorna o bloco final formatado. Wrapper só passa-pra-frente.
