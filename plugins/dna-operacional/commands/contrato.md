---
description: Edita modelo de contrato (.docx ou .pdf fornecido pelo user) substituindo placeholders com dados do cliente + projeto DNA. Invoca skill global `docx` pra edição estrutural. Suporta docx→docx, pdf→docx (converte), opcional docx→pdf no final. Use quando digitar "/contrato", "gerar contrato", "personalizar contrato <modelo>", "adaptar modelo de contrato".
argument-hint: "[path do modelo .docx ou .pdf]"
---

Usuário invocou `/contrato $ARGUMENTS`.

Esse é um **comando-skill novo** — não é wrapper de skill existente. Detecta placeholders, pergunta valores (pré-preenchendo do DNA), aplica find-replace via skill `docx`.

## Passo 1 — Validar modelo de entrada

Inspecionar `$ARGUMENTS`:

```bash
if [ -z "$ARGUMENTS" ]; then
  # Perguntar ao user: "Qual modelo? Me passa o path (.docx ou .pdf) OU digita 'padrao' pra eu gerar um modelo padrão do zero."
elif [ ! -f "$ARGUMENTS" ]; then
  # Erro: "Arquivo não encontrado: $ARGUMENTS"
fi

EXT="${ARGUMENTS##*.}"
case "$EXT" in
  docx|DOCX) MODE="docx";;
  pdf|PDF)   MODE="pdf-convert";;
  *)         MODE="unknown";;
esac
```

**3 caminhos:**
- **docx** → edição direta via skill `docx`
- **pdf** → converter pra docx (avisar user que output final será .docx, com opção de re-gerar PDF no fim)
- **padrao** → gerar modelo padrão usando `templates/contrato-padrao-structure.md`

Se `MODE == "unknown"`:
> "⚠ Formato não suportado. Só aceito .docx ou .pdf (ou 'padrao' pra gerar modelo do zero)."

## Passo 2 — Ler contexto DNA

| Arquivo | Uso |
|---------|-----|
| `CLAUDE.md` | Empresa, CNPJ da empresa (em CLAUDE.md) (se cadastrado), e-mail, cidade |
| `data/clientes/<slug>/cliente.json` | Dados do cliente já cadastrado (se `/orcamento` rodou antes) |
| `reference/publico-alvo.md` | Contexto do nicho |

## Passo 3 — Extrair conteúdo + detectar placeholders

### 3.1 Se MODE == docx

Invocar **Skill tool** `docx` com `op: extract-text` passando o path. Receber texto bruto.

### 3.2 Se MODE == pdf-convert

Invocar **Skill tool** `pdf` com `op: extract-text`. Receber texto + imagens/tabelas extraídas.

Avisar user:
> "📄 PDF convertido pra edição. O output final será `.docx`. Quer que eu gere também um PDF do contrato personalizado no fim? [S/n]"

### 3.3 Se MODE == padrao

Gerar base docx usando **Skill tool** `docx` com `op: create` passando o conteúdo descrito em `${CLAUDE_PLUGIN_ROOT}/templates/contrato-padrao-structure.md`.

### 3.4 Detectar placeholders

Aplicar regex `/\{\{([A-Z_0-9]+)\}\}/g` no texto. Colecionar set único.

Placeholders esperados (pré-mapeados pra contexto DNA):

| Placeholder | Fonte auto-preenchimento |
|-------------|-------------------------|
| `{{EMPRESA}}` | CLAUDE.md — nome do projeto |
| `{{CNPJ_EMPRESA}}` | CLAUDE.md — CNPJ da empresa (em CLAUDE.md) (se tiver) |
| `{{EMAIL_EMPRESA}}` | CLAUDE.md — e-mail |
| `{{CIDADE}}` | CLAUDE.md — cidade (se tiver), senão "Fortaleza/CE" |
| `{{DATA_ASSINATURA}}` | `$(date +%d/%m/%Y)` |
| `{{CLIENTE_NOME}}` | cliente.json ou perguntar |
| `{{CLIENTE_CNPJ}}` | cliente.json ou perguntar |
| `{{CLIENTE_EMAIL}}` | cliente.json ou perguntar |
| `{{OBJETO}}` | perguntar |
| `{{VALOR}}` | perguntar (puxar de orcamentos.csv se mesmo cliente) |
| `{{FORMA_PAGAMENTO}}` | perguntar (pré-selecionar "50% aceite / 50% entrega") |
| `{{PRAZO}}` | perguntar (em dias) |

Se o modelo tem placeholders NÃO mapeados, tratá-los como perguntas genéricas:
> "Placeholder desconhecido: `{{FOO_BAR}}`. Qual valor?"

## Passo 4 — Coletar valores

Pra cada placeholder:

1. Se tem fonte auto → pré-preencher + confirmar com user ("Detectei `{{EMPRESA}}` = '{{EMPRESA}}'. Confirma? [S/n]")
2. Se não tem fonte → perguntar direto

**Sessão de perguntas** em bloco único (não uma por uma):

```
📋 Preenchimento do contrato

Pré-preenchido do DNA:
  EMPRESA = {{EMPRESA}}
  CNPJ_EMPRESA = 00.000.000/0001-00
  EMAIL_EMPRESA = {{EMAIL_EMPRESA}}
  CIDADE = Fortaleza/CE
  DATA_ASSINATURA = 21/04/2026

Falta você informar:
  CLIENTE_NOME =
  CLIENTE_CNPJ =
  CLIENTE_EMAIL =
  OBJETO =
  VALOR =
  FORMA_PAGAMENTO =
  PRAZO =

Me manda tudo de uma vez (ou linha a linha, como preferir).
```

## Passo 5 — Aplicar find-replace

Invocar **Skill tool** `docx` com `op: find-replace`:

```
input_file: <path do .docx extraído/gerado>
replacements: [
  { find: "{{EMPRESA}}", replace: "<valor>" },
  { find: "{{CNPJ_EMPRESA}}", replace: "<valor>" },
  ...
]
output_file: <temp path>
```

A skill `docx` preserva formatação (negrito, tabelas, estilos) enquanto substitui o texto.

## Passo 6 — Salvar output

```bash
slug = lowercase(CLIENTE_NOME).replace(/[^a-z0-9]+/g, '-').slice(0, 40)
date = $(date +%Y-%m-%d)
out_dir = "data/clientes/${slug}/contratos/${date}"
mkdir -p "${out_dir}"

mv <temp_docx> "${out_dir}/contrato-${slug}.docx"
```

Se MODE == pdf-convert e user confirmou output PDF no Passo 3.2:

Invocar **Skill tool** `pdf` com `op: docx-to-pdf`:
```
input: ${out_dir}/contrato-${slug}.docx
output: ${out_dir}/contrato-${slug}.pdf
```

## Passo 7 — Registrar

### 7.1 Garantir `cliente.json`

Se `data/clientes/${slug}/cliente.json` não existe, criar com os dados coletados:

```json
{
  "nome": "{{CLIENTE_NOME}}",
  "slug": "<slug>",
  "cnpj": "{{CLIENTE_CNPJ}}",
  "email": "{{CLIENTE_EMAIL}}",
  "created_at": "<ISO>"
}
```

### 7.2 Append em `data/contratos.csv`

Header:
```
id,cliente,slug,modelo_origem,output_path,formato,valor,prazo,created_at
```

Nova linha com:
- `modelo_origem` = path de `$ARGUMENTS` ou "padrao"
- `output_path` = path do .docx (e .pdf se gerado)
- `formato` = "docx" ou "docx+pdf"

## Passo 8 — Output pro usuário

```
╔══════════════════════════════════════════════════════════════════╗
║  📜 Contrato personalizado                                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Cliente:       <CLIENTE_NOME>                                   ║
║  Objeto:        <OBJETO>                                         ║
║  Valor:         <VALOR>                                          ║
║  Prazo:         <PRAZO> dias                                     ║
║                                                                  ║
║  Substituições: <N> placeholders preenchidos                     ║
║                                                                  ║
║  Output:        data/clientes/<slug>/contratos/<data>/           ║
║                 ├── contrato-<slug>.docx                         ║
║                 └── contrato-<slug>.pdf  (opcional)              ║
║                                                                  ║
║  ⚠ ATENÇÃO                                                       ║
║    Contrato é documento legal. Revise manualmente ANTES de       ║
║    assinar:                                                      ║
║      • Valores e datas                                           ║
║      • Nome + CNPJ do cliente                                    ║
║      • Cláusulas de rescisão e foro                              ║
║      • Assinaturas previstas                                     ║
║                                                                  ║
║    Se é contrato importante/longo, pede revisão jurídica.        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Erros comuns

| Situação | Ação |
|----------|------|
| Skill `docx` não instalada | Bloquear: "Instala a skill `docx` antes de usar `/contrato`." |
| Skill `pdf` não instalada (modo pdf-convert) | Bloquear: "Instala a skill `pdf` ou me passa um .docx direto." |
| Modelo sem placeholders `{{X}}` | Avisar: "Não achei placeholders `{{X}}`. Quer editar manualmente ou usar modelo padrão?" |
| Cliente sem `cliente.json` nem dados | Coletar no briefing e criar cliente.json |
| Placeholder aparece múltiplas vezes | Substituir todas as ocorrências (find-replace é greedy por default) |

## Regra ferro

**NUNCA** assumir que o contrato está correto. SEMPRE imprimir o aviso ⚠ no Passo 8. Responsabilidade legal é do usuário.
