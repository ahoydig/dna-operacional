# Roadmap — DNA Operacional

## v0.1.0-alpha (atual) — Scaffolding

Plugin instalável mas **vazio** (só com `/dna`). Propósito: validar arquitetura antes de migrar skills.

- [x] `/dna` (menu central + jornadas)
- [x] Estrutura de repo (marketplace + plugin nested)
- [x] Banner ASCII sunset com `by @flavioahoy`
- [x] `CONVENCOES.md`, `JORNADAS.md`, `ROADMAP.md`
- [x] README, CHANGELOG, LICENSE

## v0.1.0-alpha.7 (em release) — 4 skills globais migradas + 3 hooks auto-obs

Marco: **fecha as 14 skills planejadas pra v0.1.0**.

- [x] `/humanizer` (lê voz dinâmica + Sinais 1 e 3 de auto-obs)
- [x] `/carrossel-instagram` (Playwright, sem storage)
- [x] `/analisar-video` (storage.write_adaptive_model + Sinal 4)
- [x] `/roteiro-viral` (storage.read_adaptive_models + write_generated_scripts + delega humanizer)
- [x] Hook Sinal 2 em `/ideias-conteudo` (já migrada em alpha.6)

**Próximos:** v0.1.0 final precisa Plan 6 (spike tokens `/schedule`) + Plan 7 (release sem alpha).

**Debt / follow-up pra v0.2:** `carrossel-instagram` introduziu `references/carrossel-instagram/` (1216 linhas de refs visuais) — primeiro precedente de subdir de refs por skill. Padronizar convenção de `references/<skill>/` (quando criar, quando colocar inline na skill, tamanho máximo) antes que outras skills façam o mesmo com critério divergente.

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

## v0.1.0-alpha.5 (em release) — Skills voz + dna-melhoria

- [x] `commands/voz.md` — slash command com 7 modos (status/criar/mostrar/evoluir/versoes/silenciar/ativar)
- [x] `lib/voz/SCHEMA.md` — fonte da verdade do `reference/voz-<handle>.md`
- [x] `lib/voz/auto-observacao.md` — 4 sinais com thresholds + hooks pra Plans 4-5
- [x] `commands/dna-melhoria.md` — slash command com 2 modos (dry-run/diff) + 5 heurísticas + scope safety
- [x] CONVENCOES §5 Voz Dinâmica
- [x] README blocos `/voz` e `/dna-melhoria`

**Não incluído (Plans 4-5):** hooks reais de auto-obs nas skills consumidoras (humanizer, ideias-conteudo, analisar-video). Voz é entregue mas integração efetiva no humanizer vem em Plan 5. `--apply` do dna-melhoria também fica como follow-up futuro (alinhamento Spec §3.1).

## v0.1.0-alpha.6 (em release) — 7 skills migradas

- [x] `/setup-projeto` (delega §13 pra `/voz criar`)
- [x] `/pesquisa-diaria` (storage layer)
- [x] `/pesquisa-concorrentes` (storage layer)
- [x] `/raio-x-ads-concorrentes` (storage layer + aviso ad_library vazia)
- [x] `/ideias-conteudo` (storage layer)
- [x] `/analista-conteudo` (Supabase-only — exceção documentada)
- [x] `/auto-melhoria` (delega padrões de voz pra `/voz`)

**Não incluído (Plan 5):** humanizer, carrossel-instagram, analisar-video, roteiro-viral (skills globais → plugin).

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
