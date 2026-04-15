# Storage Adapter — Google Sheets

Implementa o `contract.md` usando skills `gws-sheets-read`, `gws-sheets-append`, `gws-sheets` (range updates).

## Pré-requisitos do user

- Conta Google Drive (qualquer gmail funciona)
- Template `dna-operacional-data` copiado pro Drive do user (ver `templates/sheets-master-template.md`)
- gws CLI autenticado + skills `gws-sheets*` disponíveis no Claude Code
- `CLAUDE.md` do projeto com:

  ```markdown
  ## Storage Backend: sheets

  - spreadsheet_id: {{SHEETS_MASTER_ID}}  # ID da URL: docs.google.com/spreadsheets/d/XXX/edit
  ```

## Estrutura física

1 planilha mestre (`dna-operacional-data`), 7 abas (uma por table):
- `competitors`
- `competitor_posts`
- `content_pipeline`
- `my_content`
- `ad_library`
- `adaptive_models`
- `generated_scripts`

Cada aba tem linha 1 = headers (exact nomes das colunas do contract). Dados começam linha 2.

## Mapeamento operations → gws-sheets

### `read_<table>(filters?)`

```
1. spreadsheet_id = <do CLAUDE.md>
2. Invocar gws-sheets-read com range="<table>!A:Z" (A:Z cobre todas colunas)
3. Primeira linha = headers, resto = records
4. Converter arrays de valores em objetos record (zip com headers)
5. Aplicar Filter DSL em memória (Sheets não tem WHERE nativo — filtra client-side)
6. Return records filtrados
```

### `read_one_<table>(id)`

```
1. Ler range "<table>!A:Z" igual acima
2. Filtrar client-side: records.find(r => r.id == id)
3. Se undefined: raise StorageNotFound
4. Return record
```

### `write_<table>(record)`

```
1. Calcular próximo id: SELECT MAX(id) pegando coluna A, +1 (ou usar timestamp se preferir)
2. Montar array na ORDEM das colunas (headers da linha 1)
3. Invocar gws-sheets-append com:
   - spreadsheet_id
   - range: "<table>!A:Z"
   - values: [[id, col1_value, col2_value, ...]]
4. Return id (atribuído na etapa 1)
```

### `update_<table>(id, patch)`

```
1. Ler aba inteira (range "<table>!A:Z")
2. Encontrar linha onde A == id (0-indexed: index = rows.findIndex(...))
3. Se não achar: raise StorageNotFound
4. Aplicar patch à linha in-memory
5. Atualizar updated_at pra NOW()
6. Invocar gws-sheets values.update com range "<table>!A{linha+2}:Z{linha+2}" e valores novos
7. Return true
```

### `upsert_<table>(record, key)`

```
1. Ler aba toda
2. Buscar linha onde <key> == record[key]
3. Se existe: update + retorna id existente
4. Se não: write + retorna novo id
```

### `delete_<table>(id)`

```
1. Ler aba
2. Encontrar linha do id
3. Se não achar: raise StorageNotFound
4. Invocar gws-sheets-delete na linha (ou clear: range values empty)
5. Return true
```

### `count_<table>(filters?)`

```
1. Ler aba
2. Aplicar filter client-side
3. Return length
```

### `execute_sql(query)` — Sheets NÃO suporta

```
raise StorageBackendUnavailable("SQL queries require Supabase backend. Current: sheets. Switch via /setup-projeto ou aguarde v0.3.")
```

## DSL → client-side filter (JavaScript-like pseudocode)

```
function matches(record, filter) {
  for (key in filter) {
    if (key == "_and") return filter[key].every(f => matches(record, f));
    if (key == "_or") return filter[key].some(f => matches(record, f));

    const v = filter[key];
    if (typeof v === "object" && v.op) {
      switch (v.op) {
        case "gte": if (!(record[key] >= v.value)) return false; break;
        case "gt": if (!(record[key] > v.value)) return false; break;
        case "lte": if (!(record[key] <= v.value)) return false; break;
        case "lt": if (!(record[key] < v.value)) return false; break;
        case "ne": if (record[key] === v.value) return false; break;
        case "in": if (!v.value.includes(record[key])) return false; break;
        case "like":
          const pattern = v.value.replace(/%/g, ".*");
          if (!new RegExp(pattern, "i").test(String(record[key]))) return false;
          break;
      }
    } else {
      if (record[key] !== v) return false;
    }
  }
  return true;
}
```

## Mapeamento erros

| Situação | Erro retornado |
|---|---|
| gws-sheets-read retorna 404 | `StorageBackendUnavailable("Sheets: planilha não encontrada ou sem permissão. spreadsheet_id: {id}")` |
| `CLAUDE.md` não tem `spreadsheet_id` | `StorageBackendUnavailable("spreadsheet_id ausente em CLAUDE.md ## Storage Backend: sheets")` |
| Aba não existe | `StorageBackendUnavailable("Aba '{table}' não encontrada. Rode o template `sheets-master-template.md`.")` |
| Aba > 10k rows | `StorageQuotaExceeded("Aba {table} tem {n} rows (limite prático: 10k). Considere migrar pra Supabase via /dna migrar-storage (v0.2+).")` |
| Planilha read-only | `StorageReadOnly("Planilha sem permissão de escrita. Ajuste compartilhamento.")` |

## Atenção a rate limits

Google Sheets API: **60 req/min por user**. Operations que fazem múltiplas reads (ex: `upsert` = read + write) consomem 2 req. Batch quando possível.

Se bater rate limit: backoff exponencial (1s → 2s → 4s → 8s, max 3 retries), depois raise `StorageBackendUnavailable("Rate limit Google Sheets atingido")`.
