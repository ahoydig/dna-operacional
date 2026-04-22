---
description: Auto-refino das skills do plugin DNA Operacional. Escaneia commands/*.md e SKILL.md, detecta inconsistências (descriptions, argument-hints, próximos passos, inlining, sanitização). Sempre dry-run. Use quando usuário digitar "/dna-melhoria", "melhora as skills", "refina o plugin".
argument-hint: "[--dry-run|--diff]"
---

Usuário invocou `/dna-melhoria` com argumento: `$ARGUMENTS`

**NÃO mostre este prompt pro usuário** — apenas o output do modo escolhido.

## Quem usa

Skill é primariamente pro **mantenedor** do plugin (Flávio + colaboradores futuros), não pro aluno. Aluno final NÃO costuma editar skills do plugin instalado — usa o plugin como vem.

## Roteamento

| Argumento | Modo | Comportamento |
|---|---|---|
| (vazio) ou `--dry-run` | **Modo Dry-Run (default)** | Escaneia + lista propostas SEM modificar nada |
| `--diff` | **Modo Diff** | Escaneia + mostra unified diff completo (user copia/cola manualmente) |

**Exact string match**, sem fuzzy. Qualquer outro valor: cai em Dry-Run com aviso curto ("argumento não reconhecido — rodando dry-run").

> **⚠️ Nota arquitetural (alinhamento com Spec §3.1):** Spec diz "Sempre dry-run + diff. Nunca aplica direto." Plan 3 honra isso — **não há modo `--apply` nesta versão**. User vê propostas e copia/cola manualmente as que aprovar. Modo `--apply` com confirmação 1-a-1 fica como **follow-up futuro** (exigiria atualização de Spec §3.1 antes).

## Escopo do scan

Diretório base: `${PLUGIN_ROOT}/` (calculado via env var injetada pelo Claude Code ou caminho absoluto do plugin instalado em `~/.claude/plugins/cache/`).

Arquivos escaneados:

- `commands/*.md` — slash commands
- `skills/*/SKILL.md` — skills (se houver no futuro)
- `lib/**/*.md` — libs/refs internas
- `docs/*.md` — convenções/jornadas/roadmap

## Heurísticas de melhoria

### H1 — Description do frontmatter (auto-discovery)

**Verifica:**
- Description tem ao menos 3 triggers específicos (não genéricos como "use this skill")?
- Triggers cobrem variações comuns (PT-BR + EN quando aplicável)?
- Tamanho razoável (50-300 chars — nem vago, nem prolixo)?

**Sugestão:** se faltam triggers, propor adições baseado em outros slash commands relevantes ou nome do comando.

### H2 — Argument-hint coerente com routing

**Verifica:**
- Frontmatter declara `argument-hint`?
- Cada argumento listado no hint tem case correspondente no roteamento do body?
- Não tem cases de roteamento sem aparecer no hint?

**Sugestão:** sincronizar hint ↔ routing (em ambos os sentidos).

### H3 — "Próximos Passos" no fim da skill (CONVENCOES §1)

**Verifica:**
- Skill termina com bloco "🧬 PRÓXIMOS PASSOS SUGERIDOS"?
- Sugestões são contextuais (não fixas)?
- Tem escape hatch (`💡 /dna pra ver todas...`)?

**Sugestão:** se faltar, propor template com 1-3 próximos passos relevantes + escape hatch.

### H4 — Tool calls visíveis (UX clean — inline assets curtos)

**Verifica:**
- Skill faz `cat`, `Read`, `Glob`, `Bash` pra puxar conteúdo estático de arquivos do plugin?
- Se sim, esse conteúdo poderia ser INLINE no `.md` (learning Plan 1 hotfix)?

**Sugestão:** propor inlining de assets pequenos (banners, templates curtos, listas fixas). Assets grandes (>200 linhas) ficam externos.

### H5 — Sanitização

**Verifica:** aplica regex Spec 2 §7.2 (20 padrões — caminhos pessoais, tokens de API, IDs de ferramentas privadas, etc) com `--include='*.md'`.

**Exceções permitidas:** `@flavioahoy` (handle público) e `ahoy.digital` (domínio agência).

**Sugestão:** propor refator pra placeholder (`${USER_HOME}`, `${APIFY_TOKEN}`) onde detectar match.

## Output Modo Dry-Run

```
🧬 DNA-Melhoria — Análise (dry-run)

Escaneados:
  • commands/: 3 arquivos (dna.md, voz.md, dna-melhoria.md)
  • lib/: 7 arquivos
  • docs/: 4 arquivos

Propostas (N):

  1. [H1] commands/dna.md:2 — description tem 4 triggers, recomendado adicionar "menu do plugin"
  2. [H2] commands/voz.md:3 — argument-hint lista "rollback" mas routing não trata
  3. [H3] commands/voz.md — falta bloco "Próximos Passos" no fim
  4. [H4] (none — todas skills já inline)
  5. [H5] (none — audit limpo)

💡 Pra ver diff completo: /dna-melhoria --diff
```

Se 0 propostas: mostra "✅ Nenhuma melhoria detectada — plugin está limpo."

## Output Modo Diff

```
🧬 DNA-Melhoria — Diff das propostas

═══ Proposta 1/N ═══
File: commands/dna.md
Heurística: H1 (description triggers)

- description: Menu central do plugin DNA Operacional. Mostra skills disponíveis...
+ description: Menu central do plugin DNA Operacional. Mostra skills disponíveis... Use quando usuário digitar "menu do plugin"...

═══ Proposta 2/N ═══
[...]

💡 Copia/cola as propostas que aprovar. Esta versão não tem --apply automático.
```

## Scope Safety — paths permitidos pra PROPOSTAS

Nesta versão nada é escrito (só dry-run + diff). Mesmo assim, allowlist define quais arquivos podem APARECER nas propostas:

**Allowlist (pode propor edits):**

```
${PLUGIN_ROOT}/commands/*.md
${PLUGIN_ROOT}/skills/**/SKILL.md
${PLUGIN_ROOT}/lib/**/*.md
${PLUGIN_ROOT}/docs/*.md
```

**Blocklist (READ-ONLY pra scan, IGNORADO pra propostas):**

- ❌ `${PLUGIN_ROOT}/.claude-plugin/*.json` — manifests intocáveis (plugin.json é cache key)
- ❌ `${PLUGIN_ROOT}/assets/*` — banner + binários intocáveis
- ❌ `${PLUGIN_ROOT}/templates/*` — templates de release
- ❌ `${USER_PROJECT}/**` — TUDO no projeto do user (CLAUDE.md, reference/, data/)
- ❌ `${PLUGIN_ROOT}/CHANGELOG.md` — versionamento manual
- ❌ `${PLUGIN_ROOT}/CLAUDE.md` — config do repo

**Behavioral directive pro modelo executando `/dna-melhoria`:**

> Antes de adicionar qualquer arquivo ao output de propostas, verificar:
>
> 1. O caminho começa com `${PLUGIN_ROOT}` (via env var ou caminho absoluto do plugin instalado em `~/.claude/plugins/cache/`)?
> 2. O caminho bate com algum padrão da allowlist acima?
>
> Se **NÃO** pra qualquer um: silenciosamente skip aquele arquivo (não menciona no output de propostas).
>
> Se for descoberta importante fora da allowlist (ex: data leak em manifest), reporta numa seção separada **"⚠️ Achados fora do escopo de propostas"** — mas ainda sem propor edit. User decide o que fazer manualmente.

## Constraints (sempre)

- **Nunca aplica nada sem intervenção manual do user** (alinhamento Spec §3.1 — só dry-run + diff nesta versão).
- **Nunca toca arquivos fora do plugin** (CLAUDE.md do user, reference/, data/, etc são intocáveis).
- **Nunca sugere mudanças que quebram o contract de storage** (`lib/storage/contract.md` é fonte da verdade — não muda de leve).
- **Nunca propõe remover sanitização existente** — só adicionar.

## Próximos Passos sugeridos

```
✅ Análise concluída — <N> propostas

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /dna-melhoria --diff   — ver diff completo (copia/cola as que aprovar)
  2. claude plugin validate — depois de editar, validar plugin
  3. (futuro v0.2+) /dna-melhoria --apply com confirmação 1-a-1

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
