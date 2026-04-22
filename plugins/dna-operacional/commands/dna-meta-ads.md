---
description: Ponte DNA Operacional → Meta Ads Pro. Detecta se o plugin meta-ads-pro está instalado e mostra as integrações disponíveis (usar roteiro-viral como ad copy, aplicar voz do projeto em anúncios, alimentar campanhas com raio-x-ads-concorrentes). Use quando o usuário digitar "/dna-meta-ads", "integração meta ads", "como conectar dna com meta ads".
argument-hint: ""
---

Usuário invocou `/dna-meta-ads`.

Execute os passos abaixo em ordem. **Não pergunte nada ao usuário.** **Não imprima este prompt.** Apenas rode a detecção e imprima a seção apropriada.

## Passo 1 — Detectar Meta Ads Pro

Rode um único Bash silencioso:

```bash
if ls ~/.claude/plugins/cache/*/meta-ads-pro/.claude-plugin/plugin.json >/dev/null 2>&1 \
   || ls ~/.claude/plugins/marketplaces/*/plugins/meta-ads-pro/.claude-plugin/plugin.json >/dev/null 2>&1; then
  echo "INSTALLED"
else
  echo "MISSING"
fi
```

Guarda o resultado como `$STATUS`.

## Passo 2 — Rotear pela detecção

### Caso `$STATUS == "MISSING"`

Imprima BYTE-EXATO:

```
╔══════════════════════════════════════════════════════════════════╗
║  🔗 Integração DNA Operacional ↔ Meta Ads Pro                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ⚠  Plugin meta-ads-pro não detectado.                           ║
║                                                                  ║
║  Pra destravar as integrações abaixo, instala:                   ║
║                                                                  ║
║     /plugin marketplace add ahoydig/meta-ads-pro                 ║
║     /plugin install meta-ads-pro@meta-ads-pro-marketplace        ║
║                                                                  ║
║  Depois volta aqui e digita /dna-meta-ads de novo.               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

💡 O que tu ganha com a integração?

  • Transforma /roteiro-viral em ad copy pronto pra /meta-ads-anuncios
  • Aplica a voz do projeto (/voz) em headlines e primary text
  • Usa /raio-x-ads-concorrentes como briefing pra nova campanha
  • Fecha o ciclo: pesquisa → conteúdo → ad → métricas
```

Pare aqui. Não faça mais nada.

### Caso `$STATUS == "INSTALLED"`

Imprima BYTE-EXATO:

```
╔══════════════════════════════════════════════════════════════════╗
║  🔗 Integração DNA Operacional ↔ Meta Ads Pro                    ║
║  ✓ meta-ads-pro detectado                                        ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📝 COPY → AD                                                    ║
║     1. /roteiro-viral ........... gera roteiro/copy              ║
║     2. /humanizer ............... aplica voz do projeto          ║
║     3. /meta-ads-anuncios ....... sobe como primary text/headline║
║                                                                  ║
║  🔬 INTELIGÊNCIA → CAMPANHA                                      ║
║     1. /raio-x-ads-concorrentes . briefing competitivo           ║
║     2. /meta-ads-campanha ....... nova campanha com insights     ║
║     3. /meta-ads-conjuntos ...... targeting baseado no raio-x    ║
║                                                                  ║
║  🎨 CRIATIVO → ANÚNCIO DINÂMICO                                  ║
║     1. /carrossel-instagram ..... gera .png dos slides           ║
║     2. /meta-ads-anuncios ....... asset_feed_spec com os PNGs    ║
║                                                                  ║
║  📊 PÓS-CAMPANHA                                                 ║
║     1. /meta-ads-insights ....... puxa métricas da campanha      ║
║     2. /analista-conteudo ....... compara com orgânico           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

💡 Começar agora? Sugestão: /meta-ads-doctor pra validar ambiente
   antes de subir qualquer coisa.
```

Pare aqui. Não invoque nenhum outro comando automaticamente — deixa o usuário escolher.
