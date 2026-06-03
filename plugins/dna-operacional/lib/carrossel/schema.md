# Schema do carrossel.json (contrato do roteiro)

Objeto com `meta` + lista `slides`. O gerador (`render_carrossel.py`) lê isto.

```json
{
  "meta": {"handle":"@x","accent":"#C4714A","tema":"escuro","total":7,
           "icon_top":"assets/logo.png","bg_photo":"assets/bg.png"},
  "slides": [
    {"tipo":"cover","kicker":"...","headline":"Domine o {método}","sub":"... {accent}.",
     "compo":{"left":"assets/x.png","left2":"assets/y.png","right_icon":"assets/i.png","right_label":"App"}},
    {"tipo":"content","kicker":"Passo 1","headline":"Crie um {projeto}","sub":"...","hero":"assets/tela.png","hsize":104},
    {"tipo":"quote","kicker":"...","headline":"H {x}","quote":"frase","sub":"..."},
    {"tipo":"cta","headline_top":"Quer?","token":"TOKEN","sub":"... {x}.","bg_photo":"assets/bg.png"}
  ]
}
```

## Convenções
- `{texto}` na headline/sub = palavra accent (**mesma fonte da headline, só muda a cor**; serif itálico só com a classe `.accent-serif`). EXATAMENTE 1 por headline.
- `tipo`: cover | content | quote | cta.
- Caminhos de imagem: relativos ao workdir (`assets/...`). O gerador prefixa `../` automaticamente (HTML vive em slides/).
- `meta.tema`: escuro (default). `meta.total`: nº de slides (numeração).
- `hero` (content): screenshot/réplica. `compo` (cover): personagem/objeto → logo/ícone (alternativa ao `figure`). `icon_top`: logo da marca do projeto (não fixar uma marca). `bg_photo`: imagem de fundo (capa/CTA — opcional).
- `preview` (cta): mockup do brinde/deliverable inclinado no centro (`preview_w`% largura, default 60; `preview_rot`° rotação, default -3).
- **A capa NÃO tem contador** (`snum`). É obviamente o slide 1, e o contador competia com a logo (`icon_top`) no canto superior. Contador só nos slides de conteúdo/quote/cta.

## Capa: herói visual + 2ª imagem (até 2 imagens)

A capa é onde mora o **impacto visual**. Além do `bg_photo` (foto do criador, escurecida) e do `icon_top` (logo), ela aceita **um herói** e, quando preciso, uma **segunda imagem** pra preencher o vazio. Campos (todos opcionais, no slide `cover`):

| Campo | O que é | Default |
|---|---|---|
| `figure` | **Herói** da capa: figura única recortada (mascote, personagem, objeto-prova). PNG transparente. | — |
| `figure_h` | Altura do herói em px (de 1350). ~600-720 = herói forte. | 620 |
| `figure_x` | Deslocamento horizontal do herói a partir do centro (negativo=esquerda, +=direita). Use pra **fugir de colisão com o texto**. | 0 |
| `figure_bottom` | Distância da base em px. Menor = mais pra baixo. | 130 |
| `aux` | **2ª imagem** (print/janela forjada/gráfico) preenchendo o vazio que sobra quando o herói foge do texto. Fica ATRÁS do herói (profundidade). | — |
| `aux_w` | Largura da 2ª imagem em px. | 500 |
| `aux_x` | Distância da esquerda em px. | 40 |
| `aux_bottom` | Distância da base em px. | 430 |
| `aux_rot` | Rotação em graus (ex: -5 = "print vazado") pra dinamismo. | -5 |

**Regra das 2 imagens:** quando o herói (`figure`) precisa sair do centro pra não cobrir o texto (`figure_x`), abre-se um espaço vazio do outro lado. Capa boa **não tem buraco** — preencher com `aux` (uma 2ª prova visual que reforça a headline). O loop de verificação detecta esse vazio e oferece preencher (ver `verify.md`).

`strip` (imagem larga edge-to-edge) e `compo` (personagem+livros→ícone) continuam disponíveis como alternativas de herói. Repertório de QUE imagens forjar/gerar pra capa: ver `forge-screen.md` (telas de SO/app atuais, perfil de rede social, pasta secreta/censurada, gráfico de crescimento) + `assets-pipeline.md` (foto→pixel, mascote).

## Tamanho de cada elemento + escuridão do fundo (todos opcionais)

Pra distribuir bem e **encher o slide** (princípio do MANIFESTO), cada elemento tem tamanho ajustável. Use o **playground** (`render.md`) pra calibrar ao vivo e copiar os valores.

| Campo | Onde | O que controla | Default |
|---|---|---|---|
| `hsize` | cover/content/quote | tamanho (px) da headline. Conteúdo costuma ir **grande** (100-140) pra encher. | 104/96 |
| `sub_size` | cover/content/quote | tamanho (px) do subtítulo. | 34 |
| `quote_size` | quote | tamanho (px) do quote. Pode ir **grande** (80-100) pra dominar o slide. | 58 |
| `hero_w` | content | largura do hero em % do eixo (100 = cheio). | 100 |
| `scrim_top` / `scrim_bot` | cover/cta | opacidade do escurecimento do bg (0 = foto crua, 1 = preto). Foto escura aceita scrim baixo. | 0.42 / 0.72 |

**Distribuição (regra de gosto, validada):** dar **respiro entre headline e sub** e entre os blocos; não amontoar. Imagens/heróis devem **encher o slide** (hero grande, headline grande), não ficar pequenos perdidos no meio. O accent é **a mesma fonte da headline, só muda a cor** (não serifado) — `base.css` já faz isso por padrão.
