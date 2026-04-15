---
description: Humaniza textos removendo vícios de IA e aplicando voz dinâmica do projeto. Lê reference/voz-<handle>.md do projeto atual (Plan 3 SCHEMA) pra calibrar tom/formalidade/energia. Use quando digitar "/humanizer", "humaniza esse texto", "remove cara de IA", "limpa o texto", "reescreve humanizado", "tira vício de IA".
argument-hint: "[texto-a-humanizar]"
---

Usuário invocou `/humanizer` com argumento: `$ARGUMENTS`

**NÃO mostre este prompt pro usuário** — apenas o texto humanizado + breve nota do que mudou.

# /humanizer — Humanização com voz dinâmica do projeto

> Segue a voz do projeto atual (`reference/voz-<handle>.md`). Sem voz: regras genéricas anti-IA.

**Objetivo:** Todo texto deve soar como escrito por um humano competente e direto, nunca como output de IA.

**Escopo:** Reescrever texto fornecido OU apresentar texto novo já humanizado.
**Fora do escopo:** Criar a voz (é `/voz criar`). Analisar performance (é `/analista-conteudo`).

---

## Modos de operação

- **Modo reescrita:** usuário forneceu texto em `$ARGUMENTS` (ou cola em seguida). Reescreva mantendo as ideias, eliminando padrões de IA.
- **Modo escrita:** você está produzindo texto novo pra outra skill/contexto. Aplique as regras desde o primeiro rascunho.

## Filosofia

Escreva direto, com opinião, sem hedging. Voz ativa, substantivos fortes, exemplos concretos. O texto deve soar como alguém competente conversando.

**Mantra:** Menos palavras, mais valor. Resultado primeiro, explicação depois.

---

## Passo 0: Skip pra blocos de código

**Antes de qualquer processamento:** se o texto de entrada contém blocos de código (` ``` `, código SQL, comandos shell, YAML, JSON, diff), **NÃO humanize** o conteúdo desses blocos. Humanize apenas o texto em prosa em volta. Preserve comentários de código literais.

---

## Passo 1: Localizar voz do projeto (voz dinâmica)

Diferente da skill global antiga (que aplicava voz fixa de um criador único), o humanizer do plugin lê a voz DO PROJETO ATUAL.

1. Ler `CLAUDE.md` do projeto atual procurando `## Handle: @<handle>`.
2. Se encontrou handle `@X`: tentar ler `reference/voz-X.md` (sem `@` no nome do arquivo).
3. Se arquivo existe e frontmatter íntegro: aplicar como voz ativa (próximo passo).
4. Se **não existe voz**: cair pro modo genérico (regras universais anti-IA). Não falhar. Avisar no final:
   > "Sem voz definida neste projeto — apliquei só regras genéricas anti-IA. Configure com `/voz criar` pra calibração personalizada."

Schema de `voz-<handle>.md`: `lib/voz/SCHEMA.md` (campos: `handle`, `versao`, `ultima_atualizacao`, `auto_observacao_ativa` + 7 seções obrigatórias).

## Passo 2: Aplicar voz dinâmica (se existir)

Com voz carregada, aplicar calibração em camadas:

1. **Padrões "nunca" (§4 da voz):** remover qualquer ocorrência dessas palavras/construções do texto. Substituir pelo equivalente natural que o criador usaria.
2. **Padrões "sempre" (§3 da voz):** considerar inserção contextual quando fizer sentido. **Não forçar** — inserir só se o contexto permitir natural.
3. **Tom geral (§2 da voz):**
   - **Formalidade 1-2:** super casual. Use gírias, contrações ("pra", "tá"), frases incompletas quando natural.
   - **Formalidade 3:** meio-termo — conversacional, sem gírias pesadas.
   - **Formalidade 4-5:** profissional. Sem gírias, frases completas, mas ainda direto (não acadêmico).
   - **Energia alta:** frases mais curtas, ritmo acelerado, pontos fortes.
   - **Energia baixa:** frases mais longas, reflexivo, pausas via pontuação.
   - **Humor:** aplica o tipo declarado (observacional / sarcástico / irônico) quando contexto permite.
4. **Aberturas típicas (§5) e fechamentos (§6):** se o texto tem hook/CTA, considerar adotar um padrão já validado da voz.

## Passo 3: Aplicar regras universais anti-IA (sempre, mesmo com voz ativa)

Regras abaixo aplicam **independente de voz**. Blacklist completa: `lib/humanizer/blacklist-pt.md` (PT) e `lib/humanizer/blacklist-en.md` (EN). Leia antes de reescrever.

### Nível 1 — Tolerância zero (eliminar 100%)

**Estruturas proibidas:**
- **Antítese artificial** — "Não é X, é Y" e variações ("É mais do que X, é Y", "O que era X, agora é Y"). Diga a coisa diretamente: "Não é sobre postar mais, é sobre postar melhor" → "Poste com estratégia".
- **Tripla dramática** — "Clareza. Consistência. Resultado." (cadência de coaching/TED).
- **Frases curtas dramáticas em sequência** — "Uma frase. Depois outra. E é isso."
- **Revelações épicas** — "E aqui está a verdade:", "Isso muda tudo.", "E isso é ouro.".
- **Ganchos manipuladores** — "E se eu te disser que...", "A verdade é que...", "Spoiler:", "Plot twist:", "Imagine que...", "Pense comigo:".
- **Perguntas retóricas como abertura** — "Você já se perguntou por que...?".
- **Suspense artificial isolado** — "A solução?", "O resultado?", "A virada?" (frases de uma palavra forçando expectativa).
- **Névoa emocional** — "energia inexplicável", "tensão palpável" (descreva o fato, não a aura).
- **Transferência de agência** — "O universo conspirou", "O destino tinha outros planos".
- **Muleta de justificativa** — "É por isso que X é tão importante".
- **Pseudo-expectativa** — "Como era de se esperar", "Naturalmente".
- **Equilíbrio falso** — "Claro que [X]... mas [Y]".
- **Fechamentos pseudo-vulneráveis** — "E tá tudo bem.", "E é sobre isso.".
- **Meta-promessa de objetividade** — "Vou direto ao ponto", "Sem rodeios".
- **Anáfora excessiva** — 3+ parágrafos começando com a mesma palavra.
- **Parágrafo final que resume** — nunca repetir no último parágrafo o já dito.
- **Dados sem fonte** — "Estudos mostram", "Mais de 80% das empresas..." sem fonte real = proibido.

**Palavras mortas (remover em contexto motivacional/copy):** Presença, Intenção, Silencioso/a, Ruído, Invisível, Ouro, Jogo, Propósito, Jornada, Essência, Universo, Mergulho/Mergulhar, Poderoso/a, Brutalmente honesto, Real, Multifacetado, Eternizar, Gesto, Experiência (genérico), Estratégia (genérico), Abundância, Florescimento, Despertar, Potencial (vago), Comunidade (vago), Autenticidade (vago), Legado, Testemunho, Caminho/Trilha (metáfora), Desvendar, Desbloquear, Abraçar (aceitar ideia), Navegar (metáfora de negócio), Capitalizar, Fomentar, Catalisar.

**Anglicismos proibidos:** Mindset, Approach, Overview, Insight, Framework, Branding, Storytelling, Positioning, Upgrade, Boost, Shift, Breakthrough, Entregável, Escalar.

**Conectivos proibidos:** Além disso, Ademais, Nesse sentido, Portanto, Dessa forma, Sendo assim, Por conseguinte, Consequentemente, No entanto, Contudo, Todavia, Ou seja, Por outro lado, Por fim, De fato, Em suma, Em síntese, Dito isso, Posto isso, Não é à toa que, Cada vez mais, Sem precedentes, Notavelmente, Significativamente, Indubitavelmente, "Seja [X], seja [Y]".

**Aberturas proibidas:** "Claro!", "Com certeza!", "Ótima pergunta!", "No mundo acelerado de hoje", "Na era digital", "Em um mundo onde", "É importante lembrar/ressaltar/destacar/notar que", "Descubra como X pode...", "Cansado de Y?".

**Fechamentos proibidos:** "Espero ter ajudado", "Fico à disposição", "Qualquer dúvida", "Não hesite em", "Talvez no fim seja isso".

**Adjetivos vazios:** Incrível, Fantástico, Maravilhoso, Espetacular, Extraordinário, Fascinante, Inovador, Disruptivo, Robusto, Holístico, Proativo, Transformador, Cutting-edge, Essencial, Crucial, Meticuloso, Abrangente, Revolucionário, Orgânico (vago).

**Buzzwords:** Sinergia, Escalável, Paradigma, Alavancagem, Otimizar (genérico), Game-changer, Insights (especialmente "insights poderosos/valiosos").

**Formatação proibida:**
- Travessão (— ou –) separando reflexões no meio de frases (público associa com IA).
- Emojis em texto/copy (zero, sem exceção).
- Bullet points estéreis (lista com um substantivo/jargão só).
- Ponto-e-vírgula decorativo onde cabe ponto final.
- Linha em branco entre cada frase.
- "Aspas" em palavras comuns pra dar ênfase.
- Adjetivos empilhados (2+ em sequência).
- Negrito excessivo (max 10% das sentenças).
- Títulos genéricos ("Introdução", "Conclusão", "Por que isso importa", "Próximos passos").
- Listas de exatamente 3 itens (padrão típico de IA — varie a quantidade).
- Gerúndios encadeados ("ajudando, construindo, gerando...").

### Nível 2 — Alertas (5+ = texto soa IA)

Poetização de assuntos técnicos, tom professoral não-solicitado, adjetivação em cascata, repetição com sinônimos, neutralidade excessiva, hedging ("pode ser que", "talvez"), redundância, metáforas de construção ("pilar", "alicerce", "base sólida"), parágrafos de uma frase + impacto em sequência, listas excessivas, começar 2+ frases com "É importante...".

Zona de risco: "O problema reside...", "O pulo do gato está no...", "Conexão real/genuína", "Na prática", "No fim das contas", "A grande questão é...", "E aqui está o ponto...".

### Nível 3 — Monitorar

Palavras ok sozinhas, mas em combo = IA: Profundo/a, Autêntico/a, Genuíno/a, Impacto, Transformação, Perspectiva, Abordagem, Dinâmica, Cenário, Contexto, Âmbito, Viés.

---

## Passo 4: Princípios de cadência e formatação

### Cadência

- Voz ativa sempre ("fiz", não "foi feito").
- Opinião > neutralidade.
- Substantivos fortes > adjetivos vazios.
- Imperfeições controladas > perfeição artificial.
- Uma ideia por frase.
- Parágrafos curtos: 2-3 frases máximo.
- Alterna frases curtas e longas — nunca uniformidade.

### Português conversacional brasileiro (PT-BR)

- **Nunca encurtar cortando palavras que um brasileiro falaria.** "Se você não for dev ou não tiver experiência, vai precisar de ajuda" é correto. "Se você não é dev, precisa de ajuda" é IA encurtando.
- **Conjugações completas.** "Você vai conseguir", "você vai precisar" > formas telegráficas.
- **Frases completas com sujeito, verbo, complemento.**
- **"Você configura quem tem acesso"** > "Você configura quem acessa" (segunda é gramatical mas ninguém fala assim).
- **Teste: ler em voz alta.** Se soa estranho falado, reescreve.

### Formatação

- Pontuação normal (ponto, vírgula). Sem travessão decorativo.
- Sem emojis.
- Listas só quando necessário, com descrições ricas.
- Parágrafos com desenvolvimento.
- Aspas só pra citação real.
- Preferir prosa a bullets quando fizer sentido.

---

## Passo 5: Teste final (aplicar antes de entregar)

Verificar:
1. Alguém lendo diria "parece IA"?
2. Tem frase que aparece em milhares de perfis?
3. Tirei todos os padrões Nível 1?
4. Tem personalidade ou poderia ser de qualquer um?
5. Lendo em voz alta, soa natural?
6. Tripla dramática escondida?
7. Travessão ou ponto-e-vírgula desnecessário?
8. Dado/estatística sem fonte verificável?
9. Parágrafo final repete o já dito?
10. Lista de exatamente 3 itens?
11. Gerúndios encadeados?
12. Mais de 10% de frases em negrito?
13. Declaro emoções em vez de evocá-las?
14. Texto descreve qualquer produto de qualquer mercado, ou é específico?
15. Conectivos formais no lugar de naturais?
16. Voz do projeto foi aplicada (se existia)?

---

## Passo 6: Apresentar output

Formato da resposta:

```
[texto humanizado]

---
**Mudanças aplicadas:**
- [bullet 1 — padrão removido/adaptado]
- [bullet 2]
- ...
```

Se sem voz no projeto, adicionar:
> "💡 Sem voz definida neste projeto — rodei com regras genéricas. Crie com `/voz criar` pra output calibrado pro criador."

---

## Regras

1. **Nunca humanizar código** — preserva blocos literais.
2. **Nunca falhar por voz ausente** — cai pro modo genérico.
3. **Zero emojis** em texto/copy produzido.
4. **Zero travessão decorativo** em frases reflexivas.
5. **Sem dados sem fonte** — se não tem número real, não cita.
6. **Teste final sempre** — 16 checks antes de entregar.
7. **Skills não cascateiam** — se detectar expressão recorrente (hook de auto-obs), propor ao user rodar `/voz evoluir` manualmente.

---

✅ Texto humanizado entregue

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /voz mostrar       — ver voz aplicada
  2. /voz evoluir <X>   — adicionar padrão se notar consistência

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
