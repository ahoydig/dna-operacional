# forge-screen — forjar telas de UI como HTML→PNG (réplica fiel)

Guia pra **forjar uma tela de produto** (ex: Claude.ai, ChatGPT, qualquer SaaS) em PT-BR
como uma imagem PNG limpa, usada depois como `hero`/`.shot` dentro de um slide do carrossel.

Não é screenshot da tela real. É uma **réplica em HTML** que imita a UI pixel a pixel,
renderizada via Playwright capturando **só o elemento da tela** (não a viewport inteira).

Use quando:
- A tela real está em inglês e você quer PT-BR.
- A tela real tem dados pessoais / ruído (sidebar, histórico, avatar) que poluem.
- Você precisa de um estado específico que é chato de reproduzir ao vivo (campo focado, erro, loading).
- Você quer um mock didático de "como seria" sem ter o produto na mão.

> Distinção importante de classes: `.shot` no `base.css` é o **wrapper de screenshot dentro do slide**
> (borda 14px + sombra). A tela forjada deste guia é capturada **antes** disso, como PNG cru, e só
> depois é injetada num slide via `hero` (o template `_content` envolve em `.hero > img.shot`).
> Aqui a gente captura o **elemento `.screen`** que a gente mesmo define no HTML de forja.

---

## 1. Princípio

**O HTML imita a UI real; o render captura só o elemento da tela.**

Três camadas:

1. **HTML/CSS de forja** — um único arquivo que desenha a tela alvo com as specs reais do produto
   (cores, raios de canto, fonte, espaçamento, sombra). Tudo dentro de um container `.screen` com
   largura/altura fixas em px.
2. **Render headless** — Playwright abre o arquivo, espera as fontes, e tira screenshot **do elemento
   `.screen`** (`locator.screenshot()`), não da página inteira. Sai um PNG justo, sem margem, com
   fundo transparente onde você quiser.
3. **Consumo no carrossel** — o PNG vira `hero` de um slide `content` no `carrossel.json`
   (ver `schema.md`). O `templates.py` resolve o path com `asset()` e envolve em `.shot`.

Por que capturar o elemento e não a viewport: a tela tem dimensão própria (ex: 920×620), não 1080×1350.
Capturar a viewport força você a centralizar/recortar depois. `locator.screenshot()` corta exatamente
no `border-box` do `.screen`, então o PNG já sai no tamanho certo, pronto pra colar.

---

## 2. Extrair as specs da tela alvo (QUALQUER produto)

Pra forjar qualquer tela (app de dieta, CRM, portal jurídico, e-commerce, dashboard, agenda...), peça
um **print / brand page do alvo real** e leia: cor de fundo, accent da marca, raio de canto, fonte,
bordas, estados (repouso/focado/erro). A tabela abaixo é **só um EXEMPLO** (Claude.ai) de como anotar
essas specs — **não é a referência da skill**, é o formato. Troque pelos valores do SEU alvo.

| Token | Valor | Onde |
|---|---|---|
| Fundo do modal/card | `#FFFFFF` (claro) ou `#2B2A27` (dark) | superfície principal |
| Canto do card | `border-radius: 16px` | modal, cards, painéis |
| Accent (cor da marca Claude) | `#D97757` | botão primário, foco, links |
| Fonte | `Inter` (UI) / `Styrene`-like; use **Inter** como proxy fiel | todo texto |
| Texto principal | `#1F1E1D` no claro / `#F5F4EF` no dark | corpo |
| Texto secundário | `#6B6B6B` / `#A8A29E` | placeholder, legendas |
| Borda neutra | `#E5E3DF` 1px | divisores, inputs em repouso |
| **Campo destacado (focado)** | borda `3px solid #D97757` + leve `box-shadow` accent | textarea/input ativo |
| Botão primário | fundo `#D97757`, texto branco, raio `10px`, padding `12px 18px` | CTA da tela |
| Sombra do card | `0 12px 40px rgba(0,0,0,0.12)` (claro) | flutuação do modal |

> Accent do produto (`#D97757`) **≠** accent do carrossel (`#C4714A` em `base.css`). São perto, mas
> não iguais — a tela usa a cor real do **produto**, não a do nosso template. Não troque um pelo outro:
> a réplica tem que parecer o produto, não o nosso carrossel.

---

## 3. Estrutura do arquivo de forja

Um HTML autossuficiente. Fontes via `@import` do Google Fonts (Inter). Body transparente
(ou com a cor de fundo do app, se a captura precisar de fundo). Container `.screen` com dimensão fixa.

```html
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*{margin:0;padding:0;box-sizing:border-box;}
html,body{background:transparent;}              /* transparente: PNG sai sem fundo */
body{font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased;
     padding:60px;}                             /* respiro pra sombra não cortar na captura */

/* ===== a tela forjada ===== */
.screen{
  width:920px; background:#FFFFFF; border-radius:16px;
  box-shadow:0 12px 40px rgba(0,0,0,0.12);
  padding:36px 40px 40px; color:#1F1E1D;
}

.brandrow{display:flex;align-items:center;gap:12px;margin-bottom:24px;}
.brandrow .logo{width:34px;height:34px;border-radius:9px;background:#D97757;
  display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;}
.brandrow .name{font-size:20px;font-weight:600;letter-spacing:-0.01em;}

.label{font-size:15px;font-weight:600;color:#6B6B6B;margin-bottom:10px;}

/* campo DESTACADO: borda accent 3px (estado focado) */
.field{
  width:100%; min-height:120px; border-radius:12px;
  border:3px solid #D97757;                     /* <- destaque accent */
  box-shadow:0 0 0 4px rgba(217,119,87,0.12);   /* halo de foco */
  padding:16px 18px; font-size:18px; line-height:1.5; color:#1F1E1D;
  background:#FFFFFF;
}
.field .caret{display:inline-block;width:2px;height:22px;background:#D97757;
  vertical-align:-4px;margin-left:1px;}         /* cursor fake, opcional */

.row{display:flex;align-items:center;justify-content:space-between;margin-top:22px;}
.hint{font-size:14px;color:#A8A29E;}

/* botão primário: fundo accent */
.btn{
  background:#D97757; color:#FFFFFF; border:none;
  border-radius:10px; padding:12px 22px;
  font-family:'Inter';font-size:16px;font-weight:600;cursor:default;
}
</style>
</head>
<body>
  <div class="screen">
    <div class="brandrow">
      <div class="logo">✶</div>
      <div class="name">Claude</div>
    </div>

    <div class="label">Como posso ajudar hoje?</div>

    <div class="field">
      Escreve um plano de conteúdo de 7 dias pro meu Instagram<span class="caret"></span>
    </div>

    <div class="row">
      <span class="hint">Claude pode cometer erros. Confira informações importantes.</span>
      <button class="btn">Enviar</button>
    </div>
  </div>
</body>
</html>
```

Notas de fidelidade:
- `padding:60px` no `body` é **respiro pra sombra**. Sem isso, `box-shadow` é cortada na borda do
  elemento. Como a captura é do `.screen` (não do body), a sombra **vaza** pra fora do border-box —
  o respiro garante que ela apareça inteira no PNG. (Ver §4 sobre incluir/excluir a sombra.)
- O glifo `✶` no `.logo` é placeholder. Pra logo real, baixe o PNG/SVG oficial e use `<img>` — não
  desenhe o logo "de cabeça", isso fabrica a marca.
- `.field` aqui está no estado **focado** (borda 3px accent + halo). Pra estado em repouso, troque por
  `border:1px solid #E5E3DF` e remova o `box-shadow`.

---

## 4. Comando de render (Playwright, captura do elemento, @2x)

Salve como `forge_shot.mjs` ao lado do HTML, ou rode inline. Diferença-chave vs `render.mjs` do
carrossel: lá a captura usa `clip` da viewport 1080×1350; **aqui usamos `locator('.screen').screenshot()`**
pra cortar exatamente no elemento, em `deviceScaleFactor: 2` (retina, nítido).

```js
// forge_shot.mjs — uso: node forge_shot.mjs <tela.html> [out.png]
import { chromium } from 'playwright';
import path from 'path';

const inp = process.argv[2];
const out = process.argv[3] || inp.replace(/\.html$/, '.png');

const b = await chromium.launch();
const p = await b.newPage({ deviceScaleFactor: 2 });   // @2x retina
await p.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
try { await p.evaluate(() => document.fonts.ready); } catch {}
await p.waitForTimeout(1200);                            // assenta fonte/layout

const el = p.locator('.screen');                         // captura SÓ o elemento
await el.screenshot({ path: out, omitBackground: true });// fundo transparente

console.log('forjado', out);
await b.close();
```

Flags que importam:
- `deviceScaleFactor: 2` → PNG sai com o dobro da resolução (ex: `.screen` de 920px vira 1840px de
  largura). Nítido quando reduzido dentro do slide.
- `locator('.screen').screenshot()` → corta no **border-box** do elemento, não na viewport.
- `omitBackground: true` → respeita `background:transparent` do body → PNG com **alpha**. Útil pra
  colar a tela sobre qualquer fundo de slide. Se quiser fundo sólido, remova essa flag e dê
  `background` no body.
- **Sombra:** `locator.screenshot()` captura o border-box do `.screen`, então a `box-shadow` (que vive
  fora do border-box) é **cortada**. Se você QUER a sombra no PNG, capture um wrapper que contém o
  `.screen` + o respiro: troque o locator pra `'.shotwrap'` envolvendo `.screen` com o `padding:60px`,
  ou deixe a sombra pro `.shot` do carrossel (o `base.css` já dá `box-shadow` no `.shot`). Em geral:
  **deixe a sombra pro `.shot`** e capture a tela limpa com `omitBackground`.

Dependência Playwright: este `lib/carrossel/` não tem `node_modules` próprio. Linke o do projeto
`propostas` (mesma estratégia do `render.mjs`):

```bash
# playwright no dir do script: instale (genérico) ou linke um node_modules que tenha
npm i playwright   # OU atalho da máquina do Flávio:
# ln -sf ~/Documents/projects/propostas/node_modules <lib>/carrossel/node_modules
```

Depois:

```bash
node /Users/flavioahoy/Documents/projects/dna-operacional/plugins/dna-operacional/lib/carrossel/forge_shot.mjs \
     /caminho/tela-claude.html  /caminho/assets/tela-claude.png
```

---

## 5. Plugar no carrossel

O PNG forjado entra como `hero` de um slide `content` no `carrossel.json` (ver `schema.md`):

```json
{
  "tipo": "content",
  "kicker": "PASSO 1",
  "headline": "Escreve em {português}",
  "sub": "A mesma tela do Claude — só que falando a sua {língua}.",
  "hero": "assets/tela-claude.png"
}
```

O `templates.py` (`_content`) resolve `assets/tela-claude.png` via `asset()` → `../assets/...`
(o HTML do slide vive em `slides/`) e envolve em `<div class="hero"><img class="shot" ...></div>`.
A borda 14px + sombra vêm do `.shot` no `base.css` — por isso a tela forjada deve sair **limpa**
(sem sombra própria, fundo transparente).

Renderize o carrossel inteiro normalmente:

```bash
python3 render_carrossel.py carrossel.json out_dir   # gera slides/*.html
node render.mjs out_dir/slides                        # gera *.png 1080x1350 @2x
```

---

## 6. Forjar o SO/app na versão ATUAL (não a velha)

Ao forjar tela de sistema operacional ou app conhecido (macOS Finder, iOS, Instagram, WhatsApp…),
replique o **design atual**, não uma versão antiga. Erro recorrente: usar **emoji** pra ícone de
sistema — o emoji renderiza o asset **velho/skeuomórfico** (ex: `📁` = a pasta cinza-azul antiga do
macOS, não a flat de hoje). Para parecer um print real e recente, **desenhe o ícone em SVG** com as
specs atuais, ou use o PNG oficial. Antes de forjar, peça uma referência real ao user ("manda um print
de como tá hoje no teu Mac/celular") — a UI muda e você pode estar com o modelo defasado.

### Pasta do macOS atual (Big Sur+) — referência

Pasta moderna = **azul ciano vivo**, flap frontal com uma **linha branca de brilho no topo**, cantos
arredondados, flat. NÃO o emoji `📁`. SVG fiel (front-facing):

```html
<svg viewBox="0 0 204 160" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="ff" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5CC8FA"/><stop offset="1" stop-color="#41BAF4"/></linearGradient></defs>
  <!-- back + aba -->
  <path d="M16 32 h58 a10 10 0 0 1 7 3 l10 10 a6 6 0 0 0 4.2 1.8 H186 a15 15 0 0 1 15 15 V139 a15 15 0 0 1 -15 15 H16 a15 15 0 0 1 -15 -15 V47 a15 15 0 0 1 15 -15 z" fill="#2BA7E8"/>
  <!-- flap frontal -->
  <rect x="5" y="64" width="194" height="90" rx="15" fill="url(#ff)"/>
  <!-- linha branca de brilho no topo do flap (a assinatura do ícone atual) -->
  <rect x="22" y="68" width="150" height="5" rx="2.5" fill="#EEFAFF" opacity="0.92"/>
</svg>
```

Janela do Finder: chrome com os 3 semáforos (`#ff5f57`/`#febc2e`/`#28c840`), título centralizado,
corpo branco (modo claro — **pop** sobre capa escura) ou `#1e1e1e` (modo escuro, se quiser bater 1:1
com um print real). Badge de cadeado moderno (não emoji dourado): círculo escuro `#1d1d1f` + cadeado
branco em SVG. Capture o elemento `.win` com `omitBackground:true` (PNG transparente, sombra inclusa
pelo `padding` do body).

## 7. Censura / borrão pixelado (efeito "secreto")

Pra esconder nomes/dados e provocar curiosidade (carrossel de "X secretos"), **não** use tarja preta
chapada — use um **mosaico pixelado** (parece texto borrado/redigido de verdade). Técnica: um grid de
células pequenas (~7px) com tons de cinza aleatórios.

```js
const PAL = ['#161616','#2b2b2b','#474747','#6c6c6c','#969696','#bdbdbd'];
function pixel(w){                                    // w = largura aprox. do "texto" censurado
  const cell=7, cols=Math.round(w/cell), rows=4, n=cols*rows;
  let cells=''; for(let i=0;i<n;i++) cells+=`<i style="background:${PAL[Math.floor(Math.random()*PAL.length)]}"></i>`;
  return `<div class="pix" style="width:${cols*cell}px;grid-template-columns:repeat(${cols},${cell}px);grid-auto-rows:${cell}px">${cells}</div>`;
}
// CSS: .pix{display:grid;gap:0;border-radius:3px;overflow:hidden} .pix i{width:7px;height:7px;display:block}
```

Varie a largura por item (nomes de tamanhos diferentes = mais real). O `gerar-imagem` também pode
pixelar/censurar uma foto, mas pro caso de nomes/labels o mosaico HTML é mais limpo e controlável.

## 8. Repertório de herói/prova pra capa (NUNCA estreitar num só)

A capa pede uma imagem-herói forte (campo `figure`/`aux` do `cover`, ver `schema.md`). Há um
**repertório** — ao propor a capa, abra TODAS as opções relevantes ao tema com exemplos concretos,
nunca ofereça só uma (ex: só "mascote"). Devices que esta lib sabe forjar/gerar:

- **Perfil de rede social viralizando** (forjado) — print de um perfil com **seguidores explodindo**
  (seta ↑, "+52k essa semana", gráfico subindo). Prova de "viral". Forje em HTML (header do IG/X) ou
  gere via `gerar-imagem`. Números: redondos/ilustrativos, nunca métrica inventada que pareça real (§9).
- **Pasta/arquivos secretos censurados** (forjado) — Finder com N itens, nomes em **mosaico pixelado**
  + cadeado (§6/§7). Ótimo pra tema "X secretos/escondidos".
- **Telas reais do produto** (forjado, §1-5) — mosaico de telas do app em PT-BR, prova de "o trabalho".
- **Enxurrada de notificações** (forjado) — pilha de toasts de curtida/seguidor/comentário subindo.
- **Gráfico/curva de crescimento** (forjado ou gerado) — engajamento/receita disparando.
- **Mascote/personagem de marca** (gerado, `gerar-imagem -i ref`) — herói recorrente da marca. Gere
  **fiel à referência** (não infantilizar, mesmo estilo do mascote). Combina com qualquer device acima
  (ex: mascote + perfil explodindo; mascote + pasta secreta). **NÃO é o default:** só entra quando a
  marca do projeto JÁ tem um personagem. A skill é genérica/multi-pessoa — priorize sempre os devices
  **agnósticos de marca** acima (perfil, telas, notificações, gráfico, cards), que servem pra qualquer
  pessoa/nicho, e ofereça o mascote como **mais uma** opção, nunca como a principal.
- **CTA com preview do brinde** — no slide `cta`, em vez de só texto, forjar um **mockup do que a pessoa vai receber** (o "passo a passo", o PDF, o guia) inclinado no centro, com a headline em cima e "Comenta TOKEN" embaixo. Mostra o valor concreto do que ela ganha ao comentar. (Padrão de criadores tipo @noevarner.)

**Forje alto o suficiente pra ENCHER o slide.** Erro recorrente: tela forjada curta (wide) que, com `width:100%` no `.shot`, fica baixa e some no meio do slide. Pra preencher, faça a tela mais **alta** (mais conteúdo: mais mensagens no chat, mais linhas, mais itens) — a altura do PNG é o que dá presença. Ex: num chat, somar mensagens ("Você tem horário essa semana?", "Olá, tem alguém aí???", "👀") deixa a conversa mais alta e o slide mais cheio.

Combos costumam bater mais forte que um device só: **2 imagens** na capa (`figure` herói +
`aux` prova), equilibrando os dois lados (ver regra das 2 imagens em `schema.md`). Ao propor a capa,
liste devices **agnósticos** primeiro; mascote/marca-específico só se o projeto tiver.

## 9. Regra de honestidade

A réplica reproduz a **forma** da UI, não fabrica **fato**.

- **Forma é livre:** cor, raio de canto, fonte, layout, estado (focado/erro/loading), texto em PT-BR.
  Isso é tradução/encenação fiel da interface — ok.
- **Fato não se inventa:**
  - **Logos** → use o arquivo oficial (PNG/SVG baixado). Nunca desenhe a marca "de cabeça".
  - **Números** (contadores, métricas, preços, "1.234 usuários") → ou são **reais** (você tem a fonte),
    ou são **claramente ilustrativos** (use valores redondos óbvios tipo `1.234`, `R$ 99`, ou rotule
    "exemplo"). Nunca um número específico inventado que pareça medido.
  - **Citações/respostas do produto** → não coloque na boca do produto/app forjado (assistente, CRM,
    app de agenda, e-commerce, IA...) uma resposta/feature que ele não deu/não tem, como se fosse real.
    Se for exemplo, que fique óbvio que é exemplo.
  - **UI que não existe** → não invente botão/feature que o produto não tem e venda como real. Se for
    conceito/mock, diga que é mock.
- **Teste do print:** se alguém der screenshot da tela forjada e disser "olha, o app faz X" — isso
  está correto? Se a forma é fiel mas o fato é inventado, você criou desinformação. Recue pro ilustrativo.

Resumo: imitar a **casca** da UI = honesto. Colocar **conteúdo falso** dentro dela como se fosse real =
fabricação. Mantenha a casca fiel e o recheio verdadeiro (ou marcado como exemplo).
