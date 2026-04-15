# Template Google Sheets — DNA Operacional

Instruções pra preparar a planilha que o backend `sheets` usa.

## Setup em 3 passos

### 1. Criar planilha nova no Drive

- Acesse https://sheets.new (abre planilha vazia)
- Renomeie pra: `dna-operacional-data`

### 2. Criar as 7 abas com headers

Crie 7 abas (tab no rodapé → +). Copie os headers abaixo pra linha 1 de cada aba (separados por TAB no copy-paste):

#### Aba `competitors`

```
id	name	instagram_username	instagram_profile_url	followers_count	foto	nicho	sub_nicho	avg_engagement_coefficient	posts_analyzed_count	last_avg_update	created_at	updated_at
```

#### Aba `competitor_posts`

```
id	competitor_id	platform	post_url	post_code	published_at	likes	comments	video_views	transcription	hook	hook_visual	angulo	pilar	categoria	formato	engagement_score
```

#### Aba `content_pipeline`

```
id	title	status	source	source_url	topic	angulo	hook_suggestion	motivo_video	research_brief	format	archetype	platform	variant_of	published_content_id	created_at	updated_at
```

#### Aba `my_content`

```
id	post_url	post_code	platform	published_at	likes	comments	saves	shares	video_views	reach	impressions	hook	topic	pilar	formato	archetype	transcript	created_at	updated_at
```

#### Aba `ad_library`

```
id	competitor_id	ad_id_meta	headline	primary_text	cta	image_url	video_url	landing_page_url	started_at	last_seen_at	running_days	countries	ad_format	created_at	updated_at
```

#### Aba `adaptive_models`

```
id	source_video_url	hook_visual	hook_falado	structure_json	arquetipo	formato	duracao	transcript	frame_analysis_json	created_at
```

#### Aba `generated_scripts`

```
id	adaptive_model_id	tema	hook	body	cta	formato	duracao_target	voz_handle	created_at
```

### 3. Colar o ID da planilha no CLAUDE.md do projeto

Copie o ID da URL. Exemplo:
- URL: `https://docs.google.com/spreadsheets/d/1aBc123XYZ/edit#gid=0`
- ID: `1aBc123XYZ`

Adicione em `CLAUDE.md` do teu projeto:

```markdown
## Storage Backend: sheets

- spreadsheet_id: 1aBc123XYZ
```

Pronto. Skills de dados vão escrever/ler desta planilha.

## Dica: template público (futuro)

Se o criador publicar um template oficial copiável, este arquivo será atualizado com o link "File → Make a copy". Por enquanto, setup manual acima é a forma canônica.

## Limites a ter em mente

- Google Sheets API: **60 req/min por user** — operações pesadas (muitos `upsert`) podem bater rate limit
- Capacidade prática: **~10k rows por aba** antes de ficar lento — migrar pra Supabase via `/dna migrar-storage` (v0.2+) quando passar disso
- Backup: Google Drive faz automático, mas considere exportar .xlsx/.csv periodicamente
