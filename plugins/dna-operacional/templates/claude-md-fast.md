# Template CLAUDE.md — Setup Fast

10 seções mínimas geradas pelo `/setup-projeto fast` a partir das 8 perguntas essenciais.

```markdown
# Projeto <nome>

## Handle/Brand: @<handle>

## Nicho: <nicho em 1 frase>

## Público: <1 frase — quem é, idade aprox, o que quer>

## Oferta Principal: <nome da oferta> — R$ <preço>

## Voz: <adj1> / <adj2> / <adj3>

## Contato: <email>

## Storage Backend: csv
data_dir: ./data

## DNA Mode: full
# (default — troca pra lowcost rodando /dna modo lowcost)

## Setup: fast
# Rodar /setup-projeto completar pra expandir pro modo completo (23 perguntas)
```

## Observações

- Tudo preenchido com valores REAIS da entrevista fast (sem placeholder `<...>` no arquivo final).
- `Storage Backend: csv` é default — user pode trocar depois editando a linha ou rodando `/setup-projeto completar`.
- `DNA Mode: full` é sempre o inicial. `/dna modo lowcost` troca quando o user quer economizar.
- Marker `## Setup: fast` é lido pelo modo `completar` pra detectar que veio do fast e precisa expandir.

## Arquivos gerados em paralelo (não neste template)

- `reference/publico-alvo.md` — 5 seções mínimas (avatar macro + dores + desejos)
- `reference/voz-<handle>.md` — delegado pra `/voz criar` (user roda manual depois)
