# Torneio de Carrosséis — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir um laboratório isolado que gera o mesmo carrossel por 4 motores diferentes (controle atual + 3 teses novas) sobre uma notícia real, julga cego por 5 dimensões, e deixa o usuário escolher o vencedor — sem tocar no `/carrossel-instagram` que já funciona.

**Architecture:** Piso de qualidade compartilhado (knowledge base + contrato de design CSS + QA lint em Python + render harness + screenshot engine) consumido por 3 commands de tese finos; um orquestrador roda os 4 motores em pastas neutras embaralhadas e dispara um juiz cego. O controle roda sem modificação. Domínio é majoritariamente Markdown de prompt; o único código executável (e portanto com TDD real) é o QA lint em Python e o `base.css` que ele valida.

**Tech Stack:** Markdown (Claude Code slash commands + references), CSS (contrato de design), Python 3 + pytest (QA lint), Playwright MCP / agent-browser (render e captura), `${CLAUDE_PLUGIN_ROOT}` para paths do plugin.

---

## Convenções deste plano

- **Repo:** `/Users/flavioahoy/Documents/projects/dna-operacional` (branch `main`). Todos os paths abaixo são relativos a `plugins/dna-operacional/` salvo indicação contrária.
- **Plugin path em runtime:** commands referenciam arquivos do plugin via `${CLAUDE_PLUGIN_ROOT}/...` (padrão já usado por `roteiro-viral.md`, `hormozi-*.md`).
- **"Verificação" substitui "teste TDD"** nas tasks de Markdown: cada task produz um artefato e a verificação é concreta (arquivo existe, estrutura bate, parseia, lint roda). Onde há código Python real (Tasks 8–12), o TDD é genuíno: teste falha → implementa → teste passa.
- **Controle intocado:** nenhuma task modifica `commands/carrossel-instagram.md` nem `references/carrossel-instagram/`. Se alguma task tentar, é erro de execução.
- **Commits frequentes:** um commit por task (ou por par teste+impl). Mensagens em PT-BR seguindo o padrão `feat(carrossel-lab): ...`.
- **Branch de trabalho:** criar `ahoydig/carrossel-torneio` antes da Task 1 (não trabalhar direto na main).

---

## File Structure (mapa de decomposição)

**Knowledge base (lazy-loaded pelos commands):**
- `references/carrossel-lab/templates.md` — 9 templates narrativos (evoluído do controle)
- `references/carrossel-lab/palettes.md` — 10 paletas (evoluído + tokens)
- `references/carrossel-lab/headline-effects.md` — 8 efeitos (evoluído)
- `references/carrossel-lab/fonts-config.md` — fontes + escala modular (evoluído)
- `references/carrossel-lab/screenshot-guide.md` — captura por fonte (evoluído)
- `references/carrossel-lab/visual-research.md` — moodboard (evoluído)
- `references/carrossel-lab/algoritmo-ig.md` — **novo** — sinais do algoritmo, second-chance, sends/saves (com fontes)
- `references/carrossel-lab/hooks-frameworks.md` — **novo** — padrões de hook + information gap + slippery slide (com fontes)
- `references/carrossel-lab/design-premium.md` — **novo** — escala modular, WCAG, grid 8pt, motifs (com fontes)

**Piso de qualidade (lib):**
- `lib/carrossel/design-contract.md` — contrato de design legível (tokens, escala, grid, safe-zone)
- `lib/carrossel/base.css` — component library CSS real (tokens, escala, componentes)
- `lib/carrossel/qa_lint.py` — **código executável** — valida HTML+CSS de slide contra o contrato
- `lib/carrossel/tests/test_qa_lint.py` — testes pytest do linter
- `lib/carrossel/tests/fixtures/` — HTML de exemplo (passa / falha) para os testes
- `lib/carrossel/render.md` — render harness determinístico
- `lib/carrossel/screenshot-engine.md` — captura real → réplica fiel

**Commands (slash commands):**
- `commands/carrossel-lab-hybrid.md` — tese A (Hybrid Director)
- `commands/carrossel-lab-viral.md` — tese B (Viral Engineer)
- `commands/carrossel-lab-editorial.md` — tese C (Editorial Premium)
- `commands/carrossel-torneio.md` — orquestrador + juiz cego

**Infra:**
- `lib/mode/low-cost-heuristics.md` — adicionar entradas das 3 teses + torneio (modify)
- `.claude-plugin/plugin.json` — bump de versão (modify)

---

## Fase 0 — Scaffolding

### Task 0: Branch e estrutura de pastas

**Files:**
- Create: (diretórios) `references/carrossel-lab/`, `lib/carrossel/`, `lib/carrossel/tests/fixtures/`

- [ ] **Step 1: Criar branch de trabalho**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git checkout main && git pull --ff-only
git checkout -b ahoydig/carrossel-torneio
```

- [ ] **Step 2: Criar diretórios**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
mkdir -p references/carrossel-lab lib/carrossel/tests/fixtures
```

- [ ] **Step 3: Verificar**

Run: `ls -d references/carrossel-lab lib/carrossel/tests/fixtures`
Expected: os três caminhos listados sem erro.

- [ ] **Step 4: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add -A && git commit -m "chore(carrossel-lab): scaffolding de pastas do laboratório de torneio"
```

---

## Fase 1 — Knowledge base (references/carrossel-lab/)

> Estratégia: as 6 references evoluídas começam como cópia fiel das atuais (mesmo conteúdo já validado), depois recebem deltas. As 3 novas são escritas do zero com o conteúdo da pesquisa (fontes reais já levantadas no spec).

### Task 1: Copiar as 6 references base do controle

**Files:**
- Create: `references/carrossel-lab/{templates,palettes,headline-effects,fonts-config,screenshot-guide,visual-research}.md` (cópia)

- [ ] **Step 1: Copiar os 6 arquivos**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
cp references/carrossel-instagram/templates.md        references/carrossel-lab/templates.md
cp references/carrossel-instagram/palettes.md         references/carrossel-lab/palettes.md
cp references/carrossel-instagram/headline-effects.md references/carrossel-lab/headline-effects.md
cp references/carrossel-instagram/fonts-config.md     references/carrossel-lab/fonts-config.md
cp references/carrossel-instagram/screenshot-guide.md references/carrossel-lab/screenshot-guide.md
cp references/carrossel-instagram/visual-research.md  references/carrossel-lab/visual-research.md
```

- [ ] **Step 2: Verificar que as 6 cópias existem e não estão vazias**

Run: `wc -l references/carrossel-lab/*.md`
Expected: 6 arquivos, cada um com >100 linhas (mesma contagem das originais).

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/references/carrossel-lab/
git commit -m "feat(carrossel-lab): base de references copiada do controle"
```

### Task 2: Reference nova — `algoritmo-ig.md`

**Files:**
- Create: `references/carrossel-lab/algoritmo-ig.md`

- [ ] **Step 1: Escrever o arquivo com o conteúdo abaixo (conteúdo real, com fontes da pesquisa)**

````markdown
# Algoritmo do Instagram — sinais que movem carrossel (2024–2026)

Base factual pra decisões de estrutura. Distinção explícita entre **fato com fonte** e **consenso de prática**.

## Fatos com fonte

- **Top-3 sinais de ranking: watch time, likes, sends.** Olhar average watch time, likes per reach, sends per reach. [Mosseri, jan/2025 — Social Media Today: https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/]
- **Sends importam mais para alcançar não-seguidores; likes para seguidores.** [mesma fonte]
- **Sends são um dos maiores sinais de ranking** — crie algo que a pessoa queira mandar pra um amigo. [Mosseri via SMK, jul/2024: https://smk.co/instagram-chief-confirms-sends-drive-algorithm-rankings/]
- **Second chance do carrossel:** se a pessoa não desliza, o IG frequentemente re-mostra começando pelo slide 2. [Mosseri, out/2024 — reel: https://www.instagram.com/mosseri/reel/DBOeUmTSmIC/ ; cobertura: https://www.threads.com/@mattnavarra/post/DBgmZcEoiZb]
- **Mais mídias = mais interações = mais reach em média** (por que carrossel supera foto única). [mesmo reel do Mosseri]
- **Carrossel/foto com música fica elegível pra aba Reels.** [anúncio IG out/2024: https://www.instagram.com/p/DBO8V2yx4vS/]
- **Limite de 20 slides** (ago/2024). [MacRumors: https://www.macrumors.com/2024/08/08/instagram-20-photos-carousel-posts/]
- **Posts não-originais (repost) são penalizados na recomendação.** [Engadget: https://www.engadget.com/2160560/...]
- **Carrossel lidera engajamento e saves** (35M posts). [Socialinsider 2025: https://www.socialinsider.io/social-media-benchmarks/instagram] **Lidera impressões/interações** (>15M posts). [Metricool: https://metricool.com/important-instagram-statistics/]

## Consenso de prática (sem dado primário auditável — NÃO citar como fato)

- Número ótimo educativo: ~8–10 slides.
- Capa: gap de informação + promessa clara + alto contraste + tipografia grande.
- Retenção: open loop entre slides, "1/7" como swipe-bait, canvas contínuo fatiado.
- Saveability: conteúdo de referência/checklist é o mais salvo.

## Regras default para o gerador

1. **Slide 1 e slide 2 são ambos capa autônoma** (o algoritmo re-entra pelo 2).
2. **8–10 slides** default; expandir até ~12 só se a ideia pedir; hard cap 20; nunca slide vazio.
3. **Engenheirar send + save:** slide final pede save com motivo + dá razão de DM.
4. **Open loop entre slides** + **uma ideia por slide** (maximiza swipe-through e watch time).
5. **Formato de referência salvável** (checklist/passo-a-passo/framework) como default.
6. **Sugerir música** quando fizer sentido (elegibilidade pra aba Reels).
7. **Nunca repost sem transformação real.**
````

- [ ] **Step 2: Verificar estrutura (headings e ausência de placeholder)**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
grep -c "^## " references/carrossel-lab/algoritmo-ig.md
grep -nE "TODO|TBD|FIXME|\\[fonte\\]" references/carrossel-lab/algoritmo-ig.md || echo "OK sem placeholder"
```
Expected: ≥3 headings `## ` e "OK sem placeholder".

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/references/carrossel-lab/algoritmo-ig.md
git commit -m "feat(carrossel-lab): reference algoritmo-ig com fontes"
```

### Task 3: Reference nova — `hooks-frameworks.md`

**Files:**
- Create: `references/carrossel-lab/hooks-frameworks.md`

- [ ] **Step 1: Escrever o arquivo com o conteúdo abaixo**

````markdown
# Frameworks de hook e copy de carrossel

## Por que isso funciona (base)

- **Information gap específico e delimitado** gera curiosidade; vagueza não. Quanto mais preciso o gap, mais motiva. [Loewenstein 1994 — Golman & Loewenstein: https://www.cmu.edu/dietrich/sds/docs/golman/golman_loewenstein_curiosity.pdf]
- **Slippery slide (Sugarman):** cada elemento só existe pra fazer ler o próximo. No carrossel: cada slide só precisa ganhar o próximo swipe. [https://credible-content.com/blog/slippery-slide-copywriting-increase-sales/]

## Padrões de hook de capa (gerar N e julgar pelo gap)

1. **Contrarian / hot take** — "Tudo que te disseram sobre X está errado."
2. **Resultado específico** — número + outcome: "2.400 seguidores em 30 dias com 1 formato."
3. **"You" problem (dor direta)** — "Você gasta 2h em cada carrossel."
4. **Listicle + objeção** — "7 erros de carrossel que matam teu alcance."
5. **Pergunta com gap** — "Por que alguns carrosséis recebem 10x mais saves?"
6. **Antes→depois pessoal** — "Antes de aprender esse framework eu..."
7. **Comando negativo** — "Pare de colocar CTA em todo slide."
8. **Data lead com gap** — "Carrossel tem 1,4x mais alcance. Mas só se você fizer isso."
9. **Prova empírica** — "Postei 100 carrosséis em 90 dias. Aprendi 3 coisas."
10. **Permission slip** — "Você não precisa postar todo dia pra crescer."
11. **Mito / o que ninguém te conta** — "O #1 motivo dos teus posts não baterem."
12. **Cliffhanger / open loop** — "Fui demitido semana passada. O que veio depois →"

[Padrões: https://resont.com/blog/top-instagram-carousel-hooks/ ; https://instacarousel.com/blog/carousel-hooks-that-stop-the-scroll/ — marcados como canônicos de copy onde sem origem única]

## Mecânica de retenção slide-a-slide

- **Slide 2 = confirmador de swipe:** restate a promessa + abre o 1º loop concreto. Nunca "intro".
- **One idea per slide** + mini-headline "road sign" de 4–7 palavras ("Erro 3: CTA fraco").
- **Seed de curiosidade** ao fim de cada slide: "mas tem mais", "→ slide 6".
- Reprovar slide que se fecha sozinho (sem loop pro próximo).

## Arcos narrativos (escolher 1 explícito antes de redigir)

1. **PAS** — Problema → Agitação → Solução.
2. **AIDA** — Atenção (capa) → Interesse (problema/dados) → Desejo (passos/prova) → Ação (CTA único).
3. **BAB** — Before → After → Bridge (o método).
4. **Listicle com escalada** — itens numerados, o mais forte no fim.
5. **Story** — Personagem → Conflito → Clímax → Resolução.

[Arcos: https://postnitro.ai/blog/post/carousel-copywriting-framework ; https://postunreel.com/blog/carousel-copywriting-guide]

## CTA (um só, ancorado em valor)

- Save: "Salva pra usar na próxima."
- Share: "Manda pra quem precisa disso."
- Follow: "Segue pra playbook semanal."

## Lint de copy (reprovar por padrão)

- Hook genérico/vago na capa.
- Body > 30 palavras / wall of text.
- Jargão que o público não decodifica.
- Frase cortada pra caber no slide.
- Slide sem função narrativa.
- Múltiplos CTAs.
````

- [ ] **Step 2: Verificar**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
grep -c "^## " references/carrossel-lab/hooks-frameworks.md
grep -nE "TODO|TBD|FIXME" references/carrossel-lab/hooks-frameworks.md || echo "OK sem placeholder"
```
Expected: ≥5 headings e "OK sem placeholder".

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/references/carrossel-lab/hooks-frameworks.md
git commit -m "feat(carrossel-lab): reference hooks-frameworks com fontes"
```

### Task 4: Reference nova — `design-premium.md`

**Files:**
- Create: `references/carrossel-lab/design-premium.md`

- [ ] **Step 1: Escrever o arquivo com o conteúdo abaixo**

````markdown
# Design premium de carrossel

## Princípios (canônico)

- **Hierarquia tipográfica é o eixo.** Tamanho/peso/cor/contraste guiam o olho. Premium = hierarquia de propósito; genérico = tudo no mesmo peso.
- **Escala modular, não tamanhos arbitrários.** Razão 1.333 (perfect fourth) dá saltos dramáticos. [https://typescale.com/]
- **Contraste é acessibilidade.** WCAG 1.4.3: ≥4.5:1 texto normal, ≥3:1 texto grande (≥24px ou ≥18.5px bold). [https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html]
- **Grid de 8pt.** Padding/gap em múltiplos de 8. [https://spec.fm/specifics/8-pt-grid]
- **Espaço negativo = intenção.** Overcrowding entrega amadorismo.

## Com fonte

- Template próprio > template genérico de Canva (genérico reforça a marca de outro). [https://www.socialhabitmarketing.com/article-posts/the-ultimate-guide-to-designing-a-perfect-instagram-carousel]
- Mixed-media (imagem real + dado) supera só-ilustração. [https://pineable.com/blog/social-media-carousel-design-best-practices]

## Sistema de consistência (acionável)

- **3 tokens de cor com papéis:** `--bg`, `--ink`, `--accent` (1 só).
- **2 fontes com papéis fixos:** 1 display (headline) + 1 sans (body). Banir a 3ª.
- **Motifs persistentes em todos os slides:** numeração 01/07, barra de progresso própria, handle no rodapé, label de seção — mesmos coords/estilo.
- **Swipe affordance** nos primeiros slides.

## Tipografia & composição

- **Canvas 1080×1350 (4:5).** Safe-zone: padding lateral 64px, topo 96px, **rodapé ≥120px** reservado pra barra de dots do IG.
- **Escala modular 1.333 ancorada em 24px:** 24 → 32 → 43 → 57 → 76 → 101px. Capa usa o topo; internos 1–2 níveis abaixo.
- **Body nunca < 24px; headline da capa ≥ 76px.** Linha ≤ ~38 caracteres. Hook da capa ≤ 12 palavras.
- **Leading:** headline 1.15–1.25; body 1.5. **Tracking:** headline ≥60px → -0.02em; all-caps/label → +0.05em.
- **Curva texto→visual** ao longo da sequência.

## Banir por default (red flags de amadorismo)

- 4+ fontes; parágrafo longo centralizado; baixo contraste; sem padding (apertado); imagem esticada/aspect quebrado; slide só-texto; overcrowding (>~12 palavras de body).

[Valores tipográficos/contraste/grid: fontes canônicas acima. Métricas de engajamento de blogs de ferramenta são diretivas, não fato.]
````

- [ ] **Step 2: Verificar**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
grep -c "^## " references/carrossel-lab/design-premium.md
grep -nE "TODO|TBD|FIXME" references/carrossel-lab/design-premium.md || echo "OK sem placeholder"
```
Expected: ≥5 headings e "OK sem placeholder".

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/references/carrossel-lab/design-premium.md
git commit -m "feat(carrossel-lab): reference design-premium com fontes"
```

### Task 5: Delta nas references evoluídas — `fonts-config.md` (escala modular)

**Files:**
- Modify: `references/carrossel-lab/fonts-config.md`

- [ ] **Step 1: Adicionar seção de escala modular ao final do arquivo**

Acrescentar ao fim de `references/carrossel-lab/fonts-config.md`:

````markdown

## Escala modular (contrato do lab)

O lab usa **escala modular fixa razão 1.333 (perfect fourth), ancorada em 24px**, substituindo os ranges livres acima quando o command for de laboratório (`carrossel-lab-*`):

| Nível | px | Uso |
|-------|----|-----|
| 0 | 24 | body mínimo |
| 1 | 32 | body destaque / subtítulo |
| 2 | 43 | label grande / dado secundário |
| 3 | 57 | headline interna |
| 4 | 76 | headline capa (mínimo) |
| 5 | 101 | headline capa dominante |
| 6 | 135 | display gigante (capa CTA) |

Tamanhos fora desta escala são **reprovados** pelo QA lint (`lib/carrossel/qa_lint.py`). Capa usa níveis 4–6; slides internos 2–3 pra headline, 0–1 pra body.
````

- [ ] **Step 2: Verificar**

Run: `grep -c "Escala modular" references/carrossel-lab/fonts-config.md`
Expected: ≥1.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/references/carrossel-lab/fonts-config.md
git commit -m "feat(carrossel-lab): escala modular 1.333 em fonts-config"
```

### Task 6: Delta nas references evoluídas — `screenshot-guide.md` (réplica fiel)

**Files:**
- Modify: `references/carrossel-lab/screenshot-guide.md`

- [ ] **Step 1: Adicionar seção de réplica fiel ao final do arquivo**

Acrescentar ao fim de `references/carrossel-lab/screenshot-guide.md`:

````markdown

## Réplica fiel (quando a captura real falha)

Ordem do lab: **captura real > réplica fiel em HTML > pedir ao user**.

1. Tentar captura real (seções acima).
2. Se falhar (login/paywall/bloqueio), **recriar o componente real** em HTML/CSS com cara de verdade — não mockup genérico:
   - **Tweet/X:** card com avatar circular, nome + @handle, texto, barra de ações, timestamp; cores reais do X.
   - **Terminal:** janela com title bar (3 dots), monospace, prompt realista, output plausível.
   - **News card:** logo do veículo, manchete na fonte certa, lede, imagem hero.
   - **Dashboard:** layout de cards/métricas com números plausíveis (nunca inventar dado real atribuído a fonte).
3. **Marcar a réplica internamente:** o elemento raiz recebe `data-replica="true"`. Nunca apresentar réplica como print autêntico de algo que não foi capturado.
4. Aplicar o mesmo `screenshot-frame` (border-radius, shadow) do contrato.

**Regra de honestidade:** réplica reproduz a *forma* do componente, não fabrica fato. Números/citações dentro da réplica seguem a regra "não fabricar": ou vêm da fonte real, ou são claramente ilustrativos.
````

- [ ] **Step 2: Verificar**

Run: `grep -c "data-replica" references/carrossel-lab/screenshot-guide.md`
Expected: ≥1.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/references/carrossel-lab/screenshot-guide.md
git commit -m "feat(carrossel-lab): réplica fiel de componente em screenshot-guide"
```

---

## Fase 2 — Contrato de design (lib/carrossel/)

### Task 7: `design-contract.md` (contrato legível)

**Files:**
- Create: `lib/carrossel/design-contract.md`

- [ ] **Step 1: Escrever o arquivo**

````markdown
# Contrato de Design do Carrossel-Lab

Contrato que TODAS as teses do lab respeitam. O `base.css` implementa; o `qa_lint.py` valida.

## Canvas

- **Formato default:** 1080×1350 (4:5). Alternativos: 1080×1440 (3:4), 1080×1080 (1:1).
- **Safe-zone:** padding lateral 64px, topo 96px, **rodapé ≥120px** (barra de dots do IG).

## Tokens de cor (3 papéis)

- `--bg` — fundo (sempre gradiente, nunca chapado).
- `--ink` — texto (headline + body).
- `--accent` — 1 cor de destaque/dado.
- **Contraste:** `--ink`↔`--bg` ≥ 4.5:1; `--accent`↔`--bg` ≥ 3:1.

## Escala modular (razão 1.333, base 24px)

24 / 32 / 43 / 57 / 76 / 101 / 135 px. Fora da escala = reprovado.

## Grid

- Tudo (padding, gap, margin) em **múltiplos de 8**.
- Leading: headline 1.15–1.25; body 1.5.

## Fontes (2 papéis)

- Display (headline) + sans (body). Default do projeto: Nofex (headline) / Inter (body) / Crankdat (accent), com fallback Google Fonts (Bebas Neue / Inter / Space Grotesk).
- Banir 3ª família fora desses papéis.

## Componentes (classes do base.css)

- `.slide` — container 1080×1350 com safe-zone.
- `.bg` — gradiente + textura.
- `.headline-group` / `.headline` — título.
- `.body` — corpo.
- `.screenshot-frame` — moldura de print/réplica.
- `.slide-number` — "01/07".
- `.progress` — barra de swipe.
- `.handle` — @ no rodapé.

## Regras invioláveis (validadas por código)

1. Body nunca < 24px; headline capa ≥ 76px.
2. Sem `object-fit: contain` + `background` em screenshot.
3. Todo slide com ≥1 visual.
4. Contraste WCAG (acima).
5. Tamanhos só da escala modular.
6. Rodapé com clearance ≥120px.
````

- [ ] **Step 2: Verificar**

Run: `grep -c "^## " lib/carrossel/design-contract.md`
Expected: ≥6.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/design-contract.md
git commit -m "feat(carrossel-lab): contrato de design legível"
```

### Task 8: `base.css` (component library)

**Files:**
- Create: `lib/carrossel/base.css`

- [ ] **Step 1: Escrever o CSS real**

```css
/* base.css — contrato de design do carrossel-lab.
   Tokens definidos por slide via inline style ou :root override.
   Escala modular 1.333 base 24px. Grid 8pt. */

:root {
  --bg: linear-gradient(135deg, #1A1A2E, #16213E);
  --ink: #FFFFFF;
  --accent: #E94560;

  --fs-0: 24px;  --fs-1: 32px;  --fs-2: 43px;
  --fs-3: 57px;  --fs-4: 76px;  --fs-5: 101px; --fs-6: 135px;

  --font-headline: 'Nofex', 'Bebas Neue', sans-serif;
  --font-headline-outline: 'Nofex Outline', 'Bebas Neue', sans-serif;
  --font-accent: 'Crankdat', 'Space Grotesk', sans-serif;
  --font-body: 'Inter', sans-serif;

  --pad-x: 64px; --pad-top: 96px; --pad-bottom: 120px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

.slide {
  width: 1080px; height: 1350px;       /* 4:5 default */
  padding: var(--pad-top) var(--pad-x) var(--pad-bottom);
  background: var(--bg);
  color: var(--ink);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 56px;                            /* múltiplo de 8 */
  font-family: var(--font-body);
}

.slide.format-3-4 { height: 1440px; }
.slide.format-1-1 { height: 1080px; }

.bg {
  position: absolute; inset: 0; z-index: 0; pointer-events: none;
}

.headline-group { position: relative; z-index: 1; text-align: center; }

.headline {
  font-family: var(--font-headline);
  font-size: var(--fs-4);
  line-height: 1.2;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  padding-top: 0.08em;                  /* Nofex clipa acento */
  overflow: visible;
}
.headline.cover { font-size: var(--fs-5); }

.body {
  font-family: var(--font-body);
  font-size: var(--fs-0);
  line-height: 1.5;
  text-align: left;
  max-width: 38ch;                      /* ~38 caracteres por linha */
  z-index: 1;
}
.body.center { text-align: center; }

.screenshot-frame {
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.06);
  overflow: hidden;
  max-width: 920px;
  width: 100%;
  z-index: 1;
}
.screenshot-frame img { width: 100%; display: block; } /* sem object-fit/background */

.screenshots-row { display: flex; gap: 16px; width: 100%; max-width: 920px; align-items: stretch; }
.screenshots-row .screenshot-frame { flex: 1; display: flex; }
.screenshots-row .screenshot-frame img { object-fit: cover; object-position: top left; }

.slide-number {
  position: absolute; top: 48px; right: 64px;
  font-family: var(--font-accent);
  font-size: var(--fs-0);
  color: var(--accent);
  z-index: 2;
}

.progress {
  position: absolute; top: 56px; left: 64px;
  display: flex; gap: 8px; z-index: 2;
}
.progress .dot { width: 24px; height: 4px; border-radius: 2px; background: rgba(255,255,255,0.25); }
.progress .dot.active { background: var(--accent); }

.handle {
  position: absolute; bottom: 56px; left: 0; right: 0;
  text-align: center;
  font-family: var(--font-body);
  font-size: var(--fs-0);
  opacity: 0.7; z-index: 2;
}
```

- [ ] **Step 2: Verificar que o CSS é válido (sem chaves desbalanceadas)**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -c "s=open('lib/carrossel/base.css').read(); assert s.count('{')==s.count('}'), 'chaves desbalanceadas'; print('CSS balanceado:', s.count('{'), 'blocos')"
```
Expected: "CSS balanceado: N blocos" sem erro.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/base.css
git commit -m "feat(carrossel-lab): base.css component library do contrato"
```

---

## Fase 3 — QA lint em Python (TDD real)

> Esta é a única parte com código executável de verdade. TDD genuíno: fixture que falha → linter detecta → fixture que passa → linter aprova. O linter recebe um arquivo HTML de slide (que linka/embute o `base.css`) e retorna lista de violações.

### Task 9: Fixtures de teste (HTML que passa e que falha)

**Files:**
- Create: `lib/carrossel/tests/fixtures/slide_ok.html`
- Create: `lib/carrossel/tests/fixtures/slide_low_contrast.html`
- Create: `lib/carrossel/tests/fixtures/slide_tiny_body.html`
- Create: `lib/carrossel/tests/fixtures/slide_contain_bg.html`

- [ ] **Step 1: Criar `slide_ok.html` (deve passar em tudo)**

```html
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
:root{--bg:#16213E;--ink:#FFFFFF;--accent:#E94560;}
.slide{background:var(--bg);color:var(--ink);}
.body{font-size:24px;}
.headline{font-size:76px;}
.screenshot-frame img{width:100%;}
</style></head><body>
<div class="slide">
  <div class="headline">TITULO DA CAPA</div>
  <div class="body">Uma ideia por slide, frase completa.</div>
  <div class="screenshot-frame"><img src="x.png"></div>
</div></body></html>
```

- [ ] **Step 2: Criar `slide_low_contrast.html` (contraste ink↔bg insuficiente)**

```html
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
:root{--bg:#777777;--ink:#888888;--accent:#E94560;}
.slide{background:var(--bg);color:var(--ink);}
.body{font-size:24px;}
.headline{font-size:76px;}
</style></head><body>
<div class="slide">
  <div class="headline">TITULO</div>
  <div class="body">Texto.</div>
  <div class="screenshot-frame"><img src="x.png"></div>
</div></body></html>
```

- [ ] **Step 3: Criar `slide_tiny_body.html` (body < 24px)**

```html
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
:root{--bg:#16213E;--ink:#FFFFFF;--accent:#E94560;}
.slide{background:var(--bg);color:var(--ink);}
.body{font-size:18px;}
.headline{font-size:76px;}
</style></head><body>
<div class="slide">
  <div class="headline">TITULO</div>
  <div class="body">Texto pequeno.</div>
  <div class="screenshot-frame"><img src="x.png"></div>
</div></body></html>
```

- [ ] **Step 4: Criar `slide_contain_bg.html` (object-fit:contain + background proibido)**

```html
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
:root{--bg:#16213E;--ink:#FFFFFF;--accent:#E94560;}
.slide{background:var(--bg);color:var(--ink);}
.body{font-size:24px;}
.headline{font-size:76px;}
.screenshot-frame img{object-fit:contain;background:#000;}
</style></head><body>
<div class="slide">
  <div class="headline">TITULO</div>
  <div class="body">Texto.</div>
  <div class="screenshot-frame"><img src="x.png"></div>
</div></body></html>
```

- [ ] **Step 5: Verificar que os 4 fixtures existem**

Run: `ls lib/carrossel/tests/fixtures/`
Expected: os 4 arquivos `.html`.

- [ ] **Step 6: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/tests/fixtures/
git commit -m "test(carrossel-lab): fixtures HTML para o QA lint"
```

### Task 10: Teste do linter — contraste WCAG (escreve o teste primeiro)

**Files:**
- Create: `lib/carrossel/tests/test_qa_lint.py`

- [ ] **Step 1: Escrever o teste falhando**

```python
import subprocess, sys, os, json
HERE = os.path.dirname(__file__)
LINT = os.path.join(HERE, "..", "qa_lint.py")
FIX = os.path.join(HERE, "fixtures")

def run_lint(fixture):
    out = subprocess.run(
        [sys.executable, LINT, os.path.join(FIX, fixture), "--json"],
        capture_output=True, text=True,
    )
    return json.loads(out.stdout)

def test_low_contrast_is_flagged():
    result = run_lint("slide_low_contrast.html")
    codes = [v["code"] for v in result["violations"]]
    assert "CONTRAST_INK_BG" in codes

def test_ok_slide_has_no_violations():
    result = run_lint("slide_ok.html")
    assert result["violations"] == []
```

- [ ] **Step 2: Rodar e ver falhar (linter ainda não existe)**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_qa_lint.py -v
```
Expected: FAIL — `FileNotFoundError`/JSONDecodeError porque `qa_lint.py` não existe.

- [ ] **Step 3: Commit do teste**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/tests/test_qa_lint.py
git commit -m "test(carrossel-lab): testes de contraste do QA lint (falhando)"
```

### Task 11: Implementar `qa_lint.py` — contraste + estrutura mínima

**Files:**
- Create: `lib/carrossel/qa_lint.py`

- [ ] **Step 1: Escrever o linter (sem dependências externas — regex + cálculo WCAG)**

```python
#!/usr/bin/env python3
"""QA lint do carrossel-lab. Valida HTML de slide contra o contrato de design.
Uso: python3 qa_lint.py <slide.html> [--json]
Sem dependências externas (regex + cálculo WCAG)."""
import re, sys, json

MODULAR = {24, 32, 43, 57, 76, 101, 135}

def _hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _luminance(rgb):
    def chan(c):
        c = c / 255.0
        return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    r, g, b = (chan(x) for x in rgb)
    return 0.2126*r + 0.7152*g + 0.0722*b

def contrast_ratio(hex1, hex2):
    l1, l2 = _luminance(_hex_to_rgb(hex1)), _luminance(_hex_to_rgb(hex2))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

def _find_var(css, name):
    m = re.search(rf'{re.escape(name)}\s*:\s*([^;]+);', css)
    return m.group(1).strip() if m else None

def _first_hex(value):
    if value is None:
        return None
    m = re.search(r'#[0-9A-Fa-f]{3,6}', value)
    return m.group(0) if m else None

def lint(html):
    violations = []
    css = " ".join(re.findall(r'<style>(.*?)</style>', html, re.S))

    bg = _first_hex(_find_var(css, '--bg'))
    ink = _first_hex(_find_var(css, '--ink'))
    accent = _first_hex(_find_var(css, '--accent'))

    if bg and ink:
        if contrast_ratio(ink, bg) < 4.5:
            violations.append({"code": "CONTRAST_INK_BG",
                "msg": f"contraste ink/bg {contrast_ratio(ink, bg):.2f} < 4.5"})
    if bg and accent:
        if contrast_ratio(accent, bg) < 3.0:
            violations.append({"code": "CONTRAST_ACCENT_BG",
                "msg": f"contraste accent/bg {contrast_ratio(accent, bg):.2f} < 3.0"})

    return {"violations": violations}

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    html = open(args[0], encoding="utf-8").read()
    result = lint(html)
    if as_json:
        print(json.dumps(result))
    else:
        if not result["violations"]:
            print("OK — sem violações")
        else:
            for v in result["violations"]:
                print(f"[{v['code']}] {v['msg']}")
    sys.exit(1 if result["violations"] else 0)

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar os testes — devem passar**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/test_qa_lint.py -v
```
Expected: 2 passed (`test_low_contrast_is_flagged`, `test_ok_slide_has_no_violations`).

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/qa_lint.py
git commit -m "feat(carrossel-lab): QA lint com checagem de contraste WCAG"
```

### Task 12: Estender linter — body<24px, object-fit:contain+bg, escala modular

**Files:**
- Modify: `lib/carrossel/tests/test_qa_lint.py`
- Modify: `lib/carrossel/qa_lint.py`

- [ ] **Step 1: Adicionar testes falhando**

Acrescentar a `lib/carrossel/tests/test_qa_lint.py`:

```python
def test_tiny_body_is_flagged():
    result = run_lint("slide_tiny_body.html")
    codes = [v["code"] for v in result["violations"]]
    assert "BODY_TOO_SMALL" in codes

def test_contain_bg_is_flagged():
    result = run_lint("slide_contain_bg.html")
    codes = [v["code"] for v in result["violations"]]
    assert "OBJECTFIT_CONTAIN_BG" in codes

def test_offscale_font_is_flagged():
    # font-size fora da escala modular (ex: 50px) deve ser pego
    import os
    p = os.path.join(FIX, "_tmp_offscale.html")
    open(p, "w").write(
        '<style>:root{--bg:#16213E;--ink:#FFFFFF;--accent:#E94560;}'
        '.slide{background:var(--bg);color:var(--ink);}'
        '.headline{font-size:50px;}.body{font-size:24px;}</style>'
        '<div class="slide"><div class="headline">T</div>'
        '<div class="body">x</div>'
        '<div class="screenshot-frame"><img src="x.png"></div></div>')
    result = run_lint("_tmp_offscale.html")
    os.remove(p)
    codes = [v["code"] for v in result["violations"]]
    assert "FONT_OFF_SCALE" in codes
```

- [ ] **Step 2: Rodar e ver os 3 novos falharem**

Run: `python3 -m pytest lib/carrossel/tests/test_qa_lint.py -v`
Expected: 2 passam, 3 falham (BODY_TOO_SMALL, OBJECTFIT_CONTAIN_BG, FONT_OFF_SCALE não detectados).

- [ ] **Step 3: Estender `lint()` em `qa_lint.py`**

Substituir o `return {"violations": violations}` em `lint()` por (inserir antes do return):

```python
    # body font-size mínimo 24px e dentro da escala modular
    for m in re.finditer(r'\.body\s*\{[^}]*font-size\s*:\s*(\d+)px', css):
        size = int(m.group(1))
        if size < 24:
            violations.append({"code": "BODY_TOO_SMALL",
                "msg": f"body {size}px < 24px"})

    # qualquer font-size declarado deve estar na escala modular
    for m in re.finditer(r'font-size\s*:\s*(\d+)px', css):
        size = int(m.group(1))
        if size not in MODULAR:
            violations.append({"code": "FONT_OFF_SCALE",
                "msg": f"font-size {size}px fora da escala modular {sorted(MODULAR)}"})

    # object-fit: contain combinado com background no mesmo bloco de screenshot
    for block in re.findall(r'\{[^}]*\}', css):
        if 'object-fit' in block and 'contain' in block and 'background' in block:
            violations.append({"code": "OBJECTFIT_CONTAIN_BG",
                "msg": "object-fit:contain + background cria bordas escuras"})

    return {"violations": violations}
```

- [ ] **Step 4: Rodar todos os testes — devem passar**

Run: `python3 -m pytest lib/carrossel/tests/test_qa_lint.py -v`
Expected: 5 passed.

> Nota: `slide_ok.html` usa só 24px e 76px (ambos na escala) e não tem object-fit:contain, então continua sem violações.

- [ ] **Step 5: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/qa_lint.py plugins/dna-operacional/lib/carrossel/tests/test_qa_lint.py
git commit -m "feat(carrossel-lab): QA lint detecta body pequeno, off-scale e object-fit:contain"
```

---

## Fase 4 — Render harness + screenshot engine (docs)

### Task 13: `render.md` (harness determinístico)

**Files:**
- Create: `lib/carrossel/render.md`

- [ ] **Step 1: Escrever o arquivo**

````markdown
# Render Harness Determinístico

Procedimento FIXO de render (idêntico para todas as teses — isola a variável no torneio).

## Passos

1. Salvar o HTML do slide no diretório de trabalho, linkando `base.css` (copiar `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/base.css` pra `./base.css`).
2. Copiar fontes locais pra `./fonts/` (ver `references/carrossel-lab/fonts-config.md`); detectar LOCAL vs FALLBACK.
3. **Rodar QA lint ANTES de renderizar:** `python3 ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/qa_lint.py <slide.html>`. Se sair com violações (exit≠0), corrigir o HTML e repetir. **Não renderiza slide que não passa no lint.**
4. Servir via `python3 -m http.server <porta livre>`.
5. Abrir via Playwright no viewport do formato (4:5 = 1080×1350; 3:4 = 1080×1440; 1:1 = 1080×1080).
6. Aguardar 3s pras fontes carregarem.
7. Capturar PNG do slide.
8. Para overlay transparente: `omitBackground: true`.
9. **Fechar o browser após cada slide.**

## Auto-review visual (reduzido)

O QA lint já cobriu o objetivo (contraste, tamanho, object-fit, escala). O auto-review humano/visual foca só no subjetivo: hierarquia, respiro, "tá bonito?", órfã, PT-BR natural. Ler cada PNG via `Read`.
````

- [ ] **Step 2: Verificar**

Run: `grep -c "qa_lint.py" lib/carrossel/render.md`
Expected: ≥1 (o harness invoca o lint).

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/render.md
git commit -m "feat(carrossel-lab): render harness determinístico com gate de lint"
```

### Task 14: `screenshot-engine.md` (captura real → réplica fiel)

**Files:**
- Create: `lib/carrossel/screenshot-engine.md`

- [ ] **Step 1: Escrever o arquivo**

````markdown
# Screenshot Engine

Ordem: **captura real > réplica fiel em HTML > pedir ao user**.

## 1. Captura real

Seguir `references/carrossel-lab/screenshot-guide.md` por fonte (X, Instagram, GitHub, notícia, etc.). Traduzir texto em inglês via DOM antes de capturar (PT-BR). Camuflar dados sensíveis.

## 2. Réplica fiel (se a captura falhar)

Recriar o componente real em HTML/CSS com cara de verdade (ver seção "Réplica fiel" em `screenshot-guide.md`). Marcar `data-replica="true"`. Renderizar como PNG via o render harness e usar como o screenshot do slide.

## 3. Fallback manual

Se nem captura nem réplica servirem, pedir o arquivo ao user e aplicar o `.screenshot-frame`.

## Honestidade (regra dura)

Réplica reproduz a forma, não fabrica fato. Número/citação dentro da réplica ou vem da fonte real, ou é claramente ilustrativo. Nunca apresentar réplica como print autêntico.
````

- [ ] **Step 2: Verificar**

Run: `grep -c "réplica\|replica" lib/carrossel/screenshot-engine.md`
Expected: ≥2.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/carrossel/screenshot-engine.md
git commit -m "feat(carrossel-lab): screenshot engine captura-real-ou-réplica"
```

---

## Fase 5 — Commands das 3 teses

> Todos compartilham um esqueleto comum (Pre-check DNA Mode → Passo 0 Handle → research-first → gates → render via harness → QA lint → entrega). A diferença é o **motor**. Para DRY, o esqueleto comum é descrito uma vez aqui e cada task referencia este bloco literalmente.

**ESQUELETO COMUM (usado nas Tasks 15–17, copiar literalmente e ajustar a seção "## Motor"):**

````markdown
---
description: [específico da tese]
argument-hint: "[tópico|URL|path-de-briefing?]"
---

Usuário invocou `/[nome]` com argumento: `$ARGUMENTS`

## Pre-check — DNA Mode (low-cost)

Ler `CLAUDE.md` → `## DNA Mode: <x>` (default: full). O torneio sempre roda em **full** (lowcost não se aplica ao lab). Se lowcost, avisar que o lab ignora e segue full.

## Passo 0: Resolver Handle

Ler `CLAUDE.md` → `## Handle: @<x>`. Fixar em `${USER_HANDLE}`. Sem handle: perguntar uma vez via `AskUserQuestion`.

## Passo 1: Research-first

Antes de qualquer copy: pesquisar o tema/notícia (Playwright/WebSearch) e ler:
- `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/algoritmo-ig.md`
- `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/hooks-frameworks.md`
- `${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/design-premium.md`
- `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/design-contract.md`

## Passo 2: Briefing

Coletar: objetivo, template (`references/carrossel-lab/templates.md`), formato (default 4:5), handle (Passo 0).

## [Gates específicos do motor — ver "## Motor"]

## Passo N: Render

Para cada slide, seguir `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/render.md` (inclui gate de QA lint). Screenshots via `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/screenshot-engine.md`.

## Passo N+1: Entrega

Salvar PNGs + `roteiro.md` (textos, caption, 5 hashtags, caminhos). Aplicar `/humanizer` na copy (delegação, não cascata).

## Motor

[ÚNICO BLOCO QUE DIFERE ENTRE AS TESES]
````

### Task 15: `carrossel-lab-hybrid.md` (Hybrid Director)

**Files:**
- Create: `commands/carrossel-lab-hybrid.md`

- [ ] **Step 1: Criar o arquivo usando o ESQUELETO COMUM acima, com `description` e `## Motor` abaixo**

`description`: `Tese Hybrid Director do carrossel-lab: research-first + best-of-N só na capa e na direção visual + pipeline de especialistas. Uso: torneio de carrossel, não produção diária.`

Bloco `## Motor`:

````markdown
## Motor — Hybrid Director

Pareto: capa/hook e direção visual decidem o carrossel. Best-of-N só neles.

### Gate A — Best-of-N de capa
1. Gerar **5 hooks** cobrindo padrões distintos de `hooks-frameworks.md`.
2. Juiz interno escolhe por *information gap delimitado* (Loewenstein). Justificar.
3. Slide 2 = confirmador de swipe (restate + 1º loop).

### Gate B — Best-of-N de direção visual
1. Propor **3 direções** (paleta de `palettes.md` + efeito de `headline-effects.md` + composição), ancoradas no moodboard (`visual-research.md`).
2. Renderizar **preview real do slide 1** das 3 (via render harness).
3. Juiz interno escolhe por impacto. Apresentar ao user pra aprovação.

### Pipeline de especialistas (resto)
- Arquiteto de narrativa: arco explícito (1 de PAS/AIDA/BAB/listicle/story), open loop entre slides.
- Diretor de arte: aplica direção aprovada a todos os slides (motifs persistentes).
- Render + QA: harness + lint por slide.
````

- [ ] **Step 2: Verificar frontmatter e referências**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
head -4 commands/carrossel-lab-hybrid.md | grep -c "description:"
grep -c "carrossel-lab/\|lib/carrossel/" commands/carrossel-lab-hybrid.md
```
Expected: `description:` presente; ≥4 referências a arquivos do lab.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/commands/carrossel-lab-hybrid.md
git commit -m "feat(carrossel-lab): command tese Hybrid Director"
```

### Task 16: `carrossel-lab-viral.md` (Viral Engineer)

**Files:**
- Create: `commands/carrossel-lab-viral.md`

- [ ] **Step 1: Criar o arquivo usando o ESQUELETO COMUM, com `description` e `## Motor` abaixo**

`description`: `Tese Viral Engineer do carrossel-lab: capa dupla (second-chance), engenharia de send/save, open loops obrigatórios, best-of-N agressivo de hook. Uso: torneio de carrossel.`

Bloco `## Motor`:

````markdown
## Motor — Viral Engineer

Aposta em alcance/retenção (base: `algoritmo-ig.md`).

### Capa dupla autônoma
- **Slide 1 E slide 2** são ambos capa completa e independente (o IG re-entra pelo slide 2). Cada um para o scroll sozinho.

### Best-of-N agressivo de hook
- Gerar **8–12 hooks** (todos os padrões de `hooks-frameworks.md`).
- Lint de retenção: reprovar hook genérico, body >30 palavras, jargão, frase cortada, slide sem função.
- Forçar especificidade numérica nos hooks de resultado.

### Engenharia de send/save
- Slide final pede **save com motivo** ("salva pra usar depois") **e** dá **razão de DM** ("manda pra quem precisa") — sends movem alcance unconnected.
- Sugerir música (elegibilidade aba Reels).

### Open loop obrigatório
- Cada slide termina abrindo loop pro próximo (slippery slide). Slide que se fecha sozinho é **reprovado e reescrito**.
- Uma ideia por slide + mini-headline "road sign" 4–7 palavras.

### Arco explícito
- Escolher 1 (PAS/AIDA/BAB/listicle-escalada/story) antes de redigir; reprovar carrossel sem progressão.
````

- [ ] **Step 2: Verificar**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
head -4 commands/carrossel-lab-viral.md | grep -c "description:"
grep -c "capa dupla\|send/save\|open loop\|Open loop" commands/carrossel-lab-viral.md
```
Expected: `description:` presente; ≥2 termos do motor viral.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/commands/carrossel-lab-viral.md
git commit -m "feat(carrossel-lab): command tese Viral Engineer"
```

### Task 17: `carrossel-lab-editorial.md` (Editorial Premium)

**Files:**
- Create: `commands/carrossel-lab-editorial.md`

- [ ] **Step 1: Criar o arquivo usando o ESQUELETO COMUM, com `description` e `## Motor` abaixo**

`description`: `Tese Editorial Premium do carrossel-lab: escala modular, contraste WCAG, grid 8pt, motifs persistentes, best-of-N de direção de arte. Cara de revista. Uso: torneio de carrossel.`

Bloco `## Motor`:

````markdown
## Motor — Editorial Premium

Aposta em design top-tier (base: `design-premium.md` + `design-contract.md`).

### Disciplina visual rígida
- Escala modular 1.333, contraste WCAG, grid 8pt — todos validados pelo QA lint (sem exceção).
- Espaço negativo intencional; curva texto→visual ao longo da sequência.

### Motifs persistentes (todos os slides)
- Numeração `01/07`, barra de progresso própria, handle no rodapé, label de seção — mesmos coords/estilo (componentes do `base.css`).

### Best-of-N de direção de arte
- Gerar **3 composições/layouts** distintos para o slide 1 (não de copy — de arte).
- Renderizar preview real das 3 (render harness).
- Juiz interno escolhe a mais "revista premium". User aprova.

### Par tipográfico
- Display + sans dentro do contrato. Default Nofex/Inter; pode propor par editorial (ex: Playfair+DM Sans) **se as fontes estiverem disponíveis** (senão fallback Google Fonts). Nunca 3ª família fora dos papéis.
````

- [ ] **Step 2: Verificar**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
head -4 commands/carrossel-lab-editorial.md | grep -c "description:"
grep -c "motif\|Motif\|escala modular\|WCAG" commands/carrossel-lab-editorial.md
```
Expected: `description:` presente; ≥2 termos do motor editorial.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/commands/carrossel-lab-editorial.md
git commit -m "feat(carrossel-lab): command tese Editorial Premium"
```

---

## Fase 6 — Orquestrador + juiz cego

### Task 18: `carrossel-torneio.md` (orquestrador)

**Files:**
- Create: `commands/carrossel-torneio.md`

- [ ] **Step 1: Escrever o command**

````markdown
---
description: Roda um torneio de carrosséis — controle atual + 3 teses do lab — sobre a mesma notícia, julga cego por 5 dimensões e deixa o user escolher o vencedor. Uso: avaliação, não produção.
argument-hint: "<URL ou tema da notícia>"
---

Usuário invocou `/carrossel-torneio` com argumento: `$ARGUMENTS`

## Passo 0: Brief normalizado

1. Resolver handle (`CLAUDE.md` → `## Handle:`).
2. A partir de `$ARGUMENTS` (URL/tema), pesquisar e montar **um brief único**: objetivo, público, fatos-chave, formato (default 4:5). Este brief é entregue **idêntico** aos 4 motores.
3. Criar diretório do torneio: `./torneio-<slug>/` com subpastas `motor-controle/`, `motor-hybrid/`, `motor-viral/`, `motor-editorial/`.

## Passo 1: Rodar os 4 motores

Para cada motor, gerar o carrossel completo no seu diretório, com o MESMO brief:
- **Controle:** seguir `${CLAUDE_PLUGIN_ROOT}/commands/carrossel-instagram.md` (sem modificação).
- **Hybrid:** seguir `${CLAUDE_PLUGIN_ROOT}/commands/carrossel-lab-hybrid.md`.
- **Viral:** seguir `${CLAUDE_PLUGIN_ROOT}/commands/carrossel-lab-viral.md`.
- **Editorial:** seguir `${CLAUDE_PLUGIN_ROOT}/commands/carrossel-lab-editorial.md`.

Mesmo formato, mesma config de fonte, mesmo piso. Controle usa suas próprias references; teses usam `carrossel-lab/`.

## Passo 2: Anonimizar (juiz cego)

1. Gerar um embaralhamento dos 4 motores → rótulos neutros `competidor-1..4`. **Não usar a ordem do Passo 1.**
2. Copiar os PNGs de cada `motor-*/` para `./torneio-<slug>/competidor-N/` conforme o embaralhamento.
3. Salvar o mapping motor→competidor em `./torneio-<slug>/.mapping.json` (NÃO mostrar ainda).

## Passo 3: Juiz cego

Avaliar APENAS os `competidor-N/` (sem saber qual motor é qual). Para cada competidor, pontuar **0–10 em cada uma das 5 dimensões**, com justificativa, **slide-a-slide E carrossel inteiro**:
1. Força viral / retenção (usar critérios de `algoritmo-ig.md`).
2. Copy / hook / narrativa (`hooks-frameworks.md`).
3. Design / impacto visual (`design-premium.md`).
4. Consistência / menos retrabalho (quantas violações o QA lint pegou; quão coeso).
5. Screenshots reais ou réplica fiel (qualidade/credibilidade do visual de prova).

Pesos default iguais (ajustáveis pelo user antes do julgamento). Produzir ranking.

## Passo 4: Montagem e revelação

1. Montar comparação lado-a-lado (capa de cada competidor + grade completa).
2. Apresentar a tabela de notas + justificativas + ranking.
3. **Só então** revelar o `.mapping.json` (qual competidor era qual motor).
4. Pedir o **veredito final do user** (juiz dá nota; decisão é humana).

## Passo 5: Aprendizado

Registrar o que ganhou e por quê em `learnings/` do projeto. **Não** promover nada a `carrossel-instagram` v2 sem aceite explícito do user (fora do escopo desta rodada).

---

✅ Torneio rodado — 4 carrosséis, juiz cego, veredito do user.
````

- [ ] **Step 2: Verificar que referencia os 4 motores e o mapping**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
grep -c "carrossel-instagram.md\|carrossel-lab-hybrid\|carrossel-lab-viral\|carrossel-lab-editorial" commands/carrossel-torneio.md
grep -c "mapping\|competidor" commands/carrossel-torneio.md
```
Expected: 4 motores referenciados; ≥2 menções a mapping/competidor.

- [ ] **Step 3: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/commands/carrossel-torneio.md
git commit -m "feat(carrossel-lab): orquestrador de torneio com juiz cego"
```

---

## Fase 7 — Infra e smoke test

### Task 19: Atualizar `low-cost-heuristics.md` e bump de versão

**Files:**
- Modify: `lib/mode/low-cost-heuristics.md`
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Adicionar entradas das teses ao `low-cost-heuristics.md`**

Acrescentar após a seção `## /carrossel-instagram`:

````markdown
## /carrossel-torneio, /carrossel-lab-hybrid, /carrossel-lab-viral, /carrossel-lab-editorial

- **Full:** pipeline completo do lab (research-first, best-of-N, render+QA lint).
- **Lowcost:** NÃO se aplica — o lab é ferramenta de avaliação, sempre roda em full. Em lowcost, avisar e seguir full.
- **Redução estimada:** 0% (intencional).
- **Acceptance:** o torneio precisa de qualidade máxima pra ser comparação justa.
````

- [ ] **Step 2: Bump de versão no `plugin.json`**

Trocar `"version": "0.4.0"` por `"version": "0.5.0"` em `.claude-plugin/plugin.json`.

- [ ] **Step 3: Verificar JSON válido**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])"
```
Expected: `0.5.0`.

- [ ] **Step 4: Commit**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git add plugins/dna-operacional/lib/mode/low-cost-heuristics.md plugins/dna-operacional/.claude-plugin/plugin.json
git commit -m "chore(carrossel-lab): heurísticas lowcost + bump 0.5.0"
```

### Task 20: Smoke test do piso (lint + estrutura) e validação do plugin

**Files:** (nenhum — só verificação)

- [ ] **Step 1: Rodar a suíte de testes do linter completa**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 -m pytest lib/carrossel/tests/ -v
```
Expected: 5 passed.

- [ ] **Step 2: Rodar o lint no `slide_ok` e num slide real do base.css embutido**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
python3 lib/carrossel/qa_lint.py lib/carrossel/tests/fixtures/slide_ok.html
echo "exit: $?"
```
Expected: "OK — sem violações", exit 0.

- [ ] **Step 3: Verificar que todos os artefatos do lab existem**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional
ls references/carrossel-lab/*.md | wc -l            # esperado: 9
ls lib/carrossel/*.md lib/carrossel/*.css lib/carrossel/*.py | wc -l   # esperado: 5 (design-contract, render, screenshot-engine, base.css, qa_lint.py)
ls commands/carrossel-lab-*.md commands/carrossel-torneio.md | wc -l   # esperado: 4
```
Expected: 9, 5, 4.

- [ ] **Step 4: Confirmar que o controle NÃO foi tocado**

Run:
```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git log --oneline main..ahoydig/carrossel-torneio -- plugins/dna-operacional/commands/carrossel-instagram.md plugins/dna-operacional/references/carrossel-instagram/ | wc -l
```
Expected: `0` (nenhum commit tocou o controle).

- [ ] **Step 5: Commit final (se houver ajustes) e resumo**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional
git status --short
```
Expected: working tree limpo (tudo commitado).

### Task 21: Torneio de fumaça com a notícia real do usuário

> Esta task é a validação end-to-end. Requer a notícia/URL que o usuário vai fornecer (decisão "Você me dá a notícia/URL" do brainstorming). É uma task **interativa** — roda o fluxo completo uma vez.

- [ ] **Step 1: Pedir a URL/tema ao usuário** (se ainda não fornecida) e rodar `/carrossel-torneio <url>`.

- [ ] **Step 2: Confirmar que os 4 motores geraram** PNGs em `torneio-<slug>/motor-*/`.

- [ ] **Step 3: Confirmar anonimização** — `competidor-1..4/` existem e `.mapping.json` está embaralhado (não na ordem controle→hybrid→viral→editorial).

- [ ] **Step 4: Confirmar que o juiz pontuou** as 5 dimensões slide-a-slide + inteiro, e que o mapping só foi revelado após o ranking.

- [ ] **Step 5: Veredito do usuário** registrado em `learnings/`.

---

## Self-Review (preenchido pelo autor do plano)

**Cobertura do spec:**
- §4 lab isolado → Tasks 0, 15–18 ✓
- §5.1 knowledge base → Tasks 1–6 ✓
- §5.2 contrato de design → Tasks 7–8 ✓
- §5.3 render harness → Task 13 ✓
- §5.4 QA lint → Tasks 9–12 ✓
- §5.5 screenshot engine → Task 14 ✓
- §5.6 research-first → embutido no esqueleto comum (Tasks 15–17, Passo 1) ✓
- §6 as 3 teses → Tasks 15–17 ✓
- §7 juiz + protocolo → Task 18 ✓
- §8 escopo (não promover v2) → Task 18 Passo 5 ✓
- §9 lowcost não se aplica → Task 19 ✓

**Consistência de tipos/nomes:** códigos de violação do lint (`CONTRAST_INK_BG`, `CONTRAST_ACCENT_BG`, `BODY_TOO_SMALL`, `FONT_OFF_SCALE`, `OBJECTFIT_CONTAIN_BG`) usados consistentemente entre Tasks 10, 11, 12. Classes CSS (`.slide`, `.headline`, `.body`, `.screenshot-frame`, `.slide-number`, `.progress`, `.handle`) consistentes entre Task 8 (base.css), Task 7 (contrato) e Task 17 (motifs).

**Placeholders:** nenhum TODO/TBD/"similar a Task N" no conteúdo de implementação. Task 21 depende de input externo (URL do user) por design — está marcado como interativo, não é placeholder.
