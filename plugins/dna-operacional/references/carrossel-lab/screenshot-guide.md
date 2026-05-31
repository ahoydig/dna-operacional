# Guia de Captura de Screenshots

Estratégias para capturar screenshots de diferentes fontes via Playwright e embutir nos slides do carrossel.

---

## Fluxo geral

1. Navegar até a URL via `browser_navigate`
2. Lidar com popups/overlays (fechar login walls, cookie banners, etc.)
3. Identificar o elemento a capturar (nem sempre é a página toda)
4. Capturar screenshot do elemento específico via `browser_take_screenshot` com `ref` e `element`
5. Salvar localmente
6. Embutir no HTML do slide como `<img>` com estilo padronizado

---

## Por fonte

### Twitter/X

**Desafio:** Login wall frequente, conteúdo em inglês precisa tradução.

**Estratégia (com cookies de auth do usuário):**
1. Definir cookies via `context.addCookies()` (auth_token, ct0, twid)
2. Definir `lang: 'pt'` nos cookies pra interface em português
3. Navegar pra URL do tweet com viewport estreito (650-700px) pra esconder sidebar
4. Esconder sidebar, bottom bar e nav:
```javascript
await page.evaluate(() => {
  const sidebar = document.querySelector('[data-testid="sidebarColumn"]');
  if (sidebar) sidebar.style.display = 'none';
  const banner = document.querySelector('[data-testid="BottomBar"]');
  if (banner) banner.style.display = 'none';
  const nav = document.querySelector('header[role="banner"]');
  if (nav) nav.style.display = 'none';
});
```
5. **TRADUZIR o texto do tweet pra PT-BR** via DOM:
```javascript
await page.evaluate(() => {
  const tweetText = document.querySelector('[data-testid="tweetText"]');
  if (tweetText) {
    tweetText.innerHTML = 'TEXTO TRADUZIDO EM PORTUGUÊS';
  }
});
```
6. Capturar o `article` isolado: `await page.locator('article').first().screenshot()`

**IMPORTANTE:** Google Translate NÃO funciona com X.com — o site quebra. Sempre usar manipulação de DOM.

**Sem cookies:** Pedir ao usuário o `auth_token` (DevTools → Application → Cookies → x.com → auth_token).

---

### Instagram Post

**Desafio:** Popup "Log in to see more" bloqueia a visualização.

**Estratégia:**
1. Navegar para a URL do post
2. Fechar popup de login (buscar botão "Close")
3. Capturar screenshot da imagem do post (não da página toda)
4. Se for carrossel, navegar pelos slides e capturar o desejado

---

### Instagram Reel

**Desafio:** Conteúdo de vídeo, não imagem estática.

**Estratégia:**
1. Navegar para a URL do Reel
2. Fechar popup de login
3. Capturar thumbnail/frame do vídeo
4. Extrair texto da legenda do Reel para usar no conteúdo textual do carrossel
5. A legenda vira matéria-prima para os slides

---

### Notícia / Artigo

**Desafio:** Layouts variados, paywalls, banners de cookie.

**Estratégia:**
1. Navegar para a URL
2. Fechar cookie banners (buscar botões "Accept", "Aceitar", "OK", "Close")
3. Capturar manchete + imagem principal (geralmente o topo da página)
4. Usar `fullPage: false` para pegar só o viewport
5. Se precisar de trecho específico, fazer snapshot e identificar o elemento

**Recorte sugerido:** Capturar viewport do topo (manchete + lead + imagem hero).

---

### GitHub Repository

**Desafio:** READMEs longos, precisa capturar seção específica.

**Estratégia:**
1. Navegar para a URL do repo ou README
2. Fazer snapshot da página
3. Identificar a seção relevante (ex: "What You Can Build", "Features", "Installation")
4. Capturar screenshot apenas dessa seção
5. Se a seção for muito longa, capturar só o início

---

### YouTube

**Desafio:** Ads, popups de consent.

**Estratégia:**
1. Navegar para a URL do vídeo
2. Fechar popups de consent/cookies
3. Capturar thumbnail do vídeo + título
4. Alternativamente, capturar apenas a thumbnail em tamanho maior via URL direta:
   `https://img.youtube.com/vi/[VIDEO_ID]/maxresdefault.jpg`

---

### LinkedIn Post

**Desafio:** Login wall agressivo.

**Estratégia:**
1. Tentar navegar para a URL
2. Se bloqueado por login, informar o usuário e pedir screenshot manual
3. Se acessível, capturar o corpo do post

**Nota:** LinkedIn é a fonte mais difícil de capturar automaticamente. Priorizar fallback manual.

---

### URL Genérica

**Estratégia:**
1. Navegar para a URL
2. Fechar popups/banners se houver
3. Perguntar ao usuário o que capturar (viewport, elemento específico, seção)
4. Capturar conforme solicitado

---

## Estilo dos screenshots no slide

**REGRA ABSOLUTA: NUNCA usar `object-fit: contain` com `background` em screenshots.** Cria bordas escuras enormes que destroem o visual. É o erro mais grave e mais recorrente.

```css
/* Screenshot único — usa base.css .screenshot-frame */
.screenshot-frame {
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.06);
  overflow: hidden;
  max-width: 920px;
  width: 100%;
}
.screenshot-frame img {
  width: 100%;
  display: block;
  /* SEM object-fit, SEM background — tamanho natural */
}

/* Dois screenshots lado a lado — mesma altura */
.screenshots-row {
  display: flex;
  gap: 16px;
  width: 100%;
  max-width: 920px;
  align-items: stretch;
}
.screenshots-row .screenshot-frame {
  flex: 1;
  display: flex;
}
.screenshots-row .screenshot-frame img {
  object-fit: cover;
  object-position: top left;
}

/* Dois screenshots lado a lado — alturas naturais diferentes */
.screenshots-row-natural {
  display: flex;
  gap: 16px;
  align-items: flex-start; /* ou flex-end conforme alinhamento desejado */
}
```

### Posicionamento

- **Slide com texto + screenshot:** screenshot na metade inferior, centralizado no flex
- **Slide dual-screenshot:** lado a lado com `align-items: stretch` + `object-fit: cover` pra igualar alturas
- **Screenshot como elemento principal:** pode ocupar até 60% do slide
- **Screenshots com aspect ratios muito diferentes:** usar `align-items: flex-start` e flex ratios diferentes (ex: `flex: 2` pro menor, `flex: 3` pro maior)

### Embutir no HTML

Os screenshots capturados devem ser convertidos para base64 e embutidos diretamente no HTML como data URI, ou referenciados como arquivo local:

```html
<!-- Via arquivo local -->
<img class="screenshot" src="./screenshots/tweet_captura.png" alt="Screenshot">

<!-- Via base64 (mais portátil) -->
<img class="screenshot" src="data:image/png;base64,..." alt="Screenshot">
```

Preferir arquivo local para não inflar o HTML. Converter para base64 apenas se necessário.

---

## Fallback manual

Quando a captura automática falhar:

1. Informar o usuário: "Não consegui capturar [URL]. O site bloqueia acesso automatizado."
2. Pedir: "Pode tirar um screenshot e me passar o caminho do arquivo?"
3. Aceitar: png, jpg, jpeg, webp
4. Aplicar o mesmo estilo (border-radius, shadow) ao embutir
