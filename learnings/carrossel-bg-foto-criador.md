# Carrossel: background da capa/CTA = foto do próprio criador

**O que aprendi:** O Flávio quer que o fundo da capa (e CTA) seja gerado a partir de uma foto DELE — não uma foto stock genérica. É o padrão que o @noevarner.ai usa (foto dele no Rio/praia, escurecida, atrás da headline).

**Por quê:** dá autenticidade e identidade pessoal ao carrossel; o criador aparece no próprio conteúdo. Foto stock genérica não tem o mesmo peso.

**Como aplicar (skill genérica):**
- Capa e CTA usam `.bg-photo` = foto do criador + `.bg-scrim` (overlay escuro rgba 0.55-0.72 / brightness 0.35-0.45) pra garantir legibilidade da headline branca por cima.
- A skill deve PEDIR/usar uma foto do usuário (ou já tê-la no projeto, ex: reference/foto-<handle>.jpg). Pode tratar/recortar/estilizar a foto via gerar-imagem se preciso.
- DYpVlG reaproveita 1 foto em 3 estados (nítida capa / blur itens / blur+escuro CTA) — economia de asset + coesão. [[carrossel-ativos-reais]]
