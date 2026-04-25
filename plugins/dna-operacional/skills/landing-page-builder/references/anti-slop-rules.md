# Anti-Slop Rules
### Padroes que fazem design parecer gerado por IA

Baseado em analise de 19 samples gerados por IA (unslop).

---

## Backgrounds proibidos

- Cluster off-white quente: `#f5f5f0`, `#f5f3f0`, `#f6f3ee`, `#faf9f7`, `#f8f7f5`, `#f8f7f6`, `#eae7e1` e qualquer variacao nessa faixa
- Near-black como unica alternativa: `#0b0f1a`, `#0B0D0F`, `#0f1117`, `#0f0f0f`
- Background nao e escolha binaria entre "cream quente" e "near-black"

**Em vez disso:** Use branco puro, cinzas frios, ou crie contraste entre secoes (dark hero + light content). Se precisar de off-white, va pro frio (cinza azulado).

## Fontes proibidas como default

- Inter como body font
- DM Sans como body font
- Poppins, Roboto, Montserrat, Open Sans
- Serif so pra heading + Inter/DM Sans body (combo overused)
- Especificamente: Playfair Display, Fraunces, Instrument Serif ou DM Serif Display como heading accent sobre Inter/DM Sans body

**Em vez disso:** Fontes premium (Envato Elements), ou Google Fonts menos usadas (Sora, Geist, Outfit, Figtree). Pra terminal/code: Bergen Mono, Geist Mono, IBM Plex Mono.

## Cores accent proibidas como default

- Cluster burnt orange/terracotta: qualquer hex no hue 10-20 (laranja-vermelho), saturacao 50-80%, lightness 35-50%
- Especificamente: `#c0522e`, `#c4410a`, `#c8553d`, `#c25b3f`, `#c0392b`, `#B8532E`, `#e85d3a`, `#C65D3E`

**Excecao:** Se terracotta/coral faz parte da identidade visual da marca, pode usar. A regra e nao defaultar pra terracotta quando nao tem direcao de cor.

## Texto proibido

- Near-black quente: `#1a1a1a`, `#1A1A18`, `#1A1714`, `#23211e`, `#2d2d2d`
- Muted gray quente: `#6b6b6b`, `#6b6560`, `#7a746b`
- Nao fazer todos os neutrals warm-toned

**Em vez disso:** `#18181b` (zinc), `#1e1e2e` (com toque azul), `#5c5f66` (muted frio).

## Bordas e cards proibidos

- Cluster borda warm gray: `#e8e8e3`, `#e5e5e0`, `#e5e0db`, `#E8E6E0`, `#e0ddd8`
- Receita de card default: `1px solid [warm-gray]` + `border-radius: 12-14px` + sem box-shadow + fundo branco
- Cards todos identicos na mesma pagina

**Em vez disso:** Variar entre cards: uns com fundo solido, outros sem fundo, variar radius e shadow. Usar sombras reais quando tiver elevacao.

## Tipografia proibida

- `letter-spacing: -0.03em` em todos os headings
- `font-weight: 800` como peso padrao de heading
- Label universal: `11-12px` + `font-weight: 600` + `uppercase` + `letter-spacing: 0.06-0.08em` em TODOS os labels

**Em vez disso:** Variar tracking por contexto. Usar peso normal quando a fonte tem carater proprio. Nao fazer todo label em uppercase tracked.

## Layouts proibidos

- 4 KPI cards no topo (label + numero grande + delta colorido)
- Header "titulo esquerda, meta direita" (`justify-content: space-between`)
- Grid 2 colunas 50/50 (`1fr 1fr; gap: 16px`)
- Sequencia rigida: header → KPI → graficos → tabela
- Formula "tool page": header → form 2 colunas → cards resultado → tabela

## Spacing proibido

- `gap: 16px` como gap universal
- `padding: 32px` como padding universal de container
- `padding: 24px` como padding universal de card
- Mesmo valor de spacing pra tudo

**Em vez disso:** Variar o ritmo. Gaps menores pra agrupar itens relacionados, gaps maiores pra separar secoes.

## Status colors proibidas

- Verde + vermelho como unico par semantico
- Pattern `↑ +12.4%` / `↓ -2.3%` com texto colorido em pill
- Pill badges como unico indicador de status

## Estrutura proibida

- Paginas sem hover states, sem transitions, sem animacoes
- Paginas sem media queries ou responsividade
- Paginas sem footer
- Grid puramente simetrico sem variacao de largura de coluna

---

## Mantra

Se voce esta prestes a usar background cream quente, fonte Inter, accent terracotta, cards com borda fina sem sombra, labels uppercase ou 4 KPI cards no topo — pare. Faca diferente.
