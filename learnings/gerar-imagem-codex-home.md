# gerar-imagem: o token do Codex vive em $CODEX_HOME (não ~/.codex) neste ambiente

**O que aprendi:** A skill `gerar-imagem` (`~/.claude/skills/gerar-imagem/scripts/gen.py`) lia o token
fixo de `~/.codex/auth.json`, mas neste ambiente o Codex é gerenciado pelo **orca** e o login fica em
**`$CODEX_HOME/auth.json`** (`~/Library/Application Support/orca/codex-runtime-home/home/auth.json`).
Lendo o arquivo errado dá `400 image_generation tool not found` (token de texto válido mas sem o tool)
ou `401 token_revoked`. **Fix aplicado:** `gen.py` agora resolve `AUTH_PATH` respeitando `$CODEX_HOME`
com fallback pra `~/.codex`.

**Por quê:** No meio da sessão a geração parou. Diagnóstico: texto funcionava no `gpt-5.4`, mas o tool
de imagem era rejeitado. Era path de auth. Detalhe traiçoeiro: `codex login --device-auth` grava em
`$CODEX_HOME`, **não** atualiza `~/.codex`, e o runtime do orca **rotaciona o token sob demanda** (JIT)
— o `access_token` parado no arquivo pode estar invalidado mesmo "fresco". O primeiro re-login deu token
já invalidado; **o segundo login** resolveu (token de 0 min funcionou na hora).

**Como aplicar:**
- Se `gerar-imagem` falhar com 401/`token_revoked`/`token_invalidated`: conferir `$CODEX_HOME`, pedir
  `!codex login --device-auth` (pode precisar **2x**), e testar logo em seguida (token rotaciona rápido,
  usar fresco). `codex login status` / `codex doctor` mostram o auth ativo e o `CODEX_HOME` real.
- Sondar HOST_MODEL aceito: `gpt-5.4`/`gpt-5.5` ok pra conta ChatGPT; os `*-codex` foram **bloqueados**.
- A skill é **sempre via Codex** (preferência do Flávio), nunca OPENAI_API_KEY.
