# Storage Adapter — Markdown Local

Implementa o `contract.md` usando arquivos `.md` em `data/` no filesystem do user. Sem dependência externa (zero infra).

## Pré-requisitos do user

- Nada. Só um projeto com pasta `data/` criada.
- `CLAUDE.md` do projeto com:

  ```markdown
  ## Storage Backend: markdown

  - data_dir: ./data  # relativo ao root do projeto
  ```

Default `data_dir`: `./data` (pode ser omitido no CLAUDE.md).

## Estrutura física

```
<project>/data/
├── competitors/
│   ├── 001-chris-bumstead.md
│   ├── 002-nikki-blackketter.md
│   └── ...
├── competitor_posts/
│   ├── 001-{timestamp}.md
│   └── ...
├── content_pipeline/
├── my_content/
├── ad_library/
├── adaptive_models/
└── generated_scripts/
```

1 arquivo = 1 record. Nome: `{id:03d}-{slug}.md` (id zero-padded + slug do campo nome principal).

## Formato de arquivo

```markdown
---
id: 42
name: "Chris Bumstead"
instagram_username: "cbum"
instagram_profile_url: "https://instagram.com/cbum"
followers_count: 15000000
nicho: "fitness"
sub_nicho: "bodybuilding"
avg_engagement_coefficient: 0.043
posts_analyzed_count: 87
last_avg_update: "2026-04-10T14:20:00Z"
created_at: "2026-04-01T10:00:00Z"
updated_at: "2026-04-14T15:30:00Z"
---

# Chris Bumstead

Mr. Olympia Classic Physique 5x. Canadense. Nicho: musculação clássica.
Sub-nicho: bodybuilding competitivo.

## Notes (opcional, free-form)

Qualquer contexto adicional que a skill queira persistir — vai no corpo do .md.
```

Frontmatter YAML = record campos. Corpo markdown = opcional (notes, contexto livre, usado só quando skill decidir usar).

## Mapeamento operations → Read/Write/Glob

### `read_<table>(filters?)`

```
1. data_dir = CLAUDE.md ## Storage Backend: markdown → data_dir (ou "./data")
2. Invocar Glob: <data_dir>/<table>/*.md
3. Pra cada arquivo: Read → parse frontmatter YAML → record
4. Aplicar Filter DSL em memória
5. Return records filtrados
```

### `read_one_<table>(id)`

```
1. Glob <data_dir>/<table>/*.md (mesmo do read_all)
2. Encontrar arquivo cujo frontmatter.id == id
3. Se não achar: raise StorageNotFound
4. Return record
```

### `write_<table>(record)`

```
1. Calcular novo id: Glob <data_dir>/<table>/*.md → parse ids → max + 1 (fallback: 1 se vazio)
2. Atribuir created_at = updated_at = NOW() (ISO 8601)
3. Gerar slug do campo principal (name, title, tema, etc):
   slug = lowercase(principal).replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-').slice(0, 50)
4. Filename: <data_dir>/<table>/{id:03d}-{slug}.md
5. Serializar: frontmatter YAML + (opcional) corpo markdown com heading
6. Invocar Write
7. Return id
```

### `update_<table>(id, patch)`

```
1. Encontrar arquivo do id (read_one)
2. Se não achar: raise StorageNotFound
3. Aplicar patch ao frontmatter + atualizar updated_at = NOW()
4. Re-serializar e Write no mesmo path
5. Return true
```

### `upsert_<table>(record, key)`

```
1. Glob + filtrar por record[key] == file.frontmatter[key]
2. Se achar 1: update + return id existente
3. Se não: write + return novo id
```

### `delete_<table>(id)`

```
1. Encontrar path do arquivo do id
2. Se não achar: raise StorageNotFound
3. Invocar Bash rm <path>  (ou ferramenta equivalente — Bash tool do Claude Code)
4. Return true
```

### `count_<table>(filters?)`

```
1. Glob + filter em memória
2. Return length
```

### `execute_sql(query)` — MD NÃO suporta

```
raise StorageBackendUnavailable("SQL queries require Supabase backend. Current: markdown. Switch via /setup-projeto ou aguarde v0.3.")
```

## Frontmatter parsing

Cada arquivo:

```
---
<yaml content>
---
<body md content>
```

Parse:
1. Read arquivo
2. Split em linhas
3. Se linha[0] == "---": primeira seção `---` até próximo `---` é frontmatter YAML
4. YAML.parse no conteúdo
5. Resto é body (armazenar em `_body` se skill precisar; senão ignorar)

Serializar (atenção: newline EXPLÍCITO entre o YAML e o `---` de fechamento, senão YAML fica malformado):

```
---
{YAML.stringify(record, {skipInvalid: false, flowLevel: -1})}
---

# {record.name || record.title || record.tema || "Record"}

{_body || ""}
```

Verificar empiricamente: o output de `YAML.stringify` geralmente JÁ termina com `\n`. Se sim, o template acima fica `\n---\n` (correto). Se não, adicionar `\n` antes do `---` na concatenação.

## DSL → client-side filter

Mesmo pseudocódigo do adapter Sheets (ambos fazem filter em memória).

## Mapeamento erros

| Situação | Erro retornado |
|---|---|
| Pasta `<data_dir>/<table>` não existe | `StorageBackendUnavailable("Pasta {dir} não existe. Rode o template data-folder-structure.md ou crie manualmente.")` |
| Glob retorna 0 arquivos em `read_one` | `StorageNotFound` |
| Write falha (permissão) | `StorageReadOnly("Permissão negada em {path}")` |
| Pasta > 100 arquivos | `StorageQuotaExceeded("Pasta {table} tem {n} arquivos (soft limit: 100). Considere migrar pra Sheets/Supabase via /dna migrar-storage (v0.2+).")` |
| YAML frontmatter inválido | `StorageBackendUnavailable("YAML inválido em {path}: {erro}")` |

## Dicas de manutenção

- Commit `data/` no git do projeto pra versionar (ou adicionar em `.gitignore` se contém info sensível).
- Editor com preview de frontmatter (Obsidian, VS Code + extensão YAML) facilita inspeção manual.
- Backup: `data/` é só filesystem, qualquer estratégia serve (rsync, Time Machine, Git).

## Quando migrar pra Sheets/Supabase

Soft limit: **~100 items por pasta**. Acima disso:
- Glob fica lento (lista todos arquivos)
- Navegação manual via editor vira dor
- Recomendação: `/dna migrar-storage sheets` (v0.2+) ou manual: exporta pra CSV, importa em planilha.
