---
description: Radar diário de conteúdo BR. Faz scraping agêntico de X, Reddit BR, portais BR (G1/UOL/Folha/InfoMoney/Neofeed/Tilt), GitHub Trending via Apify e WebSearch. Use quando digitar "/pesquisa-diaria", "radar matinal", "tendências BR", "novidades do dia".
argument-hint: "[fast|full]"
---

# /pesquisa-diaria — Radar Agêntico Brasileiro

> Público: empreendedor brasileiro. Zero jargão de dev. PT-BR sempre.

## Padrão de autenticação Apify (documentado UMA vez — outras skills referenciam)

As 3 skills de scraping (`pesquisa-diaria`, `pesquisa-concorrentes`, `raio-x-ads-concorrentes`) usam `${APIFY_TOKEN}` via curl direto (sem MCP). Ordem de carregamento (compatível com zsh/bash no macOS):

```bash
# 1. Tenta var de ambiente exportada
if [ -z "$APIFY_TOKEN" ]; then
  # 2. Fallback: .env do projeto atual
  if [ -f .env ]; then
    set -a; source .env; set +a
  fi
fi

# 3. Se ainda vazio, para com erro claro
if [ -z "$APIFY_TOKEN" ]; then
  echo "❌ APIFY_TOKEN não encontrado. Opções pra resolver:"
  echo "  1. Exporta em ~/.zshenv: export APIFY_TOKEN=<teu-token>"
  echo "  2. Adiciona no .env do projeto atual"
  exit 1
fi
```

> ⚠️ **Compatibilidade de shell:** as skills assumem **zsh no macOS**. Comandos `date -v-1d` abaixo são BSD (macOS). Se rodar em Linux, trocar por `date -d yesterday`.

Template de chamada curl pra qualquer Apify actor:
```bash
curl -s -X POST "https://api.apify.com/v2/acts/<ACTOR_ID>/run-sync-get-dataset-items?token=${APIFY_TOKEN}&timeout=180" \
  -H "Content-Type: application/json" \
  -d '{"chave": "valor"}'
```

---

## Passo 0: Anti-repetição

Verificar logs anteriores em `research-logs/YYYY-MM-DD.md` (data calculada em `America/Sao_Paulo`, nunca UTC):

```bash
DATA_BR=$(TZ=America/Sao_Paulo date +%Y-%m-%d)
ONTEM_BR=$(TZ=America/Sao_Paulo date -v-1d +%Y-%m-%d)
test -f research-logs/$ONTEM_BR.md && cat research-logs/$ONTEM_BR.md
```

Qualquer tópico que apareceu nos últimos 2 dias deve ser **PULADO** a menos que haja desenvolvimento novo (ex: nova versão, polêmica que escalou, dado novo publicado).

## Passo 1: Carregar contexto

Ler arquivos do projeto atual:
1. `CLAUDE.md` — nicho, pilares de conteúdo, handles, sazonalidade do nicho específico, `## Storage Backend`
2. `reference/publico-alvo.md` — quem é o público (macro + micro)
3. `reference/voz-<handle>.md` — voz, hooks validados, aberturas típicas (gerado pela skill `/voz`)
4. Calendário sazonal BR embutido na skill — verificar se hoje cai numa **janela sazonal ativa**

Se `CLAUDE.md` não existir, pedir ao user: "Você ainda não configurou o teu projeto. Quer rodar `/setup-projeto` primeiro pra eu ter contexto do teu nicho?"

Se `reference/voz-<handle>.md` não existir, avisar: "Sem voz do projeto ainda. Vou gerar hooks genéricos PT-BR. Pra calibrar, roda `/voz criar` quando puder."

## Passo 2: Scraping paralelo (5 fontes, todas com filtro BR)

Rodar em paralelo — se 1 actor falhar, anotar e continuar com os outros.

### Fonte A — X/Twitter (Apify)

Actor: `61RPP7dywgiy0JPD0` (Tweet Scraper V2)

Termos de busca em **PT-BR + EN** (combinar pra não perder tendências globais não traduzidas):

**PT-BR nativos:**
- `"acabei de criar" IA OR ChatGPT OR Claude`
- `"acabei de lançar" ferramenta OR app`
- `"ninguém fala sobre" IA`
- `"para de usar" ChatGPT OR Claude`
- `"tô passando mal" IA OR ferramenta`
- `"rapaz olha isso" nova`
- `"gente, essa IA"`
- `"nova ferramenta" grátis`

**EN (top performers globais):**
- `"I built" AI`
- `"just dropped" AI`
- `"stop using" ChatGPT`

Parâmetros:
```json
{
  "searchTerms": ["lista acima — substituir pelos termos reais"],
  "maxItems": 30,
  "sort": "Top",
  "tweetLanguage": "pt",
  "start": "{ONTEM_BR}",
  "end": "{DATA_BR}",
  "includeSearchTerms": true
}
```

Chamada curl:
```bash
curl -s -X POST "https://api.apify.com/v2/acts/61RPP7dywgiy0JPD0/run-sync-get-dataset-items?token=${APIFY_TOKEN}&timeout=180" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["acabei de criar IA", "acabei de lançar ferramenta", "ninguém fala sobre IA", "I built AI", "just dropped AI"], "maxItems": 30, "sort": "Top", "tweetLanguage": "pt"}'
```

### Fonte B — Reddit BR (Apify)

Actor: `trudax/reddit-scraper-lite`

Subreddits BR obrigatórios:
- `r/brasil`
- `r/brdev`
- `r/empreendedorismo`
- `r/investimentos`
- `r/DigitalMarketingBR`

+ 2-3 subreddits específicos do nicho do user (extrair do `CLAUDE.md`)

Parâmetros:
```json
{
  "startUrls": [
    {"url": "https://www.reddit.com/r/brasil/top/?t=day"},
    {"url": "https://www.reddit.com/r/brdev/top/?t=day"},
    {"url": "https://www.reddit.com/r/empreendedorismo/top/?t=day"},
    {"url": "https://www.reddit.com/r/investimentos/top/?t=day"},
    {"url": "https://www.reddit.com/r/DigitalMarketingBR/top/?t=day"}
  ],
  "maxItems": 75,
  "maxPostCount": 15,
  "skipComments": true,
  "proxy": {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL_BR"]}
}
```

Chamada curl:
```bash
curl -s -X POST "https://api.apify.com/v2/acts/trudax~reddit-scraper-lite/run-sync-get-dataset-items?token=${APIFY_TOKEN}&timeout=180" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": [{"url": "https://www.reddit.com/r/brasil/top/?t=day"}, {"url": "https://www.reddit.com/r/brdev/top/?t=day"}, {"url": "https://www.reddit.com/r/empreendedorismo/top/?t=day"}, {"url": "https://www.reddit.com/r/investimentos/top/?t=day"}, {"url": "https://www.reddit.com/r/DigitalMarketingBR/top/?t=day"}], "maxItems": 75, "maxPostCount": 15, "skipComments": true, "proxy": {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL_BR"]}}'
```

### Fonte C — Portais BR via WebSearch

Portais: **G1**, **UOL**, **Folha** de S.Paulo, **Estadão**, **InfoMoney**, **Neofeed**, **Tilt** UOL.

Queries nativas (rodar em paralelo):
- G1: `site:g1.globo.com [nicho] [mês ano]`
- UOL: `site:uol.com.br [nicho] [mês ano]`
- Folha: `site:folha.uol.com.br [nicho] [mês ano]`
- Estadão: `site:estadao.com.br [nicho] [mês ano]`
- InfoMoney: `site:infomoney.com.br [nicho] [mês ano]` (B2B/finanças)
- Neofeed: `site:neofeed.com.br [nicho]` (business/startup BR)
- Tilt: `site:tilt.uol.com.br [nicho]` (tech BR)

Substituir `[nicho]` e `[mês ano]` com os valores reais do `CLAUDE.md` + data atual.

### Fonte D — GitHub Trending via WebFetch

Buscar:
- `https://github.com/trending?since=daily`
- `https://github.com/trending/python?since=daily`
- `https://github.com/trending/typescript?since=daily`

Procurar: repos/ferramentas plug-and-play com 100+ stars no dia, especialmente templates, ferramentas sem código e automações.
**GAP de oportunidade:** poucos criadores BR monitoram GitHub Trending — qualquer repo interessante vira conteúdo diferenciado.

### Fonte E — Web global via WebSearch

Pra tendências globais não traduzidas ainda:
- `"[nicho] news today {DATA_BR}"`
- `"[produto/ferramenta do nicho] update [mês ano]"`
- `"[nicho] launch OR release OR announcement [mês ano]"`

---

## Passo 3: Avaliação agêntica (LÊ o conteúdo, não só escaneia títulos)

Pra cada item coletado, verificar se encaixa em um dos **10 arquétipos virais**:

### 8 arquétipos universais
1. **Alguém Construiu X com Y** (Prova de Magia)
2. **Empresa Lançou X** (Notícia de Produto)
3. **Ferramenta Gratuita** (Revelação de Segredo)
4. **Você tá fazendo X errado** (Correção Contrária)
5. **X vs Y** (Comparação/Batalha)
6. **X agora consegue Y** (Nova Capacidade)
7. **Isso muda tudo** (Choque)
8. **Demo de Automação Divertida** (Personalidade + Tech)

### 2 arquétipos BR nativos
9. **Drama/Polêmica da Semana** — brasileiro engaja muito em polêmica (cancelamento, cobrança pública, "exposed"). Ativar SÓ se alinha com voz/nicho do criador.
10. **Gambiarra/Jeitinho** — "Descobri um jeitinho de X sem pagar Y" (cultural forte BR — economia criativa)

**Se não encaixa em NENHUM arquétipo, PULA.**

Se encaixa, avaliar por estes critérios:

### Critério 1 — TAM BR
- **Alto:** ferramentas/produtos pra consumidor geral, gratuitas, hacks de economia em R$, qualquer pessoa pode usar
- **Baixo:** exclusivo pra devs, papers acadêmicos, enterprise B2B, nicho pequeno

### Critério 2 — Demonstrabilidade
- **SIM:** ferramenta, repo, feature, workflow, hack — dá pra mostrar na tela
- **NÃO:** opinião pura, mudança de preço, notícia política sem demonstração

### Critério 3 — Potencial de Hook (PT-BR literal)
O tópico mapeia num hook brasileiro?
- Arquétipo 1 → "Esse cara acabou de criar [X] com [Y]"
- Arquétipo 3 → "Achei uma ferramenta grátis que faz [coisa incrível]"
- Arquétipo 4 → "Para de usar [X], usa [Y] no lugar"
- Arquétipo 9 → "[Cara/empresa X] cancelou [coisa] e o motivo é absurdo"
- Arquétipo 10 → "Aprendi um jeitinho de [X] sem pagar [Y]"

### Critério 4 — Frescor
Já apareceu em `research-logs/` dos últimos 2 dias? Se sim, PULA (a menos que haja desenvolvimento novo).

### Critério 5 — Originalidade
Todo criador BR grande já tá cobrindo? Se sim, precisa de ângulo único pra entrar.

### Critério 6 — [BÔNUS] Sazonalidade ativa
Se hoje cai numa janela sazonal BR ativa, dá **+1 bônus** pra tópicos alinhados:
- Black Friday (15-30/11) → temas de oferta, escassez, urgência
- Carnaval (móvel, fev-mar) → conteúdo leve ou contrário ("enquanto todo mundo tá no carnaval...")
- Dia das Mães (maio) → storytelling emocional
- Natal/Ano Novo (dez) → retrospectiva, metas, planejamento

### Decisão final
- **GRAVAR** — encaixa arquétipo + TAM alto + demonstrável + hook forte
- **TALVEZ** — encaixa mas fraco em 1-2 critérios
- **PULAR** — sem encaixe, TAM baixo, não demonstrável, já coberto

---

## Passo 4: Apresentar Top 10

Se `/humanizer` estiver instalado (plugin v0.2+), humanize o output antes de apresentar ao user:

```
# Top 10 Tópicos — {DATA_BR}

**Fontes:** X ({N}), Reddit BR ({N}), Portais BR ({N}), GitHub ({N}), Web ({N})
**Avaliados:** {total} itens → {10} que valem
**Pulados por repetição:** {N}
**Janela sazonal ativa:** {janela ou "nenhuma hoje"}

---

### 1. [Título do tópico]
**Fonte:** [X/Reddit/GitHub/Portais_BR/Web] | [URL real]
**Arquétipo:** {número e nome}
**Por que é vídeo:** [TAM, demonstrabilidade, hook]
**Ângulo PT-BR:** "[sugestão de hook literal — em PT-BR, nunca traduzido]"
{⭐ Bônus sazonal: [motivo] — se aplicável}

### 2. [Título]
...

### 10. [Título]
---

Escolhe os números que quer salvar no pipeline (ex: "1, 3, 5"), "todos" ou "nenhum".
```

**PARA e pergunta** via `AskUserQuestion`. **Não auto-prossegue.**

---

## Passo 5: Salvar escolhas no content_pipeline

**Pré-check (obrigatório):** Ler `CLAUDE.md` do projeto atual. Se não tiver seção `## Storage Backend: <opção>`, abortar com:

```
⚠️ Backend de storage não configurado. Rode /setup-projeto pra escolher
   (Supabase / Google Sheets / Markdown) antes de persistir escolhas.
```

Se tem backend, pra cada item escolhido pelo user, chamar operação abstrata do storage layer (`lib/storage/contract.md`):

```
storage.write_content_pipeline({
  title: '[título do tópico]',
  status: 'Ideia',
  source: 'pesquisa-diaria',
  source_url: '[URL real do item]',
  topic: '[tópico resumido em 1-3 palavras]',
  angulo: '[enquadramento — ex: contrário, tutorial, vitrine]',
  hook_suggestion: '[hook PT-BR literal sugerido]',
  motivo_video: '[por que esse tópico é um bom vídeo — 1 frase]',
  format: 'Short',
  archetype: '[número do arquétipo: 1-10]',
  platform: 'instagram'
})
```

O adapter (`supabase.md` / `sheets.md` / `markdown.md`) traduz a chamada pro runtime nativo. **Nunca escrever SQL inline aqui** — regra ferro do contract (§4.7).

**Erros possíveis:**
- `StorageBackendUnavailable` → avisar: "Backend configurado ({backend}) não tá acessível. Verifica as credenciais no `CLAUDE.md`."
- `StorageQuotaExceeded` (Sheets 10k rows ou MD 500+ items) → sugerir `/dna migrar-storage` (v0.2+)

## Passo 6: Salvar log de pesquisa

Criar arquivo `research-logs/{DATA_BR}.md` com:

```markdown
# Radar {DATA_BR}

## Top 10 selecionados
[lista completa com fonte + URL + arquétipo]

## Também notados (não entraram)
[itens que apareceram mas foram pulados + motivo: repetição / TAM baixo / sem demo / já coberto]

## Termos de busca usados
[lista dos termos que geraram mais resultados úteis]

## Fontes que performaram hoje
- X: {N úteis}/{N total}
- Reddit: {N úteis}/{N total}
- Portais BR: {N úteis}/{N total}
- GitHub: {N úteis}/{N total}
- Web: {N úteis}/{N total}

## Notas
[o que funcionou, o que não funcionou, sugestão de termos pra amanhã]
```

**Dupla função:** entregável (não perde se o chat fechar) + anti-repetição (rodada de amanhã lê antes de começar).

## Passo 7: Aguardar próxima ação

Via `AskUserQuestion`:

```
O que quer fazer com os tópicos de hoje?
1. Adicionei no pipeline — quero desenvolver 1-2 agora (roda /ideias-conteudo)
2. Só salvar por ora, volto depois
3. Quer re-rankear ou ajustar algum item do Top 10?
```

**NÃO auto-invoca** `/ideias-conteudo`. Espera direcionamento explícito do user.

---

## Regras

1. **NUNCA fabrica URLs ou títulos** — só dados reais vindos das fontes
2. **LÊ o conteúdo** de cada item — não é só scan de headlines
3. **SEMPRE checa `research-logs/`** antes de apresentar qualquer Top 10
4. **SEMPRE salva `research-logs/{DATA_BR}.md`** após finalizar
5. **Se 1 actor Apify falhar**, anota no log e continua com as outras fontes — não bloqueia
6. **Se TODOS os scrapers falharem**, cai pra modo WebSearch-only e avisa: "Scrapers fora do ar hoje — usei só WebSearch. Resultado pode ser menos atual."
7. **Hooks sempre em PT-BR literal** — nunca traduzir do inglês
8. **Output do Top 10 via `/humanizer`** se disponível (v0.2+ do plugin)
9. **Timezone obrigatória:** `America/Sao_Paulo` — nunca UTC pra cálculo de "hoje/ontem"
10. **LGPD:** não persiste dados pessoais de autores dos tweets/posts — só URL pública e conteúdo público
