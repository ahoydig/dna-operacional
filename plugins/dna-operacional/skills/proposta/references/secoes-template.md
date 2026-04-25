# Seções Template - Propostas {{EMPRESA}}

Templates HTML para cada seção de proposta. Use o CSS completo de `design-system.md`. Adapte o conteúdo conforme o serviço vendido.

## Índice

1. [Capa (dark)](#1-capa)
2. [Apresentação](#2-apresentação)
3. [O Que Vamos Construir](#3-o-que-vamos-construir)
4. [Como Funciona](#4-como-funciona)
5. [Ferramentas](#5-ferramentas)
6. [Comparativo + ROI](#6-comparativo--roi)
7. [Investimento + Custos + Pagamento](#7-investimento)
8. [Observações](#8-observações)
9. [Próximos Passos + Contato (dark)](#9-próximos-passos)

Cada proposta tem entre 8 e 10 páginas. As seções 3 e 4 podem ocupar mais de uma página dependendo da complexidade do serviço.

---

## 1. Capa

Página dark com branding completo. Adaptar título e subtítulo ao tipo de serviço.

```html
<div class="page cover">
  <div class="cover-pattern"></div>
  <div class="cover-line-top"></div>
  <img class="logo-cover" src="{{LOGO_DARK_PATH}}" alt="{{EMPRESA}}">
  <div class="green-line"></div>
  <h1>{{TÍTULO PRINCIPAL}}<br><span>{{SUBTÍTULO DESTAQUE}}</span></h1>
  <p class="subtitle">Preparado para {{NOME_EMPRESA}}</p>
  <div class="meta">
    <div class="label">Destinatário</div>
    <div class="value">{{NOME_DESTINATARIO}}</div>
    <div class="date">{{MÊS ANO}}</div>
  </div>
  <div class="cover-footer">
    <div class="footer-text">Documento confidencial &bull; {{EMPRESA}}</div>
  </div>
</div>
```

**Títulos por tipo de serviço:**

| Serviço | Título | Subtítulo (span lime) |
|---------|--------|----------------------|
| Automação com IA | Proposta de Automação com | Inteligência Artificial |
| Tráfego Pago | Proposta de Gestão de | Tráfego Pago |
| Dashboard | Proposta de Dashboard | Inteligente |
| Chatbot IA | Proposta de Chatbot com | Inteligência Artificial |
| Agente SDR | Proposta de Agente SDR com | Inteligência Artificial |
| Agente RAG | Proposta de Base de Conhecimento com | Inteligência Artificial |
| Integração | Proposta de Integração | de Sistemas |
| Consultoria IA | Proposta de Consultoria em | Inteligência Artificial |

---

## 2. Apresentação

Introdução da {{EMPRESA}} + contexto do problema do cliente + stats bar.

```html
<div class="page content-page">
  <div class="page-header">
    <img class="logo-header" src="{{LOGO_LIGHT_PATH}}" alt="{{EMPRESA}}">
    <span class="page-label">Proposta Comercial</span>
  </div>

  <span class="section-number">01</span>
  <h2 class="section-title">Apresentação</h2>

  <p class="highlight-text">{{FRASE_DESTAQUE}}</p>

  <p>Entendemos que a <strong>{{NOME_EMPRESA}}</strong> {{DESCRIÇÃO_DO_PROBLEMA_OU_NECESSIDADE}}</p>

  <p>{{FRASE_DA_SOLUÇÃO_PROPOSTA}}</p>

  <div class="stats-bar">
    <div class="stat-item">
      <span class="stat-value">{{VALOR}}</span>
      <span class="stat-label">{{LABEL}}</span>
    </div>
    <!-- Repetir 3-4 stat-items -->
  </div>

  {{PAGE_FOOTER}}
</div>
```

**Stats por tipo de serviço (sugestões):**

| Serviço | Stat 1 | Stat 2 | Stat 3 | Stat 4 |
|---------|--------|--------|--------|--------|
| Automação IA | N inteligências | 24/7 disponível | X min por tarefa | 100% automatizado |
| Tráfego Pago | X plataformas | Otimização diária | ROI médio X% | Relatórios semanais |
| Dashboard | X métricas | Tempo real | X integrações | Alertas automáticos |
| Chatbot | 24/7 | X idiomas | Xms resposta | X% resolução |
| Agente SDR | X leads/dia | 24/7 prospecção | X% conversão | Multi-canal |

---

## 3. O Que Vamos Construir

Cards com itens numerados do que será entregue. Usar grid 2x para itens pares, com último item full-width se ímpar.

```html
<div class="page content-page">
  {{PAGE_HEADER}}

  <span class="section-number">02</span>
  <h2 class="section-title">{{TÍTULO_DA_SEÇÃO}}</h2>

  <p class="highlight-text">{{RESUMO_DO_QUE_SERÁ_ENTREGUE}}</p>

  <p>{{DESCRIÇÃO_COMPLEMENTAR}}</p>

  <div class="ia-grid">
    <div class="ia-card">
      <div class="ia-badge">01</div>
      <div class="ia-content">
        <h4>{{NOME_DO_ITEM}}</h4>
        <p>{{DESCRIÇÃO_CURTA}}</p>
      </div>
    </div>
    <!-- Repetir para cada item -->
    <!-- Último item ímpar: adicionar class="ia-card ia-card-full" -->
  </div>

  {{PAGE_FOOTER}}
</div>
```

**Títulos por tipo de serviço:**

| Serviço | Título da seção | Tipo de cards |
|---------|----------------|---------------|
| Automação IA | Seu Time Digital | IAs/especialistas do sistema |
| Tráfego Pago | O Que Vamos Fazer | Etapas do serviço (auditoria, setup, otimização) |
| Dashboard | O Que Será Monitorado | Métricas e painéis inclusos |
| Chatbot | Capacidades do Chatbot | Funcionalidades (FAQ, agendamento, escalação) |
| Agente SDR | O Agente SDR | Capacidades (prospecção, qualificação, follow-up) |
| Integração | Sistemas Integrados | Cada sistema/API conectada |

**Limites de conteúdo por página:** Máximo 7 cards (grid 2x3 + 1 full). Se tiver mais, dividir em duas páginas.

---

## 4. Como Funciona

Cards de fases/etapas + pipeline de status (quando aplicável).

```html
<div class="page content-page">
  {{PAGE_HEADER}}

  <span class="section-number">03</span>
  <h2 class="section-title">Como Funciona</h2>

  <p class="highlight-text">{{RESUMO_DO_FLUXO}}</p>

  <div class="phase-grid">
    <div class="phase-card">
      <span class="phase-num">Fase 01</span>
      <h4>{{NOME_DA_FASE}}</h4>
      <p>{{DESCRIÇÃO}}</p>
    </div>
    <!-- Repetir para cada fase (4-5 fases) -->
    <!-- Última fase ímpar: adicionar class="phase-card phase-card-full" -->
  </div>

  <!-- PIPELINE (opcional, apenas para serviços com workflow de status) -->
  <div class="pipeline-section">
    <p class="pipeline-label">{{TÍTULO_DO_PIPELINE}}</p>
    <div class="pipeline-row">
      <span class="pipeline-badge badge-dark">{{STATUS_1}}</span>
      <span class="pipeline-arrow">&rarr;</span>
      <span class="pipeline-badge badge-dark">{{STATUS_2}}</span>
      <span class="pipeline-arrow">&rarr;</span>
      <span class="pipeline-badge badge-lime">{{STATUS_ATIVO}}</span>
      <span class="pipeline-arrow">&rarr;</span>
      <span class="pipeline-badge badge-green">{{STATUS_FINAL}}</span>
    </div>
  </div>

  {{PAGE_FOOTER}}
</div>
```

**Pipeline legend (página seguinte se pipeline for complexo):**

```html
<div class="pipeline-legend">
  <div class="legend-item">
    <span class="legend-badge badge-dark">{{STATUS}}</span>
    <span class="legend-text">{{DESCRIÇÃO_DO_STATUS}}</span>
  </div>
  <!-- Repetir -->
  <!-- Último item ímpar: style="grid-column: 1 / -1;" -->
</div>
```

---

## 5. Ferramentas

Cards com borda lateral verde para cada ferramenta.

```html
<div class="page content-page">
  {{PAGE_HEADER}}

  <span class="section-number">04</span>
  <h2 class="section-title">Ferramentas</h2>

  <div class="tool-card">
    <h4>{{NOME_FERRAMENTA}}: {{SUBTÍTULO}}</h4>
    <p>{{DESCRIÇÃO}}</p>
  </div>

  <!-- Opcional: opções para o cliente escolher -->
  <div class="tool-card">
    <h4>{{NOME}}: {{SUBTÍTULO}}</h4>
    <p>{{DESCRIÇÃO}}</p>
    <div class="tool-options">
      <div class="tool-option">{{OPÇÃO_1}}</div>
      <div class="tool-option">{{OPÇÃO_2}}</div>
      <div class="tool-option">{{OPÇÃO_3}}</div>
    </div>
    <p class="tool-rec">{{RECOMENDAÇÃO}}</p>
  </div>

  {{PAGE_FOOTER}}
</div>
```

**Regras sobre ferramentas:**
- NÃO mencionar nomes de ferramentas internas da empresa
- Referir à automação como "sistema proprietário da {{EMPRESA}}"
- Claude API / IA referir como "inteligência artificial" ou "consumo de IA"
- Ferramentas do cliente (ClickUp, CRMs, etc.) podem ser nomeadas

---

## 6. Comparativo + ROI

Tabela comparativa + ROI boxes + custo total.

```html
<div class="page content-page">
  {{PAGE_HEADER}}

  <span class="section-number">05</span>
  <h2 class="section-title">Comparativo: {{SOLUCAO}} vs. {{ALTERNATIVA}}</h2>

  <table class="comparison-table">
    <thead>
      <tr>
        <th style="width: 26%;"></th>
        <th style="width: 37%;">{{ALTERNATIVA_NOME}}</th>
        <th style="width: 37%;">{{SOLUCAO_NOME}}</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>{{CRITÉRIO}}</td><td>{{VALOR_ALT}}</td><td>{{VALOR_PROPOSTA}}</td></tr>
      <!-- Repetir 6-8 linhas -->
    </tbody>
  </table>

  <div class="roi-grid">
    <div class="roi-box">
      <div class="roi-label">Economia mensal estimada</div>
      <div class="roi-value">R$ {{VALOR}}</div>
      <div class="roi-detail">{{DETALHE}}</div>
    </div>
    <div class="roi-box">
      <div class="roi-label">Economia anual estimada</div>
      <div class="roi-value">R$ {{VALOR}}</div>
      <div class="roi-detail">{{DETALHE}}</div>
    </div>
  </div>

  <div class="total-box">
    <div class="total-label">Custo total mensal estimado (tudo incluso)</div>
    <div class="total-value">R$ {{MIN}} a R$ {{MAX}} /mês</div>
    <div class="total-detail">{{BREAKDOWN}}</div>
  </div>

  {{PAGE_FOOTER}}
</div>
```

**Alternativas comuns por serviço:**

| Serviço | Comparar com |
|---------|-------------|
| Automação IA | Profissional humano (roteirista, social media, assistente) |
| Tráfego Pago | Gestão interna / agência genérica |
| Dashboard | Planilhas manuais / ferramentas avulsas |
| Chatbot | Atendente humano / SAC tradicional |
| Agente SDR | SDR humano / prospecção manual |
| Integração | Processos manuais / copiar/colar entre sistemas |

---

## 7. Investimento

Setup + mensalidade + custos adicionais + formas de pagamento.

```html
<div class="page content-page">
  {{PAGE_HEADER}}

  <span class="section-number">06</span>
  <h2 class="section-title">Investimento</h2>

  <div class="investment-grid">
    <div class="investment-card">
      <div class="inv-label">Pagamento único</div>
      <div class="inv-price">R$ {{SETUP}}</div>
      <div class="inv-period">Setup e configuração</div>
      <ul>
        <li>{{ITEM_SETUP_1}}</li>
        <li>{{ITEM_SETUP_2}}</li>
        <!-- 4-5 itens -->
      </ul>
    </div>
    <div class="investment-card">
      <div class="inv-label">Mensalidade</div>
      <div class="inv-price">R$ {{MENSAL}}</div>
      <div class="inv-period">Por mês</div>
      <ul>
        <li>{{ITEM_MENSAL_1}}</li>
        <li>{{ITEM_MENSAL_2}}</li>
        <!-- 4-5 itens -->
      </ul>
    </div>
  </div>

  <div style="height: 16px;"></div>

  <!-- CUSTOS ADICIONAIS (se houver) -->
  <span class="section-number" style="font-size: 32pt;">07</span>
  <h2 class="section-title" style="font-size: 15pt;">Custos Adicionais</h2>
  <p style="font-size: 9pt; color: var(--gray); margin-bottom: 10px;">Responsabilidade do cliente</p>

  <div class="costs-box">
    <div class="cost-item">
      <span class="cost-name">{{NOME_CUSTO}}</span>
      <span class="cost-value">{{VALOR_ESTIMADO}}</span>
    </div>
    <!-- Repetir -->
  </div>

  <p style="font-size: 8.5pt; color: var(--gray); margin-top: 8px; font-style: italic;">{{NOTA_CUSTOS}}</p>

  <div style="height: 12px;"></div>

  <p style="font-size: 10pt; font-weight: 600; color: var(--dark); margin-bottom: 6px;">Formas de pagamento</p>
  <div class="payment-row">
    <div class="payment-badge">Pix</div>
    <div class="payment-badge">Transferência Bancária</div>
  </div>
  <p class="payment-note">Consulte condições de parcelamento para o setup.</p>

  {{PAGE_FOOTER}}
</div>
```

**Itens de setup comuns por serviço:**

| Serviço | Itens do setup |
|---------|---------------|
| Automação IA | Configuração do sistema, treinamento das IAs, integração com ferramentas, fluxos automáticos, testes |
| Tráfego Pago | Auditoria atual, setup de contas, criação de campanhas, pixels/tracking, primeira otimização |
| Dashboard | Levantamento de métricas, conexão com fontes, design dos painéis, alertas, treinamento |
| Chatbot | Mapeamento de fluxos, treinamento da IA, integração com sistemas, testes, deploy |
| Agente SDR | Definição de ICP, templates de mensagem, integração com CRM, configuração de cadências, testes |

**Itens da mensalidade comuns:**
- Monitoramento contínuo (observabilidade)
- Atualizações quando APIs mudam
- Correção de bugs e problemas
- Otimização de performance
- Suporte técnico

---

## 8. Observações

Cards com borda verde lateral + info badges para prazo e validade.

```html
<div class="page content-page">
  {{PAGE_HEADER}}

  <span class="section-number">08</span>
  <h2 class="section-title">Observações Importantes</h2>

  <div class="note-item">
    <p><strong>{{TÍTULO}}:</strong> {{TEXTO}}</p>
  </div>
  <!-- Repetir 3-5 notas -->

  <div class="info-row">
    <div class="info-badge">
      <div class="info-label">Prazo de entrega</div>
      <div class="info-value">{{PRAZO}}</div>
      <div style="font-size: 8pt; color: var(--gray); margin-top: 2px;">{{CONDIÇÃO}}</div>
    </div>
    <div class="info-badge">
      <div class="info-label">Validade da proposta</div>
      <div class="info-value">30 dias</div>
      <div style="font-size: 8pt; color: var(--gray); margin-top: 2px;">A partir da data de emissão ({{MÊS ANO}})</div>
    </div>
  </div>

  {{PAGE_FOOTER}}
</div>
```

**Observações padrão (incluir sempre que aplicável):**
- Aprovação humana: nada é publicado/executado sem aprovação
- Manutenção contínua: APIs mudam, a mensalidade garante correção rápida
- Melhoria contínua: o sistema melhora com o tempo
- Responsabilidades do cliente: o que o cliente precisa fornecer/fazer

---

## 9. Próximos Passos + Contato (dark closing)

Página de fechamento dark com steps numerados e contato.

```html
<div class="page closing-page">
  <div class="cover-pattern"></div>

  <img src="{{LOGO_DARK_PATH}}" alt="{{EMPRESA}}" style="width: 180px; margin-bottom: 40px;">

  <span class="section-number" style="color: var(--lime);">09</span>
  <h2 style="font-family: '{{FONT_HEADLINE_NAME}}', sans-serif; font-size: 20pt; text-transform: uppercase; letter-spacing: 2px; color: var(--light); margin-bottom: 8px;">Próximos Passos</h2>
  <p style="font-size: 11pt; color: rgba(255,255,255,0.5); margin-bottom: 8px;">Veja como é simples começar:</p>

  <div class="step-grid">
    <div class="step-item">
      <div class="step-number">1</div>
      <div class="step-content">
        <h4>{{PASSO_TÍTULO}}</h4>
        <p>{{PASSO_DESCRIÇÃO}}</p>
      </div>
    </div>
    <!-- Repetir 4-5 passos -->
  </div>

  <div class="contact-section">
    <div class="contact-label">Entre em contato</div>
    <div class="contact-value">{{EMAIL_EMPRESA}}</div>
  </div>

  <div class="validity-note">
    Esta proposta é válida por 30 dias a partir da data de emissão &bull; Documento confidencial &bull; {{EMPRESA}} &bull; {{MÊS ANO}}
  </div>
</div>
```

**Próximos passos padrão:**
1. Aceite a proposta (confirme e realize pagamento do setup)
2. {{PASSO_ESPECÍFICO_DO_SERVIÇO}} (ex: envie as Skills, forneça acessos, etc.)
3. Configuração do sistema (nossa equipe configura em X dias)
4. Treinamento de uso (como usar o sistema)
5. Sistema ativo (tudo funcionando)

---

## Fragmentos Reutilizáveis

### Page Header (content pages)
```html
<div class="page-header">
  <img class="logo-header" src="{{LOGO_LIGHT_PATH}}" alt="{{EMPRESA}}">
  <span class="page-label">Proposta Comercial</span>
</div>
```

### Page Footer (content pages)
```html
<div class="page-footer">
  <img class="footer-logo" src="{{LOGO_LIGHT_PATH}}" alt="{{EMPRESA}}">
  <span class="footer-text">Proposta Comercial &bull; {{NOME_EMPRESA}} &bull; {{MÊS ANO}}</span>
</div>
```

---

## Regras de Montagem

1. **Numeração de seções**: Sequencial de 01 a 09 (ou menos se proposta menor). Se duas seções dividem uma página, a segunda usa `font-size: 32pt` para o number e `font-size: 15pt` para o title.
2. **Overflow**: Cada página tem `overflow: hidden`. Se o conteúdo não cabe, divida em duas páginas.
3. **Grid ímpar**: Último card de grid 2-col com número ímpar de items usa `grid-column: 1 / -1` para ocupar full width.
4. **Pipeline**: Só usar quando o serviço tem workflow de status. Tráfego pago e consultoria geralmente não têm.
5. **ROI**: Sempre calcular economia comparada à alternativa. Sem ROI não tem comparativo.
6. **Custos adicionais**: Só incluir se houver custos fora do pacote (tokens IA, ferramentas, etc.). Se tudo está incluso, pular esta seção.
7. **Observações**: Adaptar ao serviço. Nem toda proposta tem "criação de Skills" como responsabilidade do cliente.
