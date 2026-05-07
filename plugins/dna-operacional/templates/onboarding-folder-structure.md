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
