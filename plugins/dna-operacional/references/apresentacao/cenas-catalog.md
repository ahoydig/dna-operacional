# Catálogo de Cenas — /apresentacao (18 tipos)

Catálogo das 18 cenas do Ahoy Presentation Engine. Cada cena = um `type` aceito em `config.scenes[].type`.

**Formato de cada entrada:**
1. Propósito (quando usar)
2. Campos esperados (`content.*`)
3. Elementos visuais chave
4. Exemplo HTML inline (template function, formato do `main.js`)

---

## 01. `hero` — Abertura com neon

**Propósito:** primeira impressão. Nome do cliente/projeto gigante em neon flicker.

**Quando usar:** SEMPRE como cena 0 em qualquer apresentação.

**Campos:**
```js
content: {
  title: "NOME DO CLIENTE",
  secondaryTitle: "SEGMENTO",                    // opcional
  secondaryTitleStyle: "stroke-light" | "accent" | "cyan",
  subtitle: "CONTEXTO DA PROPOSTA",              // opcional
  effects: { neonFlicker: true, divider: true }
}
```

**Visuais:** mega-title 12vw, neon flicker sequence (500ms scare → 800ms attempt → 1.2s ignition strobe → stabilize), hero-divider animado em scaleX.

**Template:**
```js
hero: c => `<section id="scene-${c.id}" class="scene scene--hero" data-type="static">
  <div class="hero-content text-center">
    <h1 class="mega-title split-chars">${c.content.title}</h1>
    ${c.content.effects?.divider ? '<div class="hero-divider"></div>' : ''}
    ${c.content.secondaryTitle ? `<h2 class="mega-title" style="font-size:6vw;margin-top:1rem"><span class="text-${c.content.secondaryTitleStyle}">${c.content.secondaryTitle}</span></h2>` : ''}
    ${c.content.subtitle ? `<p class="hero-sub split-words" style="margin-top:2rem">${c.content.subtitle}</p>` : ''}
  </div>
</section>`
```

---

## 02. `whoWeAre` — Manifesto

**Propósito:** apresentar a empresa/marca. Nome em destaque + manifesto filosófico.

**Quando usar:** keynote, pitch deck, apresentação institucional. Slide 2 ou 3.

**Campos:**
```js
content: {
  mainText: "AHOY",
  subText: "DIGITAL",
  manifesto: {
    title: "O MANIFESTO",
    text: "Nós não seguimos tendências. Nós as caçamos. Resultados brutais. Sem desculpas."
  }
}
```

**Visuais:** título giant com skewX + glitch horizontal, manifesto revelado linha-por-linha com block reveal (div opaco deslizando de esquerda pra direita).

**Template:**
```js
whoWeAre: c => `<section id="scene-${c.id}" class="scene scene--who-we-are" data-type="static">
  <div class="who-we-are-container">
    <h1 class="who-title-giant" data-text="${c.content.mainText}">${c.content.mainText}</h1>
    <p class="who-subtitle">${c.content.subText}</p>
    <div class="who-manifesto">
      <div class="manifesto-title">${c.content.manifesto.title}</div>
      <div class="manifesto-body">
        ${c.content.manifesto.text.split('. ').map(l => l.trim() ? `<div class="manifesto-line-wrapper"><span class="manifesto-text">${l}.</span><div class="manifesto-block-reveal"></div></div>` : '').join('')}
      </div>
    </div>
  </div>
</section>`
```

---

## 03. `crewShowcase` — Tripulação

**Propósito:** humanizar a empresa. Fotos + nome + cargo + especialidade.

**Quando usar:** pitch, sales deck premium. Máx 7-8 membros.

**Campos:**
```js
content: {
  preTitle: "CONHEÇA O TIME",
  title: "TRIPULAÇÃO",
  subtitle: "sua equipe de operações",
  members: [
    { image: "assets/time/flavio.webp", name: "Flávio Montenegro", role: "Estrategista", specialty: "Growth e IA" },
    // ...
  ]
}
```

**Visuais:** cards com scanlines (cyberpunk), corners em L, photo-overlay gradient, glitch-sm no pre-title, glitch-lg no title.

**Template:** (ver trecho `crewShowcase` no `main.js` de referência — usa 4 corners, scanline, info com `>_ specialty`)

---

## 04. `imageShowcase` — Imagem grande

**Propósito:** exibir logos de clientes, dashboard, print de resultado.

**Quando usar:** prova social, case de sucesso, screenshot de produto.

**Campos:**
```js
content: {
  header: { title: "Nossos", highlight: "Clientes", highlightClass: "text-cyan", subtitle: "..." },
  image: { src: "assets/clientes/logos.png", alt: "...", fit: "contain" }
}
```

**Template:**
```js
imageShowcase: c => `<section id="scene-${c.id}" class="scene scene--image-showcase" data-type="static">
  <div class="scene-glow scene-glow-cyan"></div>
  <div class="showcase-container">
    <div class="showcase-header">
      <h2>${c.content.header.title} <span class="${c.content.header.highlightClass}">${c.content.header.highlight}</span></h2>
      <p class="showcase-subtitle">${c.content.header.subtitle}</p>
    </div>
    <div class="showcase-image-wrapper">
      <img src="${c.content.image.src}" alt="${c.content.image.alt}" class="showcase-image" style="object-fit:${c.content.image.fit || 'contain'}" loading="lazy">
    </div>
  </div>
</section>`
```

---

## 05. `bento` — Grid de cards (logos, stats, resultados)

**Propósito:** grid visual denso pra resultados, marcas, métricas.

**Variants:** `"logos"` | `"maquina"` | `"stats"`

**Campos:**
```js
{
  type: "bento", variant: "maquina", accentColor: "cyan",
  content: {
    header: { title: "NOSSOS", highlight: "RESULTADOS", highlightClass: "text-cyan", subtitle: "..." },
    cards: [
      { type: "result", span: "full", headline: { dot: "cyan pulse", text: "IMPACTO" }, value: 76, plus: true, prefix: "R$", unit: "MILHÕES" },
      { type: "process", span: "2", headline: { dot: "cyan", text: "MÉTRICAS" }, steps: [{ icon: "ph-currency-dollar", label: "INVESTIDO", desc: "R$ 20M" }, ...] },
      { type: "context", headline: { dot: "purple", text: "CAC" }, year: "-68%", tags: [...], caption: "Redução via IA" }
    ]
  }
}
```

**Tipos de card:** `logo` | `result` | `process` | `context` | `alert` | `audit` | `cta`

**Visuais:** CSS Grid com spans (`card-span-2`, `card-full`, `card-row-2`), scene-glow atrás, headline-dot pulsante colorido.

---

## 06. `testimonialCarousel` — Carrossel de depoimentos

**Propósito:** prova social em screenshots de WhatsApp/Instagram.

**Campos:**
```js
content: {
  header: { title: "O que", highlight: "dizem", highlightClass: "text-accent", subtitle: "..." },
  testimonials: [
    { src: "assets/depoimentos/Diego.webp", name: "Diego" },
    // mín 6, duplica pra infinite scroll
  ],
  autoplay: true,
  interval: 4000
}
```

**Visuais:** track infinito (array duplicado), fade-left + fade-right, animation `marqueeScroll`.

---

## 07. `cards` — 3 cards (dores ou diferenciais)

**Propósito:** dor (tint red) ou diferencial (neutro).

**Campos:**
```js
content: {
  header: { title: "O CENÁRIO ATUAL", titleClass: "text-accent glitch-target", subtitle: "\"...\"" },
  background: "gradient-red" | null,
  cards: [
    { icon: "ph-hourglass-medium", title: "Alto Volume", description: "<strong>100+</strong> interações/dia", tint: "red" },
    // 3 cards
  ],
  footer: { label: "CUSTO OCULTO", value: "R$ 54 MIL/ANO", sublabel: "(só em horas)" }
}
```

**Visuais:** glass-card com `red-tint` quando `tint: "red"`, tilt 3D no hover, big-number no footer.

**Template:**
```js
cards: c => `<section id="scene-${c.id}" class="scene scene--cards" data-type="static">
  ${c.content.background ? `<div class="bg-${c.content.background}"></div>` : ''}
  <div class="problem-header text-center">
    <h2 class="${c.content.header.titleClass || ''}">${c.content.header.title}</h2>
    <p class="problem-sub">${c.content.header.subtitle}</p>
  </div>
  <div class="problem-grid">
    ${c.content.cards.map(d => `<div class="card-problem glass-card ${d.tint ? d.tint + '-tint' : ''}">
      <div class="p-icon"><i class="ph ${d.icon}"></i></div>
      <h3>${d.title}</h3><p>${d.description}</p>
    </div>`).join('')}
  </div>
  ${c.content.footer ? `<div class="problem-footer">
    <div class="highlight-box">
      <p>${c.content.footer.label}</p>
      <div class="big-number text-accent split-chars">${c.content.footer.value}</div>
      <p style="opacity:0.5;font-size:0.8rem">${c.content.footer.sublabel}</p>
    </div>
  </div>` : ''}
</section>`
```

---

## 08. `methodology` — Placas 3D empilhadas

**Propósito:** processo de trabalho em etapas com scroll trap interno.

**Campos:**
```js
content: {
  steps: [
    { icon: "ph-crosshair", title: "DIAGNÓSTICO TÁTICO", desc: "Análise de gargalos..." },
    { icon: "ph-gear", title: "IMPLEMENTAÇÃO", desc: "Deploy em sprints..." },
    { icon: "ph-rocket-launch", title: "ESCALA", desc: "Ajustes contínuos..." }
  ]
}
```

**Visuais:** placas 3D com `transform: translateZ(-Npx)` empilhadas. Scroll trap: Observer incrementa índice sem mudar de cena até chegar na última. Cada placa ativa ganha `translateZ(0)` + `scale(1)`.

---

## 09. `solution` — Solução com radar

**Propósito:** apresentação de produto/feature com radar sweep girando atrás.

**Campos:**
```js
content: {
  tagline: "A SOLUÇÃO — FASE 1",
  title: "ACELERADOR DE CONVERSÃO",
  titleClass: "text-cyan glitch-target",
  subtitle: "Agente 24/7.<br>Triagem automática.",
  effects: { radar: true },
  sources: [
    { number: "01", icon: "ph-whatsapp-logo", name: "WHATSAPP" },
    { number: "02", icon: "ph-robot", name: "AGENTE IA" },
    { number: "03", icon: "ph-calendar-check", name: "AGENDAMENTO" }
  ]
}
```

**Visuais:** radar-bg com `conic-gradient` rotation 4s infinite, radar-grid overlay, solution-title 6vw com glitch-target, 3 source-items.

**Template:**
```js
solution: c => `<section id="scene-${c.id}" class="scene scene--solution" data-type="static">
  ${c.content.effects?.radar ? '<div class="radar-bg"></div><div class="radar-grid"></div>' : ''}
  <div class="solution-content">
    <p class="tagline">${c.content.tagline}</p>
    <h1 class="solution-title ${c.content.titleClass}">${c.content.title}</h1>
    <p class="solution-sub">${c.content.subtitle}</p>
    <div class="source-list">
      ${c.content.sources.map(s => `<div class="source-item">
        <div class="source-number">${s.number}</div>
        <i class="ph ${s.icon} source-icon"></i>
        <span class="source-name">${s.name}</span>
      </div>`).join('')}
    </div>
  </div>
</section>`
```

---

## 10. `pipeline` — Fluxo horizontal (scroll trap)

**Propósito:** etapas técnicas de um processo. Navegação horizontal por scroll.

**Campos:**
```js
{
  type: "pipeline", accentColor: "cyan" | "purple",
  content: {
    header: { prefix: "FLUXO", highlight: "VENDAS" },
    scrollHint: "SCROLL TO EXPLORE",
    nodes: [
      { icon: "ph-chat-circle-dots", title: "Lead", desc: "Mensagem no WhatsApp" },
      // 5-9 nodes
    ]
  }
}
```

**Visuais:** pipeline-track em flex horizontal, nodes 300x400px glass-card, scroll trap: Observer consome delta até `progress > 1` e libera pra próxima cena.

**Template:**
```js
pipeline: c => `<section id="scene-${c.id}" class="scene scene--pipeline accent-${c.accentColor}" data-type="pipeline">
  <div class="pipeline-header">
    <h2>${c.content.header.prefix} <span class="text-${c.accentColor}">${c.content.header.highlight}</span></h2>
    <div class="scroll-hint"><i class="ph ph-arrow-right"></i> ${c.content.scrollHint}</div>
  </div>
  <div class="pipeline-track-wrapper">
    <div class="pipeline-track">
      ${c.content.nodes.map((n, i) => `<div class="pipeline-node glass-card" data-step="${i + 1}">
        <div class="node-icon"><i class="ph ${n.icon}"></i></div>
        <h3>${n.title}</h3><p>${n.desc}</p>
        <div class="node-number">${String(i + 1).padStart(2, '0')}</div>
      </div>`).join('')}
    </div>
  </div>
</section>`
```

---

## 11. `value` — Tabela de ROI expansível

**Propósito:** antes/depois de métricas em accordion 3D.

**Campos:**
```js
content: {
  hud: { left: "// ROI_FASE_1", right: "CALCULADO :: CONSERVADOR" },
  header: { parts: [{ text: "ROI", class: "text-glow-white" }, { text: "&", class: "text-outline" }, { text: "GANHOS", class: "text-neon" }], subtitle: "..." },
  rows: [
    { icon: "ph-users", title: "Pacientes Recuperados", subtitle: "Payback Imediato", kpiValue: 2, kpiSuffix: "/ Mês",
      details: { before: { label: "Situação Atual", text: "..." }, after: { label: "Com o Sistema", text: "..." } } }
  ]
}
```

**Visuais:** cyber-table com `transform-style: preserve-3d`, luz passando no `::before` em hover, row.active expande pra mostrar before/after. KPI number anima com `countUp()` helper.

---

## 12. `logicMath` — Cupom fiscal / conta de padaria

**Propósito:** matemática do investimento em formato criativo.

**Campos:**
```js
content: {
  title: "EXTRATO DE RISCO ZERO",
  items: [
    { label: "Investimento Setup", value: "R$ 10.000,00" },
    { label: "Retorno (2 pacientes)", value: "R$ 12.000,00" }
  ],
  total: { label: "SALDO FINAL", value: "+POSITIVO" },
  stamp: "LUCRO GARANTIDO"
}
```

**Visuais:** cupom com typewriter aparecendo linha por linha, carimbo com entrada elástica (`elastic.out(1, 0.3)`), fundo textura papel-recibo.

---

## 13. `investment` — Oferta inicial (preços)

**Propósito:** apresentar preços com âncora (preço riscado) e comparativo.

**Campos:**
```js
content: {
  pricingCards: [
    { label: "SETUP (ÚNICO)", oldPrice: "R$ 15.000", newPrice: "R$ 12.000", features: ["Impl.", "CRM", "Treino"], badge: "50% Aceite / 50% Entrega" },
    { label: "MENSALIDADE", oldPrice: "R$ 2.500", newPrice: "R$ 1.900", features: [...], badge: null }
  ],
  valueColumn: {
    headline: "MELHOR ROI IMEDIATO.",
    crossOutList: ["TRIAGEM MANUAL", "LEADS PERDIDOS"],
    comparison: { label: "1 FUNCIONÁRIO CLT", strikeText: "R$ 4.900/mês", savingsLabel: "ECONOMIA DE", savingsPercent: 72 },
    quote: "\"Recuperando 2 pacientes, se paga.\""
  }
}
```

**Visuais:** 2 colunas, cross-out-list com strike-line animada (width: 0 → 100%), savings-percent countUp, price-headline italic 4vw.

---

## 14. `hazard` — Transição dramática / alerta

**Propósito:** criar tensão. "Pare." Visual de área restrita.

**Campos:**
```js
content: {
  marqueeTop: "ALERTA: VENDER É SÓ O COMEÇO // ...",
  marqueeOverlay: "/// ATENÇÃO_CRÍTICA",
  center: {
    icon: "ph-skull" | "ph-warning-circle",
    title: "PARE.",
    subtitle: "Vender é Só o Começo",
    box: { label: "[ALERTA CRÍTICO]:", text: "O balde furado..." }
  },
  stamp: "RETENÇÃO É LUCRO",
  marqueeBottom: "💡 FASE 2: VENDAS + RETENÇÃO 💡"
}
```

**Visuais:** cyber-grid perspective top/bottom, alarm-pulse, skull 8rem com breathing `sine.inOut` yoyo, hazard-title 10vw com glitch RGB contínuo, stamp seal rotacionado -15deg.

**Template:**
```js
hazard: c => `<section id="scene-${c.id}" class="scene scene--hazard" data-type="static">
  <div class="cyber-grid top"></div><div class="cyber-grid bottom"></div>
  <div class="alarm-pulse"></div>
  <div class="hazard-marquee top">
    <div class="marquee-track"><span class="marquee-text">${c.content.marqueeTop.repeat(4)}</span></div>
    <div class="marquee-overlay">${c.content.marqueeOverlay}</div>
  </div>
  <div class="hazard-center">
    <div class="glitch-layer" data-text="${c.content.center.title}">
      <i class="ph ${c.content.center.icon} hazard-skull"></i>
      <h1 class="hazard-title">${c.content.center.title}</h1>
    </div>
    <p class="hazard-subtitle">${c.content.center.subtitle}</p>
    <div class="hazard-box"><span class="box-label">${c.content.center.box.label}</span> ${c.content.center.box.text}</div>
  </div>
  <div class="stamp-seal"><span>${c.content.stamp}</span></div>
  <div class="hazard-marquee bottom">
    <div class="marquee-track reverse"><span class="marquee-text">${c.content.marqueeBottom.repeat(4)}</span></div>
  </div>
</section>`
```

---

## 15. `investmentFull` — Pacote completo com gráfico

**Propósito:** pacote combinado (Fase 1 + 2) com barras comparativas.

**Campos:**
```js
content: {
  header: { title: "PACOTE", highlight: "COMPLETO", highlightClass: "text-purple", subtitle: "..." },
  pricing: {
    setup: { label: "SETUP TOTAL", badge: "FASE 1 + 2", oldPrice: 18500, newPrice: 15000, subtext: "...", features: [...] },
    monthly: { label: "MENSALIDADE", oldPrice: 3200, newPrice: 2550, addedValue: "+R$ 650", highlight: true, badges: [...], features: [...] }
  },
  comparison: {
    title: "DESTRAVANDO", titleHighlight: "A", titleEnd: "ESCALA",
    marketLine: "Bloqueio Humano",
    bars: [
      { label: "CAPACIDADE ATUAL", value: "~350", type: "expensive", height: 30, strikethrough: true },
      { label: "COM PACOTE", value: "1.000+", type: "cheap", height: 60 },
      { label: "ESCALA MÁXIMA", value: "ILIMITADO", type: "profit", height: 100, icon: "ph-rocket-launch" }
    ],
    savings: "LUCRO 100% ESCALÁVEL"
  }
}
```

**Visuais:** 2 colunas (pricing-glass-card + chart-container), barras com shockwave ao atingir altura final, profit bar com particles.

---

## 16. `protagonistOffer` — Oferta final (Pix de compromisso)

**Propósito:** fechamento agressivo. "Feche agora."

**Campos:**
```js
content: {
  badge: "🔥 EXCLUSIVO PARA QUEM FECHA AGORA",
  headline: { pre: "PIX DE COMPROMISSO", highlight: "R$ 1.000", post: "AGORA" },
  subheadline: "Abate direto do Setup • Garante sua vaga",
  benefits: [
    { type: "setup", icon: "ph-tag", title: "SETUP FACILITADO", oldPrice: "R$ 15.000", newPrice: "R$ 12.500", badge: "R$ 2.500 OFF" },
    { type: "scale", icon: "ph-rocket-launch", title: "PARCEIRO DE ESCALA", feature: "6 MESES DE CARÊNCIA", subfeature: "Módulo Retenção", price: "R$ 1.900/mês", priceNote: "(Fase 1)" }
  ],
  mathBox: {
    title: "MATEMÁTICA DA OPORTUNIDADE",
    rows: [{ label: "Economia Setup", value: "R$ 2.500" }, { label: "Economia Mensal (6x)", value: "R$ 3.900" }],
    total: { label: "VANTAGEM TOTAL", value: "R$ 6.400" },
    tag: "POR DECIDIR AGORA"
  },
  cta: { text: "FECHAR AGORA", icon: "ph-handshake" }
}
```

**Visuais:** protagonist-particles (canvas ou CSS), protagonist-glow central pulsante, benefits em 2 colunas (setup com preço riscado, scale com feature + price), math-box com entrada elástica.

---

## 17. `outro` — Fechamento

**Propósito:** slide final com CTA gigante.

**Campos:**
```js
content: {
  lines: [
    { text: "VAMOS", style: "normal" },
    { text: "TRANSFORMAR", style: "normal" },
    { text: "JUNTOS?", style: "accent-cyan", inline: false }
  ],
  fontSize: "10vw" | "15vw"
}
```

**Template:**
```js
outro: c => `<section id="scene-${c.id}" class="scene scene--outro" data-type="static">
  <h1 class="mega-title split-chars" style="font-size:${c.content.fontSize};line-height:0.8">
    ${c.content.lines.map(l => l.inline
      ? `<span class="${l.style !== 'normal' ? 'text-' + l.style.replace('accent-', '') : ''}">${l.text}</span>`
      : l.text + '<br>'
    ).join('')}
  </h1>
</section>`
```

---

## 18. `blackout` — Slide coringa (objeções)

**Propósito:** slide oculto pra tratar objeções ao vivo.

**Campos:**
```js
content: { hint: "SLIDE DE OBJEÇÃO" }
```

**Template:**
```js
blackout: c => `<section id="scene-${c.id}" class="scene scene--blackout" data-type="static">
  <div class="blackout-hint">${c.content.hint}</div>
</section>`
```

---

## Ícones Phosphor mais usados

| Contexto | Ícones |
|----------|--------|
| Vendas | `ph-chart-line-up`, `ph-trend-up`, `ph-currency-dollar`, `ph-handshake`, `ph-calendar-check` |
| Tempo | `ph-clock`, `ph-clock-countdown`, `ph-hourglass-medium`, `ph-timer` |
| Tech/IA | `ph-robot`, `ph-brain`, `ph-lightning`, `ph-whatsapp-logo`, `ph-code` |
| Comunicação | `ph-chat-circle-dots`, `ph-envelope`, `ph-phone`, `ph-device-mobile` |
| Dados | `ph-database`, `ph-chart-bar`, `ph-funnel`, `ph-kanban` |
| Retenção | `ph-heart`, `ph-users`, `ph-bell-ringing`, `ph-download-simple` |
| Alerta | `ph-warning`, `ph-warning-circle`, `ph-skull`, `ph-trend-down` |
| Sucesso | `ph-check-circle`, `ph-star`, `ph-trophy`, `ph-rocket-launch` |

---

## Animation Presets (por cena)

| Preset | Efeito | Recomendação |
|--------|--------|--------------|
| `zoomIn` | Zoom de fora pra dentro | Padrão maioria |
| `zoomInFar` | Zoom mais distante | Pipelines, fechamento |
| `zoomOut` | Zoom de dentro pra fora | Leave padrão |
| `zoomOutFar` | Zoom mais agressivo | Após solution |
| `slideLeft` | Desliza da direita | ImageShowcase |
| `slideRight` | Desliza da esquerda | Leave de slideLeft |
| `fadeBlur` | Fade com blur | Transições suaves |
| `splitExit` | Divide e sai | Após investment |
| `explosionIn` | Explode centralmente | Protagonist Offer |

---

## Subsets recomendados por tipo de briefing

**Sales deck (10 slides):**
1. hero → 2. cards (dor) → 3. solution → 4. pipeline → 5. value → 6. hazard → 7. investment → 8. imageShowcase (clientes) → 9. protagonistOffer → 10. outro

**Keynote (8 slides):**
1. hero → 2. whoWeAre → 3. bento (stats) → 4. methodology → 5. solution → 6. imageShowcase → 7. cards (diferenciais) → 8. outro

**Pitch deck investidor (12 slides):**
1. hero → 2. whoWeAre → 3. cards (problem) → 4. solution → 5. bento (market) → 6. imageShowcase (traction) → 7. methodology → 8. value → 9. crewShowcase → 10. investmentFull → 11. protagonistOffer → 12. outro

**Workshop educativo (6 slides):**
1. hero → 2. whoWeAre → 3. methodology → 4. pipeline → 5. solution → 6. outro

**Kickoff cliente (7 slides):**
1. hero → 2. whoWeAre → 3. methodology → 4. pipeline (cronograma) → 5. value (expectativa) → 6. crewShowcase → 7. outro
