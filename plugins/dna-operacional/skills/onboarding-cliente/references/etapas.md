# Etapas detalhadas — Skill onboarding-cliente

Cada etapa = uma responsabilidade. Skill principal chama em ordem. Erro em qualquer uma → status `falhou_etapa_N` + log.

---

## Etapa 2 — Shared Drive + Pastas padrão

**Objetivo:** criar Shared Drive `<Cliente> — Ahoy` com a árvore canônica + permissões.

**Inputs (da Etapa 1):**
- `cliente_nome`
- `cliente_email`
- `equipe_whatsapp` (números — não emails; precisa pegar e-mails da equipe via reference futura ou config — ver "Gotcha #1")

**Sub-passos:**

### 2.1 Criar Shared Drive

```bash
DRIVE_ID=$(gws drive shared-drive create \
  --name "<cliente_nome> — Ahoy" \
  --json | jq -r '.id')
```

Validar: `[ -n "$DRIVE_ID" ] || abort "falha criar shared drive"`.

### 2.2 Adicionar membros da equipe (organizer)

Pra cada `email` em `equipe_emails` (ver Gotcha #1):

```bash
gws drive permissions add "$DRIVE_ID" \
  --email "$email" \
  --role organizer \
  --notify=false
```

### 2.3 Adicionar cliente (fileOrganizer)

```bash
gws drive permissions add "$DRIVE_ID" \
  --email "<cliente_email>" \
  --role fileOrganizer \
  --notify=false  # mensagem é pelo WhatsApp, não pelo Drive
```

### 2.4 Criar árvore de pastas

Lista de pastas (ordem importa pra criar com prefixo certo):

```
00 — Briefing
00 — Briefing/Materiais do Briefing
01 — Estratégia
01 — Estratégia/Voz e Tom
01 — Estratégia/Público e Persona
01 — Estratégia/Posicionamento
02 — Conteúdo
02 — Conteúdo/Roteiros
02 — Conteúdo/Carrosséis
02 — Conteúdo/Vídeos brutos
02 — Conteúdo/Publicado
03 — Ads
03 — Ads/Briefings de campanha
03 — Ads/Criativos
03 — Ads/Relatórios
04 — Landing Pages
05 — Reuniões
05 — Reuniões/Atas e gravações
99 — Anexos do cliente
```

Pra cada path, criar via `gws drive folder create --parent <parent_id> --name <leaf>`. Manter mapa local `path → folder_id` pra resolver pais nos próximos.

Pseudocódigo:

```python
folder_ids = {"": DRIVE_ID}  # raiz
for path in tree:
    parts = path.split("/")
    parent = "/".join(parts[:-1])
    leaf = parts[-1]
    parent_id = folder_ids[parent]
    new_id = gws_drive_folder_create(parent=parent_id, name=leaf)
    folder_ids[path] = new_id
```

Guardar `briefing_folder_id = folder_ids["00 — Briefing"]` pra Etapa 3.

### 2.5 Output

Retorna pra orquestrador:
- `drive_id`
- `drive_url = https://drive.google.com/drive/folders/<drive_id>`
- `briefing_folder_id`

### Gotcha #1: e-mails da equipe ≠ números do WhatsApp

`equipe_whatsapp` e `equipe_emails` são listas independentes:
- **`equipe_whatsapp`**: quem entra no GRUPO WhatsApp do cliente (mais enxuto — quem fala diretamente)
- **`equipe_emails`**: quem tem acesso ao Drive (mais amplo — equipe inteira)

Validação na Etapa 0:
- `equipe_emails` tem ≥ 1 e-mail
- Todos e-mails são válidos (regex `^[^@]+@[^@]+\.[^@]+$`)
- Cada `equipe_whatsapp` segue formato BR (`^55\d{10,11}$`)

Sem requisito de igualdade entre listas. A equipe WhatsApp pode ser subconjunto, conjunto disjunto, ou superset da equipe Drive — depende da operação.

### Rollback se falha

Se 2.1 falha → não cria nada. Aborta.
Se 2.2-2.5 falha → Drive já existe; loga `drive_id` no `cliente.json` com `status: falhou_etapa_2_pastas` e instrui:
> Drive criado em <url>. Estrutura parcial. Pra completar manualmente, segue template em `templates/onboarding-folder-structure.md`.

---

## Etapa 3 — Google Form de briefing

**Objetivo:** duplicar o Form template + linkar respostas em Sheet dentro do Drive.

**Inputs:**
- `briefing_form_template_id` (do CLAUDE.md)
- `cliente_nome`
- `briefing_folder_id` (da Etapa 2)

**Sub-passos:**

### 3.1 Duplicar template

```bash
FORM_ID=$(gws forms copy \
  --source "$BRIEFING_FORM_TEMPLATE_ID" \
  --name "Briefing — $CLIENTE_NOME" \
  --json | jq -r '.id')
```

### 3.2 Mover pra pasta `00 — Briefing/`

```bash
gws drive move "$FORM_ID" --parent "$BRIEFING_FOLDER_ID"
```

### 3.3 Atualizar título e descrição (substituir placeholder)

Se o template usa `{{cliente_nome}}` no título, gws-forms permite update:

```bash
gws forms update "$FORM_ID" \
  --title "Briefing — $CLIENTE_NOME" \
  --description "Esse briefing nos dá o contexto pra começar..."
```

### 3.4 Linkar respostas a Sheet

```bash
SHEET_ID=$(gws forms link-sheet "$FORM_ID" \
  --sheet-name "Briefing (respostas)" \
  --json | jq -r '.spreadsheet_id')
```

A Sheet aparece automaticamente em `00 — Briefing/Briefing (respostas)` (Forms põe na mesma pasta do Form).

### 3.5 Pegar URL pública

```bash
FORM_URL=$(gws forms get-public-url "$FORM_ID")
# Format: https://docs.google.com/forms/d/e/<id>/viewform
```

### 3.6 Output

- `form_id`
- `form_url`
- `form_responses_sheet_id`

### Rollback

Se 3.1 falha → loga, status `falhou_etapa_3`. Drive da Etapa 2 fica como está (não desfaz).
Se 3.2-3.5 falha → Form criado mas em local errado. Status `falhou_etapa_3_partial`. Loga `form_id` pra fix manual.

---

## Etapa 4 — NotebookLM vazio

**Objetivo:** criar notebook nomeado, sem sources iniciais (popular vem em hook futuro).

**Inputs:**
- `cliente_nome`

**Sub-passos:**

### 4.1 Criar notebook via CLI

```bash
NOTEBOOK_ID=$(notebooklm create \
  --title "$CLIENTE_NOME — DNA" \
  --json | jq -r '.id')
```

### 4.2 Construir URL

```
NOTEBOOK_URL="https://notebooklm.google.com/notebook/$NOTEBOOK_ID"
```

### 4.3 Output

- `notebooklm_id`
- `notebooklm_url`

### Gotcha #2: notebook vazio é "ok"

NotebookLM aceita notebook sem sources. UI mostra empty state. Não é bug. Hook futuro (v0.5) adiciona briefing como source quando Form é preenchido.

### Rollback

Se 4.1 falha → status `falhou_etapa_4`. Etapas 2-3 ficam. Skill imprime instrução manual:
> NotebookLM falhou. Cria manualmente: https://notebooklm.google.com → "Novo notebook" → título "<cliente> — DNA". Cola o ID no `cliente.json`.

---

## Etapa 5 — Grupo WhatsApp + Mensagem de boas-vindas

**Objetivo:** criar grupo via uazapi com 3+ números, mandar mensagem de boas-vindas com links das etapas 2-4.

**Inputs:**
- `cliente_whatsapp` (principal)
- `whatsapps_extras` (lista)
- `bruna_whatsapp` (do CLAUDE.md)
- `equipe_whatsapp` (lista, do CLAUDE.md)
- `cliente_nome`
- `drive_url`, `form_url` (das etapas anteriores)
- `uazapi_url`, `uazapi_token` (env)

### 5.1 Criar grupo

Endpoint uazapi: `POST /group/create`

```bash
RESPONSE=$(curl -X POST "$UAZAPI_URL/group/create" \
  -H "Content-Type: application/json" \
  -H "token: $UAZAPI_TOKEN" \
  -d "{
    \"name\": \"Ahoy × $CLIENTE_NOME\",
    \"participants\": [
      \"$CLIENTE_WHATSAPP\",
      $(echo "$WHATSAPPS_EXTRAS_JSON"),
      $(echo "$EQUIPE_WHATSAPP_JSON")
    ]
  }")

GROUP_JID=$(echo "$RESPONSE" | jq -r '.group.jid')
# Format: 120363XXXXXXXXX@g.us
```

> **Nota:** `bruna_whatsapp` NÃO entra em `participants` — é o número da própria instância UAZAPI (admin do grupo automaticamente).

### 5.2 Promover equipe a admin (opcional, recomendado)

Endpoint: `POST /group/promote`

```bash
for num in $EQUIPE_WHATSAPP; do
  curl -X POST "$UAZAPI_URL/group/promote" \
    -H "Content-Type: application/json" \
    -H "token: $UAZAPI_TOKEN" \
    -d "{\"groupJid\": \"$GROUP_JID\", \"participants\": [\"$num\"]}"
done
```

### 5.3 Mandar mensagem de boas-vindas

Template em `references/mensagens.md`. Render:

```
Oi <primeiro nome do cliente>! 🌊

A Ahoy tá oficialmente onboard. Aqui é a Bruna — vou ser teu ponto de contato pro dia-a-dia.

Pra a gente começar com tudo, fiz 3 coisas:

📋 Briefing rápido (15 min):
<form_url>

📁 Tua pasta no Drive (já tem acesso):
<drive_url>

Qualquer foto, áudio, PDF, contrato anterior, vídeo de referência — joga em "99 — Anexos do cliente" lá no Drive.

Assim que preencher o briefing, a equipe começa a montar a estratégia. Qualquer dúvida, é por aqui mesmo.

Bem-vindo(a)! 💙
```

Endpoint: `POST /send/text`

```bash
curl -X POST "$UAZAPI_URL/send/text" \
  -H "Content-Type: application/json" \
  -H "token: $UAZAPI_TOKEN" \
  -d "{
    \"number\": \"$GROUP_JID\",
    \"text\": \"$MESSAGE_RENDERED\"
  }"
```

### 5.4 Output

- `whatsapp_group_jid`

### Gotcha #3: rate limit do uazapi

Free tier: 30 msgs/min. Mensagem única não chega perto. Mas se rodar onboarding em loop pra múltiplos clientes, separar com sleep 2s entre.

### Gotcha #4: número precisa ter WhatsApp

Se `cliente_whatsapp` não tem WhatsApp, `/group/create` falha com `participant_not_found`. Skill detecta e retorna mensagem amigável:
> Número <X> não tem WhatsApp. Confirma o número com o cliente e roda de novo.

### Rollback

Se 5.1 falha → grupo não existe. Status `falhou_etapa_5`. Etapas 2-4 ficam. Skill instrui:
> Grupo WhatsApp falhou. Pra completar: cria grupo manual com Bruna + Flávio + cliente, e cola o JID via `/onboarding --resume <slug> --group-jid <jid>` (v0.5).
>
> Por ora, copia esses links e manda manual:
> Drive: <drive_url>
> Briefing: <form_url>

Se 5.1 OK mas 5.3 (mensagem) falha → grupo existe sem mensagem. Status `falhou_etapa_5_msg`. Skill imprime:
> Grupo criado. Mensagem falhou. Manda manual:
> [conteúdo da mensagem]
