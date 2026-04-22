# Mode Contract — DNA Operacional

Flag global do plugin sinaliza se user quer modo econômico (poupa tokens).

## Estado

CLAUDE.md do projeto tem linha:

```
## DNA Mode: full      # default
## DNA Mode: lowcost   # economia
```

Se ausente, assumir `full`.

## Como skill lê

Toda skill que tem operação "cara" (scraping, análise, geração múltipla) faz
no início:

```
MODE = ler CLAUDE.md linha "## DNA Mode: <x>" (default: full)
Se MODE == "lowcost": aplicar heurísticas do low-cost-heuristics.md §<skill>
```

Padrão de detecção via Bash silencioso:

```bash
if [ -f CLAUDE.md ]; then
  MODE=$(grep -E "^## DNA Mode:" CLAUDE.md | sed -E "s/.*DNA Mode: *([a-z]+).*/\1/" | head -1)
  [ -z "$MODE" ] && MODE="full"
else
  MODE="full"
fi
```

## Como skill sinaliza

Quando em lowcost, imprimir UMA LINHA no início do output:

```
💡 Modo lowcost ativo — resultado reduzido. /dna modo full pra ativar completo.
```

## Controle (comando `/dna modo`)

```
/dna modo          → mostra estado atual + opções + diff por skill
/dna modo lowcost  → seta CLAUDE.md `## DNA Mode: lowcost`
/dna modo full     → seta CLAUDE.md `## DNA Mode: full`
```

## Contrato pra skills

Toda skill que implementa heurística low-cost DEVE:

1. Ler a flag no início (antes de qualquer operação cara)
2. Imprimir linha-sinal quando em lowcost
3. Aplicar a heurística específica documentada em `low-cost-heuristics.md`
4. Entregar output ainda ÚTIL — lowcost NÃO pode virar lixo

Skills que NÃO são cost-sensitive não precisam implementar. Ver lista em
`low-cost-heuristics.md` §"Skills SEM heurística low-cost".

## Invariantes

- `full` é sempre o default — ausência da flag = full
- Lowcost nunca altera estrutura de dados persistida (CSV/Sheets/Supabase) — só reduz volume processado
- Toggle é idempotente — rodar `/dna modo full` várias vezes não quebra nada
- A flag vive em CLAUDE.md do PROJETO (não global no ~/.claude) — cada projeto escolhe
