# Capa de carrossel pode precisar de 2 imagens (herói + 2ª prova), e o loop tem que oferecer

**O que aprendi:** A capa boa costuma pedir **duas** imagens, não uma. Quando o herói (`figure`, ex:
mascote) é deslocado do centro (`figure_x`) pra não cobrir o texto, abre um **espaço vazio** do outro
lado. Capa boa é densa e equilibrada — não tem buraco. Esse vazio se preenche com uma **2ª imagem**
(`aux`: print/janela forjada/gráfico) que reforça a headline.

**Por quê:** Mandei a capa com o herói tampando o fim do subtítulo, e depois com um buraco à esquerda.
O Flávio: isso eu deveria ter pego no loop antes de mandar; e "pra deixar melhor a capa, a gente
precisaria de 2 imagens — você precisa ter essa análise". O ponto fino: **escolher QUE 2ª imagem entra
é decisão criativa do user** — o loop não deve auto-preencher no escuro; deve **parar e oferecer** com
2-3 sugestões concretas + a opção de enviar como está.

**Como aplicar:**
- Loop pega `FIGURE_OVER_TEXT` (herói sobre texto → `figure_x`/`figure_bottom`) e `COVER_EMPTY_GAP`
  (vazio após deslocar → oferecer `aux`). Posição/tamanho da 2ª imagem é auto (`aux_w/x/bottom/rot`);
  o **conteúdo**, pergunta.
- Campos no `_cover` do `templates.py`: `figure`+`figure_x`+`figure_h`+`figure_bottom` (herói),
  `aux`+`aux_w`+`aux_x`+`aux_bottom`+`aux_rot` (2ª imagem, atrás do herói = profundidade). Doc em
  `lib/carrossel/schema.md` e `verify.md` itens 12-13. [[carrossel-loop-verificacao]] [[carrossel-repertorio-capa]]
