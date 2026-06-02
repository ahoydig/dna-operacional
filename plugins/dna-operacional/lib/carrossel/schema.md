# Schema do carrossel.json (contrato do roteiro)

Objeto com `meta` + lista `slides`. O gerador (`render_carrossel.py`) lê isto.

```json
{
  "meta": {"handle":"@x","accent":"#C4714A","tema":"escuro","total":7,
           "icon_top":"assets/claude-sun.png","bg_photo":"assets/bg.png"},
  "slides": [
    {"tipo":"cover","kicker":"...","headline":"Clone o {Hormozi}","sub":"... {accent}.",
     "compo":{"left":"assets/x.png","left2":"assets/y.png","right_icon":"assets/i.png","right_label":"Claude"}},
    {"tipo":"content","kicker":"Passo 1","headline":"Crie um {projeto}","sub":"...","hero":"assets/tela.png","hsize":104},
    {"tipo":"quote","kicker":"...","headline":"H {x}","quote":"frase","sub":"..."},
    {"tipo":"cta","headline_top":"Quer?","token":"TOKEN","sub":"... {x}.","bg_photo":"assets/bg.png"}
  ]
}
```

## Convenções
- `{texto}` na headline/sub = palavra accent (vira serif itálico colorido). EXATAMENTE 1 por headline.
- `tipo`: cover | content | quote | cta.
- Caminhos de imagem: relativos ao workdir (`assets/...`). O gerador prefixa `../` automaticamente (HTML vive em slides/).
- `meta.tema`: escuro (default). `meta.total`: nº de slides (numeração).
- `hero` (content): screenshot/réplica. `compo` (cover): personagem+livros → ícone. `bg_photo`: foto de fundo (capa/CTA).
