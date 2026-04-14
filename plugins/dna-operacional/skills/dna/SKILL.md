---
name: dna
description: Menu central do plugin DNA Operacional. Mostra skills disponíveis agrupadas por categoria e jornadas completas. Use quando o usuário digitar "/dna", "menu do dna", "o que o dna faz", "quais skills do dna", "dna jornadas".
---

# /dna — Menu Central do Plugin DNA Operacional

Meta-skill do plugin. Não faz trabalho "real" — serve como **mapa** pras outras skills.

## Modos de uso

| Comando | O que faz |
|---|---|
| `/dna` | Banner + menu principal agrupado por categoria |
| `/dna jornadas` | 4 jornadas completas (criador / carrossel / inteligência competitiva / manutenção) |
| `/dna setup` | Alias explícito — roteia pra `/setup-projeto` |

## Comportamento

### Modo 1: `/dna` (sem args)

1. Renderizar banner ASCII:
   ```bash
   cat ${PLUGIN_ROOT}/assets/banner.txt
   ```
   Onde `${PLUGIN_ROOT}` resolve pra pasta do plugin no cache do Claude Code.

2. Imprimir menu principal (14 skills da v0.1.0 agrupadas por categoria):

```
╔══════════════════════════════════════════════════════════════════╗
║  🧬 Comandos disponíveis (v0.1.0)                                ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  🎯 SETUP                                                        ║
║     /setup-projeto .... Configure qualquer projeto               ║
║     /voz .............. Cria/evolui voz da marca                 ║
║                                                                  ║
║  🔍 PESQUISA                                                     ║
║     /pesquisa-diaria .......... Radar matinal BR (auto-schedule) ║
║     /pesquisa-concorrentes .... Mapeia concorrentes Instagram    ║
║     /raio-x-ads-concorrentes .. Briefing de ads competidores     ║
║                                                                  ║
║  🎬 CONTEÚDO (CICLO COMPLETO)                                    ║
║     /ideias-conteudo ..... 10 frameworks de hook                 ║
║     /analisar-video ...... Engenharia reversa → adaptive_models  ║
║     /roteiro-viral ....... Roteiros baseados em adaptive_models  ║
║     /carrossel-instagram . Carrosséis via Playwright             ║
║     /analista-conteudo ... Análise SQL do feed (Supabase only)   ║
║     /humanizer ........... Limpa IA + aplica voz do projeto      ║
║                                                                  ║
║  🤖 META                                                         ║
║     /auto-melhoria ....... Detecta padrões → propõe edits        ║
║     /dna-melhoria ........ Melhora as próprias skills do plugin  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

💡 Não sabe por onde começar? Digite:  /dna jornadas
```

3. Sugerir `/dna jornadas` como next step.

### Modo 2: `/dna jornadas`

Imprimir as 4 jornadas em boxes ASCII (detalhes no Step 7.1).

### Modo 3: `/dna setup`

Alias pra `/setup-projeto`. Na v0.1.0 (plugin vazio), `setup-projeto` ainda não tá migrada — retorna:

```
⚠️  /setup-projeto ainda não está disponível nesta versão (v0.1.0-alpha).
Previsão: v0.1.0 final (próxima sessão de migração).

Por enquanto, essa skill está na sua global (~/.claude/skills/setup-projeto/).
Digite /setup-projeto normalmente — o Claude Code invoca a versão global.
```

### Modo 4: fallback (arg não reconhecido)

Se user digita `/dna <palavra>` e palavra não bate com nenhum modo:
- Mostrar menu principal
- No topo, mensagem amigável: "Não reconheci '<palavra>'. Modos disponíveis: `/dna`, `/dna jornadas`, `/dna setup`. Mostrando menu principal."

**Sem fuzzy match automático** (decisão Spec 1 §6). Exact string match apenas.
