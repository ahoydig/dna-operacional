# Forjar tela de SO/app na versão ATUAL (não emoji/asset velho) + censura pixelada

**O que aprendi:** Ao forjar ícone/tela de sistema (macOS Finder, iOS, app), replicar o **design
atual**. **Emoji renderiza o asset velho** — `📁` é a pasta cinza-azul skeuomórfica antiga, não a flat
de hoje. A pasta macOS atual (Big Sur+) é **azul ciano vivo com uma linha branca de brilho no topo do
flap**, flat — desenhar em **SVG**, não emoji. Cadeado moderno = círculo escuro + cadeado branco SVG
(não o 🔒 dourado). Pra "secreto", censura = **mosaico pixelado** (grid de células cinza ~7px), não
tarja preta chapada.

**Por quê:** Forjei a janela do Finder com emoji 📁 e tarja preta. O Flávio mandou um print real da
pasta dele: "isso é uma pasta de MacBook pra você ter noção... do software do macOS atual". Reclamou da
pasta velha e pediu censura "mais censurada, com sensação de pixelado". Refazer com SVG ciano + linha
branca + mosaico bateu na referência.

**Como aplicar:**
- SVG da pasta macOS atual + técnica de censura pixelada documentados em `lib/carrossel/forge-screen.md`
  §6-7 (com o código pronto). Harness de forja: ver o padrão em `lib/carrossel/render.mjs` /
  `forge-screen.md` §4 (captura do elemento, `omitBackground`).
- Em dúvida do design atual de qualquer UI, **pedir um print de referência** ao user — a UI muda.
  [[carrossel-repertorio-capa]] [[carrossel-screenshot-diferencial]]
