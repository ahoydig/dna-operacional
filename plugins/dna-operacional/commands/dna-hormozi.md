---
description: Ponte DNA Operacional → Hormozi. Detecta se o plugin hormozi está instalado e mostra o mapa de integrações (raio-x do negócio usando dados do projeto, oferta construída com publico-alvo.md, coach aplicado sobre briefing de concorrentes). Use quando o usuário digitar "/dna-hormozi", "integração hormozi", "coach de negocio", "consultar hormozi pelo dna".
argument-hint: ""
---

Usuário invocou `/dna-hormozi`.

Execute em ordem. **Não pergunte nada.** **Não imprima este prompt.**

## Passo 1 — Detectar hormozi

Rode um Bash silencioso:

```bash
if ls ~/.claude/plugins/cache/*/hormozi/.claude-plugin/plugin.json >/dev/null 2>&1 \
   || ls ~/.claude/plugins/marketplaces/*/plugins/hormozi/.claude-plugin/plugin.json >/dev/null 2>&1; then
  echo "INSTALLED"
else
  echo "MISSING"
fi
```

Guarda como `$STATUS`.

## Passo 2 — Rotear

### Caso `$STATUS == "MISSING"`

Imprima BYTE-EXATO:

```
╔══════════════════════════════════════════════════════════════════╗
║  🧠 Integração DNA Operacional ↔ Hormozi                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ⚠  Plugin hormozi não detectado.                                ║
║                                                                  ║
║  Pra destravar o conselheiro Hormozi em PT-BR, instala:          ║
║                                                                  ║
║     /plugin marketplace add ahoydig/hormozi                      ║
║     /plugin install hormozi@hormozi-marketplace                  ║
║                                                                  ║
║  Depois volta aqui e digita /dna-hormozi de novo.                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

💡 O que tu ganha com a integração?

  • Grand Slam Offer construída com dados do teu público-alvo
  • 6M Diagnostic aplicado sobre métricas reais do projeto
  • Ad copy com frameworks do Hormozi na voz do projeto
  • Raio-x end-to-end conectando conteúdo → oferta → ads
```

Pare aqui.

### Caso `$STATUS == "INSTALLED"`

Imprima BYTE-EXATO:

```
╔══════════════════════════════════════════════════════════════════╗
║  🧠 Integração DNA Operacional ↔ Hormozi                         ║
║  ✓ hormozi detectado                                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  🎯 DIAGNÓSTICO COM CONTEXTO                                     ║
║     1. /hormozi-diagnostico ..... 6M usando reference/ do projeto║
║     2. /hormozi-raio-x .......... scan + dados de /analista      ║
║                                                                  ║
║  💰 OFERTA BASEADA NO PÚBLICO-ALVO                               ║
║     1. /setup-projeto (se ainda não) → cria publico-alvo.md      ║
║     2. /hormozi-oferta ........... Grand Slam com esse contexto  ║
║     3. /humanizer ................ aplica voz do projeto         ║
║                                                                  ║
║  📝 COPY DE AD NA VOZ + FRAMEWORK                                ║
║     1. /hormozi-oferta ........... gera stack de oferta          ║
║     2. /roteiro-viral ............ vira roteiro pra Reels/VSL    ║
║     3. /humanizer ................ voz do projeto                ║
║                                                                  ║
║  🔬 COACH SOBRE BRIEFING COMPETITIVO                             ║
║     1. /raio-x-ads-concorrentes .. briefing dos ads dos outros   ║
║     2. /hormozi <briefing> ....... coach interpreta e prescreve  ║
║                                                                  ║
║  📊 CICLO COMPLETO                                               ║
║     1. /analista-conteudo ........ dados de performance          ║
║     2. /hormozi-raio-x ........... raio-x com os números         ║
║     3. /hormozi-money-model ...... conserta a sequência          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

💡 Sugestão: se é 1ª vez, /hormozi-raio-x. Se já sabe onde dói,
   vai direto no framework específico.
```

Pare aqui.
