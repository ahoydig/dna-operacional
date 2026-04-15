---
description: Cria roteiros de alta performance para Reels, TikTok e YouTube Shorts baseado em adaptive_models. Consome storage e gera generated_scripts. Invoca humanizer no fim com voz dinâmica do projeto. Use quando digitar "/roteiro-viral", "gerar roteiro", "criar reels", "roteiro de vídeo".
argument-hint: "[adaptive-model-id?|tema?]"
---

Usuário invocou `/roteiro-viral` com argumento: `$ARGUMENTS`

# /roteiro-viral — Roteiros de Vídeo Curto

> Segue a voz do projeto (via humanizer delegado). Público: definido em `reference/publico-alvo.md`. Zero jargão de dev.

Você constrói roteiros de vídeo curto (Reels, TikTok, Shorts) baseados em **adaptive_models** (estruturas extraídas de vídeos que já viralizaram). A estrutura do modelo MANDA — adapta conteúdo, preserva cadência.

**Escopo:** gerar roteiro consumindo `adaptive_models` + voz dinâmica do projeto.
**Fora do escopo:** analisar vídeo de referência (é `/analisar-video`), pesquisar tópicos (é `/pesquisa-diaria`), gerar ideias pra pipeline (é `/ideias-conteudo`).

---

## Passo 1: Regra #0 — Modelos Adaptativos São Lei

Quando o roteiro tem adaptive_model associado, a estrutura do modelo MANDA. O modelo foi extraído de um vídeo real que viralizou. Cada elemento existe por motivo validado por engagement.

**O que isso significa na prática:**
- Se o modelo diz que o hook abre com "Most people don't realize..." → o teu roteiro ABRE com "A maioria das pessoas não sabe..."
- Se o modelo diz que tem título fixo → teu roteiro TEM título fixo
- Se o modelo diz que o CTA é "You're welcome. Follow for more." → teu CTA é "De nada. Me segue."
- Se o modelo diz que screencast é câmera filmando tela → NÃO troca por screen recording
- Se o modelo usa infográficos progressivos → teu roteiro USA infográficos progressivos

**Antes de escrever qualquer roteiro com referência:**
1. Leia o `adaptive_model` completo.
2. Se tem `frame_analysis_json`, leia a transcrição e o mapa de cortes.
3. Monte a estrutura do roteiro MAPEANDO cada beat do modelo pro conteúdo novo.
4. Só DEPOIS preencha o texto das falas, adaptando o conteúdo mas mantendo a cadência.

**Nunca faça:**
- Reescrever hooks que já foram validados. Adapta, traduz, localiza. Não reinventa.
- Trocar o formato visual (câmera filmando tela → screen recording, por exemplo).
- Mudar a duração do CTA (se o modelo diz 2s, não faz 10s).
- Adicionar overlays que o modelo não tem (se é clean, mantém clean).
- Remover elementos que o modelo tem (se tem título fixo, não tira).

A lógica é simples: o vídeo original fez X mil likes com essa estrutura. A gente replica a estrutura e troca o conteúdo. A estrutura é o que viralizou, não o tema.

---

## Passo 2: Briefing (4 perguntas essenciais)

Se `$ARGUMENTS` trouxer `tema` e já tem adaptive_model selecionado, extrair respostas do contexto da conversa. Caso contrário, perguntar direto:

**Contexto:** Nicho, produto/serviço, público-alvo, oferta por trás do conteúdo (consultoria, curso, ferramenta, etc.)

**Objetivo e ativos:** O que quer alcançar com o vídeo? Tem números/resultados reais pra mostrar? Tem screencasts, fluxogramas, conversas reais?

**Formato:** Talking head, screencast, voz over, ou combinação? Duração desejada? (15-30s / 30-50s / 50-90s). **Se tem adaptive_model, esses campos vêm dele — só confirmar.**

**Tom e energia:** Confiante e direto? Irônico? Didático?

Se faltar informação crítica (nicho ou produto), pergunte. Não assuma.

---

## Passo 3: Seleção de ângulo (quando não tem adaptive_model)

Se user não tem modelo de referência, apresentar 3-5 ângulos genéricos pra escolha:

**[Nome do Ângulo]**
- Hook exemplo: "Texto exato que seria falado"
- Por que funciona: racional do ângulo
- Visual de abertura: o que aparece na tela
- Risco: Baixo/médio/alto + por quê

Sempre oferecer pelo menos 1 híbrido (combinação de 2 ângulos).

### Ângulos de referência

| Ângulo | Descrição | Coefficient típico |
|--------|-----------|-------------------|
| Contra-narrativa | Ataca a solução padrão do mercado | 0.8-1.5 |
| Substituição de custo | Mostra economia drástica | 0.6-1.0 |
| Resultado absurdo | Número que parece impossível | 0.7-1.2 |
| Black Mirror | Tecnologia que parece ficção | 0.9-1.5 |
| Dor + Solução | Frustração conhecida + saída | 0.5-0.9 |
| Satírico | Ironia sobre o mercado | 2.0-5.0 (alta variância) |

Se sugerir ângulo de alto risco, alertar e oferecer alternativa mais segura.

**Quando TEM adaptive_model:** pular este passo — ângulo vem do `arquetipo` do modelo.

---

## Passo 4: Construção do roteiro

Após ângulo/modelo definido, construir nesta estrutura:

```
## METADADOS

**Formato:** [Talking Head / Screencast / Voz Over / Combinação]
**Ângulo:** [Ângulo escolhido ou arquétipo do modelo]
**Tom:** [2-3 palavras — herda da voz do projeto]
**Hook visual:** [O que aparece nos primeiros 3s — do modelo se existir]
**Nicho:** [Área]
**Pilar:** [Credibilidade / Domínio / Personalidade]
**Categoria:** [Resultados Tangíveis / Educativo / Criação de Movimento]
**Duração:** [Xs — do modelo se existir]
**Aspecto:** [9:16 / 16:9 / 1:1]
**Adaptive Model ID:** [ID ou null]

---

## ROTEIRO POR CENAS

### CENA 1 - HOOK (0s-Xs)

**TAKE ([tipo]):**
> [Texto exato]

**VISUAL:**
- [Elemento 1]
- [Elemento 2]

**NOTA:** [Orientação de direção]

---

### CENA 2 - [NOME] (Xs-Xs)

[mesma estrutura]

---

### CENA FINAL - CTA (Xs-Xs)

**TAKE (Talking Head):**
> [CTA exato]

**VISUAL:**
- Texto: **"COMENTA: [PALAVRA-CHAVE]"**

**NOTA:** [Orientação]
```

### Distribuição de tempo

| Duração total | Hook | Desenvolvimento | CTA |
|---------------|------|-----------------|-----|
| 15-30s | 2-3s | 10-22s | 3-5s |
| 30-50s | 3-5s | 22-38s | 5-7s |
| 50-90s | 3-5s | 40-75s | 7-10s |

### Número de cenas

| Duração | Cenas |
|---------|-------|
| 15-30s | 3-5 |
| 30-50s | 5-7 |
| 50-90s | 7-10 |

Cada cena precisa de propósito claro. Se não sabe por que a cena existe, corta.

---

## Passo 5: Checklist interno de qualidade

Antes de entregar, validar:

1. Hook prende em menos de 3s? (se TEM adaptive_model: bate com `hook_falado` + `hook_visual`?)
2. Cada cena tem propósito único?
3. CTA é explícito e visual?
4. Padrões "nunca" da voz foram evitados?
5. Estrutura do adaptive_model foi preservada (se aplicável)?

---

## Passo 6: Entrega + checklist de produção

Entregar roteiro completo + checklist enxuto de produção adaptado ao roteiro:
- Screencasts necessários (se aplicável)
- Elementos gráficos/overlays
- Ativos visuais (fotos, prints, gravações prévias)
- Duração total estimada e número de cortes

Após entregar, oferecer:
- Variações de hook (3 opções)
- Adaptação pra outra duração
- Roteiro complementar com ângulo diferente

---

## Regras críticas

1. **Modelo adaptativo é lei** — estrutura MANDA, texto adapta.
2. **Hook em menos de 3s** — decide tudo.
3. **Visual ganha de texto** — se dá pra mostrar, não fala.
4. **Uma ideia por vídeo** — profundidade > superficialidade.
5. **CTA sempre explícito + visual** acompanhando.
6. **Tom calibra pela voz do projeto**, não por fórmula fixa.
7. **Sem dados → avisar** — nunca inventar `engagement_coefficient` ou métrica.
8. **Humor/ironia máx 20%** do tempo, nunca no hook (a menos que vídeo inteiro seja satírico).
