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

## ⚠️ Status atual: v0.1.0-alpha.6

Esta versão entrega **10 skills** (3 de scaffolding + 7 migradas de globais). Faltam 4 skills (`humanizer`, `carrossel-instagram`, `analisar-video`, `roteiro-viral`) que chegam na **v0.1.0 final** (Plan 5).

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

### v0.1.0-alpha.6 (atual) — 10 skills

| Skill | O que faz |
|---|---|
| `/dna` | Menu central do plugin + jornadas |
| `/voz` | Mantém voz escrita do projeto (7 modos) |
| `/dna-melhoria` | Auto-refino das skills do plugin (mantenedores) |
| `/setup-projeto` | Configura projeto com CLAUDE.md rico; delega §13 pra `/voz criar` |
| `/pesquisa-diaria` | Radar diário BR → alimenta `content_pipeline` |
| `/pesquisa-concorrentes` | Mapeia concorrentes IG → `competitors` + `competitor_posts` |
| `/raio-x-ads-concorrentes` | Briefing de ads a partir de `ad_library` + `competitors` |
| `/ideias-conteudo` | Multiplica ideias do pipeline em 5 vídeos |
| `/analista-conteudo` | Análise SQL 14 seções (Supabase-only) |
| `/auto-melhoria` | Orquestradora metacognitiva; delega padrões de voz pra `/voz` |

### v0.1.0 (próxima) — 4 skills restantes

`humanizer`, `carrossel-instagram`, `analisar-video`, `roteiro-viral` — Plan 5. Ver [ROADMAP.md](plugins/dna-operacional/docs/ROADMAP.md).

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
