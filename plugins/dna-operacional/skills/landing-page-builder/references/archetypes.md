# Arquetipos de Layout
### Catalogo de padroes para secoes de landing page

Nunca repetir o mesmo arquetipo entre secoes consecutivas.

---

## Grid e Densidade

| Arquetipo | Descricao | Quando usar |
|---|---|---|
| **Bento Box Dinamico** | Celulas assimetricas que reorganizam no resize | Servicos, features com quantidade variavel |
| **Broken Grid / Brutalismo** | Elementos sobrepostos intencionalmente | Marcas ousadas, tech, portfolio |
| **Responsive Typography Grid** | Tipografia massiva dita o fluxo | Heroes, CTAs, statements |
| **Editorial Asymmetry** | Vazios horizontais com texto fino | Depoimentos, quotes, sobre |
| **Swiss Poster Grid** | Precisao matematica anos 60 | Clean, minimal, corporativo |
| **Chaotic Stacking** | Container central com z-index sobrepostos | Destaque de produto, showcase |

## Profundidade e Camadas

| Arquetipo | Descricao | Quando usar |
|---|---|---|
| **Glassmorphism Imersivo** | Camadas translucidas com backdrop blur | Premium, SaaS, fintech |
| **Parallax Layers** | Camadas scroll-driven a 120fps | Storytelling, produto |
| **Z-Index Traps** | Elementos revelados atras de containers scrolling | Surpresa, gamificacao |
| **Atmospheric Perspective** | Camadas distantes com contraste reduzido | Paisagem, profundidade |

## Fluxo e Cinematica

| Arquetipo | Descricao | Quando usar |
|---|---|---|
| **GSAP Pinned Sections** | Scroll para, tela divide lateralmente | Processo, timeline |
| **Horizontal Scroll Hijack** | Conversao vertical→horizontal | Portfolio, galeria |
| **Scroll por Clip-Path** | Desenrola como cortina | Reveal dramatico |
| **Sticky Typography Masks** | Texto gigante de fundo preenche overlays | Statement, branding |
| **Progressive Disintegration** | Scroll decompoe texto em pecas flutuantes | Artistico, experimental |

## Foco Unico

| Arquetipo | Descricao | Quando usar |
|---|---|---|
| **Hero Dominante Absoluto** | 100vh, texto massivo centralizado | Lancamento, waitlist |
| **Isolamento de Mascara** | Resto da tela escuro, CTA isolado | Oferta, pricing |
| **Vast Negative Space** | 80% vazio, micro-info nas margens | Luxo, minimal |
| **The Monolith** | Elemento central gigante rotacionando 3D | Produto fisico, app |
| **Tunnel Vision** | "Portas" concentricas forcando olhar pro CTA | Conversao agressiva |

## Tipografia Brutalista

| Tecnica | CSS | Quando usar |
|---|---|---|
| **Headline Esmagadora** | `clamp(4rem, 10vw, 12rem)` | Hero, CTA final |
| **Texto Recortado** | `background-clip: text` sobre video/SVG | Hero criativo |
| **Marquee Interminavel** | text-stroke, scroll infinito | Social proof, parceiros |
| **Outline Font** | `-webkit-text-stroke`, fill on hover | Interativo, menu |
| **Vertical Japanese** | `writing-mode: vertical-rl` | Sidebar, labels |
| **Perspective Type** | `rotateX(45deg) skew(-10deg)` | Statement dramatico |

## Textura e Visual

| Tecnica | Implementacao | Quando usar |
|---|---|---|
| **Noise CSS** | SVG filter `feTurbulence` @ 0.05 opacity | Grunge, vintage |
| **Radial Blobs** | border-radius 50% + blur animado | Fundo organico |
| **Mesh Gradients** | 4 pontos rotacionando mesh organico | Background premium |
| **Vignette** | `box-shadow: inset` escurecendo bordas | Foco central, dramatico |
| **Glitch Offset** | text-shadow RGB split + skew | Tech, hacker, terminal |
| **Scanlines** | repeating-linear-gradient 2-4px | Retro, terminal |
| **Grid Pattern** | background-image com linhas finas | Tech, blueprint |

---

## Regra de Ouro

Escolha arquetipos que contrastem entre si. Se a secao 1 e hero dominante com tipografia massiva, a secao 2 pode ser offset grid com cards ou editorial asymmetry. Nunca 2 secoes consecutivas com o mesmo padrao visual.
