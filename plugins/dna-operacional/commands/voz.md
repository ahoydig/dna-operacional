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

<!-- preenchido em Task 4 -->

## Modo Mostrar

<!-- preenchido em Task 5 -->

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
