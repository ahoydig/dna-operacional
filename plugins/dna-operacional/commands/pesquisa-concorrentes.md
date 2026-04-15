---
description: Descobre criadores e marcas concorrentes no Instagram do teu nicho e popula competitors + competitor_posts. Instagram-first exclusivo. Use quando digitar "/pesquisa-concorrentes", "mapear concorrentes", "analisar concorrência IG".
argument-hint: "[seed-handle?]"
---

# /pesquisa-concorrentes — Inteligência de Conteúdo Instagram

> Público: empreendedor brasileiro. Zero jargão de dev. PT-BR sempre.

## Pré-check: APIs necessárias

Antes de executar, verificar tokens/configs obrigatórios:

### APIFY_TOKEN

Se `$APIFY_TOKEN` ausente:

```
❌ APIFY_TOKEN não configurado.

Pra configurar (3 passos):

1. Acessa https://console.apify.com/account#/integrations e copia teu Personal API token
2. Adiciona em ~/.zshrc:
     export APIFY_TOKEN='apify_api_XXXX...'
3. Reload shell:
     source ~/.zshrc

Depois rode a skill de novo. Guia completo: docs/APIS-EXTERNAS.md#apify
```

Abortar execução até fix.

## ⚠️ Escopo: conteúdo orgânico, não prospecção B2B

Esta skill descobre **criadores e marcas do teu nicho pra estudar hooks, ângulos e pilares** — inteligência de conteúdo. Não é pra montar lista fria B2B (CNPJ, Google Maps, cold outreach).

Se o user pedir lista B2B ("quero 500 clínicas pra prospectar"), parar e redirecionar:
> "Isso é caso de uma skill de prospecção B2B (via CNAE/Google Maps). Esta skill foca em inteligência de conteúdo no Instagram. Quer seguir com essa mesmo assim?"

## Padrão de autenticação Apify

Mesmo bloco de `${APIFY_TOKEN}` descrito em `/pesquisa-diaria`: env → `.env` do projeto → erro com instruções. Em resumo:

```bash
if [ -z "$APIFY_TOKEN" ] && [ -f .env ]; then
  set -a; source .env; set +a
fi
[ -z "$APIFY_TOKEN" ] && echo "❌ APIFY_TOKEN não encontrado. Exporta em ~/.zshenv ou adiciona no .env" && exit 1
```

---

## Passo 1: Contexto

Ler `CLAUDE.md` do projeto:
- `nicho` + `sub_nicho` (pra focar a busca)
- Seção `## Handles Multi-Plataforma` — handles próprios do user (pra **nunca se auto-adicionar** como concorrente)
- `## Storage Backend` (pra persistir depois)
- Sazonalidade do nicho — se há janela ativa, priorizar concorrentes que publicam nela

Se `## Storage Backend` ausente, abortar com:
> "⚠️ Backend de storage não configurado. Rode `/setup-projeto` pra escolher (Supabase / Google Sheets / Markdown)."

## Passo 2: Detectar intenção

Antes de qualquer scraping, verificar palavras na solicitação do user:

**Se contiver:** "prospecção", "leads", "CSV", "empresas pra vender", "captação", "cold outreach", "lista fria", "CNPJ", "endereço" →

**PARAR imediatamente** e avisar:
> "Pelo que descreveu parece que quer uma lista B2B pra prospecção — essa skill foca em inteligência de conteúdo no Instagram, não em lista fria. Quer seguir mesmo assim?"

**Senão** → prosseguir.

## Passo 3: Concorrentes seed

Se o argumento `[seed-handle?]` veio preenchido, usar como primeiro seed. Senão:

Via `AskUserQuestion`:
> "Me fala 3-5 concorrentes que você já conhece de cabeça no nicho [X]."

Se o user não souber nenhum: "Tudo bem, vou descobrir a partir de hashtags. Só confirma: teu nicho é [X], certo?"

## Passo 4: Descoberta multi-fonte (foco Instagram)

Rodar as 3 fontes abaixo pra montar lista de candidatos.

### Fonte A — WebSearch direcionado BR

Queries:
- `"top criadores instagram [nicho] brasil"`
- `"maiores perfis [nicho] brasileiro"`
- `"quem seguir [nicho] no instagram"`
- `"melhores [nicho] pra seguir instagram"`

Extrair @s mencionados, eliminar duplicatas com seeds.

### Fonte B — Apify Instagram Hashtag Scraper

Actor: `apify/instagram-hashtag-scraper`

Hashtags BR do nicho (montar a partir do CLAUDE.md):
- `#[nicho]brasil`
- `#[nicho]br`
- `#[variação-do-nicho]`

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~instagram-hashtag-scraper/run-sync-get-dataset-items?token=${APIFY_TOKEN}&timeout=180" \
  -H "Content-Type: application/json" \
  -d '{"hashtags": ["[nicho]brasil", "[nicho]br"], "resultsType": "posts", "resultsLimit": 50}'
```

Extrair os @ que mais aparecem nos top posts das últimas 2 semanas.

### Fonte C — Busca lateral via Similar Accounts

Pra cada concorrente seed, chamar Apify Instagram Profile Scraper e extrair o campo "similar accounts" (se o actor retornar esse dado). Descobre perfis relacionados por afinidade de audiência que nenhuma busca manual encontra.

---

## Passo 4.5: Dedup via storage (antes de validar)

Antes de tentar adicionar, consultar o backend pra evitar reprocessamento:

```
existentes = storage.read_competitors({nicho: '<nicho do CLAUDE.md>'})
handles_ja_registrados = [c.instagram_username for c in existentes]
candidatos_novos = [h for h in descobertos if h not in handles_ja_registrados]
```

## Passo 5: Validação e priorização BR

Pra cada candidato novo:
1. `WebSearch` confirma o @ oficial (ex: "instagram [nome]" pra pegar o @ exato)
2. Verifica **localidade BR**: bio tem cidade BR / usa R$ / posta em PT-BR
3. **Prioridade:** concorrentes BR entram primeiro; internacionais só se o nicho é global

## Passo 6: Enriquecimento via Apify Instagram Profile Scraper

Actor: `apify/instagram-profile-scraper`

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token=${APIFY_TOKEN}&timeout=180" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["perfil1", "perfil2", "perfil3"]}'
```

Extrair de cada perfil:
- `foto` (campo `avatarUrl` ou `profilePicUrl`)
- `followers_count`
- `instagram_profile_url` (URL verificada)
- bio completa → deduzir `sub_nicho` + detectar idioma (PT = BR, outro = internacional)

**LGPD:** não salvar email, telefone, endereço físico nem CPF — só dados públicos de perfil.

## Passo 7: Upsert em competitors

Pra cada perfil enriquecido, chamar o storage layer (`lib/storage/contract.md`):

```
storage.upsert_competitor({
  name: '[nome da marca ou criador]',
  instagram_username: '[@handle sem @]',
  instagram_profile_url: '[URL verificada]',
  followers_count: <número>,
  foto: '[URL da foto de perfil]',
  nicho: '[nicho do CLAUDE.md]',
  sub_nicho: '[sub_nicho deduzido da bio]'
}, key='instagram_username')
```

O `upsert` com `key='instagram_username'` garante que re-rodadas atualizam em vez de duplicar. Adapter (`supabase.md`/`sheets.md`/`markdown.md`) traduz pro runtime nativo. **Nunca escrever SQL inline aqui** — regra ferro do contract.

**Erros possíveis:**
- `StorageBackendUnavailable` → avisar: "Backend configurado ({backend}) não tá acessível. Verifica credenciais no `CLAUDE.md`."
- `StorageQuotaExceeded` → sugerir `/dna migrar-storage` (v0.2+)

## Passo 8: Scraping de posts (opcional — confirmar custo)

Via `AskUserQuestion`:
> "Achei {N} concorrentes. Quer que eu puxe os posts recentes (últimos 30 dias) de cada um pra analisar hooks e ângulos? Vai custar ~R$ {estimativa} em Apify. Bora?"

**Estimativa de custo:** ~R$ 0,50-1,00 por perfil (depende de volume de posts). Calcular com base em N concorrentes × 30 posts cada.

Se SIM, rodar Apify `apify/instagram-post-scraper`:

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~instagram-post-scraper/run-sync-get-dataset-items?token=${APIFY_TOKEN}&timeout=300" \
  -H "Content-Type: application/json" \
  -d '{"directUrls": ["https://www.instagram.com/perfil1/", "https://www.instagram.com/perfil2/"], "resultsType": "posts", "resultsLimit": 30}'
```

Pra cada post, fazer análise agêntica — **NUNCA traduzir, manter literal PT-BR**:
- `hook` — primeiras palavras da legenda OU primeiros 3 segundos do vídeo (transcrever literal)
- `hook_visual` — o que aparece na tela (thumbnail, texto sobreposto, cenário)
- `angulo` — tipo de enquadramento: "contrário", "tutorial", "vitrine", "emocional", "polêmica", "gambiarra"
- `pilar` — tema principal (ex: "nutrição funcional", "automação n8n", "tráfego pago")
- `categoria` — formato de conteúdo (ex: "lista", "comparação", "antes e depois")
- `formato` — Reel / Carrossel / Foto

Upsert em `competitor_posts`:

```
storage.upsert_competitor_post({
  competitor_id: <id retornado do upsert_competitor>,
  platform: 'instagram',
  post_url: '[URL do post]',
  post_code: '[shortcode do post]',
  published_at: '[timestamp UTC]',
  likes: <likes>,
  comments: <comments>,
  video_views: <views, se vídeo>,
  transcription: '[transcrição se vídeo]',
  hook: '[hook literal PT-BR]',
  hook_visual: '[descrição visual]',
  angulo: '[angulo]',
  pilar: '[pilar]',
  categoria: '[categoria]',
  formato: '[Reel|Carrossel|Foto]'
}, key=['competitor_id', 'post_code'])
```

A chave composta `['competitor_id', 'post_code']` garante dedup — mesmo post do mesmo concorrente nunca duplica.

## Passo 9: Resumo final

Se `/humanizer` instalado (plugin v0.2+), humanize antes de apresentar:

```
🔥 CONCORRENTES ADICIONADOS

✅ {N_total} perfis salvos
   - {N_BR} brasileiros
   - {N_internacional} internacionais

📸 {N_posts} posts analisados (últimos 30 dias)

🎯 Os 3 hooks que mais bombaram no teu nicho:
1. "[hook literal PT-BR]"
2. "[hook literal PT-BR]"
3. "[hook literal PT-BR]"
```

---

## Regras

1. **NUNCA usa fontes de prospecção B2B** (CNAE, Google Maps) — skills de lista B2B vivem fora deste plugin
2. **NUNCA exporta CSV** — escopo é inteligência de conteúdo, não prospecção
3. **Sempre prioridade BR** — perfis brasileiros entram antes de internacionais
4. **Hooks literais PT-BR** — nunca traduzir, copiar exatamente como aparece
5. **LGPD-aware** — nunca salva endereço físico, telefone, email de PF, CPF
6. **Confirmar custo Apify** antes de scraping de posts (Passo 8)
7. **Upsert ativo** — re-run da skill atualiza em vez de duplicar (key em `instagram_username` e `['competitor_id','post_code']`)
8. **Output final via `/humanizer`** se disponível
9. **Detectar B2B antes de qualquer scraping** — salva tempo e Apify credits
10. **Nunca escrever SQL inline** — sempre via `storage.<op>_<table>()` do contract

---

## Fim da execução — bloco "Próximos Passos"

Após upsert concluído, apresentar:

```
✅ Pesquisa de concorrentes finalizada: {N} competitors + {N_posts} posts no {backend}.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /raio-x-ads-concorrentes — briefing dos ads (precisa /coletar-anuncios v0.2)
  2. /analista-conteudo        — calibra benchmarks vs tua performance

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Fallback ASCII** (terminais sem unicode):

```
----------------------------------------
>>> PROXIMOS PASSOS SUGERIDOS
----------------------------------------
  1. /raio-x-ads-concorrentes - briefing ads (v0.2)
  2. /analista-conteudo        - calibra benchmarks

  >>> /dna pra ver todas
----------------------------------------
```
