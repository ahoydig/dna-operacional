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

### Etapa 9 — Persistir adaptive_model

Salvar o modelo adaptativo na estrutura `adaptive_models` (ver `lib/storage/contract.md`). Implementação via storage layer definida em Sub-task B.

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

## Regras

1. **Zero SQL inline** — toda persistência via `storage.write_adaptive_model(...)` (CONVENCOES §4)
2. **Pré-check backend é soft** — avisa mas não aborta (diferente de `/analista-conteudo`)
3. **Pipeline completo** — nunca pular etapa de frames ou transcrição
4. **Paralelismo** quando possível — frames + áudio juntos
5. **Path do Whisper nunca hardcodado** — usa env ou skill global `transcribe-audio`
6. **Frame analysis pode ser pesado** — avisar user antes de salvar em sheets/markdown
7. **Retornar id do adaptive_model** pra user encadear com `/roteiro-viral`
