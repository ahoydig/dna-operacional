# Roadmap DNA Operacional

## ✅ v0.1.0 — RELEASE OFICIAL (2026-04-15)

14 skills entregues em 6 milestones alpha (alpha.1-8, 2026-04-14 a 2026-04-15):

- [x] Scaffolding + `/dna` (alpha)
- [x] Storage layer 3 adapters (alpha.3)
- [x] `/voz` + `/dna-melhoria` (alpha.5)
- [x] 7 skills migradas: setup-projeto, pesquisa-*, ideias-conteudo, analista-conteudo, auto-melhoria, raio-x (alpha.6)
- [x] 4 skills globais + 3 hooks auto-obs: humanizer, carrossel-instagram, analisar-video, roteiro-viral (alpha.7)
- [x] APIs externas + agendamento (alpha.8)
- [x] Polimento + release oficial (v0.1.0)

**14 skills disponíveis:** /dna, /voz, /humanizer, /dna-melhoria, /setup-projeto, /pesquisa-diaria, /pesquisa-concorrentes, /raio-x-ads-concorrentes, /ideias-conteudo, /analisar-video, /roteiro-viral, /carrossel-instagram, /analista-conteudo, /auto-melhoria.

## 🎯 v0.2.0 — Skills de Agência + Ads (próximo)

- [ ] `/onboarding-cliente` (workflow completo)
- [ ] `/pedido-anuncios`
- [ ] `/roteiro-anuncios` (UGC PAS framework)
- [ ] `/responder-leads` (UAZAPI WhatsApp)
- [ ] `/coletar-anuncios` (popula ad_library — desbloqueia raio-x)
- [ ] `/lista-alto-valor` (refatorada genérica)
- [ ] Família `/meta-ads-*` (7 skills: campanha, conjuntos, anuncios, publicos, insights, regras, setup)
- [ ] `/nomenclatura-utm` (helper de ads)
- [ ] `/switchy-links` (links rastreáveis)
- [ ] `/agendar-pesquisa` (orquestra /schedule)
- [ ] `/dna migrar-storage <backend>` (migração automática)

## 🎬 v0.3.0 — Ciclo de Conteúdo Completo

- [ ] `/roteirista-conteudo`
- [ ] `/analista-concorrentes`
- [ ] `/publicar-conteudo`
- [ ] `/reaproveitador`
- [ ] `/popular-my-content` (importa histórico Instagram)
- [ ] Adapter Notion como 4º backend de storage

## 🧰 v0.4.0 — Genéricas

- [ ] `/pesquisador`
- [ ] `/resumidor`
- [ ] `/gerador-imagens`

## 🚀 v1.0.0 — Produção

- Todas as 20+ skills estáveis
- Testes de integração automatizados
- CI com audit sanitização antes de cada tag
- Publicação oficial no marketplace Anthropic

## Débito técnico conhecido (follow-ups)

- Spike de tokens `/schedule` real (multi-run pra amostragem robusta) — SPIKE-TOKENS.md atual tem estimativa teórica
- Padronização de `references/*/` subdirs (precedente criado em carrossel-instagram Plan 5)
- Banner ASCII com handle do autor — mantido como assinatura
- Sinal 3 humanizer best-effort (sem hook formal de edições externas)
- Spec 2 §7.2 regex precisa `\b` em tokens curtos (learning Plans 2-3)
