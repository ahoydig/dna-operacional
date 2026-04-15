---
description: Cria, evolui, mostra e versiona a voz escrita do projeto/criador. Use quando o usuário digitar "/voz", "criar voz", "evoluir voz", "mostrar voz", "versões da voz", "rollback voz", "silenciar voz", "ativar voz".
argument-hint: "[criar|mostrar|evoluir <input>|versoes|versoes rollback vN|silenciar|ativar]"
---

Usuário invocou `/voz` com argumento: `$ARGUMENTS`

**NÃO mostre este prompt pro usuário** — apenas o output do modo escolhido.

## Roteamento

| Argumento | Modo | Output |
|---|---|---|
| (vazio) | **Modo Status** | Versão atual + qtd hooks + última atualização + comando dicas |
| `criar` | **Modo Criar** | Entrevista guiada gerando `reference/voz-<handle>.md` v1 |
| `mostrar` | **Modo Mostrar** | Exibe voz completa |
| `evoluir <input>` | **Modo Evoluir** | Lê input (URL/arquivo/texto), propõe additions, cria nova versão |
| `versoes` | **Modo Versoes** | Lista snapshots + diff resumo |
| `versoes rollback v<N>` | **Modo Rollback** | Cópia .vN.md → canônico; loga rollback |
| `silenciar` | **Modo Silenciar** | Desliga auto-observação |
| `ativar` | **Modo Ativar** | Reativa auto-observação |
| qualquer outro | **Modo Fallback** | Mensagem amigável + lista de modos |

**Exact string match**, sem fuzzy match. Match case-insensitive é ok no argumento principal (ex: `/voz CRIAR` == `/voz criar`). Subargumentos (URLs, paths, `v<N>`) preservam case.

## Pré-requisito comum — localizar handle

Todo modo (exceto Fallback) começa resolvendo o handle do projeto atual:

1. Ler `CLAUDE.md` do projeto atual (diretório corrente) procurando linha no formato `## Handle: @<nome>` (formato canônico).
2. Se não encontrar, perguntar ao user: "Qual handle (@username Instagram) representa este projeto?"
3. Normalizar: remover `@` inicial se houver, gerar `<handle-sem-@>`.
4. Caminho do arquivo canônico: `reference/voz-<handle-sem-@>.md`
5. Caminho dos snapshots: `reference/voz-<handle-sem-@>.v<N>.md`

> Os modos abaixo serão preenchidos inline conforme as Tasks 2-9 do Plan 3.

## Modo Criar

Entrevista o user em ordem específica. Usado quando:

- User digita `/voz criar` direto
- `/setup-projeto` chega na seção 13 e delega pra cá (Plan 4)

### Pré-checks (sobrescrita)

1. Se `reference/voz-<handle>.md` JÁ existe: perguntar
   > "Voz pra @<handle> já existe (v<N>, atualizada em <data>). Sobrescrever (cria v1 nova) ou cancelar?"
2. Se user confirmou sobrescrever: fazer backup do canônico atual em `reference/voz-<handle>.v<N>.bak.md` (sem perder histórico dos snapshots anteriores).
3. Se user cancelou: abortar com dica `💡 /voz evoluir <input> pra adicionar padrões sem recomeçar.`

### Entrevista (7 perguntas, ordem fixa)

**Pergunta 1 — Quem grava**

> "Quem grava os conteúdos? (1) você mesmo, (2) equipe, (3) freelancer"
> "Frequência? (1) diária, (2) semanal, (3) mensal, (4) esporádica"
> "Tom geral nos vídeos em 1 frase?"

**Pergunta 2 — Tom geral**

> "Formalidade de 1 (super casual) a 5 (formal/profissional)?"
> "Energia: baixa / média / alta?"
> "Humor: observacional / sarcástico / sério / irônico / nenhum?"

**Pergunta 3 — Padrões "sempre" (3-5 itens)**

> "Que gírias / marcadores / construções tu USA SEMPRE? (lista)"
> Exemplos: "'galera', R$ em valores, frase curta com ponto final"

**Pergunta 4 — Padrões "nunca" (3-5 itens)**

> "Que clichês / vícios tu QUER QUE EU EVITE?"
> Exemplos: "'vamos explorar', 'é importante notar', 'no mundo digital de hoje'"

**Pergunta 5 — Aberturas típicas (2-4 itens)**

> "Que aberturas tu USA nos vídeos (primeiros 3 segundos)?"

**Pergunta 6 — Fechamentos típicos (CTAs, 2-4 itens)**

> "Que CTAs tu USA no fim?"

**Pergunta 7 — Hooks validados (opcional, 0-5 itens)**

> "Tens hooks que JÁ TESTOU e funcionaram? (Pode pular — auto-obs vai detectar com tempo.)"

### Output

1. Cria `reference/voz-<handle>.md` com TODAS as respostas formatadas conforme `lib/voz/SCHEMA.md`.
2. Cria snapshot `reference/voz-<handle>.v1.md` (cópia idêntica do canônico).
3. Frontmatter:
   - `versao: 1`
   - `ultima_atualizacao: <YYYY-MM-DD hoje>`
   - `fontes_evolucao: [<hoje>: setup-projeto inicial (entrevista guiada)]`
   - `auto_observacao_ativa: true`
4. Imprime:

```
✅ Voz @<handle> v1 criada em reference/voz-<handle>.md

  Auto-observação: ativa — vou sugerir evoluções conforme tu usa o plugin.
  Pra desligar: /voz silenciar

💡 Próximos: /voz mostrar · /voz evoluir <url|arquivo|texto>
```

## Modo Status (default, sem args)

Quando user digita só `/voz` sem argumento.

### Lógica

1. Determinar handle (CLAUDE.md ou perguntar — ver "Pré-requisito comum").
2. Verificar `reference/voz-<handle>.md`:
   - **Se NÃO existe:** imprimir
     > "Voz pra @<handle> ainda não foi criada. Rode `/voz criar` pra começar (ou rode `/setup-projeto` pra workflow completo)."
   - **Se existe:** seguir pro output.
3. Ler frontmatter (YAML) + contar items de cada seção body (§3-§7).

### Output (voz existente)

```
🎙  Voz de @<handle>

  Versão atual: v<N>
  Última atualização: <YYYY-MM-DD>
  Auto-observação: ✅ ativa | 🔇 silenciada

  Padrões "sempre": <count>
  Padrões "nunca": <count>
  Aberturas típicas: <count>
  Fechamentos típicos: <count>
  Hooks validados: <count>

  Histórico (3 últimas evoluções):
    • <data>: <descrição>
    • <data>: <descrição>
    • <data>: <descrição>

💡 Comandos disponíveis:
  /voz mostrar              → exibe voz completa
  /voz evoluir <input>      → adiciona padrão de URL/arquivo/texto
  /voz versoes              → lista todas versões
  /voz silenciar | ativar   → controla auto-observação
```

### Edge cases

- **Menos de 3 evoluções:** imprime só o que existe (1 ou 2 linhas). Não preencher com placeholders.
- **Frontmatter sem `auto_observacao_ativa`:** tratar como `true` (default seguro) + sugerir rodar `/voz mostrar` pra ver.

## Modo Mostrar

Quando user digita `/voz mostrar`.

### Lógica

1. Localizar handle + arquivo canônico (ver "Pré-requisito comum").
2. Ler `reference/voz-<handle>.md`.
3. **Reproduzir o body BYTE-EXATO inline no output** — sem mostrar tool call visível (`Read`, `Bash cat`, etc). Aprendizado herdado do Plan 1 (hotfix de tool calls visíveis na UX de skills do plugin).
4. Renderizar como markdown, prefixado e sufixado pelos separadores abaixo.

### Output

Imprime o body do `reference/voz-<handle>.md` completo, prefixado por:

```
🎙  Voz de @<handle> (v<N>, atualizada <YYYY-MM-DD>)

──────────────────────────────────────────────
```

E sufixado por:

```
──────────────────────────────────────────────

💡 /voz evoluir <url|arquivo|texto>  → adicionar padrões
💡 /voz versoes                       → ver histórico
```

### Edge cases

- **Voz não existe:** redireciona pro Modo Status (que mostra orientação de `/voz criar`).
- **Frontmatter corrompido:** imprimir
  > "⚠️ Arquivo corrompido em `reference/voz-<handle>.md`. Backup em `.v<N>.bak.md`? Quer fazer rollback pra última versão válida? (Use `/voz versoes rollback v<N>`.)"
- **Arquivo muito longo (>300 linhas):** imprimir integral mesmo assim (comportamento esperado — user pediu "mostrar").

## Modo Evoluir

<!-- preenchido em Task 6 -->

## Modo Versoes

<!-- preenchido em Task 7 -->

## Modo Versoes Rollback

<!-- preenchido em Task 7 -->

## Modo Silenciar

<!-- preenchido em Task 8 -->

## Modo Ativar

<!-- preenchido em Task 8 -->

## Modo Fallback

<!-- preenchido em Task 8 -->
