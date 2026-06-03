# Crankdat ficou órfã no rebuild do base.css (declarada, nunca aplicada)

**O que aprendi:** No rebuild v2 do `base.css` do carrossel-lab, troquei o sistema tipográfico (Nofex display + Instrument Serif na palavra-chave + JetBrains mono) e, no processo, removi a variável `--font-accent: Crankdat` que existia no v1. O `@font-face` da Crankdat continuou declarado em todo slide, mas NENHUMA classe a aplicava — fonte carregada e nunca usada. O Flávio (autor da fonte) percebeu na hora que ela sumiu.

**Por quê:** Reescrever um sistema tipográfico do zero faz esquecer papéis secundários. `@font-face` declarado ≠ fonte usada. Não foi legibilidade — foi omissão.

**Como aplicar:** Crankdat é a fonte autoral do Flávio e tem personalidade de marca (traço marker/brush, energia) — papel ideal de ACCENT. Sempre incluí-la como `--font-accent` e aplicá-la em: kicker/handle/motifs + comentários/labels rotacionados (uso original na skill). Ao reescrever qualquer sistema de design dele, verificar que toda fonte declarada tem uma classe que a usa (senão é peso morto + perda de identidade). [[carrossel-densidade]]
