# Template — Contrato Padrão Ahoy (gerado sob demanda)

Spec de estrutura do contrato padrão que a skill `/contrato` gera quando o user não tem modelo próprio (`/contrato padrao`). O skill `docx` usa esse spec pra montar o .docx do zero.

## Placeholders esperados

Todos em CAPS, formato `{{NOME}}`, auto-detectáveis pela regex `/\{\{([A-Z_0-9]+)\}\}/g`.

### Dados da Ahoy (pré-preenchidos do CLAUDE.md)

| Placeholder | Fonte | Exemplo |
|-------------|-------|---------|
| `{{EMPRESA}}` | CLAUDE.md `# Projeto <nome>` | `Ahoy Digital` |
| `{{EMPRESA_RAZAO_SOCIAL}}` | CLAUDE.md (seção empresa) | `Ahoy Digital Ltda.` |
| `{{CNPJ_EMPRESA}}` | CLAUDE.md (seção empresa) | `00.000.000/0001-00` |
| `{{EMAIL_EMPRESA}}` | CLAUDE.md `## Contato: <email>` | `contato@ahoydigital.ag` |
| `{{ENDERECO_EMPRESA}}` | CLAUDE.md (opcional) | `Rua X, 100, Fortaleza/CE` |
| `{{REPRESENTANTE_EMPRESA}}` | CLAUDE.md ou perguntar | `Flávio Montenegro` |

### Dados do Cliente (coletados no briefing)

| Placeholder | Fonte | Exemplo |
|-------------|-------|---------|
| `{{CLIENTE_NOME}}` | perguntar | `Matheus Moita` |
| `{{CLIENTE_RAZAO_SOCIAL}}` | perguntar | `MM Consultoria Ltda.` |
| `{{CLIENTE_CNPJ}}` | perguntar | `11.222.333/0001-44` |
| `{{CLIENTE_EMAIL}}` | perguntar | `matheus@mm.com.br` |
| `{{CLIENTE_ENDERECO}}` | perguntar | `...` |
| `{{CLIENTE_REPRESENTANTE}}` | perguntar | `Matheus Moita` |

### Dados do Contrato

| Placeholder | Fonte | Exemplo |
|-------------|-------|---------|
| `{{OBJETO}}` | perguntar (1 frase) | `Implementação de Agente de Pré-Vendas IA via WhatsApp` |
| `{{VALOR_SETUP}}` | perguntar (ou orcamentos.csv) | `R$ 12.000,00` |
| `{{VALOR_MENSAL}}` | perguntar (se aplicável) | `R$ 1.900,00` |
| `{{FORMA_PAGAMENTO}}` | perguntar | `50% na aceitação (sinal) + 50% na entrega` |
| `{{PRAZO}}` | perguntar (em dias) | `45` |
| `{{DATA_ASSINATURA}}` | `$(date +%d/%m/%Y)` | `21/04/2026` |
| `{{CIDADE}}` | CLAUDE.md ou default `Fortaleza/CE` | `Fortaleza/CE` |
| `{{FORO}}` | default `Fortaleza/CE` | `Fortaleza/CE` |

## Estrutura de seções (ordem)

1. **Cabeçalho** — "CONTRATO DE PRESTAÇÃO DE SERVIÇOS" + "Contrato Nº {{DATA}}-{{CLIENTE_SLUG}}"

2. **Identificação das Partes**
   - CONTRATADA: `{{EMPRESA_RAZAO_SOCIAL}}` (nome fantasia `{{EMPRESA}}`), CNPJ `{{CNPJ_EMPRESA}}`, endereço `{{ENDERECO_EMPRESA}}`, representada por `{{REPRESENTANTE_EMPRESA}}`.
   - CONTRATANTE: `{{CLIENTE_RAZAO_SOCIAL}}` (ou pessoa física `{{CLIENTE_NOME}}`), CNPJ/CPF `{{CLIENTE_CNPJ}}`, endereço `{{CLIENTE_ENDERECO}}`, representada por `{{CLIENTE_REPRESENTANTE}}`.

3. **Cláusula 1ª — Do Objeto**
   - O presente contrato tem por objeto a prestação, pela CONTRATADA à CONTRATANTE, dos seguintes serviços: `{{OBJETO}}`.

4. **Cláusula 2ª — Do Valor e Forma de Pagamento**
   - Valor total do serviço: `{{VALOR_SETUP}}` (setup único).
   - Mensalidade (se aplicável): `{{VALOR_MENSAL}}`/mês, a partir do go-live.
   - Forma de pagamento: `{{FORMA_PAGAMENTO}}`.
   - Pagamento via PIX, boleto ou transferência bancária, conforme acordo entre as partes.

5. **Cláusula 3ª — Do Prazo**
   - Prazo de execução: `{{PRAZO}}` dias corridos, contados a partir da data de aceite deste contrato e recebimento do sinal (ou conforme cronograma anexo).
   - Possíveis atrasos causados por falta de insumos da CONTRATANTE (conteúdo, acessos, aprovações) estendem o prazo proporcionalmente.

6. **Cláusula 4ª — Das Obrigações da CONTRATADA**
   - Entregar os serviços conforme escopo descrito.
   - Garantir sigilo sobre dados da CONTRATANTE.
   - Corrigir defeitos identificados em até 10 dias úteis após notificação formal.

7. **Cláusula 5ª — Das Obrigações da CONTRATANTE**
   - Fornecer todos os insumos necessários (acessos, conteúdo, briefing, materiais) no prazo combinado.
   - Efetuar os pagamentos na forma e prazo ajustados.
   - Participar ativamente das validações de cada etapa.

8. **Cláusula 6ª — Da Rescisão**
   - O presente contrato pode ser rescindido:
     a) Por mútuo acordo entre as partes.
     b) Por inadimplemento de qualquer cláusula, com notificação prévia de 15 dias.
   - Em caso de rescisão, valores já pagos pelas etapas concluídas não são reembolsáveis.

9. **Cláusula 7ª — Da Confidencialidade**
   - As partes comprometem-se a manter sigilo sobre informações confidenciais trocadas durante a execução do contrato, pelo prazo de 2 (dois) anos após o término.

10. **Cláusula 8ª — Da Propriedade Intelectual**
    - Os entregáveis (códigos, fluxos, configurações, copys) passam a ser de propriedade da CONTRATANTE após quitação integral.
    - Ferramentas/frameworks proprietárias da CONTRATADA continuam sendo dela (licença de uso não exclusiva pra CONTRATANTE).

11. **Cláusula 9ª — Do Foro**
    - Fica eleito o foro da Comarca de `{{FORO}}` para dirimir quaisquer dúvidas ou controvérsias oriundas do presente contrato.

12. **Assinaturas**
    - `{{CIDADE}}`, `{{DATA_ASSINATURA}}`.
    - Linha 1: `{{REPRESENTANTE_EMPRESA}}` (pela CONTRATADA)
    - Linha 2: `{{CLIENTE_REPRESENTANTE}}` (pela CONTRATANTE)
    - Linha 3: Testemunha 1 (opcional)
    - Linha 4: Testemunha 2 (opcional)

## Formatação docx

- Fonte: Times New Roman 12pt (padrão jurídico) ou Calibri 11pt
- Margens: 2.5cm todas
- Títulos de cláusula em negrito
- Espaçamento 1.5 entre linhas
- Parágrafos justificados
- Numeração automática de páginas no rodapé

## Observação legal

Este é um **template base** pra contratos simples de prestação de serviço. Pra contratos complexos (M&A, exclusividade, multas específicas, cláusulas trabalhistas) SEMPRE consultar advogado. A skill `/contrato` imprime aviso automático no output reforçando essa recomendação.
