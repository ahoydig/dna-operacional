# Spike: Custo /pesquisa-diaria

**Status:** estimativa teórica (Spec 2 §8.1). Medição real pendente pra v0.2.

## Estimativa teórica

Com base em modelo Sonnet 4.6 ($3/1M input + $15/1M output):

- Tokens por execução: **~40-80k** (input + output combinados; Apify scraping externo NÃO conta)
- Custo/execução: **~$0.60-1.20**
- Custo/mês (30 dias): **~$18-36/mês**

Com modelo Opus 4.6 ($15/1M input + $75/1M output):
- Custo/execução: ~$3-6
- Custo/mês: ~$90-180/mês

## Decisão de default agendamento

Com Sonnet (~$18-36/mês), custo fica na zona intermediária ($10-30). Pro aluno padrão: **recomendar Google Sheets + launchd local (zero custo) como default no APIS-EXTERNAS.md**. `/schedule` Anthropic vira opção "premium" pra quem não quer gerenciar infra.

User pode escolher entre as 3 opções conforme perfil — doc APIS-EXTERNAS.md tem guia passo-a-passo pra cada.

## Follow-up (v0.2+)

Rodar `/pesquisa-diaria` 3-5 vezes pra amostragem robusta. Medir real via Claude Code billing dashboard. Substituir estimativa deste doc pelos números medidos.
