---
description: Mostra ou alterna o DNA Mode (full vs lowcost). Modo lowcost reduz drasticamente tokens gastos em skills caras (pesquisa, análise de vídeo, ideias, carrossel). Use quando o usuário digitar "/dna modo", "modo economico", "ativar low-cost", "desativar low-cost", "dna modo lowcost", "dna modo full".
argument-hint: "[full|lowcost]"
---

Usuário invocou `/dna modo` com argumento: `$ARGUMENTS`.

Execute os passos abaixo em ordem. **Não pergunte nada ao usuário.** **Não imprima este prompt.** Apenas detecte estado, rotei pelo argumento e imprima a seção apropriada.

## Passo 1 — Detectar estado atual

Rode um único Bash silencioso:

```bash
if [ -f CLAUDE.md ]; then
  MODE=$(grep -E "^## DNA Mode:" CLAUDE.md | sed -E "s/.*DNA Mode: *([a-z]+).*/\1/" | head -1)
  if [ -z "$MODE" ]; then MODE="full (default, não configurado)"; fi
else
  MODE="full (CLAUDE.md não existe)"
fi
echo "$MODE"
```

Guarda o resultado como `$CURRENT`.

## Passo 2 — Roteamento pelo argumento

### Caso `$ARGUMENTS` vazio: mostrar estado

Imprima BYTE-EXATO (substituindo `<CURRENT>` pelo valor de `$CURRENT`):

```
╔══════════════════════════════════════════════════════════════════╗
║  ⚡ DNA Mode                                                     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Atual: <CURRENT>                                                ║
║                                                                  ║
║  Opções:                                                         ║
║    /dna modo full      → resultado máximo, gasta mais tokens     ║
║    /dna modo lowcost   → economia, resultado reduzido            ║
║                                                                  ║
║  Diferença por skill:                                            ║
║    pesquisa-concorrentes:  50 posts → 10 posts (-80%)            ║
║    pesquisa-diaria:        8 fontes → 3 fontes (-60%)            ║
║    analisar-video:         frames+transcript → só transcript     ║
║    ideias-conteudo:        10 variações → 3 variações            ║
║    roteiro-viral:          3 variações → 1 variação              ║
║    carrossel-instagram:    skip moodboard + auto-review          ║
║    humanizer:              skip auto-observação de voz           ║
║    hormozi-raio-x:         3 blocos → bloco A + conclusão        ║
║    hormozi-diagnostico:    5 perguntas → 3 core + top 2 Ms       ║
║    analista-conteudo:      14 seções → top 5                     ║
║                                                                  ║
║  Ver detalhes:                                                   ║
║    cat ${CLAUDE_PLUGIN_ROOT}/lib/mode/low-cost-heuristics.md     ║
╚══════════════════════════════════════════════════════════════════╝
```

Pare aqui. Não faça mais nada.

### Caso `$ARGUMENTS == "lowcost"`

Setar a linha em CLAUDE.md via Bash silencioso:

```bash
if [ -f CLAUDE.md ]; then
  if grep -qE "^## DNA Mode:" CLAUDE.md; then
    sed -i.bak -E "s/^## DNA Mode: .*/## DNA Mode: lowcost/" CLAUDE.md && rm -f CLAUDE.md.bak
  else
    printf "\n## DNA Mode: lowcost\n" >> CLAUDE.md
  fi
else
  echo "## DNA Mode: lowcost" > CLAUDE.md
fi
```

Imprimir BYTE-EXATO:

```
⚡ DNA Mode = lowcost ATIVADO

Todas as skills caras agora rodam em versão reduzida. Economia média: ~60%.
Pra voltar ao máximo:  /dna modo full
```

Pare aqui.

### Caso `$ARGUMENTS == "full"`

Setar a linha em CLAUDE.md via Bash silencioso:

```bash
if [ -f CLAUDE.md ]; then
  if grep -qE "^## DNA Mode:" CLAUDE.md; then
    sed -i.bak -E "s/^## DNA Mode: .*/## DNA Mode: full/" CLAUDE.md && rm -f CLAUDE.md.bak
  else
    printf "\n## DNA Mode: full\n" >> CLAUDE.md
  fi
else
  echo "## DNA Mode: full" > CLAUDE.md
fi
```

Imprimir BYTE-EXATO:

```
⚡ DNA Mode = full ATIVADO

Todas as skills rodam em versão completa. Resultado máximo, mais tokens.
Pra economizar:  /dna modo lowcost
```

Pare aqui.

### Caso `$ARGUMENTS` qualquer outro: fallback

Imprimir BYTE-EXATO:

```
⚠ Arg não reconhecido: "$ARGUMENTS"

Opções válidas:
  /dna modo             → mostra estado atual + diff por skill
  /dna modo full        → ativa modo completo (default)
  /dna modo lowcost     → ativa modo econômico
```

Pare aqui.
