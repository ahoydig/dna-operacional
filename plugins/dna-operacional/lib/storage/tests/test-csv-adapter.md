# Tests — CSV Adapter

Casos de teste MANUAIS (runbook) pra validar o adapter CSV (`lib/storage/csv.md`). Rodar em projeto de teste vazio (ex: `/tmp/test-dna-csv/`) com `CLAUDE.md` contendo `## Storage Backend: csv` + `data_dir: ./data`.

Cada caso tem: Setup, Operação, Retorno esperado, Verificação (arquivos + conteúdo).

---

## T1: write_competitor → read_one_competitor

**Objetivo:** Sanity check — write cria arquivo + header, read_one traz record de volta.

**Setup:**
- `data/` vazio (sem `competitors.csv`)

**Operação:**
```
storage.write_competitor({
  name: "Test Creator",
  instagram_username: "test",
  instagram_profile_url: "https://instagram.com/test"
})
```

**Retorno esperado:** `id=1`

**Verificação:**
- `data/competitors.csv` existe
- Linha 1 (header) contém: `id,name,instagram_username,instagram_profile_url,...`
- Linha 2 contém: `1,Test Creator,test,https://instagram.com/test,...`
- `created_at` e `updated_at` preenchidos com ISO 8601 UTC atual

**Seguida:**
```
storage.read_one_competitor(1)
```

**Retorno esperado:** record com `name == "Test Creator"`, `instagram_username == "test"`, `id == 1`.

---

## T2: upsert_competitor idempotente

**Objetivo:** Upsert com key existente não duplica linha.

**Setup:** T1 já rodou (1 competitor com `instagram_username="test"`).

**Operação:**
```
storage.upsert_competitor(
  {name: "Test Creator Updated", instagram_username: "test", instagram_profile_url: "https://instagram.com/test"},
  key="instagram_username"
)
```

**Retorno esperado:** `id=1` (mesmo id, não cria 2).

**Verificação:**
- `data/competitors.csv` ainda tem só 1 linha de dado (+ header)
- Campo `name` na linha foi atualizado pra `"Test Creator Updated"`
- `updated_at` mudou; `created_at` ficou igual ao T1

**Operação complementar:** upsert de record com key nova:
```
storage.upsert_competitor(
  {name: "Other", instagram_username: "other", instagram_profile_url: "https://instagram.com/other"},
  key="instagram_username"
)
```

**Retorno esperado:** `id=2` (novo record criado).
**Verificação:** 2 linhas de dado na CSV.

---

## T3: Filter DSL — equality + composição

**Objetivo:** Filtros em memória retornam subset correto.

**Setup:** CSV com 3 competitors:
```
1, A, nicho=fitness, followers=10000
2, B, nicho=moda, followers=50000
3, C, nicho=fitness, followers=100000
```

**Operação 1 — equality:**
```
storage.read_competitors({nicho: "fitness"})
```
**Retorno esperado:** 2 records (ids 1 e 3).

**Operação 2 — comparação:**
```
storage.read_competitors({followers_count: {op: "gte", value: 50000}})
```
**Retorno esperado:** 2 records (ids 2 e 3).

**Operação 3 — composição:**
```
storage.read_competitors({
  _and: [
    {nicho: "fitness"},
    {followers_count: {op: "gte", value: 50000}}
  ]
})
```
**Retorno esperado:** 1 record (id 3).

**Operação 4 — in list:**
```
storage.read_competitors({nicho: {op: "in", value: ["fitness", "moda"]}})
```
**Retorno esperado:** 3 records (todos).

---

## T4: Long field redirect (D2)

**Objetivo:** Campo `transcription` > 500 chars é redirecionado pra `texts/transcriptions/post_<id>.txt` com referência na CSV.

**Setup:** `data/` vazio.

**Operação:**
```
storage.write_competitor_post({
  competitor_id: 1,
  platform: "instagram",
  post_url: "https://instagram.com/p/ABC123",
  post_code: "ABC123",
  transcription: "<string de 1000 chars — ex: Lorem ipsum repetido>"
})
```

**Retorno esperado:** `id=1`.

**Verificação CSV:**
- `data/competitor_posts.csv` existe
- Header contém coluna `transcription_file` (NÃO `transcription`)
- Linha de dado tem `transcription_file=texts/transcriptions/post_1.txt`
- Campo `transcription` cru NÃO aparece na linha

**Verificação filesystem:**
- `data/texts/transcriptions/post_1.txt` existe
- Conteúdo do arquivo = string de 1000 chars original (byte-exato)

**Operação complementar — read hidrata:**
```
storage.read_one_competitor_post(1)
```
**Retorno esperado:** record com `record["transcription"]` preenchido com os 1000 chars (a skill não vê `_file`). `record["transcription_file"]` também disponível (detalhe de storage).

**Caso curto (controle):** Write com transcription de 200 chars:
- Arquivo em `texts/` NÃO deve ser criado
- Valor fica inline na CSV (coluna `transcription`, sem sufixo)

---

## T5: Markdown backend fallback (regressão zero)

**Objetivo:** Projetos existentes com `Storage Backend: markdown` continuam funcionando sem regressão.

**Setup:**
- Novo projeto `/tmp/test-md/` com `CLAUDE.md` contendo:
  ```
  ## Storage Backend: markdown
  - data_dir: ./data
  ```
- `data/competitors/` existe (vazia)

**Operação:**
```
storage.write_competitor({name: "MD Test", instagram_username: "mdtest", instagram_profile_url: "https://instagram.com/mdtest"})
```

**Retorno esperado:** `id=1` (mesma API).

**Verificação:**
- `data/competitors/001-md-test.md` existe (padrão markdown atual)
- NÃO existe `data/competitors.csv`
- Frontmatter YAML do `.md` tem os campos corretos
- Nenhuma mudança no comportamento do adapter markdown comparado a v0.1.x

**Operação complementar — read:**
```
storage.read_one_competitor(1)
```
**Retorno esperado:** record idêntico ao que seria retornado em v0.1.x — zero mudança observável pra skill.

---

## T6: Supabase backend continua (regressão zero)

**Objetivo:** Projetos com Supabase não foram afetados por v0.2.0.

**Setup:**
- Projeto com `CLAUDE.md`:
  ```
  ## Storage Backend: supabase
  - project_id: {{TEST_PROJECT_ID}}
  ```
- MCP Supabase autenticado
- Migration `templates/migrations-v0.1.0.sql` aplicada

**Operação 1 — write via API:**
```
storage.write_competitor({name: "SB Test", instagram_username: "sbtest", instagram_profile_url: "https://instagram.com/sbtest"})
```
**Retorno esperado:** id (autogen pelo Postgres).
**Verificação:** `mcp__supabase__execute_sql("SELECT * FROM competitors WHERE instagram_username = 'sbtest'")` retorna 1 row.

**Operação 2 — execute_sql direto:**
```
storage.execute_sql("SELECT COUNT(*) FROM competitors")
```
**Retorno esperado:** count correto, funciona igual v0.1.x.

**Operação 3 — comparação com CSV:**
```
# Em projeto CSV:
storage.execute_sql("SELECT * FROM competitors")
```
**Retorno esperado:** `StorageBackendUnavailable("SQL queries require Supabase backend. Current: csv. ...")`.

Confirma que a seleção de backend via CLAUDE.md funciona — mesma skill, comportamento correto por backend.

---

## Checklist resumido

Pra validar o adapter como "pronto pra v0.2.0", todos os 6 casos precisam passar:

- [ ] T1: write + read_one (sanity)
- [ ] T2: upsert idempotente
- [ ] T3: Filter DSL (equality + comparison + composition + in)
- [ ] T4: Long field redirect (D2 — texts/ + hidratação)
- [ ] T5: Markdown fallback sem regressão
- [ ] T6: Supabase continua + execute_sql barra CSV

## Notas de execução

- Testes são manuais por enquanto. Automação vem junto com a migração pra Python binário (v0.3+).
- Executar em ordem — T2 depende de T1, e assim por diante quando indicado no Setup.
- Reset entre suites: `rm -rf /tmp/test-dna-csv/data` antes de cada rodada limpa.
- Cronômetro informal: suite completa em projeto limpo ≤ 10 min de operação manual.
