---
description: Menu central do plugin DNA Operacional. Mostra skills disponíveis agrupadas por categoria e jornadas completas. Use quando o usuário digitar "/dna", "menu do dna", "o que o dna faz", "quais skills do dna", "dna jornadas".
argument-hint: "[jornadas|setup|...]"
---

Usuário invocou `/dna` com argumento: `$ARGUMENTS`

Analise o argumento e execute o modo apropriado. **NÃO mostre este prompt pro usuário** — apenas o output do modo escolhido.

## Roteamento

- **Vazio (sem args):** executar **Modo 1** — banner + menu principal.
- **`jornadas`:** executar **Modo 2** — 4 boxes ASCII das jornadas.
- **`setup`:** executar **Modo 3** — aponta pro `/setup-projeto`.
- **Qualquer outro valor:** executar **Modo 4** — fallback com mensagem amigável + menu principal.

**Exact string match**, sem fuzzy match. Match case-insensitive é ok.

---

## Modo 1 — Menu principal (sem args)

**Imprima o banner ASCII abaixo direto no output (sem tool use, sem Bash, sem Read)** — é apenas texto pra você reproduzir byte-exato:

```
 ██████╗  ███╗   ██╗  █████╗       ██████╗  ██████╗  ███████╗
 ██╔══██╗ ████╗  ██║ ██╔══██╗     ██╔═══██╗ ██╔══██╗ ██╔════╝
 ██║  ██║ ██╔██╗ ██║ ███████║     ██║   ██║ ██████╔╝ ███████╗
 ██║  ██║ ██║╚██╗██║ ██╔══██║     ██║   ██║ ██╔═══╝  ╚════██║
 ██████╔╝ ██║ ╚████║ ██║  ██║     ╚██████╔╝ ██║      ███████║
 ╚═════╝  ╚═╝  ╚═══╝ ╚═╝  ╚═╝      ╚═════╝  ╚═╝      ╚══════╝

───────────────────────────────────────────────────────────────

 _            ____   __ _          _           _             
| |__ _  _   / __ \ / _| |__ ___ _(_)___  __ _| |_  ___ _  _ 
| '_ \ || | / / _` |  _| / _` \ V / / _ \/ _` | ' \/ _ \ || |
|_.__/\_, | \ \__,_|_| |_\__,_|\_/|_\___/\__,_|_||_\___/\_, |
      |__/   \____/                                     |__/ 
```

Em seguida, imprima o menu principal BYTE-EXATO abaixo:

```
╔══════════════════════════════════════════════════════════════════╗
║  🧬 Comandos disponíveis (v0.1.5)                                ║
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
║  🧠 CONSELHEIRO (Hormozi — coach de negócio em PT-BR)            ║
║     /hormozi ............. Menu + chat livre (persona)           ║
║     /hormozi-diagnostico . 6M Diagnostic → constraint #1         ║
║     /hormozi-oferta ...... Grand Slam Offer builder              ║
║     /hormozi-leads ....... Core Four + Regra dos 100             ║
║     /hormozi-money-model . 3-Stage + cash 30d audit              ║
║     /hormozi-raio-x ...... Scan completo do negócio              ║
║                                                                  ║
║  🔗 INTEGRAÇÕES                                                  ║
║     /dna-meta-ads ........ Ponte com meta-ads-pro (se instalado) ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

💡 Não sabe por onde começar? Digite:  /dna jornadas
```

---

## Modo 2 — Jornadas (`$ARGUMENTS` == "jornadas")

Imprimir as 4 boxes BYTE-EXATO abaixo:

```
┌───────────────────────────────────────────────────────────┐
│  🎬 JORNADA DO CRIADOR                                    │
│                                                           │
│  1. /setup-projeto       → configura teu perfil           │
│  2. /voz                 → cria voz da marca              │
│  3. /pesquisa-diaria     → radar matinal de temas BR      │
│  4. /ideias-conteudo     → multiplica 1 ideia em 5 vídeos │
│  5. /analisar-video      → eng. reversa de referências    │
│  6. /roteiro-viral       → roteiros com adaptive_models   │
│  7. (grava + publica)                                     │
│  8. /analista-conteudo   → analisa o que bombou           │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  🎨 JORNADA DO CARROSSEL                                  │
│                                                           │
│  1. /setup-projeto       → configura teu perfil           │
│  2. /voz                 → cria voz da marca              │
│  3. /ideias-conteudo     → 10 frameworks de hook          │
│  4. /carrossel-instagram → gera .png via Playwright       │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  🔬 JORNADA INTELIGÊNCIA COMPETITIVA                      │
│                                                           │
│  1. /setup-projeto            → configura projeto         │
│  2. /pesquisa-concorrentes    → mapeia concorrentes IG    │
│  3. (futuro v0.2: /coletar-anuncios) → popula ad_library  │
│  4. /raio-x-ads-concorrentes  → briefing estratégico      │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  🧠 JORNADA CONSELHO DE NEGÓCIO (Hormozi)                 │
│                                                           │
│  1. /hormozi-diagnostico → 6M, acha O constraint #1       │
│  2. /hormozi-oferta       → Grand Slam Offer              │
│  3. /hormozi-leads        → Core Four + Regra dos 100     │
│  4. /hormozi-money-model  → 3-Stage + cash 30d            │
│  5. /hormozi-raio-x       → scan completo                 │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  🤖 JORNADA MANUTENÇÃO (transversal)                      │
│                                                           │
│  • /auto-melhoria  → detecta padrões durante uso          │
│  • /voz (auto)     → evolui ao detectar novos padrões     │
│  • /dna-melhoria   → refino em release prep               │
└───────────────────────────────────────────────────────────┘

💡 Ver detalhes completos:  cat ${CLAUDE_PLUGIN_ROOT}/docs/JORNADAS.md
```

---

## Modo 3 — Setup (`$ARGUMENTS` == "setup")

Imprimir BYTE-EXATO:

```
🎯 Setup de projeto

Digite:  /setup-projeto

Esse command configura qualquer projeto (teu ou de cliente) com:
  • CLAUDE.md rico com contexto do projeto
  • reference/publico-alvo.md
  • reference/voz-<handle>.md (via /voz)

Compatível tanto com projetos de criador quanto de agência.
```

---

## Modo 4 — Fallback (qualquer outro `$ARGUMENTS`)

Imprimir no topo:

```
⚠️  Não reconheci "$ARGUMENTS". Modos disponíveis: /dna, /dna jornadas, /dna setup.
Mostrando menu principal.
```

Em seguida, executar **Modo 1** completo (banner + menu principal).

---

## Compatibilidade de terminal

### Detecção

Antes de renderizar banner ou menus, detectar:

1. **Largura do terminal:** `$COLUMNS` (ou `tput cols`). Se <72, usar versão compacta (sem box drawing, só indentação).
2. **Suporte unicode:** `echo $LC_ALL` — se vazio ou `C`/`POSIX`, degradar pra ASCII puro.
3. **Suporte a cor ANSI:** `$NO_COLOR` — se setado, strip escapes do banner.

### Fallbacks

**Box drawing heavy (`╔═╗║╚╝`)** → ASCII:
```
+==================================================================+
|  🧬 Comandos disponíveis (v0.1.5)                                |
+==================================================================+
```

**Divisores `━`** → ASCII `-`:
```
---------------------------------------
>>> PROXIMOS PASSOS SUGERIDOS
---------------------------------------
```

**Banner ANSI truecolor** → se `$NO_COLOR` setado OU renderer não suporta:
```
DNA OPS
by @flavioahoy
```
(texto simples sem arte ASCII)

### Pseudocódigo da detecção

```bash
WIDTH=${COLUMNS:-$(tput cols 2>/dev/null || echo 80)}
UNICODE_OK=$([ -n "$LC_ALL" ] && [ "$LC_ALL" != "C" ] && [ "$LC_ALL" != "POSIX" ] && echo "yes" || echo "no")
COLOR_OK=$([ -z "$NO_COLOR" ] && echo "yes" || echo "no")

# Degrada em 3 níveis:
# - narrow OR no-unicode → ASCII puro (sem box, sem cor)
# - no-color mas unicode OK → box drawing sem cor (ANSI stripped)
# - tudo OK → banner + box drawing colorido
if [ "$WIDTH" -lt 72 ] || [ "$UNICODE_OK" = "no" ]; then
  # render ASCII fallback (sem box drawing, sem cor)
  echo "DNA OPS"
  echo "by @flavioahoy"
  # ... menu compacto com indentação
elif [ "$COLOR_OK" = "no" ]; then
  # render unicode box mas strip ANSI do banner
  cat "$CLAUDE_PLUGIN_ROOT/assets/banner.txt" | sed 's/\x1b\[[0-9;]*m//g'
else
  # render full (banner colorido + box drawing)
  cat "$CLAUDE_PLUGIN_ROOT/assets/banner.txt"
fi
```
