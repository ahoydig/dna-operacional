# Playground HTML pra ajustar o carrossel ao vivo (em vez de ping-pong de JSON)

**O que aprendi:** Pra calibrar tamanho/posição dos elementos, um **playground** ao vivo bate muito ping-pong de "muda o número → re-renderiza → vê → repete". `lib/carrossel/playground.html` carrega os `slides/NN.html` REAIS num iframe (1:1 com o PNG, mesma `base.css`/fontes) e expõe sliders por slide: headline/sub/quote, hero, figure/aux da capa, scrim, cor do accent. Botão "Copiar carrossel.json" cospe os valores.

**Por quê:** A gente gastou várias rodadas afinando `hsize`/`figure_x`/`aux_*` no olho. O Flávio pediu o playground pra ajustar ele mesmo e validar (principalmente a capa). Funcionou: ele tunou tudo e colou o JSON de volta.

**Como aplicar:**
- Rodar precisa de servidor (iframe same-origin + fontes): `cp playground.html <workdir> && cd <workdir> && python3 -m http.server 8777 && open http://localhost:8777/playground.html`. file:// não funciona (bloqueia contentDocument).
- Os controles só funcionam porque os elementos têm hooks: `.headline`/`.sub`/`.quote`/`.shot`/`.scrim` + `#cover-fig`/`#cover-aux` (ids adicionados no `templates.py`). Knobs que round-trip pro JSON: `hsize`, `sub_size`, `quote_size`, `hero_w`, `figure_h/x/bottom`, `aux_w/x/bottom/rot`, `scrim_top/bot`, `meta.accent`.
- Documentado em `render.md` (§ Playground) + Passo 4.5 do command. [[carrossel-distribuicao-tamanho]]
