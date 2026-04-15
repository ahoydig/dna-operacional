# Roadmap — DNA Operacional

## v0.1.0-alpha (atual) — Scaffolding

Plugin instalável mas **vazio** (só com `/dna`). Propósito: validar arquitetura antes de migrar skills.

- [x] `/dna` (menu central + jornadas)
- [x] Estrutura de repo (marketplace + plugin nested)
- [x] Banner ASCII sunset com `by @flavioahoy`
- [x] `CONVENCOES.md`, `JORNADAS.md`, `ROADMAP.md`
- [x] README, CHANGELOG, LICENSE

## v0.1.0 (próxima sessão) — 14 skills migradas

- [ ] `/setup-projeto` (17 seções adaptativas, delega seção 13 pra `/voz`)
- [ ] `/voz` (criar, evoluir, mostrar, versões — auto-observa pra sugerir evoluções)
- [ ] `/humanizer` (limpa IA + aplica voz do projeto via `reference/voz-<handle>.md`)
- [ ] `/pesquisa-diaria` (com `/schedule` nativo da Anthropic como agendamento default)
- [ ] `/pesquisa-concorrentes` (Instagram-first)
- [ ] `/raio-x-ads-concorrentes` (briefing 10 seções)
- [ ] `/ideias-conteudo` (10 frameworks de hook)
- [ ] `/analista-conteudo` (14 seções SQL com KPIs BR)
- [ ] `/auto-melhoria` (orquestradora metacognitiva; delega pra `/voz` quando padrão de voz)
- [ ] `/carrossel-instagram` (visual final via Playwright)
- [ ] `/analisar-video` (engenharia reversa → `adaptive_models` no Supabase)
- [ ] `/roteiro-viral` (consome `adaptive_models`)
- [ ] `/dna-melhoria` (auto-melhora as próprias skills do plugin)

## v0.1.0-alpha.3 (em release) — Storage layer entregue

- [x] `lib/storage/contract.md` — API, DSL, errors (fonte da verdade)
- [x] `lib/storage/supabase.md` — adapter Supabase via MCP
- [x] `lib/storage/sheets.md` — adapter Google Sheets via gws-sheets
- [x] `lib/storage/markdown.md` — adapter Markdown local via Read/Write/Glob
- [x] `templates/migrations-v0.1.0.sql` — Supabase (7 tabelas + indexes + triggers)
- [x] `templates/sheets-master-template.md` — setup manual Google Sheets
- [x] `templates/data-folder-structure.md` — setup Markdown local
- [x] CONVENCOES §4 atualizada de stub pra conteúdo completo

**Não incluído (fica pra Plans 4-5):** migração real das 13 skills pra usar storage layer.

## v0.2.0 — Skills de agência + ads (família grande)

- [ ] `onboarding-cliente` (workflow completo)
- [ ] `pedido-anuncios`
- [ ] `roteiro-anuncios` (UGC PAS framework)
- [ ] `responder-leads` (UAZAPI WhatsApp)
- [ ] `coletar-anuncios` (popula `ad_library` — desbloqueia `raio-x-ads-concorrentes`)
- [ ] `lista-alto-valor` (refatorada genérica, lê nicho do `CLAUDE.md`)
- [ ] `meta-ads` (família 7 skills: campanha, conjuntos, anuncios, publicos, insights, regras, setup)
- [ ] `nomenclatura-utm` (helper de ads)
- [ ] `switchy-links` (links rastreáveis pra ads)
- [ ] `agendar-pesquisa` (orquestra `/schedule` pra automação)
- [ ] `/dna migrar-storage` (move dados entre backends)

## v0.3.0 — Ciclo completo de conteúdo

- [ ] `roteirista-conteudo`
- [ ] `analista-concorrentes`
- [ ] `publicar-conteudo`
- [ ] `reaproveitador`
- [ ] `popular-my-content` (importa histórico Instagram pra analista funcionar)
- [ ] Adapter Notion como 4º backend

## v0.4.0 — Genéricas úteis

- [ ] `pesquisador`
- [ ] `resumidor`
- [ ] `gerador-imagens`

## v1.0.0 — Produção

- Todas as 20+ skills estáveis
- Documentação completa
- Testes de integração automatizados
- CI com audit de sanitização antes de cada tag
- Publicado oficialmente no marketplace do Claude Code (quando Anthropic abrir)
