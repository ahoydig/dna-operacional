---
description: Gera apresentação Awwwards-ready em HTML + CSS + JS Vanilla + GSAP (NÃO pptx). Engine de 18 cenas — hero neon, whoWeAre manifesto, pipeline scroll trap, hazard glitch RGB, investment, protagonistOffer. Pré-preenche com voz e público do projeto DNA. Invoca ui-ux-pro-max + taste-skill pra direção visual. Use quando digitar "/apresentacao", "criar deck", "apresentação pra <cliente>", "slide deck <tema>", "pitch deck", "keynote".
argument-hint: "[tema ou cliente]"
---

Usuário invocou `/apresentacao $ARGUMENTS`.

**CRÍTICO:** essa skill NÃO gera `.pptx`. Gera **site cinematográfico em HTML + CSS + JS Vanilla + GSAP** — 4 arquivos auto-contidos rodáveis em qualquer navegador (e em Netlify). Zero build step.

## Passo 1 — Ler contexto DNA do projeto

Ler (silent fallback se faltar):

| Arquivo | Uso |
|---------|-----|
| `CLAUDE.md` | Nome empresa, handle, voz adjetivos, oferta principal |
| `reference/publico-alvo.md` | Briefing completo (se existir) |
| `reference/voz-*.md` | Tom da copy dos slides |

Se CLAUDE.md ausente:
> "⚠ Projeto não configurado. Rodando modo briefing direto — faço a direção visual do zero."

## Passo 2 — Ler references do engine

**Obrigatório** antes de montar config:

```
${CLAUDE_PLUGIN_ROOT}/references/apresentacao/design-system.md   ← tokens, tipografia, efeitos
${CLAUDE_PLUGIN_ROOT}/references/apresentacao/cenas-catalog.md   ← 18 cenas com templates
${CLAUDE_PLUGIN_ROOT}/references/apresentacao/gsap-patterns.md   ← 14 padrões GSAP
```

Esses 3 arquivos são a fonte de verdade do engine. Qualquer cena nova ou padrão de animação DEVE sair deles.

## Passo 3 — Briefing

Perguntar ao user (pular o que já veio em `$ARGUMENTS` ou no contexto):

1. **Tema/objetivo** — vendas? keynote? pitch investidor? workshop? kickoff cliente?
2. **Público da apresentação** em 1 frase (quem vai assistir, nível de conhecimento, ticket médio se for sales)
3. **Duração** esperada (em minutos) — calibra densidade
4. **Quantidade de slides** aproximada (6-12 é o sweet spot; se user não sabe, sugerir com base no tema)
5. **Cliente/destinatário** (se aplicável — vira hero title)
6. **Já existe material base?** (link de briefing, doc, site) — se sim, ler antes

## Passo 4 — Direção visual (ui-ux-pro-max)

Invocar **Skill tool** com `skill: "ui-ux-pro-max"` passando:

```
Contexto:
- Tema: <tema>
- Público: <público>
- Voz do projeto: <adjetivos>
- Cliente: <cliente>

Request:
- 3 paletas alinhadas (cada uma com --c-cyan, --c-purple, --c-accent, --c-success — 4 cores minimalistas)
- 3 font pairings (display + body + mono) compatíveis com Google Fonts
- 1 style dominant: brutalism | glassmorphism | editorial | cyberpunk | minimalism
```

Apresentar ao user com mockup ASCII das 3 opções, pedir pra escolher 1.

**Fallback se user não escolhe:** default é `Obsidian Quantum` (§2 de design-system.md) + Anton/Manrope/mono + cyberpunk.

## Passo 5 — Outline (taste-skill)

Invocar **Skill tool** com `skill: "taste-skill"` com parâmetros:

```
DESIGN_VARIANCE = 9     # a caixa tá sendo rompida
MOTION_INTENSITY = 7    # animações fortes mas não gratuitas
VISUAL_DENSITY = 5      # info densa onde conta, respiro no hero/outro

Request:
Dado tema "<tema>" e público "<público>", propor outline de <N> slides usando subset do catálogo (ver subsets por briefing em cenas-catalog.md §subsets):

- Sales deck → hero, cards (dor), solution, pipeline, value, hazard, investment, imageShowcase, protagonistOffer, outro
- Keynote → hero, whoWeAre, bento (stats), methodology, solution, imageShowcase, cards (diferenciais), outro
- Pitch investidor → hero, whoWeAre, cards (problem), solution, bento (market), imageShowcase, methodology, value, crewShowcase, investmentFull, protagonistOffer, outro
- Workshop → hero, whoWeAre, methodology, pipeline, solution, outro
- Kickoff cliente → hero, whoWeAre, methodology, pipeline (cronograma), value, crewShowcase, outro

Pra cada slide, incluir:
- type (string do catálogo)
- id (slug-único)
- animation: { enter, leave } (ver animation presets em cenas-catalog.md)
- content skeleton (campos do tipo de cena) com placeholders
```

## Passo 6 — Preencher content com copy real

Pra cada slide do outline, preencher o `content` aplicando voz do projeto:

- Headlines em CAPS, curtas (3-6 palavras)
- Subheadlines com 1-2 frases
- Números reais (ou placeholders claros `{{METRICA_X}}` se user não informou)
- Ícones Phosphor apropriados (tabela em cenas-catalog.md §ícones)

**Regra voz:** se `reference/voz-*.md` existir, passar cada headline pela voz. Sem hedging, sem corporativês.

## Passo 7 — Selecionar slug + criar estrutura de output

```bash
# Slug a partir do cliente/tema
slug = lowercase(cliente || tema).replace(/[^a-z0-9]+/g, '-').slice(0, 40)
date = $(date +%Y-%m-%d)
out_dir = "data/clientes/${slug}/apresentacoes/${date}"

mkdir -p "${out_dir}/assets"
```

## Passo 8 — Gerar os 4 arquivos

### 8.1 `index.html` (boilerplate)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="theme-color" content="#050505">
  <title>{{TITULO}}</title>
  <meta name="description" content="{{DESCRICAO}}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family={{FONT_DISPLAY}}&family={{FONT_BODY}}:wght@300;400;600&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/fill/style.css">
  <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/regular/style.css">

  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="noise-overlay"></div>
  <div class="cursor-dot"></div>
  <div class="cursor-ring"></div>

  <div class="ui-layer">
    <button id="fullscreen-btn" class="glass-btn" aria-label="Fullscreen">
      <i class="ph ph-arrows-out-simple"></i>
    </button>
    <div class="progress-bar"><div class="progress-fill"></div></div>
    <div id="slide-counter" class="slide-counter"></div>
  </div>

  <main id="app"></main>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/Observer.min.js"></script>
  <script type="module" src="main.js"></script>
</body>
</html>
```

### 8.2 `style.css`

Copiar tokens + keyframes + componentes UI + scene styles de `references/apresentacao/design-system.md`. Aplicar paleta escolhida no Passo 4 sobrescrevendo `:root { --c-* }`.

**Ordem do arquivo:**
1. `:root` tokens
2. Reset + base (`html, body, #app, .scene`)
3. Componentes persistentes (`noise-overlay`, `cursor-dot`, `cursor-ring`, `slide-counter`, `glass-card`, `ui-layer`)
4. Efeitos de texto (`neon-off/on`, `text-neon`, `text-outline`, `text-stroke`, `glitch-layer`)
5. Scenes (uma seção por tipo de cena USADO no outline — não copiar os 18 se só 7 são usados)
6. Keyframes (`@keyframes gridScroll`, `alarmPulse`, `titleGlitch`, `glitchCyan/Red`, `shockwave`, `marqueeScroll`, `radarSweep`)
7. Responsividade (`@media (max-width: 768px)`, `@media (prefers-reduced-motion)`)

### 8.3 `main.js`

Baseado no engine reference. Estrutura:

```js
import { config } from './config.js';

gsap.registerPlugin(ScrollTrigger, Observer);

const State = { currIndex: 0, isAnimating: false, totalScenes: 0, fromIndex: undefined };

// === Helpers (§9-12 de gsap-patterns.md) ===
const injectTheme = (theme) => { /* aplica config.theme.colors/fonts/easing em :root */ };
const scrambleText = (el, duration) => { /* glitch char-scramble */ };
const splitText = (sel, type) => { /* chars ou words */ };
const countUp = (el, duration) => { /* animated number */ };

// === Templates (um por tipo de cena usado) ===
const Templates = {
  hero: c => `...`,       // ver cenas-catalog.md §01
  whoWeAre: c => `...`,   // §02
  // ... (só os tipos presentes no outline)
};

// === Scene Animations ===
const sceneAnimations = {
  hero: { enter: (el) => neonFlickerIn(el.querySelector('.mega-title')), leave: (el) => gsap.to(el, { opacity: 0 }) },
  hazard: { enter: (el) => { const t = startMarquee(...); const g = startGlitchLoop(...); return () => { t.kill(); g(); }; } },
  pipeline: { enter: (el) => createPipelineTrap(el, el.querySelector('.pipeline-track')) },
  // ...
};

// === Transições Z-axis (§1 de gsap-patterns.md) ===
const transitionToScene = (from, to, direction) => { /* ... */ };

// === Bootstrap ===
const init = () => {
  injectTheme(config.theme);
  const app = document.getElementById('app');
  app.innerHTML = config.scenes.map(c => Templates[c.type](c)).join('');
  initCustomCursor();
  renderSlideCounter(config.scenes.length);
  config.scenes[0].classList?.add('active');
  Observer.create({ type: 'wheel,touch,pointer', onDown: () => navigate('next'), onUp: () => navigate('prev'), tolerance: 10 });
  window.addEventListener('keydown', handleKeyboard);
  // fullscreen button
  document.getElementById('fullscreen-btn').addEventListener('click', () => document.documentElement.requestFullscreen());
};

init();
```

### 8.4 `config.js`

```js
export const config = {
  meta: {
    title: "{{TITULO}}",
    description: "{{DESCRICAO}}",
    client: "{{CLIENTE}}",
    createdAt: "{{DATA}}"
  },
  theme: {
    colors: {
      bg: "#050505",
      text: "#FFFFFF",
      cyan: "{{PALETA_CYAN}}",
      purple: "{{PALETA_PURPLE}}",
      accent: "{{PALETA_ACCENT}}",
      success: "{{PALETA_SUCCESS}}"
    },
    fonts: {
      display: "'{{FONT_DISPLAY}}', sans-serif",
      body: "'{{FONT_BODY}}', sans-serif",
      mono: "ui-monospace, 'JetBrains Mono', monospace",
      googleFontsUrl: "https://fonts.googleapis.com/css2?family={{FONT_DISPLAY}}&family={{FONT_BODY}}..."
    },
    easing: {
      "out-expo": "cubic-bezier(0.16, 1, 0.3, 1)",
      "in-out": "cubic-bezier(0.65, 0, 0.35, 1)"
    }
  },
  scenes: [
    // Array com cada slide do outline preenchido
    { id: "hero", type: "hero", animation: { enter: "zoomIn", leave: "zoomOut" }, content: { title: "...", /* ... */ } },
    // ...
  ]
};
```

## Passo 9 — Assets (se user tem logos/fotos)

Se user forneceu caminhos de imagens (logos de clientes, fotos do time, screenshots):

1. Copiar pra `${out_dir}/assets/`
2. Referenciar nos templates com paths relativos (ex: `"assets/cliente-logo.png"`)

Se user não forneceu:
- Imagens viram placeholders tipo `<div class="placeholder-img">LOGO AQUI</div>`
- Footer aviso: "⚠ Substitua os placeholders em `assets/` antes de apresentar."

## Passo 10 — Preview no navegador

Tentar abrir preview local:

```bash
# Tenta 3 portas em ordem
PORT=8787
for P in 8787 8788 8789; do
  if ! lsof -i :$P > /dev/null 2>&1; then PORT=$P; break; fi
done

cd "${out_dir}"
python3 -m http.server ${PORT} > /dev/null 2>&1 &
SERVER_PID=$!
sleep 1
open "http://localhost:${PORT}"

echo "Servidor na porta ${PORT}, PID ${SERVER_PID}. Pra parar: kill ${SERVER_PID}"
```

Se `python3` não tá disponível, avisar usuário pra rodar manualmente:
> "Abre `${out_dir}/index.html` direto no navegador (ou roda `npx serve` dentro dela)."

## Passo 11 — Registrar + output final

### 11.1 Append em `data/apresentacoes.csv`

Header (se arquivo não existir):
```
id,tema,cliente,slug,out_dir,slides_count,paleta,tema_visual,created_at
```

Nova linha:
```
<id>,<tema>,<cliente>,<slug>,data/clientes/<slug>/apresentacoes/<data>/,<count>,<nome paleta>,<style>,<ISO>
```

### 11.2 Output pro usuário

```
╔══════════════════════════════════════════════════════════════════╗
║  🎬 Apresentação gerada                                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Cliente:   <cliente>                                            ║
║  Tema:      <tema>                                               ║
║  Slides:    <N> cenas                                            ║
║  Paleta:    <nome>                                               ║
║  Style:     <style>                                              ║
║                                                                  ║
║  Output:    data/clientes/<slug>/apresentacoes/<data>/           ║
║             ├── index.html                                       ║
║             ├── style.css                                        ║
║             ├── main.js                                          ║
║             ├── config.js                                        ║
║             └── assets/                                          ║
║                                                                  ║
║  Preview:   http://localhost:<porta>                             ║
║                                                                  ║
║  Navegação: wheel/touch/setas/espaço                             ║
║  Fullscreen: botão no canto superior direito                     ║
║                                                                  ║
║  Deploy:    git init && netlify deploy --prod --dir=.            ║
║             (ou drag-drop a pasta no Netlify Drop)               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Princípios do output

### O que FAZER

- **Auto-contido:** 4 arquivos, só CDN de fonts/icons/gsap, zero npm
- **Tokens-first:** toda cor/fonte vem de CSS custom property pra fácil rebrand
- **Cleanup obrigatório:** toda cena com animação contínua registra cleanup function (§13 gsap-patterns.md)
- **Reduced motion:** respeitar `prefers-reduced-motion` (desliga neon flicker + glitch)
- **Mobile OK:** viewport meta + breakpoint 768px funcional
- **Navegação acessível:** wheel + touch + arrows + espaço
- **Slide counter + progress bar:** sempre visíveis

### O que NÃO fazer

- NÃO gerar `.pptx` (não é o objetivo)
- NÃO usar React/Vue/framework (Vanilla only)
- NÃO incluir npm scripts ou build tools
- NÃO duplicar todas as 18 cenas em CSS se só 7 estão no outline
- NÃO usar imagens geradas por IA sem avisar o user
- NÃO hardcodar cores — sempre via `:root` tokens
- NÃO pular o Passo 4 (ui-ux-pro-max) — é o que garante direção visual coerente

## Erros comuns

| Situação | Ação |
|----------|------|
| Skill `ui-ux-pro-max` não encontrada (bundled+global ausentes) | Fallback default (Obsidian Quantum + Anton/Manrope) + aviso. Bundled vem em `${CLAUDE_PLUGIN_ROOT}/skills/ui-ux-pro-max/` por padrão. |
| Skill `taste-skill` não encontrada | Usar subset do briefing direto (cenas-catalog.md §subsets). Bundled em `${CLAUDE_PLUGIN_ROOT}/skills/taste-skill/`. |
| User não escolhe paleta | Default Obsidian Quantum |
| `python3` não disponível pra preview | Instruir abrir manual ou `npx serve` |
| `data/` não existe | `mkdir -p` silencioso |
| CLAUDE.md ausente | Rodar modo briefing direto (sem pré-preenchimento DNA) |
