---
description: Engenharia reversa completa de vídeos (Reels, TikTok, Shorts). Baixa vídeo, extrai frames, transcreve áudio com Whisper, analisa composição visual frame-by-frame e popula adaptive_models via storage layer. Use quando digitar "/analisar-video", "engenharia reversa", "analisar reel", "modelar esse vídeo", "dissecar conteúdo", "extrair o formato", ou quando o user mandar um link/arquivo de vídeo pra análise.
argument-hint: "[url-vídeo|path-arquivo]"
---

Usuário invocou `/analisar-video` com argumento: `$ARGUMENTS`

# /analisar-video — Engenharia Reversa de Vídeos

> Transforma qualquer Reel/TikTok/Short num `adaptive_model` documentado com estrutura narrativa, padrões visuais, tom, CTA, e guia de replicação. Popula `adaptive_models` via storage layer (`lib/storage/contract.md`).

**Objetivo:** Mapear um vídeo viral em modelo replicável com estrutura, regras visuais, tom, hook e CTA — pronto pra ser consumido por `/roteiro-viral`.

**Escopo:** Download → frames → transcrição → análise visual → modelo adaptativo → persistência storage.
**Fora do escopo:** Gerar roteiro adaptado (é `/roteiro-viral`), analisar conteúdo próprio publicado (é `/analista-conteudo`).

---

## Passo 0: Pré-requisitos + Backend

### Dependências do sistema
- `yt-dlp` instalado (baixar vídeos de URLs)
- `ffmpeg` / `ffprobe` instalados (extrair frames e áudio)
- Skill `transcribe-audio` configurada (Whisper)
- Claude multimodal (lê imagens)

### Backend de storage

Ler `CLAUDE.md` do projeto → `## Storage Backend: <opção>`. Opções: `supabase`, `sheets`, `markdown`.

**Pré-check soft (não aborta):**

Se backend **!= supabase**, avisar:
> "Backend atual: `<opção>`. Frame analysis pode ficar pesado (~50KB JSON por vídeo). Supabase recomendado pra escala. Prossigo? (y/n)"

Sem `## Storage Backend:` definido:
> "Configure backend em CLAUDE.md `## Storage Backend: <opção>` — opções: supabase / sheets / markdown."

---

## Pipeline de Análise

### Etapa 1 — Download

Se for URL, baixar com yt-dlp:
```bash
yt-dlp -o "<destino>/<id>.%(ext)s" "<url>"
```

Destino padrão: `./refs/` no projeto do user, ou `/tmp/video-analysis/` se estiver fora de projeto.

Se for arquivo local: pular esta etapa.

### Etapa 2 — Extrair metadados

```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 <video>
```

Registrar: duração, resolução, aspecto.

### Etapa 3 — Extrair frames

Taxa de extração depende da duração:

| Duração | FPS | Frames esperados |
|---------|-----|------------------|
| < 30s   | 2fps | ~60 |
| 30-60s  | 1fps | ~30-60 |
| 60-120s | 1fps | ~60-120 |
| > 120s  | 0.5fps | varia |

```bash
mkdir -p <destino>/frames-<id>
ffmpeg -i <video> -vf "fps=<taxa>" <destino>/frames-<id>/f_%03d.jpg -y
```

### Etapa 4 — Extrair e transcrever áudio

```bash
ffmpeg -i <video> -vn -acodec libmp3lame <destino>/audio-<id>.mp3 -y
```

Transcrever via skill `transcribe-audio` (global). O path da integração Whisper vive em `${USER_WHISPER_DIR}` ou no setup da skill global — não hardcodar caminho absoluto. Chamada tipo:

```bash
# Via skill transcribe-audio — idioma "en" default, "pt" pra português. Whisper detecta auto.
transcribe-audio --file-path "<path-do-audio>" --language "<idioma>"
```

### Etapa 5 — Análise visual (frames)

Ler frames em intervalos estratégicos. Mapear CADA corte e transição.

**Abordagem por camadas:**

1. **Varredura rápida (obrigatória):** Ler frames a cada 5s (primeiro, 25%, 50%, 75%, último). Identificar tipo de conteúdo (TH, screencast, gráfico), cortes principais, texto na tela.
2. **Varredura detalhada (quando necessário):** Se varredura rápida mostrar muitos cortes, ler frames adicionais nos trechos densos (a cada 1-2s).
3. **Análise de corte:** Comparar frames consecutivos. Mudança drástica de composição = corte. Registrar timestamp de cada corte.

**Para cada frame analisado, registrar:**
- Timestamp aproximado
- Tipo: TH close-up / TH médio / TH wide / screencast filmado / screen recording / gráfico / split screen
- Texto na tela (overlays, legendas, títulos)
- Expressão/gesto do criador (se TH)
- O que aparece na tela (se screencast)
- Se houve corte em relação ao frame anterior

### Etapa 6 — Montar mapa de cortes

Cruzar transcrição (timestamps quando disponíveis) + análise visual:

```
| Tempo | Frames | Visual | Fala | Técnica |
|-------|--------|--------|------|---------|
| 0-3s  | 1-6    | TH close-up, título fixo "X = Y" | "Hook" | Título bold no topo |
| 3-5s  | 7-10   | TH zoom extremo | "Eu não deveria..." | Zoom digital edição |
```

### Etapa 7 — Identificar padrões

Extrair do mapa de cortes:

1. **Estrutura de beats:** Quantas cenas, duração, função (hook, dev, CTA)
2. **Tipo de screencast:** Câmera filmando tela vs screen recording vs overlay flutuante
3. **Título:** Fixo o vídeo todo? Só no hook? Muda por seção?
4. **CTA:** Duração, estilo (keyword, seco, mockup DM), posição
5. **Tom/energia:** Casual vs profissional, alta vs baixa, constante vs variável
6. **Overlays:** Quais, quando aparecem, quanto tempo
7. **Enquadramento TH:** Close-up, médio, wide, zoom digital, selfie vs tripé

### Etapa 8 — Gerar modelo adaptativo

Compilar tudo num documento estruturado:

```markdown
## Modelo Adaptativo: [Nome]

**Fonte:** [criador] — [URL]
**Duração:** [Xs] | **Engagement:** [likes, comments se disponível]
**Analisado de:** [N] frames + transcrição Whisper

### Resumo
[1-2 frases descrevendo o formato]

### Estrutura (N beats em ~Xs)
| Beat | Tempo | Tipo | Função |
|------|-------|------|--------|

### Regras Visuais
- Título: [comportamento]
- Screencast: [tipo]
- Overlays: [lista]
- Enquadramento: [padrões]
- Cortes: [estilo]

### Tom e Energia
- O que É: [descrição]
- O que NÃO É: [descrição]

### CTA
- Estilo: [descrição]
- Duração: [Xs]

### Quando Usar
- [cenários ideais]
```

### Etapa 9 — Persistir via storage layer

Após gerar o modelo adaptativo, salvar na estrutura `adaptive_models` via storage abstraction (CONVENCOES §4 — zero SQL inline):

```
storage.write_adaptive_model({
  source_video_url: "<url do vídeo>",
  hook_visual: "<descrição primeiros 3s — enquadramento, cores, texto na tela>",
  hook_falado: "<transcrição primeiros 3s>",
  structure_json: <estrutura narrativa em JSON — beats, tempos, funções>,
  arquetipo: "<arquétipo detectado — ex: tutorial, revelação, contrário>",
  formato: "<'reel' | 'tiktok' | 'short'>",
  duracao: <segundos>,
  transcript: "<transcrição completa>",
  frame_analysis_json: <análise frame-by-frame em JSON>
})
```

Retorna `id` do novo registro. Confirmar ao user:
> "Modelo adaptativo salvo como `adaptive_models.id={id}`. Pronto pra `/roteiro-viral` consumir."

**Aviso específico quando backend != supabase:** `frame_analysis_json` pode gerar arquivo/linha pesada (~50KB). Em `markdown` backend vira frontmatter grande; em `sheets` satura célula. Se user prosseguiu após aviso do Passo 0, proceder mesmo assim.

---

## Paralelismo

Sempre que possível, rodar etapas em paralelo:
- Etapas 3 e 4 (frames + áudio) podem rodar juntas
- Transcrição e análise visual podem rodar em paralelo
- Análise detalhada de frames pode ser dividida em batches

---

## Onde salvar (filesystem)

- Frames: `<projeto>/refs/frames-<id>/`
- Áudio: `<projeto>/refs/audio-<id>.mp3`
- Transcrição: `<projeto>/refs/audio-<id>.txt` (gerado pelo Whisper)
- Modelo adaptativo (cópia legível humana): `<projeto>/modelos/<nome>.md`
- Vídeo original: `<projeto>/refs/<id>.mp4`

Os artifacts estruturados vivem na storage layer. Os artifacts de trabalho (vídeo, frames, áudio) ficam no filesystem do projeto.

---

## Integração com `/roteiro-viral`

Após salvar o modelo adaptativo via storage, instruir user:
> "Modelo salvo (`id={id}`). Pra gerar roteiro adaptado, rode:
> `/roteiro-viral {id}`"

Skills não cascateiam — cada slash é invocação explícita do user.

---

## Hook auto-obs: Sinal 4 (vídeo do criador analisado)

Após análise concluída e persistência via storage (Etapa 9), disparar hook de auto-observação conforme padrão em `CLAUDE.md` §Auto-Obs Hooks e `lib/voz/auto-observacao.md` §Sinal 4.

### 1. Verificar se engine está ativa

Ler frontmatter de `reference/voz-<handle>.md` do projeto atual (handle resolvido pelo CLAUDE.md `## Handle: @<x>`).

- Arquivo não existe OU `auto_observacao_ativa: false` → **skip hook silenciosamente** (sem log, sem aviso).
- `auto_observacao_ativa: true` → prosseguir.

### 2. Extrair handle do URL do vídeo analisado

Identificar handle do criador do vídeo conforme plataforma:

| Plataforma | Método |
|------------|--------|
| **Instagram** (`instagram.com/p/...` ou `/reel/...`) | Metadata da página via WebFetch / Playwright — buscar `username` no OG tag ou scraping da página do post |
| **TikTok** (`tiktok.com/@<handle>/video/...`) | Handle direto do path da URL (segmento após `@`) |
| **YouTube** (`youtube.com/watch?v=...` ou `youtu.be/...`) | Scrape da página pelo channel handle (`@channel` no canto da página) ou `channel_url` do metadata yt-dlp |

Se não conseguir extrair (URL mal formada, vídeo privado, scrape falhou): **skip hook** — não propaga erro ao user.

### 3. Comparar com handle da voz + aplicar threshold

Carregar `handle` do frontmatter de `reference/voz-<handle>.md`.

**Threshold (Spec §5.4 / lib/voz/auto-observacao.md §Sinal 4):**

- **Handle do vídeo == handle da voz do projeto:** **1 ocorrência basta** (sinal forte — é o próprio criador se auto-observando).
- **Handle terceiro (criador externo):** exige **3 ocorrências com mesmo padrão de abertura** em vídeos diferentes pra disparar (evita ruído de inspiração aleatória).

Para o caso de terceiros, manter contador em `reference/.voz-tracking.json` (chave `sinal_4.aberturas_terceiros`) — ver schema em `lib/voz/auto-observacao.md`. Incrementar contador no `frame_analysis_json` + abertura detectada + handle.

### 4. Detectar "aberturas típicas" novas

Do modelo adaptativo recém-gerado, extrair candidatos a abertura típica:

- **Primeiros 3s falados** do `transcript` (hook verbal).
- **Primeiros 3s visuais** do `frame_analysis_json` (enquadramento + texto na tela + expressão).

Comparar com a seção **"5. Aberturas típicas"** do `reference/voz-<handle>.md`:

- Se a abertura detectada já está listada → **skip** (não propor duplicata).
- Se for nova → candidata a evolução.

### 5. Propor evolução ao user

Se threshold atingido + pelo menos 1 abertura nova detectada:

```
🧬 Auto-observação (Sinal 4)

Detectei novas aberturas que você usa nos vídeos:
- "<abertura 1>"
- "<abertura 2>"

Adiciona em "Aberturas típicas" da sua voz? (y/n)
```

Se user responder **y**: instruir explicitamente (skills não cascateiam):

> "Pra aplicar, rode:
> `/voz evoluir <abertura>`
>
> Ou pra adicionar todas de uma vez: `/voz evoluir --batch` (cole a lista)."

Se **n**: marcar a(s) abertura(s) como "rejected" no tracking pra não propor de novo.

### 6. Privacy (crítico)

⚠️ **Scraping do handle é SOMENTE pra match com voz local do projeto. NADA sai upstream.**

- `.voz-tracking.json` fica no filesystem do projeto do user (gitignore recomendado — `setup-projeto` cuida).
- Plugin nunca envia dados do tracking pra Anthropic ou terceiros.
- Handle do criador de vídeos terceiros fica armazenado APENAS pra contagem de threshold — não é usado pra outros fins.

---

## Regras

1. **Zero SQL inline** — toda persistência via `storage.write_adaptive_model(...)` (CONVENCOES §4)
2. **Pré-check backend é soft** — avisa mas não aborta (diferente de `/analista-conteudo`)
3. **Pipeline completo** — nunca pular etapa de frames ou transcrição
4. **Paralelismo** quando possível — frames + áudio juntos
5. **Path do Whisper nunca hardcodado** — usa env ou skill global `transcribe-audio`
6. **Frame analysis pode ser pesado** — avisar user antes de salvar em sheets/markdown
7. **Retornar id do adaptive_model** pra user encadear com `/roteiro-viral`
8. **Auto-obs Sinal 4** — disparar apenas se `auto_observacao_ativa: true`. Scrape de handle só pra match local. Nada upstream.

---

✅ Modelo adaptativo gerado e persistido

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /roteiro-viral   — gera roteiro consumindo o adaptive_model criado

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
