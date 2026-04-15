# Storage Adapter — Supabase

Implementa o `contract.md` usando MCP Supabase (`mcp__supabase__execute_sql`, `mcp__supabase__apply_migration`, `mcp__supabase__list_tables`, etc).

## Pré-requisitos do user

- Projeto Supabase criado (free tier: supabase.com/new)
- MCP Supabase autenticado no Claude Code (via `/plugin` ou settings)
- Migration `templates/migrations-v0.1.0.sql` aplicada 1 vez no projeto do user
- `CLAUDE.md` do projeto com:

  ```markdown
  ## Storage Backend: supabase

  - project_id: {{SUPABASE_PROJECT_ID}}
  ```

## Mapeamento operations → MCP calls

### `read_<table>(filters?)`

Skill chama: `storage.read_competitors({nicho: "fitness"})`

Implementação:

```
1. Converter Filter DSL pra cláusula SQL WHERE (ver seção "DSL → SQL" abaixo).
2. Invocar mcp__supabase__execute_sql com:
   - project_id: <do CLAUDE.md>
   - query: "SELECT * FROM competitors WHERE nicho = 'fitness' ORDER BY id DESC"
3. Retornar result.rows (array de records)
```

### `read_one_<table>(id)`

```
query: "SELECT * FROM competitors WHERE id = {id} LIMIT 1"
Se rows.length == 0: raise StorageNotFound
Else: return rows[0]
```

### `write_<table>(record)`

```
1. Extrair colunas e valores do record (excluir id, created_at, updated_at — autogen)
2. query: "INSERT INTO competitors (col1, col2, ...) VALUES ($1, $2, ...) RETURNING id"
3. Return result.rows[0].id
```

### `update_<table>(id, patch)`

```
1. Extrair pares coluna=valor do patch
2. query: "UPDATE competitors SET col1 = $1, col2 = $2, updated_at = NOW() WHERE id = {id}"
3. Se result.rowCount == 0: raise StorageNotFound
4. Return true
```

### `upsert_<table>(record, key)`

```
query: "INSERT INTO competitors (...) VALUES (...) ON CONFLICT ({key}) DO UPDATE SET col1 = EXCLUDED.col1, ... RETURNING id"
Return result.rows[0].id
```

### `delete_<table>(id)`

```
query: "DELETE FROM competitors WHERE id = {id}"
Se result.rowCount == 0: raise StorageNotFound
Return true
```

### `count_<table>(filters?)`

```
query: "SELECT COUNT(*) FROM competitors WHERE <filter clause>"
Return result.rows[0].count (int)
```

### `execute_sql(query)` — Supabase-only

```
Invocar mcp__supabase__execute_sql direto.
Return result.rows.
```

## DSL → SQL

| DSL | SQL WHERE clause |
|---|---|
| `{campo: valor}` | `campo = <valor>` (escape apropriado por tipo) |
| `{campo: {op: "gte", value: 100}}` | `campo >= 100` |
| `{campo: {op: "gt", value: 100}}` | `campo > 100` |
| `{campo: {op: "lte", value: 100}}` | `campo <= 100` |
| `{campo: {op: "lt", value: 100}}` | `campo < 100` |
| `{campo: {op: "ne", value: "x"}}` | `campo <> 'x'` |
| `{campo: {op: "in", value: ["a", "b"]}}` | `campo IN ('a', 'b')` |
| `{campo: {op: "like", value: "%Nike%"}}` | `campo ILIKE '%Nike%'` (case-insensitive) |
| `{_and: [f1, f2]}` | `(<f1>) AND (<f2>)` |
| `{_or: [f1, f2]}` | `(<f1>) OR (<f2>)` |

**⚠️ SQL Injection:** sempre use parâmetros `$1, $2, ...` no `execute_sql`. NUNCA concatene valores direto na string.

## Mapeamento erros

| Situação | Erro retornado |
|---|---|
| `result.rows.length == 0` em `read_one_*` / `update_*` | `StorageNotFound` |
| MCP Supabase não conecta (timeout, auth inválida) | `StorageBackendUnavailable("Supabase: {msg MCP}")` |
| `CLAUDE.md` não tem `project_id` | `StorageBackendUnavailable("project_id ausente em CLAUDE.md ## Storage Backend: supabase")` |
| User atingiu plano Supabase (raro, free tier generoso) | `StorageQuotaExceeded("Supabase free tier: 500MB, 50MB egress/mo")` |

## Checklist de migration

Antes de qualquer operation:

1. Skill lê `CLAUDE.md` do projeto → acha `## Storage Backend: supabase` + `project_id`
2. Skill chama `mcp__supabase__list_tables` → confirma que as 7 tabelas existem
3. Se NÃO existem: orienta user a rodar `templates/migrations-v0.1.0.sql` no SQL Editor do Supabase
4. Pode operar

## Exemplos runtime

### Exemplo 1: pesquisa-concorrentes insere competitor

```
skill chama: storage.write_competitor({
  name: "Chris Bumstead",
  instagram_username: "cbum",
  instagram_profile_url: "https://instagram.com/cbum",
  nicho: "fitness"
})

adaptor Supabase executa:
  mcp__supabase__execute_sql(project_id="xyz", query="""
    INSERT INTO competitors (name, instagram_username, instagram_profile_url, nicho)
    VALUES ('Chris Bumstead', 'cbum', 'https://instagram.com/cbum', 'fitness')
    RETURNING id
  """)

retorna: 42
```

### Exemplo 2: ideias-conteudo lê pipeline

```
skill chama: storage.read_content_pipeline({status: "Ideia"})

adaptor Supabase executa:
  mcp__supabase__execute_sql(project_id="xyz", query="""
    SELECT * FROM content_pipeline
    WHERE status = 'Ideia'
    ORDER BY id DESC
  """)

retorna: array de records
```
