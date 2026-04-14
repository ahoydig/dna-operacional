# Jornadas do DNA Operacional

Caminhos completos que encadeiam as skills pra entregar um resultado de ponta-a-ponta. Cada jornada resolve uma dor específica.

## 🎬 Jornada do Criador (8 skills)

**Dor que resolve:** "Eu quero gerar conteúdo recorrente sem ter que pensar do zero todo dia."

**Fluxo:**

```
setup-projeto → voz (criar) → pesquisa-diaria → ideias-conteudo →
analisar-video (vídeo de referência) → roteiro-viral →
(grava + publica) → analista-conteudo
```

**Skills envolvidas:** 8

### Passo-a-passo

1. **`/setup-projeto`** — entrevista 17 seções, gera `CLAUDE.md` + `reference/publico-alvo.md`.
2. **`/voz`** — cria `reference/voz-<handle>.md` (chamada pelo setup-projeto na seção 13).
3. **`/pesquisa-diaria`** — agendada (`/schedule 7:00 BRT /pesquisa-diaria`), popula `content_pipeline` com top 10 temas BR.
4. **`/ideias-conteudo`** — multiplica 1 ideia do pipeline em 5 variações (10 frameworks de hook).
5. **`/analisar-video`** — engenharia reversa de um vídeo referência, popula `adaptive_models`.
6. **`/roteiro-viral`** — gera roteiro baseado no `adaptive_model` escolhido.
7. **(off-Claude)** — grava, edita, publica.
8. **`/analista-conteudo`** — análise SQL do feed, identifica o que bombou.

**Output final:** conteúdo publicado + aprendizado pro próximo ciclo.

---

## 🎨 Jornada do Carrossel (4 skills)

**Dor que resolve:** "Preciso de carrossel Instagram bonito rapidão, com copy na minha voz."

**Fluxo:**

```
setup-projeto → voz → ideias-conteudo → carrossel-instagram
```

### Passo-a-passo

1. **`/setup-projeto`** (se ainda não configurou).
2. **`/voz`** (se ainda não tem voz).
3. **`/ideias-conteudo`** — gera hooks + estrutura do carrossel.
4. **`/carrossel-instagram`** — renderiza via Playwright, exporta .png.

**Output final:** pasta `carrossel-out/` com os slides prontos.

---

## 🔬 Jornada Inteligência Competitiva (4 skills)

**Dor que resolve:** "Preciso entender o que os concorrentes do meu nicho estão fazendo pra saber onde me posicionar."

**Fluxo:**

```
setup-projeto → pesquisa-concorrentes → (futuro: coletar-anuncios em v0.2) →
raio-x-ads-concorrentes
```

### Passo-a-passo

1. **`/setup-projeto`**.
2. **`/pesquisa-concorrentes`** — mapeia concorrentes IG, popula `competitors` e `competitor_posts`.
3. **(v0.2 — pendente)** `/coletar-anuncios` — popula `ad_library` via Apify.
4. **`/raio-x-ads-concorrentes`** — briefing estratégico 10 seções.

**⚠️ Bloqueio atual (v0.1.0):** passo 3 não existe ainda. `raio-x-ads-concorrentes` avisa "ad_library vazia, aguarde v0.2".

**Output final:** briefing `.md` com tese de posicionamento.

---

## 🤖 Jornada Manutenção (3 skills, transversal)

**Dor que resolve:** "Como meu sistema de skills evolui junto com meu estilo e com o mercado?"

**Fluxo:**

```
auto-melhoria (durante uso) → voz (auto-evoluir) → dna-melhoria (release prep)
```

### Quando cada uma ativa

- **`/auto-melhoria`** — detecta padrões **durante** outras skills (ex: user corrigiu output 3x da mesma forma). Propõe edits ao `CLAUDE.md` do projeto.
- **`/voz` (auto-observação)** — quando `auto-melhoria` detecta padrão de **voz** (expressão repetida, hook validado), delega pra `voz` propor evolução.
- **`/dna-melhoria`** — roda manualmente em release prep. Escaneia SKILL.md das skills do plugin, sugere refinos (descriptions, próximos passos, deps). **Sempre dry-run + diff. Nunca aplica direto.**

**Output final:** plugin + projeto do user continuamente afinados.

---

## Grafo visual completo

Ver Spec 2 §6 pra o grafo ASCII com todas as dependências.
