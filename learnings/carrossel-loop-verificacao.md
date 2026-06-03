# Carrossel: loop de verificação visual obrigatório (gerar→render→ler→corrigir)

**O que aprendi:** O Flávio pediu explicitamente um "loop de verificação para ajuste" depois que eu entreguei slides com seta errada, anotação sobreposta, texto atrás do personagem. Vários defeitos só apareceram quando EU LI o PNG renderizado — não dá pra confiar no HTML "no escuro".

**Por quê:** HTML que parece certo no código produz colisões reais no render (position:absolute sobre texto, screenshot cortando, fonte fora de proporção). Sem olhar o pixel final, entrega bug.

**Como aplicar (passo obrigatório da skill):**
- Ciclo: gerar HTML → renderizar PNG (Playwright) → **Read de CADA PNG** → listar defeitos (sobreposição, alinhamento/eixo, fonte proporcional, anotação fora do texto, contraste, texto cortado) → corrigir no gerador → re-renderizar → repetir até passar.
- Formalizado como **agente revisor automático + auto-correção** (decisão do Flávio): a skill renderiza, um agente compara cada slide com os virais de referência (MANIFESTO-DIAGRAMACAO.md), corrige sozinho e re-renderiza até bater, só então mostra ao user.
- Defeitos recorrentes a checar: anotação handwritten sobre texto/borda; personagem sobre subtítulo; palavra accent menor que o display; ícone/logo pequeno demais; livro/screenshot escondido. [[carrossel-clonar-geometria]] [[carrossel-ativos-reais]]
