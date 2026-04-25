# Deploy via Netlify

## Novo Projeto

```bash
# 1. Git
git init && git add . && git commit -m "feat: landing page"

# 2. GitHub (repo privado)
gh repo create nome --private --source=. --push

# 3. Netlify
netlify sites:create --name nome
netlify env:set CHAVE "valor"  # env vars
netlify deploy --prod

# 4. Redirect raiz (netlify.toml)
[[redirects]]
  from = "/"
  to = "/pasta-da-pagina/"
  status = 302
  force = true
```

## Atualizacao

```bash
git add . && git commit -m "descricao" && git push
netlify deploy --prod
```

## netlify.toml

```toml
[build]
  publish = "."
  functions = "netlify/functions"

[dev]
  publish = "."
  functions = "netlify/functions"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/*.{css,js,woff2,svg}"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

## Custom Domain
Netlify Dashboard: Site configuration > Domain management > Add custom domain

## Servidor Local
Exclusivamente `netlify dev`. Verificar portas antes:

```bash
lsof -i :8888 -i :3999 2>/dev/null | grep node
kill $(lsof -ti :8888) 2>/dev/null
netlify dev
```
