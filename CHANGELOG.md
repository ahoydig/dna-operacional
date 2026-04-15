# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versionamento segue [Semver](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Previsto pra v0.1.0 final

- `/dna-melhoria --apply` com confirmação 1-a-1 (exigiria atualizar Spec §3.1 antes)
- Sanitização completa (20 padrões pessoais → placeholders) — em rolling audit a cada release
- Spike de tokens `/schedule` (estimativa real $ por execução de pesquisa-diaria automática) — Plan 6
- Release v0.1.0 final (remove `-alpha`) — Plan 7

---

## [0.1.0-alpha.8] — 2026-04-15

### Adicionado — Onboarding de APIs Externas

- `docs/APIS-EXTERNAS.md` — guia autoritativo com setup passo-a-passo pra:
  - **Apify** (`/pesquisa-diaria`, `/pesquisa-concorrentes`, `/analisar-video`)
  - **Supabase** (`/analista-conteudo`, storage backend)
  - **Modal** Whisper (`/analisar-video`)
  - **Google Sheets** (storage backend alternativo)
  - **`/schedule` Anthropic** (agendamento default pro `/pesquisa-diaria`)
  - **GitHub Actions** (agendamento grátis alternativo)
  - **launchd** (Mac local)
- `docs/SPIKE-TOKENS.md` — medição real de tokens/custo `/pesquisa-diaria`
- Pré-checks inline com instruções em 5 skills:
  - `/pesquisa-diaria` — APIFY_TOKEN
  - `/pesquisa-concorrentes` — APIFY_TOKEN
  - `/analisar-video` — APIFY_TOKEN + MODAL_APP_NAME
  - `/raio-x-ads-concorrentes` — APIFY_TOKEN + aviso `/coletar-anuncios` v0.2
  - `/analista-conteudo` — Supabase backend

### Mudado

- `commands/setup-projeto.md` — orienta APIS-EXTERNAS.md após setup base
- `README.md` — blocos "🔑 Setup de APIs" e "⏰ Agendamento"
- `docs/ROADMAP.md` — milestone v0.1.0-alpha.8

### Infra

- Git tag `v0.1.0-alpha.8` anotada
- `plugin.json.version` bumpado pra `0.1.0-alpha.8`
- Audit Spec §7.2 com regex refinado (whitelisted `apify_api_XXXX` em instruções de doc)
- `claude plugin validate` zero warnings

### Não incluído (Plan 7)

- Release v0.1.0 final (remove `-alpha`)
- Testes integrados automatizados
- Anúncio pros alunos do curso

### Decisão de default de agendamento

Ver `docs/SPIKE-TOKENS.md` pra medição real + regra. User escolhe conforme perfil no `APIS-EXTERNAS.md`.

---

## [0.1.0-alpha.7] — 2026-04-15

**Marco:** fecha as 14 skills planejadas pra v0.1.0. Próximos: spike tokens (Plan 6) + release final v0.1.0 (Plan 7).

### Adicionado — 4 Skills Migradas (globais → plugin)

- `commands/humanizer.md` — humaniza textos lendo voz dinâmica `reference/voz-<handle>.md`. Sem voz definida, cai pra regras genéricas anti-IA. Skip pra blocos de código.
- `commands/carrossel-instagram.md` — Playwright HTML-to-Image, moodboard agent-browser, output em `carrossel-out/`.
- `commands/analisar-video.md` — engenharia reversa completa via Apify + transcribe-audio (Whisper). Storage: writes `adaptive_models`.
- `commands/roteiro-viral.md` — consome `adaptive_models`, escreve `generated_scripts`, delega humanizer no fim.

### Adicionado — Hooks de Auto-Observação (3 sinais reais)

- **Sinal 1** (humanizer): expressão recorrente — threshold ≥3 ocorrências em ≥2 e ≤5 sessões. Tracking `reference/.voz-tracking.json`.
- **Sinal 2** (ideias-conteudo): hook salvo no pipeline com status=Roteirizado/Gravado — threshold 1 ocorrência (sinal forte).
- **Sinal 3** (humanizer): edição manual repetida 2× — tracking `reference/.humanizer-edits.json`. Best-effort em context window.
- **Sinal 4** (analisar-video): vídeo do criador (handle bate via scrape do URL) — threshold 1 ocorrência se handle == voz, 3 se terceiro.

Engine completa documentada em `lib/voz/auto-observacao.md` (Plan 3).

### Mudado

- `CLAUDE.md`: nova seção "Auto-Obs Hooks pattern (Plan 5)"
- `README.md`: tabela skills atualizada pra 14 (fecha alpha planejado)
- `docs/ROADMAP.md`: milestone v0.1.0-alpha.7 (alpha completion)

### Infra

- Git tag `v0.1.0-alpha.7` anotada
- `plugin.json.version` bumpado pra `0.1.0-alpha.7`
- Audit Spec §7.2 (regex completo + filtro pós-grep): 0 matches
- `claude plugin validate`: zero warnings

### Não incluído (Plans 6+7)

- Spike de tokens `/schedule` (estimativa real $ por execução de pesquisa-diaria automática) — Plan 6
- Release v0.1.0 final (remove `-alpha`) — Plan 7
- Skill `/dna migrar-storage <backend>` (v0.2+)

---

## [0.1.0-alpha.6] — 2026-04-15

### Adicionado — 7 Skills Migradas

- `commands/setup-projeto.md` — configura projeto com CLAUDE.md rico, delega §13 pra `/voz criar`
- `commands/pesquisa-diaria.md` — radar diário BR (storage: writes `content_pipeline`)
- `commands/pesquisa-concorrentes.md` — mapeia concorrentes IG (storage: upserts `competitors` + `competitor_posts`)
- `commands/raio-x-ads-concorrentes.md` — briefing de ads (storage: reads `ad_library` + `competitors`; aviso quando `ad_library` vazia)
- `commands/ideias-conteudo.md` — multiplica ideias do pipeline em 5 vídeos (storage: read/update `content_pipeline`)
- `commands/analista-conteudo.md` — análise SQL 14 seções (Supabase-only via `storage.execute_sql`, pré-check abortando se backend != supabase)
- `commands/auto-melhoria.md` — orquestradora metacognitiva (delega padrões de voz pra `/voz`)

### Mudado

- `README.md`: tabela "Skills incluídas" atualizada pra 10 (era 3)
- `docs/ROADMAP.md`: milestone v0.1.0-alpha.6
- `CLAUDE.md`: skill migration checklist documentado
- Cross-cutting: terminologia `avatar` → `publico-alvo` nas 7 skills migradas (alinhamento com vocabulário do curso MaestrIA — marketeiros BR, não devs)

### Infra

- Git tag `v0.1.0-alpha.6` anotada
- `plugin.json.version` bumpado pra `0.1.0-alpha.6`
- Audit Spec §7.2 (regex completo + filtro pós-grep): 0 matches
- `claude plugin validate`: zero warnings

### Notas conhecidas

- `raio-x-ads-concorrentes` pode ter degradação de performance quando `ad_library` estiver populada em escala (centenas+ de ads). Refator de paginação/batching previsto pra v0.2+.

### Não incluído (Plan 5)

- Skills globais → plugin: `humanizer`, `carrossel-instagram`, `analisar-video`, `roteiro-viral`
- Hooks reais de auto-observação nas skills consumidoras (`humanizer`, `ideias-conteudo`, `analisar-video`)

---

## [0.1.0-alpha.5] — 2026-04-15

### Adicionado — Skills Novas

- `commands/voz.md` — slash command com 7 modos:
  - **Status** (sem args): versão atual + counts + histórico
  - **Criar**: entrevista guiada 7 perguntas → v1
  - **Mostrar**: exibe voz completa formatada
  - **Evoluir** `<input>`: aceita URL/arquivo/áudio/vídeo/texto, propõe diff, cria v_N+1 com confirmação
  - **Versoes**: lista snapshots + diff resumo
  - **Versoes rollback v<N>**: restaura snapshot (snapshots posteriores preservados como audit trail)
  - **Silenciar / Ativar**: controla auto-observação
- `commands/dna-melhoria.md` — slash command com 2 modos (dry-run default / `--diff`), 5 heurísticas (description quality, argument-hint coerência, próximos passos, tool calls visíveis, sanitização) + scope safety com allowlist explícita. Alinhado com Spec §3.1 (só dry-run + diff, sem `--apply` em v0.1.0-alpha.5).
- `lib/voz/SCHEMA.md` — fonte da verdade do `reference/voz-<handle>.md` (frontmatter + 7 seções)
- `lib/voz/auto-observacao.md` — engine de auto-observação com 4 sinais e thresholds explícitos (Sinal 1 exige ≥2 sessões pra evitar falso positivo)

### Mudado

- `docs/CONVENCOES.md`: nova §5 "Voz Dinâmica por projeto" (§5 Sanitização renumerada pra §6)
- `docs/ROADMAP.md`: novo milestone v0.1.0-alpha.5; linhas `/voz` e `/dna-melhoria` removidas da seção v0.1.0 (já entregues)
- `README.md`: blocos "🎙 Voz Dinâmica" e "🧬 DNA-Melhoria" após "🗄️ Storage Layer"

### Infra

- Git tag `v0.1.0-alpha.5` anotada
- `plugin.json.version` bumpado pra `0.1.0-alpha.5` (cache key correto)
- Sanitization audit rodou com regex completo Spec §7.2 (20 padrões) + filtro pós-grep pras exceções públicas (`@flavioahoy`, `ahoy.digital`) — 1 leak real detectado e corrigido em `dna-melhoria.md` H5 (wording da heurística referenciava tokens literais do próprio regex); audit final 0 matches
- `claude plugin validate` zero warnings

### Validado em smoke

- Marketplace update pulou de `0.1.0-alpha.4/` pra `0.1.0-alpha.5/`
- `/reload-plugins` detectou 18 skills (era 16 — `/voz` + `/dna-melhoria` adicionadas)
- `/dna` sem regressão
- `/voz` (Modo Status sem args) orientou criar voz pra `@flavioahoy` (projeto novo sem `reference/voz-<handle>.md`)
- `/dna-melhoria` (Modo Dry-Run) escaneou 13 arquivos e gerou 3 propostas reais (H3 voz próximos passos, H3 dna-melhoria static template, H1 dna description) — confirma heurísticas funcionando end-to-end

### Não incluído (por design, fica pra Plans 4-5)

- Hooks reais de auto-observação nas skills consumidoras (`humanizer`, `ideias-conteudo`, `analisar-video`) — Plan 3 entrega a engine documentada, integração vem em Plan 5
- Humanizer real lendo voz dinâmica (Plan 5 implementa)
- Migração das 11 skills restantes pra usar storage layer + voz dinâmica (Plan 4)
- `/dna-melhoria --apply` (follow-up futuro; exigiria atualizar Spec §3.1)

---

## [0.1.0-alpha.4] — 2026-04-14

### Mudado — Banner

- "by @flavioahoy" no banner ASCII bumpado de fonte tiny (2 linhas) pra `figlet -f small` (5 linhas, blocky bonito). Mantém estética coerente com o "DNA OPS" do topo.
- Atualizado em `assets/banner.txt` E inline em `commands/dna.md` (sem dependência de `cat` continua valendo).

### Infra

- Git tag `v0.1.0-alpha.4`
- `plugin.json.version` bumpado pra `0.1.0-alpha.4` (cache key correto)

---

## [0.1.0-alpha.3] — 2026-04-14

### Adicionado — Storage Layer

- `plugins/dna-operacional/lib/storage/` com 5 arquivos:
  - `README.md` (overview + fluxo de consumo)
  - `contract.md` (fonte da verdade: 7 tabelas, 7 operations, DSL de filtros, erros)
  - `supabase.md` (adapter via MCP Supabase)
  - `sheets.md` (adapter via skills `gws-sheets-*`)
  - `markdown.md` (adapter via tools nativos Read/Write/Glob)
- `plugins/dna-operacional/templates/` com 3 templates:
  - `migrations-v0.1.0.sql` (Supabase: 7 tabelas + indexes + triggers de updated_at)
  - `sheets-master-template.md` (Google Sheets: setup manual em 3 passos)
  - `data-folder-structure.md` (Markdown: `mkdir data/*` + exemplos de record com frontmatter)

### Mudado

- `docs/CONVENCOES.md` §4 Storage: substituído stub por conteúdo completo com fluxo, DSL, regra ferro, templates
- `docs/ROADMAP.md`: novo milestone "v0.1.0-alpha.3 — Storage layer entregue"
- `README.md`: novo bloco "🗄️ Storage Layer" com comparativo de backends
- `CLAUDE.md`: seção Storage Layer adicionada

### Infra

- Git tag `v0.1.0-alpha.3`
- `plugin.json.version` bumpado pra `0.1.0-alpha.3` (cache key correto)

### Não incluído (por design, fica pra Plans 4-5)

- Migração das 13 skills pra usar o storage layer
- Skill `/dna migrar-storage` (v0.2+)

---

## [0.1.0-alpha.2] — 2026-04-14

### Corrigido

- Bump `plugin.json.version` de `0.1.0` pra `0.1.0-alpha.2`. Claude Code usa `plugin.json.version` como cache path key — sem bump, `/plugin marketplace update` não baixa nova versão mesmo com tag nova no GitHub. A alpha.1 tinha o fix do banner inline no código, mas o manifest não bumpado impedia o download pelos users. Esta release resolve cache staleness e entrega efetivamente o fix da alpha.1 + bump de manifest.

### Infra

- Git tag `v0.1.0-alpha.2`

### Aprendizado

- Em hotfixes futuros: "tag version ↔ `plugin.json.version` match" é check obrigatório no release-engineer antes de abrir GitHub release. Sem isso, release é doc-only pro user.

---

## [0.1.0-alpha.1] — 2026-04-14

### Corrigido

- `/dna` e `/dna <arg desconhecido>` não mostram mais "Read 1 file" no terminal — banner ASCII agora é bloco markdown inline em `commands/dna.md` (byte-exato vs `assets/banner.txt`), sem dependência de tool call.

### Infra

- Git tag `v0.1.0-alpha.1`

---

## [0.1.0-alpha] — 2026-04-14

### Adicionado (scaffolding)

- Estrutura de repo: marketplace na root + plugin nested em `plugins/dna-operacional/`
- `.claude-plugin/marketplace.json` apontando pro plugin nested
- `plugins/dna-operacional/.claude-plugin/plugin.json` com metadata v0.1.0
- Slash command `/dna` (em `commands/dna.md`) com 3 modos (`/dna`, `/dna jornadas`, `/dna setup`)
- Banner ASCII sunset colorido em `assets/banner.txt` (ANSI truecolor, 18 linhas)
- `docs/CONVENCOES.md` — padrão "Próximos Passos" obrigatório
- `docs/JORNADAS.md` — 4 jornadas detalhadas
- `docs/ROADMAP.md` — plano v0.1.0-alpha → v1.0.0
- `README.md` com instalação e mapa de skills
- `LICENSE` MIT

### Infra

- Repo em `github.com/ahoydig/dna-operacional`
- Git tag `v0.1.0-alpha`

### Notas conhecidas

- Banner ANSI pode não renderizar com cor em todos os terminais — fallback documentado em `commands/dna.md`
- `/dna setup` redireciona pra `/setup-projeto` global do user (skill ainda não migrada pro plugin nesta versão)
- Nenhuma skill produtiva ainda — apenas scaffolding

---

## Convenções de release

- Versão **0.x.y** indica pré-release (1.0 depois das 4 rodadas completas)
- Cada release tem git tag (`v0.1.0-alpha`, `v0.1.0`, `v0.2.0`, etc)
- Breaking changes **só em major bumps** (0.1 → 0.2 pode quebrar, 0.1.0 → 0.1.1 não)
- User precisa rodar `/plugin marketplace update dna-operacional` após bumps (cache staleness documentado em `risks` do Spec 1)
