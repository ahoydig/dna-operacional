# Carrossel: buscar ativo REAL e usar como referência > gerar do nada

**O que aprendi:** O Flávio ficou frustrado ("ficou uma bosta kkk") quando gerei do zero: o Hormozi saiu careca (ele não é), os livros eram genéricos (não os dele), o logo do Claude era um desenho meu ruim. A correção que destravou: BAIXAR imagens reais (foto real do Hormozi, capas reais dos 3 livros $100M, PNG oficial do logo Claude) e usar a foto real como REFERÊNCIA image-to-image no `gerar-imagem` (-i). Aí o pixel art saiu fiel.

**Por quê:** gpt-image gera "uma pessoa genérica" se você só descreve. Com `-i foto.jpg` ele preserva identidade. E logo/capas de produtos têm versão oficial — desenhar ou inventar fica amador na hora.

**Como aplicar (pipeline de ativos da skill de carrossel):**
1. **Pessoa real** (criador, celebridade citada) → baixar foto real → `gerar-imagem -i foto.jpg` pra pixel art/estilização fiel.
2. **Logos de produto/marca** → baixar PNG oficial (brandfetch, wikimedia, site oficial), nunca desenhar.
3. **Capas de livro/produto** → baixar real (Amazon/site oficial), recortar fundo.
4. **Screenshots de UI** → capturar real; se não der, forjar réplica fiel em HTML→PNG (ex: telas do Claude.ai em PT-BR).
5. **Background da capa/CTA** → **foto do PRÓPRIO criador** tratada/escurecida (overlay rgba 0.55-0.72), igual noevarner usa foto dele. Na skill genérica: pedir/usar foto do usuário.
6. Lição-mãe: **ativo real como referência > gerar do nada.** [[carrossel-clonar-geometria]] [[carrossel-loop-verificacao]]
