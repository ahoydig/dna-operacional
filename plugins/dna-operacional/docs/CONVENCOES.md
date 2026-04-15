# Convenções do plugin DNA Operacional

> Extensão da Spec 1 §7 cobrindo as 14 skills da v0.1.0.

Documento canônico das convenções que TODA skill do plugin deve seguir.

## 1. Bloco "Próximos Passos" (obrigatório no fim da skill)

Toda skill termina com este bloco após a execução principal:

```
✅ [resultado da skill em uma frase]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /<skill-sugerida-1>   — <1 linha do porquê>
  2. /<skill-sugerida-2>   — <1 linha do porquê>

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Regras

- **1-3 sugestões** máximo (mais que isso vira ruído).
- Sugestões **contextuais** (depende do resultado da execução).
  - Ex: se `pesquisa-concorrentes` rodou mas não populou `competitor_posts`, NÃO sugerir `raio-x-ads-concorrentes`.
- **Escape hatch obrigatório:** linha `💡 /dna pra ver todas...` no final, sempre.

### Fallback ASCII (terminais sem unicode)

Se `$LC_ALL` indicar ASCII-only, degradar `━` pra `-`:

```
----------------------------------------
>>> PROXIMOS PASSOS SUGERIDOS
----------------------------------------
  1. /<skill-1>   - <desc>
  2. /<skill-2>   - <desc>

  >>> /dna pra ver todas
----------------------------------------
```

## 2. Mapeamento inicial de sugestões (v0.1.0 — 14 skills)

| Skill | Sugere ao fim |
|---|---|
| `setup-projeto` | `/voz`, `/pesquisa-concorrentes`, `/pesquisa-diaria` |
| `voz` | `/humanizer` (teste imediato), `/setup-projeto` (se ainda não configurou) |
| `humanizer` | nenhum forçado (contextual) |
| `pesquisa-diaria` | `/ideias-conteudo` (se user salvou no pipeline), `/analista-conteudo` |
| `pesquisa-concorrentes` | `/raio-x-ads-concorrentes` (se `ad_library` populada, v0.2+), `/analista-conteudo` |
| `raio-x-ads-concorrentes` | `/ideias-conteudo`, `/pesquisa-concorrentes` |
| `ideias-conteudo` | `/analisar-video` (modelo), `/roteiro-viral`, `/analista-conteudo` |
| `analisar-video` | `/roteiro-viral` (consumir `adaptive_model` gerado) |
| `roteiro-viral` | `/carrossel-instagram` (visual), `/analista-conteudo` |
| `carrossel-instagram` | `/ideias-conteudo` (próximo tópico) |
| `analista-conteudo` | `/ideias-conteudo` (com insights), `/pesquisa-diaria` (temas frescos) |
| `auto-melhoria` | nenhum forçado |
| `dna-melhoria` | nenhum forçado |
| `dna` | nenhum (ele É o menu) |

## 3. Saudação (opcional, start de skill)

Skills que começam com operação longa (ex: scraping, análise) podem abrir com saudação curta:

```
🧬 [skill] iniciada. <sumário em 1 linha do que vai fazer>
```

Evitar verbosidade. Nunca mostrar banner no start (só `/dna` e `setup-projeto` primeira vez).

## 4. Storage layer (contrato abstrato) — v0.1.0-alpha.3

Toda skill que persiste dado **DEVE** chamar funções abstratas do `lib/storage/contract.md` — **nunca escreve SQL inline** (exceção: `analista-conteudo` que é Supabase-only, documentada no próprio contract).

### Fluxo de consumo

1. Skill lê `CLAUDE.md` **do projeto do user** (não deste repo) procurando seção `## Storage Backend: <opção>`.
2. Opções válidas: `supabase`, `sheets`, `markdown`.
3. Skill carrega `lib/storage/<opção>.md` — encontra o mapeamento de cada operation pro runtime.
4. Skill chama operations do contract (`storage.read_competitors(...)`, `storage.write_competitor(...)`, etc).
5. Adapter traduz pra runtime nativo (MCP Supabase / gws-sheets / Read-Write-Glob) e retorna.

### Operations disponíveis (7 por tabela × 7 tabelas = 49 operations)

Tabelas: `competitors`, `competitor_posts`, `content_pipeline`, `my_content`, `ad_library`, `adaptive_models`, `generated_scripts`.

Por tabela: `read`, `read_one`, `write`, `update`, `upsert`, `delete`, `count`.

Extra Supabase-only: `execute_sql(query)` — usado apenas por `analista-conteudo`.

### DSL de filtros (universal)

- Equality: `{nicho: "fitness"}`
- Comparison: `{followers_count: {op: "gte", value: 10000}}`
- In list: `{formato: {op: "in", value: ["reel", "tiktok"]}}`
- Like: `{name: {op: "like", value: "%Nike%"}}`
- Combinações: `{_and: [...], _or: [...]}`

### Regra ferro (code review)

Grep obrigatório antes de merge de qualquer skill:

```bash
grep -rE "SELECT |INSERT |UPDATE |DELETE " plugins/dna-operacional/skills/*/SKILL.md
```

Expected: zero matches (exceto `analista-conteudo` que é exceção documentada).

### Templates do user

- **Supabase:** `templates/migrations-v0.1.0.sql` (roda 1 vez)
- **Sheets:** `templates/sheets-master-template.md` (setup manual em 3 passos)
- **Markdown:** `templates/data-folder-structure.md` (mkdir + CLAUDE.md)

### Migração entre backends

v0.1.0-alpha.3: escolha é persistente. Trocar = migração manual.
v0.2+: skill `/dna migrar-storage <novo>` automatiza (Spec 2 §4.6).

## 5. Voz Dinâmica por projeto (v0.1.0-alpha.5)

Skill `/voz` mantém a voz escrita do projeto/criador em `reference/voz-<handle>.md`. **Toda skill que produz texto final pro user** invoca o humanizer (Plan 5), que lê voz dinâmica do projeto atual.

### Schema

Ver `lib/voz/SCHEMA.md` — fonte da verdade do formato.

### Modos disponíveis

```
/voz                       → status (v atual, counts, histórico)
/voz criar                 → entrevista 7 perguntas → v1
/voz mostrar               → exibe voz completa
/voz evoluir <input>       → URL/arquivo/texto, propõe diff, cria v_N+1
/voz versoes               → lista snapshots + diff
/voz versoes rollback v<N> → restaura snapshot
/voz silenciar | ativar    → controla auto-observação
```

### Auto-observação

Engine documentada em `lib/voz/auto-observacao.md`. 4 sinais com thresholds, sempre pede confirmação. User pode silenciar via `/voz silenciar`.

### Como skills devem consumir

- **Quem produz copy:** invoca humanizer no fim, que lê voz dinâmica
- **Quem detecta padrões:** dispara hooks de auto-obs (Plans 4-5 implementam)
- **Quem precisa de handle:** lê CLAUDE.md `## Handle: @<nome>` do projeto do user
- **Sem voz definida:** humanizer cai pra regras genéricas anti-IA

### Versionamento

- Sempre cópia, nunca symlink
- Snapshot `.v<N>.md` é imutável (audit trail)
- Canônico `voz-<handle>.md` é cópia do snapshot mais recente
- Rollback é cópia de snapshot antigo pro canônico — snapshots posteriores ficam preservados

## 6. Sanitização (IDs pessoais)

Antes de qualquer skill entrar no plugin, passa por audit com grep dos 20 padrões listados no Spec 2 §7.1. Placeholders substituem dados pessoais.

Ver Spec 2 §7 pro checklist completo.
