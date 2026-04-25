# Design System - Propostas {{EMPRESA}}

## Cores

| Variável | Hex | Uso |
|----------|-----|-----|
| `--dark` | `{{COR_PRIMARIA}}` (default `#0F172A`) | Background capa, dark pages, badges |
| `--green` | `{{COR_DESTAQUE}}` (default `#10B981`) | Section numbers, acentos, badges |
| `--green-bright` | `{{COR_DESTAQUE_BRIGHT}}` (default `#34D399`) | Destaques secundários |
| `--lime` | `{{COR_LIME}}` (default `#A7F3D0`) | Títulos destaque na capa, ROI values |
| `--light` | `{{COR_FUNDO_CLARO}}` (default `#F2F2F2`) | Background páginas de conteúdo |
| `--gray` | #8a9199 | Textos secundários, labels |
| `--card-bg` | #FFFFFF | Background de cards |
| `--text` | #1a1a2e | Texto principal em páginas claras |
| `--text-muted` | #555 | Texto secundário em cards |

## Tipografia

- **Headlines**: font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif
- **Body**: font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif
- **Section numbers**: 40pt {{FONT_HEADLINE_NAME}}, color: var(--green)
- **Section titles**: 18pt {{FONT_HEADLINE_NAME}}, uppercase, letter-spacing: 2px
- **Highlight text**: 12pt, font-weight: 600
- **Body text**: 11pt, line-height: 1.65
- **Card titles**: 10-11pt, font-weight: 700, uppercase
- **Card body**: 9-9.5pt, color: var(--text-muted)

## Estrutura de Página A4

Cada página DEVE ter:
- `width: 210mm; height: 297mm`
- `overflow: hidden` (CRÍTICO: previne content overflow)
- `page-break-after: always` (exceto última)
- `page-break-inside: avoid`

### Cover page (dark)
- Background: var(--dark)
- Pattern: dot grid com radial-gradient (opacidade 0.05 max)
- Green line no topo: 4px, gradient green→lime→green
- Logo: 260px width
- Título: 30pt {{FONT_HEADLINE_NAME}}, uppercase
- Span destaque: color: var(--lime)

### Content pages (light)
- Background: var(--light)
- Padding: 32px 46px 56px
- Header: logo (38px height) + "Proposta Comercial" label
- Footer: absolute bottom, logo (24px, opacity 0.5) + texto

### Closing page (dark)
- Background: var(--dark)
- Flex column, justify-content: center
- Pattern: dot grid (mesma da cover, opacidade 0.04)
- Logo: 180px width

## Assets e Paths

Todos relativos ao diretório `${PROPOSTAS_DIR}/`:

```
Fonte de headlines (configurável — default Inter se ausente):
  {{FONT_HEADLINE_PATH_WOFF2}}
  {{FONT_HEADLINE_PATH_WOFF}}

Logo branco (fundo escuro):
  {{LOGO_DARK_PATH}}

Logo escuro (fundo claro):
  {{LOGO_LIGHT_PATH}}
```

## Regras de Print (Chromium)

1. **background-clip: text** = PROIBIDO. Renderiza como retângulos sólidos. Use `color` direto.
2. **radial-gradient com transparent em elementos grandes** = PROIBIDO. Renderiza como blocos. Só usar para dot patterns com opacidade < 0.05.
3. **cover-glow divs** = NÃO USAR. Aqueles divs com radial-gradient para efeito de glow NÃO funcionam em print. Remova-os.
4. **SVG inline** = NÃO USAR. Sempre use `<img src="...svg">` para logos.
5. **file:// protocol** = NÃO FUNCIONA no Playwright. Sempre use HTTP server.
6. **print-color-adjust: exact** = OBRIGATÓRIO no body.
7. **@page { size: A4 portrait; margin: 0; }** = OBRIGATÓRIO.

## CSS Completo

Copie este CSS inteiro para o `<style>` de cada proposta. Adapte apenas as classes específicas do conteúdo se necessário.

```css
@font-face {
  font-family: '{{FONT_HEADLINE_NAME}}';
  src: url('{{FONT_HEADLINE_PATH_WOFF2}}') format('woff2'),
       url('{{FONT_HEADLINE_PATH_WOFF}}') format('woff');
  font-weight: normal; font-style: normal; font-display: swap;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --dark: {{COR_PRIMARIA}}; --green: {{COR_DESTAQUE}}; --green-bright: {{COR_DESTAQUE_BRIGHT}};
  --lime: {{COR_LIME}}; --light: {{COR_FUNDO_CLARO}}; --gray: #8a9199;
  --card-bg: #FFFFFF; --text: #1a1a2e; --text-muted: #555;
}

body {
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--dark); color: var(--light);
  font-size: 11pt; line-height: 1.6;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}

@page { size: A4 portrait; margin: 0; }

.page {
  width: 210mm; height: 297mm; margin: 0 auto;
  position: relative; overflow: hidden;
  page-break-after: always; page-break-inside: avoid;
}
.page:last-child { page-break-after: auto; }

/* COVER */
.cover {
  display: flex; flex-direction: column; justify-content: center;
  align-items: center; text-align: center;
  padding: 60px 50px; height: 297mm; background: var(--dark); position: relative;
}
.cover-pattern {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(circle, rgba(43,194,14,0.05) 1.2px, transparent 1.2px);
  background-size: 28px 28px; pointer-events: none; z-index: 0;
}
.cover-line-top {
  position: absolute; top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, var(--green), var(--lime), var(--green)); z-index: 1;
}
.cover > * { z-index: 1; position: relative; }
.cover .logo-cover { width: 260px; margin-bottom: 50px; }
.cover .green-line {
  width: 80px; height: 3px;
  background: linear-gradient(90deg, var(--green), var(--lime));
  margin: 0 auto 36px; border-radius: 2px;
}
.cover h1 {
  font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 30pt; font-weight: normal;
  letter-spacing: 3px; text-transform: uppercase; color: var(--light);
  line-height: 1.3; margin-bottom: 16px;
}
.cover h1 span { display: block; color: var(--lime); }
.cover .subtitle { font-size: 14pt; color: var(--gray); margin-bottom: 70px; letter-spacing: 1px; }
.cover .meta { text-align: center; }
.cover .meta .label { font-size: 9pt; color: var(--gray); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px; }
.cover .meta .value { font-size: 14pt; color: var(--light); font-weight: 500; margin-bottom: 24px; }
.cover .meta .date { font-size: 10pt; color: var(--gray); margin-top: 8px; }
.cover-footer {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 20px 50px; display: flex; justify-content: center; align-items: center; z-index: 1;
}
.cover-footer .footer-text { font-size: 8pt; color: #3a4550; }

/* CONTENT PAGES */
.content-page {
  padding: 32px 46px 56px; background: var(--light);
  color: var(--dark); height: 297mm; position: relative; overflow: hidden;
}
.page-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 24px; padding-bottom: 10px; border-bottom: 2px solid #e0e0e0;
}
.page-header .logo-header { height: 38px; }
.page-header .page-label { font-size: 8pt; color: var(--gray); text-transform: uppercase; letter-spacing: 2px; }

.section-number {
  font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 40pt;
  color: var(--green); line-height: 1; margin-bottom: 0; display: block;
}
.section-title {
  font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 18pt; color: var(--dark);
  text-transform: uppercase; letter-spacing: 2px; margin-bottom: 16px; line-height: 1.3;
}
.content-page p { margin-bottom: 10px; line-height: 1.65; color: var(--text); font-size: 11pt; }
.highlight-text { font-size: 12pt; color: var(--dark); font-weight: 600; line-height: 1.6; margin-bottom: 14px; }

/* PAGE FOOTER */
.page-footer {
  position: absolute; bottom: 0; left: 0; right: 0; padding: 12px 46px;
  display: flex; justify-content: space-between; align-items: center;
  border-top: 2px solid #e0e0e0; background: var(--light);
}
.page-footer .footer-logo { height: 24px; opacity: 0.5; }
.page-footer .footer-text { font-size: 7.5pt; color: var(--gray); }

/* STATS BAR */
.stats-bar { display: flex; margin-top: 36px; background: var(--card-bg); border-radius: 14px; border: 1px solid #e0e0e0; overflow: hidden; }
.stat-item { flex: 1; text-align: center; padding: 22px 16px; border-right: 1px solid #e0e0e0; }
.stat-item:last-child { border-right: none; }
.stat-value { font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 20pt; color: var(--green); display: block; margin-bottom: 4px; }
.stat-label { font-size: 8.5pt; color: var(--gray); text-transform: uppercase; letter-spacing: 1px; }

/* CARDS (para items do serviço) */
.ia-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; }
.ia-card { background: var(--card-bg); border: 1px solid #e0e0e0; border-radius: 12px; padding: 16px 16px 14px; display: flex; gap: 14px; align-items: flex-start; }
.ia-badge { width: 38px; height: 38px; min-width: 38px; background: linear-gradient(135deg, var(--green), var(--lime)); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 10pt; color: var(--dark); font-weight: 700; }
.ia-content h4 { font-size: 10pt; font-weight: 700; color: var(--dark); margin-bottom: 3px; text-transform: uppercase; letter-spacing: 0.5px; }
.ia-content p { font-size: 9pt !important; color: var(--text-muted) !important; margin: 0 !important; line-height: 1.45 !important; }
.ia-card-full { grid-column: 1 / -1; }

/* PHASE CARDS */
.phase-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 14px 0; }
.phase-card { background: var(--card-bg); border: 1px solid #e0e0e0; border-radius: 12px; padding: 18px; position: relative; overflow: hidden; }
.phase-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--green), var(--lime)); }
.phase-card .phase-num { font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 12pt; color: var(--green); display: block; margin-bottom: 4px; }
.phase-card h4 { font-size: 11pt; font-weight: 700; color: var(--dark); margin-bottom: 6px; }
.phase-card p { font-size: 9.5pt !important; color: var(--text-muted) !important; margin: 0 !important; line-height: 1.5 !important; }
.phase-card-full { grid-column: 1 / -1; }

/* PIPELINE */
.pipeline-section { margin-top: 18px; }
.pipeline-label { font-size: 9.5pt; color: var(--gray); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
.pipeline-row { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 8px; }
.pipeline-badge { font-size: 8pt; padding: 6px 12px; border-radius: 20px; font-weight: 600; letter-spacing: 0.3px; white-space: nowrap; }
.badge-dark { background: var(--dark); color: var(--light); }
.badge-green { background: var(--green); color: var(--dark); font-weight: 700; }
.badge-lime { background: linear-gradient(135deg, #0a2010, #0d3015); color: var(--lime); }
.pipeline-arrow { color: var(--green); font-size: 11pt; font-weight: 700; }

/* PIPELINE LEGEND */
.pipeline-legend { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 12px; }
.legend-item { display: flex; gap: 10px; align-items: flex-start; padding: 8px 10px; background: var(--card-bg); border-radius: 8px; border: 1px solid #e8e8e8; }
.legend-badge { font-size: 7pt; padding: 3px 8px; border-radius: 12px; font-weight: 700; white-space: nowrap; margin-top: 1px; min-width: fit-content; }
.legend-text { font-size: 8.5pt; color: var(--text-muted); line-height: 1.4; }

/* TOOL CARDS */
.tool-card { background: var(--card-bg); border: 1px solid #e0e0e0; border-radius: 12px; padding: 18px 20px; margin-bottom: 12px; border-left: 4px solid var(--green); }
.tool-card h4 { font-size: 11pt; font-weight: 700; color: var(--dark); margin-bottom: 6px; }
.tool-card p { font-size: 9.5pt !important; color: var(--text-muted) !important; margin: 0 !important; line-height: 1.55 !important; }
.tool-options { display: flex; gap: 10px; margin-top: 10px; }
.tool-option { background: var(--light); border: 1px solid #ddd; border-radius: 8px; padding: 8px 16px; text-align: center; flex: 1; font-size: 9.5pt; font-weight: 600; color: var(--dark); }
.tool-rec { font-size: 8.5pt; color: var(--gray); margin-top: 10px; font-style: italic; padding-left: 2px; }

/* COMPARISON TABLE */
.comparison-table { width: 100%; border-collapse: separate; border-spacing: 0; border-radius: 12px; overflow: hidden; margin-top: 14px; font-size: 9.5pt; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.comparison-table thead th { background: var(--dark); color: var(--light); padding: 12px 14px; text-align: left; font-weight: 600; font-size: 9.5pt; }
.comparison-table thead th:last-child { background: linear-gradient(135deg, #0a2010, #0d3015); color: var(--lime); }
.comparison-table tbody td { padding: 10px 14px; border-bottom: 1px solid #eee; color: #333; }
.comparison-table tbody tr:nth-child(even) { background: #f8f9fa; }
.comparison-table tbody tr:last-child td { border-bottom: none; }
.comparison-table tbody td:first-child { font-weight: 600; color: var(--dark); }
.comparison-table tbody td:last-child { color: #0a6b00; font-weight: 500; }

/* ROI */
.roi-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 16px; }
.roi-box { background: linear-gradient(135deg, #071a0a, #0d2810); border-radius: 12px; padding: 20px; border: 1px solid rgba(43,194,14,0.2); }
.roi-label { font-size: 8.5pt; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(255,255,255,0.5); margin-bottom: 4px; font-weight: 600; }
.roi-value { font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 22pt; color: var(--lime); line-height: 1.2; margin-bottom: 4px; }
.roi-detail { font-size: 8.5pt; color: rgba(255,255,255,0.5); }
.total-box { background: var(--card-bg); border-radius: 12px; padding: 18px 20px; border: 2px solid var(--green); margin-top: 14px; }
.total-label { font-size: 8.5pt; text-transform: uppercase; letter-spacing: 1.5px; color: var(--gray); margin-bottom: 4px; font-weight: 600; }
.total-value { font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 16pt; color: var(--dark); line-height: 1.2; }
.total-detail { font-size: 8.5pt; color: var(--gray); margin-top: 2px; }

/* INVESTMENT */
.investment-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px; }
.investment-card { background: var(--card-bg); border-radius: 14px; padding: 22px 20px; border: 1px solid #e0e0e0; position: relative; overflow: hidden; }
.investment-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--green), var(--lime)); }
.inv-label { font-size: 8.5pt; text-transform: uppercase; letter-spacing: 2px; color: var(--gray); margin-bottom: 4px; font-weight: 600; }
.inv-price { font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 24pt; color: var(--dark); margin-bottom: 2px; line-height: 1.2; }
.inv-period { font-size: 9pt; color: var(--gray); margin-bottom: 14px; }
.investment-card ul { list-style: none; padding: 0; }
.investment-card ul li { font-size: 9pt; color: #444; padding: 4px 0 4px 18px; position: relative; line-height: 1.5; }
.investment-card ul li::before { content: ''; position: absolute; left: 0; top: 10px; width: 8px; height: 8px; border-radius: 50%; background: linear-gradient(135deg, var(--green), var(--lime)); }

/* COSTS */
.costs-box { background: var(--card-bg); border-radius: 12px; border: 1px solid #e0e0e0; padding: 8px 20px; }
.cost-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; }
.cost-item:last-child { border-bottom: none; }
.cost-item .cost-name { font-size: 10pt; color: var(--dark); font-weight: 500; }
.cost-item .cost-value { font-size: 10pt; color: var(--gray); font-weight: 500; }

/* PAYMENT */
.payment-row { display: flex; gap: 12px; margin-top: 12px; }
.payment-badge { background: var(--card-bg); border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px 20px; font-size: 10pt; font-weight: 600; color: var(--dark); }
.payment-note { font-size: 8.5pt; color: var(--gray); margin-top: 8px; font-style: italic; }

/* NOTES */
.note-item { margin-bottom: 12px; padding: 14px 16px; background: var(--card-bg); border-radius: 10px; border: 1px solid #e0e0e0; border-left: 4px solid var(--green); }
.note-item p { font-size: 9.5pt !important; color: #444 !important; margin: 0 !important; line-height: 1.55 !important; }

/* INFO BADGES */
.info-row { display: flex; gap: 14px; margin-top: 16px; }
.info-badge { flex: 1; background: var(--card-bg); border-radius: 10px; border: 1px solid #e0e0e0; padding: 14px 16px; text-align: center; }
.info-badge .info-label { font-size: 8pt; text-transform: uppercase; letter-spacing: 1.5px; color: var(--gray); font-weight: 600; margin-bottom: 4px; }
.info-badge .info-value { font-size: 10.5pt; color: var(--dark); font-weight: 600; }

/* CLOSING PAGE */
.closing-page {
  padding: 50px; background: var(--dark); color: var(--light);
  height: 297mm; position: relative; overflow: hidden;
  display: flex; flex-direction: column; justify-content: center;
}
.closing-page .cover-pattern { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: radial-gradient(circle, rgba(43,194,14,0.04) 1.2px, transparent 1.2px); background-size: 28px 28px; pointer-events: none; z-index: 0; }
.closing-page > * { z-index: 1; position: relative; }

.step-grid { margin: 24px 0; }
.step-item { display: flex; gap: 16px; align-items: flex-start; margin-bottom: 16px; }
.step-number { width: 40px; height: 40px; min-width: 40px; background: linear-gradient(135deg, var(--green), var(--lime)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: '{{FONT_HEADLINE_NAME}}', 'Inter', sans-serif; font-size: 13pt; color: var(--dark); font-weight: 700; }
.step-content h4 { font-size: 11pt; font-weight: 700; color: var(--light); margin-bottom: 2px; }
.step-content p { font-size: 9.5pt; color: rgba(255,255,255,0.5); line-height: 1.5; }

.contact-section { margin-top: 40px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.1); text-align: center; }
.contact-section .contact-label { font-size: 8.5pt; text-transform: uppercase; letter-spacing: 2px; color: rgba(255,255,255,0.4); margin-bottom: 12px; }
.contact-section .contact-value { font-size: 12pt; color: var(--light); margin-bottom: 6px; }
.validity-note { margin-top: 30px; text-align: center; font-size: 9pt; color: rgba(255,255,255,0.35); }
```
