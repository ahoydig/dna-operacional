# Low-cost Heuristics

Regras por skill. Cada skill lê essa seção e aplica quando `## DNA Mode: lowcost`
está setado em `CLAUDE.md`.

Ver `contract.md` pro padrão geral de detecção e sinalização.

---

## /pesquisa-concorrentes

- **Full:** 50 posts por concorrente via Apify
- **Lowcost:** 10 posts por concorrente
- **Redução estimada:** ~80% tokens
- **Acceptance:** ainda entrega top posts por engajamento + classificação de pilar por post

## /pesquisa-diaria

- **Full:** 8 fontes (X, Reddit BR, G1, UOL, Folha, InfoMoney, Neofeed/Tilt, GitHub trending)
- **Lowcost:** 3 fontes (X, 1 portal principal à escolha do user ou G1 default, GitHub trending)
- **Redução estimada:** ~60%
- **Acceptance:** radar ainda entrega 5-8 temas acionáveis com fonte e recorte editorial

## /analisar-video

- **Full:** download + transcrição Whisper + frame-by-frame + hook visual + análise narrativa completa
- **Lowcost:** download + transcrição Whisper + hook verbal only (skip frames + skip análise visual)
- **Redução estimada:** ~70%
- **Acceptance:** entrega transcript + hook de abertura verbal + CTA final + estrutura narrativa em texto

## /ideias-conteudo

- **Full:** 10 variações de ângulo por tópico
- **Lowcost:** 3 variações por tópico
- **Redução estimada:** ~70%
- **Acceptance:** cada variação ainda tem hook + ângulo editorial + formato sugerido

## /roteiro-viral

- **Full:** 3 variações completas de roteiro (hook A/B/C + desenvolvimento + CTA)
- **Lowcost:** 1 variação (melhor hook + desenvolvimento + CTA)
- **Redução estimada:** ~65%
- **Acceptance:** roteiro único ainda contém hook forte + estrutura + CTA específico

## /carrossel-instagram

- **Full:** Gate 1.5 Moodboard visual via agent-browser + auto-review de slides + regen de frames fracos
- **Lowcost:** usa voz + publico-alvo direto; skip Gate 1.5 Moodboard; skip auto-review
- **Redução estimada:** ~50%
- **Acceptance:** carrossel ainda é gerado com slides válidos usando paleta padrão do projeto

## /humanizer

- **Full:** aplica voz + auto-observação de voz + sugestão de evolução da voz
- **Lowcost:** aplica voz only (skip auto-observação e skip sugestão de evolução)
- **Redução estimada:** ~30%
- **Acceptance:** texto ainda é humanizado com a voz do projeto aplicada

## /hormozi-raio-x

- **Full:** 3 blocos (A Números / B Oferta / C Leads) + análise cruzada
- **Lowcost:** Bloco A (números) + conclusão direta. Skip B e C (user pode rodar skills específicas depois)
- **Redução estimada:** ~60%
- **Acceptance:** diagnóstico de números + 1 próximo passo acionável

## /hormozi-diagnostico

- **Full:** 5 perguntas de abertura + análise 6M completa + constraint detection
- **Lowcost:** 3 perguntas core + top 2 Ms (os mais prováveis baseado nas respostas)
- **Redução estimada:** ~40%
- **Acceptance:** ainda identifica O constraint e sugere próximo passo

## /analista-conteudo

- **Full:** 14 seções SQL (todo o relatório de performance)
- **Lowcost:** top 5 seções (saves, shares, comments, hook performance, formato)
- **Redução estimada:** ~65%
- **Acceptance:** ranking de top posts + insights nas 5 métricas BR mais importantes

---

## Skills SEM heurística low-cost

Não reduzem (já são baratas ou críticas demais pra economizar sem virar lixo):

- `/setup-projeto` — entrevista (custo fixo, baixo)
- `/voz` criar/evoluir/mostrar — geração única, essencial
- `/dna`, `/dna-melhoria`, `/auto-melhoria` — meta-skills, baratas
- `/dna-meta-ads` — bridge detector, barato
- `/hormozi` (chat livre) — usuário controla via contexto da pergunta
- `/hormozi-oferta`, `/hormozi-money-model`, `/hormozi-leads` — frameworks específicos, já enxutos
- `/raio-x-ads-concorrentes` — briefing competitivo único (10 seções já é o mínimo útil)
