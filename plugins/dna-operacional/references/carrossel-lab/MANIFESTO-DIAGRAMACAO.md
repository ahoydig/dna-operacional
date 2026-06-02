# MANIFESTO DE DIAGRAMAÇÃO — Carrosséis Virais Claude Code/IA

> Destilado de 10 RECEITAs de engenharia reversa. 3 contas: **@itstylergermain** (7), **@noevarner.ai** (2), **@tenfoldmarc** (1). Total ~83K engajamentos. Foco: precisão técnica para reconstruir em HTML/CSS e gerar assets por IA.
>
> Cada conta tem dialeto próprio dentro do mesmo sistema. Quando divergem, o manifesto dá o RANGE e marca o mais comum. **Tyler Germain (7/10) é o padrão dominante.**

---

## 0. AS 3 ESCOLAS (calibre tudo por isto)

| Escola | Fundo | Headline | Accent | Elemento herói | Mascote |
|---|---|---|---|---|---|
| **Tyler Germain** (dominante, 7 posts) | Preto `#0d0d0d`–`#1a1a1a` (conteúdo); foto darkened (capa/CTA) | Mix: serif bold OU sans condensed black | Terracota `#C4714A`–`#E8805A` | Screenshot real OU code box | Pixel-art 8-bit (varia por post) |
| **Noe Varner** (2 posts) | Preto roxo `#0a0007`–`#0d0008` + ondas; foto praia/Rio (capa/CTA) | Sans black/900 (Archivo/Inter) | Coral-laranja `#E8602A`–`#E8673A` | Screenshot real + composição | **Voxel 3D laranja conectado por cabo** |
| **Tenfold Marc** (1 post) | **Creme claro `#F2EDE6`** (ÚNICO claro) | Sans black + **serif itálica accent** | Rust `#B85C38` | **Dashboard gerado por IA (shadcn)** | Nenhum |

**Regra-mãe que TODAS compartilham:** fundo de alto contraste + headline gigante + UMA palavra/cor accent + UM elemento-herói por slide + footer fixo + CTA "Comment [PALAVRA]". A diferença é só o dialeto.

---

## 1. CANVAS & GRID

**Dimensão:** `1080 × 1350px` (4:5 portrait) — padrão absoluto, 8/10 posts.
- Exceções: Tenfold usa `928 × 1232px` (≈3:4); DYpVlG estima `1008×1260`. Todos convergem em **4:5 portrait**. Use **1080×1350**.

**Padding lateral (o "eixo de coluna" — valor mais citado):**
- **`48px` de cada lado** é o valor canônico (Tyler DW1rsdxkY2w, Tenfold, DYpVlG). Range observado: `48–65px` (≈4.4%–6%).
- Tyler DWSJiOqkcbi usa `58px`; Noe usa `~5.5%` (~60px). **Default: 48px.**

**A regra do padding-x consistente (CRÍTICA — é o segredo do "alinhamento maravilhoso" do Tenfold):**
- Headline, screenshot/card, code box e footer **TODOS começam no mesmo `margin-left: 48px`**.
- Largura de conteúdo: `width: calc(100% - 96px)` para os 3 elementos principais.
- A **esquerda é sagrada** (left-align nos slides internos); a direita varia (headline mais curta, card/código mais largos). O olho lê como grid sem ver grid.
- Topo: `~60–72px`. Base: `~48–80px` (reservar para footer).

---

## 2. SISTEMA DE ZONAS VERTICAIS (template-base de slide de conteúdo)

Estrutura canônica topo→base. Há **duas variantes dominantes**:

### Variante A — "Screenshot/Card no meio" (mais comum)
| Zona | % altura | Conteúdo |
|---|---|---|
| Topo / âncora | 0–12% | Logo Claude OU watermark número OU vazio |
| Headline + step/play label | 12–30% | Label pequeno + headline gigante |
| Subtítulo / impacto | 30–45% | 1 linha sub + 1 linha accent (itálico) |
| **Elemento herói** | 45–88% | Screenshot real / code box / card |
| Footer | 88–100% | Handle + save/swipe |

### Variante B — "Code box embaixo" (Tyler prompts)
| Zona | % altura | Conteúdo |
|---|---|---|
| Watermark "Prompt #N" (ghost) | 0–18% | Numeração tipográfica gigante opacity 4% |
| Headline H2 (serif) + sublinhado | 18–42% | Headline + underline handwritten |
| Sub-label handwritten + seta | 42–50% | "Send Claude this message" + seta curva |
| **Code box** | 50–88% | Bloco de prompt monospace |
| Footer | 88–100% | Handle + save |

**Como evitam "buraco" (preencher o canvas):**
1. **Elemento herói grande** (35–48% da altura) ancora a metade inferior.
2. **Mascote/voxel "vaza" da borda** (Tyler/Noe) preenche o canto direito e o respiro entre headline e herói.
3. **Watermark ghost** (opacity 4%) ocupa a zona superior sem peso visual.
4. **Headline gigante** (ver §3) toma 18–30% sozinha.
5. **Tenfold faz o OPOSTO no CTA:** deixa ~28% vazio embaixo de propósito = sinal de autoridade ("não preciso encher").
6. Background com ondas/topografia/noise dá textura sem competir.

---

## 3. TIPOGRAFIA

### Headline — há DOIS sistemas concorrentes:

**Sistema 1 — Sans condensada black/900** (Noe sempre; Tyler em ~metade; Tenfold na sans)
- Fontes: **Anton** (mais citada como match), **Bebas Neue**, **Archivo Black**, **Barlow Condensed 900**, Inter 900/Impact.
- Peso: **900 (black)**. Tracking negativo `-0.02em`. Line-height `0.9–1.05` (muito tight).
- ALL CAPS frequente (Noe capa, Tyler DWSJiOqkcbi, DYpVlG).

**Sistema 2 — Serif bold/black** (Tyler DV9/DW1; Tenfold accent)
- Fontes: **Playfair Display Bold/ExtraBold** (mais citada), Libre Baskerville Bold, Abril Fatface, Cormorant.
- Peso: 700–800. A palavra accent costuma ser **serif itálica**.

> **Decisão:** Tyler alterna entre os dois conforme o post. **Anton/Bebas (sans condensed)** e **Playfair (serif)** são os dois pilares. Escolha um por carrossel e mantenha.

**Tamanho da headline (é GIGANTE — range concreto, escala 1080px):**
- Capa: **`80–140px`** (Tyler DV9 capa 80–96px; Tyler/Tenfold sans condensed chega a `140px`; DWSJiOqkcbi reporta `~185px` em Bebas condensada — letras condensadas permitem extremos).
- Slides internos: **`52–110px`** (mais comum `64–88px`).
- CTA: **a MAIOR do carrossel** sempre (`96–120px+`). Regra: escalada de intensidade no fim.
- Tenfold faz **rampa crescente** dentro da capa: `96 → 112 → 124px` (palavra de valor é a maior).

**O padrão "palavra colorida" (o accent tipográfico):**
- **Forma mais comum: cor sólida accent** numa palavra-chave (produto: "Claude Code", "Claude", ou o benefício).
- **Serif itálico accent:** Tyler (DV9, DW1) e Tenfold trocam a última palavra/frase por **serif itálica na cor accent** (`*Content Dashboard*`, `*get started.*`) — ponto final SEMPRE incluído na palavra itálica (detalhe refinado).
- **Highlight block (marca-texto):** DYpVlG usa retângulo accent ATRÁS do texto (`background-color: accent; padding: 0 8px 2px`), não cor no texto.
- **Regra de ouro:** **exatamente 1 palavra/grupo accent por headline**. Nunca duas.
- Variação Tyler: a 2ª linha às vezes vai em **cinza** (`#888888`) em vez de accent — hierarquia sem mudar tamanho.
- Contra-intuitivo (DWHr4SzkecE): às vezes o accent cai no VERBO/artigo, não no substantivo, pra forçar leitura completa.

**Corpo / subtítulo:**
- **Inter** ou **DM Sans**, peso 400–500. Tamanho `~22–28px` (4–5% da altura). Cor: branco `#FFF` ou cinza claro `#CCC`/`#D1D1D1`. Line-height 1.4–1.5.
- A "linha de impacto" abaixo do sub vai em **itálico na cor accent** (Noe: "I stopped guessing what to post.").

**Handwritten (anotações, sub-labels, CTA):**
- **Caveat** (mais citada), alternativas Kalam, Patrick Hand, Permanent Marker, Pacifico/Dancing Script (DYpVlG no footer).
- Tamanho `28–48px`. Cor: branco OU accent. Uso **limitado a 2 funções** (sub-label + CTA keyword) — mais que isso vira caos.

**Mono (prompt/code box):**
- **JetBrains Mono** (mais citada) ou Fira Code. Peso 400. Tamanho `~19–24px` (canvas) = ~13–14px visual. Line-height 1.55–1.7.

**Import canônico Google Fonts:**
```
Anton + Bebas Neue + Playfair Display(700,800,ital) + Inter(400,500,700,900)
+ Caveat(400,700) + JetBrains Mono(400)
```

---

## 4. CORES

### Paleta dominante (hex que mais se repetem):

**Fundo:**
- Escuro: **`#0d0d0d`** (mais comum) → `#0a0a0a` → `#111111` → `#1a1a1a`. Noe puxa pra roxo-vinho: `#0d0008` / `#0a0007`.
- Claro: **`#F2EDE6`** creme (SÓ Tenfold).
- Texto sobre claro: `#1A1209` (preto-marrom, nunca preto puro).

**Texto:**
- Branco: **`#FFFFFF`** (dominante). Tyler DW1 usa creme `#f5f0eb`. Cinza body: `#CCCCCC`/`#D1D1D1`/`#DDDDDD`.

**Accent (a cor que define cada conta — TODAS na família laranja/terracota):**
| Conta | Hex accent |
|---|---|
| Noe Varner | **`#E8602A`** / `#E8673A` (coral-laranja saturado) |
| Tyler (terracota) | **`#C4714A`** / `#C8613A` / `#D4734A` / `#c9764a` (terracota/cobre — "NÃO laranja puro") |
| Tyler (salmão) | `#E07A5F` / `#E8805A` / `#E8714A` |
| Tenfold | **`#B85C38`** (rust, o mais escuro) |

> **Faixa accent consolidada: laranja-coral a terracota, `#B85C38`–`#E8673A`.** Para clonar Tyler use **`#C4714A`–`#D4734A`**. Para Noe use **`#E8602A`**.

**Vermelho de destaque (DIFERENTE do accent):** `#E03030`/`#E53935`/`#E8453C`/`#FF5F57` — usado SÓ para bordas/setas de "OLHA AQUI" em screenshots. Quebra o sistema laranja de propósito.

**Verde (crescimento):** `#43A047`/`#4CAF50` — só em métricas/sparklines positivas e círculos "depois".

### Claro vs escuro:
**Escuro PREDOMINA esmagadoramente (9/10).** Só Tenfold é claro. O escuro vende "tech/sofisticado" e faz screenshots brancos e code boxes flutuarem com contraste máximo.

### Regra do accent (quando usar):
1. **Headline:** 1 palavra accent por slide.
2. **Linha de impacto:** itálico accent.
3. **Code box:** borda accent + keywords accent.
4. **Setas/anotações handwritten:** accent.
5. **Reserva psicológica (DYpVlG, DWSJiOqkcbi):** alguns reservam o accent **APENAS para capa + CTA**, deixando os slides de conteúdo monocromáticos (branco). Cria "arco emocional": entra com energia → relaxa → fecha com pressão. **Tática deliberada.**

---

## 5. ELEMENTO VISUAL (o herói de cada slide)

Tipos catalogados, com specs de integração:

### A. Screenshot real (o mais credível — "proof of work")
- **O quê:** captura real da UI (Claude.ai, terminal Claude Code, VSCode Extensions, Supabase, Instagram Insights, app próprio Next.js).
- **Tamanho:** `~85–95%` da largura, `~38–48%` da altura.
- **Moldura:** `border-radius: 8–16px` (12–16 mais comum). `box-shadow` densa em camadas: `0 20px 60px rgba(0,0,0,0.5–0.7)` — profundidade.
- **Captura limpa:** sem chrome do browser (DevTools "capture node screenshot"), Retina 2x. Mac window dots (●●●) quando é terminal.
- **Integração:** flutua sobre fundo escuro; às vezes rotacionado `±5–8°` (Tyler DV1 site VSCode) pra quebrar grid.
- **Crop intencional:** corta "above the fold", mostra só o que importa. Zoom extremo isola UM ícone (Tyler DV1 toolbar).

### B. App construído + screenshotado (variação de A)
- Tyler DV9 (Shipyard Next.js+shadcn) e Tenfold (dashboard shadcn terracota).
- **Tenfold é GERADO por IA via Claude Code** (não captura de app pré-existente): shadcn/ui + tema custom, dados fictícios mas coerentes (287.4K, $48.2K), screenshot sem chrome. Estado ativo da sidebar muda por slide.
- Specs: `~78% largura, ~35% altura, border-radius 16px, box-shadow 0 2px 16px rgba(0,0,0,0.08)` (sombra MUITO suave no fundo claro). Sidebar 28% + main 72%.

### C. Bloco de prompt / code box (CSS puro — NÃO screenshot)
- **O quê:** `<div>` estilizado imitando editor/terminal. Texto = prose com highlight seletivo (não código real).
- **Specs:** `border: 1.5–2px solid [accent]`, `border-radius: 8–12px`, fundo `#111`/`#0d0d0d`/`#1a1410` (marrom-escuro com tint quente), padding `24–32px`.
- **Box-shadow: NENHUM (flat)** — a borda accent é suficiente.
- Mono, texto branco, **keywords/substantivos-chave em accent** (pseudo-syntax-highlight: `/memory`, `decisions.md`, `Supabase`, `cron job`).
- Parágrafos separados por linha em branco. Sem números de linha, sem language tag.
- Variação terminal (DWSJiOqkcbi): adiciona `●●●` macOS dots no topo + label `#Prompt:`.

### D. Imagem gerada por IA
- **Mascote/voxel** (ver §6).
- **Foto-fundo aspiracional** (praia, Rio, gym, setup dev) — ver §5G.
- **Logo Instagram 3D** glossy (Noe) — gerado, não o flat oficial.
- **Cabo USB/Lightning 3D** (Noe) — render isolado PNG transparente.
- **Dashboard fake** (Tenfold, via Claude Code — tecnicamente "construído" não "gerado por difusão").

### E. Infográfico (gerado, estilo "papel/whiteboard")
- Tyler DV1 slide 07 "FILE STRUCTURE": árvore de diretório, fundo creme `#F5F0E8`, emojis de pasta, destaques coloridos por pasta, 4 estrelinhas (✦) nos cantos. Contraste claro sobre slide escuro.

### F. Foto + logo composta (capa Noe DYksqdyFjt4)
- Cut-out real (Hormozi, fundo removido via Remove.bg) + capas de livros reais sobrepostas em leque + seta `→` + app icon Claude. Tudo remontado em Figma/Canva (NÃO IA generativa).

### G. Foto-fundo (capa + CTA)
- Foto real do criador (setup dev, praia, Rio, gym, rua). **Overlay escuro `rgba(0,0,0,0.55–0.72)`** flat ou gradiente (mais denso na base). `filter: brightness(0.35–0.45)`.
- DYpVlG: foto única em **3 estados** (nítida capa / `blur(20px)` itens / `blur(20px) brightness(0.35)` CTA) — economia de assets + coesão.

### Folder emoji macOS (DYpVlG — substitui screenshot)
- macOS Big Sur folder (`#6BB8E8` azul) com asterisco Claude dentro. ~38% da largura. "Produto tangível" universal, zero captura.

---

## 6. MASCOTE (importante)

### Mascote NOE VARNER — voxel 3D laranja + cabo (descrição PRECISA para gerar igual):

**Estilo:** Pixel-art / **voxel 3D isométrico** (não 2D plano). Render 3D com profundidade, sombras suaves, iluminação lateral. "Minecraft-style mob em alta qualidade" / "3D low-poly voxel character".

**Forma:** corpo quadrado/retangular de **cubos empilhados**, mais largo que alto (~1.2:1) — "robô caixote" / "computador arcade antigo". Cabeça = bloco cúbico sem pescoço. Dois olhos quadrados vazados (recortes escuros). Dois braços (blocos laterais curtos), dois pés (blocos na base).

**Cor:** **100% laranja `#E8602A`** (mesma cor do asterisco Claude). Faces com sombreamento 3D: topo claro `~#F07040`, frontal média, laterais escuras `~#B34818`. Luz de cima-esquerda. **Sem outras cores.** A cor laranja idêntica ao asterisco É a referência ao Claude (sem texto).

**Conexão Instagram (o detalhe que brilha):** mascote ligado ao logo Instagram via **cabo USB/Lightning 3D físico**, com curva natural de gravidade. Leitura E→D: mascote (Claude) → cabo → asterisco → cabo → logo IG. Metáfora literal de "Claude Code alimenta meu Instagram".

**Como aparece:** **capa** (pequeno, topo, na fileira mascote-cabo-asterisco-cabo-IG) e **CTA** (grande, flutuando sobre o Rio, conectado ao logo IG 3D no ombro do criador sentado de costas). **NÃO aparece nos slides de conteúdo** do Noe.

**Prompt de geração (do RECEITA):**
```
A cute 3D voxel robot character, Minecraft-style, made entirely of orange
(#E8602A) cubes, square blocky head with two dark square eye holes, small arm
extensions on each side, two feet blocks at base, 3D isometric render, soft
lighting from top-left, dark faces on sides, bright face on top, isolated on
transparent background, game asset style, no background, high quality render
```
Cabo adicionado em composição separada ("USB-C cable 3D render isolated transparent PNG"). Render 1024px+, escalar depois.

### Mascotes TYLER (variam por post — pixel-art 8/16-bit):
- DV9 (Claude Code super-hero): personagem **capa vermelha + ícone "C" no peito**, 8-bit, ~25% da largura, na capa.
- DWHr4SzkecE: cabeça quadrada terracota, olhos quadrados pretos, sorriso, hoodie laranja. **Em TODOS os slides de conteúdo**, canto superior direito sobreposto ao título. Capa mostra estado "antes→depois" (primitivo → completo).
- DWSJiOqkcbi: pixel musculoso fazendo bíceps, cabeça quadrada laranja. Capa (grande) + CTA (**blurred** pra não competir com CTA).
- DV1: polvo/octopus laranja estilo Funko (no course card thumbnail).
- DW1: bloco laranja, óculos redondos, chapéu cowboy bege, segurando celular.

**Regra geral mascote:** sempre **gerado por IA** (Midjourney/DALL-E pixel-art) OU Aseprite/Piskel. Cor = cor accent (unidade visual). Posição consistente = branding. **Quando usar:** capa sempre; conteúdo (opcional, alguns em todos os slides, outros não pra não saturar — DW1 só em 2/6); CTA frequente (às vezes blurred). **Quando NÃO:** Tenfold não usa mascote (escola "editorial premium").

---

## 7. LOGO DO CLAUDE

**Dois logos distintos — NÃO confundir:**

1. **Sunburst/asterisco coral** (8 raios arredondados, "sparkle"): é o **logo oficial do app Claude (Anthropic)**. Cor laranja/coral sólida (`#E8602A`/`#E8673A`). **É o usado nos carrosséis** como âncora de topo (Noe slides 2-6; DWSJiOqkcbi topo da capa).
   - **Posição:** topo, **centralizado horizontalmente**, `~5.5–8%` do topo.
   - **Tamanho:** `~120–130px` (`~11–12%` da largura).
   - `filter: drop-shadow(0 6px 20px rgba(232,96,42,0.45))`.
   - Substitui o handle no topo = "logo-first branding": reconhece o tema antes de ler.

2. **Logo Claude Code (CLI)** = blocos ASCII (██), NÃO o sunburst. **Nenhum carrossel usa o ASCII como logo** — todos usam o asterisco do app, mesmo falando de Claude Code. (Nota interna: ao clonar conteúdo de Claude Code-CLI, o ASCII seria o tecnicamente correto, mas o mercado padronizou o asterisco coral por reconhecimento.)

3. **App icon Claude** (container branco arredondado `border-radius ~22%` + asterisco coral dentro + "Claude" embaixo em preto): usado na composição de capa do Noe (estilo iOS/Android store).

Aparece também **dentro de screenshots reais** (terminal Claude Code mostra o asterisco; VSCode toolbar mostra o ícone laranja).

---

## 8. ANOTAÇÕES (setas / círculos / labels handwritten)

### Taxonomia de setas (do RECEITA Tyler DV1, a mais completa):
| Tipo | Cor | Estilo | Uso |
|---|---|---|---|
| **Seta curva hand-drawn** | accent | SVG path bezier, stroke 3px, linecap round, fill none | Transição/swipe (canto inf. dir.); label de anotação |
| **Seta sólida vermelha** | `#E8453C` | Filled, triangular, grossa (NÃO hand-drawn) | "Instrução hard" DENTRO de screenshot — "OLHA AQUI" |
| **Seta handwritten para baixo** | accent | Stroke 4px, maior | CTA final, aponta pros comentários |

**Regra:** **seta vermelha sólida = instrução dura em screenshot; seta accent hand-drawn = transição/anotação suave.**

### Círculos handwritten (Noe DY79):
- Traço irregular simulando caneta (brush tool, ~6px). **Vermelho `#E53935` = "antes" (ruim); verde `#43A047` = "depois" (bom).** Before/after instantâneo em números de seguidores.

### Bordas de destaque em screenshots:
- **Borda vermelha `#E03030`** (3px solid, border-radius 8px) ao redor do campo/item exato a notar. Cor sólida uniforme adicionada em pós (Figma/Canva), não nativa da UI. Noe usa MUITO (steps 1-5).

### Labels handwritten (Caveat):
- "Send Claude this message", "download this", "this is what you want", "it looks like this", "my free course". Acompanham seta curva apontando ao alvo.

### Underline/sublinhado da headline:
- Pincelada accent abaixo da palavra-chave. SVG path curvo (`stroke 4px`) OU `background-color` pill rotacionado `-1.5°`. Ponto de "landing" do olhar.

**Onde posicionar (regra pra não sobrepor):**
- Setas de swipe SEMPRE no **canto inferior direito** (~75% X, ~80% Y), fora do bloco de texto.
- Anotações em screenshot ficam na **borda externa** do screenshot apontando pra dentro (overflow visible no wrapper).
- Labels handwritten **acima ou ao lado** do alvo, nunca sobre texto legível.

---

## 9. MOTIFS PERSISTENTES (o que se repete em TODO slide)

### Handle / footer (o mais consistente — pixel-perfect idêntico em todos os slides):
- **Tyler (7 posts):** esquerda = ícone Instagram (outline branco ~16-20px) + `@itstylergermain` (Inter regular ~14px). Direita = ícone bookmark + **"save for later"** (Caveat/cursiva). Footer height ~54-80px, padding-x igual ao corpo. Às vezes linha `1px #333` acima.
- **Noe (2):** `@noevarner.ai` + ícone IG, **centralizado** ou esquerda, rodapé. ~3% da altura.
- **Tenfold (1):** header bar (topo!) com `@TENFOLDMARC` + `0X / 09` contador. Footer = avatar circular + handle + **"SWIPE →"** (vira "END →" no último).

> **Default Tyler (dominante):** footer split — handle IG (esq) + "save for later" handwritten (dir). "save for later" é CTA passivo de bookmark repetido = mais saves = algoritmo.

### Numeração:
- **Watermark ghost:** "Prompt #1" em serif display gigante, `opacity 0.04`, atrás do conteúdo (Tyler DV1). Numeração sem poluição.
- **"Play #N" / "STEP N"** (Noe, Tenfold): label pequeno acima da headline. Tenfold: `STEP 0X · NOME` + `0X / 09`.
- **Vários NÃO numeram** (DYpVlG argumenta: numerar lembra que é longo → pior retenção em 9+ slides).

### Swipe / progress:
- Seta curva (accent ou branca) canto inferior direito nos slides internos. Presente em ~todos exceto o último.
- "(save this for later...)" como subtítulo de capa (DWSJiOqkcbi) = âncora de retenção logo no slide 1.

### Background motif (textura que se repete):
- **Ondas/topografia** (linhas de contorno orgânicas) — Noe slides 2-5. Cor `~#1a0010`/`#200015` sobre o fundo, opacity ~0.35. SVG bezier ou Haikei.app.
- **Noise/grain** — Tyler (feTurbulence SVG opacity 8-12% OU PNG). Tenfold: cor sólida sem textura.
- **Asterisco/snowflake** no topo da capa (Noe, DWSJiOqkcbi, Tenfold) — âncora antes da headline.
- **Corner brackets** (Tenfold): 4 cantos com linhas accent `22px, border 2px` — moldura editorial.

---

## 10. OS 3 TEMPLATES (DYpVlG provou: é só 3 templates repetidos)

DYpVlG = 11 slides = **Template Capa (1) + Template Item (9, idênticos, 94% do carrossel) + Template CTA (1)**. Esta é a arquitetura universal.

### TEMPLATE A — CAPA
- **Fundo:** foto real do criador darkened (`rgba(0,0,0,0.5–0.7)` overlay/gradiente) OU composição com asset. (Tyler conteúdo-puro às vezes usa fundo escuro liso.)
- **Topo:** asterisco Claude OU mascote-row OU vazio.
- **Headline:** a mais agressiva, ALL CAPS ou black/900, **centralizada** (capa é o único slide centralizado em várias escolas). 2-5 linhas. 1 palavra accent (cor sólida, serif itálica, ou highlight block).
- **Subtítulo:** "Here's the playbook." / "Here's how to build one..." (casual).
- **Prova opcional:** screenshots de before/after, mascote.
- **Swipe arrow** + footer.
- **Função:** parar o scroll em 0.3s. Promessa quantificada ("90K in 4 Months").

### TEMPLATE B — CONTEÚDO (o core, repetido N vezes)
- **Fundo:** escuro liso/texturizado (`#0d0d0d`–`#1a1a1a`) OU foto blur reaproveitada (DYpVlG).
- **Âncora topo:** asterisco / watermark "#N" / mascote no canto.
- **Headline:** label pequeno (STEP/Play/Prompt #N) + headline gigante **left-aligned**, 1 palavra accent.
- **Sub + linha de impacto** (itálico accent).
- **Elemento herói** (45-88%): screenshot real OU code box OU card OU folder emoji — UM por slide.
- **Anotações** opcionais (seta vermelha em screenshot, label handwritten).
- **Mascote** opcional (canto dir.). **Footer** fixo.
- **Regra:** só MUDA o herói + o texto. Estrutura, fonte, cor, footer, mascote-posição = constantes. Isso é o que torna o sistema clonável e coeso.

### TEMPLATE C — CTA
- **Fundo:** volta à foto da capa (bookend/loop narrativo) OU escuro com mascote.
- **Headline:** **a MAIOR do carrossel** ("Want the Full System?", "Want These Exact Prompts?"). Accent retorna (se foi reservado).
- **Visual:** lead magnet com **blur estratégico** (doc/playbook borrado = curiosidade + gating) OU course card OU mascote+IG.
- **CTA texto:** `Comment "[PALAVRA]" + I'll send it over`. PALAVRA entre aspas em accent bold. Ícone balão 💬. Às vezes "(not free)"/"(this is not free)" pra qualificar lead.
- **Seta handwritten** apontando pra baixo (= comentários). Footer.
- **Função:** comentário = engajamento = alcance algorítmico + lead no DM.

---

## 11. O QUE É GERADO POR IA vs CAPTURADO vs CSS PURO

| Elemento | Origem | Notas |
|---|---|---|
| **Mascote (pixel-art / voxel 3D)** | **GERADO IA** (Midjourney/DALL-E) ou Aseprite/Piskel | Sempre na cor accent; PNG transparente |
| **Cabo USB 3D** (Noe) | **GERADO IA** / render Blender | Composição separada |
| **Logo Instagram 3D glossy** (Noe) | **GERADO IA** | Não é o flat oficial |
| **Foto-fundo** (praia, Rio, gym, setup, rua) | **CAPTURADO** (foto real do criador / stock) | Overlay escuro CSS |
| **Foto do criador** (rosto, de costas) | **CAPTURADO** | Tratamento desaturação/vinheta |
| **Dashboard fake** (Tenfold) | **GERADO via Claude Code** (shadcn/ui) → screenshot sem chrome | NÃO difusão de imagem; é app real renderizado |
| **Infográfico file-structure** (Tyler DV1) | **GERADO** (Canva/Figma/IA, estilo papel) | Fundo creme + estrelinhas |
| **Course card / thumbnail** | **GERADO** (mascote IA + texto Canva) | Imagem de marketing pré-existente |
| **Cut-out Hormozi + capas de livros** (Noe capa) | **CAPTURADO + background removal** + assets reais | Remontado em Figma — NÃO IA |
| **Screenshots de UI** (Claude.ai, terminal, VSCode, Supabase, Insights) | **CAPTURADO real** (DevTools, Retina 2x, sem chrome) | Credibilidade = proof of work. Nunca mockup |
| **App próprio** (Shipyard Tyler DV9) | **CAPTURADO** do Next.js rodando local | |
| **Mockups de smartphone/celular** | **Template Figma/Canva** + screenshot real inserido | Device mockup |
| **Code box / prompt block** | **CSS PURO** (`<div>` + border accent + mono + spans) | NÃO screenshot |
| **Highlight block na headline** | **CSS PURO** (`background-color` no span) | |
| **Watermark ghost número** | **CSS PURO** (opacity 0.04) | |
| **Setas hand-drawn / sublinhados** | **SVG** (path bezier, stroke round) | Ou brush Procreate→PNG |
| **Setas vermelhas sólidas** | **Editor de imagem** (Figma/Canva sobre screenshot) | |
| **Bordas vermelhas em screenshot** | **CSS/Figma overlay** | Não nativo da UI |
| **Círculos vermelho/verde** (Noe) | **Desenhados** (brush pen, traço irregular) | |
| **Folder emoji macOS** | **PNG system emoji** (+ asterisco composto em Figma) | |
| **Ondas / topografia de fundo** | **SVG/CSS** (bezier) ou Haikei.app / heropatterns | |
| **Noise / grain** | **CSS** (feTurbulence SVG) ou PNG overlay opacity 8-12% | |
| **Corner brackets** (Tenfold) | **CSS PURO** (pseudo-elementos/divs) | |
| **Dashed circle decorativo** (Tyler DV1) | **CSS PURO** (`border: dashed`) | |
| **Speech bubble** (Tyler DWHr4) | **CSS PURO** (div border-radius + rgba) | |
| **Sparklines/gráficos** | **SVG/Recharts** ou parte do screenshot | |
| **Toda tipografia + cores + footer** | **CSS PURO** (Google Fonts + variáveis) | |
| **Logo Claude asterisco** | **Asset oficial Anthropic** (SVG) ou recriado | 8 raios arredondados |

**Síntese:** o **conteúdo de prova** (UI, dashboards, métricas) é **capturado real**; o **conteúdo de marca** (mascote, fundos aspiracionais, logos 3D) é **gerado por IA**; toda a **estrutura** (tipografia, code box, setas, bordas, footer, texturas) é **CSS/SVG puro**. O único caso de "dashboard que parece screenshot mas é construído" é o Tenfold (Claude Code + shadcn → screenshot limpo).

---

## APÊNDICE — DEFAULTS PRONTOS PRA CLONAR (perfil Tyler Germain, o dominante)

```css
:root {
  --bg: #0d0d0d;              /* escuro liso (conteúdo) */
  --bg-photo-overlay: rgba(0,0,0,0.60); /* capa/CTA */
  --text: #FFFFFF;
  --text-gray: #CCCCCC;
  --accent: #C4714A;          /* terracota Tyler */
  --red-highlight: #E8453C;   /* "olha aqui" em screenshot */
  --green: #43A047;           /* crescimento */
  --code-bg: #111111;
  --font-display: 'Anton', 'Bebas Neue', sans-serif;  /* OU Playfair p/ serif */
  --font-serif: 'Playfair Display', serif;
  --font-sans: 'Inter', sans-serif;
  --font-hand: 'Caveat', cursive;
  --font-mono: 'JetBrains Mono', monospace;
  --pad-x: 48px;              /* eixo de coluna sagrado */
}
.slide { width:1080px; height:1350px; position:relative; overflow:hidden;
         background:var(--bg); padding:60px var(--pad-x) 48px; box-sizing:border-box; }
.screenshot { width:calc(100% - 0px); border-radius:14px;
              box-shadow:0 20px 60px rgba(0,0,0,0.7); }
.code-box { border:2px solid var(--accent); border-radius:12px; background:var(--code-bg);
            padding:28px 32px; box-shadow:none; font-family:var(--font-mono); }
.code-box .kw { color:var(--accent); }
```

**Checklist de fidelidade:**
- [ ] Toda headline tem EXATAMENTE 1 palavra/grupo accent.
- [ ] padding-x igual (48px) em headline + herói + code box + footer.
- [ ] Elemento herói ocupa 35-48% da altura (não deixa buraco).
- [ ] Screenshots = capturas REAIS sem chrome de browser.
- [ ] Code box = CSS flat com borda accent, keywords em accent.
- [ ] Footer idêntico em 100% dos slides (handle IG + "save for later").
- [ ] CTA = headline maior do carrossel + `Comment "X"` + seta pra baixo.
- [ ] Accent só na capa/CTA SE optar pelo arco emocional.
- [ ] Mascote (se usar) na cor accent, PNG transparente, posição consistente.

---

*Destilado de 10 RECEITAs. Valores são proporções estimadas a partir de canvas 1080×1350px. Onde as contas divergem, o RANGE foi dado e o dominante (Tyler Germain) marcado como default.*
