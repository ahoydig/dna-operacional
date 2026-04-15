# DNA Operacional — Plugin Claude Code

Plugin @ahoydig — skills concatenadas pra criador, agência, inteligência competitiva BR.

## Stack
- Markdown + JSON (manifests)
- Slash command `/dna` em `commands/dna.md`
- Banner ASCII inline (sem tool calls)
- Docs: CONVENCOES, JORNADAS, ROADMAP, README, CHANGELOG

## Storage Layer (v0.1.0-alpha.3)

Plugin abstrai persistência via `lib/storage/contract.md`. 3 adapters:
- `supabase.md` — via MCP Supabase
- `sheets.md` — via gws-sheets skills
- `markdown.md` — via Read/Write/Glob nativos

Skills consumidoras leem o backend escolhido em `CLAUDE.md` do PROJETO DO USER (não deste repo), seção `## Storage Backend: <opção>`, e seguem o adapter correspondente.

## Regras principais
- `plugin.json.version` deve sempre bater com a git tag (senão cache marketplace não atualiza — ver LEARNINGS)
- Banner ASCII inline, nunca via cat/Bash (UX do user)
- Sanitização: 18 padrões bloqueados via regex Spec 2 §7.2

## Skill Migration Checklist (Plan 4 / v0.1.0-alpha.6)

Pra migrar uma skill da global pro plugin, seguir 5 sub-tasks:

A. Copy + sanitize (placeholders pra tokens pessoais)
B. Adapt pra storage layer (substituir SQL inline por storage.<op>_<table>)
C. Adicionar bloco "Próximos Passos" (CONVENCOES §1)
D. Audit Spec §7.2 (regex + filtro pós-grep, 0 matches)
E. Smoke + review

Skills global do Flávio em ~/.claude/skills/ permanecem intactas — plugin é cópia adaptada.
Skills no plugin têm precedência se mesmo nome (Claude Code resolve pra slash command do plugin).

## Auto-Obs Hooks (Plan 5 / v0.1.0-alpha.7)

Skills consumidoras implementam hooks pra disparar a engine de auto-observação documentada em `lib/voz/auto-observacao.md`. Padrão de hook:

1. Após action principal da skill, verificar `auto_observacao_ativa: true` no frontmatter de `reference/voz-<handle>.md` do projeto.
2. Se ativa: detectar sinal específico (varia por skill).
3. Atualizar tracking JSON apropriado (`reference/.voz-tracking.json` ou `.humanizer-edits.json`).
4. Se threshold atingido: propor evolução ao user com confirmação (y/n).
5. Se y: instruir user a rodar `/voz evoluir <padrão>` (skills não cascateiam).

Skills com hooks (Plan 5):
- `humanizer`: Sinal 1 (expressão recorrente) + Sinal 3 (edição manual repetida)
- `ideias-conteudo`: Sinal 2 (hook no pipeline status=Roteirizado/Gravado)
- `analisar-video`: Sinal 4 (vídeo do criador, handle bate)
