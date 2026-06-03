# Loop de verificação visual — agente revisor + auto-correção

Protocolo OBRIGATÓRIO entre "render gerado" e "mostrar ao user". Decisão do user: **a verificação é
um agente revisor automático que LÊ cada PNG, compara com o MANIFESTO, e auto-corrige** mexendo no
`carrossel.json`/assets, re-renderizando, e repetindo até **zero defeitos**. O user só vê o resultado
no fim. Nunca apresentar carrossel que não passou o loop completo (lint exit 0 em todos + revisor
retornando `[]` de defeitos).

Vale pra qualquer carrossel produzido por esta lib. Artefatos canônicos referenciados aqui:
`base.css` (contrato visual), `templates.py` (geometria/tipos), `render_carrossel.py` (json → html),
`render.mjs` (html → png), `qa_lint.py` (lint estrutural), `schema.md` (formato do json),
`${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md` (blueprint de geometria — a fonte de verdade
do revisor).

---

## O CICLO (5 etapas, repetir até passar)

```
                ┌─────────────────────────────────────────────┐
                │  carrossel.json  +  assets/  +  fonts/       │
                └─────────────────────────────────────────────┘
                                   │
   (1) RENDER ESTRUTURAL  python3 render_carrossel.py carrossel.json slides/
                                   │   → slides/NN.html
   (2) RENDER VISUAL      node render.mjs slides/
                                   │   → slides/NN.png  (1080×1350 @2x, clip fixo)
   (3) LINT ESTRUTURAL    python3 qa_lint.py slides/NN.html  (cada slide, exit 0)
                                   │   falhou? → corrige json/css → volta a (1)
   (4) REVISOR VISUAL     Read de CADA slides/NN.png  vs MANIFESTO  → JSON [{slide,defeitos}]
                                   │   defeitos? → (5)
   (5) AUTO-CORREÇÃO      edita carrossel.json / regenera asset  → volta a (1)
                                   │
                          zero defeitos em TODOS  →  ✅ mostra ao user
```

### Etapa 1 — Render estrutural (json → html)

```bash
python3 <lib>/carrossel/render_carrossel.py <workdir>/carrossel.json <workdir>/slides
```

Gera `slides/01.html … NN.html`. Cada HTML linka `../base.css` e injeta `@import` Google Fonts +
`@font-face` Nofex/Crankdat de `../fonts/`. Os HTML vivem em `slides/`, então **todo caminho de asset
no json é relativo ao workdir** (`assets/x.png`) e `templates.asset()` prefixa `../`
automaticamente. Não escrever `../` no json.

### Etapa 2 — Render visual (html → png)

```bash
# render.mjs roda DE DENTRO do workdir (ESM resolve playwright a partir da pasta do script, não do cwd).
cp <lib>/carrossel/render.mjs <workdir>/render.mjs
ln -sfn /Users/flavioahoy/Documents/projects/propostas/node_modules <workdir>/node_modules
cd <workdir> && node ./render.mjs ./slides
# rodar direto de <lib>/carrossel/render.mjs falha com ERR_MODULE_NOT_FOUND: playwright
```

Playwright, viewport 1080×1350, deviceScaleFactor 2, `waitUntil:networkidle` + `document.fonts.ready`
+ 2200ms. Captura por **clip fixo `{x:0,y:0,width:1080,height:1350}`** — NÃO o bounding box do
elemento. Consequência prática: **qualquer coisa que vaze do `.slide` (texto cortado na base,
personagem saindo embaixo, footer empurrado pra fora) é cortada pelo clip e some no PNG, ou aparece
truncada.** O revisor TEM que pegar isso olhando o PNG, não o HTML. Se o PNG não foi gerado pra algum
slide, é erro fatal — não seguir.

### Etapa 3 — Lint estrutural (gate automático, exit code)

```bash
for f in <workdir>/slides/*.html; do
  python3 <lib>/carrossel/qa_lint.py "$f" --json || echo "FALHOU: $f"
done
```

`qa_lint.py` lê CSS de 3 fontes: bloco `<style>` inline no HTML gerado, `base.css` linkado via
`<link>` e atributos `style=` inline em cada elemento. Por isso os checks de contraste funcionam
de verdade no HTML real — não são mais inertes. Códigos que ele detecta e o que cada um quer
dizer / como corrigir:

| Código | O que pega | Auto-correção |
|---|---|---|
| `CONTRAST_INK_BG` | contraste `--text`/`--bg` < 4.5 (WCAG AA) | escurecer bg (mais scrim) ou clarear texto |
| `CONTRAST_ACCENT_BG` | contraste `--accent`/`--bg` < 3.0 | não mexer no `--accent` canônico `#C4714A`; aumentar densidade do `.scrim` na capa/CTA |
| `BODY_TOO_SMALL` | `.body` < 24px | subir pra ≥24px |
| `OBJECTFIT_CONTAIN_BG` | `object-fit:contain` + `background` no mesmo bloco (bordas escuras na imagem) | trocar pra `cover` ou cortar a imagem antes |
| `HEADLINE_NO_ACCENT` | headline sem `<span class="em">` (≥1 palavra accent — regra do MANIFESTO) | adicionar `{palavra}` na headline do json |
| `HEADLINE_TOO_SMALL` | headline inline com `font-size` < 76px | subir `hsize` no json |

**Regra dura:** lint precisa sair `exit 0` em **todos** os slides antes de chamar o revisor visual.
Defeito de lint é mais barato de pegar que de olho — resolve primeiro. `HEADLINE_NO_ACCENT` e
contraste são os mais recorrentes: `HEADLINE_NO_ACCENT` aparece quando o `{x}` do json foi omitido
ou mal fechado; contraste aparece quando a foto-fundo clareia o bg além do que o `.scrim` cobre —
aumentar a densidade do scrim ou trocar a foto resolve.

**Escala modular × lint:** a escala `24/32/43/57/76/101/135` é referência de design (no MANIFESTO),
mas o lint **não reprova por ela**. Designs aprovados usam 96/104/112px; a régua real é o gosto
validado. O lint só garante que a headline não fique pequena (≥76px via `HEADLINE_TOO_SMALL`).

### Etapa 4 — Revisor visual (o coração do loop)

Aqui entra o **agente revisor**. Ele NÃO lê HTML/CSS — lê **PIXEL**. Faz `Read` de cada
`slides/NN.png` (a tool renderiza a imagem visualmente) e compara com o MANIFESTO + o checklist
abaixo. Retorna **só JSON**, formato `[{ "slide": N, "defeitos": [ ... ] }]`. Slide sem defeito não
aparece (ou aparece com `"defeitos": []`). Array vazio `[]` = carrossel aprovado.

Por que um agente e não só o lint: os defeitos que mais quebram carrossel **não são detectáveis no
texto** — são sobreposição, oclusão, proporção, crop, leitura de acento. Só olhando o PNG renderizado.

### Etapa 5 — Auto-correção

Pra cada defeito do JSON do revisor, aplicar a correção **na fonte** (`carrossel.json` ou regenerar o
asset), NUNCA editando o HTML/PNG direto (são gerados — seriam sobrescritos no próximo render). Mapa
defeito → ação na tabela "Checklist do revisor" abaixo. Depois de corrigir, **voltar à etapa 1** e
rodar o ciclo inteiro de novo. Repetir até o revisor devolver `[]`. Limite de segurança: se após **5
iterações** ainda houver defeito, parar e reportar ao user o que não convergiu (não entrar em loop
infinito, não baixar a régua).

---

## Checklist do revisor (defeitos REAIS, recorrentes nesta lib)

Cada item: **o que procurar no PNG**, **por que é defeito** (referência ao MANIFESTO), **como
auto-corrigir** na fonte. Esta é a lista de inspeção que o agente revisor aplica slide a slide. Todos
foram defeitos que de fato apareceram produzindo carrosséis com esta lib.

1. **Anotação handwritten sobre texto/borda** — `.note` (Caveat, accent) caindo POR CIMA de headline,
   sub, screenshot legível, ou colado na borda do slide. MANIFESTO §8: "Labels handwritten acima ou ao
   lado do alvo, **nunca sobre texto legível**"; anotação na borda externa do herói apontando pra
   dentro. *Corrigir:* reposicionar a `.note` (ajustar top/left no slide via override no json), ou
   remover se não tem espaço. Não pode tocar texto.

2. **Personagem/`compo` sobre o subtítulo** — o composto da capa (`compo.left`/`left2`, personagem +
   livros) subindo e cobrindo o `.sub` ou a headline. No `_cover` o `compo` é `position:absolute;
   bottom:118px` e a `.sub` tem `max-width:26ch` — se a headline+sub forem longas, o personagem invade.
   MANIFESTO §2: herói "vaza da borda" mas NÃO compete com o texto; §10 capa "1 palavra accent,
   centralizada, 2-5 linhas". *Corrigir:* encurtar sub/headline no json (menos linhas), ou reduzir a
   altura do personagem (`compo.left` height), ou subir o `bottom` do compo. O texto sempre vence.

3. **Palavra accent menor que o display** — a `<span class="em">` (serif itálico, a palavra colorida)
   parecendo MENOR que o resto da headline Nofex. No `base.css` o `.em` já tem `font-size:1.18em` de
   propósito (serif itálico precisa ser maior pra ter o mesmo peso óptico). Se no PNG ela ainda parece
   pequena/encolhida, ou se a quebra de linha isolou a palavra accent num canto, é defeito. MANIFESTO
   §3: "exatamente 1 palavra/grupo accent por headline", e o accent é o ponto de pouso do olho — tem
   que dominar. *Corrigir:* escolher palavra accent mais curta/forte no json (`{palavra}`), ou ajustar
   `hsize` pra a headline caber sem isolar o accent. Nunca duas palavras accent.

4. **Ícone/logo pequeno demais** — `meta.icon_top` (logo da marca do projeto) ou `compo.right_icon` minúsculo,
   perdido. MANIFESTO §7: asterisco do app "~120–130px (~11–12% da largura)", centralizado no topo.
   *Corrigir:* o template fixa `icon_top` em 84px (cover) / 104px (cta) e o `right_icon` em 210px num
   chip de 300px — se o PNG mostra logo apagado, normalmente é **asset com resolução baixa ou muito
   padding transparente**; regenerar o PNG do logo (recortar o padding, exportar maior) em vez de
   esticar no CSS.

5. **Screenshot/livro escondido ou cortado** — `.shot` (hero do content) ou as capas de livro do
   `compo` saindo pelo clip de 1080×1350, ou cobertas por outro elemento, ou com `border-radius`/sombra
   comidos pela borda. MANIFESTO §5: herói ocupa "~38-48% da altura", flutua sobre o fundo com
   box-shadow densa — precisa estar INTEIRO e respirando. Lembrar que `render.mjs` corta por clip fixo:
   o que vaza some. *Corrigir:* reduzir `hsize`/sub pra abrir espaço vertical (o `.spacer` do `_content`
   distribui o respiro), trocar a imagem por um crop que caiba, ou reduzir a altura do asset do compo.

6. **Headline sem accent** — nenhuma `<span class="em">` na headline. Isto o `qa_lint.py` já pega
   (`HEADLINE_NO_ACCENT`), mas o revisor confirma no PNG que a palavra colorida REALMENTE aparece (um
   `{}` mal fechado no json gera `em` que não renderiza). MANIFESTO §3 regra de ouro. *Corrigir:*
   garantir exatamente um par `{palavra}` na headline do json.

7. **Texto cortado** — headline/sub/quote estourando a largura (`--pad-x:64px` de cada lado, conteúdo
   `1080 - 128 = 952px`) ou a altura, e sendo cortado pelo `overflow:hidden` do `.slide` + clip do
   render. É o defeito mais sorrateiro porque o HTML "tá certo", só não cabe. *Corrigir:* reduzir
   `hsize`, encurtar a frase, ou aumentar quebras — sempre no json. Nunca espremer reduzindo padding
   (quebra o eixo, ver item 8).

8. **Eixo de coluna inconsistente** — headline, kicker, sub, herói e footer NÃO começando no mesmo
   `--pad-x`. MANIFESTO §1 (a regra CRÍTICA): "a esquerda é sagrada", tudo no mesmo `margin-left`. O
   `base.css` resolve isso via `--pad-x:64px` no `.slide` (o MANIFESTO observa 48px nos virais; **nossa
   lib usa 64px** — é o valor canônico daqui, não mudar). Se no PNG algum bloco está desalinhado,
   geralmente é override inline no json forçando margin/padding diferente. *Corrigir:* remover o
   override; deixar o eixo vir do `--pad-x`. (Nota: capa e CTA são `text-align:left`/`center`
   intencionalmente — alinhamento centralizado na capa/CTA é do MANIFESTO §10, não é defeito.)

9. **Contraste fraco** — texto/accent sumindo no fundo, principalmente em capa/CTA com `bgphoto`. O
   `qa_lint.py` checa contraste das VARIÁVEIS, mas sobre foto real o contraste efetivo depende da
   imagem. MANIFESTO §5G: foto-fundo com overlay `rgba(0,0,0,0.55–0.72)` / `brightness 0.35–0.45`. O
   `base.css` `.scrim` é `linear-gradient(rgba(8,6,5,0.62)→0.86)`. Se no PNG o texto ainda compete com a
   foto, *corrigir:* escolher/regenerar uma `bg_photo` mais escura, ou aumentar a densidade do scrim, OU
   trocar a foto por um crop com zona escura onde o texto pousa. Nunca clarear o texto abaixo do branco.

10. **Footer/handle ausente** — `.footer` (handle Crankdat centralizado) ou `.swipe` faltando, cortado
    na base, ou empurrado pra fora pelo clip. MANIFESTO §9: footer "pixel-perfect idêntico em TODOS os
    slides" — é o motif mais consistente, sumir nele quebra a coesão. CTA usa `swipe=False` de
    propósito (último slide não tem "arrasta →"). *Corrigir:* se sumiu por overflow, reduzir o conteúdo
    acima (item 5/7) pra o footer (`bottom:48px`) caber dentro dos 1350px.

11. **PT-BR / acentos** — texto em inglês onde devia ser PT-BR, ou acento clipado/faltando
    (Nofex/Crankdat às vezes clipam acentos no topo — `base.css` já dá `padding-top:0.04em` na
    `.headline`). O revisor LÊ o texto do PNG e confere: idioma PT-BR, "não" com til, "ã/õ/ç/é/ê"
    renderizando inteiros (sem corte no topo do glifo). MANIFESTO + voz do projeto: conteúdo no idioma
    do projeto (PT-BR no default), sem hardcode de pessoa. *Corrigir:* texto errado → editar o json; acento clipado → garantir que a headline usa a
    classe `.headline` (que tem o `padding-top`), ou subir levemente o `padding-top` via override só
    naquele slide se o glifo específico ainda cortar.

12. **Herói (`figure`) sobre o texto** — a figura-herói da capa (mascote/personagem/objeto, campo
    `figure`) subindo e cobrindo a `.headline` ou o `.sub`. É o mesmo pecado do item 2, mas pro `figure`
    (não o `compo`). *Corrigir:* deslocar lateralmente com `figure_x` (negativo=esquerda, +=direita)
    pra fugir do texto; descer com `figure_bottom` menor; ou reduzir `figure_h`. **O texto sempre
    vence** — nunca deixar o herói tampar palavra/acento legível.

13. **Buraco na capa depois de deslocar o herói** — quando o `figure` foi pro lado (`figure_x`) pra
    largar o texto, sobra um **espaço vazio** do outro lado. Capa boa é densa e equilibrada, não tem
    buraco. *Corrigir:* preencher com `aux` (2ª imagem — prova que reforça a headline; repertório em
    `forge-screen.md` §8). **Defeito especial:** QUAL imagem entra é decisão criativa — o loop deve
    **parar e oferecer ao user** preencher o vazio, com **2-3 sugestões concretas** de device (perfil
    viralizando, pasta secreta/censurada, gráfico de crescimento, telas do produto…) + a opção de
    enviar como está. Auto-corrige posição/tamanho (`aux_x`/`aux_w`/`aux_bottom`/`aux_rot`); o
    **conteúdo** da 2ª imagem, pergunta — não inventa no escuro.

14. **Contador sobre a logo** — `snum` (NN/NN) colidindo com `icon_top`/logo no mesmo canto. Na capa
    isto não acontece (a capa não leva contador — `templates.py` removeu o `snum` do `_cover`), mas em
    qualquer slide onde contador e logo caiam no mesmo canto é defeito. *Corrigir:* tirar o contador
    daquele slide ou reposicionar a logo.

Defeitos extras a varrer sempre que o PNG mostrar: **slide só-texto sem visual** (MANIFESTO §5/§10: todo
content tem UM herói — se um content não tem `hero` nem motivo, é buraco), **duas palavras accent na
mesma headline** (proibido, §3), **mascote/compo competindo com a headline** (§6 "não saturar"),
**proporção do herói fora de 35-48% da altura** (§2: buraco ou esmagamento).

---

## Prompt-modelo do agente revisor

Despachar como subagente (ou inline) com este prompt. Ele recebe os caminhos dos PNG, faz `Read` de
cada um, e devolve **só** o JSON. Sem prosa.

```
Você é o REVISOR VISUAL de carrosséis. Tarefa: olhar cada PNG renderizado e listar defeitos
comparando com o MANIFESTO de diagramação. NÃO leia HTML/CSS — julgue só o PIXEL do PNG.

Faça Read de cada arquivo:
  <workdir>/slides/01.png
  <workdir>/slides/02.png
  ... (todos)

Referência de verdade: ${CLAUDE_PLUGIN_ROOT}/references/carrossel-lab/MANIFESTO-DIAGRAMACAO.md
(eixo de coluna sagrado à esquerda; herói 35-48% da altura; EXATAMENTE 1 palavra accent por
headline; footer idêntico em todos; capa/CTA com foto escurecida; CTA = headline maior; PT-BR).

Para CADA slide, verifique e reporte qualquer um destes defeitos (use exatamente estes códigos):
  - NOTE_OVER_TEXT      anotação handwritten sobre texto/borda
  - COMPO_OVER_SUB      personagem/composto cobrindo subtítulo ou headline
  - ACCENT_TOO_SMALL    palavra accent menor/encolhida vs a display
  - ICON_TOO_SMALL      ícone/logo pequeno demais ou apagado
  - HERO_HIDDEN_CROPPED screenshot/livro escondido, cortado pelo clip, ou comido na borda
  - HEADLINE_NO_ACCENT  headline sem a palavra colorida visível
  - TEXT_CLIPPED        texto cortado (largura/altura)
  - AXIS_INCONSISTENT   eixo de coluna desalinhado entre blocos
  - LOW_CONTRAST        texto/accent sumindo no fundo (esp. sobre foto)
  - FOOTER_MISSING      footer/handle ausente ou cortado (CTA legitimamente sem swipe)
  - LANG_OR_ACCENT      texto não-PT-BR ou acento clipado/faltando (ã õ ç é ê não)
  - NO_VISUAL           slide de conteúdo sem nenhum elemento herói (buraco)
  - DOUBLE_ACCENT       duas+ palavras accent na mesma headline
  - HERO_PROPORTION     herói fora de ~35-48% da altura (buraco ou esmagado)
  - FIGURE_OVER_TEXT    herói da capa (figure) cobrindo headline/sub — deslocar via figure_x
  - COVER_EMPTY_GAP     capa com vazio após o herói sair do centro — PARAR e oferecer 2ª imagem (aux) ao user
  - COUNTER_OVER_LOGO   contador (snum) colidindo com a logo no mesmo canto
  - CRAMPED_LAYOUT      headline e sub coladas / blocos amontoados — falta respiro (subir margem ou reduzir tamanho)
  - HERO_TOO_SMALL      hero/imagem pequena perdida no slide — devia encher mais (subir hsize/quote_size, hero mais alto, ou hero_w)

Para cada defeito inclua: code, e uma "obs" curta dizendo ONDE no slide e a correção sugerida
na FONTE (carrossel.json/asset), nunca no HTML. **Exceção COVER_EMPTY_GAP:** não auto-preencher —
sinalizar pro controlador parar e perguntar ao user qual 2ª imagem entra (com sugestões).

Responda SÓ com JSON, sem markdown, sem cercas:
[
  {"slide": 1, "defeitos": [
     {"code":"COMPO_OVER_SUB","obs":"personagem cobre a 2a linha do sub; encurtar sub ou subir bottom do compo"}
  ]},
  {"slide": 3, "defeitos": []}
]
Slides perfeitos: "defeitos": []. Carrossel impecável: todos com [] (ou array geral vazio).
```

---

## Critério de saída (gate final, sem exceção)

Só apresentar ao user quando **as três condições** baterem:

1. `render.mjs` gerou um PNG pra **cada** slide (nenhum faltando).
2. `qa_lint.py` saiu **exit 0** em **todos** os HTML.
3. O revisor visual devolveu **zero defeitos** (todos `[]`).

Enquanto qualquer uma falhar: auto-corrigir na fonte → re-render → re-checar. Nunca declarar "pronto"
sem ter olhado os PNGs finais (princípio 1 do CLAUDE.md: verificar antes de declarar pronto). Se
travar após 5 iterações, reportar honestamente o defeito residual ao user em vez de baixar a régua.
