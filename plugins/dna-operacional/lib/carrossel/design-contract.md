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
