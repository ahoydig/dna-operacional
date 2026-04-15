---
description: Briefing de inteligência competitiva dos ads dos teus concorrentes a partir de ad_library (Meta Ad Library). 10 seções — sumário executivo, mercado, tier de concorrentes, padrões criativos, ofertas, benchmarks BR. Use quando digitar "/raio-x-ads-concorrentes", "raio-x ads", "análise de ads competidores".
argument-hint: "[nicho?]"
---

# /raio-x-ads-concorrentes — Raio-X dos Ads dos Concorrentes

> Público: empreendedor brasileiro. Zero jargão de dev. PT-BR sempre.

**Tese central:** longevidade = lucratividade. Ad rodando há 30+ dias é vencedor validado — o anunciante não queimaria dinheiro senão.

**Entrega:** briefing completo de 10 seções salvo em `pesquisa/briefings/raio-x-ads-{YYYY-MM-DD}.md`.

---

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

> ℹ️ A skill `/coletar-anuncios` (que popula `ad_library`) entra em v0.2 e também usará `APIFY_TOKEN`. Por ora, `ad_library` precisa ser populada manualmente (ver Pré-requisitos abaixo).

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

1. Ler `CLAUDE.md` seção `## Storage Backend` — se ausente, abortar pedindo `/setup-projeto`
2. Ler `CLAUDE.md` seção `## Raio-X Ads` → extrair `competitor_ids` de cada tier
3. Verificar data atual em `America/Sao_Paulo` + checar janela sazonal BR ativa
4. Carregar dados do backend via storage layer (ver "Carregamento de dados" abaixo) — se vazio, aviso humanizado
5. **Agregar em memória** pra montar as 10 seções (group by, count, filter, string_agg equivalente)
6. Montar briefing humanizado
7. Salvar em `pesquisa/briefings/raio-x-ads-{YYYY-MM-DD}.md`

## Carregamento de dados (uma vez, no início)

```
competitor_ids = [...]  # extraídos de CLAUDE.md (todos os tiers)

competitors = storage.read_competitors({
  id: {op: "in", value: competitor_ids}
})

ads = storage.read_ad_library({
  _and: [
    {competitor_id: {op: "in", value: competitor_ids}},
    {language: "pt"},
    {country: "BR"}
  ]
})

if len(ads) == 0:
  # aviso humanizado ad_library vazia — ver Pré-requisitos acima
  abort()
```

A partir daqui, todo agrupamento/contagem é **in-memory** sobre as listas `competitors` e `ads`. **Nunca escrever SQL inline** — regra ferro do contract (exceção documentada só pra `/analista-conteudo`).

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

Agregar in-memory sobre `ads` + `competitors`. Por concorrente:

- `total_ads` — count de ads
- `ads_ativos` — count onde `is_active = true`
- `media_longevidade_dias` — média de `longevidade_dias`
- `spend_min_estimado_brl` / `spend_max_estimado_brl` — sum de `spend_estimated_min`/`max`
- `runners_30d` — count onde `longevidade_dias >= 30`
- `runners_60d` — count onde `longevidade_dias >= 60`

Ordenar por `spend_max_estimado_brl` desc.

Complementar com:
- Tabela Ângulo × Longevidade (agrupar por `angulo`, contar long-runners 60d+)
- Tabela Formato × Longevidade (agrupar por `formato`, comparar vídeo vs imagem vs carrossel)

### Seção 3: Tier Direto

Filtrar `ads` onde `competitor_id ∈ tier_direto_ids` e `is_active = true`. Agrupar por (concorrente × angulo):

- `total` — count
- `media_longevidade` — média dias
- `long_runners_60d` — count onde `longevidade_dias >= 60`
- `hooks_vencedores` — concat dos `hook` onde `longevidade_dias >= 60`, ordenado por `longevidade_dias` desc

Ordenar por `long_runners_60d` desc.

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
- **Filtros obrigatórios:** `language = 'pt' AND country = 'BR'` aplicados na `storage.read_ad_library` do carregamento inicial

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
9. **Se ad_library vazia**, retornar aviso humanizado recomendando `/pesquisa-concorrentes` — nunca deixar erro técnico aparecer pro user
10. **Nunca escrever SQL inline** — usar sempre `storage.read_*()` do contract; agregação fica in-memory (exceção só pra `/analista-conteudo`)

## Salvar relatório

```bash
DATA_BR=$(TZ=America/Sao_Paulo date +%Y-%m-%d)
# Salvar em: pesquisa/briefings/raio-x-ads-${DATA_BR}.md
```

Diretório `pesquisa/briefings/` criado se não existir.

---

## Fim da execução — bloco "Próximos Passos"

Após salvar o briefing, apresentar:

```
✅ Raio-X salvo em pesquisa/briefings/raio-x-ads-{DATA_BR}.md ({N} concorrentes analisados).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /ideias-conteudo        — usa insights pra gerar conteúdo orgânico
  2. /pesquisa-concorrentes  — popula mais concorrentes pra próxima rodada

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Se ad_library estava vazia** (caso esperado em v0.1.0), mostrar apenas:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 ENQUANTO /coletar-anuncios NÃO CHEGA (v0.2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /pesquisa-concorrentes — mapeia concorrentes IG sem depender de ads

  💡 /dna pra ver todas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Fallback ASCII** (terminais sem unicode):

```
----------------------------------------
>>> PROXIMOS PASSOS SUGERIDOS
----------------------------------------
  1. /ideias-conteudo        - conteúdo orgânico a partir dos insights
  2. /pesquisa-concorrentes  - popula mais concorrentes

  >>> /dna pra ver todas
----------------------------------------
```
