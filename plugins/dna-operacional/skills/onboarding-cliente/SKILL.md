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
