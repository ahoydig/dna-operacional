# Carrossel viral: clonar a GEOMETRIA real, não extrair padrões abstratos

**O que aprendi:** Minhas primeiras 3 tentativas de carrossel ficaram "lixo" (palavra do Flávio) porque eu extraía padrões abstratos (cor/copy) e mandava subagente montar HTML às cegas. O resultado tinha buraco, mau alinhamento, mascote solto. Só funcionou quando eu MEDÍ a geometria real dos virais (eixo de coluna 48px, headline 80-140px, herói 35-48% da altura, 3 templates) e cloneei com minhas mãos — construindo o template, renderizando, comparando com o original lado a lado.

**Por quê:** "Padrão abstrato" (ex: "headline gigante + 1 accent") não basta pra reproduzir — perde as proporções e a distribuição vertical que fazem o slide preencher o canvas sem buraco. O segredo do alinhamento é o **padding-x consistente** (headline + screenshot + footer no mesmo eixo esquerdo) — "grid sem grid".

**Como aplicar:**
- Antes de gerar, ter o MANIFESTO-DIAGRAMACAO.md (medições reais dos virais) como blueprint.
- Construir o gerador (Python → HTML/CSS) com 3 templates fixos (capa/conteúdo/CTA), eixo 48px, NÃO delegar a montagem cega.
- Ver: `scrape-virais/MANIFESTO-DIAGRAMACAO.md` + as RECEITA.md por carrossel. [[carrossel-loop-verificacao]] [[carrossel-ativos-reais]]
