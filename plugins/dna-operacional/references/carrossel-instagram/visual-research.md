# Pesquisa Visual Autônoma — Moodboard

Este guia é lido pela skill durante o **Gate 1.5: Moodboard Visual**. Descreve como coletar referências visuais externas usando `agent-browser` (engine principal de pesquisa) e Playwright MCP (fallback e captura pontual).

## Quando aplicar

**SEMPRE** antes do Gate 3 (Direção Visual). A proposta de paleta/efeito/layout deve estar ancorada em referências reais, não em achismo.

## Objetivo do moodboard

Coletar **3-5 moodboards full-page** (1 por fonte) sobre o tema do carrossel para:
1. Validar tendências de design atuais (paleta, composição, tipografia)
2. Identificar padrões visuais de alto engajamento no tema
3. Ancorar a proposta do Gate 3 em evidências externas
4. Apresentar ao usuário um moodboard visual junto com as opções de paleta/efeito

**Preferir screenshot full-page da grade de busca** (captura ~15 pins de uma vez) em vez de capturar pins individualmente. Captura individual só quando o usuário pedir detalhe de um pin específico.

## Fontes por prioridade

| Ordem | Fonte | URL padrão | Por que |
|-------|-------|-----------|---------|
| 1 | Pinterest | `https://www.pinterest.com/search/pins/?q=[TEMA]+carousel` | Sem login wall bloqueante, melhor curadoria visual |
| 2 | Dribbble | `https://dribbble.com/search/[tema]-carousel` | Design profissional, tendências de UI |
| 3 | Behance | `https://www.behance.net/search/projects?search=[tema]+carousel` | Projetos completos, sistemas visuais |
| 4 | Google Imagens | `https://www.google.com/search?q=[tema]+instagram+carousel&tbm=isch` | Fallback genérico |
| 5 | Instagram | `https://www.instagram.com/explore/tags/[tag]` | Referência direta (mas tem login wall) |

Usar **pelo menos 2 fontes diferentes** por carrossel. Pinterest + Dribbble é o combo default.

---

## Fluxo com agent-browser (engine principal)

**Pré-requisito:** `agent-browser` instalado (`npm i -g agent-browser && agent-browser install`).

### Passo 1: Pesquisa no Pinterest

Pinterest não bloqueia search results sem login — banner dismissível aparece mas o conteúdo renderiza. **Requer wait** porque os pins carregam via JS/lazy load mesmo tendo o title pronto no `open`.

```bash
agent-browser batch \
  "open https://www.pinterest.com/search/pins/?q=[TEMA]+carousel" \
  "wait 5000" \
  "scroll down 800" \
  "wait 2000" \
  "screenshot --full ./moodboard/pinterest-full.png"
```

**Não usar o caminho simples `open` + `screenshot`** — o screenshot sai com placeholders cinza. Sempre batch com wait + scroll.

### Passo 2: Pesquisa no Dribbble (requer wait pra lazy load)

Dribbble tem lazy loading agressivo. Usar `batch` com `wait` + `scroll` antes do screenshot:

```bash
agent-browser batch \
  "open https://dribbble.com/search/[TEMA]-carousel" \
  "wait 5000" \
  "scroll down 1500" \
  "wait 2000" \
  "screenshot --full ./moodboard/dribbble-full.png"
```

### Passo 3: Pesquisa no Behance

```bash
agent-browser batch \
  "open https://www.behance.net/search/projects?search=[TEMA]+carousel" \
  "wait 5000" \
  "scroll down 1500" \
  "wait 2000" \
  "screenshot --full ./moodboard/behance-full.png"
```

### Passo 4: Captura de pin individual (opcional)

Se um pin específico do Pinterest for muito relevante e precisar de alta resolução:

```bash
# 1. Rodar snapshot pra achar o ref do pin
agent-browser snapshot -i | head -100

# 2. Identificar o ref (ex: @e23) e clicar pra abrir a página do pin
agent-browser click @e23

# 3. Aguardar e capturar full-page
agent-browser batch "wait 3000" "screenshot --full ./moodboard/pinterest-pin-[nome].png"

# 4. Voltar pra grade
agent-browser back
```

### Passo 5: Instagram (última prioridade — tem login wall)

Instagram exige login mesmo para tags. Se a sessão persistente do agent-browser já tem cookies (do carrossel anterior), reaproveita automaticamente. Se for primeira vez:

```bash
agent-browser open "https://www.instagram.com/accounts/login/"
# Pedir ao usuário para fazer login manual no browser controlado pelo daemon
# O daemon mantém cookies entre sessões, então login é one-time
```

Depois de logado:

```bash
agent-browser batch \
  "open https://www.instagram.com/explore/tags/[tag]" \
  "wait 4000" \
  "screenshot --full ./moodboard/instagram-full.png"
```

### Sintaxe de referência

| Comando | Uso |
|---------|-----|
| `agent-browser open <url>` | Navegar (NÃO é `navigate`) |
| `agent-browser snapshot -i` | Accessibility tree com refs inline |
| `agent-browser screenshot --full <path>` | Screenshot full-page |
| `agent-browser screenshot <selector> <path>` | Screenshot de elemento específico |
| `agent-browser batch "cmd1" "cmd2" ...` | Chain de comandos |
| `agent-browser wait <ms>` | Esperar tempo (dentro de batch) |
| `agent-browser scroll down <px>` | Rolar página |
| `agent-browser click @eN` | Clicar em ref do snapshot |
| `agent-browser get url` | URL atual (testa sessão) |
| `agent-browser back` | Voltar |
| `agent-browser close --all` | Fechar browser (raro, só pra reset) |

---

## Fluxo com Playwright MCP (fallback)

Usar quando: (a) `agent-browser` não está disponível, (b) a fonte requer interação que só Playwright MCP resolve (ex: `browser_run_code` para manipulação DOM), (c) captura pontual de 1-2 referências onde o overhead do daemon não vale.

```
1. browser_navigate para a URL de busca
2. browser_wait_for (aguardar seletor de pin carregar)
3. browser_take_screenshot (fullPage: true) salvando em ./moodboard/{fonte}-full.png
4. browser_close no final
```

**Importante:** para pesquisa visual em profundidade (3+ fontes), preferir `agent-browser` pela economia de tokens (~6x menos tokens no snapshot) e sessão persistente. Playwright MCP continua sendo o default para o **render final do carrossel (Gate 4)** e **captura de tweets com tradução DOM**.

---

## Estrutura local do moodboard

No diretório de trabalho do carrossel atual (ex: `carrossel-claude-code-vs-cursor/`), criar:

```
moodboard/
├── pinterest-full.png     # grade da busca Pinterest
├── dribbble-full.png      # grade da busca Dribbble
├── behance-full.png       # grade da busca Behance (opcional)
├── instagram-full.png     # grade da busca Instagram (opcional)
├── pinterest-pin-[N].png  # captures individuais (opcional, quando relevante)
└── moodboard.md           # notas da curadoria
```

O `moodboard.md` contém:

```markdown
# Moodboard — [Nome do Carrossel]

**Tema:** [tema]
**Template:** [template escolhido no Gate 1]
**Data:** [YYYY-MM-DD]

## Fontes capturadas

- `pinterest-full.png` — busca "[query]" — ~15 pins visíveis
- `dribbble-full.png` — busca "[query]" — ~10 pins visíveis
- (outras, se aplicável)

## Destaques visuais

Listar 3-5 referências específicas que se destacaram, com observação do que elas fazem bem:

- **[Nome/descrição do pin]** (em `pinterest-full.png`, quadrante superior-esquerdo) — [o que se destaca: paleta, tipografia, layout]
- ...

## Padrões observados

- **Paletas dominantes:** [listar 2-3 que se repetem entre as fontes]
- **Tipografia:** [sans-serif bold? serif editorial? display condensada?]
- **Composição:** [centralizada? assimétrica? full-bleed? grade?]
- **Elementos recorrentes:** [números grandes? screenshots de terminal? ícones de marca? emojis?]
- **Mood geral:** [dark/premium? clean/editorial? vibrante/jovem?]

## Direção sugerida pro Gate 3

Com base nos padrões observados, sugerir direção preliminar:

- **Paleta:** [paleta do references/palettes.md que bate OU paleta custom baseada nas cores dominantes do moodboard]
- **Efeito tipográfico:** [efeito do references/headline-effects.md que combina]
- **Layout/composição:** [que inspiração do moodboard seguir]

Esta é uma **prévia** — a proposta final vem no Gate 3 com paletas alternativas.
```

Este `moodboard.md` é a ponte entre a pesquisa visual e o Gate 3.

---

## Critérios de curadoria

Ao analisar os screenshots full-page das fontes, identificar os pins/projetos que atendem:

### Obrigatório (ignorar se falhar)

- **Alinhamento com o tema** — pin sobre o mesmo assunto (IA, código, produtividade, etc.)
- **Qualidade visual** — não considerar pins pixelados, com marca d'água grande, ou mal compostos
- **Formato próximo** — priorizar referências em formato carrossel (3:4, 4:5, 1:1)

### Desejável (pontos positivos)

- **Alto engajamento** (likes/shares visíveis no Pinterest/Instagram quando aparecer)
- **Estilo distinto** — evitar destacar 5 referências com o mesmo look
- **Combinação tema + mood** — se carrossel é "hot take" sobre IA, preferir referências com mood editorial/polêmico

### Proibido

- **Carrosséis do próprio criador (handle do projeto)** — queremos inspiração externa, não auto-referência
- **Templates genéricos do Canva** — baixa qualidade de design
- **Imagens AI-generated com artefatos óbvios** (mãos deformadas, texto ilegível)

---

## Apresentação ao usuário

Ao final do Gate 1.5, apresentar ao usuário:

1. **Lista das fontes capturadas** com caminhos locais
2. **Destaques visuais** — 3-5 referências específicas que se destacaram
3. **Padrões observados** (paletas dominantes, tipografia, composição)
4. **Direção sugerida** para o Gate 3 — prévia da proposta

### Formato da mensagem

```markdown
## Moodboard coletado

Fontes capturadas:
- Pinterest: `./moodboard/pinterest-full.png` (~15 pins)
- Dribbble: `./moodboard/dribbble-full.png` (~10 pins)

### Destaques visuais
- **[pin 1]**: [por que]
- **[pin 2]**: [por que]
- **[pin 3]**: [por que]

### Padrões que vi se repetindo
- **Paleta:** [observação]
- **Tipografia:** [observação]
- **Composição:** [observação]

### Minha sugestão preliminar pro Gate 3
- **Paleta:** [paleta do references/palettes.md OR custom baseada no moodboard]
- **Efeito:** [efeito do references/headline-effects.md]
- **Layout:** [composição sugerida]

Moodboard completo em: `./moodboard/`

**Aprovar moodboard e seguir pro Gate 2 (Conteúdo Textual)?**
```

### Gate: usuário aprova ou pede ajuste/mais referências antes de seguir.

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Screenshot full-page vem branco | JS não carregou. Adicionar `wait 4000-6000` antes do screenshot |
| Pinterest com placeholders cinza (retângulos vazios) | Aconteceu quando o screenshot foi tirado cedo demais. SEMPRE usar `batch` com `wait 5000` + `scroll down 800` + `wait 2000` no Pinterest, nunca `open` + `screenshot` direto |
| Dribbble/Behance com muitos placeholders cinza | Lazy loading. Adicionar `scroll down 1500` + `wait 2000` no batch |
| Pinterest com banner "signed out" ocupando espaço | OK — o banner é dismissível mas os pins ao redor renderizam normalmente. Aceitar |
| Instagram exige login | Sessão persistente reaproveita cookies. Primeira vez: fazer login manual no browser do daemon, depois skill reusa automaticamente |
| Comando `navigate` retorna "Unknown command" | Sintaxe correta é `open`, não `navigate` |
| `agent-browser get url` retorna vazio | Daemon foi fechado. Rodar `agent-browser open <url>` pra reativar |
| Carrossel anterior deixou daemon com URL errada | OK — `open` sobrescreve. Não precisa `close` entre carrosséis |
