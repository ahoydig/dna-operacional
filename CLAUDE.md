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
