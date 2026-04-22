---
description: Gera orçamento/proposta comercial em PDF com dados pré-preenchidos do projeto DNA (público, voz, oferta principal). Invoca a skill global `proposta` (design premium Ahoy + precificação + Playwright PDF). Salva em data/clientes/<slug>/orcamentos/. Use quando digitar "/orcamento", "gerar orçamento", "proposta pra <cliente>", "fazer proposta".
argument-hint: "[nome do cliente]"
---

Usuário invocou `/orcamento $ARGUMENTS`.

Esse comando é um **wrapper fino** pra skill global `proposta` — aplica o contexto do projeto DNA antes de delegar.

## Passo 1 — Ler contexto DNA do projeto

Ler no diretório atual (silenciosamente, não abortar se faltar):

| Arquivo | Pra quê |
|---------|---------|
| `CLAUDE.md` | Nome do projeto, e-mail, handle, voz em 3 adjetivos, oferta principal (se Setup Fast) |
| `reference/publico-alvo.md` | Briefing detalhado — pode já ter oferta + preço + argumentos |
| `reference/voz-*.md` | Voz aplicada na copy do PDF (tom, vícios, jargões proibidos) |

Se CLAUDE.md não existir:
> "⚠ Projeto não configurado. Rode `/setup-projeto fast` antes pra eu pré-preencher 70% do orçamento."
>
> Perguntar se quer rodar mesmo assim (coleta tudo do zero).

## Passo 2 — Coletar info do cliente

Perguntar APENAS o que não veio em `$ARGUMENTS` ou no contexto:

1. **Nome do cliente** (se não veio em args)
2. **Razão social + CNPJ** (opcional — pra nota fiscal)
3. **Nicho do cliente** (ex: clínica odontológica, SaaS B2B, infoprodutor fitness)
4. **Escopo do projeto** em 1-3 frases (o que a Ahoy vai entregar)
5. **Deadline esperado** (em semanas/meses)
6. **Faixa de orçamento** (opcional — ajuda a calibrar precificação)
7. **Nome + cargo de quem assina** pelo cliente

**Pré-preencher do contexto:**
- `{{EMPRESA_AHOY}}` = nome do projeto em CLAUDE.md
- `{{EMAIL_AHOY}}` = e-mail em CLAUDE.md
- `{{VOZ}}` = voz dos adjetivos em CLAUDE.md ou `reference/voz-*.md`

## Passo 3 — Invocar skill global `proposta`

Usar a **Skill tool** com `skill: "proposta"` passando contexto agregado:

```
Contexto DNA aplicado:
- Empresa: <nome>
- Voz: <tom direto/provocador/nordestino>
- Público-alvo referência: <trecho de publico-alvo.md>
- Oferta base: <se CLAUDE.md tem Oferta Principal>

Dados do cliente:
- Nome: <cliente>
- CNPJ: <se informado>
- Nicho: <nicho>
- Escopo: <escopo>
- Deadline: <prazo>
- Faixa orçamento: <faixa>
- Assinatura: <nome + cargo>

Gera proposta premium, aplica Nofex font + A4 print-friendly, saída em PDF.
```

A skill `proposta` cuida de:
- Precificação guiada (setup + mensalidade)
- Design premium (paleta Ahoy: `#010B12` + `#2BC20E`)
- Renderização Playwright → PDF
- Histórico em `propostas/historico-propostas.json`

## Passo 4 — Reubicar output + registrar

Após a skill `proposta` retornar o path do PDF:

### 4.1 Slug do cliente

```
slug = lowercase(nome_cliente).replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40)
```

### 4.2 Mover PDF

```bash
mkdir -p "data/clientes/${slug}/orcamentos/$(date +%Y-%m-%d)"
mv "<pdf_origem>" "data/clientes/${slug}/orcamentos/$(date +%Y-%m-%d)/orcamento-${slug}.pdf"
```

### 4.3 Garantir metadata do cliente

Se `data/clientes/${slug}/cliente.json` não existir, criar com:

```json
{
  "nome": "<cliente>",
  "slug": "<slug>",
  "razao_social": "<razao_social ou null>",
  "cnpj": "<cnpj ou null>",
  "nicho": "<nicho>",
  "contato_nome": "<nome que assina>",
  "contato_cargo": "<cargo>",
  "created_at": "<ISO date>"
}
```

### 4.4 Append em `data/orcamentos.csv`

**Header (linha 1, criar se arquivo não existir):**

```
id,cliente,slug,nicho,pdf_path,valor,status,created_at
```

**Nova linha:**

```
<id auto incrementado>,<cliente>,<slug>,<nicho>,data/clientes/<slug>/orcamentos/<data>/orcamento-<slug>.pdf,<valor total>,enviado,<ISO date>
```

Usar RFC 4180 escape (aspas duplas em campos com vírgula/aspas).

## Passo 5 — Output pro usuário

```
╔══════════════════════════════════════════════════════════════════╗
║  📄 Orçamento gerado                                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Cliente: <nome>                                                 ║
║  Valor:   R$ <valor>                                             ║
║  PDF:     data/clientes/<slug>/orcamentos/<data>/orcamento-<slug>.pdf  ║
║                                                                  ║
║  Próximos passos:                                                ║
║    1. Revisar o PDF                                              ║
║    2. Enviar pro cliente                                         ║
║    3. Quando fechar: /contrato pra personalizar contrato         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Erros comuns

| Situação | Ação |
|----------|------|
| Skill `proposta` não instalada | Instruir: "Instale a skill `proposta` via `/plugin` antes de usar `/orcamento`." |
| PDF não gerou | Repassar erro da skill `proposta` sem censurar |
| `data/` não existe | Criar silenciosamente com `mkdir -p` |
| CLAUDE.md ausente | Avisar uma vez, rodar fluxo coletando tudo do zero |
