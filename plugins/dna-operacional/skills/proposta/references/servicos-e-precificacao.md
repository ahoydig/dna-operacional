# Catálogo de Serviços e Precificação - {{EMPRESA}}

Referência para precificação de propostas. Valores são guias, não tabelados. Cada projeto é precificado caso a caso.

## Índice

1. [Frentes de Atuação](#frentes-de-atuação)
2. [Catálogo de Serviços](#catálogo-de-serviços)
3. [Calculadora de Preço](#calculadora-de-preço)
4. [Referência de Custos Operacionais](#referência-de-custos-operacionais)
5. [Tabela Resumo de Faixas](#tabela-resumo-de-faixas)

---

## Frentes de Atuação

### 1. Performance (Tráfego Pago)
Gestão de campanhas pagas em plataformas digitais.

**Plataformas:** Meta Ads (Facebook/Instagram), Google Ads, LinkedIn Ads, TikTok Ads

**O que inclui:**
- Auditoria das contas atuais
- Estratégia de campanhas
- Criação e gestão de anúncios
- Otimização contínua (diária/semanal)
- Relatórios de performance
- Setup de pixels e tracking

### 2. Automação e Inteligência Artificial
Sistemas automatizados com IA para diversas aplicações.

**Ferramentas internas (não mencionar ao cliente pelo nome):**
- Ferramenta interna A (orquestração de workflows)
- Ferramenta interna B (automação)
- Ferramenta interna C (framework de agentes IA)

**Referir ao cliente como:** "sistema proprietário da {{EMPRESA}}", "plataforma de automação", "motor de inteligência artificial"

**Tipos de projetos:**

#### Automação de Conteúdo
- Transcrição → conteúdo pronto
- Calendário editorial automático
- Roteiros, legendas, hashtags
- Agendamento de publicações

#### Chatbot com IA
- Atendimento 24/7
- FAQ inteligente
- Agendamento de reuniões
- Escalação para humano
- Integração com WhatsApp, site, Instagram

#### Agente SDR (Sales Development Representative)
- Prospecção automatizada
- Qualificação de leads
- Cadências de email/mensagem
- Follow-up automático
- Integração com CRM

#### Agente RAG (Retrieval-Augmented Generation)
- Base de conhecimento inteligente
- Busca semântica em documentos
- Respostas contextuais
- Treinamento com dados do cliente

#### Automação de Processos
- Integração entre sistemas
- Workflows automatizados
- Notificações inteligentes
- ETL (extração, transformação, carga de dados)

### 3. Dashboards
Painéis de visualização de dados em tempo real.

**O que inclui:**
- Levantamento de métricas-chave
- Conexão com fontes de dados (APIs, bancos, planilhas)
- Design dos painéis
- Alertas automáticos
- Treinamento de uso

### 4. Integrações
Conexão entre sistemas e plataformas do cliente.

**Exemplos:**
- CRM → ERP
- E-commerce → sistema de estoque
- Formulário → CRM → email
- Planilha → dashboard → alertas

### 5. Consultoria em IA
Diagnóstico e planejamento estratégico para uso de IA no negócio.

**O que inclui:**
- Diagnóstico de processos
- Mapeamento de oportunidades de automação
- Plano de implementação
- ROI estimado
- Priorização de projetos

---

## Calculadora de Preço

### Metodologia

O preço é composto por duas partes:

```
SETUP (pagamento único) = (Horas estimadas × Valor/hora) + Custos fixos de implementação
MENSALIDADE = (Horas mensais de manutenção × Valor/hora) + Custos recorrentes
```

### Passo a passo

**1. Estimar horas de trabalho**

Perguntar ao usuário:
- Quantas horas você estima para o setup?
- Quantas horas mensais de manutenção?
- Qual a complexidade? (baixa / média / alta)

Se o usuário não souber, usar as referências abaixo.

**2. Definir valor/hora**

O valor/hora varia conforme complexidade e tipo de serviço. Perguntar ao usuário qual valor deseja praticar, ou sugerir baseado na complexidade:

| Complexidade | Faixa sugerida |
|-------------|----------------|
| Baixa | R$ 80 - 120/h |
| Média | R$ 120 - 200/h |
| Alta | R$ 200 - 350/h |

**3. Levantar custos operacionais**

Custos de ferramentas e APIs que o projeto exige. Ver seção "Referência de Custos Operacionais" abaixo.

**4. Aplicar margem sobre custos operacionais**

Margem de **50% a 80%** sobre custos operacionais que a {{EMPRESA}} gerencia.

Exemplo: se o custo operacional de automação é R$ 50/mês, cobrar R$ 75-90/mês (50-80% de margem).

Custos que são responsabilidade direta do cliente (tokens de IA, ferramentas que ele usa) NÃO levam margem. São listados como "custos adicionais, responsabilidade do cliente".

**5. Montar a proposta de preço**

```
SETUP = (horas_setup × valor_hora) + custos_implementacao
MENSALIDADE = (horas_manutencao × valor_hora) + (custos_recorrentes × margem)
```

### Exemplo de cálculo

**Projeto: Automação de Conteúdo**
- Complexidade: média
- Valor/hora: R$ 150
- Horas de setup: 20h
- Horas de manutenção mensal: 4h
- Custo da ferramenta de automação: R$ 50/mês (interno {{EMPRESA}})
- Margem: 60%

```
SETUP = (20 × R$ 150) + R$ 100 (licenças) = R$ 3.100
MENSALIDADE = (4 × R$ 150) + (R$ 50 × 1.6) = R$ 600 + R$ 80 = R$ 680
```

Arredondar para valores "limpos": Setup R$ 3.100, Mensalidade R$ 700.

---

## Referência de Custos Operacionais

Custos aproximados de ferramentas e APIs. Valores de referência, podem variar.

### Custos {{EMPRESA}} (inclusos na mensalidade, com margem)

| Item | Custo estimado | Notas |
|------|---------------|-------|
| Ferramenta interna A (orquestração) | R$ 0-50/mês | Self-hosted, custo de infra |
| Servidor/hosting | R$ 30-100/mês | Depende da escala |
| Domínios e DNS | ~R$ 5/mês | Se necessário |

### Custos do Cliente (listados como "custos adicionais")

| Item | Custo estimado | Notas |
|------|---------------|-------|
| Tokens de IA (Claude/OpenAI) | R$ 50-300/mês | Depende muito do volume |
| ClickUp | Gratuito ou R$ 30-80/mês | Plano free é suficiente para maioria |
| CRM (Hubspot, Pipedrive) | R$ 0-200/mês | Muitos têm plano gratuito |
| Ferramenta de agendamento (mLabs, Buffer) | R$ 50-150/mês | Depende do plano |
| Meta Ads (verba) | Variável | Cliente define budget |
| Google Ads (verba) | Variável | Cliente define budget |
| Ferramentas de email (Resend, SendGrid) | R$ 0-50/mês | Planos gratuitos generosos |
| Hospedagem web | R$ 20-100/mês | Se projeto inclui frontend |
| Domínio | R$ 40-80/ano | Se necessário |

---

## Tabela Resumo de Faixas

Faixas de preço por tipo de serviço. São referências para ajudar na precificação, não valores fixos.

| Serviço | Setup (faixa) | Mensalidade (faixa) | Horas setup | Horas/mês |
|---------|--------------|--------------------|-----------:|----------:|
| Automação de Conteúdo | R$ 2.500 - 6.000 | R$ 600 - 1.500 | 15-35h | 3-8h |
| Chatbot com IA | R$ 2.000 - 5.000 | R$ 500 - 1.200 | 12-30h | 3-6h |
| Agente SDR | R$ 3.000 - 8.000 | R$ 800 - 2.000 | 20-40h | 4-10h |
| Agente RAG | R$ 2.500 - 7.000 | R$ 600 - 1.500 | 15-35h | 3-8h |
| Automação de Processos | R$ 1.500 - 5.000 | R$ 400 - 1.200 | 10-25h | 2-6h |
| Dashboard | R$ 1.500 - 4.000 | R$ 300 - 800 | 10-20h | 2-4h |
| Integração de Sistemas | R$ 1.000 - 4.000 | R$ 300 - 800 | 8-20h | 2-4h |
| Tráfego Pago | R$ 1.000 - 3.000 | R$ 800 - 2.500 | 8-15h | 8-20h |
| Consultoria IA | R$ 2.000 - 5.000 | - | 10-25h | - |

**Notas:**
- Tráfego pago tem setup menor mas mensalidade maior (gestão contínua intensiva)
- Consultoria geralmente não tem mensalidade (entrega pontual)
- Projetos de alta complexidade podem ultrapassar essas faixas
- Combos de serviços: oferecer desconto de 10-15% no setup total

---

## Regras de Apresentação de Preço na Proposta

1. **Sempre arredondar** para valores "limpos" (R$ 900, R$ 4.100, não R$ 873,50)
2. **Não mostrar breakdown de horas/valor-hora** para o cliente. Mostrar apenas o valor final do setup e da mensalidade com lista do que inclui
3. **Custos adicionais separados**: Listar custos do cliente em seção separada com estimativas de faixa (~R$ 100 a 200/mês)
4. **Custo total mensal**: Calcular e mostrar o custo total (mensalidade + custos adicionais estimados) para o cliente ter visão real
5. **ROI**: Sempre comparar com a alternativa (profissional humano, agência, etc.) para justificar o investimento
6. **Formas de pagamento padrão**: Pix, Transferência Bancária
7. **Parcelamento**: "Consulte condições de parcelamento para o setup"
