# Onboarding de Cliente — Implementation Plan

> **For agentic workers:** REQUIRED: Use team-powers:team-driven-development (if Agent Teams available) or team-powers:executing-plans to implement this plan. For simpler single-domain tasks, subagent-driven approach is still valid. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adicionar comando `/onboarding` ao plugin DNA Operacional que orquestra o ritual de boas-vindas de um novo cliente: cria grupo WhatsApp (cliente + Bruna + equipe), Shared Drive com pastas padrão, Google Form de briefing, NotebookLM vazio nomeado e dispara mensagem de boas-vindas pela Bruna.

**Architecture:** Wrapper command `/onboarding` em `commands/` invoca skill bundled `skills/onboarding-cliente/SKILL.md`. Skill consome 3 skills externas globais (uazapi, gws-drive, gws-forms, notebooklm) — invocadas via `Skill` tool. Persistência segue o padrão `data/clientes/<slug>/` já estabelecido pelas skills de entrega (`/orcamento`, `/contrato`), com extensão do schema `cliente.json` pra carregar IDs do onboarding (whatsapp_group_jid, drive_id, form_id, sheets_id, notebooklm_id).

**Tech Stack:** Markdown skill prompts + JSON manifests + uazapi REST (grupos + send/text) + Google Workspace via gws CLI (Drive Shared Drive create, Forms duplicate from template, Sheets read responses) + notebooklm CLI (notebook create) + storage layer existente (markdown adapter pra rollup CSV).

---

## Pré-requisitos do user (validar antes de executar)

Antes de a skill rodar, o projeto do user precisa ter no `CLAUDE.md`:

```markdown
## Onboarding (cliente)
- bruna_whatsapp: 5511936187040
- equipe_whatsapp:
  - 5581998385073   # Flávio
- equipe_emails:
  - contato@ahoydigital.ag
  - fran@ahoydigital.ag
  - pedrocaracciolov@gmail.com
  - leonardo.ahoydigital@gmail.com
  - isabelleahoymidia@gmail.com
  - pedrocaracciolo.ahoydigital@gmail.com
- uazapi_url: https://ahoydigital.uazapi.com
- uazapi_token_env: UAZAPI_TOKEN_BRUNA
- briefing_form_template_id: <ID do Form modelo no Drive — criar 1× manualmente, ver Task 3>
- shared_drive_parent: ""   # vazio = cria Shared Drive novo por cliente (default)
- gws_account: contato@ahoydigital.ag
```

E env var (NÃO commitar — vai em `~/.zshrc` ou `~/.bashrc`):
```bash
export UAZAPI_TOKEN_BRUNA='<uuid-da-instância>'
```

Se faltar qualquer item, skill aborta com mensagem amigável apontando o que configurar.

**Confirmações pendentes do user (já alinhadas em conversa, registrar aqui):**

- ✅ Número Flávio: `5581998385073` (formato BR completo, com 9 inicial)
- ✅ Número Bruna (instância UAZAPI): `5511936187040` (admin do grupo automaticamente)
- ✅ Briefing: Google Form (respostas → Sheets dentro do Shared Drive)
- ✅ Shared Drive: novo por cliente, com pastas padrão
- ✅ NotebookLM: criado vazio no onboarding, populado via hook quando briefing for preenchido (hook é fora do escopo deste plan — entra em v0.5)
- ✅ Equipe Drive: 6 e-mails (lista acima) entram como `organizer`. Equipe WhatsApp começa só com Flávio — quando crescer, adicionar mais números em `equipe_whatsapp:`.
- ✅ UAZAPI server: `https://ahoydigital.uazapi.com` (instância dedicada Ahoy)

---

## File Structure

### Arquivos a CRIAR

| Path | Responsabilidade |
|---|---|
| `plugins/dna-operacional/commands/onboarding.md` | Wrapper fino do comando `/onboarding`. Lê contexto DNA, coleta dados, invoca skill. |
| `plugins/dna-operacional/skills/onboarding-cliente/SKILL.md` | Skill bundled. Orquestra 5 etapas (coleta, grupo WhatsApp, Drive, Form, NotebookLM, msg boas-vindas). |
| `plugins/dna-operacional/skills/onboarding-cliente/references/etapas.md` | Detalhamento de cada etapa com payloads exatos, error handling, rollback parcial. |
| `plugins/dna-operacional/skills/onboarding-cliente/references/mensagens.md` | Templates de mensagens (boas-vindas, briefing pendente, follow-up) com placeholders. |
| `plugins/dna-operacional/templates/briefing-form-template.md` | Spec do Google Form modelo de briefing (perguntas, seções, campo email obrigatório). |
| `plugins/dna-operacional/templates/onboarding-folder-structure.md` | Estrutura padrão das pastas dentro do Shared Drive do cliente. |
| `plugins/dna-operacional/skills/onboarding-cliente/tests/smoke.md` | Smoke test conversacional documentado (input fixtures + expected outputs). |

### Arquivos a MODIFICAR

| Path | Mudança | Linhas aprox. |
|---|---|---|
| `plugins/dna-operacional/.claude-plugin/plugin.json` | Bump versão `0.3.0` → `0.4.0` | linha 3 |
| `plugins/dna-operacional/commands/dna.md` | Adicionar `/onboarding` no menu CLIENTE + nova jornada "Onboarding" | linhas 78-83 (menu) + 144-152 (jornadas) |
| `plugins/dna-operacional/templates/clientes-folder-structure.md` | Estender schema `cliente.json` com 5 campos de onboarding | linhas 42-60 (cliente.json schema) |
| `plugins/dna-operacional/docs/CONVENCOES.md` | Adicionar `/onboarding` na tabela de mapeamento (sugere `/orcamento`) | tabela §2 |
| `plugins/dna-operacional/docs/JORNADAS.md` | Documentar jornada de onboarding completa | append no fim |
| `plugins/dna-operacional/docs/APIS-EXTERNAS.md` | Seção UAZAPI + seção NotebookLM | append novas seções |
| `CHANGELOG.md` | Entry v0.4.0 com feat onboarding | topo |

### Arquivo de rollup novo

| Path (criado em runtime no projeto do user) | Schema |
|---|---|
| `data/onboardings.csv` | `id,cliente,slug,whatsapp_group_jid,drive_id,form_id,notebooklm_id,status,created_at` |

---

## Schema Extensions

### `cliente.json` — campos novos (extensão, retrocompatível)

```json
{
  "nome": "Matheus Moita",
  "slug": "matheus-moita",
  "razao_social": "...",
  "cnpj": "...",
  "email": "...",
  "telefone": "+55 85 99999-0000",
  "nicho": "...",
  "endereco": "...",
  "contato_nome": "...",
  "contato_cargo": "...",
  "created_at": "...",
  "updated_at": "...",
  "notes": "...",

  "onboarding": {
    "whatsapp_principal": "5585999990000",
    "whatsapps_extras": ["5585988880000"],
    "whatsapp_group_jid": "120363...@g.us",
    "drive_id": "0AB...XYZ",
    "drive_url": "https://drive.google.com/drive/folders/0AB...XYZ",
    "form_id": "1aBc...",
    "form_url": "https://docs.google.com/forms/d/e/.../viewform",
    "form_responses_sheet_id": "1xyZ...",
    "notebooklm_id": "uuid-...",
    "notebooklm_url": "https://notebooklm.google.com/notebook/...",
    "status": "iniciado",
    "started_at": "2026-05-07T10:00:00-03:00",
    "completed_at": null
  }
}
```

**Status do onboarding:** `iniciado` | `briefing_enviado` | `briefing_recebido` | `concluido` | `falhou_<etapa>`

**Regra de write:** se `cliente.json` já existe (cliente teve `/orcamento` antes), faz merge — adiciona apenas o objeto `onboarding`. Não sobrescreve campos top-level.

---

## Chunk 1: Templates + Schema + Coleta

### Task 1: Bumpar versão do plugin

**Files:**
- Modify: `plugins/dna-operacional/.claude-plugin/plugin.json:3`

- [ ] **Step 1: Atualizar `version`**

```json
{
  "name": "dna-operacional",
  "version": "0.4.0",
```

- [ ] **Step 2: Verificar que git tag vai bater (ver LEARNINGS — cache do marketplace)**

A regra do CLAUDE.md do plugin: `plugin.json.version` deve bater com a git tag. Anota mental: depois de mergear, criar tag `v0.4.0`. (Não fazer agora — apenas no final.)

- [ ] **Step 3: Commit isolado**

```bash
git add plugins/dna-operacional/.claude-plugin/plugin.json
git commit -m "chore(plugin): bump versão pra v0.4.0 (onboarding)"
```

---

### Task 2: Template — estrutura de pastas do Shared Drive

**Files:**
- Create: `plugins/dna-operacional/templates/onboarding-folder-structure.md`

- [ ] **Step 1: Criar template documentando árvore canônica**

Conteúdo do arquivo:

````markdown
# Shared Drive do Cliente — Estrutura padrão

Cada novo onboarding cria um Shared Drive `[Cliente] — Ahoy` com a árvore abaixo. Nomes em PT-BR (cliente abre, equipe trabalha).

## Árvore

```
[Cliente] — Ahoy/
├── 00 — Briefing/
│   ├── Briefing (respostas)         # Sheets gerado pelo Form
│   └── Materiais do Briefing/       # áudios, prints, refs do cliente
├── 01 — Estratégia/
│   ├── Voz e Tom/
│   ├── Público e Persona/
│   └── Posicionamento/
├── 02 — Conteúdo/
│   ├── Roteiros/
│   ├── Carrosséis/
│   ├── Vídeos brutos/
│   └── Publicado/
├── 03 — Ads/
│   ├── Briefings de campanha/
│   ├── Criativos/
│   └── Relatórios/
├── 04 — Landing Pages/
├── 05 — Reuniões/
│   └── Atas e gravações/
└── 99 — Anexos do cliente/         # cliente joga aqui o que não souber onde
```

## Permissões

- **Owner:** equipe Ahoy (todos da `equipe_whatsapp` viram membros com role `manager`)
- **Cliente:** convidado como `contentManager` na raiz (pode ver/editar tudo, não pode deletar a estrutura)
- **`00 — Briefing/`:** acesso restrito de leitura pro cliente após preenchimento (a equipe ajusta no fim do onboarding se necessário)

## Convenções de nome

- Pastas com prefixo numérico (`00`, `01`, `02`...) pra ordem fixa no Drive
- Em PT-BR
- Cliente nunca cria pasta na raiz — só dentro de `99 — Anexos do cliente/`

## API mapping (gws-drive)

| Operação | Endpoint gws | Notas |
|---|---|---|
| Criar Shared Drive | `gws drive shared-drive create --name "<Cliente> — Ahoy"` | retorna `drive_id` |
| Adicionar membro | `gws drive permissions add <drive_id> --email <email> --role <role>` | role: `organizer` (equipe), `fileOrganizer` (cliente) |
| Criar pasta | `gws drive folder create --parent <drive_id> --name "<nome>"` | repetir pra cada nó |
````

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/templates/onboarding-folder-structure.md
git commit -m "docs(templates): estrutura padrão do Shared Drive de cliente (onboarding)"
```

---

### Task 3: Template — Google Form de briefing

**Files:**
- Create: `plugins/dna-operacional/templates/briefing-form-template.md`

- [ ] **Step 1: Criar spec do Form**

````markdown
# Google Form — Briefing de cliente

Spec do Form modelo que a skill `/onboarding` duplica pra cada cliente. Tem que existir 1 vez na conta `contato@ahoydigital.ag` e ter o `briefing_form_template_id` registrado no CLAUDE.md.

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
````

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/templates/briefing-form-template.md
git commit -m "docs(templates): spec do Google Form de briefing"
```

---

### Task 4: Estender schema cliente.json em clientes-folder-structure.md

**Files:**
- Modify: `plugins/dna-operacional/templates/clientes-folder-structure.md:42-60`

- [ ] **Step 1: Adicionar bloco `onboarding` no schema documentado**

Substituir o bloco `## cliente.json — schema` adicionando o objeto `onboarding` opcional. Manter retrocompatibilidade — campos top-level continuam idênticos.

**Patch a aplicar:**

Logo depois da linha 59 (`"notes": "Preferência por WhatsApp. Assinou em 21/04."`), antes de fechar o `}`, adicionar:

```json
,
  "onboarding": {
    "whatsapp_principal": "5585999990000",
    "whatsapps_extras": [],
    "whatsapp_group_jid": "120363...@g.us",
    "drive_id": "0AB...XYZ",
    "drive_url": "https://drive.google.com/drive/folders/0AB...XYZ",
    "form_id": "1aBc...",
    "form_url": "https://docs.google.com/forms/d/e/.../viewform",
    "form_responses_sheet_id": "1xyZ...",
    "notebooklm_id": "uuid-...",
    "notebooklm_url": "https://notebooklm.google.com/notebook/...",
    "status": "iniciado",
    "started_at": "2026-05-07T10:00:00-03:00",
    "completed_at": null
  }
```

E adicionar nota abaixo do bloco JSON:

> **Bloco `onboarding`:** opcional. Populado pela skill `/onboarding`. Se cliente teve `/orcamento` antes do onboarding, o bloco é mergeado depois — top-level fica intocado.
>
> **Status:** `iniciado` (skill rodou) | `briefing_enviado` (mensagem disparada) | `briefing_recebido` (Form preenchido — atualizado por hook futuro v0.5) | `concluido` | `falhou_<etapa>` (rollback parcial executado)

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/templates/clientes-folder-structure.md
git commit -m "docs(templates): estender cliente.json com bloco onboarding (retrocompat)"
```

---

### Task 5: Skill onboarding-cliente — etapa de coleta

**Files:**
- Create: `plugins/dna-operacional/skills/onboarding-cliente/SKILL.md`

Esta task cria APENAS a estrutura inicial da skill + a etapa 1 (coleta de dados). Etapas 2-5 entram em tasks subsequentes.

- [ ] **Step 1: Criar skeleton da SKILL.md**

````markdown
---
name: onboarding-cliente
description: Onboarding completo de cliente novo. Cria grupo WhatsApp (cliente + Bruna + equipe), Shared Drive com pastas padrão, Google Form de briefing, NotebookLM nomeado, e dispara mensagem de boas-vindas pela Bruna com links. Use quando o usuário digitar "/onboarding", "novo cliente", "iniciar cliente", "kickoff cliente".
---

# Onboarding de Cliente — Skill

Skill orquestra 5 etapas. Cada etapa é independente e idempotente: se uma falha, retorna `falhou_<etapa>` no `cliente.json` e a skill pode ser re-executada com `/onboarding --resume <slug>` (não no MVP, anotado pra v0.5).

## Pré-checks (Etapa 0)

Antes de qualquer ação:

1. Ler CLAUDE.md do projeto. Validar presença de:
   - `## Onboarding (cliente)` section
   - `bruna_whatsapp`, `equipe_whatsapp`, `uazapi_url`, `uazapi_token_env`, `briefing_form_template_id`, `gws_account`
2. Validar env var apontada por `uazapi_token_env` (default: `UAZAPI_TOKEN_BRUNA`).
3. Validar formato dos números: `^55\d{10,11}$` (BR). Avisar se faltar `9` no celular.
4. Verificar que `gws auth status` retorna logged-in pra `gws_account`.
5. Verificar que `notebooklm status` retorna autenticado.

Se qualquer falha:

```
⚠ Onboarding precisa de configuração antes de rodar.
Faltando:
  • <item 1>
  • <item 2>

Ver: ${CLAUDE_PLUGIN_ROOT}/docs/APIS-EXTERNAS.md#onboarding
```

E aborta.

## Etapa 1 — Coleta conversacional

Perguntar (uma de cada vez, conversacional):

1. **Nome do cliente** (se não veio em `$ARGUMENTS`)
2. **WhatsApp principal do cliente** (validar formato BR, normalizar com `9` se faltar)
3. **Mais algum WhatsApp pra adicionar no grupo?** (lista, vazio = só o principal)
4. **E-mail do cliente** (pra dar acesso ao Shared Drive)
5. **Nicho** (livre — vira input de Etapa 4 título do NotebookLM)

Calcular `slug` segundo regra de `clientes-folder-structure.md`.

Confirmar dados antes de prosseguir:

```
Vou rodar onboarding pra:
  Cliente: Matheus Moita (slug: matheus-moita)
  WhatsApp: +55 85 99999-0000
  Extras:   nenhum
  E-mail:   matheus@mm.com.br
  Nicho:    nutricionista

Vou criar:
  ✓ Grupo WhatsApp com 3 números (cliente + Bruna + Flávio)
  ✓ Shared Drive "Matheus Moita — Ahoy" com 6 pastas padrão
  ✓ Google Form de briefing (cópia do template)
  ✓ NotebookLM "Matheus Moita — DNA" (vazio, equipe popula depois)
  ✓ Mensagem de boas-vindas da Bruna no grupo (com links)

Confirma? (s/n)
```

Se `s`, prossegue. Se `n`, aborta sem criar nada (zero side effects até aqui).

## Etapa 2-5

Documentadas em `references/etapas.md`. Skill chama em ordem:

1. Etapa 2: Cria Shared Drive + pastas (gws-drive)
2. Etapa 3: Cria Form briefing duplicando template (gws-forms) + linka Sheet
3. Etapa 4: Cria NotebookLM vazio (notebooklm CLI)
4. Etapa 5: Cria grupo WhatsApp (uazapi) + Bruna manda mensagem boas-vindas com links

Ordem importante: WhatsApp por último porque mensagem precisa dos URLs gerados pelas etapas 2-4.

## Etapa 6 — Persistência

Após sucesso de todas:

1. Cria/atualiza `data/clientes/<slug>/cliente.json` (merge se existe)
2. Append em `data/onboardings.csv`:
   ```
   id,cliente,slug,whatsapp_group_jid,drive_id,form_id,notebooklm_id,status,created_at
   ```
3. Atualiza `cliente.onboarding.status = "briefing_enviado"`

## Etapa 7 — Output pro user

```
╔══════════════════════════════════════════════════════════════════╗
║  🎉 Onboarding criado: Matheus Moita                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📱 Grupo WhatsApp:  +55 85 99999-0000 + Bruna + Flávio          ║
║  📁 Drive:           https://drive.google.com/...                ║
║  📋 Briefing:        https://forms.gle/...                       ║
║  🧠 NotebookLM:      https://notebooklm.google.com/notebook/...  ║
║                                                                  ║
║  Próximos passos:                                                ║
║    • Aguardar cliente preencher briefing                         ║
║    • Quando preencher: /setup-projeto pra criar projeto DNA dele ║
║    • Depois: /orcamento pra mandar a proposta                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

E o bloco "Próximos Passos" do CONVENCOES.md §1:

```
✅ Onboarding de Matheus Moita criado em 4 sistemas.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 PRÓXIMOS PASSOS SUGERIDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. /setup-projeto matheus-moita    — quando briefing chegar
  2. /orcamento Matheus Moita        — proposta comercial

  💡 /dna pra ver todas · /dna jornadas pra caminhos completos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Rollback parcial

Se Etapa N falha após Etapa N-1 ter sucedido, skill:
1. NÃO desfaz etapas anteriores (leave-it-and-log).
2. Atualiza `cliente.onboarding.status = "falhou_etapa_N"`.
3. Imprime instrução manual de cleanup OU re-execução parcial.

Detalhe por etapa em `references/etapas.md`.

## Storage layer

Onboarding **não usa** as 7 tabelas do contract.md (são pra dados de criador, não cliente).
Dados de cliente seguem o padrão `data/clientes/<slug>/` já estabelecido pelas skills `/orcamento`, `/contrato`. Append em `data/onboardings.csv` segue convenção RFC 4180.

Reuso conforme regra: nenhum SQL inline. Persistência via Read/Write nativos.
````

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/skills/onboarding-cliente/SKILL.md
git commit -m "feat(skill): skeleton da skill onboarding-cliente (etapa 1: coleta)"
```

---

## Chunk 2: Integrações externas (Etapas 2-5)

### Task 6: references/etapas.md — Etapa 2 (Shared Drive)

**Files:**
- Create: `plugins/dna-operacional/skills/onboarding-cliente/references/etapas.md`

- [ ] **Step 1: Criar arquivo com Etapa 2 detalhada**

````markdown
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
````

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/skills/onboarding-cliente/references/etapas.md
git commit -m "docs(skill): etapas detalhadas (Drive, Form, NotebookLM, WhatsApp)"
```

---

### Task 7: references/mensagens.md — templates de mensagens

**Files:**
- Create: `plugins/dna-operacional/skills/onboarding-cliente/references/mensagens.md`

- [ ] **Step 1: Criar arquivo com templates**

````markdown
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
````

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/skills/onboarding-cliente/references/mensagens.md
git commit -m "docs(skill): templates de mensagens da Bruna (boas-vindas + futuras)"
```

---

### Task 8: SKILL.md — integrar referências às etapas

**Files:**
- Modify: `plugins/dna-operacional/skills/onboarding-cliente/SKILL.md`

- [ ] **Step 1: Substituir o bloco "## Etapa 2-5" pela invocação real**

Agora que `references/etapas.md` existe, o SKILL.md aponta pra ele explicitamente. Trocar o stub por:

```markdown
## Etapas 2-5 — Execução

Skill executa em ordem (sequencial — etapa N+1 precisa do output de N):

| Etapa | Ação | Reference |
|---|---|---|
| 2 | Cria Shared Drive + 6 pastas padrão | `references/etapas.md#etapa-2` |
| 3 | Duplica Form briefing + linka Sheet | `references/etapas.md#etapa-3` |
| 4 | Cria NotebookLM vazio | `references/etapas.md#etapa-4` |
| 5 | Cria grupo WhatsApp + manda mensagem boas-vindas | `references/etapas.md#etapa-5` |

Cada etapa retorna IDs/URLs que entram no `cliente.json`. Erro em qualquer etapa → status `falhou_etapa_N`, skill aborta SEM desfazer etapas anteriores. User vê instrução manual de fix em cada caso.

Mensagens disparadas pela Bruna seguem templates em `references/mensagens.md`.
```

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/skills/onboarding-cliente/SKILL.md
git commit -m "feat(skill): integrar SKILL.md com etapas + mensagens references"
```

---

## Chunk 3: Wrapper, menu, persistência, smoke

### Task 9: Wrapper command /onboarding

**Files:**
- Create: `plugins/dna-operacional/commands/onboarding.md`

- [ ] **Step 1: Criar wrapper fino seguindo padrão do `/orcamento`**

````markdown
---
description: Onboarding completo de cliente novo — cria grupo WhatsApp (cliente + Bruna + equipe), Shared Drive com pastas padrão, Google Form de briefing, NotebookLM nomeado, e dispara mensagem de boas-vindas pela Bruna com links. Use quando digitar "/onboarding", "novo cliente", "iniciar cliente <nome>", "kickoff cliente".
argument-hint: "[nome do cliente]"
---

Usuário invocou `/onboarding $ARGUMENTS`.

Wrapper fino pra skill `onboarding-cliente` bundled em `${CLAUDE_PLUGIN_ROOT}/skills/onboarding-cliente/SKILL.md`.

## Resolução da skill

1. Bundled (preferencial): `${CLAUDE_PLUGIN_ROOT}/skills/onboarding-cliente/SKILL.md`
2. Sem fallback global (skill é nova, exclusiva do plugin).

Se ausente: abortar com `⚠ Skill onboarding-cliente não encontrada. Reinstale o plugin DNA Operacional.`

## Passo 1 — Pré-checks

Antes de invocar a skill, validar config no CLAUDE.md do projeto. Ver Etapa 0 do SKILL.md.

Se config faltando, imprimir instrução amigável e abortar.

## Passo 2 — Invocar skill

Usar **Skill tool** com `skill: "onboarding-cliente"` passando `$ARGUMENTS` (nome do cliente, se veio).

Se vazio, skill faz a coleta conversacional completa.

## Passo 3 — Output

Skill retorna o bloco final formatado. Wrapper só passa-pra-frente.
````

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/commands/onboarding.md
git commit -m "feat(command): /onboarding wrapper fino"
```

---

### Task 10: Atualizar /dna menu

**Files:**
- Modify: `plugins/dna-operacional/commands/dna.md:78-83`

- [ ] **Step 1: Adicionar `/onboarding` no menu CLIENTE**

Localizar o bloco:

```
║  📄 CLIENTE (entrega end-to-end)                                 ║
║     /orcamento ............ Proposta comercial PDF               ║
║     /apresentacao ......... Deck HTML+GSAP fora-da-caixa         ║
║     /landing-page ......... Landing de alta conversão            ║
║     /contrato ............. Edita .docx/.pdf → personalizado     ║
```

Substituir por:

```
║  📄 CLIENTE (entrega end-to-end)                                 ║
║     /onboarding ........... Kickoff (grupo WA + Drive + Form)    ║
║     /orcamento ............ Proposta comercial PDF               ║
║     /apresentacao ......... Deck HTML+GSAP fora-da-caixa         ║
║     /landing-page ......... Landing de alta conversão            ║
║     /contrato ............. Edita .docx/.pdf → personalizado     ║
```

- [ ] **Step 2: Atualizar versão do menu**

Linha `║  🧬 Comandos disponíveis (v0.2.0)` → `║  🧬 Comandos disponíveis (v0.4.0)`.

- [ ] **Step 3: Adicionar/atualizar jornada CLIENTE em Modo 2**

Substituir o bloco:

```
┌───────────────────────────────────────────────────────────┐
│  📄 JORNADA ENTREGA DE CLIENTE (fecha o loop)             │
│                                                           │
│  1. /setup-projeto        → configura projeto do cliente  │
│  2. /orcamento            → proposta comercial PDF        │
│  3. (assinatura)                                          │
│  4. /contrato             → contrato personalizado        │
│  5. /apresentacao         → kickoff deck (HTML+GSAP)      │
│  6. /landing-page         → LP do projeto                 │
└───────────────────────────────────────────────────────────┘
```

Por:

```
┌───────────────────────────────────────────────────────────┐
│  📄 JORNADA ENTREGA DE CLIENTE (fecha o loop)             │
│                                                           │
│  1. /onboarding           → grupo WA + Drive + briefing   │
│  2. (cliente preenche briefing)                           │
│  3. /setup-projeto        → configura projeto do cliente  │
│  4. /orcamento            → proposta comercial PDF        │
│  5. (assinatura)                                          │
│  6. /contrato             → contrato personalizado        │
│  7. /apresentacao         → kickoff deck (HTML+GSAP)      │
│  8. /landing-page         → LP do projeto                 │
└───────────────────────────────────────────────────────────┘
```

- [ ] **Step 4: Commit**

```bash
git add plugins/dna-operacional/commands/dna.md
git commit -m "feat(menu): adicionar /onboarding no menu CLIENTE + jornada atualizada"
```

---

### Task 11: Atualizar CONVENCOES.md

**Files:**
- Modify: `plugins/dna-operacional/docs/CONVENCOES.md`

- [ ] **Step 1: Adicionar `/onboarding` na tabela §2**

Procurar a tabela `## 2. Mapeamento inicial de sugestões`. Adicionar linha:

```
| `onboarding-cliente` | `/setup-projeto` (após briefing chegar), `/orcamento` |
```

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/docs/CONVENCOES.md
git commit -m "docs(convencoes): mapeamento de sugestões /onboarding"
```

---

### Task 12: Atualizar JORNADAS.md

**Files:**
- Modify: `plugins/dna-operacional/docs/JORNADAS.md`

- [ ] **Step 1: Adicionar seção "Jornada Onboarding"**

Append no fim:

````markdown
## Jornada: Onboarding de Cliente

Fecha o loop antes da entrega. Quando bate um cliente novo, este é o primeiro `/comando`.

### Fluxo

1. **`/onboarding`** — coleta dados (5 perguntas), cria 4 ativos:
   - Grupo WhatsApp (Cliente + Bruna + equipe Ahoy)
   - Shared Drive `<Cliente> — Ahoy` com 6 pastas padrão
   - Google Form de briefing (cópia do template)
   - NotebookLM `<Cliente> — DNA` (vazio, equipe popula depois)
2. **Cliente preenche briefing** (~15 min)
3. **(Hook futuro v0.5)** Form preenchido → respostas viram source no NotebookLM
4. **`/setup-projeto <slug>`** — gera o projeto DNA do cliente baseado no briefing
5. **`/orcamento <Cliente>`** — proposta comercial
6. **`/contrato <Cliente>`** — contrato personalizado
7. Resto da jornada CLIENTE segue normal

### Pré-requisitos no CLAUDE.md do user

```markdown
## Onboarding (cliente)
- bruna_whatsapp: <55XX9XXXXXXXX>
- equipe_whatsapp:
  - <55XX9XXXXXXXX>
- equipe_emails:
  - <email-google-workspace>
- uazapi_url: <https://...>
- uazapi_token_env: UAZAPI_TOKEN_BRUNA
- briefing_form_template_id: <ID do Form modelo>
- gws_account: <email>
```

E env var `$UAZAPI_TOKEN_BRUNA` apontada.
````

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/docs/JORNADAS.md
git commit -m "docs(jornadas): documentar jornada de onboarding"
```

---

### Task 13: Atualizar APIS-EXTERNAS.md

**Files:**
- Modify: `plugins/dna-operacional/docs/APIS-EXTERNAS.md`

- [ ] **Step 1: Adicionar tabela na visão geral**

Adicionar linhas na tabela `## Visão geral`:

```
| [UAZAPI](#uazapi) | `/onboarding` | Plano Ahoy: ~R$ 79/mês por instância |
| [NotebookLM](#notebooklm) | `/onboarding` | Free tier — 100 notebooks |
| [Google Forms](#google-forms) | `/onboarding` | Grátis (Workspace) |
```

- [ ] **Step 2: Adicionar seção UAZAPI**

Append depois de `## Modal`:

````markdown
## UAZAPI

API REST brasileira pra WhatsApp Business. Usado por `/onboarding` (criar grupo + mandar mensagem boas-vindas).

### 1. Conta + instância

1. Acessa https://uazapi.com (ou self-hosted https://ahoydigital.uazapi.com)
2. Cria conta, contrata plano com 1+ instância
3. Conecta WhatsApp via QR Code (escaneia com o número que vai mandar mensagens — ex: número da Bruna)

### 2. Obter token da instância

1. Painel UAZAPI → tua instância → "Token de instância"
2. Copia (formato UUID)

### 3. Configurar no sistema

```bash
export UAZAPI_TOKEN_BRUNA='<seu-token-uuid>'
```

E no `CLAUDE.md` do projeto:

```markdown
## Onboarding (cliente)
- bruna_whatsapp: 5511936187040
- uazapi_url: https://ahoydigital.uazapi.com
- uazapi_token_env: UAZAPI_TOKEN_BRUNA
```

### 4. Custo

- Plano Ahoy hosted: ~R$ 79/mês por instância
- Free tier: https://free.uazapi.com (1 instância, sem garantia)

### 5. Endpoints usados pelo plugin

- `POST /group/create` — criar grupo (Etapa 5.1)
- `POST /group/promote` — promover membros a admin (Etapa 5.2)
- `POST /send/text` — mandar mensagem (Etapa 5.3)

Reference completa em `~/.claude/skills/uazapi/SKILL.md` (skill global).

---

## NotebookLM

Notebook de pesquisa do Google. Usado por `/onboarding` (criar notebook nomeado pra equipe).

### 1. Instalar CLI

```bash
pip install notebooklm-py
notebooklm login   # OAuth Google
```

### 2. Verificar

```bash
notebooklm status
# deve mostrar "Authenticated as <email>"
```

### 3. Custo

- Free tier: 100 notebooks por conta Google
- Plus: ilimitado (R$ 100/mês)

### 4. Comandos usados pelo plugin

- `notebooklm create --title <nome>` — criar notebook (Etapa 4)

Reference completa em `~/.claude/skills/notebooklm/SKILL.md`.

---

## Google Forms

Usado por `/onboarding` (briefing do cliente).

### 1. Pré-requisito: ter o Form template

1. Cria 1 Google Form modelo seguindo `templates/briefing-form-template.md`
2. Salva em qualquer pasta do Google Drive da conta `gws_account`
3. Copia o ID da URL (`https://docs.google.com/forms/d/<ID>/edit`)

### 2. Configurar no CLAUDE.md

```markdown
## Onboarding (cliente)
- briefing_form_template_id: <ID do Form>
```

### 3. Custo

Grátis com Google Workspace.

### 4. Comandos gws-forms usados

- `gws forms copy --source <id> --name <novo>` — duplicar (Etapa 3.1)
- `gws drive move <form_id> --parent <pasta_id>` — mover pra pasta certa (Etapa 3.2)
- `gws forms link-sheet <form_id>` — linkar respostas (Etapa 3.4)
- `gws forms get-public-url <form_id>` — pegar URL viewform (Etapa 3.5)
````

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/docs/APIS-EXTERNAS.md
git commit -m "docs(apis): UAZAPI + NotebookLM + Google Forms (consumidos por /onboarding)"
```

---

### Task 14: Smoke test conversacional

**Files:**
- Create: `plugins/dna-operacional/skills/onboarding-cliente/tests/smoke.md`

- [ ] **Step 1: Criar smoke test documentado**

````markdown
# Smoke Test — onboarding-cliente

Teste manual conversacional. Roda 1× antes de cada release que mexe na skill.

## Setup

Cliente fictício:
- Nome: `Teste Smoke`
- WhatsApp principal: **número de teste do Flávio** (não cliente real!)
- E-mail: `flavio@ahoy.digital`
- Nicho: `teste`

CLAUDE.md do projeto de teste deve ter a seção `## Onboarding (cliente)` configurada com env vars válidas.

## Roteiro

1. Rodar `/onboarding Teste Smoke`
2. Skill pergunta WhatsApp principal → responder com **número de teste** (não cliente real)
3. Pergunta extras → vazio
4. Pergunta e-mail → `flavio@ahoy.digital`
5. Pergunta nicho → `teste`
6. Skill mostra confirmação → responder `s`
7. Aguardar Etapas 2-5 rodarem (~30-60s)

## Verificações

| Item | Como verificar |
|---|---|
| Shared Drive criado | Acessa Drive web → "Meus drives compartilhados" → existe `Teste Smoke — Ahoy` |
| 6 pastas padrão | Abre o Drive → vê `00 — Briefing/`, `01 — Estratégia/` etc com sub-pastas |
| Permissões | Settings do Drive → Flávio é organizer, cliente é fileOrganizer |
| Form criado | Em `00 — Briefing/` → existe `Briefing — Teste Smoke` |
| Sheet linkada | Em `00 — Briefing/` → existe `Briefing (respostas)` (vazia) |
| NotebookLM criado | https://notebooklm.google.com → existe `Teste Smoke — DNA` (vazio) |
| Grupo WhatsApp | WhatsApp do Flávio → existe grupo `Ahoy × Teste Smoke` com 3 membros |
| Mensagem boas-vindas | Lida no grupo, contém `form_url` e `drive_url` clicáveis |
| `cliente.json` | `data/clientes/teste-smoke/cliente.json` existe + bloco `onboarding` populado |
| `onboardings.csv` | `data/onboardings.csv` tem linha com `slug=teste-smoke` |

## Cleanup pós-teste

```bash
# Drive
gws drive shared-drive delete "$DRIVE_ID"

# NotebookLM
notebooklm delete "$NOTEBOOK_ID"

# Grupo WhatsApp
curl -X POST "$UAZAPI_URL/group/leave" \
  -H "token: $UAZAPI_TOKEN" \
  -d "{\"groupJid\": \"$GROUP_JID\"}"

# Cliente local
rm -rf data/clientes/teste-smoke/
# Remove linha do onboardings.csv manualmente
```

## Critério de pass

Todos 10 itens da tabela ✓. Cleanup ✓. Sem mensagens de erro no console.

## Smoke automático (futuro v0.5)

Substituir por script Python que valida via APIs sem depender de inspeção visual.
````

- [ ] **Step 2: Commit**

```bash
git add plugins/dna-operacional/skills/onboarding-cliente/tests/smoke.md
git commit -m "test(skill): smoke test conversacional pra onboarding-cliente"
```

---

### Task 15: Audit Spec §7.2 — sanitização

Esta task é cumulativa: roda no fim de tudo, antes do release.

- [ ] **Step 1: Audit grep de IDs pessoais**

```bash
cd /Users/flavioahoy/Documents/projects/dna-operacional

# Pattern 1: números pessoais hardcoded
grep -rE "5511936187040|5581998385073" plugins/dna-operacional/skills/onboarding-cliente/ plugins/dna-operacional/templates/onboarding-folder-structure.md plugins/dna-operacional/templates/briefing-form-template.md plugins/dna-operacional/commands/onboarding.md
```

Expected: zero matches dentro de skill/templates (só dentro de docs/JORNADAS.md como **exemplo** explícito é ok). Se acharem em SKILL.md ou commands, **substituir por placeholder** `<55XX9XXXXXXXX>`.

- [ ] **Step 2: Audit emails pessoais**

```bash
grep -rE "contato@ahoydigital\.ag|fran@ahoydigital\.ag|pedrocaracciolov@gmail\.com|leonardo\.ahoydigital@gmail\.com|isabelleahoymidia@gmail\.com|pedrocaracciolo\.ahoydigital@gmail\.com" plugins/dna-operacional/skills/onboarding-cliente/ plugins/dna-operacional/commands/onboarding.md plugins/dna-operacional/templates/onboarding-folder-structure.md plugins/dna-operacional/templates/briefing-form-template.md
```

Expected: zero matches (substituir por `<email-equipe>` ou comentário "ex:"). Os e-mails reais ficam apenas no `CLAUDE.md` do projeto do user, NUNCA no plugin.

- [ ] **Step 3: Audit URLs de Drive/Form/Notebook reais**

```bash
grep -rE "drive\.google\.com/drive/folders/0A|docs\.google\.com/forms/d/e/1[A-Za-z0-9_-]{40,}|notebooklm\.google\.com/notebook/[a-f0-9]{8}" plugins/dna-operacional/skills/onboarding-cliente/
```

Expected: zero matches (URLs reais nunca entram no plugin — só placeholders tipo `<form_url>`, `0AB...XYZ`, etc).

- [ ] **Step 3.5: Audit token UAZAPI**

```bash
grep -rE "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}" plugins/dna-operacional/
```

Expected: zero matches que sejam tokens reais. Se aparecer UUID que **não** seja exemplo claramente fake (`<uuid-da-instância>`, `xxxxxxxx-xxxx-...`), é vazamento de credencial — substituir IMEDIATAMENTE e rotacionar token no painel UAZAPI.

- [ ] **Step 4: Audit SQL inline**

```bash
grep -rE "SELECT |INSERT |UPDATE |DELETE " plugins/dna-operacional/skills/onboarding-cliente/
```

Expected: zero matches (skill não toca em storage layer).

- [ ] **Step 5: Se algum dos 4 audits achar algo → fix imediato + re-run**

- [ ] **Step 6: Commit dos fixes (se houver)**

```bash
git add plugins/dna-operacional/
git commit -m "audit(spec-7.2): sanitização final de IDs pessoais em onboarding-cliente"
```

---

### Task 16: CHANGELOG + final commit

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Adicionar entry v0.4.0 no topo**

````markdown
## v0.4.0 — Onboarding de Cliente (2026-05-07)

### Adicionado

- **`/onboarding`** — comando que orquestra ritual de boas-vindas de cliente novo. Cria em ordem:
  - Shared Drive `<Cliente> — Ahoy` com 6 pastas padrão
  - Google Form de briefing duplicado de template + Sheet linkada
  - NotebookLM `<Cliente> — DNA` (vazio, equipe popula depois)
  - Grupo WhatsApp via UAZAPI (cliente + Bruna + equipe Ahoy)
  - Mensagem de boas-vindas da Bruna com links clicáveis
- Skill bundled `skills/onboarding-cliente/` (SKILL.md + 2 references + smoke test)
- Templates `templates/onboarding-folder-structure.md` e `templates/briefing-form-template.md`
- Documentação UAZAPI + NotebookLM + Google Forms em `docs/APIS-EXTERNAS.md`
- Jornada de onboarding em `docs/JORNADAS.md`

### Modificado

- `cliente.json` ganha bloco opcional `onboarding` (retrocompatível)
- `/dna` menu mostra `/onboarding` na seção CLIENTE
- Jornada CLIENTE agora começa com `/onboarding`, não com `/setup-projeto`

### Pré-requisitos novos

Ver `docs/JORNADAS.md#jornada-onboarding-de-cliente` — bloco `## Onboarding (cliente)` no CLAUDE.md do projeto + env var `UAZAPI_TOKEN_BRUNA`.

### Fora do escopo (entra em v0.5)

- Hook que dispara quando briefing é preenchido (popula NotebookLM + muda status)
- `/onboarding --resume <slug>` pra retomar onboarding parcial
- Smoke test automatizado
````

- [ ] **Step 2: Commit final**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): release v0.4.0 — onboarding de cliente"
```

- [ ] **Step 3: NÃO criar tag ainda**

Tag `v0.4.0` só depois do user rodar smoke test e aprovar. Esperar comando explícito.

---

## Sequência de execução recomendada

1. **Chunk 1** (Tasks 1-5): Fundação — versão, templates, schema, skill skeleton + Etapa 1
2. Verificar no console: `git log --oneline | head -5` mostra 5 commits recentes
3. **Chunk 2** (Tasks 6-8): Integrações — etapas detalhadas + mensagens
4. **Chunk 3** (Tasks 9-16): Wrapper, menu, docs, smoke, audit, changelog

Cada chunk passa por review antes de avançar (ver Plan Review Loop da skill writing-plans).

## Riscos conhecidos

| Risco | Mitigação |
|---|---|
| `gws-cli` não suportar `forms copy` ou `shared-drive create` exatos | Validar em pré-check (Etapa 0). Se falta, instruir user a updatar `gws` ou abortar antes. |
| UAZAPI rejeitar criação de grupo se número não tem WA | Detectar erro `participant_not_found` e mensagem amigável (Gotcha #4 da Etapa 5). |
| Cliente não aceitar e-mail Drive | E-mail Drive é informativo (`--notify=false`). Cliente clica no link da mensagem WhatsApp. |
| NotebookLM CLI mudar API entre releases | Pinar versão em `requirements.txt` se virar dependência permanente do plugin (decisão fora do escopo deste plan). |
| Token UAZAPI vazar via skill | Skill nunca loga `$UAZAPI_TOKEN`. `set +x` antes de qualquer curl com token. |

## Definition of Done

- [ ] Todas 16 tasks completed (checkboxes marcados)
- [ ] Smoke test passou em ambiente real (Flávio rodou)
- [ ] Audit Spec §7.2 zero matches
- [ ] CHANGELOG atualizado
- [ ] `plugin.json.version === 0.4.0`
- [ ] User aprovou pra criar tag `v0.4.0` (passo manual fora deste plan)
