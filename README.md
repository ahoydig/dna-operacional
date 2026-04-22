# DNA Operacional 🧬

**O sistema operacional da Ahoy Digital — do setup ao lançamento.**

20 skills Claude Code pra criador, agência, inteligência competitiva e **conselho de negócio** em BR. Inclui o coach **Hormozi em PT-BR** (Grand Slam Offer, Core Four, 3-Stage Money Model, 6M Diagnostic). Instala em 2 comandos, funciona em qualquer projeto.

## 🚀 Instalação

```
/plugin marketplace add ahoydig/dna-operacional
/plugin install dna-operacional
```

Pronto. Digita `/dna` pra ver tudo que dá pra fazer.

## O que tu ganha (20 skills)

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

### 🤖 Meta & Integrações

| Skill | O que faz |
|---|---|
| `/auto-melhoria` | Detecta padrões + propõe edits ao CLAUDE.md |
| `/dna-melhoria` | Auto-refino das skills do plugin (mantenedor) |
| `/dna-meta-ads` | Ponte com plugin meta-ads-pro (se instalado) |
| `/dna` | Menu central + jornadas |

---

## 🗄️ Storage Layer

Plugin abstrai persistência — tu escolhe onde guardar os dados das skills:

| Backend | Pra quem | Setup |
|---|---|---|
| **Supabase** | Power user / agência / escala | Médio (criar projeto + rodar migration) |
| **Google Sheets** | Maioria dos casos | Fácil (copiar planilha + colar ID) |
| **Markdown local** | Iniciante / pessoal | Trivial (`mkdir data/`) |

Sem lock-in. Trocar backend = passar pela skill `/dna migrar-storage` (v0.2+) ou migração manual.

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
| Modal | Whisper transcrição (`/analisar-video`) | $30/mês crédito |
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
