---
name: proposta
description: Gera propostas comerciais premium em PDF para a {{EMPRESA}}. Fluxo guiado que coleta dados do cliente, ajuda na precificação (calculadora com custos operacionais e margem de 50-80%), gera HTML com design premium (dark cover + light content pages, fonte {{FONT_HEADLINE_NAME}}, branding configurável), converte para PDF via Playwright, verifica visualmente cada página, e salva histórico. Use SEMPRE que o usuário mencionar "proposta", "criar proposta", "gerar proposta", "nova proposta", "proposta para [cliente]", ou quiser montar uma proposta comercial. Também use quando pedir para "precificar", "calcular preço de projeto", ou "quanto cobrar".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Gerador de Propostas Comerciais - {{EMPRESA}}

Cria propostas comerciais premium em PDF com o branding da {{EMPRESA}}. Inclui módulo de precificação com calculadora de custos.

## Diretório de trabalho

Todas as propostas ficam em: `${PROPOSTAS_DIR}/` (default: `data/clientes/<slug>/orcamentos/` se rodando dentro do plugin DNA Operacional, ou pergunte ao usuário).

Assets necessários no diretório:
- `{{LOGO_DARK_PATH}}` (logo branco, para fundo escuro)
- `{{LOGO_LIGHT_PATH}}` (logo escuro, para fundo claro)
- `{{FONT_HEADLINE_PATH_WOFF2}}` (fonte headlines, formato woff2)

## Branding configurável (passo zero)

Antes de gerar qualquer proposta, a skill precisa saber o branding da empresa que está enviando a proposta. Lê na seguinte ordem de prioridade:

1. `${CWD}/reference/branding.md` (criado pelo `/setup-projeto` do plugin DNA Operacional)
2. `CLAUDE.md` do projeto (seções `# Projeto <nome>`, `## Contato:`, `## Branding:`)
3. Pergunta interativa via `AskUserQuestion` (último recurso)

Placeholders que precisam ser preenchidos antes de gerar HTML:

| Placeholder | Default neutro | Descrição |
|------------|---------------|-----------|
| `{{EMPRESA}}` | `Sua Empresa` | Nome da empresa que envia a proposta |
| `{{EMPRESA_RAZAO_SOCIAL}}` | `Sua Empresa Ltda.` | Razão social completa |
| `{{EMAIL_EMPRESA}}` | `contato@sua-empresa.com` | E-mail de contato |
| `{{HANDLE}}` | `@suaempresa` | Handle Instagram/social |
| `{{COR_PRIMARIA}}` | `#0F172A` (slate-900) | Cor escura (background capa, dark pages) |
| `{{COR_DESTAQUE}}` | `#10B981` (emerald-500) | Cor de destaque (section numbers, badges) |
| `{{COR_DESTAQUE_BRIGHT}}` | `#34D399` | Variante mais vibrante |
| `{{COR_LIME}}` | `#A7F3D0` | Highlight em capa (ROI, títulos destaque) |
| `{{LOGO_DARK_PATH}}` | (sem default — perguntar) | SVG do logo branco (fundo escuro) |
| `{{LOGO_LIGHT_PATH}}` | (sem default — perguntar) | SVG do logo escuro (fundo claro) |
| `{{FONT_HEADLINE_NAME}}` | `Inter` (fallback se ausente) | Nome da família de headlines |
| `{{FONT_HEADLINE_PATH_WOFF2}}` | (opcional — usa Inter se ausente) | Path da fonte |

Se o user não tiver logos/fontes próprias, oferecer **modo padrão neutro**: usar Inter para tudo + emoji ou nome da empresa em texto no lugar do logo. Não bloqueia.

## Fluxo de Execução

### Fase 1: Coleta de Dados (Conversa Guiada)

Use `AskUserQuestion` para coletar dados em rodadas:

**Rodada 1 - Cliente:**
- Nome da empresa/marca do cliente
- Nome do destinatário (pessoa que recebe a proposta)

**Rodada 2 - Serviço:**
- Tipo de serviço (apresentar opções baseadas no catálogo em `references/servicos-e-precificacao.md`)
- Descrição do escopo (o que será entregue)
- Ferramentas envolvidas

**Rodada 3 - Preço e Detalhes:**
- Precisa de ajuda com precificação? (Sim → vai para Fase 2, Não → pede valores diretos)
- Se não: valor do setup e valor da mensalidade
- Custos adicionais do cliente (tokens IA, ferramentas, etc.)
- Observações especiais (responsabilidades do cliente, prazos especiais, etc.)

### Fase 2: Precificação (Opcional)

Quando o usuário pedir ajuda para precificar:

1. Leia `references/servicos-e-precificacao.md` para entender faixas e referências
2. Pergunte ao usuário:
   - Complexidade do projeto (baixa/média/alta)
   - Horas estimadas (ou peça para o usuário estimar)
   - Valor/hora desejado (ou sugira baseado na complexidade)
   - Custos operacionais fixos (ferramentas, APIs, hospedagem)
3. Calcule:
   - **Setup** = (horas estimadas × valor/hora) + custos fixos de implementação
   - **Mensalidade** = (horas mensais de manutenção × valor/hora) + custos recorrentes
   - Aplique margem de **50% a 80%** sobre custos operacionais
4. Apresente a sugestão com breakdown detalhado
5. Peça confirmação ou ajustes do usuário

### Fase 3: Geração do HTML

1. Leia `references/design-system.md` para o CSS completo e regras de estrutura
2. Leia `references/secoes-template.md` para os padrões HTML de cada seção
3. Monte o HTML completo adaptando o conteúdo ao serviço vendido
4. Cada proposta deve ter entre 8 e 10 páginas (adaptar conforme o conteúdo)
5. Salve como `proposta-[nome-cliente-lowercase].html`

**Seções obrigatórias em toda proposta:**
1. Capa (dark) - logo, título, cliente, destinatário, data
2. Apresentação - quem é a {{EMPRESA}}, entendimento do problema do cliente, stats bar
3. O Que Vamos Construir - descrição do sistema/solução com detalhes
4. Como Funciona - fases do processo, pipeline de status
5. Ferramentas - tecnologias utilizadas, explicações
6. Comparativo + ROI - tabela comparativa, economia estimada, custo total mensal
7. Investimento - setup + mensalidade, custos adicionais, formas de pagamento
8. Observações - responsabilidades, aprovação humana, manutenção, melhoria contínua
9. Próximos Passos + Contato (dark) - steps numerados, email, prazo, validade

### Fase 4: Conversão para PDF

1. Verifique se há um servidor HTTP rodando na porta 8766:
   ```bash
   lsof -i :8766 2>/dev/null | head -3
   ```
2. Se não houver, inicie um:
   ```bash
   cd ${PROPOSTAS_DIR} && python3 -m http.server 8766 &
   ```
3. Navegue com Playwright: `http://localhost:8766/proposta-[cliente].html`
4. Gere o PDF com:
   ```javascript
   await page.pdf({
     path: '${PROPOSTAS_DIR}/proposta-[cliente].pdf',
     format: 'A4',
     printBackground: true,
     margin: { top: '0', right: '0', bottom: '0', left: '0' }
   });
   ```

### Fase 5: Verificação Visual

**Leia o PDF gerado com a Read tool e verifique CADA PÁGINA:**
- Conteúdo completo (nenhum texto cortado ou overflow)
- Logos aparecendo corretamente nos headers e footers
- Sem barras verdes ou artefatos visuais
- Acentos corretos em português
- Sem espaços vazios excessivos
- Pipeline de status legível
- Tabelas completas sem linhas cortadas

Se encontrar problemas, corrija o HTML e regenere. Repita até estar perfeito.

### Fase 6: Histórico

Após gerar o PDF final, salve o registro em `${PROPOSTAS_DIR}/historico-propostas.json`:

```json
{
  "propostas": [
    {
      "id": "YYYY-MM-cliente",
      "cliente": "Nome da Empresa",
      "destinatario": "Nome da Pessoa",
      "servico": "Tipo de serviço",
      "setup": 4100,
      "mensal": 900,
      "data": "YYYY-MM-DD",
      "arquivo_html": "proposta-cliente.html",
      "arquivo_pdf": "proposta-cliente.pdf",
      "status": "gerada",
      "notas": ""
    }
  ]
}
```

Se o arquivo já existir, adicione ao array. Se não, crie-o.

## Regras Críticas de Design (Chromium Print)

Estas regras são inegociáveis. Violar qualquer uma causa bugs visuais no PDF:

1. **NUNCA** use `background-clip: text` com `-webkit-text-fill-color: transparent`. Renderiza como retângulos sólidos no print. Use `color: var(--green)` ou `color: var(--lime)` direto.
2. **NUNCA** use `radial-gradient` com `transparent` em elementos visíveis. Renderiza como blocos coloridos. Dot patterns sutis com opacidade muito baixa (0.04-0.05) são ok.
3. **NUNCA** use `file://` para carregar no Playwright. Sempre use servidor HTTP local.
4. Cada página deve ter `height: 297mm`, `overflow: hidden`, `page-break-after: always`.
5. Logos devem ser `<img>` tags, nunca SVG inline (trunca o conteúdo).

## Regras de Conteúdo

1. **Português perfeito**: Todos os acentos corretos (automação, inteligência, não, está, etc.)
2. **Sem vícios de IA**: Nunca use em-dashes (—), hífens estilísticos, ou construções como "—" entre frases. Use dois pontos, pontos, ou parênteses.
3. **Tom profissional**: Direto, claro, sem jargão excessivo. O cliente precisa entender.
4. **Contato padrão**: {{EMAIL_EMPRESA}}
5. **Validade padrão**: 30 dias
6. **Prazo padrão**: 7 a 10 dias úteis (ajustar conforme projeto)
7. **Formas de pagamento**: Pix, Transferência Bancária

## Referências

- `references/design-system.md` - CSS completo, estrutura de página, cores, tipografia
- `references/secoes-template.md` - HTML de cada seção com exemplos e orientações
- `references/servicos-e-precificacao.md` - Catálogo de serviços, precificação, calculadora
