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
