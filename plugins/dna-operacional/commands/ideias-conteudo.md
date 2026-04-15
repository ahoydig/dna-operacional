---
description: Puxa ideias do content_pipeline (status=Ideia), pesquisa profunda via WebSearch cruzado PT-BR + EN, e multiplica cada tópico em 5 variações de vídeo escolhidas dos 10 frameworks de hook. Use quando digitar "/ideias-conteudo", "gerar ideias", "multiplicar ideia em vídeos", "frameworks de hook".
argument-hint: "[topic-id?]"
---

Usuário invocou `/ideias-conteudo` com argumento: `$ARGUMENTS`

# /ideias-conteudo — Pesquisa + Multiplicação de Vídeos

> Segue a voz do projeto (via humanizer). Público: definido em `reference/publico-alvo.md`. Zero jargão de dev.

**Objetivo:** Transformar 1 tópico do pipeline em 3-5 vídeos diferentes. Volume é a estratégia.

**Escopo:** Pesquisar tópicos, multiplicar em variações, salvar no pipeline.
**Fora do escopo:** Encontrar tópicos novos (é `/pesquisa-diaria`), escrever roteiros (é `/roteiro-viral`).

---

## Passo 0: Puxar Pipeline

Ler backend de storage em `CLAUDE.md` do projeto (`## Storage Backend: <opção>`). Opções: `supabase`, `sheets`, `markdown`. Contract: `lib/storage/contract.md`.

Se backend ausente:
> "Configure backend em CLAUDE.md `## Storage Backend: <opção>` — opções: supabase / sheets / markdown."

Puxar ideias pendentes via contract abstrato:

```
storage.read_content_pipeline({status: "Ideia"})
```

Se `$ARGUMENTS` trouxer `topic-id` (número), usar `storage.read_one_content_pipeline(id)` pra esse registro só.

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
1. `reference/publico-alvo.md` (quem é o público)
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

Pra cada variação escolhida, **antes de gravar**, buscar o `research_brief` do registro original:

```
original = storage.read_one_content_pipeline(id_do_original)
```

Montar o `research_brief` final como aditivo (concatenar, nunca sobrescrever):
- Se `original.research_brief` não for NULL: `{original.research_brief}\n\n---\n\n{brief_novo}`
- Se NULL: usar só o brief novo

Gravar cada variação via contract:

```
storage.write_content_pipeline({
  title: "[título da variação]",
  status: "Ideia",
  source: "ideias-conteudo",
  topic: "[tópico original]",
  angulo: "[enquadramento — Contrário, Tutorial, Revelação, etc]",
  hook_suggestion: "[hook literal PT-BR]",
  motivo_video: "[por que esse enquadramento funciona pra esse tópico]",
  research_brief: "[brief aditivo montado acima]",
  format: "[Short/Long/Carrossel]",
  archetype: "[número do framework 1-10]",
  platform: "[instagram/tiktok/youtube]",
  variant_of: id_do_original
})
```

Após gravar todas as variantes, promover o registro original:

```
storage.update_content_pipeline(id_do_original, {status: "Roteirizado"})
```

Confirmar ao user: "Adicionei [N] variações no pipeline. Prontas pra roteirizar quando quiser."

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
11. **Zero SQL inline** — tudo via `storage.*` do contract (Spec 2 §4, CONVENCOES §4)

---

## Hook auto-obs: Sinal 2 (hook salvo no pipeline)

Após user salvar uma das variações geradas no `content_pipeline` com `status` mudando pra `Roteirizado` ou `Gravado`:

1. Verificar `reference/voz-<handle>.md` existe E `auto_observacao_ativa: true`.
2. Extrair `hook_suggestion` do record salvo.
3. **Threshold (Plan 3 §5.4):** **1 ocorrência (sinal forte)** — não precisa repetir.
4. Trigger imediato:
   > "Hook '<X>' que você roteirizou — quer adicionar em 'Hooks validados' da voz? (y/n)"
5. Se y: instruir user a rodar `/voz evoluir "<hook literal>"`.

Tracking (opcional, pra evitar sugerir 2× o mesmo): adicionar `hook_id` em `reference/.voz-tracking.json` campo `hooks_sugeridos`.

---

✅ Variações geradas e salvas no pipeline

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /analisar-video       — analisa vídeo de referência pra criar adaptive_model
  2. /roteiro-viral        — gera roteiro com base no adaptive_model
  3. /analista-conteudo    — valida hipótese contra performance histórica

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
