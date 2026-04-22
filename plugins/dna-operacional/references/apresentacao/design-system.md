# Design System — /apresentacao (Ahoy Presentation Engine)

Referência destilada do **Ahoy Presentation Engine** (Awwwards-ready) — base do plugin DNA Operacional. Tudo aqui é pra ser consumido pela skill `/apresentacao` ao gerar HTML + CSS + JS Vanilla + GSAP.

> **Filosofia do engine:** build 100% Vanilla JS + GSAP. Zero framework. Rodável em Netlify. Tokens via CSS custom properties injetadas em runtime.
>
> **Filosofia:** apresentação NÃO é .pptx. É um site cinematográfico — transições Z-axis, neon flicker, glitch RGB, scroll trap em pipelines, custom cursor, noise overlay. Fullscreen browser. Rodável em Netlify.

---

## 1. Arquitetura do output

```
<slug>/
├── index.html           # boilerplate com <main id="app">
├── style.css            # tokens + scene styles + animations
├── main.js              # GSAP engine (Observer + ScrollTrigger) + Templates
└── config.js            # dados da apresentação (scenes array)
```

**Padrão:** `index.html` é estático. `main.js` lê `config.js`, seleciona template por tipo de cena, injeta tokens do tema, monta DOM em `#app`, ativa Observer pra navegação wheel/touch/teclado, roda animação de entrada por cena.

---

## 2. Design Tokens — Obsidian Quantum Theme (default)

```css
:root {
    /* Core */
    --c-bg: #050505;                            /* Background principal */
    --c-text: #FFFFFF;                          /* Texto principal */
    --c-text-dim: rgba(255, 255, 255, 0.5);     /* Texto secundário */

    /* Accent palette */
    --c-cyan: #00F0FF;                          /* Sentinela, radar, neon */
    --c-purple: #7000FF;                        /* Fábrica, pipeline v2 */
    --c-accent: #FF4D4D;                        /* Problema, strike lines */
    --c-success: #00FF94;                       /* ROI, pricing, success */

    /* Hazard inline (cena warning) */
    --c-hazard-red: #FF003C;                    /* Skull, stamp, glitch */
    --c-hazard-yellow: #F0E600;                 /* Marquee borders */

    /* Easing */
    --e-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    --e-in-out: cubic-bezier(0.65, 0, 0.35, 1);
}
```

**Como `/apresentacao` escolhe paleta:**

A skill chama `ui-ux-pro-max` pra sugerir 3 paletas alinhadas com o briefing. O user escolhe. A paleta escolhida sobrescreve os tokens acima via `injectTheme(config.theme)` no início do `main.js`.

Exemplos de paletas alternativas (fallback quando user não escolhe):

| Tema | `--c-cyan` | `--c-purple` | `--c-accent` | `--c-success` |
|------|-----------|-------------|-------------|--------------|
| Obsidian Quantum (default) | `#00F0FF` | `#7000FF` | `#FF4D4D` | `#00FF94` |
| Warm Editorial | `#FFB800` | `#FF3366` | `#E85D04` | `#06D6A0` |
| Cold Minimal | `#4EA1F7` | `#6C5CE7` | `#EB4D4B` | `#10B981` |

---

## 3. Tipografia

### Famílias

| Token | Fonte | Uso |
|-------|-------|-----|
| `--f-display` | `'Anton', sans-serif` | Títulos mega, números grandes, CTAs |
| `--f-body` | `'Manrope', sans-serif` | Corpo de texto, descrições |
| `--f-mono` | `ui-monospace, 'JetBrains Mono', monospace` | HUD, counters, marquee, tags |

**CDN Google Fonts:**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@300;400;600&display=swap" rel="stylesheet">
```

### Escala (viewport-relative, fluid)

| Classe | Tamanho | Onde |
|--------|---------|------|
| `.mega-title` (hero) | `12vw` | Hero title (neon flicker) |
| `.mega-title` (outro) | `15vw` | Slide final |
| `.hazard-title` | `10vw` | Cena hazard (glitch RGB) |
| `.value-header h1` | `7vw` italic | Header de ROI |
| `.solution-title` | `6vw` | Nome do produto |
| `.big-number` | `6vw` | Números grandes (cards) |
| `.price-headline` | `4vw` italic | Chamada de preço |
| `.pipeline-header h2` | `4vw` | Título de pipeline |
| `.savings-percent` | `4rem` | % de economia |
| `.kpi-number` | `3rem` | Números em accordion ROI |
| `.highlight-number` | `2.5rem` | Gauges e dashboards |
| `.hero-sub` | `1.2rem` + `letter-spacing: 0.3em` | Tagline, supporting copy |

**Regra:** toda headline importante ganha **font-feature**: `font-variant-ligatures: none; letter-spacing: -0.02em;`. Tudo maiúsculo (`text-transform: uppercase`) por default em headers de cena.

---

## 4. Efeitos de Texto (signatures do engine)

### 4.1 Neon Flicker (Hero)

```css
.neon-off {
    -webkit-text-stroke: 1px rgba(255, 255, 255, 0.15);
    color: transparent;
    opacity: 0.1;
}
.neon-on {
    color: #FFFFFF;
    opacity: 1;
    text-shadow:
        0 0 10px rgba(0, 240, 255, 0.8),
        0 0 20px rgba(0, 240, 255, 0.6),
        0 0 40px rgba(0, 240, 255, 0.4);
}
```

### 4.2 Glow Variants

```css
.text-neon { color: var(--c-success); text-shadow: 0 0 10px rgba(0, 255, 148, 0.5), 0 0 30px rgba(0, 255, 148, 0.4); }
.text-outline { -webkit-text-stroke: 2px rgba(255, 255, 255, 0.6); color: transparent; }
.text-glow-white { text-shadow: 0 0 20px rgba(255, 255, 255, 0.3); }
.text-cyan { color: var(--c-cyan); }
.text-purple { color: var(--c-purple); }
.text-accent { color: var(--c-accent); }
```

### 4.3 Stroke Variants

```css
.text-stroke { -webkit-text-stroke: 2px white; color: transparent; }
.text-stroke-light { -webkit-text-stroke: 1px rgba(255, 255, 255, 0.5); color: transparent; }
.strike-dim { text-decoration: line-through; opacity: 0.3; color: #666; }
```

### 4.4 Glitch RGB (Hazard + Crew titles)

```css
.glitch-layer::before,
.glitch-layer::after {
    content: attr(data-text);
    position: absolute;
    inset: 0;
    pointer-events: none;
}
.glitch-layer::before { color: var(--c-cyan); }
.glitch-layer::after { color: var(--c-hazard-red); }
.glitch-layer.active::before { animation: glitchCyan 0.3s steps(2) infinite; }
.glitch-layer.active::after  { animation: glitchRed  0.3s steps(2) infinite; }
```

(Keyframes em §8.)

---

## 5. Componentes UI persistentes

### 5.1 Noise Overlay (fixed)

```css
.noise-overlay {
    position: fixed; inset: 0; z-index: 9000;
    opacity: 0.04; pointer-events: none;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence baseFrequency='0.9' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='0.5'/></svg>");
}
```

### 5.2 Custom Cursor

```css
.cursor-dot  { width: 8px;  height: 8px;  mix-blend-mode: difference; transition: 0.1s; z-index: 10000; }
.cursor-ring { width: 40px; height: 40px; mix-blend-mode: difference; transition: 0.4s; z-index: 9999; border: 1px solid white; border-radius: 50%; }
```

### 5.3 Slide Counter (fixed bottom-left)

```css
.slide-counter { position: fixed; bottom: 20px; left: 20px; z-index: 9999; display: flex; gap: 8px; }
.slide-dot { width: 32px; height: 32px; border: 1px solid rgba(255,255,255,0.3); font-family: var(--f-mono); font-size: 0.7rem; display: grid; place-items: center; }
.slide-dot.active { color: var(--c-cyan); border-color: var(--c-cyan); }
```

### 5.4 Glass Card

```css
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
}
.glass-card.red-tint   { background: rgba(255, 77, 77, 0.05); border-color: rgba(255, 77, 77, 0.2); }
.glass-card.cyan-tint  { background: rgba(0, 240, 255, 0.04); border-color: rgba(0, 240, 255, 0.2); }
.glass-card.purple-tint { background: rgba(112, 0, 255, 0.04); border-color: rgba(112, 0, 255, 0.25); }
```

---

## 6. Layout Base (body → scene → content)

```css
html, body { width: 100%; height: 100%; overflow: hidden; background: var(--c-bg); color: var(--c-text); cursor: none; }

#app { position: relative; width: 100vw; height: 100vh; perspective: 1000px; transform-style: preserve-3d; }

.scene {
    position: absolute; inset: 0;
    display: grid; place-items: center;
    visibility: hidden;
    will-change: transform, opacity;
    transform-style: preserve-3d;
}
.scene.active { visibility: visible; z-index: 10; }
```

**Regra ferro:** cenas inativas ficam `visibility: hidden` (não consomem GPU). `.active` é adicionado pela engine durante transições Z-axis.

---

## 7. Z-Index Stack (obrigatório)

| Camada | z-index | Elemento |
|--------|---------|----------|
| 10000 | Cursor Dot | |
| 9999  | Cursor Ring, Slide Counter | |
| 9000  | Noise Overlay | |
| 5000  | UI Layer (fullscreen button, progress bar) | |
| 20    | Stamp Seal, Pipeline Header | |
| 10    | Scene Active, Hazard Center | |
| 5     | Marquee | |

---

## 8. Keyframes essenciais

```css
@keyframes gridScroll { from { background-position: 0 0; } to { background-position: 50px 50px; } }

@keyframes alarmPulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 0.8; } }

@keyframes titleGlitch {
    0%, 90%, 100% { text-shadow: none; transform: translate(0); }
    91% { text-shadow: -2px 0 cyan, 2px 0 #FF003C; transform: translate(-1px, 1px); }
    92% { text-shadow: 2px 0 cyan, -2px 0 #FF003C; transform: translate(1px, -1px); }
    93% { text-shadow: -2px 0 cyan, 2px 0 #FF003C; transform: translate(-1px, -1px); }
    94% { text-shadow: 2px 0 cyan, -2px 0 #FF003C; transform: translate(1px, 1px); }
}

@keyframes glitchCyan {
    0%   { transform: translate(-2px, 2px); opacity: 0.8; clip-path: inset(20% 0 30% 0); }
    50%  { transform: translate(2px, -2px); opacity: 0.6; clip-path: inset(50% 0 20% 0); }
    100% { transform: translate(-2px, 2px); opacity: 0.8; clip-path: inset(10% 0 60% 0); }
}

@keyframes glitchRed {
    0%   { transform: translate(2px, -2px); opacity: 0.8; clip-path: inset(40% 0 20% 0); }
    50%  { transform: translate(-2px, 2px); opacity: 0.6; clip-path: inset(20% 0 50% 0); }
    100% { transform: translate(2px, -2px); opacity: 0.8; clip-path: inset(60% 0 10% 0); }
}

@keyframes shockwave {
    0%   { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0.5); }
    100% { box-shadow: 0 0 0 30px rgba(0, 240, 255, 0); }
}

@keyframes marqueeScroll {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
}

@keyframes radarSweep { to { transform: rotate(360deg); } }
```

---

## 9. GSAP Easing Reference

| Ease | Uso |
|------|-----|
| `power2.out` | Cursor tween, scroll, fade in |
| `power3.inOut` | Scene transitions (Z-axis) |
| `power3.out` | Title reveals, splitText entrances |
| `back.out(1.5-1.7)` | Card entrances, new price pops, highlights |
| `elastic.out(1, 0.3-0.5)` | Skull entrance, stamp explosive, sources |
| `expo.out` | Module entrances (factory), header slides |
| `sine.inOut` | Skull breathing, radar pulse (yoyo) |
| `none` (linear) | Radar rotation, marquee scroll |

---

## 10. Responsividade

```css
@media (max-width: 768px) {
    .mega-title { font-size: 18vw; }
    .hazard-title { font-size: 15vw; }
    .hazard-skull { font-size: 5rem; }
    .price-headline { font-size: 2.5rem; }
    .investment-grid,
    .factory-dashboard { grid-template-columns: 1fr; }
    .stamp-seal { position: relative; margin-top: 2rem; }
    .pipeline-node { width: 260px; height: 360px; }
}

@media (prefers-reduced-motion: reduce) {
    .neon-on, .glitch-layer.active::before, .glitch-layer.active::after { animation: none !important; }
}
```

**Mobile-first:** a engine respeita `prefers-reduced-motion`. Se user ativa, a skill injeta `data-reduced="true"` no body e desliga `neon-flicker` + `glitch` automaticamente.

---

## 11. Performance (boas práticas)

1. `will-change: transform, opacity` em `.scene` e `.pipeline-track`
2. Usar `transform: translate3d(...)` em vez de mudança de `top`/`left`
3. `visibility: hidden` remove cenas inativas da árvore de renderização
4. Event listeners removidos no `leave()` de cada cena (evita leak)
5. `gsap.killTweensOf(target)` antes de iniciar nova animação
6. `clearInterval()` de qualquer loop (glitch random, marquee lento) quando cena deixa o viewport
7. `<img>` com `loading="lazy"` e `decoding="async"`
8. Fontes com `font-display: swap`

---

## 12. Sinalização visual por tipo de briefing

**Sales deck (venda direta):**
- Paleta: Obsidian Quantum default
- Heavy use: `hero` (neon) → `cards` (dor) → `solution` (radar) → `pipeline` → `investment` + `protagonistOffer` → `outro`

**Keynote / thought leadership:**
- Paleta: Warm Editorial
- Heavy use: `hero` → `whoWeAre` (manifesto) → `bento` (stats) → `methodology` (placas 3D) → `imageShowcase` → `outro`

**Pitch deck (investidor):**
- Paleta: Cold Minimal
- Heavy use: `hero` → `cards` (problem) → `solution` → `bento` (market size) → `value` (projeções) → `investmentFull` → `outro`

**Workshop / educativo:**
- Paleta: qualquer, low-intensity
- Heavy use: `hero` → `whoWeAre` → `methodology` → `pipeline` (módulos) → `outro`

---

## 13. Princípios core

- 18 cenas catalogadas (ver `cenas-catalog.md`)
- 7 cores core + 2 hazard na paleta base
- Inline CDN (Phosphor icons + Anton + Manrope) — zero build step
- `injectTheme()` na inicialização permite override dinâmico da paleta via ui-ux-pro-max
- Custom cursor + noise overlay persistentes por default
- Respeita `prefers-reduced-motion`
