# DNA Operacional 🧬

**O sistema operacional da Ahoy Digital — do setup ao lançamento.**

24 skills Claude Code pra criador, agência, inteligência competitiva, **conselho de negócio** e **entrega de cliente end-to-end** (orçamento → contrato → apresentação → landing page) em BR. Inclui o coach **Hormozi em PT-BR** (Grand Slam Offer, Core Four, 3-Stage Money Model, 6M Diagnostic). Instala em 2 comandos, funciona em qualquer projeto.

## 🚀 Instalação

```
/plugin marketplace add ahoydig/dna-operacional
/plugin install dna-operacional
```

Pronto. Digita `/dna` pra ver tudo que dá pra fazer.

## O que tu ganha (24 skills)

### 🎯 Setup & Conteúdo

| Skill | O que faz |
|---|---|
| `/setup-projeto` | Configura qualquer projeto (teu ou cliente) em 17 seções |
| `/voz` | Cria/evolui/versiona a voz escrita do projeto |
| `/humanizer` | Remove cara de IA + aplica voz do projeto |
| `/pesquisa-diaria` | Radar matinal BR (X, Reddit, portais, GitHub) |
| `/pesquisa-concorrentes` | Mapeia concorrentes Instagram |
| `/raio-x-ads-concorrentes` | Briefing de ads competidores |
| `/ideias-conteudo` | 10 frameworks de hook + multiplica ideias |
| `/analisar-video` | Eng. reversa de Reels/TikTok → adaptive_models |
| `/roteiro-viral` | Roteiros baseados em adaptive_models |
| `/carrossel-instagram` | Carrosséis Instagram via Playwright |
| `/analista-conteudo` | Análise SQL do teu feed (KPIs BR) |

### 🧠 Conselheiro Hormozi (PT-BR)

| Skill | O que faz |
|---|---|
| `/hormozi` | Menu + chat livre na voz do coach |
| `/hormozi-diagnostico` | 6M Diagnostic → identifica O constraint #1 |
| `/hormozi-oferta` | Grand Slam Offer builder (Equação de Valor + bonus stack + garantia) |
| `/hormozi-leads` | Core Four + Regra dos 100 + Mais/Melhor/Novo |
| `/hormozi-money-model` | Audita 3 estágios (Atração/Upsell/Continuity) + cash 30d |
| `/hormozi-raio-x` | Scan completo do negócio end-to-end |

### 🧠 Client Delivery

Entrega end-to-end pra cliente de agência/consultoria. Fecha o loop: do orçamento à landing no ar.

| Skill | O que faz |
|---|---|
| `/orcamento` | Proposta comercial PDF (wrapper de `proposta` com contexto DNA do projeto) |
| `/apresentacao` | Deck HTML+CSS+JS Vanilla+GSAP (NÃO pptx) — animações cinematográficas, fora-da-caixa |
| `/landing-page` | LP alta conversão (wrapper `landing-page-builder` + `taste-skill` + `ui-ux-pro-max` + opcional Impeccable polish) |
| `/contrato` | Edita modelo `.docx`/`.pdf` substituindo placeholders com dados do cliente + projeto |

### 🤖 Meta & Integrações

| Skill | O que faz |
|---|---|
| `/auto-melhoria` | Detecta padrões + propõe edits ao CLAUDE.md |
| `/dna-melhoria` | Auto-refino das skills do plugin (mantenedor) |
| `/dna-meta-ads` | Ponte com plugin meta-ads-pro (se instalado) |
| `/dna` | Menu central + jornadas |

---

## ⚡ Modo Lowcost

Flag em `CLAUDE.md` que economiza **30–80% tokens** reduzindo escopo das skills (menos perguntas, menos frameworks, menos saídas) sem perder o essencial.

```
/dna modo            → mostra modo atual (full | lowcost)
/dna modo lowcost    → ativa modo econômico em todas as skills
/dna modo full       → volta pro padrão completo
```

Quando ativado (`dna_mode: lowcost` em `CLAUDE.md`), 10 skills respeitam a flag:

| Skill | Redução em lowcost |
|---|---|
| `/setup-projeto` | 17 seções → **fast mode** (8 perguntas essenciais em ~3 min) |
| `/pesquisa-diaria` | 6 fontes → **3 fontes core** (X + Reddit + portais BR) |
| `/pesquisa-concorrentes` | 10 concorrentes → **5 concorrentes** |
| `/raio-x-ads-concorrentes` | Briefing completo → **top 3 anúncios + angle principal** |
| `/ideias-conteudo` | 10 frameworks → **3 hooks high-performers** |
| `/analisar-video` | 6 camadas → **roteiro + hook + estrutura** |
| `/roteiro-viral` | 3 variantes → **1 variante polida** |
| `/carrossel-instagram` | 10 slides + moodboard → **6 slides + template direto** |
| `/analista-conteudo` | 14 seções SQL → **4 KPIs core** |
| `/hormozi-diagnostico` | 6M completo → **3 Ms críticos (Money/Market/Model)** |

Heurística completa em [`lib/mode/low-cost-heuristics.md`](plugins/dna-operacional/lib/mode/low-cost-heuristics.md).

---

## 🗄️ Storage Layer

Plugin abstrai persistência — tu escolhe onde guardar os dados das skills:

| Backend | Pra quem | Setup |
|---|---|---|
| **CSV local** (default) | **Todo mundo começa aqui** — marketeiro, empresário, criador | Trivial (zero config — skills criam `data/*.csv` automático) |
| **Google Sheets** | Quem quer visualizar em planilha compartilhada | Fácil (copiar planilha + colar ID) |
| **Supabase** | Power user only — agência/escala com SQL complexo (`/analista-conteudo`) | Médio (criar projeto + rodar migration) |

Sem lock-in. Trocar backend = passar pela skill `/dna migrar-storage` (v0.3+) ou migração manual.

Detalhes completos em [`lib/storage/`](plugins/dna-operacional/lib/storage/) e [`templates/`](plugins/dna-operacional/templates/).

---

## 🎙 Voz Dinâmica

Plugin tem skill `/voz` que mantém a voz escrita do teu projeto. Cada projeto tem sua voz em `reference/voz-<handle>.md`.

Modos:
```
/voz                       → status da voz atual
/voz criar                 → entrevista guiada (cria v1)
/voz mostrar               → exibe voz completa
/voz evoluir <input>       → URL/arquivo/texto pra adicionar padrões
/voz versoes               → lista versões + rollback
/voz silenciar | ativar    → controla auto-observação
```

**Auto-observação:** quando você usa o plugin, ele detecta padrões de voz e sugere evoluções (com confirmação). Pra desligar: `/voz silenciar`.

Detalhes em [`lib/voz/SCHEMA.md`](plugins/dna-operacional/lib/voz/SCHEMA.md) e [`lib/voz/auto-observacao.md`](plugins/dna-operacional/lib/voz/auto-observacao.md).

---

## 📦 Skills bundled (a partir da v0.3.0)

Comandos como `/landing-page`, `/apresentacao`, `/orcamento` dependiam de skills externas que tinham que ser instaladas separadamente. **Agora vêm dentro do plugin** — instalou, funciona.

| Skill bundled | Onde mora | Usada por |
|---|---|---|
| `landing-page-builder` | `${CLAUDE_PLUGIN_ROOT}/skills/` | `/landing-page` |
| `taste-skill` | `${CLAUDE_PLUGIN_ROOT}/skills/` | `/landing-page`, `/apresentacao` |
| `ui-ux-pro-max` | `${CLAUDE_PLUGIN_ROOT}/skills/` | `/landing-page`, `/apresentacao` |
| `proposta` | `${CLAUDE_PLUGIN_ROOT}/skills/` | `/orcamento` |

Branding (paleta, fonte, logos, contato) é **configurável via placeholders** — cada user preenche os dele no `setup-projeto`. Defaults neutros caso não configure.

### Skill que NÃO vem bundled: `transcribe-audio` (Modal.com)

`/analisar-video` e qualquer transcrição de áudio precisam de GPU (Whisper). A solução é Modal.com (free tier de US$ 30/mês cobre ~300-600h de áudio). Como precisa de conta e CLI, é setup explícito:

1. Segue [`docs/SETUP-MODAL.md`](plugins/dna-operacional/docs/SETUP-MODAL.md) (~10 minutos)
2. Roda `/setup-transcribe-audio` no Claude Code — valida o setup e instala a skill local

A skill `impeccable` (polish opcional) também não vem bundled — é totalmente opcional, comandos seguem sem ela.

---

## 🔑 Antes de rodar: configure as APIs

Algumas skills precisam de chaves externas (Apify, Supabase, Modal). **Zero hardcoded — cada aluno configura a sua.**

Guia completo passo-a-passo:
```
cat ~/.claude/plugins/cache/dna-operacional-marketplace/dna-operacional/0.1.0/docs/APIS-EXTERNAS.md
```

Ou veja [`docs/APIS-EXTERNAS.md`](plugins/dna-operacional/docs/APIS-EXTERNAS.md) no repo.

**Resumo:**

| API | Pra quê | Free tier |
|---|---|---|
| Apify | Scraping (pesquisas, video download) | $5/mês de créditos |
| Supabase | SQL analytics (`/analista-conteudo`) + storage | 500MB DB grátis |
| Modal | Whisper transcrição (`/analisar-video`) — guia em [`docs/SETUP-MODAL.md`](plugins/dna-operacional/docs/SETUP-MODAL.md) + comando `/setup-transcribe-audio` | $30/mês crédito |
| Google Sheets | Storage backend alternativo | Grátis |

Cada skill faz pré-check no início — se falta config, mostra passo-a-passo pra fix.

---

## ⏰ Agendamento `/pesquisa-diaria`

3 opções (user escolhe no `APIS-EXTERNAS.md`):

- **`/schedule` Anthropic** — zero infra, paga tokens. Medido: ~$18-36/mês com Sonnet (estimativa teórica; ver `docs/SPIKE-TOKENS.md`)
- **GitHub Actions** — grátis em repo público
- **launchd (Mac)** — grátis, só com Mac ligado

---

## 🧬 DNA-Melhoria (mantenedores)

Skill `/dna-melhoria` faz auto-refino das próprias skills do plugin. Pra mantenedores (não pro aluno final).

```
/dna-melhoria              → análise dry-run (default)
/dna-melhoria --diff       → mostra diff completo (copia/cola manual)
```

A skill é **só dry-run + diff** (alinhado com Spec §3.1). `--apply` com confirmação 1-a-1 fica como follow-up futuro.

Heurísticas: descriptions de auto-discovery, argument-hints, próximos passos, tool calls visíveis, sanitização. Detalhes em [`commands/dna-melhoria.md`](plugins/dna-operacional/commands/dna-melhoria.md).

---

## Começa por aqui

```
/setup-projeto
```

Ele te entrevista, monta teu `CLAUDE.md`, define público-alvo e delega a voz pro `/voz`. A partir daí, cada skill te orienta pro próximo passo.

## Jornadas

- 🎬 **Criador** (8 skills) — setup → voz → pesquisa → ideias → análise → roteiro → publica → analisa
- 🎨 **Carrossel** (4 skills) — setup → voz → ideias → carrossel
- 🔬 **Inteligência Competitiva** (4 skills) — setup → concorrentes → (v0.2 ads) → raio-x
- 🧠 **Conselho de Negócio** (5 skills) — diagnóstico 6M → oferta → leads → money model → raio-x
- 📄 **Entrega de Cliente** (4 skills) — orcamento → contrato → apresentacao → landing-page
- 🤖 **Manutenção** (3 transversais) — auto-melhoria + voz auto-observa + dna-melhoria

Detalhes em `/dna jornadas`.

---

## 🛠️ Desenvolvimento local (pra contribuir)

```bash
git clone https://github.com/ahoydig/dna-operacional.git
cd ..
claude plugin marketplace add ./dna-operacional
/plugin install dna-operacional
```

Depois de editar arquivos:

```
/plugin marketplace update dna-operacional
```

---

## Links

- 📺 Curso Maestria IA Claude Code: [url quando lançar]
- 📸 Instagram: [@flavioahoy](https://instagram.com/flavioahoy)
- 🐛 Bugs/feedback: [issues](https://github.com/ahoydig/dna-operacional/issues)

## Licença

MIT. Use, forke, aprenda.

---

Feito com 🧬 por [@flavioahoy](https://instagram.com/flavioahoy). Pra alunos do curso Maestria IA.
