---
description: Análise de performance do TEU conteúdo via SQL em 14 seções com KPIs brasileiros (saves > shares > comments > likes > views). Requer my_content populada no Supabase (storage backend = supabase). Use quando digitar "/analista-conteudo", "análise do feed", "performance dos posts", "top conteúdos".
argument-hint: "[period?]"
---

Usuário invocou `/analista-conteudo` com argumento: `$ARGUMENTS`

# /analista-conteudo — Raio-X do Teu Conteúdo

> Segue a voz do projeto (via humanizer). Público: definido em `reference/avatar.md`. Zero jargão de dev.

Você é analista de performance do conteúdo do criador. **Escopo:** apenas o conteúdo publicado pelo próprio user (handles da Brand Config do CLAUDE.md do projeto). **Fora do escopo:** análise de concorrentes (`/pesquisa-concorrentes`) e tendências de mercado (`/pesquisa-diaria`).

---

## Setup: Ler Contexto do Projeto

**Antes de rodar qualquer consulta, leia o `CLAUDE.md` do projeto** pra obter:
- Seção `## Brand Config` (plataformas e handles do user)
- Seção `## Pilares de conteúdo`
- Seção `## Sazonalidade do Nicho`
- Ordem de prioridade de KPIs (default BR: saves > shares > comments > likes > views)

Os handles serão usados em todas as cláusulas `WHERE handle IN (...)`.

Se `my_content` estiver vazia, parar e orientar:

> "Tua tabela `my_content` tá vazia. Pra eu analisar, precisa popular ela primeiro. Opções:
> 1. INSERT manual via SQL (te ajudo a montar)
> 2. Importar de CSV se tem export do Instagram Insights
> 3. Script de integração Instagram Graph API (skill futura `popular-my-content`)
>
> Qual caminho?"

---

## Como calcular outlier BR (KPIs calibrados)

**Por que não só views:** no Brasil, o feed do Instagram pesa saves e shares como sinal forte de valor. Views são infladas por autoplay. Um Reel com 10k views e 800 saves vale MUITO mais que um com 50k views e 50 saves.

**Outlier BR = multi-KPI em cascata:**
- `saves >= 2x AVG(saves)`
- OU `shares >= 2x AVG(shares)`
- OU `(views >= 2x AVG AND comments >= 1.5x AVG)`

**Ordenação de outliers — sempre:** `saves DESC, shares DESC, comments DESC, views DESC`

**Filtro padrão:** `views >= 200` (corta ruído de posts sem tração mínima). **NÃO filtrar por idade do post** — visão completa.

---

## Execução: 14 Seções em Ordem

Roda em paralelo quando possível. Cada query usa o CTE padrão:

```sql
-- CTE padrão "avgs" (reutilizado em quase todas seções)
WITH avgs AS (
  SELECT platform,
    AVG(views)    AS avg_views,
    AVG(saves)    AS avg_saves,
    AVG(shares)   AS avg_shares,
    AVG(comments) AS avg_comments
  FROM public.my_content
  WHERE handle IN ({handles_do_criador})
    AND views >= 200
  GROUP BY platform
)
```

Nas seções abaixo, referencio `avgs` sem repetir a CTE.

---

### Seção 1: Visão Geral de Performance

Cross-platform + breakdown mensal em timezone BR:

```sql
-- 1a: Geral por plataforma
[CTE avgs padrão]
SELECT c.platform, COUNT(*) AS total_videos,
  ROUND(AVG(c.views)::numeric, 0) AS avg_views,
  SUM(c.views) AS total_views, MAX(c.views) AS max_views,
  SUM(CASE WHEN c.saves >= a.avg_saves * 2 OR c.shares >= a.avg_shares * 2
        OR (c.views >= a.avg_views * 2 AND c.comments >= a.avg_comments * 1.5)
       THEN 1 ELSE 0 END) AS outliers,
  ROUND(100.0 * [mesma condição] / COUNT(*)::numeric, 1) AS outlier_rate,
  ROUND(AVG(c.saves)::numeric, 0) AS avg_saves,
  ROUND(AVG(c.shares)::numeric, 0) AS avg_shares,
  ROUND(AVG(c.comments)::numeric, 0) AS avg_comments
FROM public.my_content c
JOIN avgs a ON c.platform = a.platform
WHERE c.handle IN ({handles_do_criador}) AND c.views >= 200
GROUP BY c.platform
ORDER BY total_views DESC
```

```sql
-- 1b: Mês a mês por plataforma (timezone BR)
[CTE avgs] ...
GROUP BY c.platform, TO_CHAR(c.published_at AT TIME ZONE 'America/Sao_Paulo', 'YYYY-MM')
```

**Formato de saída:** tabela `| Plataforma | Vídeos | Média Views | Total Views | Máx | Outliers | Taxa | Média Saves | Média Shares | Média Comments |` + tendência mensal com ↑↓→.

---

### Seção 2: Performance de Estrutura de Hook

```sql
[CTE avgs]
SELECT c.spoken_hook_structure AS hook_structure, COUNT(*) AS videos,
  ROUND(AVG(c.views)::numeric, 0) AS avg_views, SUM(c.views) AS total_views,
  SUM(CASE WHEN [regra outlier BR] THEN 1 ELSE 0 END) AS outliers,
  ROUND(100.0 * [...] / NULLIF(COUNT(*), 0)::numeric, 1) AS outlier_rate
FROM public.my_content c JOIN avgs a ON c.platform = a.platform
WHERE c.handle IN ({handles_do_criador}) AND c.views >= 200
  AND c.spoken_hook_structure IS NOT NULL
GROUP BY c.spoken_hook_structure HAVING COUNT(*) >= 3
ORDER BY outlier_rate DESC, avg_views DESC
```

**Output:** tabela rankeada + "o que funciona / o que não funciona" com top/bottom 2-3.

---

### Seção 3: Top 20 Frameworks de Hook

```sql
[CTE avgs]
SELECT c.spoken_hook_framework, c.spoken_hook, c.views, c.saves, c.shares,
  ROUND((c.views / a.avg_views)::numeric, 1) AS outlier_score,
  c.spoken_hook_structure, c.platform, c.visual_format, c.text_hook, c.topic, c.post_url
FROM public.my_content c JOIN avgs a ON c.platform = a.platform
WHERE c.handle IN ({handles_do_criador}) AND c.views >= 200
ORDER BY c.saves DESC, c.shares DESC, c.views DESC
LIMIT 20
```

**IMPORTANTE:** `spoken_hook_framework` é o **template reutilizável** (TÍTULO no output). `spoken_hook` é a **instância específica** (exemplo). Framework > hook pra reprodução. Se framework for NULL, anotar "Sem framework marcado."

Após os 20: analisar padrões — quais frameworks repetem, palavras que dominam, estruturas dominantes, tópicos dominantes.

---

### Seção 4: Análise de Alinhamento de Hooks

3-5 comparações SEPARADAS onde vídeos quase idênticos (mesmo hook/tópico) tiveram performance diferente. Dentro da plataforma primeiro, depois cross-platform.

**Passo 1:** top 5 vencedores por plataforma (BR-calibrado). **Passo 2:** pra cada vencedor, buscar vídeos com palavras-chave similares via ILIKE. **Passo 3:** escolher comparações válidas.

**Output:** `VENCEDOR` vs `UNDERPERFORMER` com falado, texto, visual, URL, e a **DIFERENÇA IDENTIFICADA** (qual variável específica mudou).

---

### Seção 5: Análise de Tópicos

3 queries: (5a) performance por tópico cross-platform, (5b) top 15 por total de views, (5c) bottom 15 (pare de fazer esses). Ambos com CTE avgs + `HAVING COUNT(*) >= 2` ou `>= 3`.

**Output:** melhores por taxa outlier, melhores por volume, piores. Insights: clusters, superutilizados underperforming, subexplorados de alta performance, combos tópico+hook vencedores.

---

### Seção 6: Análise de Text Hook

3 queries: (6a) top 30 text hooks, (6b) performance por `text_hook_layout`, (6c) por `text_hook_motion`.

**Output:** 3 tabelas + insight "hooks que ADICIONAM vs REPETEM o hook falado — qual performa melhor?"

---

### Seção 7: Performance de Formato Visual

2 queries: (7a) `visual_format`, (7b) `visual_hook_graphic`. Ambos com CTE avgs + outlier BR.

**Output:** rankings de formato e de graphic de hook visual.

---

### Seção 8: Performance de Duração

Buckets: `0-15`, `16-30`, `31-45`, `46-60`, `61-90`, `90+` segundos. GROUP BY faixa, ordena por outlier_rate DESC.

---

### Seção 9: Performance de Estrutura de Conteúdo

`content_structure` com CTE avgs + HAVING COUNT(*) >= 3.

---

### Seção 10: Deep Dives por Plataforma

**Crítico.** Pra CADA plataforma ativa do criador, rodar separadamente:

1. **Performance de estrutura de hook** por plataforma (subqueries de AVG por `platform = '{PLATAFORMA}'`).
2. **Top 5 vídeos** por plataforma (ordenado saves/shares/views).
3. **Performance de duração** por plataforma (buckets).

Hooks, formatos e durações funcionam diferente em cada lugar — breakdowns separados são obrigatórios.

---

### Seção 11: Rankings de Performance (Resumo Final)

**Output:**

```
### O Que Funciona (Dobrar a Aposta)
| Categoria | Top Performer | Por Quê |
| Estrutura de Hook | [X] | [taxa outlier]%, [avg saves] saves |
| Formato Visual | [X] | ... |
| Duração | [X] | ... |
| Estrutura de Conteúdo | [X] | ... |

### O Que Não Funciona (Reduzir ou Corrigir)
[mesmo formato]

### Recomendações por Plataforma
Instagram / TikTok / YouTube — melhor hook / duração / insight chave

### Insights Cross-Platform
- Qual conteúdo transfere bem
- Quais plataformas amplificam vs suprimem
```

---

### Seção 12: Brief pro Roteirista

Resumo **denso, acionável, legível por LLM** que alimenta `/roteiro-viral`. Formato:

```
### Fórmula Vencedora (maior probabilidade de outlier BR)
- Estrutura de hook: [X] ([X]% taxa outlier)
- Framework de hook: "[template]"
- Tópico: [X]
- Duração: [X] seg
- Estrutura de conteúdo: [X]
- Formato visual: [X]

### Regras de Hook (dos dados)
1. FAÇA: [padrão dos top 20]
2. NÃO FAÇA: [anti-padrão]

### Regras de Tópico
1. Tópicos quentes: [top 3-5 por outlier + volume]
2. Tópicos mortos: [bottom 3-5]
3. Subexplorados: [alta saves mas poucos vídeos]

### Top 5 Frameworks pra Reutilizar
1. "[template]" — [avg saves], [outlier rate]%
[...]
```

---

### Seção 13: Análise de Horário de Publicação GMT-3

**Por que importa:** algoritmo do IG favorece engajamento nas primeiras horas. Postar quando tua audiência tá ativa faz diferença. BR = GMT-3 (São Paulo, sem horário de verão desde 2019).

```sql
[CTE avgs]
-- Distribuição por hora do dia (timezone BR)
SELECT EXTRACT(HOUR FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') AS hora_br,
  c.platform, COUNT(*) AS videos,
  ROUND(AVG(c.views)::numeric, 0) AS avg_views,
  ROUND(AVG(c.saves)::numeric, 0) AS avg_saves,
  ROUND(AVG(c.shares)::numeric, 0) AS avg_shares,
  SUM(CASE WHEN [regra outlier BR] THEN 1 ELSE 0 END) AS outliers,
  ROUND(100.0 * [...] / NULLIF(COUNT(*), 0), 1) AS outlier_rate
FROM public.my_content c JOIN avgs a ON c.platform = a.platform
WHERE c.handle IN ({handles_do_criador}) AND c.views >= 200
  AND c.published_at IS NOT NULL
GROUP BY hora_br, c.platform
ORDER BY c.platform, outlier_rate DESC
```

```sql
-- Distribuição por dia da semana (timezone BR)
SELECT TO_CHAR(c.published_at AT TIME ZONE 'America/Sao_Paulo', 'Day') AS dia_semana,
  EXTRACT(DOW FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') AS dow_num,
  c.platform, COUNT(*) AS videos,
  ROUND(AVG(c.views)::numeric, 0) AS avg_views,
  ROUND(AVG(c.saves)::numeric, 0) AS avg_saves
FROM public.my_content c
WHERE c.handle IN ({handles_do_criador}) AND c.views >= 200
  AND c.published_at IS NOT NULL
GROUP BY dia_semana, dow_num, c.platform
ORDER BY c.platform, dow_num
```

**Output:** "Horário nobre do teu IG: [X]h — [X]% outlier (default BR: 19h-21h)". Melhor dia da semana. Recomendação prática.

---

### Seção 14: Análise Sazonal BR

**Por que importa:** janelas sazonais (Dia das Mães, Black Friday, Janeiro/metas) performam diferente. Separa sazonalidade de qualidade — evita confundir "conteúdo melhorou" com "foi só o período".

```sql
SELECT TO_CHAR(c.published_at AT TIME ZONE 'America/Sao_Paulo', 'YYYY-MM') AS mes_br,
  CASE
    WHEN EXTRACT(MONTH FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') = 1  THEN 'Janeiro (Metas/Recomeço)'
    WHEN EXTRACT(MONTH FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') = 5
     AND EXTRACT(DAY FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') <= 14  THEN 'Dia das Mães'
    WHEN EXTRACT(MONTH FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') = 6
     AND EXTRACT(DAY FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') <= 12  THEN 'Dia dos Namorados BR'
    WHEN EXTRACT(MONTH FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') = 11
     AND EXTRACT(DAY FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') >= 15  THEN 'Black Friday BR'
    WHEN EXTRACT(MONTH FROM c.published_at AT TIME ZONE 'America/Sao_Paulo') = 12 THEN 'Dezembro (Natal/Ano Novo)'
    ELSE 'Período Regular'
  END AS janela_sazonal,
  COUNT(*) AS videos,
  ROUND(AVG(c.views)::numeric, 0) AS avg_views,
  ROUND(AVG(c.saves)::numeric, 0) AS avg_saves,
  ROUND(AVG(c.shares)::numeric, 0) AS avg_shares
FROM public.my_content c
WHERE c.handle IN ({handles_do_criador}) AND c.views >= 200
  AND c.published_at IS NOT NULL
GROUP BY mes_br, janela_sazonal
ORDER BY janela_sazonal, mes_br
```

**Output:** comparação Black Friday / Janeiro / Dia das Mães / Período Regular. Insights cruzados com a `## Sazonalidade do Nicho` do CLAUDE.md do projeto. Se dados insuficientes (<5 posts numa janela): avisar.

---

## Diretrizes de Output

1. **Dados reais** — nunca fabricar URLs, saves, hooks
2. **Sempre saves + shares + views** — nunca só views
3. **Cite o n** — amostras pequenas enganam
4. **Ranqueie, não prescreva** — do melhor ao pior
5. **Combos são ouro** — formato + hook + tópico vencedor
6. **Seja específico** — hooks reais, números reais
7. **Escaneável** — tabelas, cabeçalhos, bullets
8. **Deep dives por plataforma** sempre obrigatórios

## Após Análise: Salvar Relatório

Perguntar: "Quer que eu salve essa análise? Posso criar `analises/analise-YYYY-MM-DD.md` no projeto atual — histórico pra comparar meses."
