# APIs Externas — Guia de Setup

Skills do plugin dependem de APIs/serviços externos pra funcionar. Este doc mostra **passo-a-passo** como obter e configurar cada uma.

**Quando precisa:** antes de rodar skills que dependem das respectivas APIs. Cada skill faz pré-check no início — se falta config, aponta pra seção daqui.

## Visão geral

| Serviço | Skills que usam | Custo |
|---|---|---|
| [Apify](#apify) | `/pesquisa-diaria`, `/pesquisa-concorrentes`, `/analisar-video`, `/raio-x-ads-concorrentes` (v0.2) | Free tier $5/mês — suficiente pra uso pessoal |
| [Supabase](#supabase) | `/analista-conteudo` (obrigatório), storage backend (opcional) | Free tier generoso (500MB DB) |
| [Modal](#modal) | `/analisar-video` (transcrição Whisper) | Free tier $30/mês |
| [Google Sheets](#google-sheets) | Storage backend (opcional) | Grátis |
| [`/schedule` Anthropic](#schedule-anthropic) | Agendamento `/pesquisa-diaria` | Paga tokens por execução |
| [GitHub Actions](#github-actions) | Agendamento alternativo | Grátis em repos públicos |
| [launchd (Mac)](#launchd-mac) | Agendamento local Mac-only | Grátis |

---

## Apify

Usado pra scraping Instagram, TikTok, X (Twitter), Reddit, portais BR.

### 1. Criar conta

1. Acessa https://console.apify.com/sign-up
2. Cadastra com email + senha OU login com Google/GitHub
3. Confirma email

### 2. Obter API token

1. Logado, vai em https://console.apify.com/account#/integrations
2. Copia o **Personal API token** (começa com `apify_api_...`)

### 3. Configurar no sistema

**Opção A — variável de ambiente permanente (recomendado):**

Adiciona em `~/.zshrc` (ou `~/.bashrc` se usa bash):

```bash
export APIFY_TOKEN='apify_api_XXXXXXXXXXXXXXXXXXXXXXXX'
```

Reload:
```bash
source ~/.zshrc
```

Verifica:
```bash
echo $APIFY_TOKEN
# deve mostrar o token
```

**Opção B — .env do projeto (alternativa):**

Criar `.env` no root do projeto:
```
APIFY_TOKEN=apify_api_XXXXXXXXXXXXXXXXXXXXXXXX
```

Adiciona `.env` no `.gitignore` do projeto pra não commitar.

### 4. Custo esperado

- Free tier: $5/mês de créditos (suficiente pra uso pessoal diário)
- Pay-as-you-go acima disso (~$0.25 por 1000 items scraped)
- Ver uso atual em https://console.apify.com/billing

### 5. Skills que usam

- `/pesquisa-diaria` — scraping X, Reddit BR, portais BR, GitHub Trending
- `/pesquisa-concorrentes` — scraping Instagram profiles
- `/analisar-video` — download de vídeo (Instagram, TikTok) antes da transcrição
- `/raio-x-ads-concorrentes` — requer também skill `/coletar-anuncios` (v0.2+) pra popular ad_library

---

## Supabase

Banco Postgres gerenciado. **Obrigatório** pra `/analista-conteudo` (que roda SQL complexo). Opcional como backend de storage layer.

### 1. Criar projeto

1. Acessa https://supabase.com/sign-up
2. Cria conta + confirma email
3. Clica "New project"
4. Escolhe:
   - Name: `dna-operacional-data` (ou nome do teu projeto)
   - Database password: **guarda bem** (precisa pra conectar depois)
   - Region: `South America (São Paulo)` (mais próximo pra PT-BR)
   - Plan: Free (500MB DB, generoso)
5. Aguarda provisioning (~2 min)

### 2. Obter project_id

1. Logado no projeto, vai em **Settings** (ícone de engrenagem) → **General**
2. Copia **Reference ID** (formato `xxxxxxxxxxxxxxxxxxxxx`, 20 chars)

### 3. Configurar no CLAUDE.md do teu projeto

No `CLAUDE.md` do teu projeto de trabalho, adiciona:

```markdown
## Storage Backend: supabase

- project_id: <cola-teu-reference-id-aqui>
```

### 4. Aplicar migration

No Supabase Dashboard → **SQL Editor** → **New query**:

1. Cola o conteúdo de `~/.claude/plugins/cache/dna-operacional-marketplace/dna-operacional/0.1.0-alpha.8/templates/migrations-v0.1.0.sql` (path pode mudar com versão)
2. Clica **Run**
3. Confirma que 7 tabelas foram criadas (ver em **Database → Tables**): `competitors`, `competitor_posts`, `content_pipeline`, `my_content`, `ad_library`, `adaptive_models`, `generated_scripts`

### 5. Conectar MCP Supabase no Claude Code

Pra skills acessarem via MCP:

1. Instala: `/plugin marketplace add anthropic/mcp-supabase` (se existe) OU segue https://modelcontextprotocol.io/servers/supabase
2. Autoriza acesso ao teu projeto Supabase (OAuth)
3. Verifica: chama `mcp__supabase__list_tables` — deve listar as 7 tabelas

### 6. Custo

- Free tier: 500MB storage, 50MB egress/mês, 50k MAU
- Mais que suficiente pra uso pessoal

---

## Modal

Serverless Python/ML platform. Usado pra rodar Whisper (transcrição áudio/vídeo) em GPU.

### 1. Criar conta

1. Acessa https://modal.com/signup
2. Cadastra + confirma email

### 2. Instalar CLI

```bash
pip install modal
modal setup  # abre browser pra OAuth
```

Verifica:
```bash
modal token list
# deve mostrar teu token ativo
```

### 3. Deploy app Whisper (one-time)

Se não tem app Modal Whisper ainda:

1. Pega template em https://github.com/modal-labs/examples/blob/main/06_gpu_and_ml/openai_whisper.py
2. Customiza (ou deixa default)
3. `modal deploy openai_whisper.py`
4. Copia a URL/app name gerada (formato `<username>/whisper-app`)

### 4. Configurar no CLAUDE.md do projeto

```markdown
## Modal App

- app_name: <teu-username>/whisper-app
```

Skill `/analisar-video` lê daí e invoca.

### 5. Custo

- Free tier: $30/mês de créditos
- Whisper large-v3 roda em ~5s por minuto de áudio em GPU T4
- ~100h de áudio/mês dentro do free tier

---

## Google Sheets

Backend alternativo do storage layer. Pra quem prefere planilhas vs SQL.

### 1. Criar planilha template

Segue guia completo em `templates/sheets-master-template.md` do plugin. Resumo:

1. Acessa https://sheets.new
2. Renomeia pra `dna-operacional-data`
3. Cria 7 abas com headers específicos (tab-separated copy-paste no template)
4. Copia ID da URL (formato `1aBc123XYZ...` entre `/d/` e `/edit`)

### 2. Configurar no CLAUDE.md do projeto

```markdown
## Storage Backend: sheets

- spreadsheet_id: 1aBc123XYZ...
```

### 3. Instalar gws CLI + autenticar

```bash
brew install gws-cli  # ou pip install gws-cli
gws auth login        # abre browser pra OAuth Google
```

Verifica:
```bash
gws auth status
# deve mostrar "Logged in as <teu-email>"
```

### 4. Limites

- 60 requisições/minuto por user
- ~10k rows por aba (soft limit — acima fica lento)
- Migrar pra Supabase via `/dna migrar-storage` (v0.2+) quando crescer

---

## `/schedule` Anthropic

Agendamento nativo do Claude Code. **Zero infra, mas paga tokens por execução.**

### 1. Verificar disponibilidade

Dentro do Claude Code:
```
/schedule --help
```

Se o comando existe e mostra opções: disponível.
Se não: precisa atualizar CLI (`npm install -g @anthropic-ai/claude-code@latest`).

### 2. Agendar `/pesquisa-diaria`

```
/schedule diariamente 7:00 BRT /pesquisa-diaria
```

Verifica:
```
/schedule list
```

### 3. Custo estimado

Ver `docs/SPIKE-TOKENS.md` pra medição real. Estimativa preliminar:
- Sonnet 4.6: ~$0.60-1.20/execução × 30 dias = $18-36/mês
- Opus 4.6: ~$3-6/execução × 30 dias = $90-180/mês

### 4. Parar agendamento

```
/schedule remove <id>
```

---

## GitHub Actions

Agendamento grátis em CI. **Recomendado se custo do `/schedule` passar de $30/mês.**

### 1. Clonar teu projeto no GitHub

Se projeto ainda não tá no GitHub:
```bash
cd <teu-projeto>
gh repo create <teu-user>/<nome-projeto> --public --source=.
```

### 2. Criar workflow

Cria `.github/workflows/pesquisa-diaria.yml`:

```yaml
name: Pesquisa Diária BR

on:
  schedule:
    - cron: '0 10 * * *'  # 07:00 BRT (10:00 UTC)
  workflow_dispatch:  # permite rodar manual

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run pesquisa-diaria
        env:
          APIFY_TOKEN: ${{ secrets.APIFY_TOKEN }}
          SUPABASE_PROJECT_ID: ${{ secrets.SUPABASE_PROJECT_ID }}
        run: |
          # Instruções específicas de como rodar a skill em batch
          # via Claude Code CLI ou script customizado
          # (a implementação depende de como integrar Claude Code em CI)
          echo "TODO: adaptar pra teu workflow"
```

### 3. Configurar secrets

No GitHub do repo: **Settings → Secrets and variables → Actions → New repository secret**

Adiciona:
- `APIFY_TOKEN` — teu token Apify
- `SUPABASE_PROJECT_ID` — se usas Supabase

### 4. Custo

- **Grátis** em repos públicos (ilimitado)
- 2000 min/mês free em repos privados

### 5. Limitação atual

Claude Code CLI em CI ainda é follow-up (requer auth via API key). Documentação completa chega em v0.2+.

---

## launchd (Mac local)

Agendamento local no Mac. Só roda com Mac ligado. **Zero custo, zero infra remota.**

### 1. Criar plist

Cria `~/Library/LaunchAgents/com.ahoydig.pesquisa-diaria.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ahoydig.pesquisa-diaria</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd ~/teu-projeto && claude --print "/pesquisa-diaria" >> ~/logs/pesquisa-diaria.log 2>&1</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
```

### 2. Carregar

```bash
launchctl load ~/Library/LaunchAgents/com.ahoydig.pesquisa-diaria.plist
```

Verifica:
```bash
launchctl list | grep pesquisa
```

### 3. Testar manualmente

```bash
launchctl start com.ahoydig.pesquisa-diaria
tail -f ~/logs/pesquisa-diaria.log
```

### 4. Desligar

```bash
launchctl unload ~/Library/LaunchAgents/com.ahoydig.pesquisa-diaria.plist
```

### 5. Limitação

- **Só roda se Mac tá ligado** — se desliga/hiberna, skip silencioso
- Ideal pra quem tem Mac sempre ligado ou pra teste

---

## FAQ

**Não tenho dinheiro pra Apify — o que fazer?**
Free tier ($5/mês) cobre uso pessoal. Se passar: pausar `/pesquisa-diaria` automática e rodar manual quando precisa.

**Quero usar só Markdown local (zero APIs) — o que perco?**
`/pesquisa-diaria` e `/pesquisa-concorrentes` ainda precisam Apify (scraping). O resto do plugin funciona 100% em MD local (Plans 1-5 entregaram storage layer 3 backends).

**Posso usar chave Apify compartilhada?**
Não. Cada aluno deve ter a sua — senão quota compartilhada esgota rápido.

**Como sei se um token vazou?**
Apify/Modal/Supabase permitem **revogar + gerar novo token** a qualquer momento via dashboard. Revoga se suspeita.
