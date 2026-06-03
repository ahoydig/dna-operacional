# Screenshot Engine

Ordem: **captura real > réplica fiel em HTML > pedir ao user**.

## 1. Captura real

Seguir `references/carrossel-lab/screenshot-guide.md` por fonte (X, Instagram, GitHub, notícia, etc.). Traduzir texto em inglês via DOM antes de capturar (PT-BR). Camuflar dados sensíveis.

## 2. Réplica fiel (se a captura falhar)

Recriar o componente real em HTML/CSS com cara de verdade (ver seção "Réplica fiel" em `screenshot-guide.md`). Marcar `data-replica="true"`. Renderizar como PNG via o render harness e usar como o screenshot do slide.

## 3. Fallback manual

Se nem captura nem réplica servirem, pedir o arquivo ao user e aplicar o `.screenshot-frame`.

## Honestidade (regra dura)

Réplica reproduz a forma, não fabrica fato. Número/citação dentro da réplica ou vem da fonte real, ou é claramente ilustrativo. Nunca apresentar réplica como print autêntico.
