# Storage Layer — DNA Operacional

Camada abstrata que desacopla as skills de dados do backend físico. Skills chamam funções do `contract.md`; cada adapter (`supabase.md`, `sheets.md`, `markdown.md`) implementa as funções usando o runtime apropriado.

## Por que existe

Plugin precisa ser portável. Aluno escolhe onde guardar dados das skills (pesquisa-concorrentes, content_pipeline, etc) conforme experiência e escala:

- **Supabase:** power user, escala, análises SQL ricas
- **Google Sheets:** maioria dos casos, visualização fácil, zero dev ops
- **Markdown local:** iniciante, zero infra, projeto pessoal

Sem esta camada, skills só funcionariam no Supabase pessoal do Flávio.

## Como skills consomem

Toda skill de dados faz:

1. Lê `CLAUDE.md` do projeto atual procurando seção `## Storage Backend: <opção>`
2. Carrega `lib/storage/<opção>.md` correspondente (supabase / sheets / markdown)
3. Executa operations conforme o contract (ex: `storage.read_competitors(...)`)
4. Nunca escreve SQL inline (exceção documentada: `analista-conteudo` é Supabase-only)

## Arquivos aqui

| Arquivo | Responsabilidade |
|---|---|
| `README.md` | Overview (este arquivo) |
| `contract.md` | Fonte da verdade — API, DSL de filtros, erros |
| `supabase.md` | Adapter Supabase (via MCP `mcp__supabase__execute_sql` + `apply_migration`) |
| `sheets.md` | Adapter Google Sheets (via skills `gws-sheets-read` / `gws-sheets-append`) |
| `markdown.md` | Adapter Markdown local (via tools nativos `Read` / `Write` / `Glob`) |

## Templates associados

Em `plugins/dna-operacional/templates/`:

- `migrations-v0.1.0.sql` — Supabase: roda 1 vez no projeto do user pra criar as 7 tabelas
- `sheets-master-template.md` — Sheets: instruções de como copiar planilha template pro Drive
- `data-folder-structure.md` — Markdown: estrutura de pastas `data/<table>/NNN-slug.md`

## Estado atual

v0.1.0-alpha.3 — scaffolding do storage layer. Skills ainda não integradas (Plans 4-5).
