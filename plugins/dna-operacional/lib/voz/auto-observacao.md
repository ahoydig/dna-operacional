# Auto-Observação da Voz

Engine que detecta sinais durante uso de outras skills do plugin e **propõe** evoluções da voz. Sempre confirma com o user antes de aplicar — nunca escreve sem autorização explícita.

## Pré-requisitos

- `reference/voz-<handle>.md` existe com frontmatter íntegro
- Campo `auto_observacao_ativa: true` no frontmatter (default na criação)
- Se `false` (após `/voz silenciar`): engine fica inerte — nenhum sinal é registrado nem proposto

## 4 sinais e thresholds (Spec §5.4)

### Sinal 1 — Expressão repetida em outputs

**Detecção:** user escreveu / aprovou outputs de skills que continham a mesma expressão `X` em **3 ocorrências distintas espalhadas em pelo menos 2 e até 5 sessões**.

**Tracking:** lib mantém contador em `reference/.voz-tracking.json`:

```json
{
  "expressoes_observadas": {
    "Pix": {
      "count": 3,
      "primeira_em": "2026-04-10",
      "ultima_em": "2026-04-13"
    }
  },
  "sessoes_analisadas": [
    "2026-04-10",
    "2026-04-11",
    "2026-04-12",
    "2026-04-13",
    "2026-04-14"
  ]
}
```

**Trigger:** quando `count >= 3` E `sessoes_analisadas` cobre **entre 2 e 5 datas distintas** (inclusive). O piso de 2 sessões evita falso positivo de brainstorm de 1 dia (ex: user escreveu "X" 3 vezes num único sprint — não reflete uso longitudinal).

**Ação:**

> "Notei que você usa 'X' bastante (3 vezes nos últimos 5 dias). Quer adicionar em 'Padrões sempre'? (y/n)"

Se `y`: disparar `/voz evoluir` programático com diff `+ "X"` em §3 Padrões "sempre".

### Sinal 2 — Hook salvo no pipeline

**Detecção:** `/ideias-conteudo` gerou hook `H`. User salvou no pipeline (storage `content_pipeline`) com `status` mudando pra `Roteirizado` ou `Gravado`.

**Threshold:** **1 ocorrência** (sinal forte — user já validou o hook ao roteirizar/gravar).

**Trigger imediato** (sem acumular tracking).

**Ação:**

> "Hook 'H' que você roteirizou — quer adicionar em 'Hooks validados' da voz? (y/n)"

### Sinal 3 — Edição manual repetida do humanizer

**Detecção:** user editou manualmente output do humanizer e a edição foi a **MESMA TRANSFORMAÇÃO** (ex: trocar "vamos" por "bora").

**Threshold:** **2 ocorrências** da mesma transformação.

**Tracking:** humanizer compara seu output com texto final salvo pelo user (em context window ou no projeto). Diff acumulado em `reference/.humanizer-edits.json`:

```json
{
  "transformacoes": {
    "vamos->bora": {
      "count": 2,
      "primeira_em": "2026-04-12",
      "ultima_em": "2026-04-14"
    }
  }
}
```

**Trigger:** mesma transformação com `count >= 2`.

**Ação:**

> "Vi que você corrige 'Y' pra 'Z' sempre. Atualizo a voz?
>  - Adicionar 'Z' em 'Padrões sempre'
>  - Adicionar 'Y' em 'Padrões nunca'
> (y/n)"

### Sinal 4 — Vídeo do próprio criador analisado

**Detecção:** `/analisar-video` rodou em vídeo cujo handle (extraído da URL Instagram/TikTok) bate com `voz-<handle>` do projeto atual.

**Threshold:**

- **1 ocorrência** se handle do vídeo == handle da voz do projeto
- **3 ocorrências com mesmo padrão** se vídeos de TERCEIROS (evita ruído de inspiração aleatória)

**Ação:**

> "Detectei novas aberturas que você usa nos vídeos: '<lista>'. Adiciona em 'Aberturas típicas'? (y/n)"

## Fluxo de execução

```
[skill X termina sua tarefa]
        │
        ▼
[verifica auto_observacao_ativa]
        │
        ├── false → skip (silenciada)
        └── true → continua
                │
                ▼
        [analisa output da skill X buscando os 4 sinais]
                │
                ▼
        [atualiza tracking JSON (sinais 1, 3, 4)]
                │
                ▼
        [se threshold atingido]
                │
                ▼
        [propõe ao user via mensagem inline]
                │
                ├── y → aplica via /voz evoluir programático (cria snapshot v<N+1>)
                └── n → não aplica (mas mantém tracking pra futuro)
```

## Hooks de integração com outras skills (entregues em Plans 4-5)

Plan 3 **documenta** o engine. Plans 4-5 implementam os hooks reais nas skills:

| Skill | Hook | Sinal disparado |
|---|---|---|
| `humanizer` | output gerado | Sinal 1 (rastreia expressões) + Sinal 3 (compara edições) |
| `ideias-conteudo` | hook salvo no pipeline (status → Roteirizado/Gravado) | Sinal 2 |
| `analisar-video` | análise concluída + handle bate com voz | Sinal 4 |

Em v0.1.0-alpha.5 nenhuma dessas skills dispara os hooks — o engine fica dormente até Plans 4-5 plugarem as skills migradas.

## Privacidade

Tracking JSONs (`reference/.voz-tracking.json`, `reference/.humanizer-edits.json`) ficam **SOMENTE no projeto do user** — plugin nunca envia upstream.

User pode limpar a qualquer momento:

```bash
rm reference/.voz-tracking.json reference/.humanizer-edits.json
```

Recomendação: adicionar `reference/.voz-tracking.json` e `reference/.humanizer-edits.json` ao `.gitignore` do projeto (skill `setup-projeto` cuida disso no Plan 4).
