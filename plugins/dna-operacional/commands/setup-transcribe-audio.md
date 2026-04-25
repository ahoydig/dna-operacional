---
description: Configura a skill `transcribe-audio` localmente — valida que o user fez o setup do Modal.com (CLI instalada, autenticado, app whisper-transcriber deployado) e gera ~/.claude/skills/transcribe-audio/SKILL.md apontando pra pasta correta. Use quando digitar "/setup-transcribe-audio", "configurar transcribe", "ativar transcrição", "ativar whisper".
argument-hint: ""
---

Usuário invocou `/setup-transcribe-audio`.

Esse comando configura a skill `transcribe-audio` no ambiente local do user. Pré-requisito: ter feito o setup do Modal.com seguindo `${CLAUDE_PLUGIN_ROOT}/docs/SETUP-MODAL.md`.

## Passo 1 — Verificar pré-requisitos

Rodar checks em sequência. Para cada um, se falhar, **abortar com instrução clara** apontando pro guia.

### 1.1 — Modal CLI instalada

```bash
command -v modal && modal --version
```

Se falhar:
> ❌ Modal CLI não encontrada no PATH. Antes de rodar este comando, segue o setup completo em `${CLAUDE_PLUGIN_ROOT}/docs/SETUP-MODAL.md` (passos 1 a 5). É grátis, leva ~10 minutos.

### 1.2 — CLI autenticada

```bash
modal token current 2>&1 | head -3
```

Se retornar erro ou vazio:
> ❌ Modal CLI não autenticada. Roda `modal token new` no terminal — abre o navegador, autentica e volta aqui.

### 1.3 — App `whisper-transcriber` deployado

```bash
modal app list 2>&1 | grep whisper-transcriber
```

Se não aparecer ou aparecer como `stopped`:
> ❌ App `whisper-transcriber` não está deployado. Volta na pasta onde tu salvou o `app.py` (ver passo 4 do guia) e roda `modal deploy app.py`.

## Passo 2 — Localizar a pasta do whisper-modal

Perguntar via `AskUserQuestion`:

> "Onde tu salvou a pasta `whisper-modal` (com o `app.py`)?"
>
> Default sugerido: `~/Documents/whisper-modal/`

Validar que o path existe e contém `app.py`:

```bash
WHISPER_DIR="<resposta>"
test -f "$WHISPER_DIR/app.py" && echo "ok" || echo "não encontrado"
```

Se não encontrar, perguntar de novo. Limite 3 tentativas, depois sugerir refazer o passo 4 do guia.

## Passo 3 — Gerar a skill local

Criar `~/.claude/skills/transcribe-audio/SKILL.md` com o conteúdo abaixo, **substituindo `<WHISPER_DIR>` pelo path absoluto** (expandindo `~` se vier assim).

```bash
mkdir -p ~/.claude/skills/transcribe-audio
```

Conteúdo do `SKILL.md`:

```markdown
---
name: transcribe-audio
description: Transcreve arquivos de áudio usando Whisper large-v3 no Modal.com. Use quando o usuário pedir para transcrever áudio, converter áudio em texto, ouvir um áudio, ou quando houver arquivos de áudio (.opus, .mp3, .wav, .m4a, .ogg, .flac, .webm) no contexto. Também ativa para "transcrever", "transcrição", "transcribe", "o que diz esse áudio", "áudio para texto".
---

# Transcribe Audio Skill

Transcreve arquivos de áudio usando Whisper large-v3 rodando em GPU no Modal.com.

## Pré-requisitos
- Modal CLI instalado e autenticado (`modal` no PATH)
- App `whisper-transcriber` deployado no Modal
- Pasta do projeto local: `<WHISPER_DIR>`

## Como usar

### Transcrição de um arquivo
\`\`\`bash
cd <WHISPER_DIR> && modal run app.py --file-path "<caminho-absoluto-do-audio>"
\`\`\`

### Parâmetros
- `--file-path`: caminho absoluto do arquivo (obrigatório)
- `--language`: idioma (default `pt`)

### Formatos suportados
.opus, .mp3, .wav, .m4a, .ogg, .flac, .webm, .wma, .aac

### Output
- Texto impresso no terminal
- Arquivo `.txt` salvo ao lado do áudio (mesmo nome)

## Fluxo da skill

1. **Identificar arquivos**: Use Glob/Read pra encontrar áudios no contexto do user
2. **Transcrever**: `modal run` pra cada um
3. **Apresentar**: mostre a transcrição no chat
4. **Salvar**: o `.txt` é salvo automaticamente

## Notas
- Primeira execução pode demorar ~1-2min (cold start)
- Execuções subsequentes: ~10-30s
- Custo: ~US$ 0,02-0,05 por hora de áudio (T4)
- Free tier do Modal cobre ~300-600h/mês
```

> **Importante:** os blocos com triplo backtick aninhado precisam ser escapados (`\`\`\``) só pro template — quando escrever no arquivo final, usa triplo backtick normal.

## Passo 4 — Smoke test (opcional)

Perguntar: "Quer rodar um teste com um áudio agora pra confirmar que tá funcionando?"

Se sim, pedir um caminho de áudio e rodar:

```bash
cd <WHISPER_DIR> && modal run app.py --file-path "<audio_path>"
```

Se transcrever com sucesso:
> ✅ Skill `transcribe-audio` configurada e validada. Agora `/analisar-video` e qualquer pedido de transcrição funcionam direto.

## Passo 5 — Output final

```
╔══════════════════════════════════════════════════════════════════╗
║  ✅ transcribe-audio configurada                                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Skill local:    ~/.claude/skills/transcribe-audio/SKILL.md      ║
║  Backend:        Modal.com (whisper-transcriber)                 ║
║  Pasta projeto:  <WHISPER_DIR>                                   ║
║                                                                  ║
║  Comandos do plugin que agora funcionam:                         ║
║    • /analisar-video                                             ║
║    • Qualquer pedido de transcrição                              ║
║                                                                  ║
║  Custo aproximado: US$ 0,02-0,05 por hora de áudio.              ║
║  Free tier do Modal: ~300-600h/mês.                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Erros comuns

| Situação | Ação |
|----------|------|
| `modal` ausente | Apontar pro `docs/SETUP-MODAL.md` passo 2 |
| Token inválido | `modal token new` |
| App não deployado | `cd <WHISPER_DIR> && modal deploy app.py` |
| Pasta whisper-modal não existe | Refazer passo 4 do guia |
| Skill já existe (~/.claude/skills/transcribe-audio/) | Confirmar se sobrescreve antes de gravar |
