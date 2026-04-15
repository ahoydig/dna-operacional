<pre>
██████╗ ███╗   ██╗ █████╗      ██████╗ ██████╗ ███████╗
██╔══██╗████╗  ██║██╔══██╗    ██╔═══██╗██╔══██╗██╔════╝
██║  ██║██╔██╗ ██║███████║    ██║   ██║██████╔╝███████╗
██║  ██║██║╚██╗██║██╔══██║    ██║   ██║██╔═══╝ ╚════██║
██████╔╝██║ ╚████║██║  ██║    ╚██████╔╝██║     ███████║
╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝     ╚═════╝ ╚═╝     ╚══════╝

                 by @flavioahoy
</pre>

> **O sistema operacional da Ahoy Digital — do setup ao lançamento.**

🧬 **DNA Operacional** é um plugin do Claude Code com skills concatenadas pra:
- 🎬 Criar conteúdo (criador/infoprodutor)
- 🏢 Tocar uma agência (clientes de todo tipo)
- 🔬 Inteligência competitiva

---

## 🚀 Instalação (3 segundos)

No Claude Code, digite:

```
/plugin marketplace add ahoydig/dna-operacional
/plugin install dna-operacional
```

Pronto. Verifica com `/dna`.

---

## 🗄️ Storage Layer (v0.1.0-alpha.3)

Plugin abstrai persistência — tu escolhe onde guardar os dados das skills:

| Backend | Pra quem | Setup |
|---|---|---|
| **Supabase** | Power user / agência / escala | Médio (criar projeto + rodar migration) |
| **Google Sheets** | Maioria dos casos | Fácil (copiar planilha + colar ID) |
| **Markdown local** | Iniciante / pessoal | Trivial (`mkdir data/`) |

Sem lock-in. Trocar backend = passar pela skill `/dna migrar-storage` (v0.2+) ou migração manual.

Detalhes completos em [`lib/storage/`](plugins/dna-operacional/lib/storage/) e [`templates/`](plugins/dna-operacional/templates/).

---

## 🎙 Voz Dinâmica (v0.1.0-alpha.5)

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

## 🧬 DNA-Melhoria (v0.1.0-alpha.5, mantenedores)

Skill `/dna-melhoria` faz auto-refino das próprias skills do plugin. Pra mantenedores (não pro aluno final).

```
/dna-melhoria              → análise dry-run (default)
/dna-melhoria --diff       → mostra diff completo (copia/cola manual)
```

Em v0.1.0-alpha.5 a skill é **só dry-run + diff** (alinhado com Spec §3.1). `--apply` com confirmação 1-a-1 fica como follow-up futuro.

Heurísticas: descriptions de auto-discovery, argument-hints, próximos passos, tool calls visíveis, sanitização. Detalhes em [`commands/dna-melhoria.md`](plugins/dna-operacional/commands/dna-melhoria.md).

---

## ⚠️ Status atual: v0.1.0-alpha.7 (alpha completion)

Esta versão fecha as **14 skills planejadas pra v0.1.0** (3 de scaffolding + 11 migradas de globais). Plus 3 hooks reais de auto-observação (Sinais 1, 2, 3, 4) nas skills consumidoras (humanizer, ideias-conteudo, analisar-video).

Continua marcada como alpha porque ainda faltam Plan 6 (spike tokens `/schedule`) + Plan 7 (release v0.1.0 final sem `-alpha`).

Se você tá usando skills globais do criador, continue usando — o plugin **não** substitui as globais, ele adiciona uma cópia adaptada e sanitizada.

Veja [ROADMAP.md](plugins/dna-operacional/docs/ROADMAP.md) pra plano completo.

---

## 🎯 Começa por aqui

No Claude Code:

```
/dna                 # menu central
/dna jornadas        # 4 caminhos completos (criador, carrossel, IC, manutenção)
```

---

## 🗺️ Jornadas disponíveis

| Jornada | Skills | Pra quem |
|---|---|---|
| 🎬 Criador | 8 skills | Quem posta Reels/TikTok/Shorts e quer ciclo completo |
| 🎨 Carrossel | 4 skills | Quem quer carrossel Instagram rápido |
| 🔬 Inteligência Competitiva | 4 skills | Quem precisa mapear concorrência + ads |
| 🤖 Manutenção | 3 skills (transversais) | Evolui voz + skills automaticamente |

Ver [JORNADAS.md](plugins/dna-operacional/docs/JORNADAS.md) pra passo-a-passo.

---

## 📦 Skills incluídas

### v0.1.0-alpha.7 (atual) — 14 skills

| Skill | O que faz |
|---|---|
| `/dna` | Menu central do plugin + jornadas |
| `/voz` | Mantém voz escrita do projeto (7 modos) |
| `/dna-melhoria` | Auto-refino das skills do plugin (mantenedores) |
| `/setup-projeto` | Configura projeto com CLAUDE.md rico; delega §13 pra `/voz criar` |
| `/pesquisa-diaria` | Radar diário BR → alimenta `content_pipeline` |
| `/pesquisa-concorrentes` | Mapeia concorrentes IG → `competitors` + `competitor_posts` |
| `/raio-x-ads-concorrentes` | Briefing de ads a partir de `ad_library` + `competitors` |
| `/ideias-conteudo` | Multiplica ideias do pipeline em 5 vídeos — hook Sinal 2 (auto-obs) |
| `/analista-conteudo` | Análise SQL 14 seções (Supabase-only) |
| `/auto-melhoria` | Orquestradora metacognitiva; delega padrões de voz pra `/voz` |
| `/humanizer` | Remove vícios de IA + aplica voz dinâmica (`reference/voz-<handle>.md`) — hooks Sinais 1+3 |
| `/carrossel-instagram` | Gera carrosséis profissionais via Playwright (HTML→PNG) |
| `/analisar-video` | Engenharia reversa Reels/TikTok → `adaptive_models` — hook Sinal 4 |
| `/roteiro-viral` | Roteiros consumindo `adaptive_models` → `generated_scripts`; delega humanizer |

**Marco:** alpha.7 fecha as 14 skills planejadas pra v0.1.0. Falta Plan 6 (spike tokens `/schedule`) + Plan 7 (release v0.1.0 final). Ver [ROADMAP.md](plugins/dna-operacional/docs/ROADMAP.md).

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

## 🔗 Links

- **Curso Maestria IA:** [url quando lançar]
- **Instagram:** [@flavioahoy](https://instagram.com/flavioahoy)
- **Issues:** https://github.com/ahoydig/dna-operacional/issues

---

## 📄 Licença

MIT — veja [LICENSE](LICENSE).
