# data/clientes/ — Convenção de Estrutura

Convenção única compartilhada pelas 4 skills de entrega: `/orcamento`, `/apresentacao`, `/landing-page`, `/contrato`. Cada cliente ganha uma subpasta com slug + subpastas por tipo de artefato + arquivos versionados por data.

## Árvore canônica

```
data/
├── clientes/
│   ├── <slug-cliente>/
│   │   ├── cliente.json              # metadata fixa
│   │   ├── orcamentos/
│   │   │   └── <AAAA-MM-DD>/
│   │   │       ├── orcamento-<slug>.pdf
│   │   │       └── briefing.json     # opcional (pra reuso)
│   │   ├── apresentacoes/
│   │   │   └── <AAAA-MM-DD>/
│   │   │       ├── index.html
│   │   │       ├── style.css
│   │   │       ├── main.js
│   │   │       ├── config.js
│   │   │       └── assets/
│   │   ├── landing-pages/
│   │   │   └── <AAAA-MM-DD>/
│   │   │       ├── index.html
│   │   │       ├── style.css
│   │   │       ├── script.js
│   │   │       └── assets/
│   │   └── contratos/
│   │       └── <AAAA-MM-DD>/
│   │           ├── contrato-<slug>.docx
│   │           └── contrato-<slug>.pdf    # opcional
│   └── outro-cliente/
│       └── ...
│
├── orcamentos.csv                     # rollup todos clientes
├── apresentacoes.csv                  # rollup
├── landing_pages.csv                  # rollup
└── contratos.csv                      # rollup
```

## cliente.json — schema

```json
{
  "nome": "Matheus Moita",
  "slug": "matheus-moita",
  "razao_social": "MM Consultoria Ltda.",
  "cnpj": "11.222.333/0001-44",
  "email": "matheus@mm.com.br",
  "telefone": "+55 85 99999-0000",
  "nicho": "nutricionista",
  "endereco": "Rua X, 100, Fortaleza/CE",
  "contato_nome": "Matheus Moita",
  "contato_cargo": "Sócio-fundador",
  "created_at": "2026-04-21T10:00:00-03:00",
  "updated_at": "2026-04-21T10:00:00-03:00",
  "notes": "Preferência por WhatsApp. Assinou em 21/04."
}
```

**Regra de write:** toda skill que gera artefato checa se `cliente.json` existe. Se não, cria com os dados coletados. Se existe, merge silencioso dos campos (não sobrescreve sem perguntar).

## Regra de Slug

```
slug = lowercase(nome_cliente)
         .normalize('NFD')               # remove acentos
         .replace(/[̀-ͯ]/g, '')
         .replace(/[^a-z0-9]+/g, '-')
         .replace(/^-+|-+$/g, '')
         .slice(0, 40)
```

Exemplos:
- "Matheus Moita" → `matheus-moita`
- "Clínica Amp. Ltda." → `clinica-amp-ltda`
- "João Silva & Cia" → `joao-silva-cia`
- "Foo Bar Baz — Long Name Corporation International" → `foo-bar-baz-long-name-corporation-internat` (40 chars)

## Rollup CSVs — schema

Todos em RFC 4180 (aspas duplas em campos com vírgula/aspas/quebra-linha).

### data/orcamentos.csv

```
id,cliente,slug,nicho,pdf_path,valor,status,created_at
1,"Matheus Moita","matheus-moita","nutricionista","data/clientes/matheus-moita/orcamentos/2026-04-21/orcamento-matheus-moita.pdf","R$ 12.000,00","enviado","2026-04-21T10:00:00-03:00"
```

**Status:** `rascunho` | `enviado` | `aceito` | `rejeitado` | `expirado`

### data/apresentacoes.csv

```
id,tema,cliente,slug,out_dir,slides_count,paleta,arquetipo,created_at
1,"Kickoff","Matheus Moita","matheus-moita","data/clientes/matheus-moita/apresentacoes/2026-04-21/",10,"Obsidian Quantum","cyberpunk","2026-04-21T11:00:00-03:00"
```

### data/landing_pages.csv

```
id,objetivo,cliente,slug,out_dir,arquetipo,paleta,polish_impeccable,created_at
1,"venda","Matheus Moita","matheus-moita","data/clientes/matheus-moita/landing-pages/2026-04-21/","clean","Editorial Warm","sim","2026-04-21T12:00:00-03:00"
```

**Objetivos:** `venda` | `captura` | `waitlist` | `evento`

### data/contratos.csv

```
id,cliente,slug,modelo_origem,output_path,formato,valor,prazo,created_at
1,"Matheus Moita","matheus-moita","padrao-ahoy","data/clientes/matheus-moita/contratos/2026-04-21/contrato-matheus-moita.docx","docx","R$ 12.000,00",45,"2026-04-21T13:00:00-03:00"
```

**Formato:** `docx` | `docx+pdf`

## Regra de append

Toda skill de entrega:
1. Checa se o CSV existe. Se não, cria com header.
2. Lê última linha pra descobrir próximo `id` (`last_id + 1`).
3. Apenda nova linha com escape RFC 4180.
4. Nunca edita/deleta linhas anteriores (log imutável).

## Por que essa estrutura

- **Cliente-first:** todos os artefatos de um cliente num lugar só. Facilita handoff e arquivamento.
- **Data no path:** história preservada. Se cliente vira contrato 3x, 3 pastas datadas.
- **CSVs achatados:** pesquisa rápida via `grep "cliente-slug" data/*.csv`. Empresário abre no Excel.
- **Metadata em JSON:** campos complexos (notes, endereço multilinha, tags) ficam legíveis.
- **Consistência cross-skill:** qualquer skill que cria cliente.json usa o mesmo schema.

## Gitignore sugerido

Se o projeto usa git, adicionar em `.gitignore` do projeto do user:

```
# Dados de clientes — nunca versionar
data/clientes/
data/texts/

# Mas versionar os rollups (sem dados sensíveis)
!data/*.csv
```

**Atenção:** verificar se os CSVs não têm PII (CNPJ, email) antes de commitar. Se tiverem, excluir todos.
