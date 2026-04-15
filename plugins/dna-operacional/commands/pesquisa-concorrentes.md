---
description: Descobre criadores e marcas concorrentes no Instagram do teu nicho e popula competitors + competitor_posts. Instagram-first exclusivo. Use quando digitar "/pesquisa-concorrentes", "mapear concorrentes", "analisar concorrência IG".
argument-hint: "[seed-handle?]"
---

# /pesquisa-concorrentes — Inteligência de Conteúdo Instagram

> Público: empreendedor brasileiro. Zero jargão de dev. PT-BR sempre.

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
- Sazonalidade do nicho — se há janela ativa, priorizar concorrentes que publicam nela

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

## Passo 5: Validação e priorização BR

Pra cada candidato descoberto:
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

## Passo 7: INSERT em competitors

```sql
INSERT INTO public.competitors (
  name, instagram_username, instagram_profile_url,
  followers_count, foto, nicho, sub_nicho
) VALUES (
  '[nome da marca ou criador]',
  '[@handle sem @]',
  '[URL verificada]',
  [número],
  '[URL da foto de perfil]',
  '[nicho do CLAUDE.md]',
  '[sub_nicho deduzido da bio]'
)
ON CONFLICT (instagram_username) DO UPDATE SET
  followers_count = EXCLUDED.followers_count,
  foto = EXCLUDED.foto,
  sub_nicho = EXCLUDED.sub_nicho,
  updated_at = now();
```

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

INSERT em `competitor_posts`:

```sql
INSERT INTO public.competitor_posts (
  competitor_id, platform, post_url, post_code,
  published_at, video_views, likes, comments,
  transcription, hook, hook_visual, angulo, pilar, categoria, formato
) VALUES (
  [id do competitor],
  'instagram',
  '[URL do post]',
  '[shortcode do post]',
  '[timestamp em UTC]',
  [views],
  [likes],
  [comments],
  '[transcrição se vídeo]',
  '[hook literal PT-BR]',
  '[descrição visual]',
  '[angulo]',
  '[pilar]',
  '[categoria]',
  '[formato]'
);
```

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
7. **ON CONFLICT ativo** — re-run da skill atualiza dados em vez de duplicar
8. **Output final via `/humanizer`** se disponível
9. **Detectar B2B antes de qualquer scraping** — salva tempo e Apify credits
