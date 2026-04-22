# Impeccable Research — Integration Decision

**Task:** 4.1 do plano `docs/team-powers/plans/2026-04-21-dna-v0.2-client-delivery-csv-setup-modes.md`
**Data:** 2026-04-21
**Branch:** `feat/v0.2-client-delivery`
**Repo investigado:** https://github.com/pbakaus/impeccable (Paul Bakaus, Apache 2.0)

---

## 1. Resumo (o que é Impeccable)

Impeccable é uma **skill + toolkit de design** criada pelo Paul Bakaus que estende a `frontend-design` original da Anthropic com expertise mais profunda e controle mais granular. Seu objetivo é combater o viés de LLMs de produzir UI genérica (Inter, gradientes roxos, cards aninhados, baixo contraste), oferecendo **guidance explícito do que fazer E do que evitar** em 7 domínios (tipografia, cor/contraste, espacial, motion, interaction, responsive, UX writing).

Além da skill, vem com **18 comandos operacionais** (`/audit`, `/critique`, `/polish`, `/animate`, `/colorize`, `/harden`, entre outros) e — o diferencial mais forte — um **CLI standalone** (`npx impeccable detect`) que analisa HTML/CSS/URL via regex e flaga 24 issues de qualidade de design de forma determinística, sem depender do LLM. Instalável em Claude Code, Cursor, OpenCode, Gemini CLI, Codex, VS Code Copilot, Kiro, Trae, Rovo Dev.

---

## 2. Feature Comparison

| Feature / Capability | taste-skill | ui-ux-pro-max | frontend-design | landing-page-builder | **Impeccable** |
|---|---|---|---|---|---|
| Anti-slop rules (tipografia, cor, layout) | Sim | Sim | Sim | Sim (PT-BR) | **Sim (mais granular, 7 domínios)** |
| Variáveis de design calibráveis (VARIANCE/MOTION/DENSITY) | **Sim (3 vars)** | Não | Não | Não | Não |
| Catálogo de estilos/paletas/fonts | Não | **Sim (67/96/57)** | Não | Parcial | Não |
| Workflow guiado por etapas | Não | Não | Não | **Sim (4 etapas PT-BR)** | Não |
| Comandos operacionais (`/polish`, `/audit`, `/critique`) | Não | Não | Não | Não | **Sim (18 comandos)** |
| **CLI detector determinístico** (regex, sem LLM) | Não | Não | Não | Não | **Sim (`npx impeccable detect`, 24 checks)** |
| Análise de URL ao vivo | Não | Não | Não | Não | **Sim** |
| Anti-patterns explícitos (gray-on-colored, pure-black, card-nesting, dated-easing) | Parcial | Parcial | Parcial | Parcial | **Sim (exaustivo)** |
| Cobertura de motion/animation granular | Parcial | Parcial | Sim | Sim | **Sim (domínio dedicado)** |
| Português BR | Não | Não | Não | **Sim** | Não |
| Licença Apache 2.0 / instalável standalone | — | — | — | — | **Sim** |

### Overlap analysis

- **taste-skill** cobre variáveis calibráveis + arquitetura React/Tailwind — Impeccable NÃO substitui.
- **ui-ux-pro-max** é catálogo enciclopédico (67 styles, 96 palettes) — Impeccable NÃO substitui.
- **frontend-design** é filosofia criativa (tom maximalista/minimalista) — Impeccable complementa com regras mais táticas.
- **landing-page-builder** é workflow PT-BR de 4 etapas (copy → design → layout → dev) — Impeccable NÃO substitui, mas **enriquece a etapa final** (polish/audit).

### Features únicas do Impeccable (nenhuma skill instalada oferece)

1. **CLI detector** (`npx impeccable detect`) — análise determinística de 24 issues via regex contra arquivo ou URL viva. **Nenhuma skill nossa faz isso.**
2. **Comando `/polish`** — passe final pré-ship estruturado.
3. **Comando `/audit`** — checklist de qualidade enumerado.
4. **Comando `/critique`** — UX review passe a passe.

---

## 3. Decisão: **(A) INSTALL + INTEGRATE**

### Justificativa (1 linha)

Impeccable adiciona 2 capacidades que NENHUMA das 4 skills instaladas oferece — um **CLI detector determinístico** (`npx impeccable detect`) e **comandos operacionais de polish/audit/critique** — e é complementar (não concorrente) ao `landing-page-builder` PT-BR, encaixando perfeitamente no **Passo 5 (opcional) do `/landing-page`** já previsto no plano (linha 922).

### Riscos aceitos

- Impeccable é em inglês: usamos só como motor de análise no polish, mantendo o UX do comando `/landing-page` em PT-BR.
- Dependência externa de `npx` — o CLI é opt-in, se não rodar o comando segue sem bloquear.

---

## 4. Installation + Integration

### 4.1 Instalação (uma vez, por máquina)

Impeccable é instalável como skill do Claude Code. Instalação oficial (seguir README upstream para comando exato):

```bash
# Clone da skill pro diretório de skills do Claude Code
git clone https://github.com/pbakaus/impeccable ~/.claude/skills/impeccable

# (Opcional) CLI detector via npx — não precisa instalar, roda sob demanda
npx impeccable detect <path-ou-url>
```

Verificação:

```bash
ls ~/.claude/skills/impeccable/SKILL.md && echo "skill OK"
npx -y impeccable detect --help
```

### 4.2 Integração no `/landing-page` (Passo 5 — Polish)

Referência: Task 3.3 do plano define `/landing-page` com **Passo 5 opcional** já reservado pra Impeccable. Snippet a incluir em `plugins/dna-operacional/commands/landing-page.md`:

```markdown
## Passo 5 — Polish com Impeccable (opcional, recomendado)

**Objetivo:** auditoria determinística + polish final da landing antes de entregar ao cliente.

### 5.1 Detecção de issues (CLI, sem LLM)

Rodar contra o arquivo gerado:

\`\`\`bash
# Contra arquivo local
npx -y impeccable detect data/clientes/<slug>/landing-pages/<data>/index.html

# Contra URL já deployada (Netlify preview)
npx -y impeccable detect https://<preview>.netlify.app
\`\`\`

Se retornar issues, listar pro usuário agrupadas por severidade.

### 5.2 Polish guiado (skill)

Se a skill `impeccable` estiver instalada (checar `~/.claude/skills/impeccable/SKILL.md`):

1. Invocar via Skill tool: `skill: "impeccable"` com instrução "polish this landing page for shipping".
2. Pedir pra rodar `/audit` e `/critique` sobre o HTML gerado.
3. Aplicar patches sugeridos (em PT-BR pro usuário, traduzindo diagnósticos).

### 5.3 Fallback

Se `npx impeccable` falhar OU a skill não estiver instalada:
- Avisar usuário uma vez: "Polish automático indisponível — considere instalar Impeccable (link)".
- Continuar sem bloquear. O deploy acontece mesmo assim.
```

### 4.3 Checklist de integração (pra Task 3.3)

- [ ] Adicionar seção "Passo 5 — Polish com Impeccable" no template do `/landing-page`.
- [ ] Detecção `which impeccable` / `test -f ~/.claude/skills/impeccable/SKILL.md` antes de invocar.
- [ ] Fallback silencioso (não bloqueia deploy).
- [ ] Documentar instalação no `docs/APIS-EXTERNAS.md` (seção "Ferramentas opcionais").

---

## 5. Follow-ups

- Avaliar, no v0.3.0, se vale extrair a lógica do CLI detector pra dentro do DNA Operacional em PT-BR (evitar dependência externa em clientes sem Node.js).
- Monitorar atualizações do repo upstream (Paul Bakaus tem histórico de iterar rápido).
