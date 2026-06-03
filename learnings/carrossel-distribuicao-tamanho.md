# Distribuição e tamanho: encher o slide, respiro entre headline e sub, accent flat

**O que aprendi:** Preferências de design do Flávio, validadas no playground:
- **Encher o slide:** headlines de conteúdo grandes (100-140px), quote grande (80-100px), e o **hero enche o slide** — imagem pequena perdida no meio é defeito. Telas forjadas têm que nascer **altas** (mais conteúdo) pra ter presença.
- **Respiro:** distribuir bem, com espaço entre headline e sub e entre os blocos; não amontoar.
- **Accent = mesma fonte (Nofex), só a cor muda** — a serifada itálica nas headlines "não ficou boa". `base.css` já é flat por padrão (`.headline .em{color:var(--accent)}`); serif virou opt-in (`.accent-serif`).
- **BG capa/CTA menos escuro** — scrim default caiu pra 0.42/0.72 (era 0.62/0.86); com foto bem escura dá até pra ir a 0 (foto crua). Ajustável por slide (`scrim_top`/`scrim_bot`).

**Por quê:** Na 1ª rodada da skill num tema novo, a capa ficou apertada e as telas dos slides ficaram pequenas/curtas. O Flávio: "deveria estar mais bem distribuído, mais respiro entre a headline e a sub, ou aumentar a imagem pra encher mais o slide". E não gostou da serifada.

**Como aplicar:** Tunar `hsize`/`sub_size`/`quote_size`/`hero_w`/`scrim_*` por slide (via playground). Loop pega `CRAMPED_LAYOUT` e `HERO_TOO_SMALL`. Princípios documentados em `schema.md`, `command` (regra 11) e `verify.md`. [[carrossel-playground]] [[carrossel-densidade]]
