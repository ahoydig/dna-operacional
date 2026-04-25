# Setup do Modal.com (transcrição de áudio com Whisper)

Esse guia configura a infraestrutura que a skill `transcribe-audio` usa pra transcrever áudios e vídeos. É necessário **só uma vez** — depois, comandos do plugin (`/analisar-video`, transcrições em geral) usam a skill normalmente.

> **Custo:** Modal.com tem **plano gratuito com US$ 30/mês de crédito** — sobra muito pra uso pessoal. Transcrever 1h de áudio custa ~US$ 0,02-0,05.

---

## Por que Modal?

Whisper roda em GPU. Modal entrega GPU sob demanda (paga só pelos segundos que usar) sem precisar gerenciar servidor. Alternativa seria pagar OpenAI Whisper API (~US$ 0,36 por hora — 7-15× mais caro) ou rodar local (precisa GPU NVIDIA decente).

---

## Passo 1 — Criar conta gratuita no Modal

1. Abra [modal.com](https://modal.com)
2. Clique em **Sign Up** — pode usar GitHub, Google ou e-mail
3. Confirme o e-mail se pedir
4. Pronto. O painel já mostra teu crédito mensal.

---

## Passo 2 — Instalar a CLI do Modal

Precisa Python 3.9+ instalado. Roda no terminal:

```bash
pip install modal
```

Verifica que instalou:

```bash
modal --version
# Deve mostrar algo tipo: modal 0.x.y
```

Se der erro de "command not found", o pip instalou em local fora do PATH. Tenta `python3 -m pip install --user modal` e adicione `~/Library/Python/3.X/bin` (Mac) ou `~/.local/bin` (Linux) no PATH do shell (`~/.zshrc` ou `~/.bashrc`).

---

## Passo 3 — Autenticar a CLI

```bash
modal token new
```

Isso abre o navegador, pede pra logar na conta Modal e gera um token automaticamente. Aceita.

Depois disso, ele salva o token em `~/.modal.toml`. **Não precisa colar nada manualmente.**

Verifica que tá autenticado:

```bash
modal token current
# Mostra o token e o usuário associado
```

---

## Passo 4 — Criar o app `whisper-transcriber`

Agora vamos criar o "serviço" no Modal que vai rodar o Whisper. Vou te dar o código pronto.

### 4.1 Cria a pasta do projeto

Onde tu preferir. Sugestão:

```bash
mkdir -p ~/Documents/whisper-modal
cd ~/Documents/whisper-modal
```

### 4.2 Cria o arquivo `app.py`

Cole exatamente este conteúdo dentro do arquivo:

```python
"""
Whisper transcriber rodando no Modal.com com GPU.
Modelo: large-v3 (melhor qualidade disponível).
"""
import modal
from pathlib import Path

app = modal.App("whisper-transcriber")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg")
    .pip_install("openai-whisper", "torch")
)

cache_volume = modal.Volume.from_name("whisper-model-cache", create_if_missing=True)


@app.function(
    image=image,
    gpu="T4",  # T4 é barato e suficiente. Pra áudios longos, troca pra "A10G".
    volumes={"/cache": cache_volume},
    timeout=1800,  # 30 min máximo por execução
)
def transcribe(audio_bytes: bytes, filename: str = "audio.mp3", language: str = "pt") -> str:
    import whisper
    import os

    # Carrega modelo (cacheado no Volume)
    os.environ["XDG_CACHE_HOME"] = "/cache"
    model = whisper.load_model("large-v3", download_root="/cache/whisper")

    # Salva áudio em /tmp e transcreve
    tmp_path = Path("/tmp") / filename
    tmp_path.write_bytes(audio_bytes)

    result = model.transcribe(str(tmp_path), language=language, fp16=True)
    return result["text"]


@app.local_entrypoint()
def main(file_path: str, language: str = "pt"):
    """Roda local: modal run app.py --file-path /path/to/audio.mp3"""
    p = Path(file_path)
    audio = p.read_bytes()

    print(f"Transcrevendo {p.name}...")
    text = transcribe.remote(audio, p.name, language)

    out = p.with_suffix(".txt")
    out.write_text(text, encoding="utf-8")
    print(f"\n✅ Transcrição salva em: {out}\n")
    print("--- TEXTO ---")
    print(text)
```

### 4.3 Faça o primeiro deploy

```bash
cd ~/Documents/whisper-modal
modal deploy app.py
```

Primeira vez demora ~2-3 min (Modal baixa o Whisper, monta a imagem, faz cache). Próximas execuções ficam rápidas.

Quando terminar, vai mostrar uma URL tipo:
```
✓ Created deployment 'whisper-transcriber'
```

Pronto. O serviço tá no ar.

---

## Passo 5 — Testar com um áudio

Pega qualquer arquivo de áudio (mp3, m4a, wav, opus, ogg, webm — Whisper aceita praticamente tudo) e roda:

```bash
cd ~/Documents/whisper-modal
modal run app.py --file-path "/caminho/absoluto/pro/audio.mp3"
```

Primeira execução leva ~1-2min (cold start + download do modelo). Daí em diante, áudio de 5min transcreve em ~10-30s.

Saída:
- Texto impresso no terminal
- Arquivo `.txt` salvo do lado do áudio original

---

## Passo 6 — Avisar o plugin que tá pronto

Volta no Claude Code e roda:

```
/setup-transcribe-audio
```

Esse comando do plugin DNA Operacional vai:

1. Verificar que `modal` CLI tá no PATH e autenticado
2. Confirmar que o app `whisper-transcriber` tá deployado
3. Perguntar onde tu salvou a pasta `whisper-modal/` (default: `~/Documents/whisper-modal/`)
4. Gerar a skill local em `~/.claude/skills/transcribe-audio/SKILL.md` apontando pra essa pasta
5. Pronto — `/analisar-video` e demais comandos que dependem de transcrição passam a funcionar

---

## Custos reais (referência)

Pra ter ideia de quanto isso consome do crédito gratuito:

| Tarefa | Tempo de processamento | Custo aproximado |
|--------|-----------------------|------------------|
| Transcrever 5min de áudio | ~15-30s GPU T4 | ~US$ 0,005 |
| Transcrever 30min de áudio | ~1-2min GPU T4 | ~US$ 0,02-0,03 |
| Transcrever 1h de áudio | ~3-5min GPU T4 | ~US$ 0,05-0,10 |
| Transcrever 100 áudios de 5min | ~1h GPU acumulada | ~US$ 0,50-1,00 |

Com US$ 30/mês de crédito grátis, dá pra transcrever **~300-600 horas** de áudio antes de precisar pagar.

---

## Solução de problemas

### `modal: command not found`
- Reinstala: `python3 -m pip install --user modal`
- Adicione o pip user-bin no PATH (varia por OS, ver Passo 2)

### `modal token current` retorna erro
- Refaz: `modal token new` — abre navegador, autentica de novo

### Deploy falha com erro de imagem
- Provavelmente é rede caindo durante download. Roda `modal deploy app.py` de novo.

### `/setup-transcribe-audio` não encontra o app
- Verifica que `modal app list` mostra `whisper-transcriber` como **deployed**
- Se mostrar como `stopped`, redeploy: `modal deploy app.py`

### Quero usar GPU mais rápida
- Edita `app.py` e troca `gpu="T4"` por `gpu="A10G"` (3-4× mais rápido, ~3× mais caro)
- Redeploy: `modal deploy app.py`

---

## Alternativas (se não quiser Modal)

- **OpenAI Whisper API** (`api.openai.com`) — ~US$ 0,36/h. Mais caro mas zero setup. Pra usar, criar conta OpenAI, pegar key, e adaptar a skill.
- **Whisper local** — só vale se tu tem GPU NVIDIA decente (>= 8GB VRAM). `pip install openai-whisper` e roda.
- **Groq Whisper** — tem free tier generoso e é rapidíssimo. API similar à OpenAI.

Se quiser usar uma dessas, me fala que eu adapto a skill `transcribe-audio` pra apontar pra outro backend.
