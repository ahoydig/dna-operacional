# Design — Torneio de Carrosséis (melhoria do `/carrossel-instagram` via competição de teses)

**Data:** 2026-05-31
**Autor:** Flávio (Ahoy Digital) + Claude
**Status:** design aprovado em brainstorming, aguardando revisão do spec
**Repo alvo:** `/Users/flavioahoy/Documents/projects/dna-operacional` (plugin `dna-operacional`, branch `main`)

---

## 1. Problema

O `/dna-operacional:carrossel-instagram` atual já é bom ("quase estado da arte"), mas tem um teto **estrutural**, não cosmético: o pipeline é **single-pass linear** — um briefing → uma copy → uma direção → um render. Ele nunca explora alternativas nem se julga contra critério explícito. Para um gerador guiado por LLM, é exatamente aí que se ganha salto de qualidade.

O objetivo do usuário é **melhorar o resultado** (economia de token é só efeito colateral bem-vindo, não meta), via **reescrita radical**, validada por um **torneio com notícia real**, mantendo a versão atual como **controle congelado** para não perder o que já funciona.

### Dimensões de "melhor" (critérios de julgamento, definidos pelo usuário)

1. **Força viral / retenção** — estrutura que segura o swipe e move o algoritmo (sends/saves/watch-time).
2. **Copy / hook / narrativa** — gancho da capa, arco slide-a-slide, CTA.
3. **Design / impacto visual** — cara de top-tier, não template genérico.
4. **Consistência / menos retrabalho** — acertar de primeira, menos iteração manual.
5. **Screenshots reais (ou recriação fiel)** — prova visual com cara de verdade.

---

## 2. Base de pesquisa (fundamenta as decisões — fontes reais)

Pesquisa conduzida com fontes verificáveis. Achados que redesenham o gerador:

- **Algoritmo / viral:** os 3 sinais top de ranking são **watch time, likes e sends** (Mosseri, jan/2025). **Sends importam mais para alcançar não-seguidores; likes para seguidores.** O carrossel ganha uma **"segunda chance"**: se a pessoa não desliza, o IG re-mostra **a partir do slide 2** (Mosseri, out/2024) → **slide 1 e slide 2 precisam ser capa autônoma.** Carrossel com música fica elegível para a aba Reels (alcance extra). Limite 20 slides. Carrossel é o formato de maior engajamento e saves (Socialinsider, 35M posts, 2025; Metricool, >15M posts).
- **Copy / retenção:** curiosidade nasce de **information gap específico e delimitado** (Loewenstein, 1994), não de vagueza. **Slippery slide** (Sugarman): cada slide só precisa ganhar o próximo swipe. **One idea per slide** + mini-headline "road sign" 4–7 palavras. Slide 2 = confirmador de swipe. Um CTA só, ancorado em valor.
- **Design premium:** hierarquia tipográfica decidida de propósito; **escala modular** (razão 1.333 perfect-fourth) em vez de tamanhos arbitrários; **contraste WCAG** ≥4.5:1 (texto normal) e ≥3:1 (texto grande); **grid 8pt**; **2 fontes com papéis fixos** (1 display headline + 1 sans body); canvas **1080×1350 (4:5)**; **clearance no rodapé** para não colidir com a barra de dots do IG; motifs persistentes (numeração, progress, handle) criam identidade.

> Achados quantitativos sem fonte primária auditável (ex.: "+20–40% reach pelo second chance", "X slides = Y% engajamento") foram tratados como **consenso de prática**, não fato. Os valores tipográficos/contraste/grid vêm de fontes canônicas (W3C, Typescale, spec.fm) e são sólidos.

A pesquisa completa vira reference compartilhada do lab (ver §5).

---

## 3. Visão geral da solução

Um **torneio** de geração de carrosséis sobre a **mesma notícia**:

```
            NOTÍCIA ÚNICA (URL fornecida pelo user)
                          │
              brief normalizado (idêntico p/ todos)
                          │
        ┌─────────┬───────┴────┬──────────────┐
        ▼         ▼            ▼               ▼
   CONTROLE   Variante A   Variante B     Variante C
 (atual,     (Hybrid)     (Viral Eng.)   (Editorial)
  congelado)
        │         │            │               │
        └─────────┴─────┬──────┴───────────────┘
                        ▼
        cada um gera carrossel completo (PNGs + roteiro.md)
                        ▼
              JUIZ CEGO pontua 5 dimensões
            (slide-a-slide + carrossel inteiro)
                        ▼
            ranking + justificativa + montagem
                        ▼
              USER CONFIRMA o vencedor
                        ▼
      (depois, com aceite) vencedor/síntese → v2 do controle
```

Princípio de isolamento de variável: **só o motor muda** entre as variantes. Mesma notícia, mesmo brief, mesmo formato, mesma config de fonte, mesmo piso de qualidade. O controle roda **sem nenhuma modificação**.

---

## 4. Componentes — Laboratório isolado (coexistência)

**Decisão:** command novo separado (não flag, não branch). Garante o controle intocado.

### Arquivos a criar (no plugin `dna-operacional`)

| Arquivo | Papel |
|---|---|
| `commands/carrossel-instagram.md` | **CONTROLE — não se toca.** Roda como está. |
| `commands/carrossel-lab-hybrid.md` | Variante A — motor Hybrid Director. |
| `commands/carrossel-lab-viral.md` | Variante B — motor Viral Engineer. |
| `commands/carrossel-lab-editorial.md` | Variante C — motor Editorial Premium. |
| `commands/carrossel-torneio.md` | Orquestrador: roda os 4, chama o juiz, monta a comparação. |

Cada command de tese é **fino**: declara o motor e consome o piso compartilhado (§5). A diferença entre teses está no motor de decisão, não no piso.

---

## 5. Componentes — Piso de qualidade compartilhado + harness

Serve às dimensões **consistência/menos retrabalho** e **screenshot real**. Tudo isto é compartilhado pelas 3 teses (o controle continua usando suas próprias references atuais).

### 5.1 Knowledge base (references do lab)

Em `references/carrossel-lab/` — cópia evoluída das 6 references atuais + novas da pesquisa. **Não toca** em `references/carrossel-instagram/` (do controle).

- Reaproveitadas/evoluídas: `templates.md`, `palettes.md`, `headline-effects.md`, `fonts-config.md`, `screenshot-guide.md`, `visual-research.md`.
- Novas (da pesquisa, com fontes): `algoritmo-ig.md` (sinais, second-chance, sends/saves), `hooks-frameworks.md` (8–12 padrões de hook + information gap + slippery slide), `design-premium.md` (escala modular, WCAG, grid 8pt, motifs, pares de fonte).

### 5.2 Contrato de design verificável (`lib/carrossel/base.css` + `design-contract.md`)

Component library que faz o slide **renderizar certo de primeira**:

- **Tokens:** `--bg`, `--ink`, `--accent` (3 papéis fixos).
- **Escala modular** razão 1.333 ancorada em 24px: 24 → 32 → 43 → 57 → 76 → 101 px. Capa usa topo; internos 1–2 níveis abaixo. Tamanhos fora da escala são banidos.
- **Grid 8pt:** todo padding/gap em múltiplos de 8.
- **Canvas 1080×1350 (4:5)** com safe-zone: padding lateral 64px, topo 96px, **rodapé ≥120px** reservado p/ barra de dots do IG.
- **2 fontes, papéis fixos:** display (headline) + sans (body). Respeita as fontes do projeto (Nofex/Crankdat/Inter) com fallback Google Fonts; Editorial pode propor par próprio dentro da regra.
- **Componentes:** `headline-group`, `body`, `screenshot-frame`, `slide-number`, `progress`, `handle` — mesmos coords/estilo entre slides (motifs persistentes).

### 5.3 Render harness determinístico (`lib/carrossel/render.md` ou script)

Procedimento fixo (não improvisado a cada vez): salvar HTML → servir → abrir Playwright no viewport do formato → esperar fontes → capturar PNG → fechar browser. Mesmo para todas as variantes, para isolar a variável.

### 5.4 QA lint automático (`lib/carrossel/qa-lint.md`)

O que dá para checar por código, checa por código (parse de HTML/CSS), não "no olho":

- Contraste `--ink`↔`--bg` ≥ 4.5:1; `--accent`↔`--bg` ≥ 3:1 → **bloqueia render** se falhar.
- Body nunca < 24px; headline capa ≥ 76px.
- Linha ≤ ~38 caracteres (força quebra).
- Proibido `object-fit: contain` + `background`.
- Todo slide com ≥1 visual.
- Sem palavra órfã na headline.
- PT-BR + valores em R$.
- Clearance da barra de dots respeitado.

O que precisa de olho (estética, "tá bonito?") continua no **auto-review visual** (ler cada PNG), mas reduzido porque o lint já pegou o objetivo.

### 5.5 Screenshot engine (`lib/carrossel/screenshot-engine.md`)

**Decisão: captura real > réplica fiel em HTML.**

1. Tentar capturar do app/site real (Playwright, cookies do user quando preciso).
2. Se falhar (login, paywall, bloqueio): **recriar réplica fiel** do componente real em HTML/CSS (tweet card, terminal, dashboard, news card) — com a cara de verdade, **não** mockup genérico.
3. A réplica é marcada internamente (`data-replica="true"`) para transparência; nunca apresentada como print autêntico de algo que não foi dito.

### 5.6 Research-first

Front-load de pesquisa do tema + busca de fórmulas/exemplos reais de hook **antes** de escrever a copy (lição registrada do usuário: pesquisar antes de copy de alto impacto).

---

## 6. Componentes — As 3 teses (motores)

Mesmo piso (§5). Diferem no **motor de decisão**.

### 6.1 Variante A — Hybrid Director (o "C" recomendado)

Pareto: o que decide um carrossel é a **capa/hook** e a **direção visual geral**.

- Research-first → **best-of-N só na capa**: gera 5 hooks (cobrindo os padrões de §2), juiz interno escolhe por *information gap* delimitado.
- **Best-of-N só na direção visual**: 3 direções com **preview real renderizado** do slide 1, escolhe por impacto.
- Resto: **pipeline de especialistas** (arquiteto de narrativa → diretor de arte → render+QA).
- Equilíbrio entre as 5 dimensões.

### 6.2 Variante B — Viral Engineer

Aposta em alcance/retenção.

- **Slide 1 + slide 2 como capa dupla autônoma** (second-chance do Mosseri).
- **Engenharia de send/save:** slide final pede save com motivo ("salva pra usar depois") + dá razão de DM ("manda pra quem precisa") — sends movem alcance unconnected.
- **Open loop obrigatório** entre todo slide (slippery slide); slide que se fecha sozinho é reprovado.
- **Best-of-N agressivo de hook** (8–12 variantes) + lint de retenção (>30 palavras reprova, jargão reprova, slide sem função reprova).
- Arco narrativo explícito escolhido antes de redigir (PAS / AIDA / BAB / listicle-escalada / story).

### 6.3 Variante C — Editorial Premium

Aposta em design top-tier.

- Escala modular 1.333, contraste WCAG, grid 8pt rígidos.
- **Motifs persistentes** em todos os slides: numeração 01/07, barra de progresso própria, handle, label de seção (mesmos coords/estilo).
- Espaço negativo intencional; curva texto→visual ao longo da sequência.
- **Best-of-N de direção de arte/composição** (não de copy): explora layouts/composições, escolhe o mais "revista premium".
- Par tipográfico editorial dentro do contrato.

---

## 7. Componentes — Juiz + protocolo do torneio

**Decisão: agente juiz pontua, user confirma.**

### 7.1 Protocolo (fairness)

- User fornece a **notícia/URL**. Brief é **normalizado** uma vez e entregue idêntico aos 4 commands.
- Os 4 motores (Controle, Hybrid, Viral, Editorial) geram cada um em sua pasta. O orquestrador então **embaralha** o mapeamento motor→letra e copia/renomeia as saídas para **pastas neutras** (`competidor-1/` … `competidor-4/`) cujos rótulos **não** correspondem à ordem de §6 — o juiz recebe só os competidores numerados, sem saber qual motor é qual (**juiz cego de verdade**). O mapping fica guardado e só é revelado após o ranking.
- Mesmo formato, mesma config de fonte, mesmo piso. Controle roda sem modificação.

### 7.2 Juiz

- Pontua cada variante nas **5 dimensões**, **slide-a-slide** E **carrossel inteiro**, com **nota + justificativa** por dimensão.
- Produz ranking. Viés de LLM é reconhecido → **decisão final é humana**.
- Pesos default iguais entre as 5 dimensões (ajustável pelo user antes do julgamento).

### 7.3 Saída

- Montagem lado-a-lado dos PNGs (capa de cada competidor + grade completa).
- Tabela de notas + justificativas por dimensão.
- Mapping (qual competidor era qual motor) revelado **só após** o ranking.
- User dá o veredito final.

### 7.4 Aprendizado / promoção

- O vencedor (ou uma **síntese** que enxerta o melhor de cada) **pode** virar a base de um `/carrossel-instagram` v2 — **apenas depois**, com aceite explícito do user. O controle nunca é sobrescrito sem aprovação.
- Lições do torneio viram `learnings/` do projeto.

---

## 8. Escopo / fora de escopo

**No escopo:** os 5 commands novos do lab, o piso compartilhado (§5), as 3 teses, o juiz/protocolo, e a execução de **um** torneio sobre a notícia que o user fornecer.

**Fora de escopo (por agora):** promover o vencedor a v2 do controle (decisão futura, com aceite); migrar o controle; A/B com métricas reais de Instagram pós-postagem (isto é julgamento de artefato, não de performance publicada).

---

## 9. Riscos e decisões abertas

- **Custo:** torneio (4 carrosséis + best-of-N + juiz + muitos PNGs/previews) é caro. Aceitável: é evento de avaliação, não produção diária. O modo lowcost não se aplica ao torneio.
- **Fontes locais vs par editorial:** Editorial Premium quer par tipográfico próprio; precisa respeitar fontes disponíveis no sistema ou cair em Google Fonts. Resolver no contrato.
- **Viés do juiz cego:** mitigado por nomes neutros de pasta + decisão humana final; opção futura de painel de 3 juízes se o usuário quiser mais robustez.
- **Notícia única como campo de prova:** um tema só pode favorecer uma tese (ex.: tema técnico favorece Viral; tema visual favorece Editorial). Aceito para a primeira rodada; rodadas futuras podem usar mais de uma notícia.

---

## 10. Sequência de implementação (alto nível — detalhada no plano)

1. Piso compartilhado (§5): contrato de design + base.css + harness + qa-lint + screenshot-engine + knowledge base.
2. As 3 teses (§6) como commands finos sobre o piso.
3. Orquestrador + juiz (§7).
4. Smoke test: rodar o torneio na notícia fornecida pelo user; confirmar que os 4 geram e o juiz pontua.
5. Iterar com base no veredito.
