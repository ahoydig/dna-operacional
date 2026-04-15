# Storage Contract — DNA Operacional

Fonte da verdade da API abstrata de storage. **Todos os adapters (supabase/sheets/markdown) implementam este contrato exato.** Skills consumidoras nunca leem um adapter direto — seguem o contract aqui.

## Estruturas de dados (tabelas)

Sete estruturas definidas. Cada adapter armazena no formato apropriado (tabela SQL, aba de planilha, pasta de .md).

### `competitors`

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | int (autogen) | sim | PK |
| `name` | string | sim | Nome público |
| `instagram_username` | string | sim | `@handle` sem o @ |
| `instagram_profile_url` | string | sim | URL completa |
| `followers_count` | int | não | Atualizado via scrape |
| `foto` | string | não | URL avatar |
| `nicho` | string | não | Nicho principal |
| `sub_nicho` | string | não | Sub-nicho |
| `avg_engagement_coefficient` | float | não | Média calculada |
| `posts_analyzed_count` | int | não | Quantos posts já raspados |
| `last_avg_update` | datetime | não | Última recalibração |
| `created_at` | datetime (autogen) | sim | Timestamp insert |
| `updated_at` | datetime (autoupdate) | sim | Timestamp última edição |

### `competitor_posts`

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | int (autogen) | sim | PK |
| `competitor_id` | int | sim | FK → competitors.id |
| `platform` | string | sim | "instagram" \| "tiktok" \| "youtube" |
| `post_url` | string | sim | URL pública |
| `post_code` | string | sim | Shortcode/ID na plataforma |
| `published_at` | datetime | não | Data publicação |
| `likes` | int | não | Curtidas |
| `comments` | int | não | Comentários |
| `video_views` | int | não | Views (se vídeo) |
| `transcription` | text | não | Transcrição áudio |
| `hook` | text | não | Hook verbal extraído |
| `hook_visual` | text | não | Descrição primeiros 3 segs visuais |
| `angulo` | string | não | Ângulo narrativo |
| `pilar` | string | não | Pilar de conteúdo |
| `categoria` | string | não | Categoria |
| `formato` | string | não | Reel/Carrossel/Post estático |
| `engagement_score` | float | não | Score normalizado |

### `content_pipeline`

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | int (autogen) | sim | PK |
| `title` | string | sim | Título resumido |
| `status` | enum | sim | "Ideia" \| "Pesquisado" \| "Roteirizado" \| "Gravado" \| "Publicado" \| "Arquivado" |
| `source` | string | não | Onde veio (pesquisa-diaria, manual, outro) |
| `source_url` | string | não | Link original se aplicável |
| `topic` | string | não | Tema central |
| `angulo` | string | não | Ângulo narrativo |
| `hook_suggestion` | text | não | Hook sugerido |
| `motivo_video` | text | não | Por que esse vídeo importa |
| `research_brief` | text | não | Briefing de pesquisa |
| `format` | string | não | Reel/Carrossel/Stories |
| `archetype` | string | não | Arquétipo narrativo |
| `platform` | string | não | instagram/tiktok/youtube |
| `variant_of` | int | não | FK → content_pipeline.id (se é variação) |
| `published_content_id` | int | não | FK → my_content.id após publicar |
| `created_at` | datetime (autogen) | sim | |
| `updated_at` | datetime (autoupdate) | sim | |

### `my_content`

> Estrutura herdada da Rodada 1 (skills já existentes do Flávio).

Campos canônicos: `id, post_url, post_code, platform, published_at, likes, comments, saves, shares, video_views, reach, impressions, hook, topic, pilar, formato, archetype, transcript, created_at, updated_at`.

### `ad_library`

> Estrutura herdada da Rodada 1. Populada pela skill futura `coletar-anuncios` (v0.2).

Campos canônicos: `id, competitor_id (FK), ad_id_meta, headline, primary_text, cta, image_url, video_url, landing_page_url, started_at, last_seen_at, running_days, countries, ad_format, created_at, updated_at`.

### `adaptive_models` (NOVO v0.1.0)

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | int (autogen) | sim | PK |
| `source_video_url` | string | sim | Vídeo de referência analisado |
| `hook_visual` | text | sim | Descrição primeiros 3 segs |
| `hook_falado` | text | sim | Hook verbal |
| `structure_json` | json/text | sim | Estrutura narrativa extraída |
| `arquetipo` | string | não | Arquétipo detectado |
| `formato` | string | não | Reel/Short/TikTok |
| `duracao` | int | não | Segundos |
| `transcript` | text | não | Transcrição completa |
| `frame_analysis_json` | json/text | não | Análise frame-by-frame |
| `created_at` | datetime (autogen) | sim | |

### `generated_scripts` (NOVO v0.1.0)

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | int (autogen) | sim | PK |
| `adaptive_model_id` | int | sim | FK → adaptive_models.id |
| `tema` | string | sim | Tema do roteiro |
| `hook` | text | sim | Hook adaptado |
| `body` | text | sim | Corpo do roteiro |
| `cta` | text | não | Call to action |
| `formato` | string | não | Reel/Short |
| `duracao_target` | int | não | Segundos alvo |
| `voz_handle` | string | não | `@handle` da voz usada |
| `created_at` | datetime (autogen) | sim | |

## Operations (API)

**7 operations por estrutura.** Ex pra `competitors` (replicar pros demais).

| Operação | Assinatura | Retorno | Erros possíveis |
|---|---|---|---|
| `read_competitors(filters?)` | `filters: Filter?` | `Competitor[]` | `StorageBackendUnavailable` |
| `read_one_competitor(id)` | `id: int` | `Competitor` | `StorageNotFound`, `StorageBackendUnavailable` |
| `write_competitor(record)` | `record: CompetitorInput` | `int` (novo id) | `StorageBackendUnavailable`, `StorageQuotaExceeded` |
| `update_competitor(id, patch)` | `id: int, patch: CompetitorPatch` | `bool` | `StorageNotFound`, `StorageBackendUnavailable` |
| `upsert_competitor(record, key)` | `record, key: string` | `int` (id do existente ou novo) | `StorageBackendUnavailable` |
| `delete_competitor(id)` | `id: int` | `bool` | `StorageNotFound`, `StorageReadOnly` |
| `count_competitors(filters?)` | `filters: Filter?` | `int` | `StorageBackendUnavailable` |

Repetir o padrão pras 6 outras estruturas: `competitor_posts`, `content_pipeline`, `my_content`, `ad_library`, `adaptive_models`, `generated_scripts`.

**Operação especial (Supabase-only):**

| Operação | Uso | Backend | Comportamento em outros |
|---|---|---|---|
| `execute_sql(query)` | Queries SQL arbitrárias (CTEs, window functions) | Supabase | Aborta com `StorageBackendUnavailable("SQL queries require Supabase backend. Current: <backend>. Switch via /setup-projeto ou aguarde v0.3.")` |

Usada APENAS por `analista-conteudo` que precisa SQL complexo. Documentada como exceção.

## Filter DSL (universal)

Todas operations `read_*` / `count_*` aceitam filtro opcional. DSL uniforme entre backends.

### Equality (simples)

```python
storage.read_competitors({nicho: "fitness"})
# → WHERE nicho = 'fitness' (Supabase)
# → filtra linhas da aba competitors onde col nicho == 'fitness' (Sheets)
# → lista arquivos em data/competitors/ onde frontmatter.nicho == 'fitness' (MD)
```

### Comparação (gte/gt/lte/lt/ne)

```python
storage.read_competitors({followers_count: {op: "gte", value: 10000}})
storage.read_competitors({created_at: {op: "gte", value: "2026-01-01"}})
```

Operators suportados: `gte`, `gt`, `lte`, `lt`, `ne`.

### In list

```python
storage.read_competitor_posts({formato: {op: "in", value: ["reel", "tiktok"]}})
```

### Partial match (like)

```python
storage.read_competitors({name: {op: "like", value: "%Nike%"}})
```

`%` é wildcard. Case-insensitive por default (ILIKE no Supabase, equiv nos outros).

### Combinações

```python
storage.read_competitors({
  _and: [
    {nicho: "fitness"},
    {followers_count: {op: "gte", value: 50000}},
    {_or: [
      {sub_nicho: "crossfit"},
      {sub_nicho: "musculacao"}
    ]}
  ]
})
```

## Errors (hierarquia)

| Erro | Quando ocorre | Ação recomendada da skill |
|---|---|---|
| `StorageNotFound` | `read_one_*(id)` ou `update_*(id, ...)` onde id não existe | Mensagem amigável ao user: "Registro {id} não encontrado" |
| `StorageBackendUnavailable` | Supabase offline, Sheets sem permissão, MD pasta não existe | Orientar: "Verifique o backend configurado no CLAUDE.md" |
| `StorageQuotaExceeded` | Sheets 10k rows/aba, MD 100+ items por pasta (soft warning) | Sugerir migração: "Backend atingiu limite. Considere /dna migrar-storage (v0.2+)" |
| `StorageReadOnly` | Backend em modo read-only (ex: planilha sem permissão write) | "Backend em modo leitura. Ajuste permissões." |

## Type aliases (reference)

```
type Filter = EqualityFilter | ComparisonFilter | InFilter | LikeFilter | CompositeFilter

type EqualityFilter = { [field: string]: string | number | boolean }
type ComparisonFilter = { [field: string]: { op: "gte"|"gt"|"lte"|"lt"|"ne", value: any } }
type InFilter = { [field: string]: { op: "in", value: any[] } }
type LikeFilter = { [field: string]: { op: "like", value: string } }
type CompositeFilter = { _and: Filter[] } | { _or: Filter[] }

type Record = { [field: string]: any }
type RecordPatch = Partial<Record>
```

## Regra ferro

> **Nenhuma skill escreve SQL inline.** Única exceção: `analista-conteudo` via `execute_sql()`.
> Em code reviews: grep `SELECT \|INSERT \|UPDATE \|DELETE ` em `skills/*/SKILL.md` deve retornar 0.
