# Google Form — Briefing de cliente

Spec do Form modelo que a skill `/onboarding` duplica pra cada cliente. Tem que existir 1 vez na conta `<gws-account>` e ter o `briefing_form_template_id` registrado no CLAUDE.md.

## Estrutura do Form

**Título:** `Briefing — {{cliente_nome}}` (skill substitui placeholder via gws-forms update)

**Descrição:**
> Esse briefing nos dá o contexto pra começar. Quanto mais detalhe, mais rápido a gente entrega valor. Demora ~15 min. Pode pular o que não fizer sentido.

### Seção 1 — O básico

| Pergunta | Tipo | Obrigatório |
|---|---|---|
| Nome da empresa / projeto | texto curto | sim |
| Site / Instagram / link principal | texto curto | não |
| Como você se descreveria em 1 frase? | texto longo | sim |
| Há quanto tempo o projeto existe? | escolha única (< 6 meses, 6m-2a, 2-5a, 5+) | sim |

### Seção 2 — Público

| Pergunta | Tipo | Obrigatório |
|---|---|---|
| Quem é o cliente ideal? Idade, profissão, dor principal | texto longo | sim |
| Onde esse cliente "mora" digitalmente? (IG, TikTok, LinkedIn, YouTube) | múltipla escolha | sim |
| O que ele NÃO entende que faz seu produto valer? | texto longo | não |

### Seção 3 — Oferta

| Pergunta | Tipo | Obrigatório |
|---|---|---|
| O que vende? (produto/serviço principal) | texto longo | sim |
| Faixa de preço atual | texto curto | não |
| Maior objeção que escuta | texto longo | não |
| Garantia oferecida (se tem) | texto longo | não |

### Seção 4 — Concorrência e referências

| Pergunta | Tipo | Obrigatório |
|---|---|---|
| 3 concorrentes diretos (links) | texto longo | sim |
| 3 perfis de inspiração de comunicação | texto longo | não |
| O que NÃO querem virar | texto longo | não |

### Seção 5 — Operação

| Pergunta | Tipo | Obrigatório |
|---|---|---|
| Quem da equipe vai ser ponto-focal? | texto curto | sim |
| Quanto vocês conseguem produzir por semana? | escolha única (<1 vídeo, 1-3, 4-7, 8+) | sim |
| Já roda ads? Quanto/mês? | texto curto | não |
| O que tá te impedindo hoje? | texto longo | sim |

### Seção 6 — Contexto livre

| Pergunta | Tipo | Obrigatório |
|---|---|---|
| Tem algo que você acha que precisamos saber e essas perguntas não cobriram? | texto longo | não |
| Pode anexar materiais (PDF, áudio, imagem) | upload de arquivos | não |

## Configuração

- **Coletar e-mail:** sim (auto-preenchido se logado em conta Google)
- **Limitar a 1 resposta por pessoa:** não
- **Permitir editar resposta:** sim
- **Página de confirmação:** "Recebido. Daqui a algumas horas a gente volta com o próximo passo."
- **Respostas:** habilitar Sheets-link (Form gera Sheets na pasta `00 — Briefing/Briefing (respostas)`)

## API mapping (gws-forms)

| Operação | Notas |
|---|---|
| Duplicar template | `gws forms copy --source <template_id> --name "Briefing — <cliente>"` retorna `form_id` |
| Mover pra Drive certo | `gws drive move <form_id> --parent <pasta_briefing_id>` |
| Linkar respostas a Sheet | `gws forms link-sheet <form_id> --sheet-name "Briefing (respostas)"` |
| Pegar URL pública | `gws forms get-public-url <form_id>` |
