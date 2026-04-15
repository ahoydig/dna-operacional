---
description: Briefing de inteligência competitiva dos ads dos teus concorrentes a partir de ad_library (Meta Ad Library). 10 seções — sumário executivo, mercado, tier de concorrentes, padrões criativos, ofertas, benchmarks BR. Use quando digitar "/raio-x-ads-concorrentes", "raio-x ads", "análise de ads competidores".
argument-hint: "[nicho?]"
---

# /raio-x-ads-concorrentes — Raio-X dos Ads dos Concorrentes

> Público: empreendedor brasileiro. Zero jargão de dev. PT-BR sempre.

**Tese central:** longevidade = lucratividade. Ad rodando há 30+ dias é vencedor validado — o anunciante não queimaria dinheiro senão.

**Entrega:** briefing completo de 10 seções salvo em `pesquisa/briefings/raio-x-ads-{YYYY-MM-DD}.md`.

---

## Pré-requisitos

### 1. Tabela ad_library

Se vazia, retornar aviso humanizado — **não erro SQL**:
> "Beleza, rodei a busca mas tua `ad_library` tá vazia ainda. Pra esse briefing funcionar, tu precisa popular a tabela primeiro. Opções:
> 1. Skill futura `/coletar-anuncios` (v0.2 — ainda não entrou)
> 2. Manual via Meta Ad Library UI + persistência direta no backend
>
> Por enquanto, recomendo focar em `/pesquisa-concorrentes` — mapeia concorrentes IG sem depender de ads. Quando tiver ad_library populada, roda este aqui de novo."

### 2. CLAUDE.md local com seção `## Raio-X Ads`

```markdown
## Raio-X Ads
Marca: [nome]

### Tiers de concorrentes
Direto: [@ ou competitor_ids que vendem a mesma coisa pro mesmo público]
Adjacente: [mercados sobrepostos — mesmo público, produto diferente]
Aspiracional: [grandes anunciantes cujo playbook criativo vale estudar]
```

Se essa seção não existir no CLAUDE.md: "Tu não tem a seção `## Raio-X Ads` no teu CLAUDE.md. Quer que eu adicione agora? Preciso saber quais concorrentes entram em cada tier (Direto, Adjacente, Aspiracional)."

---

## Fluxo

1. Ler `CLAUDE.md` seção `## Raio-X Ads` → extrair `competitor_ids` de cada tier
2. Verificar data atual em `America/Sao_Paulo` + checar janela sazonal BR ativa
3. Checar se `ad_library` tem dados dos competitor_ids do user — se vazia, retornar aviso (acima)
4. Rodar as 10 seções SQL em sequência
5. Montar briefing humanizado
6. Salvar em `pesquisa/briefings/raio-x-ads-{YYYY-MM-DD}.md`

---

## As 10 Seções do Briefing

### Seção 1: Sumário Executivo

6 achados numerados, cada um com número concreto em **R$**:

> "1. O concorrente X gasta ~R$ 47k/mês em 38 ads, dos quais 22 rodam há 60+ dias.
> 2. O ângulo dominante no tier direto é 'escassez + prova social' (14 de 22 long-runners).
> 3. Nenhum concorrente direto usa preço literal nos ads — gap de oportunidade pra testar R$ no criativo.
> ..."

Sem achado com número = não entra no sumário.

### Seção 2: Visão Geral do Mercado

```sql
-- Quem gasta mais e por quanto tempo
SELECT
  c.name AS concorrente,
  COUNT(al.id) AS total_ads,
  COUNT(CASE WHEN al.is_active THEN 1 END) AS ads_ativos,
  ROUND(AVG(al.longevidade_dias)::numeric, 0) AS media_longevidade_dias,
  SUM(al.spend_estimated_min) AS spend_min_estimado_brl,
  SUM(al.spend_estimated_max) AS spend_max_estimado_brl,
  COUNT(CASE WHEN al.longevidade_dias >= 30 THEN 1 END) AS runners_30d,
  COUNT(CASE WHEN al.longevidade_dias >= 60 THEN 1 END) AS runners_60d
FROM public.competitors c
JOIN public.ad_library al ON al.competitor_id = c.id
WHERE al.language = 'pt' AND al.country = 'BR'
  AND c.id IN ({competitor_ids_do_user})
GROUP BY c.id, c.name
ORDER BY spend_max_estimado_brl DESC;
```

Complementar com:
- Tabela Ângulo × Longevidade (quais ângulos têm mais long-runners)
- Tabela Formato × Longevidade (vídeo vs imagem vs carrossel)

### Seção 3: Tier Direto

Análise focada no tier que vende a mesma coisa pro mesmo público.

```sql
SELECT
  c.name, al.angulo, COUNT(*) AS total,
  ROUND(AVG(al.longevidade_dias)::numeric, 0) AS media_longevidade,
  COUNT(CASE WHEN al.longevidade_dias >= 60 THEN 1 END) AS long_runners_60d,
  STRING_AGG(
    CASE WHEN al.longevidade_dias >= 60 THEN al.hook ELSE NULL END,
    ' | ' ORDER BY al.longevidade_dias DESC
  ) AS hooks_vencedores
FROM public.competitors c
JOIN public.ad_library al ON al.competitor_id = c.id
WHERE al.language = 'pt' AND al.country = 'BR' AND al.is_active = true
  AND c.id IN ({competitor_ids_tier_direto})
GROUP BY c.id, c.name, al.angulo
ORDER BY long_runners_60d DESC;
```

"A história": oceano azul (ninguém testa certo ângulo) vs oceano vermelho (todo mundo usa o mesmo).

### Seção 4: Tier Adjacente

Deep dives nos concorrentes de mercado sobreposto — o que eles fazem que o tier direto não testa?

### Seção 5: Tier Aspiracional

Breakdown completo do maior anunciante do tier + top 5 hooks por longevidade.

### Seção 6: Mini Briefings por Concorrente

Pra cada concorrente em qualquer tier:
- Total de ads e % ativos
- Ângulo principal (mais frequente nos long-runners)
- Formato principal
- Ad mais longevo: hook literal PT-BR + dias rodando + se tem urgência ou preço

### Seção 7: Playbook Estratégico

**O que criar primeiro** — 4-5 briefs de ads prioritários baseados nos gaps detectados:
> "Nenhum concorrente direto testou [ângulo X]. Cria um ad com hook '[sugestão PT-BR]' — custo de teste: ~R$ 50/dia por 7 dias."

**O que evitar** — padrões com zero long-runners (saturados ou que não convertem):
> "Ângulo 'desconto percentual' tem longevidade média de 4 dias no tier direto — não teste."

**Framework de testes** — cadência semana a semana:
- Semana 1: testar hook do ângulo mais longevo do tier direto
- Semana 2: testar variação contrária do mesmo ângulo
- Semana 3: testar formato que o tier adjacente usa mas o direto ignora
- Semana 4: analisar performance, matar o que não rodou 7+ dias

### Seção 8 [BR]: Benchmarks BR vs tier

**Benchmarks de referência (Meta Ads Brasil):**
- CPM BR: **R$ 8-15** (Meta Feed IG)
- CTR BR: **1-2%** (IG Feed) / **0.5-1%** (FB Feed)
- Tickets típicos pra ROAS realista: infoproduto R$ 47-497 / mentoria R$ 497-2.997 / serviço B2B R$ 1k-5k/mês

Perfil de ads high-performance por concorrente (long-runners + urgência + preço literal). Interpretação obrigatória: "Ads com urgência + preço literal E longevidade >= 60 dias = playbook alto-conversão BR comprovado."

### Seção 9 [BR]: Análise sazonal

Verificar se hoje cai numa janela sazonal BR ativa (Black Friday / Carnaval / Dia das Mães / Natal).

**Oportunistas** = ads surgidos nas últimas 2 semanas (pra janela atual).
**Evergreens** = ads rodando 60+ dias independente da janela.

Sinalizar quais concorrentes entraram na janela com que hooks e quais ficaram de fora.

### Seção 10: Metodologia

- **Long-runner 30d:** ad ativo por 30+ dias consecutivos
- **Long-runner 60d:** ad ativo por 60+ dias (threshold de validação forte)
- **Oportunista:** first_seen < 14 dias atrás
- **Evergreen:** longevidade_dias >= 60
- **Taxa de corte:** excluídos ads com `is_active = false` exceto pra análise histórica explícita
- **Exclusão DCO:** ads dinâmicos podem inflar contagem — agregar por `angulo` em vez de contar individualmente
- **Filtros obrigatórios:** `language = 'pt' AND country = 'BR'` em todas as queries

---

## Regras de qualidade

1. **Toda afirmação com número** — não "prova social funciona" mas "prova social tem mediana de 45 dias em 141 ads de 6 concorrentes"
2. **Hooks sempre literais PT-BR** — citação exata da `ad_library.hook`. Nunca inventa nem traduz
3. **Recomendações com referência a dados** — longevidade, contagem, gap identificado
4. **Tabelas ordenadas por insight** — mediana de dias ou contagem de 60d+, nunca ordem alfabética
5. **Briefing imediatamente acionável** — equipe criativa começa a produzir a partir da Seção 7 hoje
6. **Valores em R$** — CPM R$ 8-15, CTR 1-2%, tickets em R$, spend estimado em BRL
7. **Output via `/humanizer`** se disponível (plugin v0.2+)
8. **Timezone:** data do arquivo e datas de análise em `America/Sao_Paulo`
9. **Se ad_library vazia**, retornar aviso humanizado — nunca deixar SQL error aparecer pro user

## Salvar relatório

```bash
DATA_BR=$(TZ=America/Sao_Paulo date +%Y-%m-%d)
# Salvar em: pesquisa/briefings/raio-x-ads-${DATA_BR}.md
```

Diretório `pesquisa/briefings/` criado se não existir.
