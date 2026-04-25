---
description: Gera landing page de alta conversão orquestrando landing-page-builder + taste-skill + ui-ux-pro-max + (se instalado) impeccable. Pré-preenche com voz + público do projeto DNA. Salva em data/clientes/<slug>/landing-pages/. Use quando digitar "/landing-page", "criar lp", "pagina de venda", "página de captura", "landing pra <cliente>".
argument-hint: "[objetivo: venda|captura|waitlist|evento]"
---

Usuário invocou `/landing-page $ARGUMENTS`.

Esse comando é um **wrapper orquestrador** — chama 3-4 skills globais em sequência e garante que o output tá coerente com o projeto DNA.

## Passo 1 — Ler contexto DNA

Ler silenciosamente:

| Arquivo | Uso |
|---------|-----|
| `CLAUDE.md` | Empresa, handle, oferta, voz em adjetivos |
| `reference/publico-alvo.md` | Dor do público (vira headline + copy), jargões permitidos/proibidos |
| `reference/voz-*.md` | Voz aplicada a TODA copy (hero, bullets, CTA, FAQ) |

Se faltar:
> "⚠ Sem contexto DNA, a copy vai ser genérica. Recomendo `/setup-projeto fast` antes (5 min)."

## Passo 2 — Briefing

Perguntar:

1. **Objetivo** — `venda`, `captura`, `waitlist`, `evento` (se veio em `$ARGUMENTS`, pular)
2. **CTA principal** — texto exato do botão (ex: "Quero minha vaga", "Agendar diagnóstico grátis")
3. **Oferta** em 1 frase (ex: "método de captação de pacientes com WhatsApp + IA por R$ 12.000")
4. **Principal dor do público** em 1 frase — se `reference/publico-alvo.md` existe, propor a dor dominante e validar
5. **Prova social disponível** — lista de 3+ elementos (depoimentos, logos de clientes, números, screenshots)
6. **Arquétipo visual** — `brutal` | `clean` | `editorial` | `clínico` | `cyberpunk` | `premium-escuro`
7. **URL de destino do CTA** — formulário? checkout? WhatsApp? Calendly?

## Passo 3 — Detectar skills disponíveis

Antes de orquestrar, verificar quais skills estão instaladas. **Resolução bundled-first** — o plugin já empacota as skills críticas; só faz fallback pra global se ausente:

```bash
# Bundled (dentro do próprio plugin) — caminho preferencial
LANDING_BUILDER=$(ls ${CLAUDE_PLUGIN_ROOT}/skills/landing-page-builder/SKILL.md 2>/dev/null && echo "bundled" \
  || ls ~/.claude/skills/landing-page-builder/SKILL.md 2>/dev/null && echo "global")
TASTE=$(ls ${CLAUDE_PLUGIN_ROOT}/skills/taste-skill/SKILL.md 2>/dev/null && echo "bundled" \
  || ls ~/.claude/skills/taste-skill/SKILL.md 2>/dev/null && echo "global")
UIUX=$(ls ${CLAUDE_PLUGIN_ROOT}/skills/ui-ux-pro-max/SKILL.md 2>/dev/null && echo "bundled" \
  || ls ~/.claude/skills/ui-ux-pro-max/SKILL.md 2>/dev/null && echo "global")
# Impeccable é opcional — só global (não vem bundled)
IMPECCABLE=$(ls ~/.claude/skills/impeccable/SKILL.md 2>/dev/null && echo "yes")
METODO_ZERO=$(ls ~/.claude/plugins/*/metodo-zero/ 2>/dev/null && echo "yes")
```

**Routing:**
- Se `METODO_ZERO` disponível E arquétipo = `premium-escuro`/`brutal` → **delegar inteiro pra `/metodo-zero:criar-pipeline`** (engine especializado). Depois só registrar no CSV.
- Caso contrário → seguir fluxo abaixo com `landing-page-builder` + skills de design.

> ⚠️ Se as skills bundled não forem encontradas (plugin instalado mal), reportar caminho esperado: `${CLAUDE_PLUGIN_ROOT}/skills/<nome>/SKILL.md`. Não bloquear se a global existir como fallback.

## Passo 4 — Direção visual (ui-ux-pro-max)

Invocar **Skill tool** `ui-ux-pro-max`:

```
Contexto:
- Objetivo: <objetivo>
- Arquétipo: <arquétipo>
- Público: <trecho de publico-alvo.md>
- Voz: <adjetivos>

Request:
- 3 paletas (background, text, primary, accent, success, danger)
- 3 font pairings (headline + body)
- Arquétipo visual dominante (brutal/clean/editorial/clínico/cyberpunk/premium-escuro)
- 3 hero layouts (split, stacked, asymmetric)
```

User escolhe 1 combinação. **Default:** paleta neutra escura + Inter/Space Grotesk + arquétipo clean se user não escolher.

## Passo 5 — Taste Layer

Invocar **Skill tool** `taste-skill`:

```
DESIGN_VARIANCE = 8
MOTION_INTENSITY = 5
VISUAL_DENSITY = 6

Request:
Dado objetivo "<objetivo>", propor estrutura de LP com seções obrigatórias + opcionais:

Sequência recomendada (venda direta):
1. Hero (oferta + CTA primário)
2. Dor (3 bullets curtos)
3. Solução (método/processo)
4. Prova social (depoimentos + logos)
5. Oferta detalhada (preço + bônus + garantia)
6. FAQ (5-7 perguntas)
7. CTA final

Sequência recomendada (captura):
1. Hero (promessa + campo e-mail)
2. Valor da isca (o que é, 3 bullets)
3. Prova social curta
4. CTA repetido

Sequência recomendada (waitlist):
1. Hero teaser (o que vem)
2. Urgência (lista fechando)
3. CTA captura

Sequência recomendada (evento):
1. Hero (data + local + tema)
2. Speakers
3. Agenda
4. Ingresso + CTA
```

## Passo 6 — Invocar landing-page-builder

**Skill tool** `landing-page-builder` com dados agregados:

```
briefing: {
  objetivo: "<objetivo>",
  oferta: "<oferta>",
  cta_texto: "<cta>",
  cta_destino: "<url>",
  dor_principal: "<dor>",
  prova_social: [<lista>],
  voz: "<adjetivos>",
  publico_alvo: "<trecho publico-alvo>"
}

direcao_visual: {
  paleta: {<tokens escolhidos>},
  fontes: {<pairing>},
  arquetipo: "<arquétipo>"
}

estrutura: [<seções do taste-skill>]
```

Skill gera:
- `index.html` (semantic, acessível, Lighthouse 90+)
- `style.css` (tokens + responsivo mobile-first)
- `script.js` (interações mínimas — scroll reveal, FAQ accordion, form validation)
- `assets/` (placeholders se user não forneceu)

## Passo 7 — (Opcional) Polish com `impeccable`

Se `~/.claude/skills/impeccable/SKILL.md` existe:

**Skill tool** `impeccable` passando path dos 3 arquivos. Skill faz:
- Auditoria de hierarquia visual
- Ajuste de contrastes (WCAG AA mínimo)
- Micro-interações refinadas
- Performance (lazy loading, preconnect, font-display)

Se `impeccable` não instalada: pular silenciosamente (não é bloqueador).

## Passo 8 — Salvar + registrar

### 8.1 Output dir

```bash
slug = lowercase(cliente || tema).replace(/[^a-z0-9]+/g, '-').slice(0, 40)
date = $(date +%Y-%m-%d)
out_dir = "data/clientes/${slug}/landing-pages/${date}"
mkdir -p "${out_dir}/assets"

# Mover arquivos gerados pras landing folder
mv <html_gerado> "${out_dir}/index.html"
mv <css_gerado>  "${out_dir}/style.css"
mv <js_gerado>   "${out_dir}/script.js"
```

### 8.2 Append em `data/landing_pages.csv`

Header:
```
id,objetivo,cliente,slug,out_dir,arquetipo,paleta,polish_impeccable,created_at
```

### 8.3 Preview local

```bash
# Porta livre
PORT=8787
for P in 8787 8788 8789; do
  if ! lsof -i :$P > /dev/null 2>&1; then PORT=$P; break; fi
done
cd "${out_dir}"
python3 -m http.server ${PORT} > /dev/null 2>&1 &
open "http://localhost:${PORT}"
```

## Passo 9 — Output pro usuário

```
╔══════════════════════════════════════════════════════════════════╗
║  🚀 Landing Page gerada                                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Cliente:       <cliente>                                        ║
║  Objetivo:      <objetivo>                                       ║
║  Arquétipo:     <arquétipo>                                      ║
║  Paleta:        <nome>                                           ║
║  Polish:        <sim/não (impeccable)>                           ║
║                                                                  ║
║  Output:        data/clientes/<slug>/landing-pages/<data>/       ║
║                 ├── index.html                                   ║
║                 ├── style.css                                    ║
║                 ├── script.js                                    ║
║                 └── assets/                                      ║
║                                                                  ║
║  Preview:       http://localhost:<porta>                         ║
║                                                                  ║
║  Deploy:        netlify deploy --prod --dir=.                    ║
║                 ou drag-drop a pasta em netlify.com/drop         ║
║                                                                  ║
║  Checklist antes de publicar:                                    ║
║    [ ] Trocar placeholders de imagens em assets/                 ║
║    [ ] Configurar pixel/GTM (roda /metodo-zero:configurar-tracking se quiser ajuda)  ║
║    [ ] Testar CTA no mobile                                      ║
║    [ ] Lighthouse audit (90+)                                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Erros comuns

| Situação | Ação |
|----------|------|
| `landing-page-builder` não instalado | Oferecer fallback pra `/metodo-zero:criar-pipeline` se disponível |
| `ui-ux-pro-max` não instalado | Fallback default (paleta neutra dark + Inter/Space Grotesk) |
| `impeccable` não instalado | Pular silenciosamente (não é obrigatório) |
| Sem contexto DNA | Avisar, seguir coletando tudo no briefing |
| Porta 8787-8789 ocupadas | Instruir preview manual |
