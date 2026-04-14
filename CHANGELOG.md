# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versionamento segue [Semver](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Previsto pra v0.1.0 final

- Migração das 14 skills (`setup-projeto`, `voz`, `humanizer`, `pesquisa-diaria`, `pesquisa-concorrentes`, `raio-x-ads-concorrentes`, `ideias-conteudo`, `analisar-video`, `roteiro-viral`, `carrossel-instagram`, `analista-conteudo`, `auto-melhoria`, `dna-melhoria`, `dna`)
- Storage layer com 3 adapters (Supabase / Google Sheets / Markdown local)
- Skill `/voz` nova (criar / evoluir / mostrar / versões)
- Skill `/dna-melhoria` nova (auto-refino do plugin)
- Sanitização completa (20 padrões pessoais → placeholders)

---

## [0.1.0-alpha] — 2026-04-14

### Adicionado (scaffolding)

- Estrutura de repo: marketplace na root + plugin nested em `plugins/dna-operacional/`
- `.claude-plugin/marketplace.json` apontando pro plugin nested
- `plugins/dna-operacional/.claude-plugin/plugin.json` com metadata v0.1.0
- Skill meta `/dna` com 3 modos (`/dna`, `/dna jornadas`, `/dna setup`)
- Banner ASCII sunset colorido em `assets/banner.txt` (ANSI truecolor, 18 linhas)
- `docs/CONVENCOES.md` — padrão "Próximos Passos" obrigatório
- `docs/JORNADAS.md` — 4 jornadas detalhadas
- `docs/ROADMAP.md` — plano v0.1.0-alpha → v1.0.0
- `README.md` com instalação e mapa de skills
- `LICENSE` MIT

### Infra

- Repo em `github.com/flavioahoy/dna-operacional`
- Git tag `v0.1.0-alpha`

### Notas conhecidas

- Banner ANSI pode não renderizar com cor em todos os terminais — fallback documentado em SKILL.md
- `/dna setup` redireciona pra `/setup-projeto` global do user (skill ainda não migrada pro plugin nesta versão)
- Nenhuma skill produtiva ainda — apenas scaffolding

---

## Convenções de release

- Versão **0.x.y** indica pré-release (1.0 depois das 4 rodadas completas)
- Cada release tem git tag (`v0.1.0-alpha`, `v0.1.0`, `v0.2.0`, etc)
- Breaking changes **só em major bumps** (0.1 → 0.2 pode quebrar, 0.1.0 → 0.1.1 não)
- User precisa rodar `/plugin marketplace update dna-operacional` após bumps (cache staleness documentado em `risks` do Spec 1)
