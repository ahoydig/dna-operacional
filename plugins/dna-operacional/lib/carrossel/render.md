# Render Harness Determinístico

Procedimento FIXO de render (idêntico para todas as teses — isola a variável no torneio).

## Passos

1. Salvar o HTML do slide no diretório de trabalho, linkando `base.css` (copiar `${CLAUDE_PLUGIN_ROOT}/lib/carrossel/base.css` pra `./base.css`).
2. Copiar fontes locais pra `./fonts/` (ver `references/carrossel-lab/fonts-config.md`); detectar LOCAL vs FALLBACK.
3. **Rodar QA lint ANTES de renderizar:** `python3 ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/qa_lint.py <slide.html>`. Se sair com violações (exit≠0), corrigir o HTML e repetir. **Não renderiza slide que não passa no lint.**
4. Servir via `python3 -m http.server <porta livre>`.
5. Abrir via Playwright no viewport do formato (4:5 = 1080×1350; 3:4 = 1080×1440; 1:1 = 1080×1080).
6. Aguardar 3s pras fontes carregarem.
7. Capturar PNG do slide.
8. Para overlay transparente: `omitBackground: true`.
9. **Fechar o browser após cada slide.**

## Auto-review visual (reduzido)

O QA lint já cobriu o objetivo (contraste, tamanho, object-fit, escala). O auto-review humano/visual foca só no subjetivo: hierarquia, respiro, "tá bonito?", órfã, PT-BR natural. Ler cada PNG via `Read`.

## Playground de ajuste fino (`playground.html`)

Depois de renderizar (e antes do loop final), dá pra **ajustar cada elemento ao vivo** num playground em vez de editar o JSON no escuro. Ele carrega os `slides/NN.html` reais num iframe (1:1 com o PNG) e expõe sliders por slide: tamanho de headline/sub/quote, largura do hero, tamanho+posição da `figure`/`aux` da capa, escuridão do bg (scrim), cor do accent. Botão **"Copiar carrossel.json"** cospe os valores ajustados.

```bash
cp ${CLAUDE_PLUGIN_ROOT}/lib/carrossel/playground.html <workdir>/playground.html
cd <workdir> && python3 -m http.server 8777 &     # serve o workdir (iframe same-origin + fontes)
open http://localhost:8777/playground.html         # abre no navegador do user
```

Fluxo: user mexe nos sliders → clica "Copiar carrossel.json" → cola de volta → re-render → loop. O playground reflete o render real porque usa o MESMO `base.css`/fontes/HTML. Útil principalmente pra **validar a distribuição da capa** (respiro entre headline e sub, tamanho dos heróis).
