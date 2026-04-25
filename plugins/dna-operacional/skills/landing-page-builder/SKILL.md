---
name: landing-page-builder
description: Framework completo para criar landing pages de alta performance com design diferenciado. Use SEMPRE que o usuario pedir para criar, editar, otimizar ou revisar uma landing page, pagina de vendas, pagina de captura, waitlist, ou qualquer pagina web estatica. Tambem use quando mencionar copy de landing page, layout de pagina, formulario de captura, deploy de pagina, ou quando estiver trabalhando dentro do projeto landing-pages. Inclui workflow de 4 etapas (copy, design, layout, desenvolver), regras anti-slop, arquetipos criativos, padroes de formulario, animacao, performance e deploy via Netlify.
---

# Landing Page Builder

Framework para criar landing pages que se destacam de templates genericos de IA.

## Fluxograma Geral

Ao iniciar qualquer trabalho com landing page, mostre este fluxograma ao usuario:

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                   LANDING PAGE BUILDER                         │
  └─────────────────────────────────────────────────────────────────┘

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐
  │  ETAPA 1 │───>│  ETAPA 2 │───>│  ETAPA 3 │───>│   ETAPA 4    │
  │  COPY    │    │  DESIGN  │    │  LAYOUT  │    │ DESENVOLVER  │
  │          │    │          │    │          │    │              │
  │ copy.md  │    │ style.css│    │layout.md │    │ index.html   │
  │ textos   │    │ tokens   │    │ spec     │    │ style.css    │
  │ SEO      │    │ fonts    │    │ detalhada│    │ script.js    │
  └────┬─────┘    └────┬─────┘    └────┬─────┘    └──────┬───────┘
       │               │               │                 │
       v               v               v                 v
  [APROVACAO]     [APROVACAO]     [APROVACAO]     [VERIFICACAO]
                                                        │
                                          ┌─────────────┼──────────────┐
                                          v             v              v
                                    ┌──────────┐ ┌──────────┐  ┌──────────┐
                                    │ OTIMIZAR │ │ TRACKING │  │ PUBLICAR │
                                    │ 90+ score│ │ GTM/Pixel│  │ deploy   │
                                    └──────────┘ └──────────┘  └──────────┘
```

A cada etapa concluida, marque no fluxograma com [OK] e mostre qual e o proximo passo.

## Idioma
Todas as mensagens em Portugues do Brasil. Termos tecnicos e codigo em ingles.

## Regra Zero: Autonomia
Execute todos os comandos sozinho. A unica excecao: informe quando o browser abrir pra autorizacao OAuth. Se algo falhar, resolva sozinho. So peca ajuda ao usuario em ultimo caso.

---

## Workflow em 4 Etapas

### Etapa 1: Copy
Criar `copy.md` com todos os textos organizados por secao.

**Antes de escrever, leia** `references/humanizer-rules.md` e aplique todas as regras. A copy deve soar como escrita por humano, nunca como output de IA.

Estrutura do arquivo:
```markdown
# Nome do Projeto - Copy
---
## SECAO 1 — HERO
**Badge:** texto
**Headline:** texto
**Subheadline:** texto
**CTA:** texto
---
## SECAO N — NOME
(conteudo)
---
## SEO
**Title:** (max 60 chars)
**Meta Description:** (max 160 chars)
**OG Title/Description**
```

Apresentar ao usuario para aprovacao antes de prosseguir.

### Etapa 2: Design Tokens
Definir tokens visuais nas custom properties do `style.css`.

**Antes de escolher, leia** `references/anti-slop-rules.md`. Nunca usar as combinacoes proibidas.

Definir:
- Paleta de cores (backgrounds, texto, accent, bordas, status)
- Font pairing (display + body + mono se aplicavel)
- Spacing rhythm (section, container, gaps)
- Direcao visual (uma frase resumindo o tom)

**Preferir fontes premium** (Envato Elements, custom) sobre Google Fonts. Se usar Google Fonts, nunca Inter, DM Sans, Roboto, Poppins, Montserrat ou Open Sans como body.

Apresentar ao usuario para aprovacao.

### Etapa 3: Layout
Criar `layout.md` com spec detalhada por secao.

**Antes de definir arquetipos, leia** `references/archetypes.md` para escolher layouts imprevisiveis.

Cada secao deve ter:
- Arquetipo + constraints unicos (nunca repetir entre secoes consecutivas)
- Layout (grid, flex, posicionamento com valores CSS)
- Tipografia especifica (tamanhos com clamp(), pesos, cores)
- Elementos visuais decorativos
- Animacoes (AOS apenas fora do hero)
- Responsividade (375px, 768px, 1024px, 1440px)

Apresentar ao usuario para aprovacao.

### Etapa 4: Desenvolver
Construir nos 3 arquivos: `index.html`, `style.css`, `script.js`.

Testar com `netlify dev`. Verificar em todos os breakpoints.

---

## Regras Criticas

### Hero: Visivel no Primeiro Frame
**Nunca adicionar opacity:0, transform, ou data-aos no hero.** O hero deve estar 100% visivel no primeiro frame. Animacoes pos-carregamento (hover, scroll, ambient, typing) sao permitidas.

### AOS (Animate on Scroll)
Apenas fora do hero. Sempre inicializar com:
```javascript
AOS.init({ once: true, duration: 600, disableMutationObserver: true });
```
Sem `disableMutationObserver: true`, o AOS causa CLS de 0.7+ no body.

### Formularios
Consultar `references/forms.md` para padroes completos. Regras essenciais:
- Netlify Forms com honeypot anti-spam
- `form name` deve coincidir com `input[name="form-name"]`
- intl-tel-input para telefone (CDN, nao npm)
- Validacao client-side + server-side
- Touch targets minimo 44x44px

### Performance
Consultar `references/performance.md`. Regras essenciais:
- Imagens: Netlify CDN (`/.netlify/images?url=...&w=...&q=80`) + width/height numericos
- Hero: `loading="eager"`, resto: `loading="lazy"`
- Fontes: sincronas com preconnect + display=swap, max 3 pesos
- Scripts pesados: Dynamic Import + IntersectionObserver, nunca `<script src>`
- CSS: sincrono durante dev (bloqueante)

### Caminhos
Sempre absolutos (`/`). Caminhos relativos (`./`, `../`) quebram em subdiretorios.

### Sem NPM
Zero build step. Todas dependencias via CDN.

---

## Anti-Patterns Proibidos

Consultar `references/anti-slop-rules.md` para lista completa. Os piores:

- Hero centralizado generico com subtitulo + CTA
- 3 cards flutuantes com icones de linha
- Grid simetrico 50/50
- Gradiente azul-roxo como identidade
- Background off-white quente (#f5f3f0 e similares) sozinho
- Inter/DM Sans como body font
- Cards com 1px border + 12px radius + sem sombra
- Labels todas em uppercase + tracking 0.06em
- Carousel com setas
- Animacoes decorativas sem proposito

---

## Principios de Design

- **Tipografia dramatica:** contraste de pesos extremo, headlines massivas
- **Layouts imprevisiveis:** variar arquetipos entre secoes
- **Espaco negativo agressivo:** como ferramenta ativa
- **Breakpoints de teste:** 375px, 768px, 1024px, 1440px
- **Touch targets:** minimo 44x44px
- **prefers-reduced-motion:** sempre respeitar

---

## Estrutura de Arquivos

```
pagina/
├── index.html
├── style.css
├── script.js
├── copy.md
├── layout.md
├── fonts/           (se custom)
├── images/          (se aplicavel)
├── netlify.toml     (se projeto standalone)
├── netlify/functions/ (se integracao server-side)
├── .env             (nunca commitar)
└── _backup_vN/      (versoes anteriores)
```

---

## Servidor Local

Exclusivamente `netlify dev`. Nunca `python -m http.server` ou `npx serve` (nao suportam CDN de imagens, redirects nem formularios Netlify).

```bash
# Verificar portas em uso
lsof -i :8888 -i :3999 2>/dev/null | grep node
# Matar se necessario
kill $(lsof -ti :8888) 2>/dev/null
# Iniciar
netlify dev
```

---

## Deploy

Consultar `references/deploy.md` para workflow completo. Resumo:

```bash
# Novo projeto
git init && git add . && git commit -m "feat: landing page"
gh repo create nome --private --source=. --push
netlify sites:create --name nome
netlify env:set CHAVE valor  # para cada env var
netlify deploy --prod

# Atualizacao
git add . && git commit -m "descricao" && git push
netlify deploy --prod
```

---

## Comandos Adicionais

Alem do workflow principal (copy → design → layout → desenvolver), existem comandos complementares:

### /otimizar
Otimiza performance para 90+ PageSpeed. Consultar `references/performance.md`.
Fluxo: medir antes (Lighthouse) → auditar → correcoes seguras → correcoes condicionais → medir depois → comparar.

### /configurar-tracking
Configura GTM e/ou Meta Pixel. Consultar `references/tracking.md`.
Coleta IDs → instala snippets na ordem correta → configura eventos de conversao → testa.

### /debug
Investiga problemas sistematicamente.
Coletar sintoma → formar hipotese → investigar → corrigir causa raiz → prevenir recorrencia.

### /publicar
Deploy para producao via Git push.
Pre-checklist (redirect, imagens CDN, hero sem animacao entrada, form, responsivo) → git push → netlify deploy.

### /previsualizar
Cria Deploy Preview via PR no GitHub para testar antes de producao.
Branch → PR → deploy preview automatico → URL para teste.

### /visualizar-local
Inicia Netlify Dev. Verificar portas → escolher par livre → iniciar servidor.

---

## Referencia Rapida

| Precisa de... | Consulte |
|---|---|
| Arquetipos de layout | `references/archetypes.md` |
| Regras anti-slop | `references/anti-slop-rules.md` |
| Padroes de formulario | `references/forms.md` |
| Performance/otimizar | `references/performance.md` |
| Animacoes | `references/animations.md` |
| Humanizacao de copy | `references/humanizer-rules.md` |
| Tracking (GTM, Pixel) | `references/tracking.md` |
| Deploy/publicar | `references/deploy.md` |
| Font pairings | `references/typography.md` |

## Origem

Esta skill foi extraida do framework em `<diretório original do framework no projeto fonte>`, que contem a documentacao original em `docs/` e os slash commands em `.claude/commands/`. Se precisar de informacao mais detalhada sobre algum topico, consulte esses arquivos diretamente.
