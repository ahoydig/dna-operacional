# 1º torneio de capa: piso novo bate o controle, mas juiz LLM diverge do humano

**O que aprendi:** Torneio capa-primeiro (notícia Anthropic US$965bi), 4 motores. Ranking do juiz cego: Viral 43 > Hybrid 39 > Editorial 38 > Controle 34. Dois fatos objetivos a favor do piso novo: controle teve 13 violações de FONT_OFF_SCALE (teses=PASS) e um bug de render real (linha sobreposta atrás de "1 TRILHÃO"). Controle também escreveu "quase 1 trilhão" pra 965bi (inflar número).

**Por quê:** O pipeline novo (contrato de design + qa_lint + best-of-N) produz capa mais consistente que o single-pass atual — isso se confirmou. MAS o humano discordou do 1º lugar do juiz: achou o campeão poluído. Juiz LLM otimiza métrica declarada; humano otimiza clareza.

**Como aplicar:** Manter o piso (lint + contrato) — ele entrega consistência mensurável. Mas (1) incluir slides de conteúdo com screenshot real nas próximas rodadas [[carrossel-screenshot-diferencial]]; (2) recalibrar o juiz pra penalizar densidade [[carrossel-densidade]]; (3) usar gosto humano como árbitro final, não a nota do juiz.
