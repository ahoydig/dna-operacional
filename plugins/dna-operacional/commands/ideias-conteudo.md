---
description: Puxa ideias do content_pipeline (status=Ideia), pesquisa profunda via WebSearch cruzado PT-BR + EN, e multiplica cada tópico em 5 variações de vídeo escolhidas dos 10 frameworks de hook. Use quando digitar "/ideias-conteudo", "gerar ideias", "multiplicar ideia em vídeos", "frameworks de hook".
argument-hint: "[topic-id?]"
---

Usuário invocou `/ideias-conteudo` com argumento: `$ARGUMENTS`

# /ideias-conteudo — Pesquisa + Multiplicação de Vídeos

> Segue a voz do projeto (via humanizer). Público: definido em `reference/avatar.md`. Zero jargão de dev.

**Objetivo:** Transformar 1 tópico do pipeline em 3-5 vídeos diferentes. Volume é a estratégia.

**Escopo:** Pesquisar tópicos, multiplicar em variações, salvar no pipeline.
**Fora do escopo:** Encontrar tópicos novos (é `/pesquisa-diaria`), escrever roteiros (é `/roteiro-viral`).

---

## Passo 0: Puxar Pipeline

Consultar Supabase do projeto (project ID em `CLAUDE.md` → `## Storage Backend: supabase` → `project_id: ${SUPABASE_PROJECT_ID}`) via `mcp__supabase__execute_sql`:

```sql
SELECT id, title, topic, angulo, hook_suggestion, motivo_video, archetype, created_at
FROM public.content_pipeline
WHERE status = 'Ideia'
ORDER BY created_at DESC;
```

Se `$ARGUMENTS` trouxer `topic-id` (número), filtrar só esse registro.

Apresentar lista numerada via `AskUserQuestion`:

```
# Pipeline de Conteúdo — Ideias disponíveis

| # | Título | Tópico | Arquétipo | Quando |
|---|--------|--------|-----------|--------|
| 1 | [título] | [tópico] | [1-10] | [data] |
...

Quais quer desenvolver? (números separados por vírgula, ou "todas")
```

**PARA e espera a escolha.**

---

## Passo 1: Pesquisa profunda (por tópico escolhido)

Antes de gerar variações, ler do projeto atual:
1. `reference/avatar.md` (quem é o público)
2. `reference/voz-${HANDLE}.md` (voz do criador — lida pelo humanizer)
3. `CLAUDE.md` seção `## Pilares de conteúdo` e `## Sazonalidade do Nicho`

Para cada ideia escolhida, fazer WebSearch **cruzado PT-BR + EN**:
- Query PT-BR: `"[tópico] brasil [mês/ano atual]"`, `"[tópico] pt-br"`, `"[tópico] empresas brasileiras"`
- Query EN: `"[topic] [month year]"`, `"[topic] latest news"`, `"[topic] analysis [year]"`

Compilar brief de pesquisa:

```
**Fatos-chave:** [datas, números, nomes concretos]
**Take óbvio brasileiro:** [o que todo criador BR vai dizer sobre isso — pra evitar]
**Gap BR específico:** [o que a audiência brasileira não sabe que seria valioso]
**Polêmica/debate:** [se tem, qual lado ninguém defende]
**Demonstrabilidade:** [dá pra mostrar na tela? que ferramentas/setup?]
```

---

## Passo 2: Palette de 10 frameworks + 5 variações

### 7 Frameworks Universais (adaptados ao contexto BR)

1. **Lista** — "Top 3 [coisas] pra [tópico]" / "5 erros de [X] que custarão caro"
2. **Foco Único** — "A ÚNICA [coisa] que tu precisa pra [tópico]" / "Só isso muda tudo"
3. **Contrário** — "Para de usar [X], usa [Y]" / "Todo mundo faz [X], eu faço [Y]"
4. **Vitrine** — "Esse [cara/empresa] acabou de [fazer coisa absurda] e ninguém tá falando"
5. **Tutorial** — "Como fazer [X] em [tempo]" / "Vou te mostrar passo a passo"
6. **Comparação** — "[X] vs [Y] — qual é melhor em [ano]?"
7. **Emocional** — "Tô passando mal com [situação relatable]" / história de superação

### 3 Frameworks PT-BR Nativos (altíssimo CTR no Brasil)

8. **"Ninguém te contou isso sobre [X]"** — revelação conspiratória leve.
9. **"Para com isso de [fazer X]"** — correção direta de hábito comum.
10. **"A verdade que [profissional] não fala"** — autoridade contrária.

### Regras obrigatórias ao gerar as 5 variações

- **Pelo menos 1 contrário** (framework 3, 9 ou 10)
- **Pelo menos 1 tutorial/educativo** (framework 5 — maior teto de saves)
- **Pelo menos 1 framework BR nativo** se o tópico permite (frameworks 8, 9 ou 10)
- Cada variação com enquadramento **genuinamente diferente**
- **Hooks sempre em PT-BR literal** — nunca traduzir direto do inglês

---

## Passo 3: Integração com Sazonalidade BR

| Janela ativa | Variação sazonal obrigatória |
|---|---|
| Black Friday (15-30/nov) | Urgência: "Só até sexta" / "Última chance antes de [X]" |
| Carnaval (móvel, fev-mar) | Leve/humor ou pausar se nicho não combina |
| Dia das Mães (2º dom mai) | Emocional/familiar |
| Dia dos Pais (2º dom ago) | Emocional/paternidade |
| Natal/Ano Novo (dez) | Retrospectiva ou planejamento do próximo ano |
| Janeiro | Metas/recomeço — "Como começar [X] esse ano" |

Se estiver em janela ativa: adicionar 1 variação sazonal como 6ª opção.

---

## Passo 4: Apresentar variações

Invocar skill `humanizer` antes de apresentar. Formato:

```
## Tópico: [título da ideia original]

**Pesquisa em 2 frases:** [resumo do WebSearch]
**Take óbvio BR:** [1 frase — pra não repetir isso]
**Gap BR específico:** [1 frase — o ângulo diferente]

### Variação 1: [Título]
Framework: 5 — Tutorial
Hook (PT-BR literal): "Vou te mostrar como [X] em 60 segundos"

### Variação 2-5: [...]
```

**PARA e espera a escolha via `AskUserQuestion`.**

---

## Passo 5: Salvar escolhas no pipeline

Pra cada variação escolhida, **antes do INSERT**, buscar o research_brief do registro original:

```sql
SELECT research_brief FROM public.content_pipeline WHERE id = {id_do_original};
```

Montar o `research_brief` final como aditivo (concatenar, nunca sobrescrever).

Depois fazer o INSERT:

```sql
INSERT INTO public.content_pipeline (
  title, status, source, source_url, topic, angulo, hook_suggestion,
  motivo_video, research_brief, format, archetype, platform, variant_of
) VALUES (
  '[título da variação]',
  'Ideia',
  'ideias-conteudo',
  NULL,
  '[tópico original]',
  '[enquadramento]',
  '[hook literal PT-BR]',
  '[por que esse enquadramento funciona]',
  '[brief aditivo montado acima]',
  '[Short/Long/Carrossel]',
  '[número do framework 1-10]',
  '[plataforma alvo]',
  {id_do_original}
);
```

Confirmar ao user: "Adicionei [N] variações no pipeline."

---

## Regras

1. **NUNCA variações genéricas**
2. **NUNCA pula a pesquisa**
3. **NUNCA inventa fatos**
4. **Hooks em PT-BR literal**
5. **Take óbvio importa**
6. **Volume é a estratégia**
7. **`research_brief` é aditivo**
8. **Cada variação = registro próprio** com `variant_of`
9. **Sazonalidade é oportunidade**
10. **Output humanizado** via skill `humanizer`
