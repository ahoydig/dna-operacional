# Convenções do plugin DNA Operacional

> Extensão da Spec 1 §7 cobrindo as 14 skills da v0.1.0.

Documento canônico das convenções que TODA skill do plugin deve seguir.

## 1. Bloco "Próximos Passos" (obrigatório no fim da skill)

Toda skill termina com este bloco após a execução principal:

```
✅ [resultado da skill em uma frase]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /<skill-sugerida-1>   — <1 linha do porquê>
  2. /<skill-sugerida-2>   — <1 linha do porquê>

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Regras

- **1-3 sugestões** máximo (mais que isso vira ruído).
- Sugestões **contextuais** (depende do resultado da execução).
  - Ex: se `pesquisa-concorrentes` rodou mas não populou `competitor_posts`, NÃO sugerir `raio-x-ads-concorrentes`.
- **Escape hatch obrigatório:** linha `💡 /dna pra ver todas...` no final, sempre.

### Fallback ASCII (terminais sem unicode)

Se `$LC_ALL` indicar ASCII-only, degradar `━` pra `-`:

```
----------------------------------------
>>> PROXIMOS PASSOS SUGERIDOS
----------------------------------------
  1. /<skill-1>   - <desc>
  2. /<skill-2>   - <desc>

  >>> /dna pra ver todas
----------------------------------------
```

## 2. Mapeamento inicial de sugestões (v0.1.0 — 14 skills)

| Skill | Sugere ao fim |
|---|---|
| `setup-projeto` | `/voz`, `/pesquisa-concorrentes`, `/pesquisa-diaria` |
| `voz` | `/humanizer` (teste imediato), `/setup-projeto` (se ainda não configurou) |
| `humanizer` | nenhum forçado (contextual) |
| `pesquisa-diaria` | `/ideias-conteudo` (se user salvou no pipeline), `/analista-conteudo` |
| `pesquisa-concorrentes` | `/raio-x-ads-concorrentes` (se `ad_library` populada, v0.2+), `/analista-conteudo` |
| `raio-x-ads-concorrentes` | `/ideias-conteudo`, `/pesquisa-concorrentes` |
| `ideias-conteudo` | `/analisar-video` (modelo), `/roteiro-viral`, `/analista-conteudo` |
| `analisar-video` | `/roteiro-viral` (consumir `adaptive_model` gerado) |
| `roteiro-viral` | `/carrossel-instagram` (visual), `/analista-conteudo` |
| `carrossel-instagram` | `/ideias-conteudo` (próximo tópico) |
| `analista-conteudo` | `/ideias-conteudo` (com insights), `/pesquisa-diaria` (temas frescos) |
| `auto-melhoria` | nenhum forçado |
| `dna-melhoria` | nenhum forçado |
| `dna` | nenhum (ele É o menu) |

## 3. Saudação (opcional, start de skill)

Skills que começam com operação longa (ex: scraping, análise) podem abrir com saudação curta:

```
🧬 [skill] iniciada. <sumário em 1 linha do que vai fazer>
```

Evitar verbosidade. Nunca mostrar banner no start (só `/dna` e `setup-projeto` primeira vez).

## 4. Storage layer (contrato abstrato)

> **⚠️ v0.1.0-alpha:** scaffolding do plugin NÃO implementa storage layer ainda. Isso vem em plano subsequente (Plan 2). Esta seção é stub.

Toda skill que persiste dado DEVE chamar funções abstratas do `lib/storage/` — NÃO escrever SQL inline (exceção: `analista-conteudo` que é Supabase-only, documentada).

Ver Spec 2 §4 e §4.7 pros detalhes do contrato.

## 5. Sanitização (IDs pessoais)

Antes de qualquer skill entrar no plugin, passa por audit com grep dos 20 padrões listados no Spec 2 §7.1. Placeholders substituem dados pessoais.

Ver Spec 2 §7 pro checklist completo.
