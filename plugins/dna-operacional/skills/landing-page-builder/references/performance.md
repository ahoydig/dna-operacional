# Performance

## Metas
- PageSpeed: 90+
- CLS: < 0.1
- TBT: < 200ms
- LCP: < 2.5s

## Imagens (Netlify CDN)

```html
<img
  src="/.netlify/images?url=/images/foto.jpg&w=600&q=80"
  width="600" height="400"
  loading="lazy"
  alt="Descricao"
>
```

- Hero: `loading="eager" fetchpriority="high"`
- Resto: `loading="lazy"`
- width/height SEMPRE numericos (nunca "auto" ou "100%")
- Formato CDN obrigatorio: `/.netlify/images?url={URL}&w={WIDTH}&q=80`

## Fontes

- Sincronas com preconnect + display=swap
- Max 3 pesos por familia
- Nunca async via media="print"

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

## Scripts

- Main: `<script src="script.js" defer></script>` no head
- Pesados: Dynamic Import + IntersectionObserver
- Nunca `<script src="three.js">` direto no HTML

## CSS

- Sincrono durante desenvolvimento
- Critical CSS inline + async so na otimizacao final

## Nunca Fazer

1. opacity:0 no hero (LCP invisivel)
2. data-aos no hero (conteudo invisivel + CLS)
3. CSS async sem critical inline (CLS 0.3-0.7)
4. Google Fonts async via media="print"
5. height="auto" em imagens (sem reserva de espaco)
6. Import estatico de libs pesadas
7. AOS sem disableMutationObserver (CLS 0.7+)
