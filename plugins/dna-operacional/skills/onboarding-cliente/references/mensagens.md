# Templates de mensagens — onboarding-cliente

Mensagens disparadas pela Bruna via uazapi. Placeholders entre `{{...}}`.

## boas-vindas

Disparada na Etapa 5 logo após criar o grupo.

```
Oi {{cliente_primeiro_nome}}! 🌊

A Ahoy tá oficialmente onboard. Aqui é a Bruna — vou ser teu ponto de contato pro dia-a-dia.

Pra a gente começar com tudo, fiz 3 coisas:

📋 Briefing rápido (~15 min):
{{form_url}}

📁 Tua pasta no Drive (já tem acesso):
{{drive_url}}

Qualquer foto, áudio, PDF, contrato anterior, vídeo de referência — joga em "99 — Anexos do cliente" lá no Drive.

Assim que preencher o briefing, a equipe começa a montar a estratégia. Qualquer dúvida, é por aqui mesmo.

Bem-vindo(a)! 💙
```

## briefing-pendente (futuro v0.5)

Se 48h depois do onboarding o briefing não foi preenchido, hook futuro dispara:

```
Oi {{cliente_primeiro_nome}}, tudo certo?

Lembrete amigável — o briefing tá esperando você:
{{form_url}}

Demora ~15 min. Se tiver alguma pergunta confusa, manda aqui que a gente reformula.
```

## briefing-recebido (futuro v0.5)

Quando hook detecta nova resposta no Form:

```
Recebido o briefing! 🎯

A equipe começa a digerir agora. Em até 48h volto com o próximo passo.
```

## Render rules

1. `{{cliente_primeiro_nome}}`: `cliente_nome.split()[0]` capitalizado.
2. `{{form_url}}` e `{{drive_url}}`: URLs completas, sem encurtador (cliente vê o domínio Google = confiança).
3. Substituições antes de mandar via `/send/text`. Se algum placeholder ficar sem substituir (`{{...}}` no output final), abortar e logar erro.

## Voz

Mensagens seguem voz dinâmica do projeto Ahoy (PT-BR direta, sem hedging, com 1-2 emojis estratégicos). Skill **não** invoca `/humanizer` — mensagens são fixas e revisadas. Se quiser editar voz, edita este arquivo direto e bumpa versão.
