# Storage Adapter — CSV Local

Implementa o `contract.md` usando arquivos `.csv` em `data/` no filesystem do user. Sem dependência externa (zero infra). **Default do plugin desde v0.2.0** — é o que novos projetos recebem quando não configuram backend.

## Pré-requisitos do user

- Nada. Só um projeto com pasta `data/` criada (o adapter cria on-demand se faltar).
- `CLAUDE.md` do projeto com:

  ```markdown
  ## Storage Backend: csv

  - data_dir: ./data  # relativo ao root do projeto
  ```

Default `data_dir`: `./data` (pode ser omitido no CLAUDE.md).

Se `## Storage Backend:` estiver ausente no CLAUDE.md, skills assumem `csv` silenciosamente — nunca abortar por falta de config.

## Estrutura física

```
<project>/data/
├── competitors.csv
├── competitor_posts.csv
├── content_pipeline.csv
├── my_content.csv
├── ad_library.csv
├── adaptive_models.csv
├── generated_scripts.csv
└── texts/
    ├── transcriptions/
    │   ├── post_42.txt
    │   ├── model_7.txt
    │   └── content_3.txt
    ├── hooks_visuais/
    │   └── post_42.txt
    ├── frame_analysis/
    │   └── video_7.json
    └── scripts/
        └── script_12.md
```

1 arquivo `.csv` = 1 tabela (N records). 1 header na linha 1. Campos longos redirecionados pra `texts/` (ver D2 abaixo).

## Formato CSV — RFC 4180

- **Encoding:** UTF-8 sem BOM.
- **Line ending:** `\n` (LF). Não CRLF.
- **Separator:** vírgula (`,`).
- **Header:** linha 1 com nomes de coluna exatamente como no `contract.md`.
- **Quoting (RFC 4180):** campo precisa ir entre aspas duplas SE contém:
  - vírgula (`,`)
  - quebra de linha (`\n` ou `\r`)
  - aspas duplas (`"`)
- **Escape de aspas dentro de campo aspado:** dobrar (`""`).
- **Campos vazios:** string vazia (`,,`) representa `None/null`. Nunca escrever literalmente `null` ou `None`.
- **Tipos:**
  - `int` / `float` — escrito cru (sem aspas, a não ser que contenha vírgula decimal — padronizamos ponto).
  - `bool` — `true` / `false` (lowercase).
  - `datetime` — ISO 8601 em UTC: `2026-04-21T14:20:00Z`.
  - `json/text` — serializado como string, sempre aspado (contém chaves e vírgulas).

Exemplo `competitors.csv`:

```csv
id,name,instagram_username,instagram_profile_url,followers_count,nicho,sub_nicho,avg_engagement_coefficient,posts_analyzed_count,last_avg_update,created_at,updated_at
1,Chris Bumstead,cbum,https://instagram.com/cbum,15000000,fitness,bodybuilding,0.043,87,2026-04-10T14:20:00Z,2026-04-01T10:00:00Z,2026-04-14T15:30:00Z
2,"Marca, Nike Brasil",nikebrasil,https://instagram.com/nikebrasil,8000000,esporte,,,,,2026-04-02T10:00:00Z,2026-04-02T10:00:00Z
3,Creator ""Aspas""",test,https://instagram.com/test,5000,lifestyle,,,,,2026-04-03T10:00:00Z,2026-04-03T10:00:00Z
```

Nota: linha 2 mostra vírgula aspada; linha 3 mostra aspa dentro de campo aspado (dobrada).

## Campos longos (D2) — redirecionamento pra `texts/`

CSV engasga com campos grandes (transcription de 5min de vídeo = 2-5KB; frame_analysis_json = ~50KB; body de roteiro = 1-3KB). Regra:

| Tabela | Campo no contract | Campo na CSV | Arquivo físico |
|---|---|---|---|
| `competitor_posts` | `transcription` (> 500 chars) | `transcription_file` | `texts/transcriptions/post_<id>.txt` |
| `competitor_posts` | `hook_visual` (> 500 chars) | `hook_visual_file` | `texts/hooks_visuais/post_<id>.txt` |
| `adaptive_models` | `frame_analysis_json` (sempre) | `frame_analysis_file` | `texts/frame_analysis/video_<id>.json` |
| `adaptive_models` | `transcript` (> 500 chars) | `transcript_file` | `texts/transcriptions/model_<id>.txt` |
| `generated_scripts` | `body` (> 500 chars) | `body_file` | `texts/scripts/script_<id>.md` |
| `my_content` | `transcript` (> 500 chars) | `transcript_file` | `texts/transcriptions/content_<id>.txt` |

**Regra de escrita:**

1. Skill chama `write_*(record)` com o campo longo inline.
2. Adapter mede `len(record[campo])` em chars.
3. Se `> 500` (ou `sempre` pra `frame_analysis_json`):
   - Grava conteúdo em `texts/<subfolder>/<prefix>_<id>.<ext>`.
   - Substitui valor na CSV pela REFERÊNCIA relativa: `texts/transcriptions/post_42.txt`.
   - Nome da coluna na CSV ganha sufixo `_file`.
4. Se `<= 500`: grava inline na CSV (sem sufixo `_file`).

**Regra de leitura:**

1. Skill chama `read_*` / `read_one_*`.
2. Adapter lê a linha da CSV.
3. Pra cada coluna sufixada `_file`:
   - `full_path = data_dir + "/" + value`
   - Read do arquivo físico.
   - Injetar conteúdo no record sob o nome ORIGINAL do campo (ex: `record["transcription"] = conteúdo`, NÃO `record["transcription_file"]`).
4. Skill recebe record com o campo longo já materializado — não sabe que houve redirect.

Convenção exposta ao contract (D2): sufixo `_file` é estável; skills que queiram o path cru (raro) podem inspecionar `record["<campo>_file"]` antes da hidratação.

## Mapeamento operations → IO

### `read_<table>(filters?)`

```
1. data_dir = CLAUDE.md ## Storage Backend: csv → data_dir (ou "./data")
2. path = <data_dir>/<table>.csv
3. Se não existe: return [] (não é erro — tabela vazia)
4. Read arquivo + parse CSV respeitando RFC 4180 quoting
5. Pra cada linha: dict(zip(header, row))
6. Aplicar hidratação de campos *_file (ver seção D2)
7. Aplicar Filter DSL em memória
8. Return records filtrados (ordenados por id DESC por default)
```

### `read_one_<table>(id)`

```
1. Chamar read_<table>({id: id})
2. Se retorna 0 records: raise StorageNotFound
3. Se retorna 1: return record
4. Se retorna > 1: raise StorageBackendUnavailable("CSV corrompido: id duplicado em <table>")
```

### `write_<table>(record)`

```
1. path = <data_dir>/<table>.csv
2. Se não existe: cria com header derivado do contract.md (colunas canônicas + *_file quando aplicável)
3. Calcular novo id: ler CSV, pegar max(id) + 1 (fallback: 1 se vazio)
4. Atribuir created_at = updated_at = NOW() (ISO 8601 UTC)
5. Pra cada campo longo (ver tabela D2):
   - Se len > threshold: grava em texts/<subfolder>/<prefix>_<id>.<ext>, substitui na row pela referência, ajusta nome da coluna pra *_file
6. Serializar row respeitando RFC 4180 (aspas em campos com vírgula/newline/aspas)
7. Append na CSV (modo "a" — zero regen pra operação O(1))
8. Validar soft/hard thresholds (ver "Thresholds" abaixo)
9. Return id
```

### `update_<table>(id, patch)`

```
1. Read CSV completa
2. Encontrar linha com id == id. Se não achar: raise StorageNotFound
3. Aplicar patch aos campos da linha + atualizar updated_at = NOW()
4. Pra cada campo longo em patch:
   - Se len > threshold: regrava arquivo em texts/ (mesmo path — sobrescreve)
   - Se len <= threshold: apaga arquivo em texts/ (se existia) + inlinea valor
5. Regen CSV completa (write_all sem a linha antiga + com a linha nova)
6. Return true
```

### `upsert_<table>(record, key)`

```
1. Read CSV completa
2. Filtrar por record[key] == row[key]
3. Se achar 1: update_<table>(row.id, record) + return row.id
4. Se não: write_<table>(record) + return novo id
5. Se achar > 1: raise StorageBackendUnavailable("Duplicate key <key>=<value> em <table>")
```

### `delete_<table>(id)`

```
1. Read CSV completa
2. Encontrar linha com id == id. Se não achar: raise StorageNotFound
3. Pra cada coluna *_file na linha: Bash rm do arquivo físico em texts/
4. Regen CSV completa sem a linha
5. Return true
```

### `count_<table>(filters?)`

```
1. Chamar read_<table>(filters) — com hidratação
2. Return length
```

Nota de performance: pra count sem filter, otimizar pra `wc -l <path> - 1` (desconta header) sem parsear.

### `execute_sql(query)` — CSV NÃO suporta

```
raise StorageBackendUnavailable(
  "SQL queries require Supabase backend. Current: csv. "
  "Skills que precisam SQL (ex: analista-conteudo) precisam migrar pra Supabase via /setup-projeto, "
  "ou aguardar versão CSV simplificada em v0.3."
)
```

## DSL → client-side filter

CSV carrega tudo em memória e filtra localmente (igual ao adapter markdown). Pseudocódigo:

```python
def apply_filter(records, filter):
    if not filter: return records
    if "_and" in filter: return reduce(intersect, [apply_filter(records, f) for f in filter["_and"]])
    if "_or" in filter: return reduce(union, [apply_filter(records, f) for f in filter["_or"]])
    # EqualityFilter, ComparisonFilter, InFilter, LikeFilter
    return [r for r in records if match(r, filter)]
```

Operators suportados: mesmos do contract (`gte`, `gt`, `lte`, `lt`, `ne`, `in`, `like`).

- `like` com `%` → converter pra regex `.*` e aplicar case-insensitive.

## Thresholds

Dois níveis de sinalização (sem bloquear o fluxo a não ser no hard limit):

- **Soft warning — 5k rows:** Logar aviso no retorno da skill:
  `"💾 Tabela <table> tem {n} linhas. CSV começa a ficar lento a partir de 5k. Considere migrar pra Sheets ou Supabase via /dna migrar-storage (v0.2+)."`
  Adapter **não raise** — apenas loga.
- **Hard limit — 50k rows:** Adapter **raise `StorageQuotaExceeded`**:
  `"CSV atingiu 50k linhas em <table> (hard limit). Migre pra Supabase via /setup-projeto antes de continuar escrevendo."`

O parse de toda a tabela em memória é O(N). Em 5k rows ainda é aceitável pra maioria dos filtros; 50k começa a passar de 1s de latência por operação em máquinas comuns.

## Mapeamento erros

| Situação | Erro retornado |
|---|---|
| Arquivo `<table>.csv` não existe em `read_*` | **Não raise** — retorna `[]` (tabela vazia é estado válido) |
| Arquivo `<table>.csv` não existe em `read_one_*` | `StorageNotFound` |
| Arquivo `<table>.csv` corrompido (CSV malformado, header sem colunas do contract) | `StorageBackendUnavailable("CSV corrompido em {path}: {erro}")` |
| Arquivo em `texts/` referenciado por `*_file` não existe no read | `StorageBackendUnavailable("Arquivo referenciado {path} não existe. CSV e texts/ fora de sincronia — rode /dna storage-doctor (v0.3+)")` |
| Write sem permissão (filesystem read-only) | `StorageReadOnly("Permissão negada em {path}")` |
| id duplicado na CSV (violação de invariante) | `StorageBackendUnavailable("id duplicado detectado em <table> — CSV corrompida")` |
| Campo obrigatório faltando no record de write | `StorageValidationError("Campo obrigatório {nome} ausente no write_<table>")` |
| Tabela com > 50k rows | `StorageQuotaExceeded("Tabela <table> atingiu 50k linhas — hard limit")` |

## Validação do contract

Os 7 records do contract devem ter `.csv` correspondente com header que bate:

- `competitors.csv`
- `competitor_posts.csv`
- `content_pipeline.csv`
- `my_content.csv`
- `ad_library.csv`
- `adaptive_models.csv`
- `generated_scripts.csv`

Headers derivados do `contract.md` §Estruturas de dados. Campos longos (ver D2) viram colunas `*_file` na CSV.

## Dicas de manutenção

- **Abrir no Excel/Numbers/Sheets (desktop):** funciona nativamente, empresário valida dados sem saber o que é CSV. Aviso: editar e salvar pode perder precisão de datetime/JSON — prefira fazer alterações via skill.
- **Versionar no git:** `data/*.csv` + `data/texts/**/*` são só texto. `git diff` mostra exatamente o que mudou.
- **Backup:** qualquer cópia de `data/` preserva tudo. rsync, Time Machine, Git, zip.
- **Migração CSV → Sheets/Supabase:** skill `/dna migrar-storage` (v0.2+) lê CSV e reescreve no destino.

## Quando migrar pra Sheets/Supabase

- **5k rows em qualquer tabela:** soft warning. Ainda dá, mas o Excel já abre devagar e skill loga aviso a cada operação.
- **50k rows:** hard limit. Skill passa a raise. Precisa migrar.
- **Precisa SQL complexo (ex: analista-conteudo):** já precisa Supabase, independente de tamanho.
- **Colaboração em tempo real (múltiplos operadores editando ao mesmo tempo):** Sheets é o ponto — git/CSV sofre merge conflict.

Caminhos de migração:
- `/dna migrar-storage sheets` ou `/dna migrar-storage supabase` (skill futura v0.2+) — automático
- Manual: importar cada `.csv` na planilha/Supabase correspondente; `texts/*` viram colunas TEXT inline no Supabase (cabe) ou continuam arquivo-referência no Sheets.
