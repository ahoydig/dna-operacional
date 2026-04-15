---
description: Gera carrosséis profissionais para Instagram via HTML-to-Image (Playwright). Coleta moodboard visual via agent-browser antes da direção visual. Suporta formatos 3:4, 4:5 e 1:1. Use quando digitar "/carrossel-instagram", "criar carrossel", "gerar slides instagram", "post instagram", "carrossel viral", "remodelar post".
argument-hint: "[tópico|URL|path-de-briefing?]"
---

Usuário invocou `/carrossel-instagram` com argumento: `$ARGUMENTS`

# /carrossel-instagram — Pipeline de 5 Gates

> Segue a voz do projeto (via `/humanizer` ao final). Handle do projeto vem de `CLAUDE.md` do user em `## Handle: @<x>`. Sem handle definido → perguntar uma vez e gravar.

**Objetivo:** Gerar carrossel pronto pra postar (PNG por slide + caption + hashtags) via HTML renderizado como imagem.

**Escopo:** Briefing → moodboard → copy → direção visual → geração final.
**Fora do escopo:** Roteirizar vídeo (`/roteiro-viral`), analisar referência em vídeo (`/analisar-video`).

---

## Passo 0: Resolver Handle

Ler `CLAUDE.md` do projeto atual: `## Handle: @<x>`. Fixar em `${USER_HANDLE}` pra toda a sessão.

Sem handle: perguntar via `AskUserQuestion` — "Qual handle do Instagram vai assinar este carrossel?" — e sugerir gravar em `CLAUDE.md` depois.

---

## Pipeline: 5 Gates

```
BRIEFING → MOODBOARD VISUAL → CONTEÚDO TEXTUAL → DIREÇÃO VISUAL → GERAÇÃO FINAL
```

Cada gate exige **aprovação explícita do user** antes de avançar. Nunca pular.

---

## Gate 1: Briefing & Pesquisa

### Inputs aceitos

| Input | Ação |
|-------|------|
| URL de notícia | Abrir via Playwright, ler, extrair pontos-chave |
| Post/Reel de Instagram | Abrir, analisar design/conteúdo, remodelar com identidade do user |
| Tweet/Thread | Capturar e transformar em carrossel |
| Repo GitHub / doc | Analisar e transformar em conteúdo educativo |
| Link YouTube | Capturar thumbnail + título |
| Ideia solta / tema | Pesquisar, buscar referências, propor ângulos |

### Coleta obrigatória

Não avança sem: **Objetivo**, **Template** (ler `references/carrossel-instagram/templates.md`), **Formato** (3:4 / 4:5 / 1:1), **Handle** (já resolvido no Passo 0).

### Defaults (nunca perguntar)

- **Formato padrão:** 3:4 (1080x1440) quando não especificado
- **Screenshots:** SEMPRE capturar via Playwright direto do app/site real. Nunca perguntar se o user quer fornecer — já abrir e capturar.

### Regras de conteúdo

- Zero jargão que o público não entende. Se precisa explicar o que é, não serve pro slide.
- Tom equilibrado ao comparar ferramentas. Nunca massacrar um produto pra vender outro.
- Pessoas reais com nome completo. Capturar perfil: Instagram > X > LinkedIn > GitHub.

### Gate 1: Apresentar resumo do briefing. Aguardar aprovação.

---

## Gate 1.5: Moodboard Visual

Ler `references/carrossel-instagram/visual-research.md`.

Após briefing aprovado, **SEMPRE** coletar moodboard de referências visuais externas antes de avançar pra copy. Esta fase ancora o Gate 3 em evidências reais.

### Fluxo resumido

1. **Engine:**
   - **Default:** `agent-browser` (sessão persistente, menos tokens, batch nativo)
   - **Fallback:** Playwright MCP
2. **Capturar screenshot full-page** de pelo menos **2 fontes** (Pinterest + Dribbble default)
3. **Salvar** em `./moodboard/{fonte}-full.png`
4. **Analisar** padrões visuais das grades capturadas
5. **Escrever** `./moodboard/moodboard.md` com destaques + direção sugerida pro Gate 3
6. **Apresentar** moodboard ao user

### Regras

- **Nunca pular** — sem moodboard, Gate 3 vira chute
- **Nunca usar 1 fonte só** — mínimo 2 (Pinterest + Dribbble)
- **1 screenshot full-page da grade** > 10 screenshots individuais

### Gate 1.5: User aprova moodboard e direção preliminar.

---

## Gate 2: Conteúdo Textual

Gerar para cada slide: título, corpo, mapa de screenshots, caption e 5 hashtags.

### Regra obrigatória: todo slide tem visual

**TODOS os slides devem ter pelo menos um elemento visual** (screenshot, imagem, logo, gráfico). Slides só-texto são proibidos. Sem screenshot natural: usar manchete capturada, gráfico de dados, logo com tratamento, ou outro visual relevante.

### Regras de copy

- **Aplicar `/humanizer`** em toda copy no final. Voz dinâmica do projeto (`reference/voz-${USER_HANDLE}.md`).
- **Cenários concretos > features.** Mostrar o que o leitor faria, não o que a ferramenta faz.
- **Tom: amigo que descobriu algo bom.** Não guru, não professor.
- **Português conversacional brasileiro real.** Frases completas. Nunca encurtar pra caber no slide.
- **Arco narrativo coeso.** Cada slide tem função na história.
- **Body text:** quebra de linha entre cada sentença.

Apresentar TUDO de uma vez pro user ver o fluxo narrativo completo.

### Gate 2: User aprova ou ajusta textos.

---

## Gate 3: Direção Visual

Ler `references/carrossel-instagram/palettes.md` e `references/carrossel-instagram/headline-effects.md`.

Propor: 2-3 paletas, efeito tipográfico, mapa de layouts, preview do slide 1.

**Efeito tipográfico aplica em TODAS as headlines**, não só na capa.

### Gate 3: User aprova paleta, efeito e estilo.

---

## Gate 4: Geração Final

1. Capturar screenshots (ler `references/carrossel-instagram/screenshot-guide.md`)
2. Gerar HTML de cada slide
3. Renderizar como PNG via Playwright
4. Apresentar ao user
5. Após aprovação, criar `roteiro.md` com textos, caption, hashtags e caminhos dos PNGs

### Gate 4: User aprova ou pede ajuste em slides específicos.

---

## Regra #1: Referências visuais SEMPRE reais

**SEMPRE buscar referências visuais reais ANTES de criar qualquer coisa.** Ordem de prioridade:

1. Abrir o app/site real via Playwright e capturar screenshot direto
2. Google Imagens — buscar "[nome] logo/screenshot/icon" via Playwright, navegar até a fonte e baixar com `curl`
3. Google Play Store / App Store — capturar o ícone oficial
4. Repositórios de ícones — simpleicons.org, brandlogos.net, wikimedia commons
5. **ÚLTIMO RECURSO:** criar mockup em HTML

**NUNCA:**
- SVGs genéricos inline (círculos, estrelas)
- Favicons (16-32px, ficam pixelados)
- Ícones inventados que não se parecem com a marca real
- Emojis como substituto de ícones reais

---

## Regra #2: Layout flexbox centralizado (NUNCA violar)

O conteúdo dos slides DEVE usar flexbox. NUNCA `position: absolute` para headline, body text, screenshots ou visuais.

**Position absolute permitido APENAS para:** Crankdat comments, handle, background blur, badges decorativos.

### Estrutura obrigatória do body

```css
body {
  width: 1080px;    /* ou 1350, 1080 conforme formato */
  height: 1440px;   /* ou 1350, 1080 conforme formato */
  padding: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 70px;         /* 100px na capa, 70px nos slides de conteúdo */
  position: relative; /* pra elementos absolute */
  overflow: hidden;
}
```

Blocos principais (headline-group, body-text, screenshot) ficam **no fluxo do flex**. Garante centralização automática.

---

## Regra #3: Alinhamento

- **Headlines:** SEMPRE `text-align: center`
- **Cards, logos, screenshots:** SEMPRE `justify-content: center`
- **Handle:** SEMPRE centralizado (`position: absolute; bottom: 50px; left: 0; right: 0; text-align: center`)
- **Subtítulo na capa:** centralizado
- **Body text em slides de conteúdo:** `text-align: left` (exceto capa e CTA = centralizado)

---

## Design dos slides

### Background

NUNCA gradiente liso sozinho. Usar gradiente + textura/glows + logo real com blur.

Logo como background: buscar LOGO REAL (Regra #1), aplicar `opacity: 0.08-0.12; filter: blur(3-5px);`, tamanho 900-1100px, centralizada, rotação leve (-5° a -10°).

**Para carrosséis sobre Claude Code / Anthropic:** usar ASCII block art "CLAUDE CODE" como background:
```css
.bg-logo {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -48%) rotate(-5deg);
  font-family: 'Courier New', monospace;
  font-size: 34px; line-height: 1.12; white-space: pre; letter-spacing: -1px;
  background: linear-gradient(180deg, #ff9966 0%, #ff5e62 50%, #ffa34e 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  opacity: 0.14; filter: blur(1.5px); z-index: 0; pointer-events: none;
}
```
Gerar o ASCII via `npx oh-my-logo "CLAUDE\nCODE" sunset --filled --block-font block --letter-spacing 0`.

**NUNCA usar o sunburst SVG como logo do Claude Code** — sunburst é da marca Claude (produto), não do Claude Code (CLI).

### Headlines

Fonte Nofex com efeito tipográfico aprovado no Gate 3. Tamanho 70-96px (capa e CTA até 120px).

**NUNCA deixar palavras órfãs** (artigos como "DO", "DA", "O", "A" sozinhos em uma linha). Verificar SEMPRE no PNG renderizado.

Como evitar:
- `&nbsp;` entre palavra curta e a seguinte: `DO&nbsp;OPENCLAW`
- Ajustar `font-size` até o texto quebrar sem órfãs
- `<br>` manual pra forçar quebras seguras
- **Nofex clipa acentos** — precisa `padding-top` e `overflow: visible` no container da headline

**Regra de conversão monetária:** Sempre em BRL (R$). Público brasileiro. $20 → ~R$120. Nunca dólar no texto do slide.

### Crankdat

Comentários com personalidade espalhados pelo slide:
- **30-36px** (slides normais), **48px+** (CTA)
- **Sem parênteses.** "de graça", não "(de graça)"
- **Posições criativas:** rotações -3° a +8°, variar entre slides
- **1-3 por slide** — variar quantidade entre slides consecutivos
- Distribuir pelas bordas e diagonais — não agrupar tudo num canto
- Cor: accent com opacidade 0.6 ou branco com opacidade 0.5

### Screenshots

- `border-radius: 16px`, box-shadow forte, GRANDES (30-35% da altura do slide)
- Centralizados no flex
- Crescem progressivamente ao longo do carrossel (curva texto→visual)
- 1 screenshot grande > grid de vários pequenos
- Mostrar RESULTADO REAL da skill/ferramenta, não mockup de terminal
- Se precisar login (Meta Ads, etc): pedir pro user logar no Playwright
- Camuflar dados sensíveis via JavaScript antes de capturar (nomes de clientes, contas)
- Vídeos fornecidos pelo user podem substituir screenshots estáticos — compor via ffmpeg

#### PROIBIDO: object-fit contain com background

**NUNCA `object-fit: contain` com `background`** — cria bordas escuras enormes. Erro #1 mais grave.

**CSS correto:**
```css
/* Screenshot único — tamanho natural, preenche largura */
.screenshot-frame img { width: 100%; display: block; }

/* Dois lado a lado — mesma altura */
.screenshots-row { display: flex; gap: 16px; width: 100%; max-width: 920px; align-items: stretch; }
.screenshots-row .screenshot-frame { flex: 1; display: flex; }
.screenshots-row .screenshot-frame img { object-fit: cover; object-position: top left; }

/* Dois lado a lado — alturas diferentes */
.screenshots-row-natural { display: flex; gap: 16px; width: 100%; max-width: 920px; align-items: flex-start; }
.screenshots-row-natural .screenshot-frame:first-child { flex: 2; }
.screenshots-row-natural .screenshot-frame:last-child { flex: 3; }
```

#### Screenshots em português

**TODOS os screenshots de fontes em inglês DEVEM ser traduzidos pra PT-BR antes de capturar.**

Método para tweets (X/Twitter):
```javascript
// Esconder sidebar e bottom bar
await page.evaluate(() => {
  ['sidebarColumn', 'BottomBar'].forEach(id => {
    const el = document.querySelector(`[data-testid="${id}"]`);
    if (el) el.style.display = 'none';
  });
  const nav = document.querySelector('header[role="banner"]');
  if (nav) nav.style.display = 'none';
});
// Traduzir texto do tweet via DOM
await page.evaluate(() => {
  const t = document.querySelector('[data-testid="tweetText"]');
  if (t) t.innerHTML = 'TEXTO TRADUZIDO';
});
// Capturar o article isolado
await (await page.locator('article').first()).screenshot({ path: 'screenshots/tweet-pt.png' });
```

**Google Translate NÃO funciona com X.com** — manipular DOM diretamente.

### Tabs coloridos (skill.md)

**NÃO usar tabs coloridos** — parecem artificiais. Substituir por mascot, ícone, ou outro visual orgânico fornecido pelo user.

### Fontes

Ler `references/carrossel-instagram/fonts-config.md`. Resumo: Headlines = Nofex (fallback Bebas Neue), Accent = Crankdat (fallback Space Grotesk), Body = Inter.

Copiar fontes locais pro diretório de trabalho antes de gerar (ver fonts-config pra detecção de OS e paths).

---

## Renderização

1. Salvar HTML no diretório de trabalho
2. Servir via `python3 -m http.server [porta]` (verificar porta livre)
3. Abrir via Playwright com viewport do formato (3:4 = 1080x1440)
4. Aguardar 3 segundos pras fontes carregarem
5. Capturar screenshot como PNG
6. **Para overlays transparentes:** `browser_run_code` com `page.screenshot({ path: 'file.png', omitBackground: true, type: 'png' })`
7. **FECHAR O BROWSER** após cada slide

### Composição de vídeo em slides

Quando um slide precisa de vídeo rodando (mascot, demo):

1. HTML do slide com placeholder vazio onde o vídeo vai
2. Playwright `evaluate()` pra medir `getBoundingClientRect()` do placeholder
3. Renderizar HTML como PNG (background estático)
4. Compor via ffmpeg: `background PNG + vídeo escalado + overlay`

Regras:
- Vídeo DEVE preencher TODA a largura da área de sombra. Usar `scale=LARGURA:-1,crop=LARGURA:ALTURA`
- `shortest=1` no overlay filter pra manter animação
- Remover fundo preto: `colorkey=0x000000:0.25:0.15`
- Para mascot: NÃO cropar laterais nem topo — só cropar espaço vazio embaixo dos pés

Exemplo ffmpeg:
```bash
ffmpeg -y -loop 1 -i bg.png -i video.mp4 \
  -filter_complex "[1:v]scale=810:-1,crop=810:550:0:(ih-550)/2[vid];[0:v][vid]overlay=135:615:shortest=1" \
  -t 10 -an -c:v libx264 -pix_fmt yuv420p -r 24 -crf 18 output.mp4
```

---

## Auto-review obrigatório (antes de mostrar ao user)

**Renderizar CADA slide como PNG e verificar visualmente ANTES de mostrar.** Usar `Read` pra visualizar cada PNG.

1. **Layout flex?** Elementos principais no fluxo do flex, NÃO position absolute?
2. **Centralizado?** Headlines, screenshots, cards e handle centralizados?
3. **Logos reais?** De fontes reais, não SVGs genéricos?
4. **Background rico?** Gradiente + textura + logo blur (ASCII block art pra Claude Code)?
5. **Crankdat OK?** Sem parênteses, 30px+, rotacionado?
6. **Português natural?** Ler em voz alta. Acentos corretos (ção, é, ê, á, ú, ô, õ).
7. **Densidade?** ~65% preenchido em slides de conteúdo. CTA = mínimo.
8. **Screenshots reais?** Resultado REAL, não mockup de terminal?
9. **Vídeos encaixados?** Largura preenche 100% da área de sombra?
10. **Ajuste pontual?** Se o user pediu mudança específica, NÃO alterar layout inteiro — só o que foi pedido.
11. **Todo slide com visual?** Cada slide tem ≥1 elemento visual?
12. **SEM bordas escuras?** Nenhum screenshot com `object-fit: contain` + `background`?
13. **Screenshots em PT-BR?** Tudo em inglês traduzido via DOM antes de capturar?
14. **Sem palavras órfãs?** Nenhuma palavra curta sozinha numa linha?
15. **Valores em reais?** Tudo em R$, nenhum dólar no texto?
16. **Screenshots legíveis?** Texto dentro dos screenshots legível no tamanho final?
17. **Alturas alinhadas?** Em layouts lado a lado, alturas compatíveis?
18. **Moodboard considerado?** Paleta/efeito/layout derivados do moodboard do Gate 1.5?

Se qualquer resposta for "não", corrigir ANTES de apresentar.

---

## Reference Files

| Arquivo | Quando ler |
|---------|-----------|
| `references/carrossel-instagram/templates.md` | Gate 1 — templates |
| `references/carrossel-instagram/visual-research.md` | Gate 1.5 — moodboard |
| `references/carrossel-instagram/palettes.md` | Gate 3 — paletas |
| `references/carrossel-instagram/headline-effects.md` | Gate 3 — efeitos |
| `references/carrossel-instagram/screenshot-guide.md` | Gate 4 — captura |
| `references/carrossel-instagram/fonts-config.md` | Antes da geração |

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Fonte não carrega | Copiar .ttf pro diretório `./fonts/` (ver fonts-config) |
| Screenshot branco/transparente errado | Usar `omitBackground: true` no `browser_run_code` |
| Servidor HTTP ocupado | Tentar outra porta |
| Vídeo composto fica branco | Verificar que bg.png tem gradiente (não transparente) |
| Elementos grudados no topo | Verificar `justify-content: center` no body |
| **Bordas escuras ao redor do screenshot** | Remover `object-fit: contain` e `background`. Usar `width: 100%` sem object-fit, ou `object-fit: cover` pra lado a lado |
| Palavra órfã na headline | `&nbsp;` entre palavra curta e a seguinte, ou ajustar font-size |
| Screenshot de tweet em inglês | Traduzir via `page.evaluate()` no `[data-testid="tweetText"]` antes de capturar |
| Google Translate quebra X.com | Não usar. Manipular DOM diretamente |
| Screenshots lado a lado com alturas diferentes | `align-items: stretch` + `object-fit: cover`, ou `flex-start` com flex ratios |
| Texto do slide em inglês | Converter TUDO pra PT-BR: "subscription" → "assinatura", valores em R$ |
| Nofex clipa acentos | `padding-top` no container da headline + `overflow: visible` |

---

## Regras

1. **Nunca pular gates** — cada um precisa aprovação do user
2. **Handle via `${USER_HANDLE}`** — ler de `CLAUDE.md`, nunca hardcodar
3. **Screenshots reais** via Playwright — não perguntar, já capturar
4. **Todo slide com visual** — só-texto é proibido
5. **Efeito tipográfico em TODAS as headlines**, não só na capa
6. **Humanizer no final** — voz dinâmica do projeto
7. **Auto-review antes de apresentar** — 18 checks obrigatórios
8. **Referências visuais reais** — nunca SVG genérico ou emoji
9. **PT-BR em tudo** — screenshots traduzidos, valores em R$
10. **Flexbox, não position absolute** — exceto Crankdat, handle, background

