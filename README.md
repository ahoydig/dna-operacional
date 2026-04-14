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
/plugin marketplace add flavioahoy/dna-operacional
/plugin install dna-operacional
```

Pronto. Verifica com `/dna`.

---

## ⚠️ Status atual: v0.1.0-alpha (scaffolding)

Esta versão entrega **apenas** a estrutura do plugin + meta-skill `/dna`.

As 14 skills reais (`setup-projeto`, `pesquisa-diaria`, etc) chegam na **v0.1.0 final** (próxima sessão de migração).

Se você tá usando skills globais do Flávio, continue usando — o plugin **não** substitui as globais, ele adiciona uma cópia adaptada e sanitizada.

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

### v0.1.0-alpha (atual)

| Skill | O que faz |
|---|---|
| `/dna` | Menu central do plugin + jornadas |

### v0.1.0 (próxima)

14 skills completas. Ver [ROADMAP.md](plugins/dna-operacional/docs/ROADMAP.md).

---

## 🛠️ Desenvolvimento local (pra contribuir)

```bash
git clone https://github.com/flavioahoy/dna-operacional.git
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
- **Issues:** https://github.com/flavioahoy/dna-operacional/issues

---

## 📄 Licença

MIT — veja [LICENSE](LICENSE).
