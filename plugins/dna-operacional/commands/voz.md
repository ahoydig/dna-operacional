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

<!-- preenchido em Task 3 -->

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
