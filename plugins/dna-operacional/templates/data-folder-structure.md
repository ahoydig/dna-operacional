# Template Markdown Local — Estrutura data/

Como preparar a pasta `data/` pra backend `markdown` do DNA Operacional.

## Setup em 2 passos

### 1. Criar estrutura de pastas

No root do teu projeto:

```bash
mkdir -p data/competitors data/competitor_posts data/content_pipeline data/my_content data/ad_library data/adaptive_models data/generated_scripts
```

Resultado:

```
data/
├── competitors/
├── competitor_posts/
├── content_pipeline/
├── my_content/
├── ad_library/
├── adaptive_models/
└── generated_scripts/
```

### 2. Adicionar config no CLAUDE.md

```markdown
## Storage Backend: markdown

- data_dir: ./data
```

Pronto. Skills de dados vão escrever `.md` lá.

## Exemplo de arquivo (por table)

Cada arquivo = 1 record. Nome: `{id:03d}-{slug}.md`. Frontmatter YAML tem todos os campos estruturados; corpo markdown é opcional (notes livres).

### Exemplo `competitors/042-chris-bumstead.md`

```markdown
---
id: 42
name: "Chris Bumstead"
instagram_username: "cbum"
instagram_profile_url: "https://instagram.com/cbum"
followers_count: 15000000
foto: "https://cdn.instagram.com/cbum.jpg"
nicho: "fitness"
sub_nicho: "bodybuilding"
avg_engagement_coefficient: 0.043
posts_analyzed_count: 87
last_avg_update: "2026-04-10T14:20:00Z"
created_at: "2026-04-01T10:00:00Z"
updated_at: "2026-04-14T15:30:00Z"
---

# Chris Bumstead

Canadense, 5x Mr. Olympia Classic Physique. Nicho: musculação clássica.
```

### Exemplo `content_pipeline/007-hook-pix-subestimado.md`

```markdown
---
id: 7
title: "Pix é a coisa mais subestimada do Brasil"
status: "Roteirizado"
source: "pesquisa-diaria"
source_url: ""
topic: "finanças digitais"
angulo: "contra-intuitivo / elogio nacional"
hook_suggestion: "Pix é a coisa mais subestimada do Brasil"
motivo_video: "Virou tema recorrente. Brasileiro não sabe o tamanho do avanço."
research_brief: "(...)"
format: "Reel"
archetype: "descoberta"
platform: "instagram"
variant_of: null
published_content_id: null
created_at: "2026-04-10T08:00:00Z"
updated_at: "2026-04-12T17:30:00Z"
---

# Pix é a coisa mais subestimada do Brasil

## Notes

Meter comparação com SWIFT/ACH americano. Mostrar dados BCB.
```

## Dica: versionar no git (opcional)

Se `data/` não tem info sensível, versiona:

```bash
git add data/
git commit -m "chore: adiciona data/ pro backend markdown"
```

Facilita ter histórico de mudanças nos records. Se houver info sensível (leads, emails de clientes), adicionar no `.gitignore` do projeto.

## Quando crescer muito

Soft limit: ~100 items por pasta. Além disso, Glob fica lento e navegação manual fica chata. Considere:
- `/dna migrar-storage sheets` (skill futura, v0.2+) — automático
- Exportação manual: ler todos .md, converter pra CSV, importar em planilha

## Troubleshooting

| Sintoma | Causa provável | Fix |
|---|---|---|
| Skill falha com "pasta não existe" | Uma das 7 subpastas não foi criada | Rode o `mkdir -p` do passo 1 |
| Records somem | `data/` está em `.gitignore` + cleanup acidental | Restaure via Time Machine / backup |
| Filename colide | Dois records com mesmo slug sendo criados simultaneamente | Fix manual: renomear um pra `NNN-{slug}-2.md`. Skills futuras terão lock. |
