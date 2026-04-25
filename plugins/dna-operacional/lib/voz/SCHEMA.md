# Schema — `reference/voz-<handle>.md`

Fonte da verdade da estrutura do arquivo de voz. Skills `voz`, `humanizer` e `auto-observacao` consomem este schema.

> **Nota sobre extensão ao Spec §5.2:** o campo `auto_observacao_ativa` (bool) NÃO aparece explícito no Spec 2 §5.2, mas é necessário pra suportar os modos `/voz silenciar` e `/voz ativar` (Spec §5.4 menciona o comportamento de silenciar/ativar, sem fixar o nome do campo no frontmatter). Adicionado aqui como **extensão obrigatória** da v0.1.0-alpha.5 — será refletido no Spec 2 na próxima revisão.

## Frontmatter (YAML)

```yaml
---
handle: "@<seuhandle>"
versao: 3
ultima_atualizacao: 2026-04-14
fontes_evolucao:
  - 2026-04-10: setup-projeto inicial (entrevista guiada)
  - 2026-04-12: evoluiu via youtube.com/watch?v=ABC123
  - 2026-04-14: detectou padrão "Pix" (auto-obs sinal #1)
auto_observacao_ativa: true
---
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `handle` | string | sim | `@username` Instagram com `@` |
| `versao` | int | sim | Versão atual (incrementa a cada `/voz evoluir`) |
| `ultima_atualizacao` | date | sim | YYYY-MM-DD |
| `fontes_evolucao` | list | sim | Histórico das mudanças com data + descrição |
| `auto_observacao_ativa` | bool | sim | Default `true`. `/voz silenciar` muda pra `false`. Extensão vs Spec §5.2. |

## Body (markdown)

7 seções obrigatórias, na ordem exata abaixo:

### 1. Quem grava

- **Responsável:** dono / equipe / freelancer
- **Frequência:** diária / semanal / mensal / esporádica
- **Tom nos vídeos:** descritivo curto (1 frase)

### 2. Tom geral

- **Formalidade:** 1 (super casual) → 5 (formal/profissional)
- **Energia:** baixa / média / alta
- **Humor:** observacional / sarcástico / sério / irônico / nenhum

### 3. Padrões "sempre"

Lista de gírias, marcadores e construções que devem aparecer. Ex:

- "galera"
- R$ em valores (nunca US$)
- frase curta + ponto final (não vírgula longa)

### 4. Padrões "nunca"

Lista de vícios e clichês a evitar. Ex:

- "vamos explorar"
- "é importante notar que"
- "no mundo digital de hoje"

### 5. Aberturas típicas (primeiros 3 segundos)

Lista de hooks/aberturas que o criador usa. Ex:

- "Olha isso aqui, gente"
- "Para de fazer X"
- "Ninguém fala sobre isso"

### 6. Fechamentos típicos (CTA)

Lista de call-to-actions. Ex:

- "Manda mensagem"
- "Comenta aqui"
- "Link na bio"

### 7. Hooks validados (literais)

Lista de hooks que o criador JÁ TESTOU e funcionaram. Auto-obs pode adicionar via sinal #2 (hook salvo no pipeline com `status` = Roteirizado/Gravado).

Ex:

- "Eu testei [X] por 30 dias e me arrependi"
- "Pix é a coisa mais subestimada do Brasil"

## Variantes / Edge cases

- **Sem voz definida:** humanizer roda só com regras genéricas anti-IA (não falha).
- **Múltiplos handles no mesmo projeto:** cada um tem seu `reference/voz-<handle>.md`. Skills perguntam qual usar quando ambíguo.
- **Snapshot vs canônico:** `voz-<handle>.md` é **cópia direta** do snapshot mais recente (`voz-<handle>.v<N>.md`). Sem symlink — sempre cópia (Spec §5.5). Evita problemas de portabilidade entre OS e de backups.
- **Frontmatter corrompido:** skills devem detectar e sugerir rollback pra snapshot íntegro (`/voz versoes rollback v<N>`).
- **Seções vazias:** aceitáveis no momento de criação (ex: §7 Hooks validados pode começar vazia). Auto-obs preenche ao longo do tempo.
