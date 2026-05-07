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
